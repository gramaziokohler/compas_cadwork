from compas_cadwork.elements.wall import Wall


def test_repr(cadwork) -> None:
    element = Wall(123)
    cadwork.ac.get_name.return_value = "Something"
    assert repr(element) == "Wall(id=123, name='Something')"
