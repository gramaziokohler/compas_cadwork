from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Final
from typing import Literal
from typing import TypeAlias
from typing import get_args

import attribute_controller as ac
import element_controller as ec

from .beam import Beam
from .dimensional_element import DimensionalElement
from .element import Element
from .element_type import ElementType
from .floor import Floor
from .oriented_element import OrientedElement
from .panel import Panel
from .roof import Roof
from .wall import Wall


if TYPE_CHECKING:
    from cadwork import ElementId


_BasicElementTypes: TypeAlias = Literal[
    ElementType.ADDITIONAL,
    ElementType.AUXILIARY,
    ElementType.CONNECTOR_NODE,
    ElementType.CONTAINER,
    ElementType.EXPORT_SOLID,
    ElementType.EXPORT_SOLID_SCENE,
    ElementType.NESTING_PARENT,
    ElementType.NONE,
    ElementType.NORMAL_NODE,
    ElementType.ROOM,
    ElementType.SECTION_TRACE,
    ElementType.TEXT_DOCUMENT,
]

_OrientedElementTypes: TypeAlias = Literal[
    ElementType.CIRCULAR_AXIS,
    ElementType.CONNECTOR_AXIS,
    ElementType.DIMENSION,
    ElementType.DRILLING_AXIS,
    ElementType.EAVE_AXIS,
    ElementType.GLOBAL_CUT,
    ElementType.LINE,
    ElementType.RECTANGULAR_AXIS,
    ElementType.ROTATION_ELEMENT,
    ElementType.SURFACE,
    ElementType.WIRE_AXIS,
]

_DimensionalElementTypes: TypeAlias = Literal[ElementType.OPENING]

AnyElement: TypeAlias = (
    Element[_BasicElementTypes]
    | OrientedElement[_OrientedElementTypes]
    | DimensionalElement[_DimensionalElementTypes]
    | Beam
    | Floor
    | Panel
    | Roof
    | Wall
)

_BASIC_ELEMENT_TYPES: Final = frozenset(get_args(_BasicElementTypes))
_ORIENTED_ELEMENT_TYPES: Final = frozenset(get_args(_OrientedElementTypes))
_DIMENSIONAL_ELEMENT_TYPES: Final = frozenset(get_args(_DimensionalElementTypes))


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

    # Specific elements
    if element_type in (ElementType.CIRCULAR_BEAM, ElementType.POLYGONAL_BEAM):
        return Beam(cadwork_id)
    if element_type == ElementType.FLOOR:
        return Floor(cadwork_id)
    if element_type == ElementType.PANEL:
        return Panel(cadwork_id)
    if element_type == ElementType.ROOF:
        return Roof(cadwork_id)
    if element_type == ElementType.WALL:
        return Wall(cadwork_id)

    # Generic elements
    if element_type in _BASIC_ELEMENT_TYPES:
        return Element(cadwork_id)
    if element_type in _ORIENTED_ELEMENT_TYPES:
        return OrientedElement(cadwork_id)
    if element_type in _DIMENSIONAL_ELEMENT_TYPES:
        return DimensionalElement(cadwork_id)

    # Base case (this should never happen)
    raise ValueError(f"Unmapped type {element_type.name!r} for Cadwork element with ID #{cadwork_id}")
