from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Final
from typing import Generic
from typing import Protocol
from typing import TypeVar

import multi_layer_cover_controller as mlc

from compas_cadwork.materials.layer_stack import AnyLayerStack


if TYPE_CHECKING:
    from cadwork import ElementId


_T = TypeVar("_T", bound=AnyLayerStack)
_T_co = TypeVar("_T_co", bound=AnyLayerStack, covariant=True)


class _ElementLike(Protocol[_T_co]):
    id: Final[ElementId]  # type: ignore[misc]

    @property
    def _layer_stack_type(self) -> type[_T_co]: ...


class LayeredMixin(Generic[_T]):
    """Mixin for elements that support having layers of materials."""

    @property
    @abstractmethod
    def _layer_stack_type(self) -> type[_T]:
        """Layer stack type.

        NOTE: Will be used by the `LayeredMixin.layers` getter to instantiate the proper layer stack type.

        Returns
        -------
        type[T]
            Layer stack type.
        """

    @property
    def layers(self: _ElementLike[_T]) -> _T | None:
        """Element layers."""
        layer_set_id = mlc.get_element_multi_layer_set(self.id)
        if layer_set_id == 0:
            return None
        return self._layer_stack_type(layer_set_id)

    @layers.setter
    def layers(self: _ElementLike[_T], value: _T) -> None:
        mlc.set_element_multi_layer_set(self.id, value.id)
