from datetime import date
from uuid import UUID

import pytest

from compas_cadwork.ifc_uuid import IfcUUID
from compas_cadwork.project import Project


def test_gets_guid(cadwork) -> None:
    project = Project()
    cadwork.uc.get_project_guid.return_value = "{12345678-AAAA-BBBB-CCCC-DDEE12345678}"
    assert project.guid == UUID("12345678-aaaa-bbbb-cccc-ddee12345678")


def test_gets_name(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_name.return_value = "???"
    assert project.name is None
    cadwork.uc.get_project_name.return_value = ""
    assert project.name is None

    # With value
    cadwork.uc.get_project_name.return_value = "Project Name"
    assert project.name == "Project Name"


def test_sets_name(cadwork) -> None:
    project = Project()

    # Without value
    project.name = None
    cadwork.uc.set_project_name.assert_called_with("")

    # With value
    project.name = "Test Value"
    cadwork.uc.set_project_name.assert_called_with("Test Value")


def test_gets_part(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_part.return_value = "???"
    assert project.part is None
    cadwork.uc.get_project_part.return_value = ""
    assert project.part is None

    # With value
    cadwork.uc.get_project_part.return_value = "Project Part"
    assert project.part == "Project Part"


def test_sets_part(cadwork) -> None:
    project = Project()

    # Without value
    project.part = None
    cadwork.uc.set_project_part.assert_called_with("")

    # With value
    project.part = "Test Value"
    cadwork.uc.set_project_part.assert_called_with("Test Value")


def test_gets_number(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_number.return_value = "???"
    assert project.number is None
    cadwork.uc.get_project_number.return_value = ""
    assert project.number is None

    # With value
    cadwork.uc.get_project_number.return_value = "Project Number"
    assert project.number == "Project Number"


def test_sets_number(cadwork) -> None:
    project = Project()

    # Without value
    project.number = None
    cadwork.uc.set_project_number.assert_called_with("")

    # With value
    project.number = "Test Value"
    cadwork.uc.set_project_number.assert_called_with("Test Value")


def test_gets_deadline(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_deadline.return_value = "???"
    assert project.deadline is None
    cadwork.uc.get_project_deadline.return_value = ""
    assert project.deadline is None

    # With value
    cadwork.uc.get_project_deadline.return_value = "31.12.2026"
    assert project.deadline == date(2026, 12, 31)


def test_sets_deadline(cadwork) -> None:
    project = Project()

    # Without value
    project.deadline = None
    cadwork.uc.set_project_deadline.assert_called_with("")

    # With value
    project.deadline = date(2029, 1, 12)
    cadwork.uc.set_project_deadline.assert_called_with("12.01.2029")


def test_gets_architect(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_architect.return_value = "???"
    assert project.architect is None
    cadwork.uc.get_project_architect.return_value = ""
    assert project.architect is None

    # With value
    cadwork.uc.get_project_architect.return_value = "Jane Doe"
    assert project.architect == "Jane Doe"


def test_sets_architect(cadwork) -> None:
    project = Project()

    # Without value
    project.architect = None
    cadwork.uc.set_project_architect.assert_called_with("")

    # With value
    project.architect = "Test Value"
    cadwork.uc.set_project_architect.assert_called_with("Test Value")


def test_gets_customer(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_customer.return_value = "???"
    assert project.customer is None
    cadwork.uc.get_project_customer.return_value = ""
    assert project.customer is None

    # With value
    cadwork.uc.get_project_customer.return_value = "John Smith"
    assert project.customer == "John Smith"


def test_sets_customer(cadwork) -> None:
    project = Project()

    # Without value
    project.customer = None
    cadwork.uc.set_project_customer.assert_called_with("")

    # With value
    project.customer = "Test Value"
    cadwork.uc.set_project_customer.assert_called_with("Test Value")


def test_gets_designer(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_designer.return_value = "???"
    assert project.designer is None
    cadwork.uc.get_project_designer.return_value = ""
    assert project.designer is None

    # With value
    cadwork.uc.get_project_designer.return_value = "Alice Scott"
    assert project.designer == "Alice Scott"


def test_sets_designer(cadwork) -> None:
    project = Project()

    # Without value
    project.designer = None
    cadwork.uc.set_project_designer.assert_called_with("")

    # With value
    project.designer = "Test Value"
    cadwork.uc.set_project_designer.assert_called_with("Test Value")


def test_gets_element_by_cadwork_id(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.ec.check_element_id.return_value = False
    with pytest.raises(ValueError, match=r"Could not find a Cadwork element with ID #1000"):
        _ = project.element(cadwork_id=1000)
    cadwork.ec.check_element_id.assert_called_once_with(1000)

    # With value
    cadwork.cadwork.element_type.is_panel.return_value = True
    cadwork.ec.check_element_id.return_value = True
    element = project.element(cadwork_id=12345)
    cadwork.ec.check_element_id.assert_called_with(12345)
    assert element.id == 12345


def test_gets_element_by_guid(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.ec.get_element_from_cadwork_guid.return_value = 0
    with pytest.raises(
        ValueError,
        match=r"Could not find a Cadwork element with GUID '{DEADBEEF-0000-0000-0000-000000000000}'",
    ):
        _ = project.element(guid=UUID("deadbeef-0000-0000-0000-000000000000"))

    # With value
    cadwork.cadwork.element_type.is_panel.return_value = True
    cadwork.ec.get_element_from_cadwork_guid.return_value = 12345
    cadwork.ec.get_element_cadwork_guid.return_value = "{2B21165D-9454-46A0-A992-6B4AA043D58D}"
    element = project.element(guid=UUID("2b21165d-9454-46a0-a992-6b4aa043d58d"))
    cadwork.ec.get_element_from_cadwork_guid.assert_called_with("{2B21165D-9454-46A0-A992-6B4AA043D58D}")
    cadwork.ec.get_element_cadwork_guid.assert_called_with(12345)
    assert element.id == 12345
    assert element.guid == UUID("2b21165d-9454-46a0-a992-6b4aa043d58d")


def test_gets_element_by_ifc_guid(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.bc.get_element_id_from_base64_ifc_guid.return_value = 0
    with pytest.raises(ValueError, match=r"Could not find a Cadwork element with IFC GUID '3UhRxl0000000000000000'"):
        _ = project.element(ifc_guid=IfcUUID("deadbeef-0000-0000-0000-000000000000"))

    # With value
    cadwork.cadwork.element_type.is_panel.return_value = True
    cadwork.bc.get_element_id_from_base64_ifc_guid.return_value = 54321
    element = project.element(ifc_guid=IfcUUID("921ab9eb-3b21-46c8-baa4-dfffc33b59be"))
    cadwork.bc.get_element_id_from_base64_ifc_guid.assert_called_with("2I6hdhEo56oBgat$$3Erc_")
    assert element.id == 54321
    cadwork.bc.get_ifc_guid.return_value = "{921AB9EB-3B21-46C8-BAA4-DFFFC33B59BE}"
    assert element.ifc_guid == IfcUUID("921ab9eb-3b21-46c8-baa4-dfffc33b59be")
    cadwork.bc.get_ifc_guid.assert_called_with(54321)


def test_gets_elements(cadwork) -> None:
    project = Project()

    # Without elements
    cadwork.ec.get_all_identifiable_element_ids.return_value = []
    assert len(list(project.elements())) == 0

    # With elements
    cadwork.cadwork.element_type.is_panel.return_value = True
    cadwork.ec.get_all_identifiable_element_ids.return_value = [505, 404, 303, 202, 101]
    assert [x.id for x in project.elements()] == [505, 404, 303, 202, 101]


def test_gets_selected_elements(cadwork) -> None:
    project = Project()

    # Without elements
    cadwork.ec.get_active_identifiable_element_ids.return_value = []
    assert len(list(project.selected_elements())) == 0

    # With elements
    cadwork.cadwork.element_type.is_panel.return_value = True
    cadwork.ec.get_active_identifiable_element_ids.return_value = [505, 404, 303, 202, 101]
    assert [x.id for x in project.selected_elements()] == [505, 404, 303, 202, 101]


def test_contains_attributes(cadwork) -> None:
    cadwork.uc.get_project_user_attribute.side_effect = lambda x: "Test Value" if x == 100 else "???"
    project = Project()
    assert 200 not in project.attributes
    cadwork.uc.get_project_user_attribute.assert_called_once_with(200)
    assert 100 in project.attributes
    cadwork.uc.get_project_user_attribute.assert_called_with(100)


def test_gets_attributes(cadwork) -> None:
    cadwork.uc.get_project_user_attribute.side_effect = lambda x: "Test Value" if x == 100 else "???"
    project = Project()
    with pytest.raises(KeyError):
        _ = project.attributes[200]
    cadwork.uc.get_project_user_attribute.assert_called_once_with(200)
    assert project.attributes[100] == "Test Value"
    cadwork.uc.get_project_user_attribute.assert_called_with(100)


def test_sets_attributes(cadwork) -> None:
    project = Project()
    project.attributes[100] = "New Value"
    cadwork.uc.set_project_user_attribute.assert_called_once_with(100, "New Value")


def test_deletes_attributes(cadwork) -> None:
    cadwork.uc.get_project_user_attribute.side_effect = lambda x: "Test Value" if x == 100 else "???"
    project = Project()
    with pytest.raises(KeyError):
        del project.attributes[200]
    cadwork.uc.get_project_user_attribute.assert_called_once_with(200)
    cadwork.uc.set_project_user_attribute.assert_not_called()
    del project.attributes[100]
    cadwork.uc.get_project_user_attribute.assert_called_with(100)
    cadwork.uc.set_project_user_attribute.assert_called_with(100, "")


def test_raises_on_iterate_attributes() -> None:
    project = Project()
    with pytest.raises(TypeError):
        _ = list(project.attributes.keys())
    with pytest.raises(TypeError):
        _ = len(project.attributes)


def test_contains_attribute_keys(cadwork) -> None:
    cadwork.uc.get_project_user_attribute_name.side_effect = lambda x: "Test Value" if x == 100 else ""
    project = Project()
    assert 200 not in project.attribute_keys
    cadwork.uc.get_project_user_attribute_name.assert_called_once_with(200)
    assert 100 in project.attribute_keys
    cadwork.uc.get_project_user_attribute_name.assert_called_with(100)


def test_gets_attribute_keys(cadwork) -> None:
    cadwork.uc.get_project_user_attribute_name.side_effect = lambda x: "Test Value" if x == 100 else ""
    project = Project()
    with pytest.raises(KeyError):
        _ = project.attribute_keys[200]
    cadwork.uc.get_project_user_attribute_name.assert_called_once_with(200)
    assert project.attribute_keys[100] == "Test Value"
    cadwork.uc.get_project_user_attribute_name.assert_called_with(100)


def test_sets_attribute_keys(cadwork) -> None:
    project = Project()
    project.attribute_keys[100] = "New Value"
    cadwork.uc.set_project_user_attribute_name.assert_called_once_with(100, "New Value")


def test_deletes_attribute_keys(cadwork) -> None:
    cadwork.uc.get_project_user_attribute_name.side_effect = lambda x: "Test Value" if x == 100 else ""
    project = Project()
    with pytest.raises(KeyError):
        del project.attribute_keys[200]
    cadwork.uc.get_project_user_attribute_name.assert_called_once_with(200)
    cadwork.uc.set_project_user_attribute_name.assert_not_called()
    del project.attribute_keys[100]
    cadwork.uc.get_project_user_attribute_name.assert_called_with(100)
    cadwork.uc.set_project_user_attribute_name.assert_called_with(100, "")


def test_raises_on_iterate_attribute_keys() -> None:
    project = Project()
    with pytest.raises(TypeError):
        _ = list(project.attribute_keys.keys())
    with pytest.raises(TypeError):
        _ = len(project.attribute_keys)


def test_contains_data(cadwork) -> None:
    cadwork.uc.get_project_data.side_effect = lambda x: "Test Value" if x == "existingKey" else ""
    project = Project()
    assert "missingKey" not in project.data
    cadwork.uc.get_project_data.assert_called_once_with("missingKey")
    assert "existingKey" in project.data
    cadwork.uc.get_project_data.assert_called_with("existingKey")


def test_gets_data(cadwork) -> None:
    cadwork.uc.get_project_data.side_effect = lambda x: "Test Value" if x == "existingKey" else ""
    project = Project()
    with pytest.raises(KeyError):
        _ = project.data["missingKey"]
    cadwork.uc.get_project_data.assert_called_once_with("missingKey")
    assert project.data["existingKey"] == "Test Value"
    cadwork.uc.get_project_data.assert_called_with("existingKey")


def test_sets_data(cadwork) -> None:
    project = Project()
    project.data["newKey"] = "New Value"
    cadwork.uc.set_project_data.assert_called_once_with("newKey", "New Value")


def test_deletes_data(cadwork) -> None:
    cadwork.uc.get_project_data.side_effect = lambda x: "Test Value" if x == "existingKey" else ""
    project = Project()
    with pytest.raises(KeyError):
        del project.data["missingKey"]
    cadwork.uc.get_project_data.assert_called_once_with("missingKey")
    cadwork.uc.delete_project_data.assert_not_called()
    del project.data["existingKey"]
    cadwork.uc.get_project_data.assert_called_with("existingKey")
    cadwork.uc.delete_project_data.assert_called_with("existingKey")


def test_iterates_data(cadwork) -> None:
    data = {
        "1st": "First",
        "2nd": "Second",
        "3rd": "",
        "4th": "Fourth",
    }
    cadwork.uc.get_project_data_keys.return_value = list(data.keys())
    cadwork.uc.get_project_data.side_effect = lambda x: data[x]
    project = Project()
    assert len(project.data) == 3
    assert list(project.data.keys()) == ["1st", "2nd", "4th"]
    assert list(project.data.values()) == ["First", "Second", "Fourth"]


def test_repr(cadwork) -> None:
    project = Project()
    cadwork.uc.get_project_guid.return_value = "{12345678-AAAA-BBBB-CCCC-DDEE12345678}"
    cadwork.uc.get_project_name.return_value = "???"
    assert repr(project) == "Project(guid=UUID('12345678-aaaa-bbbb-cccc-ddee12345678'), name=None)"
