# TODO: Once shifting anchor points is no longer required, remove this module as replaced by datamodel.dimension
from typing import List
from typing import Tuple
from typing import Union

import dimension_controller as dc
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector

from compas_cadwork.conversions import point_to_compas
from compas_cadwork.conversions import vector_to_compas
from compas_cadwork.datamodel import Element


def _get_dimension_element(element: Union[int, Element]) -> Tuple[List[Point], Vector, float]:
    element_id = element.id if isinstance(element, Element) else element
    points = dc.get_dimension_points(element_id)
    points = [point_to_compas(p) for p in points]
    text_normal = Vector(*dc.get_plane_normal(element_id))
    seg_count = dc.get_segment_count(element_id)
    distances = []
    directions = []
    for i in range(seg_count):
        distances.append(dc.get_segment_distance(element_id, i))
        directions.append(vector_to_compas(dc.get_segment_direction(element_id, i)))
    xaxis = vector_to_compas(dc.get_plane_xl(element_id))
    return points, xaxis, text_normal, distances, directions


def _frame_from_dim(points, xaxis, text_normal):
    """Construct a Frame object from the dimension points and text normal."""
    zaxis = -Vector(*text_normal)
    yaxis = xaxis.cross(zaxis).unitized()
    ref_frame = Frame(points[0], xaxis, yaxis)
    return ref_frame


def _shift_anchor_points_to_line(points, distances, ref_frame, directions):
    new_anchors = []
    for point, distance, direction in zip(points, distances, directions):
        point = point + direction * distance
        new_anchors.append(point)
    new_frame = Frame(new_anchors[0], ref_frame.xaxis, ref_frame.yaxis)
    return new_anchors, new_frame


def get_dimension_data(element: Union[int, Element]) -> Tuple[Frame, List[Point]]:
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
    points, xaxis, text_normal, distances, directions = _get_dimension_element(element)
    ref_frame = _frame_from_dim(points, xaxis, text_normal)
    new_anchors, new_frame = _shift_anchor_points_to_line(points, distances, ref_frame, directions)
    return new_frame, new_anchors
