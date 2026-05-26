from uuid import UUID

import pytest

from compas_cadwork.elements.element import Element


def test_get_element_from_guid(cadwork) -> None:
    cadwork.ec.get_element_from_cadwork_guid.return_value = 12345
    cadwork.ec.get_element_cadwork_guid.return_value = "{2B21165D-9454-46A0-A992-6B4AA043D58D}"
    element = Element.from_guid(UUID("2b21165d-9454-46a0-a992-6b4aa043d58d"))
    cadwork.ec.get_element_from_cadwork_guid.assert_called_once_with("{2B21165D-9454-46A0-A992-6B4AA043D58D}")
    cadwork.ec.get_element_cadwork_guid.assert_called_once_with(12345)
    assert element.guid == UUID("2b21165d-9454-46a0-a992-6b4aa043d58d")
    assert element.id == 12345


def test_raises_on_unknown_guid(cadwork) -> None:
    cadwork.ec.get_element_from_cadwork_guid.return_value = ""
    with pytest.raises(ValueError, match=r"Could not find a Cadwork element with GUID .+"):
        Element.from_guid(UUID("deadbeef-0000-0000-0000-000000000000"))


def test_raises_on_deleted_element(cadwork) -> None:
    element = Element(123)

    # For Cadwork GUID
    cadwork.ec.get_element_cadwork_guid.return_value = ""
    with pytest.raises(RuntimeError, match=r"Cadwork element #123 no longer exists"):
        _ = element.guid

    # For IFC GUID
    cadwork.bc.get_ifc_base64_guid.return_value = ""
    with pytest.raises(RuntimeError, match=r"Cadwork element #123 no longer exists"):
        _ = element.ifc_guid


def test_gets_element_guid(cadwork) -> None:
    element = Element(123)
    cadwork.ec.get_element_cadwork_guid.return_value = "{12345678-AAAA-BBBB-CCCC-DDEE12345678}"
    assert element.guid == UUID("12345678-aaaa-bbbb-cccc-ddee12345678")
    cadwork.ec.get_element_cadwork_guid.assert_called_once_with(123)


def test_gets_element_ifc_guid(cadwork) -> None:
    element = Element(123)
    cadwork.bc.get_ifc_base64_guid.return_value = "34kOveOgv2nQmKGs$RWHRP"
    assert element.ifc_guid == "34kOveOgv2nQmKGs$RWHRP"
    cadwork.bc.get_ifc_base64_guid.assert_called_once_with(123)


def test_gets_element_name(cadwork) -> None:
    element = Element(123)

    # Without value
    cadwork.ac.get_name.return_value = ""
    assert element.name is None
    cadwork.ac.get_name.assert_called_once_with(123)

    # With value
    cadwork.ac.get_name.return_value = "Element Name"
    assert element.name == "Element Name"


def test_sets_element_name(cadwork) -> None:
    element = Element(123)

    # Without value
    element.name = None
    cadwork.ac.set_name.assert_called_once_with([123], "")

    # With value
    element.name = "Test Value"
    cadwork.ac.set_name.assert_called_with([123], "Test Value")


def test_gets_element_group_from_group(cadwork) -> None:
    element = Element(123)
    cadwork.ac.get_element_grouping_type.return_value = cadwork.cadwork.element_grouping_type.group

    # Without value
    cadwork.ac.get_group.return_value = ""
    assert element.group is None
    cadwork.ac.get_group.assert_called_once_with(123)
    cadwork.ac.get_subgroup.assert_not_called()

    # With value
    cadwork.ac.get_group.return_value = "Group Name"
    assert element.group == "Group Name"
    cadwork.ac.get_group.assert_called_with(123)  # type: ignore[unreachable]
    cadwork.ac.get_subgroup.assert_not_called()


def test_sets_element_group_from_group(cadwork) -> None:
    element = Element(123)
    cadwork.ac.get_element_grouping_type.return_value = cadwork.cadwork.element_grouping_type.group

    # With value
    element.group = None
    cadwork.ac.set_group.assert_called_once_with([123], "")
    cadwork.ac.set_subgroup.assert_not_called()

    # With value
    element.group = "Test Value"
    cadwork.ac.set_group.assert_called_with([123], "Test Value")
    cadwork.ac.set_subgroup.assert_not_called()


def test_gets_element_group_from_subgroup(cadwork) -> None:
    element = Element(123)
    cadwork.ac.get_element_grouping_type.return_value = cadwork.cadwork.element_grouping_type.subgroup

    # Without value
    cadwork.ac.get_subgroup.return_value = ""
    assert element.group is None
    cadwork.ac.get_group.assert_not_called()
    cadwork.ac.get_subgroup.assert_called_once_with(123)

    # With value
    cadwork.ac.get_subgroup.return_value = "Subgroup Name"
    assert element.group == "Subgroup Name"
    cadwork.ac.get_group.assert_not_called()  # type: ignore[unreachable]
    cadwork.ac.get_subgroup.assert_called_with(123)


def test_sets_element_group_from_subgroup(cadwork) -> None:
    element = Element(123)
    cadwork.ac.get_element_grouping_type.return_value = cadwork.cadwork.element_grouping_type.subgroup

    # Without value
    element.group = None
    cadwork.ac.set_group.assert_not_called()
    cadwork.ac.set_subgroup.assert_called_once_with([123], "")

    # With value
    element.group = "Test Value"
    cadwork.ac.set_group.assert_not_called()
    cadwork.ac.set_subgroup.assert_called_with([123], "Test Value")


def test_deletes_element(cadwork) -> None:
    element = Element(123)
    element.delete()
    cadwork.ec.delete_elements.assert_called_once_with([123])


def test_repr(cadwork) -> None:
    element = Element(123)
    cadwork.ac.get_name.return_value = "Something"
    assert repr(element) == "Element(id=123, name='Something')"
