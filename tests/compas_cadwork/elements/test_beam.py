from compas_cadwork.elements.beam import Beam


def test_repr(cadwork) -> None:
    element = Beam(123)
    cadwork.ac.get_name.return_value = "Something"
    assert repr(element) == "Beam(id=123, name='Something')"
