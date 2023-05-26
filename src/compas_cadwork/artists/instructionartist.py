from monosashi.sequencer import Text3d

from compas.artists import Artist


class Text3dInstrcutionArtist(Artist):
    def __init__(self, text_instruction: Text3d, **kwargs) -> None:
        super().__init__()
        self.text_instruction = text_instruction

    def draw(self):
        print(f"using cadwork API to draw Text3d instruction in viewport")
