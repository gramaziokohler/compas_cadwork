from __future__ import annotations

import cadwork
from compas.geometry import Point
from compas.geometry import Vector


def cwpoint_to_point(value: cadwork.point_3d) -> Point:
    """Convert Cadwork point to COMPAS point.

    Parameters
    ----------
    value : cadwork.point_3d
        Cadwork point.

    Returns
    -------
    Point
        COMPAS point.
    """
    return Point(value.x, value.y, value.z)


def cwpoint_to_vector(value: cadwork.point_3d) -> Vector:
    """Convert Cadwork point to COMPAS vector.

    Parameters
    ----------
    value : cadwork.point_3d
        Cadwork point.

    Returns
    -------
    Vector
        COMPAS vector.
    """
    return Vector(value.x, value.y, value.z)


def compas_to_cwpoint(value: Point | Vector) -> cadwork.point_3d:
    """Convert COMPAS point or vector to Cadwork point.

    Parameters
    ----------
    value : Point | Vector
        COMPAS point or vector.

    Returns
    -------
    cadwork.point_3d
        Cadwork point.
    """
    return cadwork.point_3d(value.x, value.y, value.z)
