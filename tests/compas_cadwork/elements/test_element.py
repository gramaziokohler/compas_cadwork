from uuid import UUID

import pytest

from compas_cadwork.batch_update import BatchUpdate
from compas_cadwork.elements.element import Element
from compas_cadwork.elements.ifc_element_type import IfcElementType
from compas_cadwork.elements.ifc_predefined_type import IfcPredefinedType
from compas_cadwork.elements.wall import Wall
from compas_cadwork.ifc_uuid import IfcUUID


class FakeElementForRepr(Element):
    pass


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


def test_gets_guid(cadwork) -> None:
    element = Element(123)
    cadwork.ec.get_element_cadwork_guid.return_value = "{12345678-AAAA-BBBB-CCCC-DDEE12345678}"
    assert element.guid == UUID("12345678-aaaa-bbbb-cccc-ddee12345678")
    cadwork.ec.get_element_cadwork_guid.assert_called_once_with(123)


def test_gets_ifc_guid(cadwork) -> None:
    element = Element(123)
    cadwork.bc.get_ifc_guid.return_value = "{C4B98E68-62AE-42C5-AC14-436FDB8116D9}"
    assert element.ifc_guid == IfcUUID("c4b98e68-62ae-42c5-ac14-436fdb8116d9")
    cadwork.bc.get_ifc_guid.assert_called_once_with(123)


def test_gets_ifc_element_type(cadwork) -> None:
    element = Element(123)
    cadwork.cadwork.ifc_2x3_element_type.return_value.__str__.return_value = "Chimney"
    cadwork.cadwork.ifc_2x3_element_type.return_value.is_ifc_chimney.return_value = True
    assert element.ifc_element_type == IfcElementType.CHIMNEY
    cadwork.bc.get_ifc2x3_element_type.assert_called_once_with(123)


def test_sets_ifc_element_type(cadwork) -> None:
    element = Element(123)
    element.ifc_element_type = IfcElementType.DOOR
    cadwork.bc.set_ifc2x3_element_type.assert_called_once_with([123], cadwork.cadwork.ifc_2x3_element_type())
    cadwork.cadwork.ifc_2x3_element_type.return_value.set_ifc_door.assert_called_once()


def test_gets_ifc_predefined_type(cadwork) -> None:
    element = Element(123)
    cadwork.cadwork.ifc_predefined_type.return_value.is_molding.return_value = True
    assert element.ifc_predefined_type == IfcPredefinedType.MOLDING
    cadwork.bc.get_ifc_predefined_type.assert_called_once_with(123)


def test_sets_ifc_predefined_type(cadwork) -> None:
    element = Element(123)
    element.ifc_predefined_type = IfcPredefinedType.GUARDRAIL
    cadwork.bc.set_ifc_predefined_type.assert_called_once_with([123], cadwork.cadwork.ifc_predefined_type())
    cadwork.cadwork.ifc_predefined_type.return_value.set_guardrail.assert_called_once()


def test_gets_name(cadwork) -> None:
    element = Element(123)

    # Without value
    cadwork.ac.get_name.return_value = ""
    assert element.name is None
    cadwork.ac.get_name.assert_called_once_with(123)

    # With value
    cadwork.ac.get_name.return_value = "Element Name"
    assert element.name == "Element Name"


def test_sets_name(cadwork) -> None:
    element = Element(123)

    # Without value
    element.name = None
    cadwork.ac.set_name.assert_called_once_with([123], "")

    # With value
    element.name = "Test Value"
    cadwork.ac.set_name.assert_called_with([123], "Test Value")


def test_gets_group_from_group(cadwork) -> None:
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


def test_sets_group_from_group(cadwork) -> None:
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


def test_gets_group_from_subgroup(cadwork) -> None:
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


def test_sets_group_from_subgroup(cadwork) -> None:
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


def test_gets_comment(cadwork) -> None:
    element = Element(123)

    # Without value
    cadwork.ac.get_comment.return_value = ""
    assert element.comment is None
    cadwork.ac.get_comment.assert_called_once_with(123)

    # With value
    cadwork.ac.get_comment.return_value = "Element Comment"
    assert element.comment == "Element Comment"


def test_sets_comment(cadwork) -> None:
    element = Element(123)

    # Without value
    element.comment = None
    cadwork.ac.set_comment.assert_called_once_with([123], "")

    # With value
    element.comment = "Test Value"
    cadwork.ac.set_comment.assert_called_with([123], "Test Value")


