from typing import Self

import element_controller as ec
import geometry_controller as gc
from compas.geometry import Frame
from compas.geometry import Vector

from compas_cadwork.batch_update import notify_element_creation
from compas_cadwork.batch_update import notify_element_modification
from compas_cadwork.conversions.primitives import point_to_compas
from compas_cadwork.conversions.primitives import vector_to_cadwork
from compas_cadwork.conversions.primitives import vector_to_compas

from .element import Element
from .element import T


class OrientedElement(Element[T]):
    """Cadwork element with a frame (position and rotation)."""

    @property
    def frame(self) -> Frame:
        """Reference frame."""
        p1 = point_to_compas(gc.get_p1(self.id))
        x_axis = vector_to_compas(gc.get_xl(self.id))
        y_axis = vector_to_compas(gc.get_yl(self.id))
        return Frame(p1, x_axis, y_axis)

    def translate(self, vector: Vector) -> None:
        """Translate element by the given vector.

        Parameters
        ----------
        vector : Vector
            The vector by which to translate the element.
        """
        ec.move_element([self.id], vector_to_cadwork(vector))
        notify_element_modification(self.id)

    def duplicate(self, vector: Vector) -> Self:
        """Duplicate element by the given vector.

        Parameters
        ----------
        vector : Vector
            The vector by which to duplicate the element.

        Returns
        -------
        Self
            New element.
        """
        new_element_ids = ec.copy_elements([self.id], vector_to_cadwork(vector))
        if len(new_element_ids) != 1:
            raise RuntimeError(f"Failed to copy Cadwork element with ID {self.id}")
        notify_element_creation(new_element_ids[0])
        return self.__class__(new_element_ids[0])
