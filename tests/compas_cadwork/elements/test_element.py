from uuid import UUID

import pytest
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector

from compas_cadwork.elements.element import Element
from compas_cadwork.ifc_uuid import IfcUUID


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


def test_gets_frame(cadwork) -> None:
    cadwork.gc.get_p1.return_value = cadwork.cadwork.point_3d(10.1, 20.2, 30.3)
    cadwork.gc.get_xl.return_value = cadwork.cadwork.point_3d(-1.0, 0.0, 0.0)
    cadwork.gc.get_yl.return_value = cadwork.cadwork.point_3d(0.0, -0.0, 1.0)
    element = Element(123)
    assert element.frame == Frame(Point(10.1, 20.2, 30.3), Vector(-1.0, 0.0, 0.0), Vector(0.0, -0.0, 1.0))
    cadwork.gc.get_p1.assert_called_once_with(123)
    cadwork.gc.get_xl.assert_called_once_with(123)
    cadwork.gc.get_yl.assert_called_once_with(123)


def test_gets_width(cadwork) -> None:
    cadwork.gc.get_width.return_value = 1000.23
    element = Element(123)
    assert element.width == 1000.23
    cadwork.gc.get_width.assert_called_once_with(123)


def test_sets_width(cadwork) -> None:
    element = Element(123)
    element.width = 543.21
    cadwork.gc.set_width_real.assert_called_once_with([123], 543.21)


def test_gets_height(cadwork) -> None:
    cadwork.gc.get_height.return_value = 1000.23
    element = Element(123)
    assert element.height == 1000.23
    cadwork.gc.get_height.assert_called_once_with(123)


def test_sets_height(cadwork) -> None:
    element = Element(123)
    element.height = 543.21
    cadwork.gc.set_height_real.assert_called_once_with([123], 543.21)


def test_gets_length(cadwork) -> None:
    cadwork.gc.get_length.return_value = 1000.23
    element = Element(123)
    assert element.length == 1000.23
    cadwork.gc.get_length.assert_called_once_with(123)


def test_sets_length(cadwork) -> None:
    element = Element(123)
    element.length = 543.21
    cadwork.gc.set_length_real.assert_called_once_with([123], 543.21)


def test_gets_centerline(cadwork) -> None:
    cadwork.gc.get_p1.return_value = cadwork.cadwork.point_3d(10.1, 20.2, 30.3)
    cadwork.gc.get_p2.return_value = cadwork.cadwork.point_3d(100.1, 200.2, 300.3)
    element = Element(123)
    assert element.centerline == Line(Point(10.1, 20.2, 30.3), Point(100.1, 200.2, 300.3))
    cadwork.gc.get_p1.assert_called_once_with(123)
    cadwork.gc.get_p2.assert_called_once_with(123)


def test_translates_element(cadwork) -> None:
    element = Element(123)
    element.translate(Vector(100.0, 200.0, 300.0))
    cadwork.ec.move_element.assert_called_once_with([123], cadwork.cadwork.point_3d(100.0, 200.0, 300.0))


def test_duplicates_element(cadwork) -> None:
    cadwork.ec.copy_elements.return_value = [124]
    element = Element(123)
    new_element = element.duplicate(Vector(100.0, 200.0, 300.0))
    assert new_element is not element
    assert new_element.id == 124
    cadwork.ec.copy_elements.assert_called_once_with([123], cadwork.cadwork.point_3d(100.0, 200.0, 300.0))


def test_deletes_element(cadwork) -> None:
    element = Element(123)
    element.delete()
    cadwork.ec.delete_elements.assert_called_once_with([123])


def test_repr(cadwork) -> None:
    element = Element(123)
    cadwork.ac.get_name.return_value = "Something"
    assert repr(element) == "Element(id=123, name='Something')"
