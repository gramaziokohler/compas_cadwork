from compas.plugins import plugin
from compas.scene import register
from compas_timber.elements import Beam

from .beamobject import BeamSceneObject
from .camera import Camera
from .instructionobject import LinearDimensionSceneObject
from .instructionobject import Text3dSceneObject
from .scene import CadworkSceneObject


__all__ = [
    "BeamSceneObject",
    "CadworkSceneObject",
    "Camera",
    "LinearDimensionSceneObject",
    "Text3dSceneObject",
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
        from compas_monosashi.sequencer import LinearDimension
        from compas_monosashi.sequencer import Text3d

        # These should move to monosashi probably
        register(Text3d, Text3dSceneObject, context=CONTEXT)
        register(LinearDimension, LinearDimensionSceneObject, context=CONTEXT)
    except Exception:  # noqa: S110
        pass
