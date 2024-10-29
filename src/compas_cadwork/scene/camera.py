from __future__ import annotations

from enum import Enum
from typing import Any
from typing import Dict

import cadwork
import visualization_controller as vc
from compas.data import Data
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas.tolerance import TOL

from compas_cadwork.conversions import point_to_cadwork
from compas_cadwork.conversions import point_to_compas
from compas_cadwork.conversions import vector_to_cadwork
from compas_cadwork.conversions import vector_to_compas


class ProjectionType(Enum):
    """Projection type of the camera.

    Attributes
    ----------
    PERSPECTIVE = 0
        Perspective projection.
    ORTHOGRAPHIC = 1
        Orthographic projection.

    """

    PERSPECTIVE = 0
    ORTHOGRAPHIC = 1


class Camera(Data):
    """This class is a wrapper for cadwork's camera data which allows to get information and manipulate the camera settings in an object-oriented way.

    ..note::
        While the cadwork document might use millimeters as the unit of length, the camera data is expected in meters.
        The caller is responsible for converting the data to the correct unit before passing it to the camera.

    Parameters
    ----------
    frame : Frame
        Position and orientation of the camera.
    fov : float
        The field of view of the camera.
    fwidth : float
        The field width of the camera.
    fheight : float
        The field height of the camera.
    target : Point
        The point the camera is looking at.
    projection_type : ProjectionType
        The projection type of the camera.

    Attributes
    ----------
    frame : :class:`~compas.geometry.Frame`, read-only
        Position and orientation of the camera.
    fov : float, read-only
        The field of view of the camera.
    fov_width : float, read-only
        The field width of the camera.
    fov_height : float, read-only
        The field height of the camera.
    position : Point
        The position of the camera.
    target : Point
        The point the camera is looking at.
    up_vector : Vector
        The up vector of the camera.

    Examples
    --------
    >>> from compas_cadwork.scene import Camera
    >>> camera = Camera.from_activedoc()
    >>> camera.position
    Point(0.0, 0.0, 0.0)

    >>> # Set the camera position to the center of the active element and zoom to it:
    >>> length = element.length * 0.001
    >>> target = element.midpoint * 0.001
    >>> location = target + element.frame.zaxis * length
    >>> camera = Camera.from_activedoc()
    >>> camera.look_at(target, up_vector=element.frame.xaxis)

    """

    @property
    def __data__(self) -> Dict[str, Any]:
        return {
            "frame": self._frame,
            "fov": self._fov,
            "fwidth": self._fwidth,
            "fheight": self._fheight,
            "target": self._target,
            "projection_type": self._projection_type,
        }

    def __init__(self, frame: Frame, fov: float, fwidth: float, fheight: float, target: Point, projection_type: ProjectionType) -> None:
        super().__init__()
        self._frame = frame
        self._fov = fov
        self._fwidth = fwidth
        self._fheight = fheight
        self._target = target
        self._projection_type = projection_type

    def __repr__(self) -> str:
        return f"Camera({self._frame}, {self._fov}, {self._fwidth}, {self._fheight}, {self._target}, {self._projection_type})"

    @property
    def fov(self) -> float:
        return self._fov

    @property
    def fov_height(self) -> float:
        return self._fheight

    @property
    def fov_width(self) -> float:
        return self._fwidth

    @property
    def frame(self) -> Frame:
        return self._frame

    @property
    def position(self) -> Point:
        return self._frame.point

    @position.setter
    def position(self, position: Point) -> None:
        self._frame.point = position.copy()
        self.apply_camera()

    @property
    def target(self) -> Point:
        return self._target

    @target.setter
    def target(self, target: Point) -> None:
        self._target = target.copy()
        self.apply_camera()

    @property
    def up_vector(self) -> Vector:
        return self._frame.zaxis

    @classmethod
    def from_activedoc(cls) -> Camera:
        """Create a camera from the camera in the currently active cadwork document.

        Returns
        -------
        Camera
            The camera object created from the active cadwork document.

        """
        data: cadwork.camera_data = vc.get_camera_data()
        target = point_to_compas(data.get_target())
        position = point_to_compas(data.get_position())
        up_vector = vector_to_compas(data.get_up_vector())
        cam_frame = cls._frame_from_camera_data(position, target, up_vector)
        return cls(
            cam_frame,
            data.get_field_of_view(),
            data.get_field_width(),
            data.get_field_height(),
            target,
            ProjectionType(data.get_projection_type()),
        )

    def look_at(self, target: Point, up_vector: Vector) -> None:
        """Set the camera to look at a specific target point.

        Raises
        ------
        ValueError
            If the up vector and the camera-to-target vector are not orthogonal.

        Parameters
        ----------
        target : Point
            The point the camera should look at.
        up_vector : Vector
            The up vector of the camera.

        """
        camera_to_target = Vector.from_start_end(self.position, target)
        if not TOL.is_zero(camera_to_target.dot(up_vector)):
            raise ValueError(f"up vector and camera-to-target vector must be orthogonal. camera_to_target: {camera_to_target}, up_vector: {up_vector}")

        self._frame = self._frame_from_camera_data(self.position, target, up_vector)
        self._target = target
        self.apply_camera()

    @staticmethod
    def _frame_from_camera_data(position: Point, target: Point, up_vector: Vector):
        vector_to_target = Vector.from_start_end(position, target).unitized()
        yaxis = vector_to_target.cross(up_vector)
        return Frame(position, vector_to_target, yaxis)

    def reload_camera(self) -> None:
        """Load the camera settings from the currently active cadwork document."""
        cam_data: cadwork.camera_data = vc.get_camera_data()
        target = point_to_compas(cam_data.get_target())
        position = point_to_compas(cam_data.get_position())
        up_vector = vector_to_compas(cam_data.get_up_vector())
        self._frame = self._frame_from_camera_data(position, target, up_vector)
        self._target = target
        self._fov = cam_data.get_field_of_view()
        self._fwidth = cam_data.get_field_width()
        self._fheight = cam_data.get_field_height()
        self._projection_type = ProjectionType(cam_data.get_projection_type())

    def apply_camera(self) -> None:
        """Apply the camera settings to the currently active cadwork document."""
        cam_data: cadwork.camera_data = vc.get_camera_data()
        cam_data.set_position(point_to_cadwork(self.position))
        cam_data.set_target(point_to_cadwork(self._target))
        cam_data.set_up_vector(vector_to_cadwork(self.up_vector))
        cam_data.set_field_of_view(self._fov)
        cam_data.set_field_width(self._fwidth)
        cam_data.set_field_height(self._fheight)
        cam_data.set_projection_type(cadwork.projection_type(self._projection_type.value))
        vc.set_camera_data(cam_data)
        vc.refresh()

    def zoom_active_element(self) -> None:
        """Zoom the camera to the currently active element."""
        vc.zoom_active_elements()
        vc.refresh()
        self.reload_camera()

    def reset_view(self) -> None:
        """Reset the camera to the standard axonometric view."""
        vc.show_view_standard_axo()
        vc.refresh()
        self.reload_camera()
