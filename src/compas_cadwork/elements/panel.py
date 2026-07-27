from __future__ import annotations

from typing import Literal
from typing import Self

import cadwork
import element_controller as ec
from compas.geometry import Frame
from compas.geometry import Polygon
from compas.geometry import Translation
from compas.geometry import bounding_box_xy
from typing_extensions import TypeVar

from compas_cadwork.batch_update import notify_element_creation
from compas_cadwork.conversions.primitives import point_to_cadwork
from compas_cadwork.conversions.primitives import vector_to_cadwork

from .dimensional_element import DimensionalElement
from .element_type import ElementType


_P = TypeVar("_P", bound=ElementType, default=Literal[ElementType.PANEL])


class Panel(DimensionalElement[_P]):
    """Panel element."""

    @classmethod
    def polygonal(cls, frame: Frame, outline: Polygon, thickness: float) -> Self:
        """Create polygonal element.

        Parameters
        ----------
        frame : Frame
            Local coordinate system of the element.
        outline : Polygon
            Polygon defining the outline. Note that the Z coordinate of its points must be zero.
        thickness : float
            Thickness in millimeters (along Z-axis).

        Returns
        -------
        Self
            New element.

        Raises
        ------
        ValueError
            If the Z coordinate of any of the polygon points is not zero, or if the thickness is not positive.
        """
        for point in outline.points:
            if point.z != 0:
                raise ValueError("The Z coordinate of all polygon points defining the outline must be zero")
        if thickness <= 0:
            raise ValueError("The element thickness must be positive")

        # Normalize outline to center it at the origin
        outline_bbox = bounding_box_xy(outline.points)
        outline_cx = (outline_bbox[0][0] + outline_bbox[2][0]) / 2
        outline_cy = (outline_bbox[0][1] + outline_bbox[2][1]) / 2
        centered_outline: Polygon = outline.transformed(Translation.from_vector([-outline_cx, -outline_cy, 0]))

        # Translate centered outline to world coordinates
        vertices = cadwork.vertex_list()
        start_point = frame.point + frame.xaxis * (thickness / 2)
        for point in [*centered_outline.points, centered_outline.points[0]]:  # Close shape by re-adding first point
            world_point = start_point + frame.zaxis * point.x + frame.yaxis * point.y
            vertices.append(point_to_cadwork(world_point))

        # Create panel
        element_id = ec.create_polygon_panel(
            vertices,
            thickness,
            vector_to_cadwork(frame.xaxis),
            vector_to_cadwork(frame.zaxis),
        )
        notify_element_creation(element_id)
        return cls(element_id)

    @classmethod
    def rectangular(cls, frame: Frame, length: float, width: float, thickness: float) -> Self:
        """Create rectangular element.

        Parameters
        ----------
        frame : Frame
            Local coordinate system of the element.
        length : float
            Length in millimeters (along X-axis).
        width : float
            Width in millimeters (along Y-axis).
        thickness : float
            Thickness in millimeters (along Z-axis).

        Returns
        -------
        Self
            New element.

        Raises
        ------
        ValueError
            If any of the dimensions are not positive.
        """
        if length <= 0:
            raise ValueError("The element length must be positive")
        if width <= 0:
            raise ValueError("The element width must be positive")
        if thickness <= 0:
            raise ValueError("The element thickness must be positive")
        element_id = ec.create_rectangular_panel_vectors(
            width,
            thickness,
            length,
            point_to_cadwork(frame.point),
            vector_to_cadwork(frame.xaxis),
            vector_to_cadwork(frame.zaxis),
        )
        notify_element_creation(element_id)
        return cls(element_id)
