from __future__ import annotations

from typing import Literal

from .element import Element
from .element_type import ElementType


class Wall(Element[Literal[ElementType.WALL]]):
    """Wall element."""
