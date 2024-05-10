from typing import List
from typing import Tuple
from typing import Union
from enum import Enum

import dimension_controller as dc

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Plane
from compas.geometry import Vector
from compas.geometry import closest_point_on_plane
from compas.utilities import pairwise

from compas_cadwork.datamodel import Element
from compas_cadwork.conversions import point_to_compas
from compas_cadwork.conversions import vector_to_compas


class DimTolerance(float, Enum):
    """Defines the minimum supported dimension length."""
    HIGH_PRECISION = 1e-6
    MEDIUM_PRECISION = 1e-3
    LOW_PRECISION = 0.1


def _get_dimension_element(element: Union[int, Element]) -> Tuple[List[Point], Vector, float]:
    """Get linear dimension by its element id or Element object.

    TODO: Return a LinearDimension object instead of a tuple once it's out of monosashi.
    TODO: Not doing it now to avoid circular dependency.

    Parameters
    ----------
    element : int or :class:`Element`
        The element id or Element object.

    Returns
    -------
    tuple
        A tuple of (points, xaxis, text_normal, distances).

    """
    distances = []
    element_id = element.id if isinstance(element, Element) else element
    points = dc.get_dimension_points(element_id)
    points = [point_to_compas(p) for p in points]
    text_normal = Vector(*dc.get_plane_normal(element_id))
    seg_count = dc.get_segment_count(element_id)
    for i in range(seg_count):
        distances.append(dc.get_segment_distance(element_id, i))
    xaxis = vector_to_compas(dc.get_plane_xl(element_id))

    return points, xaxis, text_normal, distances


def _dimension_frame(points, xaxis, text_normal):
    """Construct a Frame object from the dimension points and text normal."""
    zaxis = -Vector(*text_normal)
    yaxis = xaxis.cross(zaxis).unitized()
    ref_frame = Frame(points[0], xaxis, yaxis)
    return ref_frame

def _dimension_from_segment(start, end, ref_frame):
    # project dimension points to start plane
    plane = Plane.from_frame(ref_frame)
    start_closest = closest_point_on_plane(start, plane)
    end_closest = closest_point_on_plane(end, plane)
    return Frame(start_closest, ref_frame.xaxis, ref_frame.yaxis), start_closest, end_closest

def get_dimension_data(element: Union[int, Element]) -> Tuple[Frame, Point, Point]:
        points, xaxis, text_normal, distances = _get_dimension_element(element)
        assert len(points) == len(distances)

        ref_frame = _dimension_frame(points, xaxis, text_normal)
        dimensions = []
        for (d_start, d_end), (p_start, p_end) in zip(pairwise(distances), pairwise(points)):
            start = p_start + ref_frame.yaxis * d_start
            end = p_end + ref_frame.yaxis * d_end
            if start.distance_to_point(end) < DimTolerance.LOW_PRECISION:
                continue
            dimensions.append(_dimension_from_segment(start, end, ref_frame))
