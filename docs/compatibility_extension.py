import ast
import re
from typing import Any

from griffe import Attribute
from griffe import Class
from griffe import Docstring
from griffe import Extension
from griffe import Function
from griffe import Object
from griffe import ObjectNode


EXTENSION_NAMESPACE = "cadwork"
"""Namespace to use when tagging Griffe objects."""

CADWORK_VERSIONS = [2024, 2025, 2026]
"""Cadwork versions to show in compatibility table."""


class CompatibilityExtension(Extension):
    def on_instance(self, *, node: ast.AST | ObjectNode, obj: Object, **kwargs: Any) -> None:
        # Skip nodes that are neither functions/methods nor attributes
        if not obj.is_function and not obj.is_attribute:
            return
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return

        # Extract minimum version from decorators (of any)
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue
            if not isinstance(decorator.func, ast.Name):
                continue
            if decorator.func.id != "requires_cadwork":
                continue
            if not isinstance(decorator.args[0], ast.Constant):
                continue
            min_cadwork_version = int(str(decorator.args[0].value))
            obj.extra[EXTENSION_NAMESPACE] = {
                "min_cadwork_version": min_cadwork_version,
            }

    def on_attribute(self, *, attr: Attribute, **kwargs: Any) -> None:
        self._parse_decorators_from_docstring(attr)
        self._add_compatibility_table(attr)

    def on_class(self, *, cls: Class, **kwargs: Any) -> None:
        if "__init__" in cls.functions:
            self._add_compatibility_table(cls)

    def on_function(self, *, func: Function, **kwargs: Any) -> None:
        self._add_compatibility_table(func)

    def _parse_decorators_from_docstring(self, obj: Object) -> None:
        if not obj.docstring:
            return
        decorator_match = re.search(r"@requires_cadwork\((\d{4})\)", obj.docstring.value)
        if not decorator_match:
            return

        # Extract minimum Cadwork version
        min_cadwork_version = int(decorator_match[1])
        obj.extra[EXTENSION_NAMESPACE] = {
            "min_cadwork_version": min_cadwork_version,
        }

        # Remove decorator from docstring
        obj.docstring.value = obj.docstring.value.replace(decorator_match[0], "").strip()

    def _add_compatibility_table(self, obj: Object) -> None:
        min_cadwork_version = obj.extra.get(EXTENSION_NAMESPACE, {}).get("min_cadwork_version", CADWORK_VERSIONS[0])

        # Generate custom block
        statuses = "".join(
            f"<td>{'✅' if version >= min_cadwork_version else '❌'} Cadwork {version}</td>"
            for version in CADWORK_VERSIONS
        )
        custom_block = (
            '<table class="cadwork-compatibility">'
            "<thead>"
            "<tr>"
            f'<th colspan="{len(CADWORK_VERSIONS)}">Software compatibility:</th>'
            "</tr>"
            "</thead>"
            "<tbody>"
            "<tr>"
            f"{statuses}"
            "</tr>"
            "</tbody>"
            "</table>\n"
        )

        # Prepend custom block to docstring
        if not obj.docstring:
            obj.docstring = Docstring(custom_block, parent=obj)
        else:
            obj.docstring.value = f"{custom_block}\n{obj.docstring.value}"
