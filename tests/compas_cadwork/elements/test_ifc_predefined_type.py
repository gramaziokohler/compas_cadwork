import pytest

from compas_cadwork.elements.ifc_predefined_type import IfcPredefinedType


@pytest.mark.parametrize("expected_type", list(IfcPredefinedType))
def test_gets_value_from_cadwork(cadwork, expected_type) -> None:
    expected_method = f"is_{expected_type.name.lower()}"
    getattr(cadwork.cadwork.ifc_predefined_type.return_value, expected_method).return_value = True
    raw_type = cadwork.cadwork.ifc_predefined_type()
    assert IfcPredefinedType.from_cadwork(raw_type) == expected_type


def test_raises_on_unknown_cadwork_type(cadwork) -> None:
    raw_type = cadwork.cadwork.ifc_predefined_type()
    with pytest.raises(ValueError, match=r"Unknown Cadwork IFC predefined type"):
        _ = IfcPredefinedType.from_cadwork(raw_type)


@pytest.mark.parametrize("expected_type", list(IfcPredefinedType))
def test_exports_value_to_cadwork(cadwork, expected_type) -> None:
    raw_type = expected_type.to_cadwork()
    match expected_type:
        case IfcPredefinedType.NAIL_PLATE:
            expected_method = "set_nailplate"
        case IfcPredefinedType.SHEAR_CONNECTOR:
            expected_method = "set_shearconnector"
        case IfcPredefinedType.STUD_SHEAR_CONNECTOR:
            expected_method = "set_studshearconnector"
        case _:
            expected_method = f"set_{expected_type.name.lower()}"
    getattr(raw_type, expected_method).assert_called_once()


@pytest.mark.parametrize("expected_type", list(IfcPredefinedType))
def test_repr(expected_type) -> None:
    assert repr(expected_type) == f"<IfcPredefinedType.{expected_type.name}>"
