import bim_controller as bc
import pytest

from compas_cadwork.elements.ifc_element_type import IfcElementType


def test_gets_value_from_cadwork(cadwork) -> None:
    cadwork.cadwork.ifc_2x3_element_type.return_value.__str__.return_value = "Ramp"
    cadwork.cadwork.ifc_2x3_element_type.return_value.is_ifc_ramp.return_value = True
    raw_type = bc.get_ifc2x3_element_type(123)
    assert IfcElementType.from_cadwork(raw_type) == IfcElementType.RAMP


def test_raises_on_unknown_cadwork_type(cadwork) -> None:
    cadwork.cadwork.ifc_2x3_element_type.return_value.__str__.return_value = "ThisDoesNotExist"
    raw_type = bc.get_ifc2x3_element_type(123)
    with pytest.raises(ValueError, match=r"'ThisDoesNotExist' is not a valid IfcElementType"):
        _ = IfcElementType.from_cadwork(raw_type)


def test_exports_value_to_cadwork(cadwork) -> None:
    _ = IfcElementType.WINDOW.to_cadwork()
    cadwork.cadwork.ifc_2x3_element_type.return_value.set_ifc_window.assert_called_once()
    cadwork.cadwork.ifc_2x3_element_type.return_value.set_none.assert_not_called()
    cadwork.cadwork.ifc_2x3_element_type.return_value.set_ifc_beam.assert_not_called()


def test_repr() -> None:
    assert repr(IfcElementType.NONE) == "<IfcElementType.NONE>"
    assert repr(IfcElementType.ROOF) == "<IfcElementType.ROOF>"
