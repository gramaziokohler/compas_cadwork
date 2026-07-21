from __future__ import annotations

from collections.abc import Generator
from collections.abc import Iterable
from datetime import date
from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING
from typing import overload
from uuid import UUID

import bim_controller as bc
import element_controller as ec
import material_controller as mc
import utility_controller as uc

from compas_cadwork.elements.factory import AnyElement
from compas_cadwork.elements.factory import get_element_instance
from compas_cadwork.ifc_uuid import IfcUUID
from compas_cadwork.materials.material import Material
from compas_cadwork.utils.storage import IterableKeyValueStorage
from compas_cadwork.utils.storage import KeyValueStorage


if TYPE_CHECKING:
    from cadwork import ElementId
    from cadwork import MaterialId


def _is_empty_value(raw_value: str) -> bool:
    """Is empty value.

    Parameters
    ----------
    raw_value : str
        Raw value coming from Cadwork.

    Return
    ------
    bool
        Whether value is considered empty.
    """
    return raw_value == "" or raw_value == "???"


class _ProjectAttributeValues(KeyValueStorage[int, str]):
    """Dictionary-like accessor for project user attribute values.

    NOTE: The first 10 user attributes are accessible in the GUI under "Preferences" > "Project data".
    """

    _KEY_TYPE = int

    @staticmethod
    def _empty(key: int, value: str) -> bool:
        return _is_empty_value(value)

    def _get(self, key: int) -> str:
        return uc.get_project_user_attribute(key)

    def _set(self, key: int, value: str) -> None:
        uc.set_project_user_attribute(key, value)

    def _delete(self, key: int) -> None:
        uc.set_project_user_attribute(key, "")  # There's no delete project user attribute function


class _ProjectAttributeKeys(KeyValueStorage[int, str]):
    """Dictionary-like accessor for project user attribute keys (i.e., names).

    NOTE: The first 10 user attributes are accessible in the GUI under "Preferences" > "Project data".
    """

    _KEY_TYPE = int

    @staticmethod
    def _empty(key: int, value: str) -> bool:
        return value == ""

    def _get(self, key: int) -> str:
        return uc.get_project_user_attribute_name(key)

    def _set(self, key: int, value: str) -> None:
        uc.set_project_user_attribute_name(key, value)

    def _delete(self, key: int) -> None:
        uc.set_project_user_attribute_name(key, "")  # There's no delete project user attribute name function


class _ProjectData(IterableKeyValueStorage[str, str]):
    """Dictionary-like accessor for project data.

    NOTE: Project data is hidden from the user and only accessible via the Cadwork API.
    """

    _KEY_TYPE = str

    @staticmethod
    def _empty(key: str, value: str) -> bool:
        return value == ""

    def _keys(self) -> Iterable[str]:
        return uc.get_project_data_keys()

    def _get(self, key: str) -> str:
        return uc.get_project_data(key)

    def _set(self, key: str, value: str) -> None:
        uc.set_project_data(key, value)

    def _delete(self, key: str) -> None:
        uc.delete_project_data(key)


