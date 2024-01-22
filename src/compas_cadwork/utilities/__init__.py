from typing import List
from typing import Literal
from typing import Dict
from typing import Union

from enum import auto

import cadwork
import utility_controller as uc
import element_controller as ec
import attribute_controller as ac
import bim_controller as bc
import visualization_controller as vc
import geometry_controller as gc

from compas_cadwork.datamodel import Element
from compas_cadwork.datamodel import ElementGroup
from compas_cadwork.datamodel.element import StrEnum

from .ifc_export import export_elements_to_ifc
from .ifc_export import IFCExportSettings


class ViewType(StrEnum):
    """CADWork Camera type"""

    NEGATIVE_X = auto()
    NEGATIVE_Y = auto()
    NEGATIVE_Z = auto()
    POSITIVE_X = auto()
    POSITIVE_Y = auto()
    POSITIVE_Z = auto()
    STANDARD_AXO = auto()


def show_view(view_spec: ViewType):
    """Sets a cadwork view.
    
    Parameters
    ----------
    view_spec : ViewType
        
    Examples
    --------
    show_view(ViewType.NEGATIVE_X)
    
    Returns:
        None
    """
    
    func_map = {
        ViewType.NEGATIVE_X: vc.show_view_negative_x,
        ViewType.NEGATIVE_Y: vc.show_view_negative_y,
        ViewType.NEGATIVE_Z: vc.show_view_negative_z,
        ViewType.POSITIVE_X: vc.show_view_positive_x,
        ViewType.POSITIVE_Y: vc.show_view_positive_y,
        ViewType.POSITIVE_Z: vc.show_view_positive_z,
        ViewType.STANDARD_AXO: vc.show_view_standard_axo,
    }
    
    func = func_map.get(view_spec)

    if callable(func):
        func()
    else:
        raise ValueError(f"Unknown camera view: {view_spec}")


def get_all_identifiable_element_ids():
    """get all identifiable element ids
    Args:

    Returns:
        List[int]
    """
    return ec.get_all_identifiable_element_ids()

def set_active(element_ids: list):
    """set active
    Args:
        element_id_list ( List[int]): element_id_list

    Returns:
        None
    """
    vc.set_active(element_ids)
 
def set_inactive(element_ids: list):
    """set inactive
    Args:
        element_id_list ( List[int]): element_id_list

    Returns:
        None
    """
    vc.set_inactive(element_ids)

def get_xl(elment_id: int):
    """get xl
    Args:
        element_id ( int): element_id

    Returns:
        point_3delement XL vector
    """
    return gc.get_xl(elment_id)

def get_yl(elment_id: int):
    """get yl
    Args:
        element_id ( int): element_id

    Returns:
        point_3delement YL vector
    """
    return gc.get_yl(elment_id)

def get_zl(elment_id: int):
    """get zl
    Args:
        element_id ( int): element_id

    Returns:
        point_3delement ZL vector
    """
    return gc.get_zl(elment_id)

def zoom_active_elements():
    """zoom active elements
    Args:

    Returns:
        None
    """
    vc.zoom_active_elements()

def get_camera_data():
    """get camera data
    Args:

    Returns:
        camera_datacamera data
    """
    return vc.get_camera_data()

def get_all_ifc_walls():
    """Returns a dictionary mapping names of the available building subgroups to their elements.

    Parameters
    ----------
    
    Returns
    -------
    dict(str, :class:`~compas_cadwork.datamodel.ElementGroup`)
        Dictionary of building group names mapped to an instance of ElementGroup.

    """
    get_grouping_name = _get_grouping_func()

    groups_elements = {}
    for element_id in ec.get_all_identifiable_element_ids():
        group_name = get_grouping_name(element_id)
        
        if not group_name:
            continue
        
        if is_framed_wall(element_id):
            if group_name not in groups_elements:
                groups_elements[group_name] = [element_id]
        else:
            continue
        
    return groups_elements
    
def _get_grouping_func() -> callable:
    if ac.get_element_grouping_type() == cadwork.element_grouping_type.subgroup:
        return ac.get_subgroup
    else:
        return ac.get_group

