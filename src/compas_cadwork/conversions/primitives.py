from cadwork import point_3d
from compas.geometry import Point
from compas.geometry import Vector


def point_to_cadwork(point: Point):
    """Convert a :class:`compas.geometry.Point` to a cadwork point_3d object.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        The point to convert

    Returns
    -------
    :class:`cadwork.point_3d`

    """
    return point_3d(point.x, point.y, point.z)


def vector_to_cadwork(vector: Vector):
    """Convert a :class:`compas.geometry.Vector` to a cadwork point_3d object.

    Parameters
    ----------
    vector : :class:`~compas.geometry.Vector`
        The vector to convert

    Returns
    -------
    :class:`cadwork.point_3d`

    """
    return point_3d(vector.x, vector.y, vector.z)


def point_to_compas(point: point_3d):
    """Convert a :class:`compas.geometry.Point` to a cadwork point_3d object.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        The point to convert

    Returns
    -------
    :class:`cadwork.point_3d`

    """
    return Point(point.x, point.y, point.z)


def vector_to_compas(vector: point_3d):
    """Convert a :class:`compas.geometry.Point` to a cadwork point_3d object.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        The point to convert

    Returns
    -------
    :class:`cadwork.point_3d`

    """
    return Vector(*point_to_compas(vector))
