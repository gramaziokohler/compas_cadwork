import geometry_controller as gc
import visualization_controller as vc
from compas.geometry import Line

from compas_cadwork.conversions.primitives import point_to_compas
from compas_cadwork.materials.material import Material
from compas_cadwork.transaction import notify_element_modification

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
        notify_element_modification(self.id)

    @property
    def width(self) -> float:
        """Width in millimeters (along Y-axis)."""
        return gc.get_width(self.id)

    @width.setter
    def width(self, value: float) -> None:
        gc.set_width_real([self.id], value)
        notify_element_modification(self.id)

    @property
    def height(self) -> float:
        """Height in millimeters (along Z-axis)."""
        return gc.get_height(self.id)

    @height.setter
    def height(self, value: float) -> None:
        gc.set_height_real([self.id], value)
        notify_element_modification(self.id)

    @property
    def centerline(self) -> Line:
        """Line connecting the two points that define the element."""
        p1 = point_to_compas(gc.get_p1(self.id))
        p2 = point_to_compas(gc.get_p2(self.id))
        return Line(p1, p2)

    @property
    def material(self) -> Material:
        """Element material."""
        material_id = vc.get_material(self.id)
        if material_id == 0:
            raise RuntimeError(f"Cadwork element #{self.id} no longer exists")
        return Material(material_id)

    @material.setter
    def material(self, value: Material) -> None:
        vc.set_material([self.id], value.id)
        notify_element_modification(self.id)
