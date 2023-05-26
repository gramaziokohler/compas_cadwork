from compas.plugins import plugin
from compas.plugins import PluginManager
from compas.artists import Artist

from monosashi.sequencer import Text3d

from .instructionartist import Text3dInstrcutionArtist

__all__ = [
    "Text3dInstrcutionArtist",
]


CONTEXT = "cadwork"

# TODO: remove
PluginManager.DEBUG = True
if CONTEXT not in Artist.AVAILABLE_CONTEXTS:
    Artist.AVAILABLE_CONTEXTS.append(CONTEXT)


@plugin(category="drawing-utils", pluggable_name="clear", requires=[CONTEXT])
def clear_cadwork():
    """TODO: clear all elements flagged as AR instruction attribute"""
    pass


@plugin(category="drawing-utils", pluggable_name="redraw", requires=[CONTEXT])
def redraw_cadwork():
    """TODO: ?"""
    pass


@plugin(category="factories", requires=[CONTEXT])
def register_artists():
    Artist.register(Text3d, Text3dInstrcutionArtist, context=CONTEXT)
    return CONTEXT
