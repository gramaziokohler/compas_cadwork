import pytest
from typing_extensions import assert_type

from compas_cadwork.elements.beam import Beam
from compas_cadwork.elements.element import Element
from compas_cadwork.elements.element_type import ElementType
from compas_cadwork.elements.factory import _BasicElementTypes
from compas_cadwork.elements.factory import _OrientedElementTypes
from compas_cadwork.elements.factory import get_element_instance
from compas_cadwork.elements.floor import Floor
from compas_cadwork.elements.line import Line
from compas_cadwork.elements.node import Node
from compas_cadwork.elements.opening import Opening
from compas_cadwork.elements.oriented_element import OrientedElement
from compas_cadwork.elements.panel import Panel
from compas_cadwork.elements.roof import Roof
from compas_cadwork.elements.wall import Wall


def test_gets_basic_element_class(cadwork) -> None:
    cadwork.ec.check_element_id.return_value = True
    cadwork.cadwork.element_type.return_value.is_text_document.return_value = True
    element = get_element_instance(123)
    assert element.type == ElementType.TEXT_DOCUMENT
    assert_type(element, Element[_BasicElementTypes])
    assert type(element) is Element


def test_gets_oriented_element_class(cadwork) -> None:
    cadwork.ec.check_element_id.return_value = True
    cadwork.cadwork.element_type.return_value.is_wire_axis.return_value = True
    element = get_element_instance(123)
    assert element.type == ElementType.WIRE_AXIS
    assert_type(element, OrientedElement[_OrientedElementTypes])
    assert type(element) is OrientedElement


@pytest.mark.parametrize(
    "element_type, expected_class, mock_method",
    [
        (ElementType.CIRCULAR_BEAM, Beam, "is_circular_beam"),
        (ElementType.POLYGONAL_BEAM, Beam, "is_rectangular_beam"),
        (ElementType.FLOOR, Floor, "is_floor"),
        (ElementType.LINE, Line, "is_line"),
        (ElementType.CONNECTOR_NODE, Node, "is_connector_node"),
        (ElementType.NORMAL_NODE, Node, "is_normal_node"),
        (ElementType.OPENING, Opening, "is_opening"),
        (ElementType.PANEL, Panel, "is_panel"),
        (ElementType.ROOF, Roof, "is_roof"),
        (ElementType.WALL, Wall, "is_wall"),
    ],
)
def test_gets_specific_element_class(cadwork, element_type, expected_class, mock_method) -> None:
    cadwork.ec.check_element_id.return_value = True
    getattr(cadwork.cadwork.element_type.return_value, mock_method).return_value = True
    element = get_element_instance(123)
    assert element.type == element_type
    assert type(element) is expected_class


def test_raises_on_invalid_cadwork_id(cadwork) -> None:
    cadwork.ec.check_element_id.return_value = False
    with pytest.raises(ValueError, match=r"Could not find a Cadwork element with ID #123"):
        _ = get_element_instance(123)
    cadwork.ec.check_element_id.assert_called_once_with(123)


def test_raises_on_invalid_element_type(cadwork) -> None:
    cadwork.ec.check_element_id.return_value = True
    with pytest.raises(ValueError, match=r"Unknown Cadwork element type"):
        _ = get_element_instance(123)
