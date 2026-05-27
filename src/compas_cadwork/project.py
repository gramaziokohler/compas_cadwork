from __future__ import annotations

from datetime import date
from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING
from typing import Generator
from uuid import UUID

import attribute_controller as ac
import element_controller as ec
import utility_controller as uc

from compas_cadwork.elements.element import Element


if TYPE_CHECKING:
    from attribute_controller import UserAttributeId


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


def _is_empty_attribute_name(attribute_id: UserAttributeId, attribute_name: str) -> bool:
    """Is empty user attribute name.

    Parameters
    ----------
    attribute_id: UserAttributeId
        User attribute ID.
    attribute_name : str
        Raw user attribute name coming from Cadwork.

    Return
    ------
    bool
        Whether user attribute name is considered empty.
    """
    return attribute_name == "" or attribute_name == f"User{attribute_id}"


class _ProjectUserAttributeNames:
    """Dictionary-like accessor for getting the names of user attributes."""

    def __contains__(self, key: UserAttributeId) -> bool:
        raw_value = ac.get_user_attribute_name(key)
        return not _is_empty_attribute_name(key, raw_value)

    def __getitem__(self, key: UserAttributeId) -> str:
        raw_value = ac.get_user_attribute_name(key)
        if _is_empty_attribute_name(key, raw_value):
            raise KeyError(key)
        return raw_value

    def __setitem__(self, key: UserAttributeId, value: str) -> None:
        ac.set_user_attribute_name(key, value)

    def __delitem__(self, key: UserAttributeId) -> None:
        if key not in self:
            raise KeyError(key)
        ac.set_user_attribute_name(key, "")

    def get(self, key: UserAttributeId, default: str | None = None) -> str | None:
        """Get user attribute name.

        Parameters
        ----------
        key : UserAttributeId
            User attribute ID.
        default : str | None, optional
            Value to return if the attribute is not set.

        Returns
        -------
        str | None
            Attribute name, or ``default`` if the attribute is not set.
        """
        return self[key] if key in self else default

    def setdefault(self, key: UserAttributeId, default: str) -> str:
        """Set user attribute name to ``default`` if not set, then return its value.

        Parameters
        ----------
        key : UserAttributeId
            User attribute ID.
        default : str
            Value to set if the attribute name is not set.

        Returns
        -------
        str
            Existing attribute name, or ``default`` if the attribute name was not set.
        """
        if key not in self:
            self[key] = default
        return self[key]


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
    def attribute_names(self) -> _ProjectUserAttributeNames:
        """User attributes name."""
        return _ProjectUserAttributeNames()

    def elements(self) -> Generator[Element, None, None]:
        """Get all elements in the project.

        Returns
        -------
        Generator[Element, None, None]
            Generator of elements.
        """
        for cadwork_id in ec.get_all_identifiable_element_ids():
            yield Element(cadwork_id)

    def selected_elements(self) -> Generator[Element, None, None]:
        """Get currently selected (active) elements.

        Returns
        -------
        Generator[Element, None, None]
            Generator of elements.
        """
        for cadwork_id in ec.get_active_identifiable_element_ids():
            yield Element(cadwork_id)

    def __repr__(self) -> str:
        return f"Project(guid={self.guid!r}, name={self.name!r})"
