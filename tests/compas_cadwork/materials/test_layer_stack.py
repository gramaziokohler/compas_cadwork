from unittest import mock

import pytest

from compas_cadwork.materials.layer import Layer
from compas_cadwork.materials.layer_stack import FloorLayerStack
from compas_cadwork.materials.layer_stack import LayerStack
from compas_cadwork.materials.layer_stack import RoofLayerStack
from compas_cadwork.materials.layer_stack import WallLayerStack
from compas_cadwork.materials.layer_type import LayerType
from compas_cadwork.materials.material import Material


@pytest.fixture
def expected_layers(cadwork) -> list[Layer]:
    layers = [
        Layer(name="Layer A", type=LayerType.STRUCTURE, material=Material(1111), thickness=100.0),
        Layer(name="Layer B", type=LayerType.PANEL, material=Material(2222), thickness=200.0),
        Layer(name="Layer C", type=LayerType.COVERING, material=Material(3333), thickness=300.0),
        Layer(name="Layer D", type=LayerType.UNDEFINED, material=Material(4444), thickness=400.0),
    ]
    cadwork.mlc.get_layer_count.return_value = len(layers)
    cadwork.mlc.get_layer_name.side_effect = lambda _, i: layers[i].name
    cadwork.mlc.get_layer_type.side_effect = lambda _, i: layers[i].type.to_cadwork()
    cadwork.mlc.get_layer_material.side_effect = lambda _, i: layers[i].material.id
    cadwork.mlc.get_layer_thickness.side_effect = lambda _, i: layers[i].thickness
    return layers


def test_creates_layer_stack(cadwork) -> None:
    # Floors
    cadwork.mlc.create_multi_layer_framed_floor.return_value = 1000
    layer_stack = FloorLayerStack.create("Floor Layer Stack")
    assert layer_stack == FloorLayerStack(1000)
    cadwork.mlc.create_multi_layer_framed_floor.assert_called_once_with("Floor Layer Stack")

    # Roofs
    cadwork.mlc.create_multi_layer_framed_roof.return_value = 2000
    layer_stack = RoofLayerStack.create("Roof Layer Stack")
    assert layer_stack == RoofLayerStack(2000)
    cadwork.mlc.create_multi_layer_framed_roof.assert_called_once_with("Roof Layer Stack")

    # Walls
    cadwork.mlc.create_multi_layer_framed_wall.return_value = 3000
    layer_stack = WallLayerStack.create("Wall Layer Stack")
    assert layer_stack == WallLayerStack(3000)
    cadwork.mlc.create_multi_layer_framed_wall.assert_called_once_with("Wall Layer Stack")


def test_gets_all_instances(cadwork) -> None:
    # Floors
    cadwork.mlc.get_multi_layer_framed_floors.return_value = [100]
    cadwork.mlc.get_multi_layer_solid_floors.return_value = [200, 300]
    assert list(FloorLayerStack._get_all()) == [FloorLayerStack(100), FloorLayerStack(200), FloorLayerStack(300)]

    # Roofs
    cadwork.mlc.get_multi_layer_framed_roofs.return_value = [400, 500]
    cadwork.mlc.get_multi_layer_solid_roofs.return_value = [600]
    assert list(RoofLayerStack._get_all()) == [RoofLayerStack(400), RoofLayerStack(500), RoofLayerStack(600)]

    # Walls
    cadwork.mlc.get_multi_layer_walls.return_value = [700]
    cadwork.mlc.get_multi_layer_log_walls.return_value = [800]
    cadwork.mlc.get_multi_layer_solid_walls.return_value = [900]
    assert list(WallLayerStack._get_all()) == [WallLayerStack(700), WallLayerStack(800), WallLayerStack(900)]

    # All
    assert list(LayerStack._get_all()) == [
        FloorLayerStack(100),
        FloorLayerStack(200),
        FloorLayerStack(300),
        RoofLayerStack(400),
        RoofLayerStack(500),
        RoofLayerStack(600),
        WallLayerStack(700),
        WallLayerStack(800),
        WallLayerStack(900),
    ]