def is_framed_wall(element_id: int):
    """is framed wall
    Args:
        element_id ( int): element_id

    Returns:
        boolis element wall
    """
    return ac.is_framed_wall(element_id)
    
def get_element_vertices_centroid(element: int):
    """get centroid of BREP vertices of element

    Args:
        element (int): element ID

    Returns:
        List[point_3d]
    """
    vertices = gc.get_element_vertices(element)
    p = len(vertices)
    x, y, z = zip(*vertices)
    return [sum(x) / p, sum(y) / p, sum(z) / p]

def get_language() -> str:
    """Returns the current language of the cadwork application.

    Returns
    -------
    str
        Language code of the cadwork application (e.g. "de", "fr", "it", "en").

    """
    return uc.get_language()

def get_group(element: int) -> str:
    """
    [:information_source: Available for script filled attributes](#){.mark-text}

    Args:
        element (int): element ID

    Returns:
        str: group name
    """
    return ac.get_group(element)

def get_subgroup(element: int) -> str:
    """get subgroup

    [:information_source: Available for script filled attributes](#){.mark-text}

    Args:
        element (int): element ID

    Returns:
        str: subgroup name
    """
    return ac.get_subgroup(element)

def get_element_grouping_type() -> int:
    """Get element grouping type

    Returns:
        element_grouping_type: grouping type
    """
    return ac.get_element_grouping_type()

def get_active_element_ids() -> list:
    """Returns the elemend ids of the active selection"""
    return ec.get_active_identifiable_element_ids()

def get_plugin_home() -> str:
    """Returns the home root directory of the currently running plugin"""
    return uc.get_plugin_path()


def get_filename() -> str:
    """Returns the name of the currently open cadwork document."""
    return uc.get_3d_file_name()


def export_elements_to_ifc(element_ids: List[int], filepath: str):
    """Exports elements to ifc file.

    Parameters
    ----------
    element_ids : list(int)
        List of element ids to export.
    filepath : str
        Path to the resulting ifc file.

    """
    try:
        bc.export_ifc2x3_silently(element_ids, filepath)
    except AttributeError:
        bc.export_ifc(element_ids, filepath)


def get_element_groups(is_wall_frame=True) -> dict[str, ElementGroup]:
    """Returns a dictionary mapping names of the available building subgroups to their elements.

    Parameters
    ----------
    is_wall_frame : bool, optional
        If True, only wall groups which contain a wall frame elements are returned, otherwise all groups are returned.

    Returns
    -------
    dict(str, :class:`~compas_cadwork.datamodel.ElementGroup`)
        Dictionary of building group names mapped to an instance of ElementGroup.

    """
    get_grouping_name = _get_grouping_func()

    groups_elements = {}
    for element_id in ec.get_all_identifiable_element_ids():
        group_name = get_grouping_name(element_id)

        if not group_name:
            continue

        if group_name not in groups_elements:
            groups_elements[group_name] = ElementGroup(group_name)
        groups_elements[group_name].add_element(Element.from_id(element_id))

    if is_wall_frame:
        _remove_wallless_groups(groups_elements)

    return groups_elements

def _get_grouping_func() -> callable:
    if ac.get_element_grouping_type() == cadwork.element_grouping_type.subgroup:
        return ac.get_subgroup
    else:
        return ac.get_group

def _remove_wallless_groups(groups: Dict[str, ElementGroup]) -> None:
    to_remove = (group for group in groups.values() if group.wall_frame_element is None)
    for group in to_remove:
        del groups[group.name]

def activate_elements(elements: List[Union[Element, int]]) -> None:
    """Activates the given elements in the cadwork viewport.

    Parameters
    ----------
    elements : list(:class:`compas_cadwork.datamodel.Element` or int)
        List of elements or element ids to activate.

    """
    element_ids = [element.id if isinstance(element, Element) else element for element in elements]
    vc.set_active(element_ids)


