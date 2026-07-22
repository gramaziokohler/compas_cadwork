from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Final

import material_controller as mc


if TYPE_CHECKING:
    from cadwork import MaterialId


def _ensure_name_is_valid(name: str) -> None:
    """Ensure material name is valid.

    Parameters
    ----------
    name : str
        Material name.

    Raises
    ------
    ValueError
        If material name is empty.
    """
    if name == "":
        raise ValueError("Material name cannot be empty")


def _ensure_name_is_unused(name: str) -> None:
    """Ensure material name is unused.

    Parameters
    ----------
    name : str
        Material name.

    Raises
    ------
    ValueError
        If material name is already in use.
    """
    material_id = mc.get_material_id(name)
    if material_id != 0:
        raise ValueError(f"Name is already in use in material #{material_id}")


class Material:
    """A material used in a Cadwork project."""

    id: Final[MaterialId]

    @classmethod
    def create(cls, name: str, raise_on_duplicate: bool = True) -> Material:
        """Create new material.

        Parameters
        ----------
        name : str
            New material name.
        raise_on_duplicate : bool
            Whether to raise an error if the material name is already in use. Otherwise, returns the existing material.

        Returns
        -------
        Material
            New material instance.

        Raises
        ------
        ValueError
            If material name is empty or already in use.
        """
        _ensure_name_is_valid(name)
        if raise_on_duplicate:
            _ensure_name_is_unused(name)
        cadwork_id = mc.create_material(name)  # Cadwork returns the existing ID for existing material names
        return cls(cadwork_id)

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
        _ensure_name_is_valid(value)
        if self.name == value:
            # Nothing to change
            return
        _ensure_name_is_unused(value)
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
