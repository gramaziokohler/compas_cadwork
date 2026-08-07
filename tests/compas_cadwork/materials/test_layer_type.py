from typing import Any
from typing import cast

import pytest

from compas_cadwork.materials.layer_type import LayerType


def test_gets_value_from_cadwork(cadwork) -> None:
    assert LayerType.from_cadwork(cadwork.cadwork.multi_layer_type.structure) == LayerType.STRUCTURE
    assert LayerType.from_cadwork(cadwork.cadwork.multi_layer_type.lathing) == LayerType.LATHING


def test_raises_on_unknown_cadwork_type() -> None:
    with pytest.raises(ValueError, match=r"100 is not a valid LayerType"):
        raw_value = cast(Any, 100)
        _ = LayerType.from_cadwork(raw_value)


def test_exports_value_to_cadwork(cadwork) -> None:
    assert LayerType.STRUCTURE.to_cadwork() == cadwork.cadwork.multi_layer_type.structure
    assert LayerType.PANEL.to_cadwork() == cadwork.cadwork.multi_layer_type.panel


def test_repr() -> None:
    assert repr(LayerType.UNDEFINED) == "<LayerType.UNDEFINED>"
    assert repr(LayerType.AIR) == "<LayerType.AIR>"
