import bim_controller as bc
import pytest

from compas_cadwork.elements.ifc_predefined_type import IfcPredefinedType


def test_gets_value_from_cadwork(cadwork) -> None:
    cadwork.cadwork.ifc_predefined_type.return_value.is_glue.return_value = True
    raw_type = bc.get_ifc_predefined_type(123)
    assert IfcPredefinedType.from_cadwork(raw_type) == IfcPredefinedType.GLUE


def test_raises_on_unknown_cadwork_type(cadwork) -> None:
    raw_type = bc.get_ifc_predefined_type(123)
    with pytest.raises(ValueError, match=r"Unknown Cadwork IFC predefined type"):
        _ = IfcPredefinedType.from_cadwork(raw_type)


def test_exports_value_to_cadwork(cadwork) -> None:
    _ = IfcPredefinedType.PARKING.to_cadwork()
    cadwork.cadwork.ifc_predefined_type.return_value.set_parking.assert_called_once()
    cadwork.cadwork.ifc_predefined_type.return_value.set_none.assert_not_called()
    cadwork.cadwork.ifc_predefined_type.return_value.set_beam.assert_not_called()


def test_repr() -> None:
    assert repr(IfcPredefinedType.NONE) == "<IfcPredefinedType.NONE>"
    assert repr(IfcPredefinedType.ARCH) == "<IfcPredefinedType.ARCH>"
