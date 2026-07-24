import attribute_controller as ac
import pytest

from compas_cadwork.elements.element_type import ElementType


def test_gets_value_from_cadwork(cadwork) -> None:
    cadwork.cadwork.element_type.return_value.is_wall.return_value = True
    raw_type = ac.get_element_type(123)
    assert ElementType.from_cadwork(raw_type) == ElementType.WALL


def test_raises_on_unknown_cadwork_type(cadwork) -> None:
    raw_type = ac.get_element_type(123)
    with pytest.raises(ValueError, match=r"Unknown Cadwork element type"):
        _ = ElementType.from_cadwork(raw_type)


def test_repr() -> None:
    assert repr(ElementType.OPENING) == "<ElementType.OPENING>"
    assert repr(ElementType.CIRCULAR_BEAM) == "<ElementType.CIRCULAR_BEAM>"
