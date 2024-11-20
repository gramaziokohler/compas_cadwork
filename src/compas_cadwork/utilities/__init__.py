from typing import List
from typing import Dict
from typing import Union
from typing import Generator

from enum import auto
from enum import Enum

import cadwork
import utility_controller as uc
import element_controller as ec
import attribute_controller as ac
import visualization_controller as vc

from compas.geometry import Point
from compas_cadwork.datamodel import Element
from compas_cadwork.datamodel import ElementGroup
from compas_cadwork.datamodel import Dimension
from compas_cadwork.conversions import point_to_compas

from .ifc_export import IFCExporter
from .ifc_export import IFCExportSettings
from .dimensions import get_dimension_data


# TODO: remove. replaced by compas_cadwork.scene.Camera
class CameraView(str, Enum):
    """The view direction to which cadwork camera should be set in viewport.

    These coinside with the standard axes.

    Attributes
    ----------
    NEGATIVE_X : literal(CameraView.NEGATIVE_X)
        Negative X.
    NEGATIVE_Y : literal(CameraView.NEGATIVE_Y)
        Negative Y.
    NEGATIVE_Z : literal(CameraView.NEGATIVE_Z)
        Negative Z.
    POSITIVE_X : literal(CameraView.POSITIVE_X)
        Positive X.
    POSITIVE_Y : literal(CameraView.POSITIVE_Y)
        Positive Y.
    POSITIVE_Z : literal(CameraView.POSITIVE_Z)
        Positive Z.
    STANDARD_AXO : literal(CameraView.STANDARD_AXO)
        Standard Axonometric view.

    """

    NEGATIVE_X = auto()
    NEGATIVE_Y = auto()
    NEGATIVE_Z = auto()
    POSITIVE_X = auto()
    POSITIVE_Y = auto()
    POSITIVE_Z = auto()
    STANDARD_AXO = auto()


def set_camera_view(view: CameraView):
    """Sets the cadwork viewport to the given view.

    Parameters
    ----------
    view : :class:`CameraView`
        The view to set.

    Examples
    --------
    set_camera_view(CameraView.NEGATIVE_X)

    Returns
    -------
    None

    """
    func_map = {
        CameraView.NEGATIVE_X: vc.show_view_negative_x,
        CameraView.NEGATIVE_Y: vc.show_view_negative_y,
        CameraView.NEGATIVE_Z: vc.show_view_negative_z,
        CameraView.POSITIVE_X: vc.show_view_positive_x,
        CameraView.POSITIVE_Y: vc.show_view_positive_y,
        CameraView.POSITIVE_Z: vc.show_view_positive_z,
        CameraView.STANDARD_AXO: vc.show_view_standard_axo,
    }

    func = func_map.get(view)

    if callable(func):
        func()
    else:
        raise ValueError(f"Unknown camera view: {view}")


def zoom_active_elements():
    """zoom active elements

    Parameters
    ----------

    Returns:
        None
    """
    vc.zoom_active_elements()


def get_active_elements() -> list[Element]:
    """Returns the currently selected elements in the cadwork viewport.

    Returns
    -------
    list(:class:`compas_cadwork.datamodel.Element`)
        List of currently selected elements.

    """
    return [Element(e_id) for e_id in ec.get_active_identifiable_element_ids()]


def get_language() -> str:
    """Returns the current language of the cadwork application.

    Returns
    -------
    str
        Language code of the cadwork application (e.g. "de", "fr", "it", "en").

    """
    return uc.get_language()


def get_element_grouping_type() -> int:
    """get element grouping type

    Parameters
    ----------

    Returns:
        element_grouping_type
    """
    return ac.get_element_grouping_type()


def get_bounding_box_from_cadwork_object(element: Union[int, Element]) -> List[Point]:
    """Returns the 8 vertices of an elements bounding box.

    Parameters
    ----------
    element : int or :class:`compas_cadwork.datamodel.Element`
        The element id or Element object.

    Returns
    -------
    list(:class:`compas.geometry.Point`)

    """
    element_id = element.id if isinstance(element, Element) else element
    bbox = ec.get_bounding_box_vertices_local(element_id, [element_id])
    return [point_to_compas(p) for p in bbox]


