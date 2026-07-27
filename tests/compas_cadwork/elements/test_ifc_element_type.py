import pytest

from compas_cadwork.elements.ifc_element_type import IfcElementType


@pytest.mark.parametrize("expected_type", list(IfcElementType))
def test_gets_value_from_cadwork(cadwork, expected_type) -> None:
    cadwork.cadwork.ifc_2x3_element_type.return_value.__str__.return_value = expected_type.value
    raw_type = cadwork.cadwork.ifc_2x3_element_type()
    assert IfcElementType.from_cadwork(raw_type) == expected_type


def test_raises_on_unknown_cadwork_type(cadwork) -> None:
    cadwork.cadwork.ifc_2x3_element_type.return_value.__str__.return_value = "ThisDoesNotExist"
    raw_type = cadwork.cadwork.ifc_2x3_element_type()
    with pytest.raises(ValueError, match=r"'ThisDoesNotExist' is not a valid IfcElementType"):
        _ = IfcElementType.from_cadwork(raw_type)


@pytest.mark.parametrize("expected_type", list(IfcElementType))
def test_exports_value_to_cadwork(cadwork, expected_type) -> None:
    raw_type = expected_type.to_cadwork()
    expected_method = "set_none" if expected_type == IfcElementType.NONE else f"set_ifc_{expected_type.name.lower()}"
    getattr(raw_type, expected_method).assert_called_once()


@pytest.mark.parametrize("expected_type", list(IfcElementType))
def test_repr(expected_type) -> None:
    assert repr(expected_type) == f"<IfcElementType.{expected_type.name}>"
