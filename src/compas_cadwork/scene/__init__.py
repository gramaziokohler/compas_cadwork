from compas.plugins import plugin
from compas.plugins import PluginManager
from compas.scene import Scene

from compas_monosashi.sequencer import Text3d
from compas_monosashi.sequencer import LinearDimension
from compas_monosashi.sequencer import Model3d

from .scene import CadworkSceneObject
from .instructionobject import Text3dSceneObject
from .instructionobject import LinearDimensionSceneObject
from .instructionobject import Model3dSceneObject

__all__ = [
    "CadworkSceneObject",
    "Text3dSceneObject",
    "LinearDimensionSceneObject",
    "Model3dSceneObject",
]


CONTEXT = "cadwork"

# TODO: remove
PluginManager.DEBUG = True


@plugin(category="drawing-utils", requires=[CONTEXT])
def clear():
    CadworkSceneObject.clear()


@plugin(category="drawing-utils", requires=[CONTEXT])
def after_draw(drawn_element_ids):
    CadworkSceneObject.refresh()


@plugin(category="factories", requires=[CONTEXT])
def register_scene_objects():
    Scene.register(Text3d, Text3dSceneObject, context=CONTEXT)
    Scene.register(LinearDimension, LinearDimensionSceneObject, context=CONTEXT)
    Scene.register(Model3d, Model3dSceneObject, context=CONTEXT)
