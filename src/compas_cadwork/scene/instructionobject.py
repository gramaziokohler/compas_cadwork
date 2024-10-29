import cadwork
from compas.geometry import Frame

# TODO: this should NOT be here. either move these to compas_cadwork or add them here and wrap them in monosashi
try:
    from compas_monosashi.sequencer import LinearDimension
    from compas_monosashi.sequencer import Text3d
except ImportError:
    pass

import dimension_controller as dc
import element_controller as ec

from compas_cadwork.conversions import point_to_cadwork
from compas_cadwork.conversions import point_to_compas
from compas_cadwork.conversions import vector_to_cadwork
from compas_cadwork.scene import CadworkSceneObject


class Text3dSceneObject(CadworkSceneObject):
    """Draws a 3d text volume instruction onto the view.


    Parameters
    ----------
    text_instruction : :class:`~monosashi.sequencer.Text3d`
        The text instruction to draw.

    """

    def __init__(self, item: "Text3d", **kwargs) -> None:
        super().__init__(item)
        self._text_instruction = item

    @staticmethod
    def _generate_translation_vectors(element_id: int, inst_frame: Frame):
        # calculates the translation vectors needed properly center the text
        width, height = Text3dSceneObject._calculate_text_size(element_id)
        shift_x = inst_frame.xaxis.scaled(-0.5 * width)
        shift_y = inst_frame.yaxis.scaled(-0.5 * height)

        # shift text 5 mm in z direction to ensure it does not get hidden inside the element
        shift_z = inst_frame.normal.scaled(5.0)
        return shift_x + shift_y + shift_z

    @staticmethod
    def _calculate_text_size(element_id: int):
        # use the bounding box to determine the size of the text
        #  0 -------- 2
        #  ^          |
        #  h          |
        #  |          |
        #  1 --------w> 3
        bb = ec.get_bounding_box_vertices_local(element_id, [element_id])
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
        text_options.set_text(self._text_instruction.text)
        text_options.set_height(self._text_instruction.size)

        loc = self._text_instruction.location
        element_id = ec.create_text_object_with_options(point_to_cadwork(loc.point), vector_to_cadwork(loc.xaxis), vector_to_cadwork(loc.yaxis), text_options)

        element = self.add_element(element_id)

        if self._text_instruction.centered:
            translation = self._generate_translation_vectors(element_id, self._text_instruction.location)
            element.translate(translation)

        element.set_is_instruction(True, self._text_instruction.id)
        return [element_id]


class LinearDimensionSceneObject(CadworkSceneObject):
    """Draw a linear dimension instruction.

    Parameters
    ----------
    linear_dimension : :class:`~monosashi.sequencer.LineraDimension`
        The linear dimension to draw.

    """

    def __init__(self, item: "LinearDimension", **kwargs) -> None:
        super().__init__(item)
        self._linear_dimension = item

    def draw(self, *args, **kwargs):
        """Adds a new dimension to the cadwork document.

        Returns
        -------
        int
            cadwork element ID of the added dimension.

        """
        text_plane_normal = self._linear_dimension.location.normal * -1.0
        inst_frame = self._linear_dimension.location
        distance_vector = inst_frame.point + self._linear_dimension.line_offset
        element_id = dc.create_dimension(
            vector_to_cadwork(inst_frame.xaxis),
            vector_to_cadwork(text_plane_normal),
            vector_to_cadwork(distance_vector),
            [point_to_cadwork(point) for point in self._linear_dimension.points],
        )
        element = self.add_element(element_id)
        element.set_is_instruction(True, self._linear_dimension.id)
        return [element_id]
