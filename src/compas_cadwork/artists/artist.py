from compas.artists import Artist


class CadworkArtist(Artist):

    DRAWN_ELEMENTS = []

    def add_element(self, element_id):
        self.DRAWN_ELEMENTS.append(element_id)

    def clear(self):
        # TODO: remove all elements from scene
        self.DRAWN_ELEMENTS = []
