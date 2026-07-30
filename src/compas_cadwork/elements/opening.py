from __future__ import annotations

from typing import Literal

import attribute_controller as ac
from compas.geometry import Frame
from compas.geometry import Polygon
from typing_extensions import Self

from .element_type import ElementType
from .panel import Panel


class Opening(Panel[Literal[ElementType.OPENING]]):
    """Opening element."""

    @classmethod
    def polygonal(cls, frame: Frame, outline: Polygon, thickness: float) -> Self:
        element = super().polygonal(frame, outline, thickness)
        ac.set_opening([element.id])
        return element

    @classmethod
    def rectangular(cls, frame: Frame, length: float, width: float, thickness: float) -> Self:
        element = super().rectangular(frame, length, width, thickness)
        ac.set_opening([element.id])
        return element
