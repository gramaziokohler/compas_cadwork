from compas.artists import Artist


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

    def clear(self):
        """Removes all elements tracked by the :class:`~compas_cadwork.artists.CadworkArtist` from the cadwork model."""
        # TODO: remove all elements from scene
        self.DRAWN_ELEMENTS = []
