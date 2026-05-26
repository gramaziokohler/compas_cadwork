from datetime import date
from uuid import UUID

from compas_cadwork.project import Project


def test_gets_project_guid(cadwork) -> None:
    project = Project()
    cadwork.uc.get_project_guid.return_value = "{12345678-AAAA-BBBB-CCCC-DDEE12345678}"
    assert project.guid == UUID("12345678-aaaa-bbbb-cccc-ddee12345678")


def test_gets_project_name(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_name.return_value = "???"
    assert project.name is None
    cadwork.uc.get_project_name.return_value = ""
    assert project.name is None

    # With value
    cadwork.uc.get_project_name.return_value = "Project Name"
    assert project.name == "Project Name"


def test_sets_project_name(cadwork) -> None:
    project = Project()

    # Without value
    project.name = None
    cadwork.uc.set_project_name.assert_called_with("")

    # With value
    project.name = "Test Value"
    cadwork.uc.set_project_name.assert_called_with("Test Value")


def test_gets_project_part(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_part.return_value = "???"
    assert project.part is None
    cadwork.uc.get_project_part.return_value = ""
    assert project.part is None

    # With value
    cadwork.uc.get_project_part.return_value = "Project Part"
    assert project.part == "Project Part"


def test_sets_project_part(cadwork) -> None:
    project = Project()

    # Without value
    project.part = None
    cadwork.uc.set_project_part.assert_called_with("")

    # With value
    project.part = "Test Value"
    cadwork.uc.set_project_part.assert_called_with("Test Value")


def test_gets_project_number(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_number.return_value = "???"
    assert project.number is None
    cadwork.uc.get_project_number.return_value = ""
    assert project.number is None

    # With value
    cadwork.uc.get_project_number.return_value = "Project Number"
    assert project.number == "Project Number"


def test_sets_project_number(cadwork) -> None:
    project = Project()

    # Without value
    project.number = None
    cadwork.uc.set_project_number.assert_called_with("")

    # With value
    project.number = "Test Value"
    cadwork.uc.set_project_number.assert_called_with("Test Value")


def test_gets_project_deadline(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_deadline.return_value = "???"
    assert project.deadline is None
    cadwork.uc.get_project_deadline.return_value = ""
    assert project.deadline is None

    # With value
    cadwork.uc.get_project_deadline.return_value = "31.12.2026"
    assert project.deadline == date(2026, 12, 31)


def test_sets_project_deadline(cadwork) -> None:
    project = Project()

    # Without value
    project.deadline = None
    cadwork.uc.set_project_deadline.assert_called_with("")

    # With value
    project.deadline = date(2029, 1, 12)
    cadwork.uc.set_project_deadline.assert_called_with("12.01.2029")


def test_gets_project_architect(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_architect.return_value = "???"
    assert project.architect is None
    cadwork.uc.get_project_architect.return_value = ""
    assert project.architect is None

    # With value
    cadwork.uc.get_project_architect.return_value = "Jane Doe"
    assert project.architect == "Jane Doe"


def test_sets_project_architect(cadwork) -> None:
    project = Project()

    # Without value
    project.architect = None
    cadwork.uc.set_project_architect.assert_called_with("")

    # With value
    project.architect = "Test Value"
    cadwork.uc.set_project_architect.assert_called_with("Test Value")


def test_gets_project_customer(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_customer.return_value = "???"
    assert project.customer is None
    cadwork.uc.get_project_customer.return_value = ""
    assert project.customer is None

    # With value
    cadwork.uc.get_project_customer.return_value = "John Smith"
    assert project.customer == "John Smith"


def test_sets_project_customer(cadwork) -> None:
    project = Project()

    # Without value
    project.customer = None
    cadwork.uc.set_project_customer.assert_called_with("")

    # With value
    project.customer = "Test Value"
    cadwork.uc.set_project_customer.assert_called_with("Test Value")


def test_gets_project_designer(cadwork) -> None:
    project = Project()

    # Without value
    cadwork.uc.get_project_designer.return_value = "???"
    assert project.designer is None
    cadwork.uc.get_project_designer.return_value = ""
    assert project.designer is None

    # With value
    cadwork.uc.get_project_designer.return_value = "Alice Scott"
    assert project.designer == "Alice Scott"


def test_sets_project_designer(cadwork) -> None:
    project = Project()

    # Without value
    project.designer = None
    cadwork.uc.set_project_designer.assert_called_with("")

    # With value
    project.designer = "Test Value"
    cadwork.uc.set_project_designer.assert_called_with("Test Value")


def test_repr(cadwork) -> None:
    project = Project()
    cadwork.uc.get_project_guid.return_value = "{12345678-AAAA-BBBB-CCCC-DDEE12345678}"
    cadwork.uc.get_project_name.return_value = "???"
    assert repr(project) == "Project(guid=UUID('12345678-aaaa-bbbb-cccc-ddee12345678'), name=None)"
