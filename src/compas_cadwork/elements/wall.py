from __future__ import annotations

from typing import Literal

from .base_element import BaseElement
from .element_type import ElementType


class Wall(BaseElement):
    """Wall element."""

    @property
    def type(self) -> Literal[ElementType.WALL]:
        return ElementType.WALL
