from enum import Enum

import cadwork
from typing_extensions import Self


class NodeSymbol(Enum):
    """Node symbol."""

    SMALL_SQUARE = cadwork.node_symbol.SmallSquare
    SQUARE = cadwork.node_symbol.Square
    CROSS = cadwork.node_symbol.Cross
    CIRCLE = cadwork.node_symbol.Circle
    FILLED_CIRCLE = cadwork.node_symbol.FilledCircle
    CHESS_SQUARE = cadwork.node_symbol.ChessSquare
    HALF_FILLED_SQUARE = cadwork.node_symbol.HalfFilledSquare
    CROSS_SQUARE = cadwork.node_symbol.CrossSquare
    FILLED_SQUARE = cadwork.node_symbol.FilledSquare

    @classmethod
    def from_cadwork(cls, raw_type: cadwork.node_symbol) -> Self:
        """Get value from Cadwork node symbol.

        Parameters
        ----------
        raw_type : cadwork.node_symbol
            Cadwork node symbol.

        Returns
        -------
        NodeSymbol
            Node symbol.

        Raises
        ------
        ValueError
            If cannot determine the correct mapping.
        """
        return cls(raw_type)

    def to_cadwork(self) -> cadwork.node_symbol:
        """Convert value to Cadwork node symbol.

        Returns
        -------
        cadwork.node_symbol
            Cadwork node symbol.
        """
        return self.value

    def __repr__(self) -> str:
        return f"<NodeSymbol.{self.name}>"
