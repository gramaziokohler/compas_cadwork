import pytest

from compas_cadwork.storey import Storey


def test_gets_height(cadwork) -> None:
    storey = Storey(name="Storey name", building="Building name")
    cadwork.bc.get_storey_height.return_value = 1234.56
    assert storey.height == 1234.56
    cadwork.bc.get_storey_height.assert_called_once_with("Building name", "Storey name")


def test_sets_height(cadwork) -> None:
    storey = Storey(name="Storey name", building="Building name")
    storey.height = 1000.22
    cadwork.bc.set_storey_height.assert_called_once_with("Building name", "Storey name", 1000.22)


def test_gets_thickness(cadwork) -> None:
    storey = Storey(name="Storey name", building="Building name")
    cadwork.bc.get_finished_floor_thickness.return_value = 543.21
    assert storey.thickness == 543.21
    cadwork.bc.get_finished_floor_thickness.assert_called_once_with("Building name", "Storey name")


def test_sets_thickness(cadwork) -> None:
    storey = Storey(name="Storey name", building="Building name")
    storey.thickness = 200.11
    cadwork.bc.set_finished_floor_thickness.assert_called_once_with("Building name", "Storey name", 200.11)


def test_raises_on_set_negative_thickness() -> None:
    storey = Storey(name="Storey name", building="Building name")
    with pytest.raises(ValueError, match=r"Finished floor thickness cannot be negative"):
        storey.thickness = -0.50


def test_raises_on_deleted_storey(cadwork) -> None:
    storey = Storey(name="Storey name", building="Building name")
    cadwork.bc.get_finished_floor_thickness.return_value = -1.0
    with pytest.raises(RuntimeError, match=r"Cadwork storey no longer exists"):
        _ = storey.thickness


def test_gets_elements(cadwork) -> None:
    storey = Storey(name="Storey name", building="Building name")

    # Without value
    cadwork.bc.get_elements_for_storey.return_value = []
    assert len(list(storey.elements)) == 0
    cadwork.bc.get_elements_for_storey.assert_called_once_with("Building name", "Storey name")
    cadwork.bc.get_elements_for_storey.reset_mock()

    # With value
    cadwork.cadwork.element_type.return_value.is_panel.return_value = True
    cadwork.bc.get_elements_for_storey.return_value = [123, 456, 789]
    assert [x.id for x in storey.elements] == [123, 456, 789]


def test_equals() -> None:
    a = Storey(name="EG", building="Some building")
    b = Storey(name="EG", building="Some building")
    c = Storey(name="OG", building="Some building")
    d = Storey(name="EG", building="Other building")
    assert a == a
    assert a == b
    assert a != c
    assert b != c
    assert c != d
    assert a is not b


def test_hash() -> None:
    a = Storey(name="EG", building="Some building")
    b = Storey(name="EG", building="Some building")
    c = Storey(name="OG", building="Some building")
    d = Storey(name="EG", building="Other building")
    assert hash(a) == hash(b)
    assert hash(a) != hash(c)
    assert hash(b) != hash(c)
    assert hash(c) != hash(d)
    assert len({a, b, c}) == 2


def test_repr(cadwork) -> None:
    storey = Storey(name="Storey name", building="Building name")
    cadwork.bc.get_storey_height.return_value = 2500.0
    assert repr(storey) == "Storey(name='Storey name', building='Building name', height=2500.0)"