def test_gets_name(cadwork) -> None:
    layers = FloorLayerStack(123)
    cadwork.mlc.get_multi_layer_set_name.return_value = "Test Value"
    assert layers.name == "Test Value"
    cadwork.mlc.get_multi_layer_set_name.assert_called_once_with(123)


def test_sets_name(cadwork) -> None:
    layers = FloorLayerStack(123)
    layers.name = "Test Value"
    cadwork.mlc.set_multi_layer_set_name.assert_called_with(123, "Test Value")


def test_gets_length(cadwork) -> None:
    layers = FloorLayerStack(123)
    cadwork.mlc.get_layer_count.return_value = 7
    assert len(layers) == 7
    cadwork.mlc.get_layer_count.assert_called_with(123)


def test_iterates_over_layers(expected_layers) -> None:
    layers = FloorLayerStack(123)
    assert list(layers) == expected_layers


def test_gets_layers(cadwork, expected_layers) -> None:
    layers = FloorLayerStack(123)

    # Single index
    for i in [*list(range(len(expected_layers))), -1, -2, -3]:
        expected_i = i % len(layers)
        assert layers[i] == expected_layers[i]
        cadwork.mlc.get_layer_name.assert_called_once_with(123, expected_i)
        cadwork.mlc.get_layer_type.assert_called_once_with(123, expected_i)
        cadwork.mlc.get_layer_material.assert_called_once_with(123, expected_i)
        cadwork.mlc.get_layer_thickness.assert_called_once_with(123, expected_i)
        cadwork.mlc.get_layer_name.reset_mock()
        cadwork.mlc.get_layer_type.reset_mock()
        cadwork.mlc.get_layer_material.reset_mock()
        cadwork.mlc.get_layer_thickness.reset_mock()
    with pytest.raises(IndexError, match=r"100"):
        _ = layers[100]

    # Slice
    assert list(layers[0:2]) == expected_layers[0:2]
    assert list(layers[1:]) == expected_layers[1:]
    assert list(layers[100:200]) == []


def test_sets_layers(cadwork) -> None:
    layers = FloorLayerStack(123)
    cadwork.mlc.get_layer_count.return_value = 4

    # Single index
    test_layer = Layer(name="Test Value", type=LayerType.AIR, material=Material(1000), thickness=22.0)
    layers[2] = test_layer
    cadwork.mlc.set_layer_name.assert_called_once_with(123, 2, "Test Value")
    cadwork.mlc.set_layer_type.assert_called_once_with(123, 2, cadwork.cadwork.multi_layer_type.air)
    cadwork.mlc.set_layer_material.assert_called_once_with(123, 2, 1000)
    cadwork.mlc.set_layer_thickness.assert_called_once_with(123, 2, 22.0)
    cadwork.mlc.set_layer_name.reset_mock()
    cadwork.mlc.set_layer_type.reset_mock()
    cadwork.mlc.set_layer_material.reset_mock()
    cadwork.mlc.set_layer_thickness.reset_mock()
    with pytest.raises(IndexError, match=r"100"):
        layers[100] = test_layer

    # Slice
    layers[2:] = [
        Layer(name="Second to Last Layer", type=LayerType.PANEL, material=Material(1000), thickness=22.0),
        Layer(name="Last Layer", type=LayerType.UNDEFINED, material=Material(2000), thickness=33.0),
    ]
    cadwork.mlc.set_layer_name.assert_has_calls(
        [
            mock.call(123, 2, "Second to Last Layer"),
            mock.call(123, 3, "Last Layer"),
        ],
    )
    cadwork.mlc.set_layer_type.assert_has_calls(
        [
            mock.call(123, 2, cadwork.cadwork.multi_layer_type.panel),
            mock.call(123, 3, cadwork.cadwork.multi_layer_type.undefined),
        ],
    )
    cadwork.mlc.set_layer_material.assert_has_calls(
        [
            mock.call(123, 2, 1000),
            mock.call(123, 3, 2000),
        ],
    )
    cadwork.mlc.set_layer_thickness.assert_has_calls(
        [
            mock.call(123, 2, 22.0),
            mock.call(123, 3, 33.0),
        ],
    )


