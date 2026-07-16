import pytest

from compas_cadwork.material import Material


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
    cadwork.mc.get_all_materials.return_value = []
    material = Material(123)
    material.name = "Test Value"
    cadwork.mc.set_name.assert_called_with(123, "Test Value")


def test_raises_on_empty_name(cadwork) -> None:
    material = Material(123)
    with pytest.raises(ValueError, match=r"Material name cannot be empty"):
        material.name = ""
    cadwork.mc.set_name.assert_not_called()


def test_raises_on_duplicate_name(cadwork) -> None:
    cadwork.mc.get_all_materials.return_value = [100, 200, 300]
    cadwork.mc.get_name.side_effect = lambda x: {100: "Wood", 200: "Glass", 300: "Paper"}[x]
    material = Material(123)
    with pytest.raises(ValueError, match=r"New name is already in use in material #200"):
        material.name = "Glass"
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
