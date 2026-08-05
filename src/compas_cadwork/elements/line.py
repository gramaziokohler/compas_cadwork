from __future__ import annotations

from typing import Literal

import element_controller as ec
import geometry_controller as gc
from compas.geometry import Point
from typing_extensions import Self

from compas_cadwork.conversions.primitives import point_to_cadwork
from compas_cadwork.conversions.primitives import point_to_compas
from compas_cadwork.transaction import notify_element_creation

from .element_type import ElementType
from .oriented_element import OrientedElement


class Line(OrientedElement[Literal[ElementType.LINE]]):
    """Line element."""

    @classmethod
    def create(cls, start: Point, end: Point) -> Self:
        """Create new line element.

        Parameters
        ----------
        start : Point
            Start point.
        end : Point
            End point.

        Returns
        -------
        Self
            New line element.
        """
        element_id = ec.create_line_points(point_to_cadwork(start), point_to_cadwork(end))
        notify_element_creation(element_id)
        return cls(element_id)

    @property
    def start(self) -> Point:
        """Start point."""
        return point_to_compas(gc.get_p1(self.id))

    @property
    def end(self) -> Point:
        """End point."""
        return point_to_compas(gc.get_p2(self.id))

    @property
    def length(self) -> float:
        """Length in millimeters."""
        return gc.get_length(self.id)
