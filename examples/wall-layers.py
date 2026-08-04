from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector

from compas_cadwork.elements import Wall
from compas_cadwork.materials import Layer
from compas_cadwork.materials import LayerType
from compas_cadwork.materials import WallLayerStack
from compas_cadwork.project import Project


# Get project instance
project = Project()

# Create a simple wall
wall = Wall.rectangular(
    frame=Frame(Point(0, -400, 1600), Vector(1, 0, 0), Vector(0, 0, 1)),
    length=4000,
    width=1000,
    thickness=360,
)

# Create some materials if they don't already exist in the project
mat_gipsfaser = project.material(name="Gipsfaser", create=True)
mat_osb = project.material(name="OSB", create=True)
mat_zellulose = project.material(name="Zellulose", create=True)
mat_weichfaser = project.material(name="Weichfaser", create=True)

# Create a layer stack for the wall
layer_stack = WallLayerStack.create("AW260")
layer_stack.append(Layer(name="Innenbeplankung", type=LayerType.PANEL, material=mat_gipsfaser, thickness=15.0))
layer_stack.append(Layer(name="Innenbeplankung", type=LayerType.PANEL, material=mat_osb, thickness=15.0))
layer_stack.append(Layer(name="Riegelwerk", type=LayerType.STRUCTURE, material=mat_zellulose, thickness=200.0))
layer_stack.append(Layer(name="Aussenbeplankung", type=LayerType.PANEL, material=mat_weichfaser, thickness=30.0))

# Assign layer stack to the wall
wall.layers = layer_stack

# Print a summary
print(f"Number of layers: {len(layer_stack)}")
print(f"Total thickness: {sum(layer.thickness for layer in layer_stack)}mm")
for layer in layer_stack:
    print(f"{layer.material.name} ({layer.type}): {layer.thickness}mm")
