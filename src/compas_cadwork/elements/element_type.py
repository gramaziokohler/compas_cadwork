from enum import Enum
from enum import auto


class ElementType(Enum):
    """Cadwork element type."""

    ADDITIONAL = auto()
    AUXILIARY = auto()
    CADWORK = auto()
    CIRCULAR_AXIS = auto()
    CIRCULAR_BEAM = auto()
    CONNECTOR_AXIS = auto()
    CONNECTOR_NODE = auto()
    CONTAINER = auto()
    DIMENSION = auto()
    DRILLING_AXIS = auto()
    EAVE_AXIS = auto()
    EXPORT_SOLID = auto()
    EXPORT_SOLID_SCENE = auto()
    FLOOR = auto()
    GLOBAL_CUT = auto()
    LINE = auto()
    NESTING_PARENT = auto()
    NONE = auto()
    NORMAL_NODE = auto()
    OPENING = auto()
    PANEL = auto()
    RECTANGULAR_AXIS = auto()
    RECTANGULAR_BEAM = auto()
    ROOF = auto()
    ROOM = auto()
    ROTATION_ELEMENT = auto()
    SECTION_TRACE = auto()
    SURFACE = auto()
    TEXT_DOCUMENT = auto()
    WALL = auto()
    WIRE_AXIS = auto()
