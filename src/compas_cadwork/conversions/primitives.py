from __future__ import annotations

import cadwork
from compas.geometry import Point
from compas.geometry import Vector


def point_to_cadwork(point: Point) -> cadwork.point_3d:
    """Convert COMPAS point to Cadwork point.

    Parameters
    ----------
    point : Point
        COMPAS point.

    Returns
    -------
    cadwork.point_3d
        Cadwork point.
    """
    return cadwork.point_3d(point.x, point.y, point.z)


def vector_to_cadwork(vector: Vector) -> cadwork.point_3d:
    """Convert COMPAS vector to Cadwork vector.

    Parameters
    ----------
    vector : Vector
        COMPAS vector.

    Returns
    -------
    cadwork.point_3d
        Cadwork point.
    """
    return cadwork.point_3d(vector.x, vector.y, vector.z)


def point_to_compas(point: cadwork.point_3d) -> Point:
    """Convert Cadwork point to COMPAS point.

    Parameters
    ----------
    point : cadwork.point_3d
        Cadwork point.

    Returns
    -------
    Point
        COMPAS point.
    """
    return Point(point.x, point.y, point.z)


def vector_to_compas(vector: cadwork.point_3d) -> Vector:
    """Convert Cadwork vector to COMPAS vector.

    Parameters
    ----------
    vector: cadwork.point_3d
        Cadwork vector.

    Returns
    -------
    Vector
        COMPAS vector.
    """
    return Vector(vector.x, vector.y, vector.z)
