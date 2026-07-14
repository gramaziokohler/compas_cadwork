from abc import abstractmethod
from collections.abc import MutableMapping
from typing import Iterable
from typing import Iterator
from typing import TypeVar


_K = TypeVar("_K")
_V = TypeVar("_V")


class KeyValueStorage(MutableMapping[_K, _V]):
    """Generic class for handling key-value storage of user attributes and additional data."""

    _KEY_TYPE: type[_K]

    @staticmethod
    @abstractmethod
    def _empty(key: _K, value: _V) -> bool:
        """Check whether a value is empty.

        NOTE: Empty values are hidden from storage to avoid confusion.
        We do this as Cadwork does not always have a reliable method of checking whether a key is set.

        Parameters
        ----------
        key : _K
            Storage key for context.
        value : _V
            Value to check.

        Returns
        -------
        bool
            Whether value is considered empty.
        """

    @abstractmethod
    def _get(self, key: _K) -> _V:
        """Get value from underlying implementation.

        Parameters
        ----------
        key : _K
            Storage key.

        Returns
        -------
        _V
            Raw value.
        """

    @abstractmethod
    def _set(self, key: _K, value: _V) -> None:
        """Set value to underlying implementation.

        Parameters
        ----------
        key : _K
            Storage key.
        value : _V
            New value.
        """

    @abstractmethod
    def _delete(self, key: _K) -> None:
        """Delete value from underlying implementation.

        Parameters
        ----------
        key : _K
            Storage key.
        """

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, self._KEY_TYPE):
            return False
        raw_value = self._get(key)
        return not self._empty(key, raw_value)

    def __getitem__(self, key: _K) -> _V:
        raw_value = self._get(key)
        if self._empty(key, raw_value):
            raise KeyError(key)
        return raw_value

    def __setitem__(self, key: _K, value: _V) -> None:
        if self._empty(key, value):
            raise ValueError("Cannot set an empty value")
        self._set(key, value)

    def __delitem__(self, key: _K) -> None:
        raw_value = self._get(key)
        if self._empty(key, raw_value):
            raise KeyError(key)
        self._delete(key)

    def __iter__(self) -> Iterator[_K]:
        raise TypeError(f"{self.__class__.__name__!r} is not iterable")

    def __len__(self) -> int:
        raise TypeError(f"{self.__class__.__name__!r} is not countable")


class IterableKeyValueStorage(KeyValueStorage[_K, _V]):
    """Superset of a key-value storage with support for iterating over its items."""

    @abstractmethod
    def _keys(self) -> Iterable[_K]:
        """Get keys from underlying implementation.

        Returns
        -------
        Iterable[_K]
            Iterator of keys.
        """

    def __iter__(self) -> Iterator[_K]:
        for key in self._keys():
            raw_value = self._get(key)
            if not self._empty(key, raw_value):
                yield key

    def __len__(self) -> int:
        count = 0
        for key in self._keys():
            raw_value = self._get(key)
            if not self._empty(key, raw_value):
                count += 1
        return count
