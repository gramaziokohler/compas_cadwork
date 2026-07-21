from compas_cadwork.elements.element import Element
from compas_cadwork.elements.mixins.layered_mixin import LayeredMixin
from compas_cadwork.materials.layer_stack import LayerStack


class DummyLayerStack(LayerStack):
    pass


class DummyElement(Element, LayeredMixin[DummyLayerStack]):
    @property
    def _layer_stack_type(self) -> type[DummyLayerStack]:
        return DummyLayerStack


def test_gets_layers(cadwork) -> None:
    # Without value
    element = DummyElement(123)
    cadwork.mlc.get_element_multi_layer_set.return_value = 0
    assert element.layers is None
    cadwork.mlc.get_element_multi_layer_set.assert_called_once_with(123)

    # With value
    element = DummyElement(123)
    cadwork.mlc.get_element_multi_layer_set.return_value = 1000
    layers = element.layers
    assert layers == DummyLayerStack(1000)
    assert type(layers) is DummyLayerStack


def test_sets_layers(cadwork) -> None:
    element = DummyElement(123)
    element.layers = DummyLayerStack(1000)
    cadwork.mlc.set_element_multi_layer_set.assert_called_once_with(123, 1000)
