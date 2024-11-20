import element_controller as ec
import visualization_controller as vc
from compas.scene import SceneObject

from compas_cadwork.datamodel import Element


class CadworkSceneObject(SceneObject):
    """Base class for all of cadwork's SceneObject."""

    DRAWN_ELEMENTS = []

    def add_element(self, element_id) -> Element:
        """Records the given element_id to track elements added by the :class:`~compas_cadwork.scene.CadworkSceneObject`.

        Parameters
        ----------
        element_id : int
            The element ID to add to tracking.

        """
        self.DRAWN_ELEMENTS.append(element_id)
        return Element(element_id)

    @classmethod
    def refresh(cls):
        if cls.DRAWN_ELEMENTS:
            ec.recreate_elements(cls.DRAWN_ELEMENTS)
        vc.refresh()

    @classmethod
    def clear(cls, *args, **kwargs):
        """Removes all elements tracked by the :class:`~compas_cadwork.scene.CadworkSceneObject` from the cadwork model."""
        if cls.DRAWN_ELEMENTS:
            ec.delete_elements(cls.DRAWN_ELEMENTS)
            vc.refresh()
        cls.DRAWN_ELEMENTS = []
