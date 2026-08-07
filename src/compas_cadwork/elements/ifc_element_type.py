from __future__ import annotations

from enum import Enum

import cadwork


class IfcElementType(Enum):
    """IFC element type."""

    NONE = "None"
    BEAM = "Beam"
    COLUMN = "Column"
    CURTAIN_WALL = "CurtainWall"
    DOOR = "Door"
    MEMBER = "Member"
    PLATE = "Plate"
    RAILING = "Railing"
    RAMP = "Ramp"
    RAMP_FLIGHT = "RampFlight"
    ROOF = "Roof"
    SLAB = "Slab"
    STAIR = "Stair"
    STAIR_FLIGHT = "StairFlight"
    WALL = "Wall"
    WALL_STANDARD_CASE = "WallStandardCase"
    WINDOW = "Window"
    BUILDING_ELEMENT_PROXY = "BuildingElementProxy"
    CHIMNEY = "Chimney"
    COVERING = "Covering"
    FOOTING = "Footing"
    FURNISHING_ELEMENT = "FurnishingElement"
    OPENING_ELEMENT = "OpeningElement"
    SPACE = "Space"
    FLOW_SEGMENT = "FlowSegment"
    BUILDING_ELEMENT_PART = "BuildingElementPart"
    DISCRETE_ACCESSORY = "DiscreteAccessory"
    FASTENER = "Fastener"
    MECHANICAL_FASTENER = "MechanicalFastener"
    ELEMENT_ASSEMBLY = "ElementAssembly"

    @classmethod
    def from_cadwork(cls, raw_type: cadwork.ifc_2x3_element_type) -> IfcElementType:
        """Get value from Cadwork IFC2x3 element type.

        Parameters
        ----------
        raw_type : cadwork.ifc_2x3_element_type
            Cadwork IFC2x3 element type.

        Returns
        -------
        IfcElementType
            IFC element type.

        Raises
        ------
        ValueError
            If cannot determine the correct mapping type.
        """
        # Here we use `__repr__` instead of querying `is_*()` methods to achieve direct O(1) lookup
        return cls(str(raw_type))

    def to_cadwork(self) -> cadwork.ifc_2x3_element_type:
        """Convert value to Cadwork IFC2x3 element type.

        Returns
        -------
        cadwork.ifc_2x3_element_type
            Cadwork IFC2x3 element type.
        """
        raw_type = cadwork.ifc_2x3_element_type()
        match self:
            case IfcElementType.NONE:
                raw_type.set_none()
            case IfcElementType.BEAM:
                raw_type.set_ifc_beam()
            case IfcElementType.COLUMN:
                raw_type.set_ifc_column()
            case IfcElementType.CURTAIN_WALL:
                raw_type.set_ifc_curtain_wall()
            case IfcElementType.DOOR:
                raw_type.set_ifc_door()
            case IfcElementType.MEMBER:
                raw_type.set_ifc_member()
            case IfcElementType.PLATE:
                raw_type.set_ifc_plate()
            case IfcElementType.RAILING:
                raw_type.set_ifc_railing()
            case IfcElementType.RAMP:
                raw_type.set_ifc_ramp()
            case IfcElementType.RAMP_FLIGHT:
                raw_type.set_ifc_ramp_flight()
            case IfcElementType.ROOF:
                raw_type.set_ifc_roof()
            case IfcElementType.SLAB:
                raw_type.set_ifc_slab()
            case IfcElementType.STAIR:
                raw_type.set_ifc_stair()
            case IfcElementType.STAIR_FLIGHT:
                raw_type.set_ifc_stair_flight()
            case IfcElementType.WALL:
                raw_type.set_ifc_wall()
            case IfcElementType.WALL_STANDARD_CASE:
                raw_type.set_ifc_wall_standard_case()
            case IfcElementType.WINDOW:
                raw_type.set_ifc_window()
            case IfcElementType.BUILDING_ELEMENT_PROXY:
                raw_type.set_ifc_building_element_proxy()
            case IfcElementType.CHIMNEY:
                raw_type.set_ifc_chimney()
            case IfcElementType.COVERING:
                raw_type.set_ifc_covering()
            case IfcElementType.FOOTING:
                raw_type.set_ifc_footing()
            case IfcElementType.FURNISHING_ELEMENT:
                raw_type.set_ifc_furnishing_element()
            case IfcElementType.OPENING_ELEMENT:
                raw_type.set_ifc_opening_element()
            case IfcElementType.SPACE:
                raw_type.set_ifc_space()
            case IfcElementType.FLOW_SEGMENT:
                raw_type.set_ifc_flow_segment()
            case IfcElementType.BUILDING_ELEMENT_PART:
                raw_type.set_ifc_building_element_part()
            case IfcElementType.DISCRETE_ACCESSORY:
                raw_type.set_ifc_discrete_accessory()
            case IfcElementType.FASTENER:
                raw_type.set_ifc_fastener()
            case IfcElementType.MECHANICAL_FASTENER:
                raw_type.set_ifc_mechanical_fastener()
            case IfcElementType.ELEMENT_ASSEMBLY:
                raw_type.set_ifc_element_assembly()
        return raw_type

    def __repr__(self) -> str:
        return f"<IfcElementType.{self.name}>"
