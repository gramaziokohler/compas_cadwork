from compas.geometry import Vector
from compas_monosashi.sequencer import LinearDimension
from compas_monosashi.sequencer import Model3d
from compas_monosashi.sequencer import Text3d
from attribute_controller import set_user_attribute
from dimension_controller import create_dimension
from element_controller import apply_transformation_coordinate
from element_controller import create_text_object_with_options
from element_controller import move_element
from element_controller import get_bounding_box_vertices_local
from file_controller import import_element_light
import cadwork

from compas_cadwork.scene import CadworkSceneObject
from compas_cadwork.conversions import point_to_cadwork
from compas_cadwork.conversions import vector_to_cadwork


class Text3dSceneObject(CadworkSceneObject):
    """Draws a 3d text volume instruction onto the view.


    Parameters
    ----------
    text_instruction : :class:`~monosashi.sequencer.Text3d`
        The text instruction to draw.

    """

    TEXT_TYPE_MAP = {"line": cadwork.line, "surface": cadwork.surface, "volume": cadwork.volume}

    def __init__(self, text_instruction: Text3d, **kwargs) -> None:
        super().__init__(text_instruction)
        self.text_instruction = text_instruction

    @staticmethod
    def _generate_translation_vectors(element_id: int):
        """Generates translation vectors from a bounding box that shift a text
        or a box from the bottom left point of the object to the center point
        of the object.


        Parameters
        ----------
        element_ids : list
            The respective texts or boxes

        Return
        ----------
        Cadwork Vector X and Z
            vx, vz
        """
        bb = get_bounding_box_vertices_local(element_id, [element_id])

        # https://github.com/inconai/innosuisse_issue_collection/issues/137
        start_vec_x = bb[5]
        end_vec_x = bb[6]
        start_vec_z = bb[6]
        end_vec_z = bb[3]

        vx = start_vec_x - end_vec_x
        dx = start_vec_x.distance(end_vec_x) / 2.0

        vx = vx.normalized()
        vx = vx * dx * -1

        vz = end_vec_z - start_vec_z
        dz = start_vec_z.distance(end_vec_z) / 2.0

        vz = vz.normalized()
        vz = vz * dz * -1  # write here why it has to be flipped
        return vx, vz

    def draw(self, *args, **kwargs):
        """Adds a text element with the text included in the provided text instruction.

        Returns
        -------
        int
            cadwork element ID of the added text.

        """

        if self.text_instruction.geometry_type not in self.TEXT_TYPE_MAP:
            raise ValueError(f"Unsupported geometry type in Text3dArtist: {self.text_instruction.geometry_type}")

        color = 5  # TODO: find a way to map compas colors to cadwork materials

        text_options = cadwork.text_object_options()
        text_options.set_color(color)
        text_options.set_element_type(self.TEXT_TYPE_MAP[self.text_instruction.geometry_type])
        text_options.set_text(self.text_instruction.text)
        text_options.set_height(self.text_instruction.size)
        text_options.set_thickness(self.text_instruction.thickness)

        loc = self.text_instruction.location
        element_id = create_text_object_with_options(
            point_to_cadwork(loc.point), vector_to_cadwork(loc.xaxis), vector_to_cadwork(loc.yaxis), text_options
        )

        vx, vz = self._generate_translation_vectors(element_id)
        move_element([element_id], vx + vz)
        self.add_element(element_id)
        set_user_attribute([element_id], self.USER_ATTR_NUMBER, self.USER_ATTR_VALUE)
        return [element_id]


class LinearDimensionSceneObject(CadworkSceneObject):
    """Draw a linear dimension instruction.

    Parameters
    ----------
    linear_dimension : :class:`~monosashi.sequencer.LineraDimension`
        The linear dimension to draw.

    """

    def __init__(self, linear_dimension: LinearDimension, **kwargs) -> None:
        super().__init__(linear_dimension)
        self.linear_dimension = linear_dimension

    def draw(self, *args, **kwargs):
        """Adds a new dimension to the cadwork document.

        Returns
        -------
        int
            cadwork element ID of the added dimension.

        """
        direction = Vector.from_start_end(
            self.linear_dimension.start, self.linear_dimension.end
        ).unitized()  # why is this even needed?
        text_plane_normal = self.linear_dimension.location.normal * -1.0
        text_plane_origin = self.linear_dimension.location.point
        element_id = create_dimension(
            vector_to_cadwork(direction),
            vector_to_cadwork(text_plane_normal),
            point_to_cadwork(text_plane_origin),
            [point_to_cadwork(self.linear_dimension.start), point_to_cadwork(self.linear_dimension.end)],
        )
        self.add_element(element_id)
        set_user_attribute([element_id], self.USER_ATTR_NUMBER, self.USER_ATTR_VALUE)
        return [element_id]


class Model3dSceneObject(CadworkSceneObject):
    """TODO: This is incomplete, complete."""

    def __init__(self, model3d: Model3d, **kwargs) -> None:
        super().__init__(model3d)
        self.model3d = model3d

    def draw(self):
        element_id = import_element_light(self.model3d.obj_filepath, point_to_cadwork(self.model3d.location.point))
        set_user_attribute([element_id], self.USER_ATTR_NUMBER, self.USER_ATTR_VALUE)
        old_loc = self.model3d.location
        new_loc = self.model3d.t_location

        # TODO: missing scaling..
        apply_transformation_coordinate(
            [element_id],
            point_to_cadwork(old_loc.point),
            vector_to_cadwork(old_loc.xaxis),
            vector_to_cadwork(old_loc.yaxis),
            point_to_cadwork(new_loc.point),
            point_to_cadwork(new_loc.xaxis),
            point_to_cadwork(new_loc.yaxis),
        )
