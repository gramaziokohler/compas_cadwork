from compas.plugins import plugin
from compas.scene import register

from .camera import Camera
from .scene import CadworkSceneObject
from .instructionobject import Text3dSceneObject
from .instructionobject import LinearDimensionSceneObject
from .instructionobject import Model3dSceneObject

__all__ = [
    "Camera",
    "CadworkSceneObject",
    "Text3dSceneObject",
    "LinearDimensionSceneObject",
    "Model3dSceneObject",
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
    try:
        from compas_monosashi.sequencer import Text3d
        from compas_monosashi.sequencer import LinearDimension
        from compas_monosashi.sequencer import Model3d

        # These should move to monosashi probably
        register(Text3d, Text3dSceneObject, context=CONTEXT)
        register(LinearDimension, LinearDimensionSceneObject, context=CONTEXT)
        register(Model3d, Model3dSceneObject, context=CONTEXT)
    except Exception as e:
        pass
