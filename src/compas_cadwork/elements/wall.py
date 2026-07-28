from __future__ import annotations

from typing import Literal
from typing import Self

import attribute_controller as ac
from compas.geometry import Frame
from compas.geometry import Polygon

from .element_type import ElementType
from .panel import Panel


class Wall(Panel[Literal[ElementType.WALL]]):
    """Wall element."""

    @classmethod
    def polygonal(cls, frame: Frame, outline: Polygon, thickness: float) -> Self:
        element = super().polygonal(frame, outline, thickness)
        ac.set_framed_wall([element.id])
        return element

    @classmethod
    def rectangular(cls, frame: Frame, length: float, width: float, thickness: float) -> Self:
        element = super().rectangular(frame, length, width, thickness)
        ac.set_framed_wall([element.id])
        return element
