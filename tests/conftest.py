import sys
from typing import Generator
from unittest.mock import MagicMock

import pytest
from compas.geometry import Point


class Mock3dPoint(Point):
    pass


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
        self.cadwork.point_3d = Mock3dPoint
        self.cadwork.element_grouping_type.group = 1
        self.cadwork.element_grouping_type.subgroup = 2


@pytest.fixture
def cadwork() -> Generator[CadworkMocks, None, None]:
    """Fixture to use and modify the Cadwork module mocks."""
    global _mocks
    _mocks.reset()
    yield _mocks


# Create Cadwork mocks
_mocks = CadworkMocks()