def test_adds_layers_to_empty_stack(cadwork) -> None:
    layers = FloorLayerStack(123)
    new_layer = Layer(name="New Layer", type=LayerType.COVERING, material=Material(1000), thickness=22.0)
    cadwork.mlc.get_layer_count.return_value = 0
    layers.append(new_layer)
    cadwork.mlc.set_layer_name.assert_not_called()
    cadwork.mlc.set_layer_type.assert_not_called()
    cadwork.mlc.set_layer_material.assert_not_called()
    cadwork.mlc.set_layer_thickness.assert_not_called()
    cadwork.mlc.add_layer.assert_called_once_with(
        123,
        cadwork.cadwork.multi_layer_type.covering,
        "New Layer",
        1000,
        22.0,
    )


def test_inserts_layers(cadwork, expected_layers) -> None:
    layers = FloorLayerStack(123)

    # At the end
    new_layer = Layer(name="End Layer", type=LayerType.COVERING, material=Material(1000), thickness=22.0)
    layers.append(new_layer)
    cadwork.mlc.set_layer_name.assert_not_called()
    cadwork.mlc.set_layer_type.assert_not_called()
    cadwork.mlc.set_layer_material.assert_not_called()
    cadwork.mlc.set_layer_thickness.assert_not_called()
    cadwork.mlc.add_layer.assert_called_once_with(
        123,
        cadwork.cadwork.multi_layer_type.covering,
        "End Layer",
        1000,
        22.0,
    )
    cadwork.mlc.add_layer.reset_mock()

    # At the start
    new_layer = Layer(name="Start Layer", type=LayerType.LATHING, material=Material(2000), thickness=140.6)
    layers.insert(0, new_layer)
    cadwork.mlc.add_layer.assert_called_once_with(
        123,
        cadwork.cadwork.multi_layer_type.undefined,
        "Layer D",
        4444,
        400.0,
    )
    cadwork.mlc.set_layer_name.assert_has_calls(
        [
            mock.call(123, 3, "Layer C"),
            mock.call(123, 2, "Layer B"),
            mock.call(123, 1, "Layer A"),
            mock.call(123, 0, "Start Layer"),
        ],
    )
    cadwork.mlc.set_layer_type.assert_has_calls(
        [
            mock.call(123, 3, cadwork.cadwork.multi_layer_type.covering),
            mock.call(123, 2, cadwork.cadwork.multi_layer_type.panel),
            mock.call(123, 1, cadwork.cadwork.multi_layer_type.structure),
            mock.call(123, 0, cadwork.cadwork.multi_layer_type.lathing),
        ],
    )
    cadwork.mlc.set_layer_material.assert_has_calls(
        [
            mock.call(123, 3, 3333),
            mock.call(123, 2, 2222),
            mock.call(123, 1, 1111),
            mock.call(123, 0, 2000),
        ],
    )
    cadwork.mlc.set_layer_thickness.assert_has_calls(
        [
            mock.call(123, 3, 300.0),
            mock.call(123, 2, 200.0),
            mock.call(123, 1, 100.0),
            mock.call(123, 0, 140.6),
        ],
    )
    cadwork.mlc.add_layer.reset_mock()
    cadwork.mlc.set_layer_name.reset_mock()
    cadwork.mlc.set_layer_type.reset_mock()
    cadwork.mlc.set_layer_material.reset_mock()
    cadwork.mlc.set_layer_thickness.reset_mock()


# TODO(josemmo): update test when deletion is implemented
def test_deletes_layers(cadwork) -> None:
    layers = FloorLayerStack(123)
    with pytest.raises(NotImplementedError):
        del layers[0]


def test_equals() -> None:
    a = FloorLayerStack(123)
    b = WallLayerStack(123)
    c = FloorLayerStack(456)
    assert a == a
    assert a == b
    assert a != c
    assert b != c
    assert a is not b


def test_repr(cadwork) -> None:
    cadwork.mlc.get_multi_layer_set_name.return_value = "Some name"
    floor_layers = FloorLayerStack(123)
    assert repr(floor_layers) == "FloorLayerStack(id=123, name='Some name')"
    wall_layers = WallLayerStack(456)
    assert repr(wall_layers) == "WallLayerStack(id=456, name='Some name')"
