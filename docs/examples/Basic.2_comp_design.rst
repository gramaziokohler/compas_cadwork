********************************************************************************
Basic.2 Computational Design
********************************************************************************

This is a simple example of how `compas_cadwork` can be used in a computational design workflow, utilizing COMPAS's pure Python geometry kernel.

.. image:: ../_images/half_dome_trimmed.gif
    :alt: Computational Design Example

.. NOTE::
    This example uses COMPAS's digital timber extension `COMPAS Timber <https://gramaziokohler.github.io/compas_timber/latest/>`_.


The followingn are the required imports

.. code-block:: python

    from compas.datastructures import Mesh
    from compas.geometry import Point, Line, Plane, Sphere, is_point_infrontof_plane
    from compas.scene import Scene

    from compas_timber.elements import Beam

First, we create a parametric sphere to use for our design, and then we create a mesh from the sphere.
The meshe's edges will become the beams.

.. code-block:: python

    SPHERE_RADIUS = 3000
    SPHERE_CENTER = Point(0, 0, 0)
    sphere = Sphere.from_point_and_radius(SPHERE_CENTER, SPHERE_RADIUS)

    MESH_RESOLUTION = 16
    mesh = Mesh.from_shape(sphere, u=MESH_RESOLUTION, v=MESH_RESOLUTION)

Next, we create a plane that will be used to filter out the beams that are not in front of the plane.
We then iterate over the mesh's edges, creating beams from the edges that are in front of the plane.

.. code-block:: python

    plane = Plane.worldXY()
    plane.point.z -= 1

    lines_and_normals = []
    for edge in mesh.edges():
        v1, v2 = edge
        start = Point(**mesh.vertex[v1])
        end = Point(**mesh.vertex[v2])
        line = Line(start, end)

        if not is_point_infrontof_plane(line.midpoint, plane):
            continue

        z_vector = mesh.vertex_normal(v1)
        lines_and_normals.append((line, z_vector))

Finally, we create the beams from the lines and normals, and add them to a scene to visualize the design.

.. code-block:: python

    BEAM_WIDTH = 80
    BEAM_HEIGHT = 140

    beam_list = []
    for line, z_vector in lines_and_normals:
        beam = Beam.from_centerline(line, BEAM_WIDTH, BEAM_HEIGHT, z_vector)
        beam_list.append(beam)

    scene = Scene(context="cadwork")
    for beam in beam_list:
        scene.add(beam)
    scene.draw()
