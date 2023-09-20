import sys
from collections import defaultdict
from typing import List
from typing import Dict

import cadwork
import utility_controller as uc
import element_controller as ec
import attribute_controller as ac
import bim_controller as bc

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


__all__ = [
    "unload_module",
    "get_plugin_home",
    "get_filename",
    "export_elements_to_ifc",
    "get_element_groups",
]
