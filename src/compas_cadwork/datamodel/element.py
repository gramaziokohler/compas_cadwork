from __future__ import annotations

from dataclasses import dataclass
from enum import auto
from enum import Enum
from typing import Generator

from compas.geometry import Frame
from compas.geometry import Vector
from compas.geometry import Point

import cadwork  # noqa: F401
from utility_controller import get_language
from element_controller import get_element_type_description
from element_controller import get_active_identifiable_element_ids
from geometry_controller import get_p1
from geometry_controller import get_xl
from geometry_controller import get_yl
from geometry_controller import get_length
from geometry_controller import get_height
from geometry_controller import get_width


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
    def frame(self) -> Frame:
        p1 = Point(*get_p1(self.id))
        x_axis = Vector(*get_xl(self.id))
        y_axis = Vector(*get_yl(self.id))
        return Frame(p1, x_axis, y_axis)

    @property
    def width(self) -> float:
        return get_width(self.id)

    @property
    def height(self) -> float:
        return get_height(self.id)

    @property
    def length(self) -> float:
        return get_length(self.id)

    @classmethod
    def from_id(cls, element_id: int) -> Element:
        """Returns an Element object for the CADwork Element with the given ID"""
        type_description = get_element_type_description(element_id)
        return Element(element_id, LOCAL_TYPE_MAP[type_description])

    @classmethod
    def from_selection(cls) -> Generator[Element]:
        """Returns a generator containing Element objects for all currently activated Elements"""
        return (Element.from_id(e_id) for e_id in get_active_identifiable_element_ids())

    @staticmethod
    def test_func():
        print("test func updated again!")


    @staticmethod
    def test_func2():
        print("test func2 updated again!")


    @staticmethod
    def test_func3():
        print("test func3 updated again!")


    @staticmethod
    def test_func4():
        print("test func4 updated again!")


    @staticmethod
    def test_func5():
        print("test func4 updated again!")
