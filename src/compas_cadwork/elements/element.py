from __future__ import annotations

from collections.abc import Iterator
from collections.abc import MutableSet
from functools import cached_property
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Final
from typing import Generic
from typing import TypeVar
from typing import final
from uuid import UUID

import attribute_controller as ac
import bim_controller as bc
import cadwork
import element_controller as ec

from compas_cadwork.ifc_uuid import IfcUUID
from compas_cadwork.transaction import enqueue_element_deletion
from compas_cadwork.transaction import is_inside_transaction
from compas_cadwork.transaction import notify_element_modification
from compas_cadwork.utils.storage import KeyValueStorage

from .element_type import ElementType
from .ifc_element_type import IfcElementType
from .ifc_predefined_type import IfcPredefinedType


if TYPE_CHECKING:
    from attribute_controller import UserAttributeId
    from cadwork import ElementId

    from .factory import AnyElement
else:
    UserAttributeId = int
    AnyElement = object


class _ElementAttributeValues(KeyValueStorage[UserAttributeId, str]):
    """Dictionary-like accessor for element user attribute values.

    NOTE: User attributes are accessible in the GUI by double-clicking an element.
    """

    _KEY_TYPE = int
    _id: Final[ElementId]

    def __init__(self, element_id: ElementId) -> None:
        self._id = element_id

    @staticmethod
    def _empty(key: UserAttributeId, value: str) -> bool:
        return value == ""

    def _get(self, key: UserAttributeId) -> str:
        return ac.get_user_attribute(self._id, key)

    def _set(self, key: UserAttributeId, value: str) -> None:
        ac.set_user_attribute([self._id], key, value)
        notify_element_modification(self._id)

    def _delete(self, key: UserAttributeId) -> None:
        ac.set_user_attribute([self._id], key, "")  # There's no delete user attribute function
        ac.delete_user_attribute(key)
        notify_element_modification(self._id)


class _ElementAttributeKeys(KeyValueStorage[UserAttributeId, str]):
    """Dictionary-like accessor for element user attribute keys (i.e., names).

    NOTE: User attributes are accessible in the GUI by double-clicking an element.
    """

    _KEY_TYPE = int

    @staticmethod
    def _empty(key: UserAttributeId, value: str) -> bool:
        return value == "" or value == f"User{key}"

    def _get(self, key: UserAttributeId) -> str:
        return ac.get_user_attribute_name(key)

    def _set(self, key: UserAttributeId, value: str) -> None:
        ac.set_user_attribute_name(key, value)

    def _delete(self, key: UserAttributeId) -> None:
        ac.set_user_attribute_name(key, "")  # There's no delete user attribute name function


class _ElementData(KeyValueStorage[str, str]):
    """Dictionary-like accessor for element additional data.

    NOTE: Element additional data is hidden from the user and only accessible via the Cadwork API.
    """

    _KEY_TYPE = str
    _id: Final[ElementId]

    def __init__(self, element_id: ElementId) -> None:
        self._id = element_id

    @staticmethod
    def _empty(key: str, value: str) -> bool:
        return value == ""

    def _get(self, key: str) -> str:
        return ac.get_additional_data(self._id, key)

    def _set(self, key: str, value: str) -> None:
        ac.set_additional_data([self._id], key, value)
        notify_element_modification(self._id)

    def _delete(self, key: str) -> None:
        ac.delete_additional_data([self._id], key)
        notify_element_modification(self._id)


