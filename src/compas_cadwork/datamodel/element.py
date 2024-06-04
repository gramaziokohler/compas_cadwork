from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from enum import IntEnum
from enum import auto
from typing import Generator
from typing import Optional

import cadwork  # noqa: F401
from attribute_controller import delete_user_attribute
from attribute_controller import get_element_grouping_type
from attribute_controller import get_element_type
from attribute_controller import get_group
from attribute_controller import get_name
from attribute_controller import get_subgroup
from attribute_controller import get_user_attribute
from attribute_controller import is_drilling
from attribute_controller import is_framed_wall
from attribute_controller import set_user_attribute
from bim_controller import get_ifc_base64_guid
from bim_controller import get_ifc_guid
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from element_controller import delete_elements
from element_controller import get_active_identifiable_element_ids
from element_controller import get_element_cadwork_guid
from element_controller import get_element_type_description
from geometry_controller import get_height
from geometry_controller import get_length
from geometry_controller import get_p1
from geometry_controller import get_width
from geometry_controller import get_xl
from geometry_controller import get_yl
from utility_controller import get_language

# These are used to identify instruction elements which were added to the cadwork file by compas_cadwork.
ATTR_INSTRUCTION_ID = 666


class StrEnum(str, Enum):
    """Why do *I* have to do this?"""

    pass


class ElementGroupingType(IntEnum):
    """CADWork Element Grouping Type"""

    GROUP = 1
    SUBGROUP = 2
    NONE = 3

    def to_cadwork(self):
        return cadwork.element_grouping_type(self.value)


class ElementType(StrEnum):
    """CADWork Element type"""

    BEAM = auto()  # Stab
    PLATE = auto()  # Platte
    SURFACE = auto()
    SHAFT = auto()
    LINE = auto()
    INSTALLATION_ROUND = auto()
    INSTALLATION_STRAIGHT = auto()
    OTHER = auto()


ELEMENT_TYPE_MAP = {
    "de": {
        "Stab": ElementType.BEAM,
        "Platte": ElementType.PLATE,
        "Achse": ElementType.SHAFT,
        "Linie": ElementType.LINE,
        "Installation rechteckig": ElementType.INSTALLATION_STRAIGHT,
        "Fläche": ElementType.SURFACE,
        "Installation rund": ElementType.INSTALLATION_ROUND,
    },
    "en": {
        "Beam": ElementType.BEAM,
        "Plate": ElementType.PLATE,
    },
}


LOCAL_TYPE_MAP = ELEMENT_TYPE_MAP[get_language()]


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

    """

    name: str
    elements: list = None
    wall_frame_element: Element = None

    def add_element(self, element: Element):
        """Adds an Element to the Element Group

        Parameters
        ----------
        element : Element
            The Element to add to the Element Group

        """
        if self.elements is None:
            self.elements = []
        self.elements.append(element)
        if element.is_wall:
            self.wall_frame_element = element

    @property
    def ifc_guid(self):
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
    type : ElementType
        The type of the Element


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
    ifc_guid : str
        The IFC GUID of the Element. See also: ifc_base64_guid.
    is_wall : bool
        Whether the Element is a framed wall i.e. container for all other elements in the building group.
    is_drilling : bool
        Whether the Element is a drilling hole

    """

    id: int
    type: ElementType

    @property
    def name(self) -> str:
        return get_name(self.id)

    @property
    def frame(self) -> Frame:
        try:
            p1 = Point(*get_p1(self.id))
            x_axis = Vector(*get_xl(self.id))
            y_axis = Vector(*get_yl(self.id))
            return Frame(p1, x_axis, y_axis)
        except ZeroDivisionError:
            # TODO: get to the bottom of this:
            # sometimes one of the axes comes back as [0,0,0] in the meantime just don't crash
            return Frame.worldXY()

    @property
    def width(self) -> float:
        return get_width(self.id)

    @property
    def height(self) -> float:
        return get_height(self.id)

    @property
    def length(self) -> float:
        return get_length(self.id)

    @property
    def group(self) -> str:
        if get_element_grouping_type() == cadwork.element_grouping_type.subgroup:
            return get_subgroup(self.id)
        else:
            return get_group(self.id)

    @property
    def ifc_base64_guid(self) -> str:
        return get_ifc_base64_guid(self.id)

    @property
    def cadwork_guid(self) -> str:
        return get_element_cadwork_guid(self.id)

    @property
    def ifc_guid(self) -> str:
        return get_ifc_guid(self.id)

    @property
    def is_wall(self) -> bool:
        return is_framed_wall(self.id)

    @property
    def is_linear_dimension(self) -> bool:
        type_ = get_element_type(self.id)
        return type_.is_dimension()

    @property
    def is_drilling(self) -> bool:
        return is_drilling(self.id)

    @property
    def is_instruction(self) -> bool:
        return get_user_attribute(self.id, ATTR_INSTRUCTION_ID) != ""

    def is_beam(self) -> bool:
        type_ = get_element_type(self.id)
        return type_.is_rectangular_beam()

    @classmethod
    def from_id(cls, element_id: int) -> Element:
        """Returns an Element object for the cadwork Element with the given ID

        Parameters
        ----------
        element_id : int
            The ID of the Element

        Returns
        -------
        Element
            The Element object for the given ID

        """
        type_description = get_element_type_description(element_id)
        try:
            type_ = LOCAL_TYPE_MAP[type_description]
        except KeyError:
            type_ = ElementType.OTHER
        return Element(element_id, type_)

    @classmethod
    def from_selection(cls) -> Generator[Element]:
        """Returns a generator containing Element objects for all currently activated Elements

        Returns
        -------
        Generator[Element]
            A generator containing Element objects for all currently activated Elements

        """
        return (Element.from_id(e_id) for e_id in get_active_identifiable_element_ids())

    def set_attribute(self, name, value):
        """Sets an attribute on the Element

        Parameters
        ----------
        name : str
            The name of the attribute
        value : str
            The value of the attribute

        """
        set_user_attribute([self.id], name, value)

    def remove_attribute(self, name):
        """Removes an attribute from the Element

        Parameters
        ----------
        name : str
            The name of the attribute

        """
        delete_user_attribute([self.id], name)

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
        return get_user_attribute(self.id, ATTR_INSTRUCTION_ID)

    def remove(self):
        """Removes the Element from the cadwork file"""
        delete_elements([self.id])
