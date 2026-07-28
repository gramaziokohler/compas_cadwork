import attribute_controller as ac
import pytest

from compas_cadwork.elements.element_type import ElementType


def test_maps_valid_types(cadwork) -> None:
    cadwork.cadwork.element_type.is_wall.return_value = True
    raw_type = ac.get_element_type(123)
    assert ElementType.from_cadwork(raw_type) == ElementType.WALL


def test_raises_on_unknown_type(cadwork) -> None:
    raw_type = ac.get_element_type(123)
    with pytest.raises(ValueError, match=r"Unknown Cadwork element type"):
        _ = ElementType.from_cadwork(raw_type)
