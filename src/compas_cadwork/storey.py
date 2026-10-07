from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING
from typing import Final

import bim_controller as bc

from compas_cadwork.utils.compatibility import requires_cadwork


if TYPE_CHECKING:
    from compas_cadwork.elements.factory import AnyElement


class Storey:
    """Storey (level) of a building."""

    name: Final[str]
    """Storey name."""

    building: Final[str]
    """Name of the building to which this storey belongs."""

    def __init__(self, *, name: str, building: str) -> None:
        """Create new instance of a Cadwork storey.

        Parameters
        ----------
        name : str
            Storey name.
        building : str
            Building name.
        """
        self.name = name
        self.building = building

    @property
    def height(self) -> float:
        """Storey height (elevation) in millimeters."""
        return bc.get_storey_height(self.building, self.name)

    @height.setter
    def height(self, value: float) -> None:
        bc.set_storey_height(self.building, self.name, value)

    @property
    @requires_cadwork(2026)
    def thickness(self) -> float:
        """Finished floor thickness in millimeters."""
        raw_value = bc.get_finished_floor_thickness(self.building, self.name)
        if raw_value < 0:
            raise RuntimeError("Cadwork storey no longer exists")
        return raw_value

    @thickness.setter
    @requires_cadwork(2026)
    def thickness(self, value: float) -> None:
        if value < 0:
            raise ValueError("Finished floor thickness cannot be negative")
        bc.set_finished_floor_thickness(self.building, self.name, value)

    @property
    @requires_cadwork(2026)
    def elements(self) -> Iterator[AnyElement]:
        """Get elements belonging to this storey.

        Returns
        -------
        Iterator[AnyElement]
            Iterator of elements.
        """
        from compas_cadwork.elements.factory import get_element_instance

        for element_id in bc.get_elements_for_storey(self.building, self.name):
            yield get_element_instance(element_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Storey) and self.name == other.name and self.building == other.building

    def __hash__(self) -> int:
        return hash((self.name, self.building))

    def __repr__(self) -> str:
        return f"Storey(name={self.name!r}, building={self.building!r}, height={self.height!r})"