def is_cadwork_window_in_dark_mode() -> bool:
    """Returns true if cadwork is in dark_mode and false if not."""
    return vc.is_cadwork_window_in_dark_mode()


def get_plugin_home() -> str:
    """Returns the home root directory of the currently running plugin"""
    return uc.get_plugin_path()


def get_filename() -> str:
    """Returns the name of the currently open cadwork document."""
    return uc.get_3d_file_name()


def get_dimensions():
    result = []
    for dim in filter(lambda element: element.is_linear_dimension, get_all_elements(include_instructions=True)):
        result.append(Dimension(dim.id))
    return result


def get_element_groups(is_wall_frame: bool = True) -> Dict[str, ElementGroup]:
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
        groups_elements[group_name].add_element(Element(element_id))

    if is_wall_frame:
        _remove_wallless_groups(groups_elements)

    return groups_elements


def _get_grouping_func() -> callable:
    if ac.get_element_grouping_type() == cadwork.element_grouping_type.subgroup:
        return ac.get_subgroup
    else:
        return ac.get_group


def _remove_wallless_groups(groups: Dict[str, ElementGroup]) -> None:
    to_remove = [group for group in groups.values() if group.wall_frame_element is None]
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


def get_all_element_ids(include_instructions: bool = False) -> Generator[int, None, None]:
    """Returns all element ids of the currently open cadwork document.

    Parameters
    ----------
    include_instructions : bool, optional
        If True, also include instruction elements in the result.

    Returns
    -------
    generator(int)
        Generator of element ids.

    """
    for element in get_all_elements(include_instructions):
        yield element.id


def get_user_point():
    """Prompts the user to select a cadwork point in the viewport and returns the coordinates of the selected point.

    Returns
    -------
    :class:`~compas.geometry.Point`
    """
    return point_to_compas(uc.get_user_point())


def get_all_elements(include_instructions: bool = False) -> Generator[Element, None, None]:
    """Returns all element ids of the currently open cadwork document.

    Parameters
    ----------
    include_instructions : bool, optional
        If True, also include instruction elements in the result.

    Returns
    -------
    generator(:class:`compas_cadwork.datamodel.Element`)
        Generator of elements.

    """
    for element_id in ec.get_all_identifiable_element_ids():
        element = Element(element_id)
        if include_instructions or not element.is_instruction:
            yield element


def get_all_elements_with_attrib(attrib_number, attrib_value=None):
    """Returns a generator containing all elements with the given user attribute set to the given value.

    Parameters
    ----------
    attrib_number : int
        The user attribute number to filter by.
    attrib_value : str, optional
        The value the user attribute should have.

    Returns
    -------
    generator(:class:`compas_cadwork.datamodel.Element`)
        Generator of elements
    """
    for element_id in ec.get_all_identifiable_element_ids():
        if ac.get_user_attribute(element_id, attrib_number) == attrib_value:
            yield Element(element_id)


def remove_elements(elements: List[Union[Element, int]]) -> None:
    """Removes the given elements from the cadwork document.

    Parameters
    ----------
    elements : list(:class:`compas_cadwork.datamodel.Element` or int)
        List of elements or element ids to remove.
    """
    element_ids = [element.id if isinstance(element, Element) else element for element in elements]
    ec.delete_elements(element_ids)


def save_project_file():
    """Saves the current cadwork project file."""
    uc.save_3d_file_silently()


__all__ = [
    "IFCExporter",
    "IFCExportSettings",
    "set_camera_view",
    "get_plugin_home",
    "get_filename",
    "get_active_elements",
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
    "zoom_active_elements",
    "get_dimension_data",
    "get_bounding_box_from_cadwork_object",
    "get_dimensions",
    "get_user_point",
    "is_cadwork_window_in_dark_mode",
]
