from __future__ import annotations

from abc import abstractmethod
from collections.abc import MutableSequence
from typing import TYPE_CHECKING
from typing import Final
from typing import Generator
from typing import Iterable
from typing import Self
from typing import TypeAlias
from typing import final
from typing import overload

import multi_layer_cover_controller as mlc

from compas_cadwork.materials.layer_type import LayerType
from compas_cadwork.materials.material import Material

from .layer import Layer


if TYPE_CHECKING:
    from cadwork import MultiLayerSetId


class LayerStack(MutableSequence[Layer]):
    """A collection of material layers to be used in elements with multi-layer support.

    In Cadwork, these are called multi-layer covers or sets.
    """

    id: Final[MultiLayerSetId]

    @classmethod
    @abstractmethod
    def create(cls, name: str) -> Self:
        """Create new layer stack.

        Parameters
        ----------
        name : str
            New layer stack name.

        Returns
        -------
        Self
            New layer stack instance.
        """

    @classmethod
    def _get_all(cls) -> Generator[AnyLayerStack, None, None]:
        """Get all layer stacks of this type in the project.

        Returns
        -------
        Generator[AnyLayerStack, None, None]
            Generator of layer stacks.
        """
        yield from FloorLayerStack._get_all()
        yield from RoofLayerStack._get_all()
        yield from WallLayerStack._get_all()

    def __init__(self, cadwork_id: MultiLayerSetId) -> None:
        """Create new instance wrapping a Cadwork multi-layer set.

        NOTE: Avoid calling directly, use ``Project.layer_stacks()`` instead to get an error in case of invalid ID.

        Parameters
        ----------
        cadwork_id : MultiLayerSetId
            Cadwork multi-layer set ID.
        """
        self.id = cadwork_id

    @property
    def name(self) -> str:
        """Layer stack name."""
        return mlc.get_multi_layer_set_name(self.id)

    @name.setter
    def name(self, value: str) -> None:
        mlc.set_multi_layer_set_name(self.id, value)

    def insert(self, index: int, value: Layer) -> None:
        # Normalize index
        # NOTE: `MutableSequence.insert()` must not raise `IndexError`s, it auto-corrects the index
        length = len(self)
        if index < 0:
            index += length
        index = max(0, min(index, length))

        # Shift layers to the right
        for i in range(length, index, -1):
            current_layer = self._get_layer(i - 1)
            if i == length:
                self._add_layer(current_layer)
            else:
                self._set_layer(i, current_layer)

        # Insert the new layer
        if index == length:
            self._add_layer(value)
        else:
            self._set_layer(index, value)

    def __len__(self) -> int:
        return mlc.get_layer_count(self.id)

    def __iter__(self) -> Generator[Layer, None, None]:
        for index in range(len(self)):
            yield self._get_layer(index)

    @overload
    def __getitem__(self, index: int) -> Layer: ...

    @overload
    def __getitem__(self, index: slice) -> list[Layer]: ...

    def __getitem__(self, index: int | slice) -> Layer | list[Layer]:
        if isinstance(index, slice):
            return [self._get_layer(i) for i in self._normalize_slice(index)]
        return self._get_layer(self._normalize_index(index))

    @overload
    def __setitem__(self, index: int, value: Layer) -> None: ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[Layer]) -> None: ...

    def __setitem__(self, index: int | slice, value: Layer | Iterable[Layer]) -> None:
        if isinstance(index, slice):
            assert isinstance(value, Iterable)
            indices = list(self._normalize_slice(index))
            layers = list(value)
            if len(indices) != len(layers):
                raise ValueError(
                    f"attempt to assign sequence of size {len(layers)} to extended slice of size {len(indices)}"
                )
            for i, layer in zip(indices, layers, strict=True):
                self._set_layer(i, layer)
        else:
            assert isinstance(value, Layer)
            self._set_layer(self._normalize_index(index), value)

    @overload
    def __delitem__(self, index: int) -> None: ...

    @overload
    def __delitem__(self, index: slice) -> None: ...

    def __delitem__(self, index: int | slice) -> None:
        raise NotImplementedError()  # TODO(josemmo): implement when Cadwork adds an API to handle deletions

    def _normalize_index(self, index: int) -> int:
        """Normalize index.

        Parameters
        ----------
        index : int
            Layer index.

        Returns
        -------
        int
            Normalized index.

        Raises
        ------
        IndexError
            If index is out of bounds.
        """
        length = len(self)
        if index < 0:
            index += length
        if index < 0 or index >= length:
            raise IndexError(index)
        return index

    def _normalize_slice(self, layers_slice: slice) -> range:
        """Normalize slice.

        Parameters
        ----------
        layers_slice : slice
            Layers slice.

        Returns
        -------
        range
            Range of layers matched by the slice.
        """
        length = len(self)
        return range(*layers_slice.indices(length))

    def _get_layer(self, index: int) -> Layer:
        """Get layer from index.

        Parameters
        ----------
        index : int
            Layer index.

        Returns
        -------
        Layer
            Layer instance.
        """
        layer_name = mlc.get_layer_name(self.id, index)
        layer_type = LayerType.from_cadwork(mlc.get_layer_type(self.id, index))
        layer_material = Material(mlc.get_layer_material(self.id, index))
        layer_thickness = mlc.get_layer_thickness(self.id, index)
        return Layer(
            name=layer_name,
            type=layer_type,
            material=layer_material,
            thickness=layer_thickness,
        )

    def _set_layer(self, index: int, layer: Layer) -> None:
        """Set layer at index.

        Parameters
        ----------
        index : int
            Layer index.
        layer : Layer
            Layer instance.
        """
        mlc.set_layer_name(self.id, index, layer.name)
        mlc.set_layer_type(self.id, index, layer.type.to_cadwork())
        mlc.set_layer_material(self.id, index, layer.material.id)
        mlc.set_layer_thickness(self.id, index, layer.thickness)

    def _add_layer(self, layer: Layer) -> None:
        """Add layer at the end of the stack (i.e., ``index = len(self)``).

        Parameters
        ----------
        layer : Layer
            Layer instance.
        """
        mlc.add_layer(self.id, layer.type.to_cadwork(), layer.name, layer.material.id, layer.thickness)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LayerStack) and self.id == other.id

    @final
    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(id={self.id!r}, name={self.name!r})"


