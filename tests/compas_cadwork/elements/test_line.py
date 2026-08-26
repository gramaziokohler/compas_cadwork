from compas.geometry import Point

from compas_cadwork.elements.line import Line


def test_creates_line(cadwork) -> None:
    cadwork.ec.create_line_points.return_value = 1000
    element = Line.create(Point(100.0, 200.0, 0.0), Point(100.0, 200.0, 300.0))
    assert element.id == 1000
    cadwork.ec.create_line_points.assert_called_once_with(
        cadwork.cadwork.point_3d(100.0, 200.0, 0.0),
        cadwork.cadwork.point_3d(100.0, 200.0, 300.0),
    )


def test_gets_start(cadwork) -> None:
    cadwork.gc.get_p1.return_value = cadwork.cadwork.point_3d(100.1, 200.2, 300.3)
    element = Line(123)
    assert element.start == Point(100.1, 200.2, 300.3)
    cadwork.gc.get_p1.assert_called_once_with(123)


def test_gets_end(cadwork) -> None:
    cadwork.gc.get_p2.return_value = cadwork.cadwork.point_3d(-100.12, 0.0, -300.99)
    element = Line(123)
    assert element.end == Point(-100.12, 0.0, -300.99)
    cadwork.gc.get_p2.assert_called_once_with(123)


def test_gets_length(cadwork) -> None:
    cadwork.gc.get_length.return_value = 123.45
    element = Line(123)
    assert element.length == 123.45
    cadwork.gc.get_length.assert_called_once_with(123)
