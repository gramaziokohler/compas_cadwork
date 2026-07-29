import pytest

from compas_cadwork.elements.wall import Wall
from compas_cadwork.transaction import Transaction
from compas_cadwork.transaction import enqueue_element_deletion
from compas_cadwork.transaction import is_inside_transaction
from compas_cadwork.transaction import notify_element_creation
from compas_cadwork.transaction import notify_element_modification


def test_raises_on_reentry_context() -> None:
    tx = Transaction()
    with tx:
        with pytest.raises(RuntimeError, match=r"Instance is already in use"):
            with tx:
                pass  # pragma: no cover


def test_sets_up_and_tears_down_context(cadwork) -> None:
    # Without elements
    with Transaction():
        cadwork.uc.disable_auto_display_refresh.assert_called_once()
        cadwork.uc.enable_auto_display_refresh.assert_not_called()
    cadwork.uc.enable_auto_display_refresh.assert_called_once()
    cadwork.uc.disable_auto_display_refresh.reset_mock()
    cadwork.uc.enable_auto_display_refresh.reset_mock()

    # With elements
    with Transaction():
        enqueue_element_deletion(1000)
        notify_element_creation(123)
        notify_element_modification(456)
        notify_element_modification(789)
        enqueue_element_deletion(2000)
    cadwork.ec.add_created_elements_to_undo.assert_called_once_with([123])
    cadwork.ec.add_modified_elements_to_undo.assert_called_once_with([456, 789])
    cadwork.ec.delete_elements_with_undo.assert_called_once_with([1000, 2000])
    cadwork.ec.make_undo.assert_not_called()


def test_rolls_back_on_error(cadwork) -> None:
    # With created, modified and deleted elements
    try:
        with Transaction():
            notify_element_creation(123)
            notify_element_modification(456)
            enqueue_element_deletion(789)
            raise RuntimeError("Oh, no!")
    except RuntimeError:
        pass
    assert cadwork.ec.make_undo.call_count == 3
    cadwork.ec.make_undo.reset_mock()

    # With created elements only
    try:
        with Transaction():
            notify_element_creation(1000)
            notify_element_creation(2000)
            raise RuntimeError("Oh, no!")
    except RuntimeError:
        pass
    assert cadwork.ec.make_undo.call_count == 1


def test_allows_nested_contexts() -> None:
    tx_outer = Transaction()
    tx_inner = Transaction()
    with tx_outer:
        notify_element_creation(1000)
        with tx_inner:
            notify_element_creation(100)
            notify_element_modification(200)
        notify_element_creation(2000)
    assert tx_outer._created_ids == {1000, 2000}
    assert tx_outer._modified_ids == set()
    assert tx_inner._created_ids == {100}
    assert tx_inner._modified_ids == {200}


def test_detects_running_inside_context() -> None:
    assert not is_inside_transaction()
    with Transaction():
        assert is_inside_transaction()
    assert not is_inside_transaction()


def test_receives_element_creation_events() -> None:
    tx = Transaction()
    with tx:
        notify_element_creation(123)
        notify_element_creation(456)
    assert tx._created_ids == {123, 456}
    assert tx._modified_ids == set()
    assert tx._deleted_ids == set()


def test_receives_element_modification_events() -> None:
    tx = Transaction()
    with tx:
        notify_element_modification(1000)
        notify_element_modification(2000)
    assert tx._created_ids == set()
    assert tx._modified_ids == {1000, 2000}
    assert tx._deleted_ids == set()


def test_handles_element_deletions() -> None:
    tx = Transaction()
    with tx:
        enqueue_element_deletion(100)
        enqueue_element_deletion(200)
    assert tx._created_ids == set()
    assert tx._modified_ids == set()
    assert tx._deleted_ids == {100, 200}


def test_raises_when_enqueuing_element_deletion_outside_context() -> None:
    with pytest.raises(RuntimeError, match=r"Cannot enqueue an element deletion outside of a transaction context"):
        enqueue_element_deletion(123)


def test_gets_created_elements(cadwork) -> None:
    tx = Transaction()
    tx._created_ids.add(123)
    tx._created_ids.add(456)
    cadwork.cadwork.element_type.return_value.is_wall.return_value = True
    assert set(tx.created_elements) == {Wall(123), Wall(456)}
    assert set(tx.modified_elements) == set()


def test_gets_modified_elements(cadwork) -> None:
    tx = Transaction()
    tx._modified_ids.add(123)
    tx._modified_ids.add(456)
    cadwork.cadwork.element_type.return_value.is_wall.return_value = True
    assert set(tx.created_elements) == set()
    assert set(tx.modified_elements) == {Wall(123), Wall(456)}


def test_gets_all_elements(cadwork) -> None:
    tx = Transaction()
    tx._created_ids.add(123)
    tx._modified_ids.add(456)
    tx._created_ids.add(789)
    cadwork.cadwork.element_type.return_value.is_wall.return_value = True
    assert set(tx.elements) == {Wall(123), Wall(456), Wall(789)}
