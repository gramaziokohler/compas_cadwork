import pytest
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Vector

from compas_cadwork.elements.beam import Beam


def test_raises_on_invalid_parameters_for_circular_beam() -> None:
    with pytest.raises(ValueError, match=r"The beam length must be positive"):
        _ = Beam.circular(
            frame=Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
            length=0.0,
            diameter=0.123,
        )
    with pytest.raises(ValueError, match=r"The beam diameter must be positive"):
        _ = Beam.circular(
            frame=Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
            length=20.0,
            diameter=-100.0,
        )


def test_creates_circular_beam(cadwork) -> None:
    cadwork.ec.create_circular_beam_vectors.return_value = 1122
    beam = Beam.circular(
        frame=Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
        length=2000.0,
        diameter=123.4,
    )
    assert beam.id == 1122
    cadwork.ec.create_circular_beam_vectors.assert_called_once_with(
        123.4,
        2000.0,
        cadwork.cadwork.point_3d(0.0, 0.0, 0.0),
        cadwork.cadwork.point_3d(0.0, 1.0, 0.0),
        cadwork.cadwork.point_3d(1.0, 0.0, 0.0),
    )


def test_raises_on_invalid_parameters_for_polygonal_beam() -> None:
    with pytest.raises(ValueError, match=r"The beam length must be positive"):
        _ = Beam.polygonal(
            frame=Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
            length=-200.0,
            section=Polygon([(0, 0), (200, 0), (100, 173.2)]),
        )
    with pytest.raises(ValueError, match=r"The Z coordinate of all polygon points defining the section must be zero"):
        _ = Beam.polygonal(
            frame=Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
            length=20.0,
            section=Polygon([(0, 0), (200, 0, -123), (100, 173.2)]),
        )


def test_creates_polygonal_beam(cadwork) -> None:
    # X-axis = (0, 1, 0)
    cadwork.ec.create_polygon_beam.return_value = 1122
    beam = Beam.polygonal(
        frame=Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
        length=500.0,
        section=Polygon([(0, 0), (200, 0), (100, 173.2)]),
    )
    assert beam.id == 1122
    cadwork.ec.create_polygon_beam.assert_called_once_with(
        cadwork.cadwork.vertex_list(
            [
                cadwork.cadwork.point_3d(-100.0, 250.0, -86.6),
                cadwork.cadwork.point_3d(100.0, 250.0, -86.6),
                cadwork.cadwork.point_3d(0.0, 250.0, 86.6),
            ],
        ),
        500.0,
        cadwork.cadwork.point_3d(0.0, 1.0, 0.0),
        cadwork.cadwork.point_3d(1.0, 0.0, 0.0),
    )

    # X-axis = (1, 0, 0)
    cadwork.ec.create_polygon_beam.return_value = 1121
    beam = Beam.polygonal(
        frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
        length=3000.0,
        section=Polygon([(0, 0), (300, 0), (150, 259.8)]),
    )
    assert beam.id == 1121
    cadwork.ec.create_polygon_beam.assert_called_with(
        cadwork.cadwork.vertex_list(
            [
                cadwork.cadwork.point_3d(1500.0, 150.0, -129.9),
                cadwork.cadwork.point_3d(1500.0, -150.0, -129.9),
                cadwork.cadwork.point_3d(1500.0, 0.0, 129.9),
            ],
        ),
        3000.0,
        cadwork.cadwork.point_3d(1.0, 0.0, 0.0),
        cadwork.cadwork.point_3d(0.0, -1.0, 0.0),
    )


def test_raises_on_invalid_parameters_for_rectangular_beam() -> None:
    with pytest.raises(ValueError, match=r"The beam length must be positive"):
        _ = Beam.rectangular(
            frame=Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
            length=0.0,
            width=0.123,
            height=1000.0,
        )
    with pytest.raises(ValueError, match=r"The beam width must be positive"):
        _ = Beam.rectangular(
            frame=Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
            length=20.0,
            width=-5.0,
            height=10.0,
        )
    with pytest.raises(ValueError, match=r"The beam height must be positive"):
        _ = Beam.rectangular(
            frame=Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
            length=20.0,
            width=5.0,
            height=-10.0,
        )


def test_creates_rectangular_beam(cadwork) -> None:
    cadwork.ec.create_rectangular_beam_vectors.return_value = 1121
    beam = Beam.rectangular(
        frame=Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
        length=4000.0,
        width=300.0,
        height=650.0,
    )
    assert beam.id == 1121
    cadwork.ec.create_rectangular_beam_vectors.assert_called_once_with(
        300.0,
        650.0,
        4000.0,
        cadwork.cadwork.point_3d(0.0, 0.0, 0.0),
        cadwork.cadwork.point_3d(0.0, 1.0, 0.0),
        cadwork.cadwork.point_3d(1.0, 0.0, 0.0),
    )
