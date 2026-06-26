from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Literal
from typing import TypeAlias

import attribute_controller as ac
import element_controller as ec

from .beam import Beam
from .element import Element
from .element_type import ElementType
from .panel import Panel
from .wall import Wall


if TYPE_CHECKING:
    from cadwork import ElementId


_GenericElementTypes: TypeAlias = Literal[
    ElementType.ADDITIONAL,
    ElementType.AUXILIARY,
    ElementType.CADWORK,
    ElementType.CIRCULAR_AXIS,
    ElementType.CONNECTOR_AXIS,
    ElementType.CONNECTOR_NODE,
    ElementType.CONTAINER,
    ElementType.DIMENSION,
    ElementType.DRILLING_AXIS,
    ElementType.EAVE_AXIS,
    ElementType.EXPORT_SOLID,
    ElementType.EXPORT_SOLID_SCENE,
    ElementType.FLOOR,
    ElementType.GLOBAL_CUT,
    ElementType.LINE,
    ElementType.NESTING_PARENT,
    ElementType.NONE,
    ElementType.NORMAL_NODE,
    ElementType.OPENING,
    ElementType.RECTANGULAR_AXIS,
    ElementType.ROOF,
    ElementType.ROOM,
    ElementType.ROTATION_ELEMENT,
    ElementType.SECTION_TRACE,
    ElementType.SURFACE,
    ElementType.TEXT_DOCUMENT,
    ElementType.WIRE_AXIS,
]

AnyElement: TypeAlias = Element[_GenericElementTypes] | Beam | Panel | Wall


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
        If the element does not exist or has an unknown type.
    """
    if not ec.check_element_id(cadwork_id):
        raise ValueError(f"Could not find a Cadwork element with ID #{cadwork_id}")
    raw_type = ac.get_element_type(cadwork_id)
    element_type = ElementType.from_cadwork(raw_type)
    if element_type == ElementType.CIRCULAR_BEAM or element_type == ElementType.POLYGONAL_BEAM:
        return Beam(cadwork_id)
    if element_type == ElementType.PANEL:
        return Panel(cadwork_id)
    if element_type == ElementType.WALL:
        return Wall(cadwork_id)
    return Element(cadwork_id)