class _ElementChildren(MutableSet[AnyElement]):
    """Mutable set of the child elements contained in a host element."""

    _id: Final[ElementId]

    def __init__(self, element_id: ElementId) -> None:
        self._id = element_id

    def __contains__(self, value: object) -> bool:
        if isinstance(value, Element):
            return value.id in self._children_ids()
        return False

    def __iter__(self) -> Iterator[AnyElement]:
        from .factory import get_element_instance

        for element_id in self._children_ids():
            yield get_element_instance(element_id)

    def __len__(self) -> int:
        return len(self._children_ids())

    def add(self, value: AnyElement) -> None:
        if value.id == self._id:
            raise ValueError(f"Cannot add {value!r} as a child of Cadwork element #{self._id}")
        children_ids = self._children_ids()
        if value.id not in children_ids:
            children_ids.add(value.id)
            ec.set_container_contents(self._id, list(children_ids))

    def discard(self, value: AnyElement) -> None:
        children_ids = self._children_ids()
        if value.id in children_ids:
            children_ids.remove(value.id)
            ec.set_container_contents(self._id, list(children_ids))

    def _children_ids(self) -> set[ElementId]:
        """Get element IDs of children.

        Returns
        -------
        set[ElementId]
            Cadwork element IDs.
        """
        return set(ec.get_container_content_elements(self._id))


T = TypeVar("T", bound=ElementType)


class Element(Generic[T]):
    """Generic Cadwork element."""

    id: Final[ElementId]
    """Cadwork element ID.

    NOTE: This identifier may change when the program is restarted.
    Do NOT rely on it as a unique ID, use ``Element.guid`` instead.
    """

    attribute_keys: ClassVar[_ElementAttributeKeys] = _ElementAttributeKeys()
    """User attribute keys (i.e., names)."""

    @final
    def __init__(self, cadwork_id: ElementId) -> None:
        """Create new instance wrapping an existing Cadwork element.

        NOTE: Avoid calling directly, use ``Project.element()`` instead to get the proper element class instance.

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
    def type(self) -> T:
        """Element type."""
        raw_type = ac.get_element_type(self.id)
        return ElementType.from_cadwork(raw_type)  # type: ignore[return-value]

    @property
    def ifc_element_type(self) -> IfcElementType:
        """IFC element type."""
        raw_type = bc.get_ifc2x3_element_type(self.id)
        return IfcElementType.from_cadwork(raw_type)

    @ifc_element_type.setter
    def ifc_element_type(self, value: IfcElementType) -> None:
        bc.set_ifc2x3_element_type([self.id], value.to_cadwork())
        notify_element_modification(self.id)

    @property
    def ifc_predefined_type(self) -> IfcPredefinedType:
        """IFC predefined type."""
        raw_type = bc.get_ifc_predefined_type(self.id)
        return IfcPredefinedType.from_cadwork(raw_type)

    @ifc_predefined_type.setter
    def ifc_predefined_type(self, value: IfcPredefinedType) -> None:
        bc.set_ifc_predefined_type([self.id], value.to_cadwork())
        notify_element_modification(self.id)

    @property
    def name(self) -> str | None:
        """Element name."""
        raw_value = ac.get_name(self.id)
        return None if raw_value == "" else raw_value

    @name.setter
    def name(self, value: str | None) -> None:
        ac.set_name([self.id], value or "")
        notify_element_modification(self.id)

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
        notify_element_modification(self.id)

    @property
    def comment(self) -> str | None:
        """Element comment."""
        raw_value = ac.get_comment(self.id)
        return None if raw_value == "" else raw_value

    @comment.setter
    def comment(self, value: str | None) -> None:
        ac.set_comment([self.id], value or "")
        notify_element_modification(self.id)

    @cached_property
    def attributes(self) -> _ElementAttributeValues:
        """User attribute values."""
        return _ElementAttributeValues(self.id)

    @cached_property
    def data(self) -> _ElementData:
        """Additional data."""
        return _ElementData(self.id)

    @cached_property
    def children(self) -> _ElementChildren:
        """Element children."""
        return _ElementChildren(self.id)

    def delete(self) -> None:
        """Delete element.

        NOTE: Once called, this element instance becomes unusable.
        """
        if is_inside_transaction():
            enqueue_element_deletion(self.id)
        else:
            ec.delete_elements([self.id])

    @final
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Element) and self.id == other.id

    @final
    def __hash__(self) -> int:
        return hash(self.id)

    @final
    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(id={self.id!r}, name={self.name!r})"
