from datetime import date
from datetime import datetime
from uuid import UUID

import utility_controller as uc


_PROJECT_UNSET_VALUE = "???"


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
        return None if raw_value == _PROJECT_UNSET_VALUE else raw_value

    @name.setter
    def name(self, value: str | None) -> None:
        uc.set_project_name(_PROJECT_UNSET_VALUE if value is None else value)

    @property
    def number(self) -> str | None:
        """Project number."""
        raw_value = uc.get_project_number()
        return None if raw_value == _PROJECT_UNSET_VALUE else raw_value

    @number.setter
    def number(self, value: str | None) -> None:
        uc.set_project_number(_PROJECT_UNSET_VALUE if value is None else value)

    @property
    def part(self) -> str | None:
        """Project part."""
        raw_value = uc.get_project_part()
        return None if raw_value == _PROJECT_UNSET_VALUE else raw_value

    @part.setter
    def part(self, value: str | None) -> None:
        uc.set_project_part(_PROJECT_UNSET_VALUE if value is None else value)

    @property
    def deadline(self) -> date | None:
        """Project deadline."""
        raw_value = uc.get_project_deadline()
        return None if raw_value == _PROJECT_UNSET_VALUE else datetime.strptime(raw_value, "%d.%m.%Y").date()

    @deadline.setter
    def deadline(self, value: date | None) -> None:
        uc.set_project_deadline(_PROJECT_UNSET_VALUE if value is None else value.strftime("%d.%m.%Y"))

    @property
    def architect(self) -> str | None:
        """Architect name."""
        raw_value = uc.get_project_architect()
        return None if raw_value == _PROJECT_UNSET_VALUE else raw_value

    @architect.setter
    def architect(self, value: str | None) -> None:
        uc.set_project_architect(_PROJECT_UNSET_VALUE if value is None else value)

    @property
    def customer(self) -> str | None:
        """Customer name."""
        raw_value = uc.get_project_customer()
        return None if raw_value == _PROJECT_UNSET_VALUE else raw_value

    @customer.setter
    def customer(self, value: str | None) -> None:
        uc.set_project_customer(_PROJECT_UNSET_VALUE if value is None else value)

    @property
    def designer(self) -> str | None:
        """Designer name."""
        raw_value = uc.get_project_designer()
        return None if raw_value == _PROJECT_UNSET_VALUE else raw_value

    @designer.setter
    def designer(self, value: str | None) -> None:
        uc.set_project_designer(_PROJECT_UNSET_VALUE if value is None else value)

    def __repr__(self) -> str:
        return f"Project(guid={self.guid!r}, name={self.name!r})"
