from compas.geometry import Point

from compas_cadwork.elements.node import Node
from compas_cadwork.elements.node_symbol import NodeSymbol


def test_creates_node(cadwork) -> None:
    cadwork.ec.create_node.return_value = 1000
    element = Node.create(Point(100.0, 200.0, 300.0), NodeSymbol.FILLED_CIRCLE)
    assert element.id == 1000
    cadwork.ec.create_node.assert_called_once_with(cadwork.cadwork.point_3d(100.0, 200.0, 300.0))
    cadwork.ac.set_node_symbol.assert_called_once_with([1000], cadwork.cadwork.node_symbol.FilledCircle)


def test_gets_position(cadwork) -> None:
    cadwork.gc.get_p1.return_value = cadwork.cadwork.point_3d(100.1, 200.2, 300.3)
    element = Node(123)
    assert element.position == Point(100.1, 200.2, 300.3)
    cadwork.gc.get_p1.assert_called_once_with(123)


def test_sets_position(cadwork) -> None:
    cadwork.gc.get_p1.return_value = cadwork.cadwork.point_3d(100.0, 200.0, 300.0)
    element = Node(123)
    element.position = Point(-100.99, 0.0, -300.99)
    cadwork.ec.move_element.assert_called_once_with([123], cadwork.cadwork.point_3d(-200.99, -200.0, -600.99))


def test_gets_symbol(cadwork) -> None:
    cadwork.ac.get_node_symbol.return_value = cadwork.cadwork.node_symbol.HalfFilledSquare
    element = Node(123)
    assert element.symbol == NodeSymbol.HALF_FILLED_SQUARE
    cadwork.ac.get_node_symbol.assert_called_once_with(123)


def test_sets_symbol(cadwork) -> None:
    element = Node(123)
    element.symbol = NodeSymbol.CIRCLE
    cadwork.ac.set_node_symbol.assert_called_once_with([123], cadwork.cadwork.node_symbol.Circle)
