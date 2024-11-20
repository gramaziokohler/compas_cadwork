from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Generator
from typing import List
from typing import Optional

import attribute_controller as ac
import bim_controller as bc
import cadwork  # noqa: F401
import element_controller as ec
import geometry_controller as gc
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector

from compas_cadwork.conversions import point_to_compas
from compas_cadwork.conversions import vector_to_cadwork

# These are used to identify instruction elements which were added to the cadwork file by compas_cadwork.
ATTR_INSTRUCTION_ID = 666


class ElementGroupingType(IntEnum):
    """CADWork Element Grouping Type

    Attributes
    ----------
    GROUP
        Elements are grouped using group as the main grouping type.
    SUBGROUP
        Elements are grouped using subgroup as the main grouping type.
    NONE
        Not setting is available.

    """

    GROUP = 1
    SUBGROUP = 2
    NONE = 3

    def to_cadwork(self):
        """Converts the ElementGroupingType to a cadwork compatible value.

        Returns
        -------
        int
            The cadwork compatible value of the ElementGroupingType
        """
        return cadwork.element_grouping_type(self.value)


@dataclass
class ElementGroup:
    """Represents a cadwork Element Group

    Parameters
    ----------
    name : str
        The name of the Element Group
    elements : list
        A list of Elements belonging to the Element Group

    Attributes
    ----------
    name : str
        The name of the Element Group
    elements : list
        A list of Elements belonging to the Element Group
    wall_frame_element : Element, optional
        The containing Element (often a wall element) which contains all other elements in the group. If any.
    ifc_guid : str
        The IFC GUID of the container element, often used to represent the whole group. See also: ifc_base64_guid

    """

    name: str
    elements: list = None
    wall_frame_element: Element = None

    def add_element(self, element: Element) -> None:
        """Adds an Element to the Element Group

        Parameters
        ----------
        element : Element
            The Element to add to the Element Group

        """
        if self.elements is None:
            self.elements = []
        self.elements.append(element)
        if element.is_wall or element.is_roof or element.is_floor:
            self.wall_frame_element = element

    @property
    def ifc_guid(self) -> str:
        if self.wall_frame_element is None:
            return None
        return self.wall_frame_element.ifc_base64_guid


