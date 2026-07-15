import pytest
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Vector

from compas_cadwork.elements.panel import Panel


def test_raises_on_invalid_parameters_for_polygonal_panel() -> None:
    with pytest.raises(ValueError, match=r"The Z coordinate of all polygon points defining the outline must be zero"):
        _ = Panel.polygonal(
            frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
            outline=Polygon([(0, 0), (200, 0, -123), (100, 173.2)]),
            thickness=20.0,
        )
    with pytest.raises(ValueError, match=r"The element thickness must be positive"):
        _ = Panel.polygonal(
            frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
            outline=Polygon([(0, 0), (200, 0), (100, 173.2)]),
            thickness=-200.0,
        )


def test_creates_polygonal_panel(cadwork) -> None:
    # Horizontal
    cadwork.ec.create_polygon_panel.return_value = 1122
    panel = Panel.polygonal(
        frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
        outline=Polygon([(0, 0), (300, 0), (150, 259.8)]),
        thickness=100.0,
    )
    assert panel.id == 1122
    cadwork.ec.create_polygon_panel.assert_called_once_with(
        cadwork.cadwork.vertex_list(
            [
                cadwork.cadwork.point_3d(50.0, 150.0, -129.9),
                cadwork.cadwork.point_3d(50.0, -150.0, -129.9),
                cadwork.cadwork.point_3d(50.0, 0.0, 129.9),
                cadwork.cadwork.point_3d(50.0, 150.0, -129.9),
            ],
        ),
        100.0,
        cadwork.cadwork.point_3d(1.0, 0.0, 0.0),
        cadwork.cadwork.point_3d(0.0, -1.0, 0.0),
    )

    # Vertical
    cadwork.ec.create_polygon_panel.return_value = 1121
    panel = Panel.polygonal(
        frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
        outline=Polygon([(0, 0), (200, 0), (100, 173.2)]),
        thickness=250.0,
    )
    assert panel.id == 1121
    cadwork.ec.create_polygon_panel.assert_called_with(
        cadwork.cadwork.vertex_list(
            [
                cadwork.cadwork.point_3d(125.0, 100.0, -86.6),
                cadwork.cadwork.point_3d(125.0, -100.0, -86.6),
                cadwork.cadwork.point_3d(125.0, 0.0, 86.6),
                cadwork.cadwork.point_3d(125.0, 100.0, -86.6),
            ],
        ),
        250.0,
        cadwork.cadwork.point_3d(1.0, 0.0, 0.0),
        cadwork.cadwork.point_3d(0.0, -1.0, 0.0),
    )


def test_raises_on_invalid_parameters_for_rectangular_panel() -> None:
    with pytest.raises(ValueError, match=r"The element length must be positive"):
        _ = Panel.rectangular(
            frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
            length=0.0,
            width=0.123,
            thickness=1000.0,
        )
    with pytest.raises(ValueError, match=r"The element width must be positive"):
        _ = Panel.rectangular(
            frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
            length=20.0,
            width=-5.0,
            thickness=10.0,
        )
    with pytest.raises(ValueError, match=r"The element thickness must be positive"):
        _ = Panel.rectangular(
            frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
            length=20.0,
            width=5.0,
            thickness=-10.0,
        )


def test_creates_rectangular_panel(cadwork) -> None:
    cadwork.ec.create_rectangular_panel_vectors.return_value = 1121
    panel = Panel.rectangular(
        frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
        length=4000.0,
        width=1000.0,
        thickness=200.0,
    )
    assert panel.id == 1121
    cadwork.ec.create_rectangular_panel_vectors.assert_called_once_with(
        1000.0,
        200.0,
        4000.0,
        cadwork.cadwork.point_3d(0.0, 0.0, 0.0),
        cadwork.cadwork.point_3d(1.0, 0.0, 0.0),
        cadwork.cadwork.point_3d(0.0, -1.0, 0.0),
    )
