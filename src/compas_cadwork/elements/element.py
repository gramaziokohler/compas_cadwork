from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING
from typing import Final
from typing import final
from uuid import UUID

import attribute_controller as ac
import bim_controller as bc
import cadwork
import element_controller as ec

from compas_cadwork.utils.ifc_uuid import IfcUUID


if TYPE_CHECKING:
    from attribute_controller import UserAttributeId
    from cadwork import ElementId


class _ElementUserAttributes:
    """Dictionary-like accessor for element user attributes.

    NOTE: User attributes can be viewed by the user when double-clicking an element in the Cadwork 3D interface.
    """

    _id: Final[ElementId]

    def __init__(self, element_id: ElementId) -> None:
        self._id = element_id

    def __contains__(self, key: UserAttributeId) -> bool:
        raw_value = ac.get_user_attribute(self._id, key)
        return raw_value != ""

    def __getitem__(self, key: UserAttributeId) -> str:
        raw_value = ac.get_user_attribute(self._id, key)
        if raw_value == "":
            raise KeyError(key)
        return raw_value

    def __setitem__(self, key: UserAttributeId, value: str) -> None:
        ac.set_user_attribute([self._id], key, value)

    def __delitem__(self, key: UserAttributeId) -> None:
        if key not in self:
            raise KeyError(key)
        ac.set_user_attribute([self._id], key, "")

    def get(self, key: UserAttributeId, default: str | None = None) -> str | None:
        """Get user attribute value.

        Parameters
        ----------
        key : UserAttributeId
            User attribute ID.
        default : str | None, optional
            Value to return if the attribute is not set.

        Returns
        -------
        str | None
            Attribute value, or ``default`` if the attribute is not set.
        """
        return self[key] if key in self else default

    def setdefault(self, key: UserAttributeId, default: str) -> str:
        """Set user attribute to ``default`` if not set, then return its value.

        Parameters
        ----------
        key : UserAttributeId
            User attribute ID.
        default : str
            Value to set if the attribute is not set.

        Returns
        -------
        str
            Existing attribute value, or ``default`` if the attribute was not set.
        """
        if key not in self:
            self[key] = default
        return self[key]


class Element:
    """Generic Cadwork element."""

    id: Final[ElementId]
    """Cadwork element ID.

    NOTE: This identifier may change when the program is restarted.
    Do NOT rely on it as a unique ID, use ``Element.guid`` instead.
    """

    @final
    @classmethod
    def from_guid(cls, guid: UUID) -> Element:
        """Get element from Cadwork GUID.

        Parameters
        ----------
        guid : UUID
            Cadwork element GUID.

        Returns
        -------
        Element
            Cadwork element.

        Raises
        ------
        ValueError
            If the element does not exist.
        """
        raw_guid = "{" + str(guid).upper() + "}"
        cadwork_id = ec.get_element_from_cadwork_guid(raw_guid)
        if ec.get_element_cadwork_guid(cadwork_id) != raw_guid:
            raise ValueError(f"Could not find a Cadwork element with GUID {raw_guid}")
        return cls(cadwork_id)

    def __init__(self, cadwork_id: ElementId) -> None:
        """Create new instance wrapping an existing Cadwork element.

        Parameters
        ----------
        cadwork_id : ElementId
            Cadwork element ID.
        """
        self.id = cadwork_id

    @property
    def guid(self) -> UUID:
        """Cadwork element GUID."""
        raw_guid = ec.get_element_cadwork_guid(self.id)
        if raw_guid == "":
            raise RuntimeError(f"Cadwork element #{self.id} no longer exists")
        return UUID(raw_guid)

    @property
    def ifc_guid(self) -> IfcUUID:
        """IFC GUID."""
        ifc_guid = bc.get_ifc_guid(self.id)
        if ifc_guid == "":
            raise RuntimeError(f"Cadwork element #{self.id} no longer exists")
        return IfcUUID(ifc_guid)

    @property
    def name(self) -> str | None:
        """Element name."""
        raw_value = ac.get_name(self.id)
        return None if raw_value == "" else raw_value

    @name.setter
    def name(self, value: str | None) -> None:
        ac.set_name([self.id], value or "")

    @property
    def group(self) -> str | None:
        """Group (or subgroup) name.

        NOTE: Maps to the appropriate attribute depending on the element grouping type configuration for the project.
        """
        use_subgroup = ac.get_element_grouping_type() == cadwork.element_grouping_type.subgroup
        raw_value = ac.get_subgroup(self.id) if use_subgroup else ac.get_group(self.id)
        return None if raw_value == "" else raw_value

    @group.setter
    def group(self, value: str | None) -> None:
        if ac.get_element_grouping_type() == cadwork.element_grouping_type.subgroup:
            ac.set_subgroup([self.id], value or "")
        else:
            ac.set_group([self.id], value or "")

    @property
    def comment(self) -> str | None:
        """Element comment."""
        raw_value = ac.get_comment(self.id)
        return None if raw_value == "" else raw_value

    @comment.setter
    def comment(self, value: str | None) -> None:
        ac.set_comment([self.id], value or "")

    @cached_property
    def attributes(self) -> _ElementUserAttributes:
        """User attributes."""
        return _ElementUserAttributes(self.id)

    def delete(self) -> None:
        """Delete element.

        NOTE: Once called, this element instance becomes unusable.
        """
        ec.delete_elements([self.id])

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(id={self.id!r}, name={self.name!r})"