def test_contains_attributes(cadwork) -> None:
    cadwork.ac.get_user_attribute.side_effect = lambda _, x: "Test Value" if x == 100 else ""
    element = Element(123)
    assert 200 not in element.attributes
    cadwork.ac.get_user_attribute.assert_called_once_with(123, 200)
    assert 100 in element.attributes
    cadwork.ac.get_user_attribute.assert_called_with(123, 100)


def test_gets_attributes(cadwork) -> None:
    cadwork.ac.get_user_attribute.side_effect = lambda _, x: "Test Value" if x == 100 else ""
    element = Element(123)
    with pytest.raises(KeyError):
        _ = element.attributes[200]
    cadwork.ac.get_user_attribute.assert_called_once_with(123, 200)
    assert element.attributes[100] == "Test Value"
    cadwork.ac.get_user_attribute.assert_called_with(123, 100)


def test_sets_attributes(cadwork) -> None:
    element = Element(123)
    element.attributes[100] = "New Value"
    cadwork.ac.set_user_attribute.assert_called_once_with([123], 100, "New Value")


def test_deletes_attributes(cadwork) -> None:
    cadwork.ac.get_user_attribute.side_effect = lambda _, x: "Test Value" if x == 100 else ""
    element = Element(123)
    with pytest.raises(KeyError):
        del element.attributes[200]
    cadwork.ac.get_user_attribute.assert_called_once_with(123, 200)
    cadwork.ac.set_user_attribute.assert_not_called()
    del element.attributes[100]
    cadwork.ac.get_user_attribute.assert_called_with(123, 100)
    cadwork.ac.set_user_attribute.assert_called_with([123], 100, "")


def test_raises_on_iterate_attributes() -> None:
    element = Element(123)
    with pytest.raises(TypeError):
        _ = list(element.attributes.keys())
    with pytest.raises(TypeError):
        _ = len(element.attributes)


def test_contains_attribute_keys(cadwork) -> None:
    cadwork.ac.get_user_attribute_name.side_effect = lambda x: "Test Value" if x == 100 else f"User{x}"
    assert 200 not in Element.attribute_keys
    cadwork.ac.get_user_attribute_name.assert_called_once_with(200)
    assert 100 in Element.attribute_keys
    cadwork.ac.get_user_attribute_name.assert_called_with(100)


def test_gets_attribute_keys(cadwork) -> None:
    cadwork.ac.get_user_attribute_name.side_effect = lambda x: "Test Value" if x == 100 else f"User{x}"
    with pytest.raises(KeyError):
        _ = Element.attribute_keys[200]
    cadwork.ac.get_user_attribute_name.assert_called_once_with(200)
    assert Element.attribute_keys[100] == "Test Value"
    cadwork.ac.get_user_attribute_name.assert_called_with(100)


def test_sets_attribute_keys(cadwork) -> None:
    Element.attribute_keys[100] = "New Value"
    cadwork.ac.set_user_attribute_name.assert_called_once_with(100, "New Value")


def test_deletes_attribute_keys(cadwork) -> None:
    cadwork.ac.get_user_attribute_name.side_effect = lambda x: "Test Value" if x == 100 else f"User{x}"
    with pytest.raises(KeyError):
        del Element.attribute_keys[200]
    cadwork.ac.get_user_attribute_name.assert_called_once_with(200)
    cadwork.ac.set_user_attribute_name.assert_not_called()
    del Element.attribute_keys[100]
    cadwork.ac.get_user_attribute_name.assert_called_with(100)
    cadwork.ac.set_user_attribute_name.assert_called_with(100, "")


def test_raises_on_iterate_attribute_keys() -> None:
    with pytest.raises(TypeError):
        _ = list(Element.attribute_keys.keys())
    with pytest.raises(TypeError):
        _ = len(Element.attribute_keys)


def test_contains_data(cadwork) -> None:
    cadwork.ac.get_additional_data.side_effect = lambda _, x: "Test Value" if x == "existingKey" else ""
    element = Element(123)
    assert "missingKey" not in element.data
    cadwork.ac.get_additional_data.assert_called_once_with(123, "missingKey")
    assert "existingKey" in element.data
    cadwork.ac.get_additional_data.assert_called_with(123, "existingKey")


def test_gets_data(cadwork) -> None:
    cadwork.ac.get_additional_data.side_effect = lambda _, x: "Test Value" if x == "existingKey" else ""
    element = Element(123)
    with pytest.raises(KeyError):
        _ = element.data["missingKey"]
    cadwork.ac.get_additional_data.assert_called_once_with(123, "missingKey")
    assert element.data["existingKey"] == "Test Value"
    cadwork.ac.get_additional_data.assert_called_with(123, "existingKey")


