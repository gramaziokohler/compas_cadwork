from __future__ import annotations

from typing import Literal

import attribute_controller as ac

from .base_element import BaseElement
from .element_type import ElementType


class Beam(BaseElement):
    """Beam element."""

    @property
    def type(self) -> Literal[ElementType.CIRCULAR_BEAM, ElementType.RECTANGULAR_BEAM]:
        raw_type = ac.get_element_type(self.id)
        if raw_type.is_circular_beam():
            return ElementType.CIRCULAR_BEAM
        if raw_type.is_rectangular_beam():
            return ElementType.RECTANGULAR_BEAM
        raise ValueError(f"Cadwork element with ID {self.id} is not a beam")
