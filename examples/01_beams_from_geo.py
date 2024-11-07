from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Plane
from compas.geometry import is_point_infrontof_plane
from compas.geometry import Sphere
from compas.geometry import Line
from compas.scene import Scene

from compas_timber.elements import Beam
from compas_timber.model import TimberModel

from compas_viewer.viewer import Viewer

viewer = Viewer()
viewer.renderer.camera.far = 100000.0
viewer.renderer.camera.near = 0.1
viewer.renderer.camera.position = [889.1, -1509.0, 561.0]
viewer.renderer.camera.target = [5.662291496992111, -7.578788697719574, 117.4088716506958]

# make a sphere
sphere = Sphere.from_point_and_radius(Point(0, 0, 0), 3000)
mesh = Mesh.from_shape(sphere, u=16, v=16)

# vertices = sphere.vertices
plane = Plane.worldXY()
plane.point.z -= 1

width = 60
height = 120

model = TimberModel()

for edge in mesh.edges():
    v1, v2 = edge
    start = Point(**mesh.vertex[v1])
    end = Point(**mesh.vertex[v2])
    line = Line(start, end)
    if not is_point_infrontof_plane(line.midpoint, plane):
        continue
    z_vector = mesh.vertex_normal(v1)
    beam = Beam.from_centerline(line, width, height, z_vector)
    model.add_element(beam)


# scene = Scene(context="cadwork")

viewer = Viewer()
for beam in model.beams:
    viewer.scene.add(beam.geometry)
    # scene.add(beam)
# scene.draw()
viewer.show()
