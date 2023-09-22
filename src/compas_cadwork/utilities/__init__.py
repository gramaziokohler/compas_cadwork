import sys
from collections import defaultdict
from typing import List
from typing import Dict
from typing import Union

import cadwork
import utility_controller as uc
import element_controller as ec
import attribute_controller as ac
import bim_controller as bc
import visualization_controller as vc

from compas_cadwork.datamodel import Element


def unload_module(module_name):
    """Unloads all loaded moduels which start with the given `module_name`"""
    modules = list(filter(lambda m: m.startswith(module_name), sys.modules))
    for module in modules:
        sys.modules.pop(module)


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


def get_element_groups() -> Dict[str, List]:
    """Returns a dictionary mapping names of the available building subgroups to their elements.

    Returns
    -------
    dict(str, list(int))
        Dictionary of building subgroups and their elements.

    """
    get_grouping_name = (
        ac.get_subgroup if ac.get_element_grouping_type() == cadwork.element_grouping_type.subgroup else ac.get_group
    )
    groups_elements = defaultdict(list)
    for element_id in ec.get_all_identifiable_element_ids():
        groups_elements[get_grouping_name(element_id)].append(Element.from_id(element_id))
    return groups_elements


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
    print(f"hide elements: {element_ids}")
    vc.set_invisible(element_ids)


def lock_elements(elements: List[Union[Element, int]]) -> None:
    """Locks the given elements in the cadwork viewport.

    Parameters
    ----------
    elements : list(:class:`compas_cadwork.datamodel.Element` or int)
        List of elements or element ids to lock.

    """
    element_ids = [element.id if isinstance(element, Element) else element for element in elements]
    print(f"set_immutable: {element_ids}")
    vc.set_immutable(element_ids)


def unlock_elements(elements: List[Union[Element, int]]) -> None:
    """Unlocks the given elements in the cadwork viewport.

    Parameters
    ----------
    elements : list(:class:`compas_cadwork.datamodel.Element` or int)
        List of elements or element ids to unlock.

    """
    element_ids = [element.id if isinstance(element, Element) else element for element in elements]
    print(f"set_mutable: {element_ids}")
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
    print(f"show elements: {element_ids}")
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


__all__ = [
    "unload_module",
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
]