def deactivate_elements(elements: List[Union[Element, int]]) -> None:
    """Deactivates the given elements in the cadwork viewport.

    Parameters
    ----------
    elements : list(:class:`compas_cadwork.datamodel.Element` or int)
        List of elements or element ids to deactivate.

    """
    element_ids = [element.id if isinstance(element, Element) else element for element in elements]
    vc.set_inactive(element_ids)


def hide_elements(elements: List[Union[Element, int]]) -> None:
    """Hides the given elements in the cadwork viewport.

    Parameters
    ----------
    elements : list(:class:`compas_cadwork.datamodel.Element` or int)
        List of elements or element ids to hide.

    """
    element_ids = [element.id if isinstance(element, Element) else element for element in elements]
    vc.set_invisible(element_ids)


def lock_elements(elements: List[Union[Element, int]]) -> None:
    """Locks the given elements in the cadwork viewport.

    Parameters
    ----------
    elements : list(:class:`compas_cadwork.datamodel.Element` or int)
        List of elements or element ids to lock.

    """
    element_ids = [element.id if isinstance(element, Element) else element for element in elements]
    vc.set_immutable(element_ids)


def unlock_elements(elements: List[Union[Element, int]]) -> None:
    """Unlocks the given elements in the cadwork viewport.

    Parameters
    ----------
    elements : list(:class:`compas_cadwork.datamodel.Element` or int)
        List of elements or element ids to unlock.

    """
    element_ids = [element.id if isinstance(element, Element) else element for element in elements]
    vc.set_mutable(element_ids)


def show_all_elements() -> None:
    """Shows all elements in the cadwork viewport."""
    vc.show_all_elements()


def set_visible(element_ids: list):
    vc.set_visible(element_ids)

def set_invisible(element_ids: list):
    vc.set_invisible(element_ids)
    
def show_elements(elements: List[Union[Element, int]]) -> None:
    """Shows the given elements in the cadwork viewport.

    Parameters
    ----------
    elements : list(:class:`compas_cadwork.datamodel.Element` or int)
        List of elements or element ids to show.

    """
    element_ids = [element.id if isinstance(element, Element) else element for element in elements]
    vc.set_visible(element_ids)


def hide_all_elements() -> None:
    """Hides all elements in the cadwork viewport."""
    vc.hide_all_elements()


def disable_autorefresh() -> None:
    """Disables the automatic refresh of the cadwork viewport."""
    uc.disable_auto_display_refresh()


def enable_autorefresh() -> None:
    """Enables the automatic refresh of the cadwork viewport."""
    uc.enable_auto_display_refresh()


def force_refresh() -> None:
    """Forces a refresh of the cadwork viewport."""
    vc.refresh()


def get_all_element_ids() -> None:
    """Returns all element ids of the currently open cadwork document."""
    return ec.get_all_identifiable_element_ids()


def get_all_elements() -> None:
    """Returns all element ids of the currently open cadwork document."""
    for element_id in ec.get_all_identifiable_element_ids():
        yield Element.from_id(element_id)


def get_all_elements_with_attrib(attrib_number, attrib_value=None):
    for element_id in ec.get_all_identifiable_element_ids():
        if ac.get_user_attribute(element_id, attrib_number) == attrib_value:
            yield Element.from_id(element_id)


def remove_elements(elements: List[Union[Element, int]]) -> None:
    element_ids = [element.id if isinstance(element, Element) else element for element in elements]
    ec.delete_elements(element_ids)


def save_project_file():
    uc.save_3d_file_silently()


__all__ = [
    "IFCExportSettings",
    "get_group",
    "get_subgroup",
    "get_active_element_ids",
    "get_plugin_home",
    "get_filename",
    "export_elements_to_ifc",
    "get_element_groups",
    "activate_elements",
    "hide_elements",
    "lock_elements",
    "unlock_elements",
    "show_all_elements",
    "hide_all_elements",
    "disable_autorefresh",
    "enable_autorefresh",
    "force_refresh",
    "get_all_element_ids",
    "get_all_elements",
    "get_all_elements_with_attrib",
    "remove_elements",
    "save_project_file",
]
