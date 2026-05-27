from uuid import UUID

import pytest

from compas_cadwork.elements.element import Element
from compas_cadwork.utils.ifc_uuid import IfcUUID


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
    cadwork.bc.get_ifc_guid.return_value = ""
    with pytest.raises(RuntimeError, match=r"Cadwork element #123 no longer exists"):
        _ = element.ifc_guid


def test_gets_element_guid(cadwork) -> None:
    element = Element(123)
    cadwork.ec.get_element_cadwork_guid.return_value = "{12345678-AAAA-BBBB-CCCC-DDEE12345678}"
    assert element.guid == UUID("12345678-aaaa-bbbb-cccc-ddee12345678")
    cadwork.ec.get_element_cadwork_guid.assert_called_once_with(123)


def test_gets_element_ifc_guid(cadwork) -> None:
    element = Element(123)
    cadwork.bc.get_ifc_guid.return_value = "{C4B98E68-62AE-42C5-AC14-436FDB8116D9}"
    assert element.ifc_guid == IfcUUID("c4b98e68-62ae-42c5-ac14-436fdb8116d9")
    cadwork.bc.get_ifc_guid.assert_called_once_with(123)


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


def test_gets_element_comment(cadwork) -> None:
    element = Element(123)

    # Without value
    cadwork.ac.get_comment.return_value = ""
    assert element.comment is None
    cadwork.ac.get_comment.assert_called_once_with(123)

    # With value
    cadwork.ac.get_comment.return_value = "Element Comment"
    assert element.comment == "Element Comment"


def test_sets_element_comment(cadwork) -> None:
    element = Element(123)

    # Without value
    element.comment = None
    cadwork.ac.set_comment.assert_called_once_with([123], "")

    # With value
    element.comment = "Test Value"
    cadwork.ac.set_comment.assert_called_with([123], "Test Value")


def test_contains_attributes(cadwork) -> None:
    element = Element(123)

    # Without value
    cadwork.ac.get_user_attribute.return_value = ""
    assert 100 not in element.attributes
    cadwork.ac.get_user_attribute.assert_called_once_with(123, 100)

    # With value
    cadwork.ac.get_user_attribute.return_value = "Test Value"
    assert 200 in element.attributes
    cadwork.ac.get_user_attribute.assert_called_with(123, 200)


def test_gets_attributes(cadwork) -> None:
    element = Element(123)

    # Without value
    cadwork.ac.get_user_attribute.return_value = ""
    with pytest.raises(KeyError):
        _ = element.attributes[300]
    cadwork.ac.get_user_attribute.assert_called_once_with(123, 300)
    assert element.attributes.get(300, None) is None
    assert element.attributes.get(300, "Default") == "Default"

    # With value
    cadwork.ac.get_user_attribute.return_value = "Test Value"
    assert element.attributes[400] == "Test Value"
    cadwork.ac.get_user_attribute.assert_called_with(123, 400)
    assert element.attributes.get(400, None) == "Test Value"
    assert element.attributes.get(400, "Default") == "Test Value"


def test_sets_attributes(cadwork) -> None:
    element = Element(123)

    # Base case
    element.attributes[500] = "New Value"
    cadwork.ac.set_user_attribute.assert_called_once_with([123], 500, "New Value")

    # Without value
    cadwork.ac.get_user_attribute.side_effect = ["", "Default Value"]
    assert element.attributes.setdefault(501, "Default Value") == "Default Value"
    cadwork.ac.get_user_attribute.assert_called_with(123, 501)
    cadwork.ac.set_user_attribute.assert_called_with([123], 501, "Default Value")

    # With value
    cadwork.ac.set_user_attribute.reset_mock()
    cadwork.ac.get_user_attribute.reset_mock(side_effect=True)
    cadwork.ac.get_user_attribute.return_value = "Existing Value"
    assert element.attributes.setdefault(502, "Default Value") == "Existing Value"
    cadwork.ac.get_user_attribute.assert_called_with(123, 502)
    cadwork.ac.set_user_attribute.assert_not_called()


def test_deletes_attributes(cadwork) -> None:
    element = Element(123)

    # Without value
    cadwork.ac.get_user_attribute.return_value = ""
    with pytest.raises(KeyError):
        del element.attributes[600]
    cadwork.ac.get_user_attribute.assert_called_once_with(123, 600)

    # With value
    cadwork.ac.get_user_attribute.return_value = "Test Value"
    del element.attributes[700]
    cadwork.ac.get_user_attribute.assert_called_with(123, 700)
    cadwork.ac.set_user_attribute.assert_called_once_with([123], 700, "")


def test_contains_data(cadwork) -> None:
    element = Element(123)

    # Without value
    cadwork.ac.get_additional_data.return_value = ""
    assert "first" not in element.data
    cadwork.ac.get_additional_data.assert_called_once_with(123, "first")

    # With value
    cadwork.ac.get_additional_data.return_value = "Test Value"
    assert "second" in element.data
    cadwork.ac.get_additional_data.assert_called_with(123, "second")


def test_gets_data(cadwork) -> None:
    element = Element(123)

    # Without value
    cadwork.ac.get_additional_data.return_value = ""
    with pytest.raises(KeyError):
        _ = element.data["third"]
    cadwork.ac.get_additional_data.assert_called_once_with(123, "third")
    assert element.data.get("third", None) is None
    assert element.data.get("third", "Default") == "Default"

    # With value
    cadwork.ac.get_additional_data.return_value = "Test Value"
    assert element.data["fourth"] == "Test Value"
    cadwork.ac.get_additional_data.assert_called_with(123, "fourth")
    assert element.data.get("fourth", None) == "Test Value"
    assert element.data.get("fourth", "Default") == "Test Value"


def test_sets_data(cadwork) -> None:
    element = Element(123)

    # Base case
    element.data["fifth"] = "New Value"
    cadwork.ac.set_additional_data.assert_called_once_with([123], "fifth", "New Value")

    # Without value
    cadwork.ac.get_additional_data.side_effect = ["", "Default Value"]
    assert element.data.setdefault("sixth", "Default Value") == "Default Value"
    cadwork.ac.get_additional_data.assert_called_with(123, "sixth")
    cadwork.ac.set_additional_data.assert_called_with([123], "sixth", "Default Value")

    # With value
    cadwork.ac.set_additional_data.reset_mock()
    cadwork.ac.get_additional_data.reset_mock(side_effect=True)
    cadwork.ac.get_additional_data.return_value = "Existing Value"
    assert element.data.setdefault("seventh", "Default Value") == "Existing Value"
    cadwork.ac.get_additional_data.assert_called_with(123, "seventh")
    cadwork.ac.set_additional_data.assert_not_called()


def test_deletes_data(cadwork) -> None:
    element = Element(123)

    # Without value
    cadwork.ac.get_additional_data.return_value = ""
    with pytest.raises(KeyError):
        del element.data["first"]
    cadwork.ac.get_additional_data.assert_called_once_with(123, "first")

    # With value
    cadwork.ac.get_additional_data.return_value = "Test Value"
    del element.data["second"]
    cadwork.ac.get_additional_data.assert_called_with(123, "second")
    cadwork.ac.delete_additional_data.assert_called_once_with([123], "second")
    cadwork.ac.set_additional_data.assert_not_called()


def test_deletes_element(cadwork) -> None:
    element = Element(123)
    element.delete()
    cadwork.ec.delete_elements.assert_called_once_with([123])


def test_repr(cadwork) -> None:
    element = Element(123)
    cadwork.ac.get_name.return_value = "Something"
    assert repr(element) == "Element(id=123, name='Something')"
