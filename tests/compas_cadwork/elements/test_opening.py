from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Vector

from compas_cadwork.elements.opening import Opening


def test_creates_polygonal_opening(cadwork) -> None:
    cadwork.ec.create_polygon_panel.return_value = 1122
    Opening.polygonal(
        frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
        outline=Polygon([(0, 0), (300, 0), (150, 259.8)]),
        thickness=100.0,
    )
    cadwork.ac.set_opening.assert_called_once_with([1122])


def test_creates_rectangular_opening(cadwork) -> None:
    cadwork.ec.create_rectangular_panel_vectors.return_value = 1121
    Opening.rectangular(
        frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
        length=4000.0,
        width=1000.0,
        thickness=200.0,
    )
    cadwork.ac.set_opening.assert_called_once_with([1121])
