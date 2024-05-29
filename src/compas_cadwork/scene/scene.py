from compas.scene import SceneObject
from element_controller import delete_elements
from element_controller import recreate_elements
from utility_controller import get_user_color
from visualization_controller import get_rgb_from_cadwork_color_id
from visualization_controller import refresh

from compas_cadwork.datamodel import Element


class CadworkSceneObject(SceneObject):
    """Base class for all of cadwork's SceneObject."""

    DRAWN_ELEMENTS = []

    def add_element(self, element_id) -> Element:
        """Records the given element_id to track elements added by the :class:`~compas_cadwork.artists.CadworkArtist`.

        Parameters
        ----------
        element_id : int
            The element ID to add to tracking.

        """
        self.DRAWN_ELEMENTS.append(element_id)
        return Element.from_id(element_id)

    @classmethod
    def get_color(cls, color_id: int) -> tuple[int, list[int]]:
        cadwork_color_id = get_user_color(color_id)
        rgb_color = get_rgb_from_cadwork_color_id(cadwork_color_id)
        return cadwork_color_id, [rgb_color.r, rgb_color.g, rgb_color.b]

    @classmethod
    def refresh(cls):
        if cls.DRAWN_ELEMENTS:
            recreate_elements(cls.DRAWN_ELEMENTS)
        refresh()

    @classmethod
    def clear(cls, *args, **kwargs):
        """Removes all elements tracked by the :class:`~compas_cadwork.artists.CadworkArtist` from the cadwork model."""
        if cls.DRAWN_ELEMENTS:
            delete_elements(cls.DRAWN_ELEMENTS)
            refresh()
        cls.DRAWN_ELEMENTS = []
