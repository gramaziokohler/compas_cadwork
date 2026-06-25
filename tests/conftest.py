import sys
from typing import Generator
from typing import Iterator
from unittest.mock import MagicMock

import pytest
from compas.geometry import Point


class Mock3dPoint(Point):
    def __repr__(self) -> str:
        return f"cadwork.point_3d({self.x!r}, {self.y!r}, {self.z!r})"


class MockVertexList:
    _vertices: list[Mock3dPoint]

    def __init__(self, vertices: list[Mock3dPoint] | None = None) -> None:
        self._vertices = vertices or []

    def count(self) -> int:
        return len(self._vertices)

    def at(self, index: int) -> Mock3dPoint:
        return self._vertices[index]

    def append(self, vertex: Mock3dPoint) -> None:
        self._vertices.append(vertex)

    def __len__(self) -> int:
        return self.count()

    def __iter__(self) -> Iterator[Mock3dPoint]:
        return iter(self._vertices)

    def __getitem__(self, index: int) -> Mock3dPoint:
        return self.at(index)

    def __repr__(self) -> str:
        return f"cadwork.vertex_list({self._vertices!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MockVertexList):
            return self._vertices == other._vertices
        return False


class CadworkMocks:
    """Utility class containing mocks for the Cadwork modules."""

    def __init__(self) -> None:
        self.cadwork = MagicMock()
        self.ac = MagicMock()
        self.bc = MagicMock()
        self.ec = MagicMock()
        self.gc = MagicMock()
        self.uc = MagicMock()

        # Apply custom patches
        self._apply_custom_patches()

        # Register mocks as modules
        sys.modules["cadwork"] = self.cadwork
        sys.modules["attribute_controller"] = self.ac
        sys.modules["bim_controller"] = self.bc
        sys.modules["element_controller"] = self.ec
        sys.modules["geometry_controller"] = self.gc
        sys.modules["utility_controller"] = self.uc

    def reset(self) -> None:
        self.cadwork.reset_mock(return_value=True, side_effect=True)
        self.ac.reset_mock(return_value=True, side_effect=True)
        self.bc.reset_mock(return_value=True, side_effect=True)
        self.ec.reset_mock(return_value=True, side_effect=True)
        self.gc.reset_mock(return_value=True, side_effect=True)
        self.uc.reset_mock(return_value=True, side_effect=True)
        self._apply_custom_patches()

    def _apply_custom_patches(self) -> None:
        self.cadwork.element_grouping_type.group = 1
        self.cadwork.element_grouping_type.subgroup = 2
        self.ac.get_element_type.return_value = self.cadwork.element_type

        self.cadwork.element_type.is_additional_element.return_value = False
        self.cadwork.element_type.is_auxiliary.return_value = False
        self.cadwork.element_type.is_cadwork.return_value = False
        self.cadwork.element_type.is_circular_axis.return_value = False
        self.cadwork.element_type.is_circular_beam.return_value = False
        self.cadwork.element_type.is_connector_axis.return_value = False
        self.cadwork.element_type.is_connector_node.return_value = False
        self.cadwork.element_type.is_container.return_value = False
        self.cadwork.element_type.is_dimension.return_value = False
        self.cadwork.element_type.is_drilling_axis.return_value = False
        self.cadwork.element_type.is_eave_axis.return_value = False
        self.cadwork.element_type.is_export_solid.return_value = False
        self.cadwork.element_type.is_export_solid_scene.return_value = False
        self.cadwork.element_type.is_floor.return_value = False
        self.cadwork.element_type.is_global_cut.return_value = False
        self.cadwork.element_type.is_line.return_value = False
        self.cadwork.element_type.is_nesting_parent.return_value = False
        self.cadwork.element_type.is_none.return_value = False
        self.cadwork.element_type.is_normal_node.return_value = False
        self.cadwork.element_type.is_opening.return_value = False
        self.cadwork.element_type.is_panel.return_value = False
        self.cadwork.element_type.is_rectangular_axis.return_value = False
        self.cadwork.element_type.is_rectangular_beam.return_value = False
        self.cadwork.element_type.is_roof.return_value = False
        self.cadwork.element_type.is_room.return_value = False
        self.cadwork.element_type.is_rotation_element.return_value = False
        self.cadwork.element_type.is_section_trace.return_value = False
        self.cadwork.element_type.is_surface.return_value = False
        self.cadwork.element_type.is_text_document.return_value = False
        self.cadwork.element_type.is_wall.return_value = False
        self.cadwork.element_type.is_wire_axis.return_value = False

        self.cadwork.point_3d = Mock3dPoint
        self.cadwork.vertex_list = MockVertexList


@pytest.fixture
def cadwork() -> Generator[CadworkMocks, None, None]:
    """Fixture to use and modify the Cadwork module mocks."""
    global _mocks
    _mocks.reset()
    yield _mocks


# Create Cadwork mocks
_mocks = CadworkMocks()
