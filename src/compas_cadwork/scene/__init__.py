from compas.plugins import plugin
from compas.scene import register

from compas_timber.elements import Beam

from .camera import Camera
from .scene import CadworkSceneObject
from .instructionobject import Text3dSceneObject
from .instructionobject import LinearDimensionSceneObject
from .beamobject import BeamSceneObject

__all__ = [
    "Camera",
    "CadworkSceneObject",
    "Text3dSceneObject",
    "LinearDimensionSceneObject",
    "BeamSceneObject",
]


CONTEXT = "cadwork"


@plugin(category="drawing-utils", requires=[CONTEXT])
def clear(*args, **kwargs):
    CadworkSceneObject.clear()


@plugin(category="drawing-utils", requires=[CONTEXT])
def after_draw(*args, **kwargs):
    CadworkSceneObject.refresh()


@plugin(category="factories", requires=[CONTEXT])
def register_scene_objects():
    register(Beam, BeamSceneObject, context=CONTEXT)
    try:
        from compas_monosashi.sequencer import Text3d
        from compas_monosashi.sequencer import LinearDimension

        # These should move to monosashi probably
        register(Text3d, Text3dSceneObject, context=CONTEXT)
        register(LinearDimension, LinearDimensionSceneObject, context=CONTEXT)
    except Exception:
        pass
