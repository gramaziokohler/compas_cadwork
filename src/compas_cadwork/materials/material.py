from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Final

import material_controller as mc


if TYPE_CHECKING:
    from cadwork import MaterialId


class Material:
    """A material used in a Cadwork project."""

    id: Final[MaterialId]

    def __init__(self, cadwork_id: MaterialId) -> None:
        """Create new instance wrapping a Cadwork material.

        NOTE: Avoid calling directly, use ``Project.material()`` instead to get an error in case of invalid ID.

        Parameters
        ----------
        cadwork_id : MaterialId
            Cadwork material ID.
        """
        self.id = cadwork_id

    @property
    def name(self) -> str:
        """Material name.

        NOTE: This has to be unique, no other material in the project can have the same name.
        """
        raw_value = mc.get_name(self.id)
        if raw_value == "":
            raise RuntimeError(f"Cadwork material #{self.id} no longer exists")
        return raw_value

    @name.setter
    def name(self, value: str) -> None:
        if value == "":
            raise ValueError("Material name cannot be empty")
        for material_id in mc.get_all_materials():
            material_name = mc.get_name(material_id)
            if material_name == value:
                raise ValueError(f"New name is already in use in material #{material_id}")
        mc.set_name(self.id, value)

    @property
    def group(self) -> str | None:
        """Material group name."""
        raw_value = mc.get_group(self.id)
        return None if raw_value == "" else raw_value

    @group.setter
    def group(self, value: str | None) -> None:
        mc.set_group(self.id, value or "")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Material) and self.id == other.id

    def __repr__(self) -> str:
        return f"Material(id={self.id!r}, name={self.name!r})"
