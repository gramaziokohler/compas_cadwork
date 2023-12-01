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

from compas_cadwork.artists import CadworkArtist
from compas_cadwork.conversions import point_to_cadwork
from compas_cadwork.conversions import vector_to_cadwork

import ctypes


TEXT_TYPE_MAP = {
            "line": cadwork.line,
            "surface": cadwork.surface,
            "volume": cadwork.volume
            }


BOUNDING_BOX_VERTICE_ORDER_MAP = {
                "Bounding Box": {
                    "start_vec_x": 0,
                    "end_vec_x": 3,
                    "start_vec_z": 3,
                    "end_vec_z": 2
                    },
                "3d text": {
                    "start_vec_x": 5,
                    "end_vec_x": 6,
                    "start_vec_z": 6,
                    "end_vec_z": 3
                }
            }


class Text3dInstructionArtist(CadworkArtist):
    """Draws a 3d text volume instruction onto the view.


    Parameters
    ----------
    text_instruction : :class:`monosashi.sequencer`
        The text instruction to draw.

    """

    def __init__(self, text_instruction: Text3d, **kwargs) -> None:
        super().__init__(text_instruction)
        self.text_instruction = text_instruction
    
    def generate_translation_vectors_from_bounding_box_local(self, element_ids: list = [],
                                                             input_geometry: str = "3d text"):
        
        """Generates translation vectors from a bounding box that shift a text
        or a box from the bottom left point of the object to the center point
        of the object.


        Parameters
        ----------
        element_ids : list
            The respective texts or boxes
        input_geometry : string
            Type of object

        Return
        ----------
        Cadwork Vector X and Z
            vx, vz
        """
        
        bb_vl = get_bounding_box_vertices_local(element_ids[0], element_ids)

        # as explained and diagrammed for some reason the bounding box vertices
        # are sorted differently for a 3d text or a 3d box

        vx = cadwork.point_3d(*bb_vl[BOUNDING_BOX_VERTICE_ORDER_MAP[input_geometry]["start_vec_x"]]) - cadwork.point_3d(
            *bb_vl[BOUNDING_BOX_VERTICE_ORDER_MAP[input_geometry]["end_vec_x"]])
        dx = cadwork.point_3d(*bb_vl[BOUNDING_BOX_VERTICE_ORDER_MAP[input_geometry]["start_vec_x"]]).distance(
            cadwork.point_3d(*bb_vl[BOUNDING_BOX_VERTICE_ORDER_MAP[input_geometry]["end_vec_x"]]))/2
        
        vx = vx.normalized()
        vx = vx*dx*-1

        vz = cadwork.point_3d(*bb_vl[BOUNDING_BOX_VERTICE_ORDER_MAP[input_geometry]["end_vec_z"]]) - cadwork.point_3d(
            *bb_vl[BOUNDING_BOX_VERTICE_ORDER_MAP[input_geometry]["start_vec_z"]])
        dz = cadwork.point_3d(*bb_vl[BOUNDING_BOX_VERTICE_ORDER_MAP[input_geometry]["start_vec_z"]]).distance(
            cadwork.point_3d(*bb_vl[BOUNDING_BOX_VERTICE_ORDER_MAP[input_geometry]["end_vec_z"]]))/2

        vz = vz.normalized()
        vz = vz*dz*-1

        return vx, vz

    def shift_text_from_bottom_left_to_center(self, element_ids: list = [], geometry_type: str = None):
        if not geometry_type == "volume":
            return None
        vx, vz = self.generate_translation_vectors_from_bounding_box_local(element_ids)
        move_element(element_ids, vx + vz)
    
    def draw(self, color: int = 3, geometry_type: str = "volume", height: float = 100.,
             thickness: float = 5., *args, **kwargs):
        """Adds a text element with the text included in the provided text instruction.
        Parameters
        -------
        color : int
            Color of the text
        geometry_type : Cadwork Element Type
            Geometry Type of the text.
            Options:        
            1) "line"
            2) "surface"
            3) "volume"
        height : float
            Height of the text in mm
        thickness : float
            Thickness of the text in mm
        
        Returns
        -------
        int
            cadwork element ID of the added text.

        """

        if geometry_type not in list(TEXT_TYPE_MAP.keys()):
            print("ERROR: Geometry Type not defined.")
            return None
        
        text_options = cadwork.text_object_options()
        text_options.set_color(color)
        text_options.set_element_type(TEXT_TYPE_MAP[geometry_type])
        text_options.set_text(self.text_instruction.text)
        text_options.set_height(height)
        text_options.set_thickness(thickness)
        
        # font = "Times New Roman"
        loc = self.text_instruction.location
        element_id = create_text_object_with_options(
            point_to_cadwork(loc.point),
            vector_to_cadwork(loc.xaxis),
            vector_to_cadwork(loc.yaxis),
            text_options
        )
        
        self.shift_text_from_bottom_left_to_center([element_id], geometry_type)
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

