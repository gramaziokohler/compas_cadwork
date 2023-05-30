from monosashi.sequencer import Text3d

from compas_cadwork.artists import CadworkArtist
from compas_cadwork.conversions import point_to_cadwork
from compas_cadwork.conversions import vector_to_cadwork

from element_controller import create_text_object


class Text3dInstrcutionArtist(CadworkArtist):
    """Draws a 3d text instruction onto the view.


    Parameters
    ----------
    text_instruction : :class:`monosashi.sequencer`
        The text instruction to draw.

    """

    def __init__(self, text_instruction: Text3d, **kwargs) -> None:
        super().__init__()
        self.text_instruction = text_instruction

    def draw(self, *args, **kwargs):
        """Adds a text element with the text included in the provided text instruction.

        Returns
        -------
        int
            cadwork element ID of the added element.

        """
        loc = self.text_instruction.location
        element_id = create_text_object(
            self.text_instruction.text,
            point_to_cadwork(loc.point),
            vector_to_cadwork(loc.xaxis),
            vector_to_cadwork(loc.normal),
            self.text_instruction.size,
        )
        self.add_element(element_id)
        return element_id
