from typing import Iterable

import pytest

from compas_cadwork.utils.storage import IterableKeyValueStorage
from compas_cadwork.utils.storage import KeyValueStorage


class BackedStorage(KeyValueStorage[int, str]):
    _KEY_TYPE = int
    _data: dict[int, str]

    def __init__(self, data: dict[int, str]) -> None:
        self._data = data

    @staticmethod
    def _empty(key: int, value: str) -> bool:
        return value == "<NIL>"

    def _get(self, key: int) -> str:
        return self._data.get(key, "<NIL>")

    def _set(self, key: int, value: str) -> None:
        self._data[key] = value

    def _delete(self, key: int) -> None:
        del self._data[key]


class IterableBackedStorage(IterableKeyValueStorage[int, str]):
    _KEY_TYPE = int
    _data: dict[int, str]

    def __init__(self, data: dict[int, str]) -> None:
        self._data = data

    @staticmethod
    def _empty(key: int, value: str) -> bool:
        return value == "<NIL>"

    def _get(self, key: int) -> str:
        return self._data.get(key, "<NIL>")

    def _set(self, key: int, value: str) -> None:
        self._data[key] = value

    def _delete(self, key: int) -> None:
        del self._data[key]

    def _keys(self) -> Iterable[int]:
        return self._data.keys()


@pytest.fixture
def storage() -> BackedStorage:
    return BackedStorage(
        {
            100: "One hundred",
            101: "<NIL>",
            200: "Two hundred",
            300: "Three hundred",
            301: "Three hundred and one",
        }
    )


@pytest.fixture
def iterable_storage() -> IterableBackedStorage:
    return IterableBackedStorage(
        {
            100: "One hundred",
            101: "<NIL>",
            200: "Two hundred",
            300: "Three hundred",
            301: "Three hundred and one",
        }
    )


def test_handles_contains(storage) -> None:
    assert 100 in storage
    assert 101 not in storage
    assert 200 in storage
    assert 201 not in storage
    assert 300 in storage
    assert 301 in storage
    assert 400 not in storage


def test_handles_get(storage) -> None:
    assert storage[100] == "One hundred"
    with pytest.raises(KeyError):
        _ = storage[101]
    assert storage[200] == "Two hundred"
    assert storage[300] == "Three hundred"
    assert storage[301] == "Three hundred and one"
    with pytest.raises(KeyError, match=r"400"):
        _ = storage[400]


def test_handles_set(storage) -> None:
    storage[101] = "One hundred and one"
    assert storage[101] == "One hundred and one"
    storage[102] = "New key"
    assert storage[102] == "New key"
    storage[300] = "New Value"
    assert storage[300] == "New Value"
    with pytest.raises(ValueError, match=r"Cannot set an empty value"):
        storage[400] = "<NIL>"


def test_handles_delete(storage) -> None:
    del storage[200]
    assert 200 not in storage
    with pytest.raises(KeyError, match=r"200"):
        del storage[200]
    with pytest.raises(KeyError, match=r"321"):
        del storage[321]


def test_handles_iterate(iterable_storage) -> None:
    assert list(iterable_storage.keys()) == [100, 200, 300, 301]
    assert list(iterable_storage.values()) == ["One hundred", "Two hundred", "Three hundred", "Three hundred and one"]


def test_handles_length(iterable_storage) -> None:
    assert len(iterable_storage) == 4
    iterable_storage[500] = "Another item"
    assert len(iterable_storage) == 5


def test_raises_on_non_iterable(storage) -> None:
    with pytest.raises(TypeError, match=r"'BackedStorage' is not iterable"):
        _ = list(storage.keys())


def test_raises_on_non_countable(storage) -> None:
    with pytest.raises(TypeError, match=r"'BackedStorage' is not countable"):
        _ = len(storage)
