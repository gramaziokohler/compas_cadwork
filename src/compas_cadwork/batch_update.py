from __future__ import annotations

from collections.abc import Iterator
from contextvars import ContextVar
from contextvars import Token
from types import TracebackType
from typing import TYPE_CHECKING
from typing import Final
from typing import Literal
from typing import Self

import element_controller as ec
import utility_controller as uc


if TYPE_CHECKING:
    from cadwork import ElementId

    from compas_cadwork.elements.factory import AnyElement


_CURRENT_INSTANCE: ContextVar[BatchUpdate | None] = ContextVar("_CURRENT_INSTANCE", default=None)


def is_inside_context() -> bool:
    """Is inside batch update context.

    Returns
    -------
    bool
        Whether calling scope is inside a batch update context.
    """
    instance = _CURRENT_INSTANCE.get()
    return True if instance else False


def notify_element_creation(cadwork_id: ElementId) -> None:
    """Notify element creation event.

    Parameters
    ----------
    cadwork_id : ElementId
        Cadwork element ID.
    """
    instance = _CURRENT_INSTANCE.get()
    if instance:
        instance._created_ids.add(cadwork_id)


def notify_element_modification(cadwork_id: ElementId) -> None:
    """Notify element modification event.

    Parameters
    ----------
    cadwork_id : ElementId
        Cadwork element ID.
    """
    instance = _CURRENT_INSTANCE.get()
    if instance:
        instance._modified_ids.add(cadwork_id)


class BatchUpdate:
    """Helper for grouping several Cadwork operations in the same batch.

    This context manager is intended to be used when working with hundreds or thousands of elements,
    improving performance by deferring rendering until the end of the batch.
    """

    _token: Token[BatchUpdate | None] | None
    _created_ids: Final[set[ElementId]]
    _modified_ids: Final[set[ElementId]]

    def __init__(self) -> None:
        self._token = None
        self._created_ids = set()
        self._modified_ids = set()

    @property
    def created_elements(self) -> Iterator[AnyElement]:
        """Elements that have been created inside this context."""
        from compas_cadwork.elements.factory import get_element_instance

        for cadwork_id in self._created_ids:
            yield get_element_instance(cadwork_id)

    @property
    def modified_elements(self) -> Iterator[AnyElement]:
        """Elements that have been modified inside this context (excluding newly created elements)."""
        from compas_cadwork.elements.factory import get_element_instance

        for cadwork_id in self._modified_ids:
            yield get_element_instance(cadwork_id)

    @property
    def elements(self) -> Iterator[AnyElement]:
        """Elements that have been created or modified inside this context."""
        yield from self.created_elements
        yield from self.modified_elements

    def __enter__(self) -> Self:
        # Keep a reference to the current instance
        if self._token is not None:
            raise RuntimeError("Instance is already in use")
        self._token = _CURRENT_INSTANCE.set(self)

        # Reset instance
        self._created_ids.clear()
        self._modified_ids.clear()

        # Disable display refresh
        uc.disable_auto_display_refresh()

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        # Handle undo
        if self._created_ids:
            ec.add_created_elements_to_undo(list(self._created_ids))
        if self._modified_ids:
            ec.add_modified_elements_to_undo(list(self._modified_ids))

        # Re-enable display refresh
        uc.enable_auto_display_refresh()
        all_elements = self._created_ids | self._modified_ids
        if all_elements:
            ec.recreate_elements(list(all_elements))

        # Restore current instance to its previous value
        if self._token is not None:
            _CURRENT_INSTANCE.reset(self._token)
            self._token = None

        return False
