import geometry_controller as gc
from compas.geometry import Line

from compas_cadwork.conversions.primitives import point_to_compas

from .element import T
from .oriented_element import OrientedElement


class DimensionalElement(OrientedElement[T]):
    """Cadwork element with dimensions."""

    @property
    def length(self) -> float:
        """Length in millimeters (along X-axis)."""
        return gc.get_length(self.id)

    @length.setter
    def length(self, value: float) -> None:
        gc.set_length_real([self.id], value)

    @property
    def width(self) -> float:
        """Width in millimeters (along Y-axis)."""
        return gc.get_width(self.id)

    @width.setter
    def width(self, value: float) -> None:
        gc.set_width_real([self.id], value)

    @property
    def height(self) -> float:
        """Height in millimeters (along Z-axis)."""
        return gc.get_height(self.id)

    @height.setter
    def height(self, value: float) -> None:
        gc.set_height_real([self.id], value)

    @property
    def centerline(self) -> Line:
        """Line connecting the two points that define the element."""
        p1 = point_to_compas(gc.get_p1(self.id))
        p2 = point_to_compas(gc.get_p2(self.id))
        return Line(p1, p2)
