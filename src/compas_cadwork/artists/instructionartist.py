from compas.geometry import Vector
from compas_monosashi.sequencer import LinearDimension
from compas_monosashi.sequencer import Model3d
from compas_monosashi.sequencer import Text3d
from compas_monosashi.sequencer import Text3d_Volume
from attribute_controller import set_user_attribute
from dimension_controller import create_dimension
from element_controller import apply_transformation_coordinate
from element_controller import create_text_object
from element_controller import create_text_object_with_font
from element_controller import create_text_object_with_options
from file_controller import import_element_light
import cadwork

from compas_cadwork.artists import CadworkArtist
from compas_cadwork.conversions import point_to_cadwork
from compas_cadwork.conversions import vector_to_cadwork

import ctypes


class Text3dInstructionArtist(CadworkArtist):
    """Draws a 3d text instruction onto the view.


    Parameters
    ----------
    text_instruction : :class:`monosashi.sequencer`
        The text instruction to draw.

    """

    def __init__(self, text_instruction: Text3d, **kwargs) -> None:
        super().__init__(text_instruction)
        self.text_instruction = text_instruction
    
    def draw(self, *args, **kwargs):
        """Adds a text element with the text included in the provided text instruction.

        Returns
        -------
        int
            cadwork element ID of the added text.

        """
        font = "Times New Roman"
        loc = self.text_instruction.location
        element_id = create_text_object_with_font(
            self.text_instruction.text,
            point_to_cadwork(loc.point),
            vector_to_cadwork(loc.xaxis),
            vector_to_cadwork(loc.yaxis),
            self.text_instruction.size,
            font 
        )
        self.add_element(element_id)
        set_user_attribute([element_id], self.USER_ATTR_NUMBER, self.USER_ATTR_VALUE)
        return element_id


class Text3dVolumeInstructionArtist(CadworkArtist):
    """Draws a 3d text volume instruction onto the view.


    Parameters
    ----------
    text_volume_instruction : :class:`monosashi.sequencer`
        The text instruction to draw.

    """

    def __init__(self, text_volume_instruction: Text3d_Volume, **kwargs) -> None:
        super().__init__(text_volume_instruction)
        self.text_volume_instruction = text_volume_instruction
    
    def draw(self, *args, **kwargs):
        """Adds a text element with the text included in the provided text instruction.

        Returns
        -------
        int
            cadwork element ID of the added text.

        """
        text_options = cadwork.text_object_options()
        text_options.set_color(5)
        text_options.set_element_type(cadwork.volume)
        text_options.set_text(self.text_volume_instruction.text)
        text_options.set_height(100.0)
        text_options.set_thickness(5.0)
        
        # font = "Times New Roman"
        loc = self.text_volume_instruction.location
        element_id = create_text_object_with_options(
            self.text_volume_instruction.text,
            point_to_cadwork(loc.point),
            vector_to_cadwork(loc.xaxis),
            vector_to_cadwork(loc.yaxis),
            text_options
        )
        self.add_element(element_id)
        set_user_attribute([element_id], self.USER_ATTR_NUMBER, self.USER_ATTR_VALUE)
        return element_id
    
    
class LinearDimensionArtist(CadworkArtist):
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
        direction = Vector.from_start_end(self.linear_dimension.start, self.linear_dimension.end).unitized()  # why is this even needed?
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
        return element_id


class Model3dArtist(CadworkArtist):
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

