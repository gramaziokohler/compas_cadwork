from __future__ import annotations

from typing import Literal

import attribute_controller as ac
import element_controller as ec
import geometry_controller as gc
from compas.geometry import Point
from typing_extensions import Self

from compas_cadwork.conversions.primitives import point_to_cadwork
from compas_cadwork.conversions.primitives import point_to_compas
from compas_cadwork.conversions.primitives import vector_to_cadwork
from compas_cadwork.transaction import notify_element_creation
from compas_cadwork.transaction import notify_element_modification

from .element import Element
from .element_type import ElementType
from .node_symbol import NodeSymbol


class Node(Element[Literal[ElementType.CONNECTOR_NODE, ElementType.NORMAL_NODE]]):
    """Node element.

    NOTE: While we support reading `ElementType.CONNECTOR_NODE`, note that this type is no longer used in cadwork 3d.
    """

    @classmethod
    def create(cls, position: Point, symbol: NodeSymbol = NodeSymbol.SMALL_SQUARE) -> Self:
        """Create new node.

        Parameters
        ----------
        position : Point
            Node position.
        symbol : NodeSymbol
            Node symbol.

        Returns
        -------
        Self
            New node element.
        """
        element_id = ec.create_node(point_to_cadwork(position))
        notify_element_creation(element_id)
        element = cls(element_id)
        element.symbol = symbol
        return element

    @property
    def position(self) -> Point:
        """Node position."""
        return point_to_compas(gc.get_p1(self.id))

    @position.setter
    def position(self, value: Point) -> None:
        translation = value - self.position
        ec.move_element([self.id], vector_to_cadwork(translation))
        notify_element_modification(self.id)

    @property
    def symbol(self) -> NodeSymbol:
        """Node symbol."""
        raw_symbol = ac.get_node_symbol(self.id)
        return NodeSymbol.from_cadwork(raw_symbol)

    @symbol.setter
    def symbol(self, value: NodeSymbol) -> None:
        ac.set_node_symbol([self.id], value.to_cadwork())
        notify_element_modification(self.id)
