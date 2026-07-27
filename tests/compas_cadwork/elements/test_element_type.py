import pytest

from compas_cadwork.elements.element_type import ElementType


@pytest.mark.parametrize("expected_type", list(ElementType))
def test_gets_value_from_cadwork(cadwork, expected_type) -> None:
    match expected_type:
        case ElementType.ADDITIONAL:
            expected_method = "is_additional_element"
        case ElementType.POLYGONAL_BEAM:
            expected_method = "is_rectangular_beam"
        case _:
            expected_method = f"is_{expected_type.name.lower()}"
    getattr(cadwork.cadwork.element_type.return_value, expected_method).return_value = True
    raw_type = cadwork.cadwork.element_type()
    assert ElementType.from_cadwork(raw_type) == expected_type


def test_raises_on_unknown_cadwork_type(cadwork) -> None:
    raw_type = cadwork.cadwork.element_type()
    with pytest.raises(ValueError, match=r"Unknown Cadwork element type"):
        _ = ElementType.from_cadwork(raw_type)


@pytest.mark.parametrize("expected_type", list(ElementType))
def test_repr(expected_type) -> None:
    assert repr(expected_type) == f"<ElementType.{expected_type.name}>"
