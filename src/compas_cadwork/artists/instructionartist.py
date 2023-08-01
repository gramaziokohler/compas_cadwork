from compas_monosashi.sequencer import Text3d
from compas_monosashi.sequencer import LinearDimension
from compas_monosashi.sequencer import Model3d

from compas_cadwork.artists import CadworkArtist
from compas_cadwork.conversions import point_to_cadwork
from compas_cadwork.conversions import vector_to_cadwork

from compas.geometry import Vector
from compas.geometry import Plane

from dimension_controller import create_dimension
from dimension_controller import set_text_size
from dimension_controller import set_precision
from dimension_controller import add_segment
from dimension_controller import set_text_color
from dimension_controller import set_line_thickness
from dimension_controller import set_default_anchor_length
from element_controller import create_text_object
from element_controller import create_line_points
from element_controller import apply_transformation_coordinate
from file_controller import import_element_light


class Text3dInstrcutionArtist(CadworkArtist):
    """Draws a 3d text instruction onto the view.


    Parameters
    ----------
    text_instruction : :class:`monosashi.sequencer`
        The text instruction to draw.

    """

    def __init__(self, text_instruction: Text3d, **kwargs) -> None:
        super().__init__()
        self.text_instruction = text_instruction

    def draw(self, *args, **kwargs):
        """Adds a text element with the text included in the provided text instruction.

        Returns
        -------
        int
            cadwork element ID of the added text.

        """
        loc = self.text_instruction.location
        element_id = create_text_object(
            self.text_instruction.text,
            point_to_cadwork(loc.point),
            vector_to_cadwork(loc.xaxis),
            vector_to_cadwork(loc.normal),
            self.text_instruction.size,
        )
        self.add_element(element_id)
        return element_id


class LinearDimensionArtist(CadworkArtist):
    """Draw a linear dimension instruction.

    Parameters
    ----------
    linear_dimension : :class:`~monosashi.sequencer.LineraDimension`
        The linear dimension to draw.

    """
    def __init__(self, linear_dimension: LinearDimension, **kwargs) -> None:
        super().__init__()
        self.linear_dimension = linear_dimension

    def draw(self, *args, **kwargs):
        """Adds a new dimension to the cadwork document.

        Returns
        -------
        int
            cadwork element ID of the added dimension.

        """
        direction = Vector.from_start_end(self.linear_dimension.start, self.linear_dimension.end).unitized()  # why is this even needed?
        text_plane_normal = self.linear_dimension.location.yaxis
        text_plane_origin = self.linear_dimension.location.point
        element_id = create_dimension(
            vector_to_cadwork(direction),
            vector_to_cadwork(text_plane_normal),
            point_to_cadwork(text_plane_origin),
            [point_to_cadwork(self.linear_dimension.start), point_to_cadwork(self.linear_dimension.end)],
        )
        self.add_element(element_id)
        return element_id


class Model3dArtist(CadworkArtist):
    def __init__(self, model3d: Model3d, **kwargs) -> None:
        super().__init__()
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

