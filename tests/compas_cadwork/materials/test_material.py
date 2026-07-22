import pytest

from compas_cadwork.materials.material import Material


def test_creates_material(cadwork) -> None:
    # Empty name
    with pytest.raises(ValueError, match=r"Material name cannot be empty"):
        Material.create("")
    cadwork.mc.get_material_id.assert_not_called()

    # Duplicate name
    cadwork.mc.get_material_id.return_value = 300
    with pytest.raises(ValueError, match=r"Name is already in use in material #300"):
        Material.create("Paper")
    cadwork.mc.get_material_id.assert_called_once_with("Paper")
    cadwork.mc.create_material.assert_not_called()
    cadwork.mc.get_material_id.reset_mock()

    # Unused name
    cadwork.mc.get_material_id.return_value = 0
    cadwork.mc.create_material.return_value = 123
    material = Material.create("Test Value")
    assert material.id == 123
    cadwork.mc.get_material_id.assert_called_once_with("Test Value")
    cadwork.mc.create_material.assert_called_once_with("Test Value")


def test_raises_on_deleted_material(cadwork) -> None:
    material = Material(123)
    cadwork.mc.get_name.return_value = ""
    with pytest.raises(RuntimeError, match=r"Cadwork material #123 no longer exists"):
        _ = material.name


def test_gets_name(cadwork) -> None:
    material = Material(123)
    cadwork.mc.get_name.return_value = "Material name"
    assert material.name == "Material name"
    cadwork.mc.get_name.assert_called_once_with(123)


def test_sets_name(cadwork) -> None:
    cadwork.mc.get_material_id.return_value = 0
    material = Material(123)
    material.name = "Test Value"
    cadwork.mc.get_material_id.assert_called_once_with("Test Value")
    cadwork.mc.set_name.assert_called_with(123, "Test Value")


def test_raises_on_set_empty_name(cadwork) -> None:
    material = Material(123)
    with pytest.raises(ValueError, match=r"Material name cannot be empty"):
        material.name = ""
    cadwork.mc.set_name.assert_not_called()


def test_raises_on_set_duplicate_name(cadwork) -> None:
    cadwork.mc.get_material_id.return_value = 200
    material = Material(123)
    with pytest.raises(ValueError, match=r"Name is already in use in material #200"):
        material.name = "Glass"
    cadwork.mc.get_material_id.assert_called_once_with("Glass")
    cadwork.mc.set_name.assert_not_called()


def test_gets_group(cadwork) -> None:
    material = Material(123)

    # Without value
    cadwork.mc.get_group.return_value = ""
    assert material.group is None
    cadwork.mc.get_group.assert_called_once_with(123)

    # With value
    cadwork.mc.get_group.return_value = "Material Group"
    assert material.group == "Material Group"


def test_sets_group(cadwork) -> None:
    material = Material(123)

    # Without value
    material.group = None
    cadwork.mc.set_group.assert_called_once_with(123, "")

    # With value
    material.group = "Test Value"
    cadwork.mc.set_group.assert_called_with(123, "Test Value")


def test_equals() -> None:
    a = Material(123)
    b = Material(123)
    c = Material(456)
    assert a == a
    assert a == b
    assert a != c
    assert b != c
    assert a is not b


def test_repr(cadwork) -> None:
    material = Material(123)
    cadwork.mc.get_name.return_value = "Some name"
    assert repr(material) == "Material(id=123, name='Some name')"
