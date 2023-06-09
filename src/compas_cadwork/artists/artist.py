from compas.artists import Artist
from compas.colors import Color

from element_controller import delete_elements


class CadworkArtist(Artist):
    """Base class for all of cadwork's Artists."""

    DRAWN_ELEMENTS = []

    def add_element(self, element_id):
        """Records the given element_id to track elements added by the :class:`~compas_cadwork.artists.CadworkArtist`.

        Parameters
        ----------
        element_id : int
            The element ID to add to tracking.

        """
        self.DRAWN_ELEMENTS.append(element_id)

    @classmethod
    def clear(cls):
        """Removes all elements tracked by the :class:`~compas_cadwork.artists.CadworkArtist` from the cadwork model."""
        if cls.DRAWN_ELEMENTS:
            delete_elements(cls.DRAWN_ELEMENTS)
        cls.DRAWN_ELEMENTS = []