class Project:
    """Currently open Cadwork project."""

    @property
    def guid(self) -> UUID:
        """Project GUID."""
        return UUID(uc.get_project_guid())

    @property
    def name(self) -> str | None:
        """Project name."""
        raw_value = uc.get_project_name()
        return None if _is_empty_value(raw_value) else raw_value

    @name.setter
    def name(self, value: str | None) -> None:
        uc.set_project_name(value or "")

    @property
    def number(self) -> str | None:
        """Project number."""
        raw_value = uc.get_project_number()
        return None if _is_empty_value(raw_value) else raw_value

    @number.setter
    def number(self, value: str | None) -> None:
        uc.set_project_number(value or "")

    @property
    def part(self) -> str | None:
        """Project part."""
        raw_value = uc.get_project_part()
        return None if _is_empty_value(raw_value) else raw_value

    @part.setter
    def part(self, value: str | None) -> None:
        uc.set_project_part(value or "")

    @property
    def deadline(self) -> date | None:
        """Project deadline."""
        raw_value = uc.get_project_deadline()
        return None if _is_empty_value(raw_value) else datetime.strptime(raw_value, "%d.%m.%Y").date()

    @deadline.setter
    def deadline(self, value: date | None) -> None:
        uc.set_project_deadline("" if value is None else value.strftime("%d.%m.%Y"))

    @property
    def architect(self) -> str | None:
        """Architect name."""
        raw_value = uc.get_project_architect()
        return None if _is_empty_value(raw_value) else raw_value

    @architect.setter
    def architect(self, value: str | None) -> None:
        uc.set_project_architect(value or "")

    @property
    def customer(self) -> str | None:
        """Customer name."""
        raw_value = uc.get_project_customer()
        return None if _is_empty_value(raw_value) else raw_value

    @customer.setter
    def customer(self, value: str | None) -> None:
        uc.set_project_customer(value or "")

    @property
    def designer(self) -> str | None:
        """Designer name."""
        raw_value = uc.get_project_designer()
        return None if _is_empty_value(raw_value) else raw_value

    @designer.setter
    def designer(self, value: str | None) -> None:
        uc.set_project_designer(value or "")

    @cached_property
    def attributes(self) -> _ProjectAttributeValues:
        """Project user attributes values."""
        return _ProjectAttributeValues()

    @cached_property
    def attribute_keys(self) -> _ProjectAttributeKeys:
        """Project user attribute keys (i.e., names)."""
        return _ProjectAttributeKeys()

    @cached_property
    def data(self) -> _ProjectData:
        """Project data."""
        return _ProjectData()

    @overload
    def element(self, *, cadwork_id: ElementId) -> AnyElement:
        """Get element from Cadwork ID.

        Parameters
        ----------
        cadwork_id : ElementId
            Cadwork element ID.

        Returns
        -------
        AnyElement
            Cadwork element.

        Raises
        ------
        ValueError
            If the element does not exist.
        """

    @overload
    def element(self, *, guid: UUID) -> AnyElement:
        """Get element from Cadwork GUID.

        Parameters
        ----------
        guid : UUID
            Cadwork element GUID.

        Returns
        -------
        AnyElement
            Cadwork element.

        Raises
        ------
        ValueError
            If the element does not exist.
        """

    @overload
    def element(self, *, ifc_guid: IfcUUID) -> AnyElement:
        """Get element from IFC GUID.

        Parameters
        ----------
        ifc_guid : IfcUUID
            Element IFC GUID.

        Returns
        -------
        AnyElement
            Cadwork element.

        Raises
        ------
        ValueError
            If the element does not exist.
        """

    def element(
        self,
        *,
        cadwork_id: ElementId | None = None,
        guid: UUID | None = None,
        ifc_guid: IfcUUID | None = None,
    ) -> AnyElement:
        # GUID to Cadwork ID
        if guid is not None:
            raw_guid = "{" + str(guid).upper() + "}"
            cadwork_id = ec.get_element_from_cadwork_guid(raw_guid)
            if ec.get_element_cadwork_guid(cadwork_id) != raw_guid:
                raise ValueError(f"Could not find a Cadwork element with GUID {raw_guid!r}")

        # IFC GUID to Cadwork ID
        if ifc_guid is not None:
            raw_guid = ifc_guid.base64
            cadwork_id = bc.get_element_id_from_base64_ifc_guid(raw_guid)
            if cadwork_id == 0:
                raise ValueError(f"Could not find a Cadwork element with IFC GUID {raw_guid!r}")

        # Cadwork ID to element
        assert cadwork_id is not None
        return get_element_instance(cadwork_id)

    def elements(self) -> Generator[AnyElement, None, None]:
        """Get all elements in the project.

        Returns
        -------
        Generator[AnyElement, None, None]
            Generator of elements.
        """
        for cadwork_id in ec.get_all_identifiable_element_ids():
            yield get_element_instance(cadwork_id)

    def selected_elements(self) -> Generator[AnyElement, None, None]:
        """Get currently selected (active) elements.

        Returns
        -------
        Generator[AnyElement, None, None]
            Generator of elements.
        """
        for cadwork_id in ec.get_active_identifiable_element_ids():
            yield get_element_instance(cadwork_id)

    @overload
    def material(self, *, cadwork_id: MaterialId) -> Material:
        """Get material from Cadwork ID.

        Parameters
        ----------
        cadwork_id : MaterialId
            Cadwork material ID.

        Returns
        -------
        Material
            Cadwork material.

        Raises
        ------
        ValueError
            If the material does not exist.
        """

    @overload
    def material(self, *, name: str) -> Material:
        """Get material from name.

        Parameters
        ----------
        name: str
            Material name.

        Returns
        -------
        Material
            Cadwork material.

        Raises
        ------
        ValueError
            If the material does not exist.
        """

    def material(
        self,
        *,
        cadwork_id: MaterialId | None = None,
        name: str | None = None,
    ) -> Material:
        # Name to Cadwork ID
        if name is not None:
            cadwork_id = mc.get_material_id(name)
            if cadwork_id == 0:
                raise ValueError(f"Could not find a Cadwork material with name {name!r}")

        # Cadwork ID to material
        assert cadwork_id is not None
        if mc.get_name(cadwork_id) == "":
            raise ValueError(f"Could not find a Cadwork material with ID #{cadwork_id}")
        return Material(cadwork_id)

    def materials(self) -> Generator[Material, None, None]:
        """Get all materials in the project.

        Returns
        -------
        Generator[Material, None, None]
            Generator of materials.
        """
        for material_id in mc.get_all_materials():
            yield Material(material_id)

    def __repr__(self) -> str:
        return f"Project(guid={self.guid!r}, name={self.name!r})"