class FloorLayerStack(LayerStack):
    @classmethod
    def create(cls, name: str) -> Self:
        cadwork_id = mlc.create_multi_layer_framed_floor(name)
        return cls(cadwork_id)

    @classmethod
    def _get_all(cls) -> Generator[Self, None, None]:
        for cadwork_id in [*mlc.get_multi_layer_framed_floors(), *mlc.get_multi_layer_solid_floors()]:
            yield cls(cadwork_id)


class RoofLayerStack(LayerStack):
    @classmethod
    def create(cls, name: str) -> Self:
        cadwork_id = mlc.create_multi_layer_framed_roof(name)
        return cls(cadwork_id)

    @classmethod
    def _get_all(cls) -> Generator[Self, None, None]:
        for cadwork_id in [*mlc.get_multi_layer_framed_roofs(), *mlc.get_multi_layer_solid_roofs()]:
            yield cls(cadwork_id)


class WallLayerStack(LayerStack):
    @classmethod
    def create(cls, name: str) -> Self:
        cadwork_id = mlc.create_multi_layer_framed_wall(name)
        return cls(cadwork_id)

    @classmethod
    def _get_all(cls) -> Generator[Self, None, None]:
        for cadwork_id in [
            *mlc.get_multi_layer_walls(),
            *mlc.get_multi_layer_log_walls(),
            *mlc.get_multi_layer_solid_walls(),
        ]:
            yield cls(cadwork_id)


AnyLayerStack: TypeAlias = FloorLayerStack | RoofLayerStack | WallLayerStack
