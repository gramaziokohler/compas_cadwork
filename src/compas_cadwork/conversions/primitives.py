try:
    from cadwork import point_3d
except ImportError:
    pass

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


def point_to_compas(point):
    """Convert a cadwork point_3d to a :class:`compas.geometry.Point` object.

    Parameters
    ----------
    point : :class:`cadwork.point_3d`
        The point to convert

    Returns
    -------
    :class:`~compas.geometry.Point`

    """
    return Point(point.x, point.y, point.z)


def vector_to_compas(vector):
    """Convert a cadwork point_3d to a :class:`compas.geometry.Point` obhect.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        The point to convert

    Returns
    -------
    :class:`cadwork.point_3d`

    """
    return Vector(*point_to_compas(vector))
