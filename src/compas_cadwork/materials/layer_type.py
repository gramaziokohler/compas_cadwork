from enum import Enum
from typing import Self

import cadwork


class LayerType(Enum):
    """Layer type."""

    UNDEFINED = cadwork.multi_layer_type.undefined
    STRUCTURE = cadwork.multi_layer_type.structure
    PANEL = cadwork.multi_layer_type.panel
    LATHING = cadwork.multi_layer_type.lathing
    AIR = cadwork.multi_layer_type.air
    COVERING = cadwork.multi_layer_type.covering

    @classmethod
    def from_cadwork(cls, raw_type: cadwork.multi_layer_type) -> Self:
        """Get value from Cadwork multi layer type.

        Parameters
        ----------
        raw_type : cadwork.multi_layer_type
            Cadwork multi layer type.

        Returns
        -------
        LayerType
            Layer type.

        Raises
        ------
        ValueError
            If cannot determine the correct mapping type.
        """
        return cls(raw_type)

    def to_cadwork(self) -> cadwork.multi_layer_type:
        """Convert value to Cadwork multi layer type.

        Returns
        -------
        cadwork.multi_layer_type
            Cadwork multi layer type.
        """
        return self.value

    def __repr__(self) -> str:
        return f"<LayerType.{self.name}>"