@dataclass
class Element:
    """Represents a cadwork Element

    Parameters
    ----------
    id : int
        The ID of the Element

    Attributes
    ----------
    name : str
        The name of the Element
    frame : Frame
        The local coordinate system of the Element
    width : float
        The width of the Element
    height : float
        The height of the Element
    length : float
        The length of the Element
    group : str
        The group the Element belongs to. Either group or subgroup depending on the current grouping type.
    ifc_base64_guid : str
        The base64 IFC GUID of the Element
    cadwork_guid : str
        The cadwork GUID of the Element
    centerline : Line
        The centerline of the Element.
    midpoint : Point
        The midpoint of the Element's centerline.
    ifc_guid : str
        The IFC GUID of the Element. See also: ifc_base64_guid.
    is_beam : bool
        Whether the Element is a beam
    is_wall : bool
        Whether the Element is a framed wall i.e. container for all other elements in the building group.
    is_drilling : bool
        Whether the Element is a drilling hole
    is_roof : bool
        Whether the Element is a framed roof i.e. container for all other elements in the building group.
    is_floor : bool
        Whether the Element is a framed floor i.e. container for all other elements in the building group.

    """

    id: int

    @property
    def name(self) -> str:
        return ac.get_name(self.id)

    @property
    def frame(self) -> Frame:
        try:
            p1 = Point(*gc.get_p1(self.id))
            x_axis = Vector(*gc.get_xl(self.id))
            y_axis = Vector(*gc.get_yl(self.id))
            return Frame(p1, x_axis, y_axis)
        except ZeroDivisionError:
            # TODO: get to the bottom of this:
            # sometimes one of the axes comes back as [0,0,0] in the meantime just don't crash
            return Frame.worldXY()

    @property
    def width(self) -> float:
        return gc.get_width(self.id)

    @property
    def height(self) -> float:
        return gc.get_height(self.id)

    @property
    def length(self) -> float:
        return gc.get_length(self.id)

    @property
    def group(self) -> str:
        if ac.get_element_grouping_type() == cadwork.element_grouping_type.subgroup:
            return ac.get_subgroup(self.id)
        else:
            return ac.get_group(self.id)

    @property
    def ifc_base64_guid(self) -> str:
        return bc.get_ifc_base64_guid(self.id)

    @property
    def cadwork_guid(self) -> str:
        return ec.get_element_cadwork_guid(self.id)

    @property
    def centerline(self) -> Line:
        p1 = point_to_compas(gc.get_p1(self.id))
        p2 = point_to_compas(gc.get_p2(self.id))
        return Line(p1, p2)

    @property
    def midpoint(self) -> Point:
        return self.centerline.midpoint

    @property
    def ifc_guid(self) -> str:
        return bc.get_ifc_guid(self.id)

    @property
    def is_wall(self) -> bool:
        return ac.is_framed_wall(self.id)

    @property
    def is_roof(self) -> bool:
        return ac.is_framed_roof(self.id)

    @property
    def is_floor(self) -> bool:
        return ac.is_framed_floor(self.id)

    @property
    def is_linear_dimension(self) -> bool:
        type_ = ac.get_element_type(self.id)
        return type_.is_dimension()

    @property
    def is_drilling(self) -> bool:
        return ac.is_drilling(self.id)

    @property
    def is_instruction(self) -> bool:
        return ac.get_user_attribute(self.id, ATTR_INSTRUCTION_ID) != ""

    def is_beam(self) -> bool:
        type_ = ac.get_element_type(self.id)
        return type_.is_rectangular_beam()

    @classmethod
    def from_selection(cls) -> Generator[Element]:
        """Returns a generator containing Element objects for all currently activated Elements

        Returns
        -------
        Generator[Element]
            A generator containing Element objects for all currently activated Elements

        """
        return (Element(e_id) for e_id in ec.get_active_identifiable_element_ids())

    def set_attribute(self, name, value):
        """Sets an attribute on the Element

        Parameters
        ----------
        name : str
            The name of the attribute
        value : str
            The value of the attribute

        """
        ac.set_user_attribute([self.id], name, value)

    def remove_attribute(self, name):
        """Removes an attribute from the Element

        Parameters
        ----------
        name : str
            The name of the attribute

        """
        ac.delete_user_attribute([self.id], name)

    def set_is_instruction(self, value: bool, instruction_id: Optional[str] = None):
        """Sets the is_instruction attribute on the Element

        Parameters
        ----------
        value : bool
            If True, this Element will be flagged as an instruction element by setting the appropriate attribute.
            If False, the attribute will be removed.
        instruction_id : str
            The ID of the instruction. This is required when setting is_instruction to True.

        """
        if value and instruction_id is None:
            raise ValueError("Instruction ID must be provided when setting is_instruction to True")

        if value:
            self.set_attribute(ATTR_INSTRUCTION_ID, instruction_id)
        else:
            self.remove_attribute(ATTR_INSTRUCTION_ID)

    def get_instruction_id(self) -> Optional[str]:
        """Returns the instruction ID of the Element

        Returns
        -------
        str, optional
            The instruction ID of the Element

        """
        return ac.get_user_attribute(self.id, ATTR_INSTRUCTION_ID)

    def get_elements_in_contact(self) -> List[Element]:
        """Returns a list of elements in contact with the current element"""
        return [Element(e_id) for e_id in ec.get_elements_in_contact(self.id)]

    def remove(self):
        """Removes the Element from the cadwork file"""
        ec.delete_elements([self.id])

    def translate(self, vector: Vector) -> None:
        """Translates the Element by the given vector.

        Parameters
        ----------
        vector : Vector
            The vector by which to translate the Element

        """
        ec.move_element([self.id], vector_to_cadwork(vector))
