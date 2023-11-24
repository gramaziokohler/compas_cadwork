from __future__ import annotations

from dataclasses import dataclass
from enum import auto
from enum import Enum
from typing import Generator

from compas.geometry import Frame
from compas.geometry import Vector
from compas.geometry import Point

import cadwork  # noqa: F401
from attribute_controller import get_subgroup
from attribute_controller import get_group
from attribute_controller import get_name
from attribute_controller import get_element_grouping_type
from attribute_controller import get_element_type
from utility_controller import get_language
from element_controller import get_element_type_description
from element_controller import get_active_identifiable_element_ids
from element_controller import get_element_cadwork_guid
from geometry_controller import get_p1
from geometry_controller import get_xl
from geometry_controller import get_yl
from geometry_controller import get_length
from geometry_controller import get_height
from geometry_controller import get_width
from bim_controller import get_ifc_guid
from bim_controller import get_ifc_base64_guid


class StrEnum(str, Enum):
    """Why do *I* have to do this?"""
    pass


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
    "de":{
        "Stab": ElementType.BEAM,
        "Platte": ElementType.PLATE,
        "Achse": ElementType.SHAFT,
        "Linie": ElementType.LINE,
        "Installation rechteckig": ElementType.INSTALLATION_STRAIGHT,
        "Fläche": ElementType.SURFACE,
        "Installation rund": ElementType.INSTALLATION_ROUND
    },
    "en":{
        "Beam": ElementType.BEAM,
        "Plate": ElementType.PLATE,
    },
}


LOCAL_TYPE_MAP = ELEMENT_TYPE_MAP[get_language()]


@dataclass
class Element:
    """Represents a CADwork Element"""
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
            # TODO: get to the bottom of this, sometimes one of the axes comes back as [0,0,0] in the meantime just don't crash
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
        return get_element_type(self.id).is_framed_wall()

    @classmethod
    def from_id(cls, element_id: int) -> Element:
        """Returns an Element object for the CADwork Element with the given ID"""
        type_description = get_element_type_description(element_id)
        try:
            type_ = LOCAL_TYPE_MAP[type_description]
        except KeyError:
            type_ = ElementType.OTHER
        return Element(element_id, type_)

    @classmethod
    def from_selection(cls) -> Generator[Element]:
        """Returns a generator containing Element objects for all currently activated Elements"""
        return (Element.from_id(e_id) for e_id in get_active_identifiable_element_ids())

