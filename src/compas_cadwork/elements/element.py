from __future__ import annotations

from typing import Literal

import attribute_controller as ac

from .base_element import BaseElement
from .element_type import ElementType


class Element(BaseElement):
    """Generic Cadwork element.

    Class that represents a Cadwork element without a more specific implementation in the library.
    """

    @property
    def type(
        self,
    ) -> Literal[
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
        ElementType.PANEL,
        ElementType.RECTANGULAR_AXIS,
        ElementType.ROOF,
        ElementType.ROOM,
        ElementType.ROTATION_ELEMENT,
        ElementType.SECTION_TRACE,
        ElementType.SURFACE,
        ElementType.TEXT_DOCUMENT,
        ElementType.WIRE_AXIS,
    ]:
        raw_type = ac.get_element_type(self.id)
        if raw_type.is_additional_element():
            return ElementType.ADDITIONAL
        if raw_type.is_auxiliary():
            return ElementType.AUXILIARY
        if raw_type.is_cadwork():
            return ElementType.CADWORK
        if raw_type.is_circular_axis():
            return ElementType.CIRCULAR_AXIS
        if raw_type.is_connector_axis():
            return ElementType.CONNECTOR_AXIS
        if raw_type.is_connector_node():
            return ElementType.CONNECTOR_NODE
        if raw_type.is_container():
            return ElementType.CONTAINER
        if raw_type.is_dimension():
            return ElementType.DIMENSION
        if raw_type.is_drilling_axis():
            return ElementType.DRILLING_AXIS
        if raw_type.is_eave_axis():
            return ElementType.EAVE_AXIS
        if raw_type.is_export_solid():
            return ElementType.EXPORT_SOLID
        if raw_type.is_export_solid_scene():
            return ElementType.EXPORT_SOLID_SCENE
        if raw_type.is_floor():
            return ElementType.FLOOR
        if raw_type.is_global_cut():
            return ElementType.GLOBAL_CUT
        if raw_type.is_line():
            return ElementType.LINE
        if raw_type.is_nesting_parent():
            return ElementType.NESTING_PARENT
        if raw_type.is_none():
            return ElementType.NONE
        if raw_type.is_normal_node():
            return ElementType.NORMAL_NODE
        if raw_type.is_opening():
            return ElementType.OPENING
        if raw_type.is_panel():
            return ElementType.PANEL
        if raw_type.is_rectangular_axis():
            return ElementType.RECTANGULAR_AXIS
        if raw_type.is_roof():
            return ElementType.ROOF
        if raw_type.is_room():
            return ElementType.ROOM
        if raw_type.is_rotation_element():
            return ElementType.ROTATION_ELEMENT
        if raw_type.is_section_trace():
            return ElementType.SECTION_TRACE
        if raw_type.is_surface():
            return ElementType.SURFACE
        if raw_type.is_text_document():
            return ElementType.TEXT_DOCUMENT
        if raw_type.is_wire_axis():
            return ElementType.WIRE_AXIS
        raise ValueError(f"Could not determine the element type for Cadwork element with ID {self.id}")
