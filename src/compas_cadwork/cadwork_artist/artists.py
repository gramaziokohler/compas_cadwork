import os, sys

import cadwork
import element_controller as ec
import utility_controller as uc


PLUGIN_PATH = uc.get_plugin_path()
SITE_PACKAGES = os.path.join(PLUGIN_PATH, "Lib", "site-packages")
sys.path.append(SITE_PACKAGES)
sys.path.append(r"C:\Users\mhelmrei\Documents\projects\monosashi\src")

from compas.geometry import Box


class BeamArtist():
    """Base class for a Compas BeamArtist in Cadwork"""
    def __init__(self, name : str = "", length : float = None, width : float = None):
        self.name = name
        self.length = length
        self.width = width
    
        
    def draw(self):
        """Draws a beam to cadwork 3d through a button action and length width input data from the
        user inteface.
        
        Parameters
        ----------
        beam_name
            string, beam name  
        beam_length
            float, beam length  
        beam_width
            float, beam width
                
        Returns
        -------
        None
        
        """
        
        
        
        cbeam = Box.from_corner_corner_height([0, 0, 0],
                                              [0 + self.width, 0 + self.length, 0],
                                              self.width)
        
        element_id = self.convert_compas_box_to_cadwork_beam(cbeam)
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
        
        element_id = self.draw_cadwork_square_beam_vectors(point, vector_x, vector_z, width, length)
        return element_id
    
    def draw_cadwork_square_beam_vectors(self, point : list = [100., 200., 300.], vector_x : list = [1., 0., 0.], vector_z : list = [0., 0., 1.], width : float = 200., length : float = 2600.):
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

        element_id = ec.create_square_beam_vectors(width, length, point, vector_x,
                                             vector_z)
        return element_id

if __name__ == "__main__":
    pass