import attribute_controller as ac
import element_controller as ec
from compas_timber.elements import Beam

from compas_cadwork.conversions import point_to_cadwork
from compas_cadwork.conversions import vector_to_cadwork

from .scene import CadworkSceneObject


class BeamSceneObject(CadworkSceneObject):
    """Scene object for COMPAS Timber Beam objects.

    Parameters
    ----------
    item : :class:`compas_timber.elements.Beam`
        The beam object.
    """

    def __init__(self, item: Beam, **kwargs) -> None:
        super().__init__(item)

    def draw(self):
        """Draw the beam object in the scene.

        Returns
        -------
        list
            List of drawn element ids.
        """
        beam = self._item
        origin = point_to_cadwork(beam.frame.point)
        xaxis = vector_to_cadwork(beam.frame.xaxis)
        zaxis = vector_to_cadwork(beam.frame.normal)
        element_id = ec.create_rectangular_beam_vectors(beam.width, beam.height, beam.length, origin, xaxis, zaxis)
        beam.attributes["cadwork_id"] = element_id
        beam.attributes["name"] = f"beam_{beam.guid}"
        ac.set_name([element_id], beam.attributes["name"])
        return [element_id]
