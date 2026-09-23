from dataclasses import dataclass

from compas_cadwork.materials.layer_type import LayerType
from compas_cadwork.materials.material import Material


@dataclass(frozen=True, kw_only=True)
class Layer:
    """Material layer."""

    name: str
    """Layer name."""

    type: LayerType
    """Layer type."""

    material: Material
    """Layer material."""

    thickness: float
    """Layer thickness in millimeters."""

    def __post_init__(self) -> None:
        if self.thickness < 0:
            raise ValueError("Layer thickness cannot be negative")
