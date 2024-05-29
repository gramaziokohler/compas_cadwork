import json

import cadwork
from compas.geometry import Vector
from compas_monosashi.sequencer import LinearDimension
from compas_monosashi.sequencer import Model3d
from compas_monosashi.sequencer import Text3d
from dimension_controller import create_dimension
from dimension_controller import set_line_color
from dimension_controller import set_text_color
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

    COLOR_PROFILES_FILE = (
        r"C:\Users\mhelmrei\Documents\projects\monosashi\src\monosashi_cadwork\view\data\project_profile_data_base.json"
    )

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

    def apply_color_profiles(self, data, instruction_type: str):
        """
        Apply color profiles to the UI based on the loaded data.

        Parameters
        ----------
        data : dict
            The loaded color profile data.
        """
        if (
            "PROJECT_NAME" in data
            and "COLOR_PROFILES" in data["PROJECT_NAME"]
            and "COLORS_INSTRUCTIONS" in data["PROJECT_NAME"]["COLOR_PROFILES"]
        ):
            return data["PROJECT_NAME"]["COLOR_PROFILES"]["COLORS_INSTRUCTIONS"][instruction_type]

    @classmethod
    def load_color_profiles(cls, instruction_type: str):
        """
        Load color profiles from the JSON file.
        """
        try:
            with open(Text3dSceneObject.COLOR_PROFILES_FILE, "r") as f:
                data = json.load(f)

                # Navigate through the dictionary structure to find the 'TEXT_INSTRUCTION'
                colors_instructions = data["PROJECT_NAME"]["COLOR_PROFILES"]["COLORS_INSTRUCTIONS"]

                for instruction in colors_instructions:
                    if instruction_type in instruction:
                        return instruction[instruction_type]
                return None
        except KeyError as e:
            print(f"KeyError: {e}")
            return None

    def draw(self, *args, **kwargs):
        """Adds a text element with the text included in the provided text instruction.

        Returns
        -------
        int
            cadwork element ID of the added text.

        """
        color = self.load_color_profiles("TEXT_INSTRUCTION")[1]

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

        direction = Vector.from_start_end(
            self.linear_dimension.start, self.linear_dimension.end
        ).unitized()  # why is this even needed?

        text_plane_normal = self.linear_dimension.location.normal * -1.0
        text_plane_origin = self.linear_dimension.location.point.copy()
        # text_plane_origin.z += self.linear_dimension.offset
        element_id = create_dimension(
            vector_to_cadwork(direction),
            vector_to_cadwork(text_plane_normal),
            point_to_cadwork(text_plane_origin),
            [point_to_cadwork(point) for point in self.linear_dimension.points],
        )
        color = Text3dSceneObject.load_color_profiles("LINEAR_DIM_INSTRUCTION")[1]
        set_text_color([element_id], color)
        set_line_color([element_id], color)

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
