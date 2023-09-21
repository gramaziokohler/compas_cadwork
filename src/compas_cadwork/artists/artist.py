from compas.artists import Artist

from element_controller import delete_elements
from element_controller import recreate_elements
from visualization_controller import refresh


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
    def redraw(cls):
        if cls.DRAWN_ELEMENTS:
            recreate_elements(cls.DRAWN_ELEMENTS)
        refresh()

    @classmethod
    def clear(cls):
        """Removes all elements tracked by the :class:`~compas_cadwork.artists.CadworkArtist` from the cadwork model."""
        if cls.DRAWN_ELEMENTS:
            delete_elements(cls.DRAWN_ELEMENTS)
            refresh()
        cls.DRAWN_ELEMENTS = []
