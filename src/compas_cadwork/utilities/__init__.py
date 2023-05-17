import sys


def unload_module(module_name):
    """Unloads all loaded moduels which start with the given `module_name`"""
    modules = list(filter(lambda m: m.startswith(module_name), sys.modules))
    for module in modules:
        sys.modules.pop(module)


__all__ = [
    "unload_module",
]
