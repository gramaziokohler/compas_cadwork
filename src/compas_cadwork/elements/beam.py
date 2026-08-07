from __future__ import annotations

from typing import Literal

import cadwork
import element_controller as ec
from compas.geometry import Frame
from compas.geometry import Polygon
from compas.geometry import Translation
from compas.geometry import bounding_box_xy

from compas_cadwork.conversions.primitives import point_to_cadwork
from compas_cadwork.conversions.primitives import vector_to_cadwork
from compas_cadwork.transaction import notify_element_creation

from .dimensional_element import DimensionalElement
from .element_type import ElementType


class Beam(DimensionalElement[Literal[ElementType.CIRCULAR_BEAM, ElementType.POLYGONAL_BEAM]]):
    """Beam element."""

    @classmethod
    def circular(cls, frame: Frame, length: float, diameter: float) -> Beam:
        """Create circular beam.

        Parameters
        ----------
        frame : Frame
            Local coordinate system of the element.
        length : float
            Length in millimeters (along X-axis).
        diameter : float
            Section diameter in millimeters (along Y/Z-axes).

        Returns
        -------
        Beam
            New beam element.

        Raises
        ------
        ValueError
            If any of the dimensions are not positive.
        """
        if length <= 0:
            raise ValueError("The beam length must be positive")
        if diameter <= 0:
            raise ValueError("The beam diameter must be positive")
        element_id = ec.create_circular_beam_vectors(
            diameter,
            length,
            point_to_cadwork(frame.point),
            vector_to_cadwork(frame.xaxis),
            vector_to_cadwork(frame.zaxis),
        )
        notify_element_creation(element_id)
        return cls(element_id)

    @classmethod
    def polygonal(cls, frame: Frame, length: float, section: Polygon) -> Beam:
        """Create polygonal beam.

        Parameters
        ----------
        frame : Frame
            Local coordinate system of the element.
        length : float
            Length in millimeters (along X-axis).
        section : Polygon
            Polygon defining the section. Note that the Z coordinate of its points must be zero.

        Returns
        -------
        Beam
            New beam element.

        Raises
        ------
        ValueError
            If the Z coordinate of any of the polygon points is not zero, or if the length is not positive.
        """
        if length <= 0:
            raise ValueError("The beam length must be positive")
        for point in section.points:
            if point.z != 0:
                raise ValueError("The Z coordinate of all polygon points defining the section must be zero")

        # Normalize section to center it at the origin
        section_bbox = bounding_box_xy(section.points)
        section_cx = (section_bbox[0][0] + section_bbox[2][0]) / 2
        section_cy = (section_bbox[0][1] + section_bbox[2][1]) / 2
        centered_section: Polygon = section.transformed(Translation.from_vector([-section_cx, -section_cy, 0]))

        # Translate centered section to world coordinates
        vertices = cadwork.vertex_list()
        start_point = frame.point + frame.xaxis * (length / 2)
        for point in centered_section.points:
            world_point = start_point + frame.zaxis * point.x + frame.yaxis * point.y
            vertices.append(point_to_cadwork(world_point))

        # Create beam
        element_id = ec.create_polygon_beam(
            vertices,
            length,
            vector_to_cadwork(frame.xaxis),
            vector_to_cadwork(frame.zaxis),
        )
        notify_element_creation(element_id)
        return cls(element_id)

    @classmethod
    def rectangular(cls, frame: Frame, length: float, width: float, height: float) -> Beam:
        """Create rectangular beam.

        Parameters
        ----------
        frame : Frame
            Local coordinate system of the element.
        length : float
            Length in millimeters (along X-axis).
        width : float
            Section width in millimeters (along Y-axis).
        height : float
            Section height in millimeters (along Z-axis).

        Returns
        -------
        Beam
            New beam element.

        Raises
        ------
        ValueError
            If any of the dimensions are not positive.
        """
        if length <= 0:
            raise ValueError("The beam length must be positive")
        if width <= 0:
            raise ValueError("The beam width must be positive")
        if height <= 0:
            raise ValueError("The beam height must be positive")
        element_id = ec.create_rectangular_beam_vectors(
            width,
            height,
            length,
            point_to_cadwork(frame.point),
            vector_to_cadwork(frame.xaxis),
            vector_to_cadwork(frame.zaxis),
        )
        notify_element_creation(element_id)
        return cls(element_id)
