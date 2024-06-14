import cadwork
from compas_monosashi.sequencer import LinearDimension
from compas_monosashi.sequencer import Model3d
from compas_monosashi.sequencer import Text3d
from dimension_controller import create_dimension
from element_controller import apply_transformation_coordinate
from element_controller import create_text_object_with_options
from element_controller import get_bounding_box_vertices_local
from element_controller import move_element
from file_controller import import_element_light

from compas_cadwork.conversions import point_to_cadwork
from compas_cadwork.conversions import vector_to_cadwork
from compas_cadwork.scene import CadworkSceneObject


class Text3dSceneObject(CadworkSceneObject):
    """Draws a 3d text volume instruction onto the view.


    Parameters
    ----------
    text_instruction : :class:`~monosashi.sequencer.Text3d`
        The text instruction to draw.

    """

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
        element_ids : int
            Cadwork element id of the text object.

        Return
        -------
        tuple(cadwork.point_3d, cadwork.point_3d, cadwork.point_3d)
            Translation vectors in x, y and z direction.
        """
        bb = get_bounding_box_vertices_local(element_id, [element_id])

        # https://github.com/inconai/innosuisse_issue_collection/issues/137
        start_vec_x = bb[0]
        end_vec_x = bb[1]
        start_vec_z = bb[0]
        end_vec_z = bb[2]

        vx = start_vec_x - end_vec_x
        dx = start_vec_x.distance(end_vec_x) / 2.0

        vx = vx.normalized()
        vx = vx * dx

        vz = start_vec_z - end_vec_z
        dz = start_vec_z.distance(end_vec_z) / 2.0

        vz = vz.normalized()
        vz = vz * dz

        # shift text in vy so it doesnt intersect with geometry
        vy = vz.cross(vx)
        vy = vy.normalized()
        vy = vy * 5

        return vx, vy, vz

    def draw(self, *args, **kwargs):
        """Adds a text element with the text included in the provided text instruction.

        Returns
        -------
        int
            cadwork element ID of the added text.

        """

        color = 112  # TODO: find a way to map compas colors to cadwork materials

        text_options = cadwork.text_object_options()
        text_options.set_color(color)
        text_options.set_element_type(cadwork.raster)
        text_options.set_text(self.text_instruction.text)
        text_options.set_height(self.text_instruction.size)

        loc = self.text_instruction.location
        element_id = create_text_object_with_options(
            point_to_cadwork(loc.point), vector_to_cadwork(loc.xaxis), vector_to_cadwork(loc.yaxis), text_options
        )
        if self.text_instruction.centered:
            vx, vy, vz = self._generate_translation_vectors(element_id)
            move_element([element_id], vx + vy + vz)

        element = self.add_element(element_id)
        element.set_is_instruction(True, self.text_instruction.id)
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
        text_plane_normal = self.linear_dimension.location.normal * -1.0
        inst_frame = self.linear_dimension.location
        distance_vector = inst_frame.point + self.linear_dimension.line_offset
        element_id = create_dimension(
            vector_to_cadwork(inst_frame.xaxis),
            vector_to_cadwork(text_plane_normal),
            vector_to_cadwork(distance_vector),
            [point_to_cadwork(point) for point in self.linear_dimension.points],
        )
        element = self.add_element(element_id)
        element.set_is_instruction(True, self.linear_dimension.id)
        return [element_id]


class Model3dSceneObject(CadworkSceneObject):
    """TODO: This is incomplete, complete."""

    def __init__(self, model3d: Model3d, **kwargs) -> None:
        super().__init__(model3d)
        self.model3d = model3d

    def draw(self):
        element_id = import_element_light(self.model3d.obj_filepath, point_to_cadwork(self.model3d.location.point))
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
        element = self.add_element(element_id)
        element.set_is_instruction(True, self.model3d.id)
        return [element_id]
