from __future__ import annotations
from dataclasses import dataclass

from dimension_controller import get_dimension_points
from dimension_controller import get_plane_normal
from dimension_controller import get_plane_xl
from dimension_controller import get_segment_distance
from dimension_controller import get_segment_direction

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas.tolerance import Tolerance

from compas_cadwork.conversions import point_to_compas
from compas_cadwork.conversions import vector_to_compas
from .element import Element
from .element import ElementType


TOL = Tolerance(unit="MM", absolute=1e-3, relative=1e-3)


@dataclass
class AnchorPoint:
    """Anchor point of a cadwork measurement. There may me 2 or more anchor points in a measurement.

    Attributes
    ----------
    location : Point
        The location of the anchor point in 3d space.
    distance : float
        The distance of the anchor point from the measurement line.
    direction : Vector
        The direction of the anchor point from the measurement line.

    """

    location: Point
    distance: float
    direction: Vector

    def __eq__(self, other: AnchorPoint) -> bool:
        if not isinstance(other, AnchorPoint):
            return False

        if not TOL.is_allclose([*self.location], [*other.location]):
            return False

        if not TOL.is_allclose([*self.direction], [*other.direction]):
            return False

        return TOL.is_close(self.distance, other.distance)


class Dimension(Element):
    """Represents a cadwork dimension"""

    def __init__(self, id):
        super().__init__(id, ElementType.DIMENSION)
        self._frame = None
        # not lazy-instantiating this so that it can be used to compare the modified instances of the same dimension
        # otherwise, the anchors values that are compared depend on the time `anchors` was first accessed
        self.anchors = self._init_anchors()

    def __str__(self) -> str:
        return f"dimension element_id:{self.id} instruction_id:{self.get_instruction_id()} length:{self.length:.0f} anchors:{len(self.anchors)}"

    def __hash__(self):
        return hash(self.cadwork_guid)

    def __eq__(self, other: Dimension):
        """Checks if this element is equal to another element.

        Two elements are considered equal if they have the same guid and their dimension points are equal
        within a tolerance of 0.0001.

        Parameters
        ----------
        other : dimension
            The other element to compare.

        """
        if not isinstance(other, Dimension):
            return False

        if self.cadwork_guid != other.cadwork_guid:
            return False

        for point_self, point_other in zip(self.anchors, other.anchors):
            if point_self != point_other:
                return False
        return True

    @property
    def frame(self):
        if not self._frame:
            zaxis = -self.text_normal
            xaxis = vector_to_compas(get_plane_xl(self.id))
            yaxis = xaxis.cross(zaxis).unitized()
            self._frame = Frame(self.anchors[0].location, xaxis, yaxis)
        return self._frame

    @property
    def text_normal(self):
        return vector_to_compas(get_plane_normal(self.id))

    @property
    def length(self):
        start: Point = self.anchors[0].location
        end: Point = self.anchors[-1].location
        return start.distance_to_point(end)

    def _init_anchors(self):
        anchors = []
        for index, point in enumerate(get_dimension_points(self.id)):
            distance = get_segment_distance(self.id, index)
            direction = get_segment_direction(self.id, index)
            anchors.append(AnchorPoint(point_to_compas(point), distance, vector_to_compas(direction)))
        return tuple(anchors)

    @classmethod
    def from_id(cls, element_id: int) -> Dimension:
        """Creates a dimension object from an element id.

        This is an override of :method:`Element.from_id`.

        Parameters
        ----------
        element_id : int
            The id of the element to create the dimension from.

        Returns
        -------
        :class:`Dimension`
            The dimension object created from the element id.

        """
        return cls(id=element_id)

    @classmethod
    def from_element(cls, element: Element) -> Dimension:
        """Creates a dimension object from an element.

        Parameters
        ----------
        element : :class:`Element`
            The element to create the dimension from.

        Returns
        -------
        :class:`Dimension`
            The dimension object created from the element.

        """
        return cls(id=element.id)
