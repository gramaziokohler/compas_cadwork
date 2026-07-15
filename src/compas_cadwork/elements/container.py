from __future__ import annotations

from typing import Literal

from .element import Element
from .element_type import ElementType
from .mixins.aggregate_mixin import AggregateMixin


class Container(Element[Literal[ElementType.CONTAINER]], AggregateMixin):
    """Container element."""
