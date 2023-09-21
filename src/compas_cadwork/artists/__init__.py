from compas.plugins import plugin
from compas.plugins import PluginManager
from compas.artists import Artist

from compas_monosashi.sequencer import Text3d
from compas_monosashi.sequencer import LinearDimension
from compas_monosashi.sequencer import Model3d

from .artist import CadworkArtist
from .instructionartist import Text3dInstrcutionArtist
from .instructionartist import LinearDimensionArtist
from .instructionartist import Model3dArtist

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
    """Recrates all elements added with auto-refresh disabled.

    This is necessary because elements that were added to cadwork document with auto-refresh disabled
    are not automatically visible even after auto-refresh is enabled again.

    """
    CadworkArtist.redraw()


@plugin(category="factories", requires=[CONTEXT])
def register_artists():
    Artist.register(Text3d, Text3dInstrcutionArtist, context=CONTEXT)
    Artist.register(LinearDimension, LinearDimensionArtist, context=CONTEXT)
    Artist.register(Model3d, Model3dArtist, context=CONTEXT)
