from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Plane
from compas.geometry import is_point_infrontof_plane
from compas.geometry import Sphere
from compas.geometry import Line
from compas.scene import Scene

from compas_timber.elements import Beam


# create a parametric sphere that will be discretized into a mesh
SPHERE_RADIUS = 3000
SPHERE_CENTER = Point(0, 0, 0)
sphere = Sphere.from_point_and_radius(SPHERE_CENTER, SPHERE_RADIUS)

MESH_RESOLUTION = 16
mesh = Mesh.from_shape(sphere, u=MESH_RESOLUTION, v=MESH_RESOLUTION)

# create a plane that will be used to filter the top half of the sphere
plane = Plane.worldXY()
plane.point.z -= 1

# traverse the edges of the discretized sphere, store the lines and normals
lines_and_normals = []
for edge in mesh.edges():
    v1, v2 = edge
    start = Point(**mesh.vertex[v1])
    end = Point(**mesh.vertex[v2])
    line = Line(start, end)

    # we just want the top half of the sphere
    if not is_point_infrontof_plane(line.midpoint, plane):
        continue

    z_vector = mesh.vertex_normal(v1)
    lines_and_normals.append((line, z_vector))


BEAM_WIDTH = 80
BEAM_HEIGHT = 140

# create beams from the lines and normals and add them to the list
beam_list = []
for line, z_vector in lines_and_normals:
    beam = Beam.from_centerline(line, BEAM_WIDTH, BEAM_HEIGHT, z_vector)
    beam_list.append(beam)

# Added the beams to the cadwork 3d scene
scene = Scene(context="cadwork")
for beam in beam_list:
    scene.add(beam)
scene.draw()
