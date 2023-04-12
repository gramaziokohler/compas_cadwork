import os, sys

import cadwork
import element_controller as ec
import utility_controller as uc



PLUGIN_PATH = uc.get_plugin_path()
SITE_PACKAGES = os.path.join(PLUGIN_PATH, "Lib", "site-packages")
sys.path.append(SITE_PACKAGES)
sys.path.append(r"C:\Users\mhelmrei\Documents\projects\monosashi\src")

from compas.geometry import Box
from monosashi_cadwork.controller.controller import set_ifc_type_beam, set_ifc_building_and_storey, set_sub_group, set_group



class BeamArtist():
    """Base class for a Compas BeamArtist in Cadwork"""
    def __init__(self, name : str = "", length : float = None, width : float = None):
        self.name = name
        self.scene_objects = {}
        self.length = length
        self.width = width
        
    def set_ifc_attributes(self, element_id : int = None):
        """Sets the ifc attributes ifc-type, ifc-building, ifc-storey, ifc-group, ifc-sub-group
        
        Parameters
        ----------
        element_id
            int, cadwork id of the elment
            
        Returns
        -------
        None
        
        """
        
        #set if type to beam
        set_ifc_type_beam(element_id)
        
        #set ifc building and storey to standard values
        set_ifc_building_and_storey(element_id)
        
        #set group to AW
        set_group(element_id)
        
        #set sub group to standard
        set_sub_group(element_id)
        
    def draw(self):
        """Creates a compas box and draws it as a beam in cadwork
        
        Parameters
        ----------
        None
            
        Returns
        -------
        None
        
        """
        
        cbeam = Box.from_corner_corner_height([100, 200, 300],
                                              [100 + self.width, 200 + self.length, 300],
                                              self.width)
        
        element_id = self.convert_compas_box_to_cadwork_beam(cbeam)
        self.set_ifc_attributes(element_id)
        
        self.scene_objects["beams"] = []
        self.scene_objects["beams"].append(element_id)
        return element_id

    def convert_compas_box_to_cadwork_beam(self, box : object = None):
        """Converts a compas box to a cadwork beam
        
        Parameters
        ----------
        box
            compas box 
            
        Returns
        -------
        draws a beam and returns element_id
        
        """
        point = box.vertices[0]
        vector_x = box._frame.xaxis
        vector_z = box._frame.zaxis
        width = box.xsize
        length = box.ysize
        return self.create_square_beam_vectors(point, vector_x, vector_z, width, length)

    def create_square_beam_vectors(self, point : list = [100., 200., 300.], vector_x : list = [1., 0., 0.], vector_z : list = [0., 0., 1.], width : float = 200., length : float = 2600.):
        """Creates a square beam in cadwork
        
        Parameters
        ----------
        point
            list of floats, start point of the beam in mm
        vector_x
            list of floats, x vector length direction
        vector_z
            list of floats, z vector height orientation
        width
            float, width/ height in mm
        length
            float, length in mm
            
        Returns
        -------
        draws a beam to cadwork and returns element_id
        
        """
        point = cadwork.point_3d(*point)
        vector_x = cadwork.point_3d(*vector_x)
        vector_z = cadwork.point_3d(*vector_z)

        return ec.create_square_beam_vectors(width, length, point, vector_x,
                                             vector_z)
        
if __name__ == "__main__":
    pass