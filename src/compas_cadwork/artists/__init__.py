from compas.plugins import plugin
from compas.plugins import PluginManager
from compas.artists import Artist

from monosashi.sequencer import Text3d
from monosashi.sequencer import LinearDimension

from .artist import CadworkArtist
from .instructionartist import Text3dInstrcutionArtist
from .instructionartist import LinearDimensionArtist

__all__ = [
    "CadworkArtist",
    "Text3dInstrcutionArtist",
]


CONTEXT = "cadwork"

# TODO: remove
PluginManager.DEBUG = True


@plugin(category="drawing-utils", pluggable_name="clear", requires=[CONTEXT])
def clear_cadwork():
    """TODO: clear all elements flagged as AR instruction attribute"""
    CadworkArtist.clear()


@plugin(category="drawing-utils", pluggable_name="redraw", requires=[CONTEXT])
def redraw_cadwork():
    """TODO: ?"""
    pass


@plugin(category="factories", requires=[CONTEXT])
def register_artists():
    Artist.register(Text3d, Text3dInstrcutionArtist, context=CONTEXT)
    Artist.register(LinearDimension, LinearDimensionArtist, context=CONTEXT)
