from __future__ import annotations

from enum import Enum
from enum import auto
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import cadwork


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
    POLYGONAL_BEAM = auto()
    RECTANGULAR_AXIS = auto()
    ROOF = auto()
    ROOM = auto()
    ROTATION_ELEMENT = auto()
    SECTION_TRACE = auto()
    SURFACE = auto()
    TEXT_DOCUMENT = auto()
    WALL = auto()
    WIRE_AXIS = auto()

    @classmethod
    def from_cadwork(cls, raw_type: cadwork.element_type) -> ElementType:
        """Get value from Cadwork element type.

        Parameters
        ----------
        raw_type : cadwork.element_type
            Cadwork element type.

        Returns
        -------
        ElementType
            Element type.

        Raises
        ------
        ValueError
            If cannot determine the correct mapping type.
        """
        if raw_type.is_additional_element():
            return cls.ADDITIONAL
        if raw_type.is_auxiliary():
            return cls.AUXILIARY
        if raw_type.is_cadwork():
            return cls.CADWORK
        if raw_type.is_circular_axis():
            return cls.CIRCULAR_AXIS
        if raw_type.is_circular_beam():
            return cls.CIRCULAR_BEAM
        if raw_type.is_connector_axis():
            return cls.CONNECTOR_AXIS
        if raw_type.is_connector_node():
            return cls.CONNECTOR_NODE
        if raw_type.is_container():
            return cls.CONTAINER
        if raw_type.is_dimension():
            return cls.DIMENSION
        if raw_type.is_drilling_axis():
            return cls.DRILLING_AXIS
        if raw_type.is_eave_axis():
            return cls.EAVE_AXIS
        if raw_type.is_export_solid():
            return cls.EXPORT_SOLID
        if raw_type.is_export_solid_scene():
            return cls.EXPORT_SOLID_SCENE
        if raw_type.is_floor():
            return cls.FLOOR
        if raw_type.is_global_cut():
            return cls.GLOBAL_CUT
        if raw_type.is_line():
            return cls.LINE
        if raw_type.is_nesting_parent():
            return cls.NESTING_PARENT
        if raw_type.is_none():
            return cls.NONE
        if raw_type.is_normal_node():
            return cls.NORMAL_NODE
        if raw_type.is_opening():
            return cls.OPENING
        if raw_type.is_panel():
            return cls.PANEL
        if raw_type.is_rectangular_axis():
            return cls.RECTANGULAR_AXIS
        if raw_type.is_rectangular_beam():
            return cls.POLYGONAL_BEAM
        if raw_type.is_roof():
            return cls.ROOF
        if raw_type.is_room():
            return cls.ROOM
        if raw_type.is_rotation_element():
            return cls.ROTATION_ELEMENT
        if raw_type.is_section_trace():
            return cls.SECTION_TRACE
        if raw_type.is_surface():
            return cls.SURFACE
        if raw_type.is_text_document():
            return cls.TEXT_DOCUMENT
        if raw_type.is_wall():
            return cls.WALL
        if raw_type.is_wire_axis():
            return cls.WIRE_AXIS
        raise ValueError("Unknown Cadwork element type")
