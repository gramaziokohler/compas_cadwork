import sys

import utility_controller as uc


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


__all__ = [
    "unload_module",
    "get_plugin_home",
    "get_filename",
]
