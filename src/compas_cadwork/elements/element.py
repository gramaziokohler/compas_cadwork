from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Final
from typing import Self
from uuid import UUID

import attribute_controller as ac
import bim_controller as bc
import cadwork
import element_controller as ec
import geometry_controller as gc
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Vector

from compas_cadwork.conversions.primitives import point_to_compas
from compas_cadwork.conversions.primitives import vector_to_cadwork
from compas_cadwork.conversions.primitives import vector_to_compas
from compas_cadwork.utils.ifc_uuid import IfcUUID
from compas_cadwork.utils.storage import KeyValueStorage


if TYPE_CHECKING:
    from attribute_controller import UserAttributeId
    from cadwork import ElementId
else:
    UserAttributeId = int  # For pytest and Sphinx


class _ElementAttributes(KeyValueStorage[UserAttributeId, str]):
    """Dictionary-like accessor for element user attributes.

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

    def _delete(self, key: UserAttributeId) -> None:
        ac.set_user_attribute([self._id], key, "")  # There's no delete user attribute function
        ac.delete_user_attribute(key)


class _ElementAttributeNames(KeyValueStorage[UserAttributeId, str]):
    """Dictionary-like accessor for element user attribute names.

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

    def _delete(self, key: str) -> None:
        ac.delete_additional_data([self._id], key)


class Element:
    """Generic Cadwork element."""

    id: Final[ElementId]
    """Cadwork element ID.

    NOTE: This identifier may change when the program is restarted.
    Do NOT rely on it as a unique ID, use ``Element.guid`` instead.
    """

    attribute_names: ClassVar[_ElementAttributeNames] = _ElementAttributeNames()
    """User attribute names."""

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
    def attributes(self) -> _ElementAttributes:
        """User attributes."""
        return _ElementAttributes(self.id)

    @cached_property
    def data(self) -> _ElementData:
        """Additional data."""
        return _ElementData(self.id)

    @property
    def frame(self) -> Frame:
        """Reference frame."""
        p1 = point_to_compas(gc.get_p1(self.id))
        x_axis = vector_to_compas(gc.get_xl(self.id))
        y_axis = vector_to_compas(gc.get_yl(self.id))
        return Frame(p1, x_axis, y_axis)

    @property
    def width(self) -> float:
        """Width in millimeters."""
        return gc.get_width(self.id)

    @width.setter
    def width(self, value: float) -> None:
        gc.set_width_real([self.id], value)

    @property
    def height(self) -> float:
        """Height in millimeters."""
        return gc.get_height(self.id)

    @height.setter
    def height(self, value: float) -> None:
        gc.set_height_real([self.id], value)

    @property
    def length(self) -> float:
        """Length in millimeters."""
        return gc.get_length(self.id)

    @length.setter
    def length(self, value: float) -> None:
        gc.set_length_real([self.id], value)

    @property
    def centerline(self) -> Line:
        """Line connecting the two points that define the element."""
        p1 = point_to_compas(gc.get_p1(self.id))
        p2 = point_to_compas(gc.get_p2(self.id))
        return Line(p1, p2)

    def translate(self, vector: Vector) -> None:
        """Translate element by the given vector.

        Parameters
        ----------
        vector : Vector
            The vector by which to translate the element.
        """
        ec.move_element([self.id], vector_to_cadwork(vector))

    def duplicate(self, vector: Vector) -> Self:
        """Duplicate element by the given vector.

        Parameters
        ----------
        vector : Vector
            The vector by which to duplicate the element.

        Returns
        -------
        Self
            New element.
        """
        new_element_ids = ec.copy_elements([self.id], vector_to_cadwork(vector))
        if len(new_element_ids) != 1:
            raise RuntimeError(f"Failed to copy Cadwork element with ID {self.id}")
        return self.__class__(new_element_ids[0])

    def delete(self) -> None:
        """Delete element.

        NOTE: Once called, this element instance becomes unusable.
        """
        ec.delete_elements([self.id])

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(id={self.id!r}, name={self.name!r})"
