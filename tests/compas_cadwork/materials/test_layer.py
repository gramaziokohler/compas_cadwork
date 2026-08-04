import pytest

from compas_cadwork.materials.layer import Layer
from compas_cadwork.materials.layer_type import LayerType
from compas_cadwork.materials.material import Material


def test_raises_on_invalid_thickness() -> None:
    # Negative values raise an error
    with pytest.raises(ValueError, match=r"Layer thickness cannot be negative"):
        Layer(name="Test Layer", type=LayerType.PANEL, material=Material(123), thickness=-100.0)

    # Zero is a valid thickness
    layer = Layer(name="Test Layer", type=LayerType.PANEL, material=Material(123), thickness=0.0)
    assert layer.thickness == 0.0
