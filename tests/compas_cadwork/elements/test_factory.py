from typing import assert_type

import pytest

from compas_cadwork.elements.beam import Beam
from compas_cadwork.elements.dimensional_element import DimensionalElement
from compas_cadwork.elements.element import Element
from compas_cadwork.elements.element_type import ElementType
from compas_cadwork.elements.factory import _BasicElementTypes
from compas_cadwork.elements.factory import _DimensionalElementTypes
from compas_cadwork.elements.factory import _OrientedElementTypes
from compas_cadwork.elements.factory import get_element_instance
from compas_cadwork.elements.oriented_element import OrientedElement
from compas_cadwork.elements.wall import Wall


def test_gets_the_correct_element_class(cadwork) -> None:
    cadwork.ec.check_element_id.return_value = True

    # For beams
    cadwork.cadwork.element_type.is_rectangular_beam.return_value = True
    element = get_element_instance(123)
    assert element.type == ElementType.POLYGONAL_BEAM
    assert_type(element, Beam)
    assert type(element) is Beam
    cadwork.cadwork.element_type.is_rectangular_beam.return_value = False

    # For walls
    cadwork.cadwork.element_type.is_wall.return_value = True
    element = get_element_instance(123)
    assert element.type == ElementType.WALL
    assert_type(element, Wall)
    assert type(element) is Wall
    cadwork.cadwork.element_type.is_wall.return_value = False

    # For generic basic elements
    cadwork.cadwork.element_type.is_text_document.return_value = True
    element = get_element_instance(123)
    assert element.type == ElementType.TEXT_DOCUMENT
    assert_type(element, Element[_BasicElementTypes])
    assert type(element) is Element
    cadwork.cadwork.element_type.is_text_document.return_value = False

    # For generic oriented elements
    cadwork.cadwork.element_type.is_wire_axis.return_value = True
    element = get_element_instance(123)
    assert element.type == ElementType.WIRE_AXIS
    assert_type(element, OrientedElement[_OrientedElementTypes])
    assert type(element) is OrientedElement
    cadwork.cadwork.element_type.is_wire_axis.return_value = False

    # For generic dimensional elements
    cadwork.cadwork.element_type.is_floor.return_value = True
    element = get_element_instance(123)
    assert element.type == ElementType.FLOOR
    assert_type(element, DimensionalElement[_DimensionalElementTypes])
    assert type(element) is DimensionalElement
    cadwork.cadwork.element_type.is_floor.return_value = False


def test_raises_on_invalid_cadwork_id(cadwork) -> None:
    cadwork.ec.check_element_id.return_value = False
    with pytest.raises(ValueError, match=r"Could not find a Cadwork element with ID #123"):
        _ = get_element_instance(123)
    cadwork.ec.check_element_id.assert_called_once_with(123)


def test_raises_on_invalid_element_type(cadwork) -> None:
    cadwork.ec.check_element_id.return_value = True
    with pytest.raises(ValueError, match=r"Unknown Cadwork element type"):
        _ = get_element_instance(123)
