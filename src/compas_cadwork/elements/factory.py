from __future__ import annotations

from typing import TYPE_CHECKING
from typing import TypeAlias

import attribute_controller as ac
import element_controller as ec

from .beam import Beam
from .element import Element
from .wall import Wall


if TYPE_CHECKING:
    from cadwork import ElementId


AnyElement: TypeAlias = Element | Beam | Wall


def get_element_instance(cadwork_id: ElementId) -> AnyElement:
    """Get element from Cadwork ID.

    Parameters
    ----------
    cadwork_id : ElementId
        Cadwork element ID.

    Returns
    -------
    AnyElement
        Cadwork element.

    Raises
    ------
    ValueError
        If the element does not exist.
    """
    if not ec.check_element_id(cadwork_id):
        raise ValueError(f"Could not find a Cadwork element with ID #{cadwork_id}")
    raw_type = ac.get_element_type(cadwork_id)
    if raw_type.is_circular_beam() or raw_type.is_rectangular_beam():
        return Beam(cadwork_id)
    if raw_type.is_wall():
        return Wall(cadwork_id)
    return Element(cadwork_id)
