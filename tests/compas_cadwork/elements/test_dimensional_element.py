from compas.geometry import Line
from compas.geometry import Point

from compas_cadwork.elements.dimensional_element import DimensionalElement


def test_gets_width(cadwork) -> None:
    cadwork.gc.get_width.return_value = 1000.23
    element = DimensionalElement(123)
    assert element.width == 1000.23
    cadwork.gc.get_width.assert_called_once_with(123)


def test_sets_width(cadwork) -> None:
    element = DimensionalElement(123)
    element.width = 543.21
    cadwork.gc.set_width_real.assert_called_once_with([123], 543.21)


def test_gets_height(cadwork) -> None:
    cadwork.gc.get_height.return_value = 1000.23
    element = DimensionalElement(123)
    assert element.height == 1000.23
    cadwork.gc.get_height.assert_called_once_with(123)


def test_sets_height(cadwork) -> None:
    element = DimensionalElement(123)
    element.height = 543.21
    cadwork.gc.set_height_real.assert_called_once_with([123], 543.21)


def test_gets_length(cadwork) -> None:
    cadwork.gc.get_length.return_value = 1000.23
    element = DimensionalElement(123)
    assert element.length == 1000.23
    cadwork.gc.get_length.assert_called_once_with(123)


def test_sets_length(cadwork) -> None:
    element = DimensionalElement(123)
    element.length = 543.21
    cadwork.gc.set_length_real.assert_called_once_with([123], 543.21)


def test_gets_centerline(cadwork) -> None:
    cadwork.gc.get_p1.return_value = cadwork.cadwork.point_3d(10.1, 20.2, 30.3)
    cadwork.gc.get_p2.return_value = cadwork.cadwork.point_3d(100.1, 200.2, 300.3)
    element = DimensionalElement(123)
    assert element.centerline == Line(Point(10.1, 20.2, 30.3), Point(100.1, 200.2, 300.3))
    cadwork.gc.get_p1.assert_called_once_with(123)
    cadwork.gc.get_p2.assert_called_once_with(123)
