from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector

from compas_cadwork.elements.oriented_element import OrientedElement


def test_gets_frame(cadwork) -> None:
    cadwork.gc.get_p1.return_value = cadwork.cadwork.point_3d(10.1, 20.2, 30.3)
    cadwork.gc.get_xl.return_value = cadwork.cadwork.point_3d(-1.0, 0.0, 0.0)
    cadwork.gc.get_yl.return_value = cadwork.cadwork.point_3d(0.0, -0.0, 1.0)
    element = OrientedElement(123)
    assert element.frame == Frame(Point(10.1, 20.2, 30.3), Vector(-1.0, 0.0, 0.0), Vector(0.0, -0.0, 1.0))
    cadwork.gc.get_p1.assert_called_once_with(123)
    cadwork.gc.get_xl.assert_called_once_with(123)
    cadwork.gc.get_yl.assert_called_once_with(123)


def test_translates_element(cadwork) -> None:
    element = OrientedElement(123)
    element.translate(Vector(100.0, 200.0, 300.0))
    cadwork.ec.move_element.assert_called_once_with([123], cadwork.cadwork.point_3d(100.0, 200.0, 300.0))


def test_duplicates_element(cadwork) -> None:
    cadwork.ec.copy_elements.return_value = [124]
    element = OrientedElement(123)
    new_element = element.duplicate(Vector(100.0, 200.0, 300.0))
    assert new_element is not element
    assert new_element.id == 124
    cadwork.ec.copy_elements.assert_called_once_with([123], cadwork.cadwork.point_3d(100.0, 200.0, 300.0))
