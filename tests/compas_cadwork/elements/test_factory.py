from typing import assert_type

import pytest

from compas_cadwork.elements.beam import Beam
from compas_cadwork.elements.element import Element
from compas_cadwork.elements.element_type import ElementType
from compas_cadwork.elements.factory import get_element_instance
from compas_cadwork.elements.wall import Wall


def test_gets_the_correct_element_class(cadwork) -> None:
    # For beams
    cadwork.cadwork.element_type.is_rectangular_beam.return_value = True
    cadwork.ec.check_element_id.return_value = True
    element = get_element_instance(123)
    assert element.type == ElementType.RECTANGULAR_BEAM
    assert_type(element, Beam)
    assert isinstance(element, Beam)
    cadwork.cadwork.element_type.is_rectangular_beam.return_value = False

    # For walls
    cadwork.cadwork.element_type.is_wall.return_value = True
    cadwork.ec.check_element_id.return_value = True
    element = get_element_instance(123)
    assert element.type == ElementType.WALL
    assert_type(element, Wall)
    assert isinstance(element, Wall)
    cadwork.cadwork.element_type.is_wall.return_value = False

    # For generic elements
    cadwork.cadwork.element_type.is_room.return_value = True
    cadwork.ec.check_element_id.return_value = True
    element = get_element_instance(123)
    assert element.type == ElementType.ROOM
    assert isinstance(element, Element)
    cadwork.cadwork.element_type.is_room.return_value = False


def test_raises_on_invalid_cadwork_id(cadwork) -> None:
    cadwork.ec.check_element_id.return_value = False
    with pytest.raises(ValueError, match=r"Could not find a Cadwork element with ID #123"):
        _ = get_element_instance(123)
    cadwork.ec.check_element_id.assert_called_once_with(123)


def test_raises_on_invalid_element_type(cadwork) -> None:
    cadwork.ec.check_element_id.return_value = True
    with pytest.raises(ValueError, match=r"Unknown Cadwork element type"):
        _ = get_element_instance(123)
