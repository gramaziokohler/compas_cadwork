import cadwork

from compas.geometry import Frame
from compas_monosashi.sequencer import LinearDimension
from compas_monosashi.sequencer import Model3d
from compas_monosashi.sequencer import Text3d
from dimension_controller import create_dimension
from element_controller import apply_transformation_coordinate
from element_controller import create_text_object_with_options
from element_controller import get_bounding_box_vertices_local
from file_controller import import_element_light

from compas_cadwork.conversions import point_to_cadwork
from compas_cadwork.conversions import vector_to_cadwork
from compas_cadwork.conversions import point_to_compas
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
    def _generate_translation_vectors(element_id: int, inst_frame: Frame):
        """Generates translation vectors from a bounding box that shift a text
        or a box from the bottom left point of the object to the center point
        of the object.

        Parameters
        ----------
        element_ids : int
            Cadwork element id of the text object.
        inst_frame : compas.geometry.Frame
            Frame of the text instruction.

        Return
        -------
        compas.geometry.Vector
            The translation vector by which the instruction must be shifted.
        """
        width, height = Text3dSceneObject._calculate_text_size(element_id)
        vx = inst_frame.xaxis.scaled(-0.5 * width)
        vy = inst_frame.yaxis.scaled(-0.5 * height)

        # shift text in vy so it doesnt intersect with geometry
        vz = inst_frame.normal.scaled(5.0)
        return vx + vy + vz

    @staticmethod
    def _calculate_text_size(element_id: int):
        # https://github.com/inconai/innosuisse_issue_collection/issues/137
        #  0 -------- 2
        #  ^          |
        #  y          |
        #  |          |
        #  1 --------x> 3
        bb = get_bounding_box_vertices_local(element_id, [element_id])
        p0 = point_to_compas(bb[0])
        p1 = point_to_compas(bb[1])
        p3 = point_to_compas(bb[3])
        d1 = p1.distance_to_point(p3)
        d2 = p0.distance_to_point(p1)

        # https://github.com/inconai/innosuisse_issue_collection/issues/259
        # this is a hack designed to get over the inconsistency of the bounding box's orientation
        # the texts are longer then they are tall, so determine which is which depending on the ratio.
        if d1 > d2:
            width = d1
            height = d2
        else:
            width = d2
            height = d1
        return width, height

    def draw(self, *args, **kwargs):
        """Adds a text element with the text included in the provided text instruction.

        Returns
        -------
        int
            cadwork element ID of the added text.

        """

        color = 8  # TODO: find a way to map compas colors to cadwork materials

        text_options = cadwork.text_object_options()
        text_options.set_color(color)
        text_options.set_element_type(cadwork.raster)
        text_options.set_text(self.text_instruction.text)
        text_options.set_height(self.text_instruction.size)

        loc = self.text_instruction.location
        element_id = create_text_object_with_options(
            point_to_cadwork(loc.point), vector_to_cadwork(loc.xaxis), vector_to_cadwork(loc.yaxis), text_options
        )

        element = self.add_element(element_id)

        if self.text_instruction.centered:
            translation = self._generate_translation_vectors(element_id, self.text_instruction.location)
            element.translate(translation)

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
