from compas.geometry import Box
import utility_controller as uc
import os, sys

PLUGIN_PATH = uc.get_plugin_path()
SITE_PACKAGES = os.path.join(PLUGIN_PATH, "Lib", "site-packages")
sys.path.append(SITE_PACKAGES)
sys.path.append(r"C:\Users\mhelmrei\Documents\projects\monosashi\src")

from monosashi_cadwork.controller.controller import set_ifc_type_beam

try:
    import cadwork
    import element_controller as ec
except:
    print("Error: Artist only available inside cadwork")


class BeamArtist():
    def __init__(self, name, length, width):
        self.name = name
        self.scene_objects = {}
        self.length = length
        self.width = width
        
    def draw(self):
        print("draw")
        cbeam = Box.from_corner_corner_height([100, 200, 300],
                                              [100 + self.width, 200 + self.length, 300],
                                              self.width)
      
        
        element_id = self.convert_compas_box_to_cadwork_beam(cbeam)
        set_ifc_type_beam(element_id)
        
        self.scene_objects["beams"] = []
        self.scene_objects["beams"].append(element_id)
    
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
        """Draws a line to the web_viewer
        
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
        draws a beam and returns element_id
        
        """
        point = cadwork.point_3d(*point)
        vector_x = cadwork.point_3d(*vector_x)
        vector_z = cadwork.point_3d(*vector_z)

        return ec.create_square_beam_vectors(width, length, point, vector_x,
                                             vector_z)
if __name__ == "__main__":
    pass