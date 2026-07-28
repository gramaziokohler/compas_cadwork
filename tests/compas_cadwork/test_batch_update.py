import pytest

from compas_cadwork.batch_update import BatchUpdate
from compas_cadwork.batch_update import is_inside_context
from compas_cadwork.batch_update import notify_element_creation
from compas_cadwork.batch_update import notify_element_modification
from compas_cadwork.elements.wall import Wall


def test_raises_on_reentry_context() -> None:
    batch = BatchUpdate()
    with batch:
        with pytest.raises(RuntimeError, match=r"Instance is already in use"):
            with batch:
                pass  # pragma: no cover


def test_sets_up_and_tears_down_context(cadwork) -> None:
    # Without elements
    with BatchUpdate():
        cadwork.uc.disable_auto_display_refresh.assert_called_once()
        cadwork.uc.enable_auto_display_refresh.assert_not_called()
    cadwork.uc.enable_auto_display_refresh.assert_called_once()
    cadwork.uc.disable_auto_display_refresh.reset_mock()
    cadwork.uc.enable_auto_display_refresh.reset_mock()

    # With elements
    with BatchUpdate():
        notify_element_creation(123)
        notify_element_modification(456)
        notify_element_modification(789)
    cadwork.ec.add_created_elements_to_undo.assert_called_once_with([123])
    cadwork.ec.add_modified_elements_to_undo.assert_called_once_with([456, 789])


def test_allows_nested_contexts() -> None:
    batch_outer = BatchUpdate()
    batch_inner = BatchUpdate()
    with batch_outer:
        notify_element_creation(1000)
        with batch_inner:
            notify_element_creation(100)
            notify_element_modification(200)
        notify_element_creation(2000)
    assert batch_outer._created_ids == {1000, 2000}
    assert batch_outer._modified_ids == set()
    assert batch_inner._created_ids == {100}
    assert batch_inner._modified_ids == {200}


def test_detects_running_inside_context() -> None:
    assert not is_inside_context()
    with BatchUpdate():
        assert is_inside_context()
    assert not is_inside_context()


def test_receives_element_creation_events() -> None:
    batch = BatchUpdate()
    with batch:
        notify_element_creation(123)
        notify_element_creation(456)
    assert batch._created_ids == {123, 456}
    assert batch._modified_ids == set()


def test_receives_element_modification_events() -> None:
    batch = BatchUpdate()
    with batch:
        notify_element_modification(1000)
        notify_element_modification(2000)
    assert batch._created_ids == set()
    assert batch._modified_ids == {1000, 2000}


def test_gets_created_elements(cadwork) -> None:
    batch = BatchUpdate()
    batch._created_ids.add(123)
    batch._created_ids.add(456)
    cadwork.cadwork.element_type.return_value.is_wall.return_value = True
    assert set(batch.created_elements) == {Wall(123), Wall(456)}
    assert set(batch.modified_elements) == set()


def test_gets_modified_elements(cadwork) -> None:
    batch = BatchUpdate()
    batch._modified_ids.add(123)
    batch._modified_ids.add(456)
    cadwork.cadwork.element_type.return_value.is_wall.return_value = True
    assert set(batch.created_elements) == set()
    assert set(batch.modified_elements) == {Wall(123), Wall(456)}


def test_gets_all_elements(cadwork) -> None:
    batch = BatchUpdate()
    batch._created_ids.add(123)
    batch._modified_ids.add(456)
    batch._created_ids.add(789)
    cadwork.cadwork.element_type.return_value.is_wall.return_value = True
    assert set(batch.elements) == {Wall(123), Wall(456), Wall(789)}
