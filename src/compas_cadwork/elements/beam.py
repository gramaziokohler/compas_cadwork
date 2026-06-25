from __future__ import annotations

from typing import Literal

from .element import Element
from .element_type import ElementType


class Beam(Element[Literal[ElementType.CIRCULAR_BEAM, ElementType.POLYGONAL_BEAM]]):
    """Beam element."""
