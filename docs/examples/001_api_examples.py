import os

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "data")


def find_top_corner_of_group_wall_with_name(target_group):
    # find the wall element
    import cadwork
    import element_controller as ec
    import attribute_controller as ac
    import geometry_controller as gc

    grouping_type = ac.get_element_grouping_type()
    if grouping_type == cadwork.element_grouping_type.subgroup:
        get_group_name = ac.get_subgroup
    else:
        get_group_name = ac.get_group

    wall_element = None
    element_ids = ec.get_all_identifiable_element_ids()
    for e_id in element_ids:
        group_name = get_group_name(e_id)
        if target_group == group_name and (ac.is_framed_wall(e_id) or ac.is_floor(e_id) or ac.is_roof(e_id)):
            wall_element = e_id
            break

    if wall_element is None:
        raise ValueError(f"Could not find wall element for group {target_group}")

    p1 = gc.get_p1(wall_element)
    y_axis = gc.get_yl(wall_element)
    width = gc.get_width(wall_element)

    shift_vector = y_axis * 0.5 * width
    top_corner = p1 + shift_vector
    return cadwork.point_3d(top_corner)


def find_top_corner_of_group_wall_with_name(target_group):
    from compas_cadwork.utilities import get_element_groups
    from compas_cadwork.conversions import point_to_cadwork

    groups = get_element_groups()
    group = groups.get(target_group)
    if group is None:
        raise ValueError(f"Could not find wall element for group {target_group}")

    wall_element = group.wall_frame_element

    shift_vector = wall_element.frame.yaxis.scaled(0.5 * wall_element.width)
    point = wall_element.frame.translated(shift_vector).point
    return point_to_cadwork(point)


def side_as_surface(beam, side_index):
    # type: (int) -> compas.geometry.PlanarSurface
    """Returns the requested side of the beam as a parametric planar surface.
    Parameters
    ----------
    side_index : int
        The index of the reference side to be returned. 0 to 5.
    """
    from compas.geometry import PlanarSurface

    # TODO: maybe this should be the default representation of the ref sides?
    ref_side = beam.ref_sides[side_index]
    if side_index in (0, 2):  # top + bottom
        xsize = beam.blank_length
        ysize = beam.width
    elif side_index in (1, 3):  # sides
        xsize = beam.blank_length
        ysize = beam.height
    elif side_index in (4, 5):  # ends
        xsize = beam.width
        ysize = beam.height
    return PlanarSurface(xsize, ysize, frame=ref_side, name=ref_side.name)


def beam_face_parametric_traverse():
    from compas.data import json_load

    # load model
    PATH = os.path.join(DATA, "stand_w_drills.json")
    model = json_load(PATH)

    # identify beam..
    import element_controller as ec
    from compas_cadwork.conversions import point_to_cadwork

    beam = model.beams[6]
    ec.create_node(point_to_cadwork(beam.frame.point))

    # create surface from face
    surface = side_as_surface(beam, 0)

    point = surface.point_at(surface.xsize * 0.5, surface.ysize * 0.5)

    ec.create_node(point_to_cadwork(point))
