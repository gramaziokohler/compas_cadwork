from functools import lru_cache
from math import cos
from math import pi
from math import radians
from math import sin

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Rotation
from compas.geometry import Vector

from compas_cadwork.elements import Beam


def frame_with_point(frame: Frame, point: Point) -> Frame:
    new_frame: Frame = frame.copy()
    new_frame.point = point
    return new_frame


@lru_cache
def create_hexagon_section(radius: float) -> Polygon:
    points: list[Point] = []
    for i in range(6):
        angle = i * (2 * pi / 6)
        x = radius * cos(angle)
        y = radius * sin(angle)
        points.append(Point(x, y))
    return Polygon(points)


frame = Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1))

for i in range(4):
    # Circular beam
    circular = Beam.circular(
        frame=frame_with_point(frame, Point(0, 0, 1000)),
        length=4000,
        diameter=500,
    )
    circular.name = f"Circular #{i}"
    print(circular, circular.frame)

    # Rectangular beam
    rectangular = Beam.rectangular(
        frame=frame_with_point(frame, Point(0, 0, 3000)),
        length=4000,
        width=500,
        height=350,
    )
    rectangular.name = f"Rectangular #{i}"
    print(rectangular, rectangular.frame)

    # Triangular beam
    triangle_section = Polygon([(0, 0), (300, 0), (150, 259.8)])
    triangular = Beam.polygonal(
        frame=frame_with_point(frame, Point(0, 0, 5000)),
        length=4000,
        section=triangle_section,
    )
    triangular.name = f"Triangular #{i}"
    print(triangular, triangular.frame)

    # Hexagonal beam
    hexagon_section = create_hexagon_section(300)
    hexagonal = Beam.polygonal(
        frame=frame_with_point(frame, Point(0, 0, 8000)),
        length=4000,
        section=hexagon_section,
    )
    hexagonal.name = f"Hexagonal #{i}"
    print(hexagonal, hexagonal.frame)

    # Rotate frame along the Y-axis
    frame = frame.transformed(Rotation.from_axis_and_angle(frame.yaxis, radians(-90), frame.point))
