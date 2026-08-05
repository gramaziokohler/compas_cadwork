from typing import Any
from typing import cast

import pytest

from compas_cadwork.elements.node_symbol import NodeSymbol


def test_gets_value_from_cadwork(cadwork) -> None:
    assert NodeSymbol.from_cadwork(cadwork.cadwork.node_symbol.Square) == NodeSymbol.SQUARE
    assert NodeSymbol.from_cadwork(cadwork.cadwork.node_symbol.ChessSquare) == NodeSymbol.CHESS_SQUARE


def test_raises_on_unknown_cadwork_value() -> None:
    with pytest.raises(ValueError, match=r"100 is not a valid NodeSymbol"):
        raw_value = cast(Any, 100)
        _ = NodeSymbol.from_cadwork(raw_value)


def test_exports_value_to_cadwork(cadwork) -> None:
    assert NodeSymbol.CIRCLE.to_cadwork() == cadwork.cadwork.node_symbol.Circle
    assert NodeSymbol.CROSS.to_cadwork() == cadwork.cadwork.node_symbol.Cross


def test_repr() -> None:
    assert repr(NodeSymbol.HALF_FILLED_SQUARE) == "<NodeSymbol.HALF_FILLED_SQUARE>"
    assert repr(NodeSymbol.SMALL_SQUARE) == "<NodeSymbol.SMALL_SQUARE>"
