from __future__ import annotations

from typing import Literal
from typing import Self

import attribute_controller as ac
from compas.geometry import Frame
from compas.geometry import Polygon

from compas_cadwork.elements.mixins.layered_mixin import LayeredMixin
from compas_cadwork.materials.layer_stack import FloorLayerStack

from .element_type import ElementType
from .panel import Panel


class Floor(Panel[Literal[ElementType.FLOOR]], LayeredMixin[FloorLayerStack]):
    """Floor element."""

    @classmethod
    def polygonal(cls, frame: Frame, outline: Polygon, thickness: float) -> Self:
        element = super().polygonal(frame, outline, thickness)
        ac.set_framed_floor([element.id])
        return element

    @classmethod
    def rectangular(cls, frame: Frame, length: float, width: float, thickness: float) -> Self:
        element = super().rectangular(frame, length, width, thickness)
        ac.set_framed_floor([element.id])
        return element

    @property
    def _layer_stack_type(self) -> type[FloorLayerStack]:
        return FloorLayerStack
