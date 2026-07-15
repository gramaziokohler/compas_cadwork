from unittest import mock

import pytest

from compas_cadwork.elements.container import Container
from compas_cadwork.elements.element import Element
from compas_cadwork.elements.mixins.aggregate_mixin import AggregateMixin
from compas_cadwork.elements.mixins.aggregate_mixin import _ContainerElementChildren
from compas_cadwork.elements.mixins.aggregate_mixin import _GroupElementChildren


class DummyElement(Element, AggregateMixin):
    pass


def test_uses_proper_children_implementation(cadwork) -> None:
    # For container parent element
    element = DummyElement(123)
    cadwork.cadwork.element_type.is_container.return_value = True
    assert isinstance(element.children, _ContainerElementChildren)
    cadwork.cadwork.element_type.is_container.return_value = False

    # For group parent element
    element = DummyElement(123)
    cadwork.cadwork.element_type.is_wall.return_value = True
    assert isinstance(element.children, _GroupElementChildren)
    cadwork.cadwork.element_type.is_wall.return_value = False


def test_raises_on_adding_self_to_children(cadwork) -> None:
    # For container parent element
    cadwork.cadwork.element_type.is_container.return_value = True
    parent = DummyElement(123)
    with pytest.raises(ValueError, match=r"Cannot add DummyElement.+ as a child of DummyElement"):
        parent.children.add(parent)
    cadwork.cadwork.element_type.is_container.return_value = False

    # For group parent element
    cadwork.cadwork.element_type.is_wall.return_value = True
    parent = DummyElement(123)
    with pytest.raises(ValueError, match=r"Cannot add DummyElement.+ as a child of DummyElement"):
        parent.children.add(parent)
    cadwork.cadwork.element_type.is_wall.return_value = False


def test_gets_children_from_container_element(cadwork) -> None:
    cadwork.cadwork.element_type.is_container.return_value = True
    parent = DummyElement(123)

    # Without value
    cadwork.ec.get_container_content_elements.return_value = []
    assert len(parent.children) == 0
    cadwork.ec.get_container_content_elements.assert_called_once_with(123)
    assert list(parent.children) == []
    assert Container(789) not in parent.children
    cadwork.ec.get_container_content_elements.reset_mock()

    # With value
    cadwork.ec.get_container_content_elements.return_value = [456, 789]
    assert len(parent.children) == 2
    cadwork.ec.get_container_content_elements.assert_called_once_with(123)
    assert {x.id for x in parent.children} == {456, 789}
    assert Container(789) in parent.children
    assert Container(100) not in parent.children


def test_adds_children_to_container_element(cadwork) -> None:
    cadwork.cadwork.element_type.is_container.return_value = True
    cadwork.ec.get_container_content_elements.return_value = [456]
    parent = DummyElement(123)

    # Existing child
    parent.children.add(Element(456))
    cadwork.ec.get_container_content_elements.assert_called_once_with(123)
    cadwork.ec.set_container_contents.assert_not_called()
    cadwork.ec.get_container_content_elements.reset_mock()

    # Non-existing child
    parent.children.add(Element(789))
    cadwork.ec.get_container_content_elements.assert_called_once_with(123)
    cadwork.ec.set_container_contents.assert_called_once_with(123, [456, 789])


def test_removes_children_from_container_element(cadwork) -> None:
    cadwork.cadwork.element_type.is_container.return_value = True
    cadwork.ec.get_container_content_elements.return_value = [456]
    parent = DummyElement(123)

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


def test_gets_children_from_group_element(cadwork) -> None:
    cadwork.ac.get_element_grouping_type.return_value = cadwork.cadwork.element_grouping_type.group
    cadwork.cadwork.element_type.is_wall.return_value = True
    parent = DummyElement(123)

    # Without value
    cadwork.ac.get_group.return_value = ""
    assert len(parent.children) == 0
    cadwork.ac.get_group.assert_called_once_with(123)
    assert list(parent.children) == []
    assert Container(789) not in parent.children
    cadwork.ac.get_group.reset_mock()

    # With value
    cadwork.ac.get_group.side_effect = lambda x: "group-name" if x in [123, 456, 789] else ""
    cadwork.ec.filter_elements.return_value = [123, 456, 789]
    assert len(parent.children) == 2
    cadwork.cadwork.element_filter.return_value.set_group.assert_called_once_with("group-name")
    assert {x.id for x in parent.children} == {456, 789}
    assert Container(789) in parent.children
    assert Container(100) not in parent.children


def test_adds_children_to_group_element_with_existing_group(cadwork) -> None:
    cadwork.cadwork.element_type.is_wall.return_value = True
    parent = DummyElement(123)

    cadwork.ac.get_group.side_effect = lambda x: "group-name" if x == 123 else ""
    cadwork.ec.filter_elements.return_value = [123]
    parent.children.add(Element(456))
    cadwork.ac.set_group.assert_called_once_with([456], "group-name")


def test_adds_children_to_group_element_without_existing_group(cadwork) -> None:
    cadwork.cadwork.element_type.is_wall.return_value = True
    cadwork.ec.get_element_cadwork_guid.return_value = "{12345678-AAAA-BBBB-CCCC-DDEE12345678}"
    parent = DummyElement(123)

    # First child
    cadwork.ac.get_group.return_value = ""
    cadwork.ec.filter_elements.return_value = []
    parent.children.add(Element(456))
    cadwork.ac.get_group.assert_called_once_with(123)
    cadwork.ac.set_group.assert_has_calls(
        [
            mock.call([123], "G-12345678-aaaa-bbbb-cccc-ddee12345678"),
            mock.call([456], "G-12345678-aaaa-bbbb-cccc-ddee12345678"),
        ],
    )
    cadwork.ac.set_group.reset_mock()

    # Subsequent children
    cadwork.ac.get_group.side_effect = lambda x: "G-12345678-aaaa-bbbb-cccc-ddee12345678" if x in [123, 456] else ""
    cadwork.ec.filter_elements.return_value = [123, 456]
    parent.children.add(Element(789))
    cadwork.ac.set_group.assert_called_with([789], "G-12345678-aaaa-bbbb-cccc-ddee12345678")


def test_removes_children_from_group_element(cadwork) -> None:
    cadwork.cadwork.element_type.is_wall.return_value = True
    parent = DummyElement(123)

    # Existing child
    cadwork.ac.get_group.side_effect = lambda x: "group-name" if x in [123, 456] else ""
    cadwork.ec.filter_elements.return_value = [123, 456]
    parent.children.discard(Element(456))
    cadwork.ac.set_group.assert_called_once_with([456], "")
    cadwork.ac.set_group.reset_mock()

    # Non-existing child
    cadwork.ac.get_group.side_effect = lambda x: "group-name" if x == 123 else "other-group"
    cadwork.ec.filter_elements.return_value = [123]
    parent.children.discard(Element(789))
    cadwork.ac.set_group.assert_not_called()


def test_clear_default_group_name_if_unused(cadwork) -> None:
    cadwork.cadwork.element_type.is_wall.return_value = True
    cadwork.ec.get_element_cadwork_guid.return_value = "{12345678-AAAA-BBBB-CCCC-DDEE12345678}"
    cadwork.ac.get_group.return_value = "G-12345678-aaaa-bbbb-cccc-ddee12345678"
    cadwork.ec.filter_elements.return_value = [123]
    parent = DummyElement(123)
    _ = len(parent.children)  # Trigger clearing of parent default group name
    cadwork.ac.set_group.assert_called_once_with([123], "")