def test_sets_data(cadwork) -> None:
    element = Element(123)
    element.data["newKey"] = "New Value"
    cadwork.ac.set_additional_data.assert_called_once_with([123], "newKey", "New Value")


def test_deletes_data(cadwork) -> None:
    cadwork.ac.get_additional_data.side_effect = lambda _, x: "Test Value" if x == "existingKey" else ""
    element = Element(123)
    with pytest.raises(KeyError):
        del element.data["missingKey"]
    cadwork.ac.get_additional_data.assert_called_once_with(123, "missingKey")
    cadwork.ac.delete_additional_data.assert_not_called()
    del element.data["existingKey"]
    cadwork.ac.get_additional_data.assert_called_with(123, "existingKey")
    cadwork.ac.delete_additional_data.assert_called_with([123], "existingKey")


def test_raises_on_iterate_data() -> None:
    element = Element(123)
    with pytest.raises(TypeError):
        _ = list(element.data.keys())
    with pytest.raises(TypeError):
        _ = len(element.data)


def test_raises_on_adding_self_to_children() -> None:
    parent = Element(123)
    with pytest.raises(ValueError, match=r"Cannot add Element.+ as a child of Cadwork element #123"):
        parent.children.add(parent)


def test_gets_children(cadwork) -> None:
    parent = Element(123)

    # Without value
    cadwork.ec.get_container_content_elements.return_value = []
    assert len(parent.children) == 0
    cadwork.ec.get_container_content_elements.assert_called_once_with(123)
    assert list(parent.children) == []
    assert Element(789) not in parent.children
    cadwork.ec.get_container_content_elements.reset_mock()

    # With value
    cadwork.cadwork.element_type.return_value.is_wall.return_value = True
    cadwork.ec.get_container_content_elements.return_value = [456, 789]
    assert len(parent.children) == 2
    cadwork.ec.get_container_content_elements.assert_called_once_with(123)
    assert {x.id for x in parent.children} == {456, 789}
    assert Wall(789) in parent.children
    assert Wall(100) not in parent.children


def test_adds_children(cadwork) -> None:
    cadwork.ec.get_container_content_elements.return_value = [456]
    parent = Element(123)

    # Existing child
    parent.children.add(Element(456))
    cadwork.ec.get_container_content_elements.assert_called_once_with(123)
    cadwork.ec.set_container_contents.assert_not_called()
    cadwork.ec.get_container_content_elements.reset_mock()

    # Non-existing child
    parent.children.add(Element(789))
    cadwork.ec.get_container_content_elements.assert_called_once_with(123)
    cadwork.ec.set_container_contents.assert_called_once_with(123, [456, 789])


def test_removes_children(cadwork) -> None:
    cadwork.ec.get_container_content_elements.return_value = [456]
    parent = Element(123)

    # Existing child
    parent.children.discard(Element(456))
    cadwork.ec.get_container_content_elements.assert_called_once_with(123)
    cadwork.ec.set_container_contents.assert_called_once_with(123, [])
    cadwork.ec.get_container_content_elements.reset_mock()
    cadwork.ec.set_container_contents.reset_mock()

    # Non-existing child
    parent.children.discard(Element(789))
    cadwork.ec.get_container_content_elements.assert_called_once_with(123)
    cadwork.ec.set_container_contents.assert_not_called()


def test_deletes_element(cadwork) -> None:
    element = Element(123)

    # Outside batch update context
    element.delete()
    cadwork.ec.delete_elements.assert_called_once_with([123])
    cadwork.ec.delete_elements_with_undo.assert_not_called()
    cadwork.ec.delete_elements.reset_mock()
    cadwork.ec.delete_elements_with_undo.reset_mock()

    # Inside batch update context
    with BatchUpdate():
        element.delete()
    cadwork.ec.delete_elements.assert_not_called()
    cadwork.ec.delete_elements_with_undo.assert_called_once_with([123])


def test_equals() -> None:
    a = Element(123)
    b = FakeElementForRepr(123)
    c = Element(456)
    assert a == a
    assert a == b
    assert a != c
    assert b != c
    assert a is not b


def test_hash() -> None:
    a = Element(123)
    b = FakeElementForRepr(123)
    c = Element(456)
    assert hash(a) == hash(b)
    assert hash(a) != hash(c)
    assert hash(b) != hash(c)
    assert len({a, b, c}) == 2


def test_repr(cadwork) -> None:
    cadwork.ac.get_name.return_value = "Something"
    element = Element(123)
    assert repr(element) == "Element(id=123, name='Something')"
    element = FakeElementForRepr(321)
    assert repr(element) == "FakeElementForRepr(id=321, name='Something')"
