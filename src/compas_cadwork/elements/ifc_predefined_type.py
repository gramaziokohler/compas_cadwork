from __future__ import annotations

from enum import Enum
from enum import auto

import bim_controller as bc
import cadwork
import element_controller as ec

from compas_cadwork.utils.compatibility import CADWORK_VERSION


def _get_cadwork_instance() -> cadwork.ifc_predefined_type:
    """Get a new IFC predefined type Cadwork instance.

    Under normal circumstances, we would just call `cadwork.ifc_predefined_type()` to get a new instance.
    However, Cadwork 2024 and Cadwork 2025 have a bug in the constructor binding.
    For those cases, we create a temporary element and get its IFC predefined type.

    See https://github.com/gramaziokohler/compas_cadwork/issues/72 for more information.
    """
    # Polyfill for buggy versions
    if CADWORK_VERSION < 2026:
        element_id = ec.create_node(cadwork.point_3d(0.0, 0.0, 0.0))
        instance = bc.get_ifc_predefined_type(element_id)
        ec.delete_elements([element_id])
        return instance

    # Use class constructor
    return cadwork.ifc_predefined_type()


class IfcPredefinedType(Enum):
    """IFC predefined type."""

    NONE = auto()
    CEILING = auto()
    CLADDING = auto()
    FLOORING = auto()
    INSULATION = auto()
    MEMBRANE = auto()
    ROOFING = auto()
    SLEEVING = auto()
    WRAPPING = auto()
    FOOTING_BEAM = auto()
    PAD_FOOTING = auto()
    PILE_CAP = auto()
    STRIP_FOOTING = auto()
    COHESION = auto()
    FRICTION = auto()
    SUPPORT = auto()
    BALUSTRADE = auto()
    GUARDRAIL = auto()
    HANDRAIL = auto()
    BASESLAB = auto()
    FLOOR = auto()
    LANDING = auto()
    ROOF = auto()
    BEAM = auto()
    HOLLOWCORE = auto()
    """@requires_cadwork(2026)"""
    JOIST = auto()
    """@requires_cadwork(2026)"""
    LINTEL = auto()
    """@requires_cadwork(2026)"""
    SPANDREL = auto()
    TBEAM = auto()
    COMPLEX = auto()
    ELEMENT = auto()
    PARTIAL = auto()
    PROVISION_FOR_SPACE = auto()
    PROVISION_FOR_VOID = auto()
    COLUMN = auto()
    PILASTER = auto()
    MOLDING = auto()
    SKIRTINGBOARD = auto()
    DOOR = auto()
    GATE = auto()
    TRAP_DOOR = auto()
    CAISSON_FOUNDATION = auto()
    BRACE = auto()
    CHORD = auto()
    COLLAR = auto()
    MEMBER = auto()
    MULLION = auto()
    PLATE = auto()
    POST = auto()
    PURLIN = auto()
    RAFTER = auto()
    STRINGER = auto()
    STRUT = auto()
    STUD = auto()
    BORED = auto()
    DRIVEN = auto()
    JETGROUTING = auto()
    CURTAIN_PANEL = auto()
    SHEET = auto()
    HALF_TURN_RAMP = auto()
    QUARTER_TURN_RAMP = auto()
    SPIRAL_RAMP = auto()
    STRAIGHT_RUN_RAMP = auto()
    TWO_QUARTER_TURN_RAMP = auto()
    TWO_STRAIGHT_RUN_RAMP = auto()
    BARREL_ROOF = auto()
    BUTTERFLY_ROOF = auto()
    DOME_ROOF = auto()
    FLAT_ROOF = auto()
    FREEFORM = auto()
    GABLE_ROOF = auto()
    GAMBREL_ROOF = auto()
    HIPPED_GABLE_ROOF = auto()
    HIP_ROOF = auto()
    MANSARD_ROOF = auto()
    PAVILION_ROOF = auto()
    RAINBOW_ROOF = auto()
    SHED_ROOF = auto()
    CURVED_RUN_STAIR = auto()
    DOUBLE_RETURN_STAIR = auto()
    HALF_TURN_STAIR = auto()
    HALF_WINDING_STAIR = auto()
    QUARTER_TURN_STAIR = auto()
    QUARTER_WINDING_STAIR = auto()
    SPIRAL_STAIR = auto()
    STRAIGHT_RUN_STAIR = auto()
    THREE_QUARTER_TURN_STAIR = auto()
    THREE_QUARTER_WINDING_STAIR = auto()
    TWO_CURVED_RUN_STAIR = auto()
    TWO_QUARTER_TURN_STAIR = auto()
    TWO_QUARTER_WINDING_STAIR = auto()
    TWO_STRAIGHT_RUN_STAIR = auto()
    CURVED = auto()
    SPIRAL = auto()
    STRAIGHT = auto()
    WINDER = auto()
    ELEMENTED_WALL = auto()
    MOVABLE = auto()
    PARAPET = auto()
    PARTITIONING = auto()
    PLUMBING_WALL = auto()
    POLYGONAL = auto()
    SHEAR = auto()
    SOLID_WALL = auto()
    STANDARD = auto()
    LIGHTDOME = auto()
    SKYLIGHT = auto()
    WINDOW = auto()
    OPENING = auto()
    RECESS = auto()
    ANCHORBOLT = auto()
    BOLT = auto()
    DOWEL = auto()
    NAIL = auto()
    NAIL_PLATE = auto()
    RIVET = auto()
    SCREW = auto()
    SHEAR_CONNECTOR = auto()
    STAPLE = auto()
    STUD_SHEAR_CONNECTOR = auto()
    GLUE = auto()
    MORTAR = auto()
    WELD = auto()
    EXTERNAL = auto()
    GFA = auto()
    INTERNAL = auto()
    PARKING = auto()
    SPACE = auto()
    ACCESSORY_ASSEMBLY = auto()
    ARCH = auto()
    BEAM_GRID = auto()
    BRACED_FRAME = auto()
    GIRDER = auto()
    REINFORCEMENT_UNIT = auto()
    RIGID_FRAME = auto()
    SLAB_FIELD = auto()
    TRUSS = auto()
    CABLE_LADDER_SEGMENT = auto()
    CABLE_TRAY_SEGMENT = auto()
    CABLE_TRUNKING_SEGMENT = auto()
    CONDUIT_SEGMENT = auto()
    BUSBAR_SEGMENT = auto()
    CABLE_SEGMENT = auto()
    CONDUCTOR_SEGMENT = auto()
    CORE_SEGMENT = auto()
    FLEXIBLE_SEGMENT = auto()
    RIGID_SEGMENT = auto()
    CULVERT = auto()
    GUTTER = auto()
    SPOOL = auto()
    AUDIO_VISUAL_OUTLET = auto()
    COMMUNICATIONS_OUTLET = auto()
    POWER_OUTLET = auto()
    DATA_OUTLET = auto()
    TELEPHONE_OUTLET = auto()
    ANCHORING = auto()
    EDGE = auto()
    LIGATURE = auto()
    MAIN = auto()
    PUNCHING = auto()
    RING = auto()

    @classmethod
    def from_cadwork(cls, raw_type: cadwork.ifc_predefined_type) -> IfcPredefinedType:
        """Get value from Cadwork IFC predefined type.

        Parameters
        ----------
        raw_type : cadwork.ifc_predefined_type
            Cadwork IFC predefined type.

        Returns
        -------
        IfcPredefinedType
            IFC predefined type.

        Raises
        ------
        ValueError
            If cannot determine the correct mapping type.
        """
        if raw_type.is_none():
            return cls.NONE
        if raw_type.is_ceiling():
            return cls.CEILING
        if raw_type.is_cladding():
            return cls.CLADDING
        if raw_type.is_flooring():
            return cls.FLOORING
        if raw_type.is_insulation():
            return cls.INSULATION
        if raw_type.is_membrane():
            return cls.MEMBRANE
        if raw_type.is_roofing():
            return cls.ROOFING
        if raw_type.is_sleeving():
            return cls.SLEEVING
        if raw_type.is_wrapping():
            return cls.WRAPPING
        if raw_type.is_footing_beam():
            return cls.FOOTING_BEAM
        if raw_type.is_pad_footing():
            return cls.PAD_FOOTING
        if raw_type.is_pile_cap():
            return cls.PILE_CAP
        if raw_type.is_strip_footing():
            return cls.STRIP_FOOTING
        if raw_type.is_cohesion():
            return cls.COHESION
        if raw_type.is_friction():
            return cls.FRICTION
        if raw_type.is_support():
            return cls.SUPPORT
        if raw_type.is_balustrade():
            return cls.BALUSTRADE
        if raw_type.is_guardrail():
            return cls.GUARDRAIL
        if raw_type.is_handrail():
            return cls.HANDRAIL
        if raw_type.is_baseslab():
            return cls.BASESLAB
        if raw_type.is_floor():
            return cls.FLOOR
        if raw_type.is_landing():
            return cls.LANDING
        if raw_type.is_roof():
            return cls.ROOF
        if raw_type.is_beam():
            return cls.BEAM
        if CADWORK_VERSION >= 2026:
            # Getters for these types were added in Cadwork 2026
            # See https://github.com/cwapi3d/cwapi3dpython/commit/6a0d0a8ba6def100ebed3cb0a4b18ed3880c5de3
            if raw_type.is_hollowcore():
                return cls.HOLLOWCORE
            if raw_type.is_joist():
                return cls.JOIST
            if raw_type.is_lintel():
                return cls.LINTEL
        if raw_type.is_spandrel():
            return cls.SPANDREL
        if raw_type.is_tbeam():
            return cls.TBEAM
        if raw_type.is_complex():
            return cls.COMPLEX
        if raw_type.is_element():
            return cls.ELEMENT
        if raw_type.is_partial():
            return cls.PARTIAL
        if raw_type.is_provision_for_space():
            return cls.PROVISION_FOR_SPACE
        if raw_type.is_provision_for_void():
            return cls.PROVISION_FOR_VOID
        if raw_type.is_column():
            return cls.COLUMN
        if raw_type.is_pilaster():
            return cls.PILASTER
        if raw_type.is_molding():
            return cls.MOLDING
        if raw_type.is_skirtingboard():
            return cls.SKIRTINGBOARD
        if raw_type.is_door():
            return cls.DOOR
        if raw_type.is_gate():
            return cls.GATE
        if raw_type.is_trap_door():
            return cls.TRAP_DOOR
        if raw_type.is_caisson_foundation():
            return cls.CAISSON_FOUNDATION
        if raw_type.is_brace():
            return cls.BRACE
        if raw_type.is_chord():
            return cls.CHORD
        if raw_type.is_collar():
            return cls.COLLAR
        if raw_type.is_member():
            return cls.MEMBER
        if raw_type.is_mullion():
            return cls.MULLION
        if raw_type.is_plate():
            return cls.PLATE
        if raw_type.is_post():
            return cls.POST
        if raw_type.is_purlin():
            return cls.PURLIN
        if raw_type.is_rafter():
            return cls.RAFTER
        if raw_type.is_stringer():
            return cls.STRINGER
        if raw_type.is_strut():
            return cls.STRUT
        if raw_type.is_stud():
            return cls.STUD
        if raw_type.is_bored():
            return cls.BORED
        if raw_type.is_driven():
            return cls.DRIVEN
        if raw_type.is_jetgrouting():
            return cls.JETGROUTING
        if raw_type.is_curtain_panel():
            return cls.CURTAIN_PANEL
        if raw_type.is_sheet():
            return cls.SHEET
        if raw_type.is_half_turn_ramp():
            return cls.HALF_TURN_RAMP
        if raw_type.is_quarter_turn_ramp():
            return cls.QUARTER_TURN_RAMP
        if raw_type.is_spiral_ramp():
            return cls.SPIRAL_RAMP
        if raw_type.is_straight_run_ramp():
            return cls.STRAIGHT_RUN_RAMP
        if raw_type.is_two_quarter_turn_ramp():
            return cls.TWO_QUARTER_TURN_RAMP
        if raw_type.is_two_straight_run_ramp():
            return cls.TWO_STRAIGHT_RUN_RAMP
        if raw_type.is_barrel_roof():
            return cls.BARREL_ROOF
        if raw_type.is_butterfly_roof():
            return cls.BUTTERFLY_ROOF
        if raw_type.is_dome_roof():
            return cls.DOME_ROOF
        if raw_type.is_flat_roof():
            return cls.FLAT_ROOF
        if raw_type.is_freeform():
            return cls.FREEFORM
        if raw_type.is_gable_roof():
            return cls.GABLE_ROOF
        if raw_type.is_gambrel_roof():
            return cls.GAMBREL_ROOF
        if raw_type.is_hipped_gable_roof():
            return cls.HIPPED_GABLE_ROOF
        if raw_type.is_hip_roof():
            return cls.HIP_ROOF
        if raw_type.is_mansard_roof():
            return cls.MANSARD_ROOF
        if raw_type.is_pavilion_roof():
            return cls.PAVILION_ROOF
        if raw_type.is_rainbow_roof():
            return cls.RAINBOW_ROOF
        if raw_type.is_shed_roof():
            return cls.SHED_ROOF
        if raw_type.is_curved_run_stair():
            return cls.CURVED_RUN_STAIR
        if raw_type.is_double_return_stair():
            return cls.DOUBLE_RETURN_STAIR
        if raw_type.is_half_turn_stair():
            return cls.HALF_TURN_STAIR
        if raw_type.is_half_winding_stair():
            return cls.HALF_WINDING_STAIR
        if raw_type.is_quarter_turn_stair():
            return cls.QUARTER_TURN_STAIR
        if raw_type.is_quarter_winding_stair():
            return cls.QUARTER_WINDING_STAIR
        if raw_type.is_spiral_stair():
            return cls.SPIRAL_STAIR
        if raw_type.is_straight_run_stair():
            return cls.STRAIGHT_RUN_STAIR
        if raw_type.is_three_quarter_turn_stair():
            return cls.THREE_QUARTER_TURN_STAIR
        if raw_type.is_three_quarter_winding_stair():
            return cls.THREE_QUARTER_WINDING_STAIR
        if raw_type.is_two_curved_run_stair():
            return cls.TWO_CURVED_RUN_STAIR
        if raw_type.is_two_quarter_turn_stair():
            return cls.TWO_QUARTER_TURN_STAIR
        if raw_type.is_two_quarter_winding_stair():
            return cls.TWO_QUARTER_WINDING_STAIR
        if raw_type.is_two_straight_run_stair():
            return cls.TWO_STRAIGHT_RUN_STAIR
        if raw_type.is_curved():
            return cls.CURVED
        if raw_type.is_spiral():
            return cls.SPIRAL
        if raw_type.is_straight():
            return cls.STRAIGHT
        if raw_type.is_winder():
            return cls.WINDER
        if raw_type.is_elemented_wall():
            return cls.ELEMENTED_WALL
        if raw_type.is_movable():
            return cls.MOVABLE
        if raw_type.is_parapet():
            return cls.PARAPET
        if raw_type.is_partitioning():
            return cls.PARTITIONING
        if raw_type.is_plumbing_wall():
            return cls.PLUMBING_WALL
        if raw_type.is_polygonal():
            return cls.POLYGONAL
        if raw_type.is_shear():
            return cls.SHEAR
        if raw_type.is_solid_wall():
            return cls.SOLID_WALL
        if raw_type.is_standard():
            return cls.STANDARD
        if raw_type.is_lightdome():
            return cls.LIGHTDOME
        if raw_type.is_skylight():
            return cls.SKYLIGHT
        if raw_type.is_window():
            return cls.WINDOW
        if raw_type.is_opening():
            return cls.OPENING
        if raw_type.is_recess():
            return cls.RECESS
        if raw_type.is_anchorbolt():
            return cls.ANCHORBOLT
        if raw_type.is_bolt():
            return cls.BOLT
        if raw_type.is_dowel():
            return cls.DOWEL
        if raw_type.is_nail():
            return cls.NAIL
        if raw_type.is_nail_plate():
            return cls.NAIL_PLATE
        if raw_type.is_rivet():
            return cls.RIVET
        if raw_type.is_screw():
            return cls.SCREW
        if raw_type.is_shear_connector():
            return cls.SHEAR_CONNECTOR
        if raw_type.is_staple():
            return cls.STAPLE
        if raw_type.is_stud_shear_connector():
            return cls.STUD_SHEAR_CONNECTOR
        if raw_type.is_glue():
            return cls.GLUE
        if raw_type.is_mortar():
            return cls.MORTAR
        if raw_type.is_weld():
            return cls.WELD
        if raw_type.is_external():
            return cls.EXTERNAL
        if raw_type.is_gfa():
            return cls.GFA
        if raw_type.is_internal():
            return cls.INTERNAL
        if raw_type.is_parking():
            return cls.PARKING
        if raw_type.is_space():
            return cls.SPACE
        if raw_type.is_accessory_assembly():
            return cls.ACCESSORY_ASSEMBLY
        if raw_type.is_arch():
            return cls.ARCH
        if raw_type.is_beam_grid():
            return cls.BEAM_GRID
        if raw_type.is_braced_frame():
            return cls.BRACED_FRAME
        if raw_type.is_girder():
            return cls.GIRDER
        if raw_type.is_reinforcement_unit():
            return cls.REINFORCEMENT_UNIT
        if raw_type.is_rigid_frame():
            return cls.RIGID_FRAME
        if raw_type.is_slab_field():
            return cls.SLAB_FIELD
        if raw_type.is_truss():
            return cls.TRUSS
        if raw_type.is_cable_ladder_segment():
            return cls.CABLE_LADDER_SEGMENT
        if raw_type.is_cable_tray_segment():
            return cls.CABLE_TRAY_SEGMENT
        if raw_type.is_cable_trunking_segment():
            return cls.CABLE_TRUNKING_SEGMENT
        if raw_type.is_conduit_segment():
            return cls.CONDUIT_SEGMENT
        if raw_type.is_busbar_segment():
            return cls.BUSBAR_SEGMENT
        if raw_type.is_cable_segment():
            return cls.CABLE_SEGMENT
        if raw_type.is_conductor_segment():
            return cls.CONDUCTOR_SEGMENT
        if raw_type.is_core_segment():
            return cls.CORE_SEGMENT
        if raw_type.is_flexible_segment():
            return cls.FLEXIBLE_SEGMENT
        if raw_type.is_rigid_segment():
            return cls.RIGID_SEGMENT
        if raw_type.is_culvert():
            return cls.CULVERT
        if raw_type.is_gutter():
            return cls.GUTTER
        if raw_type.is_spool():
            return cls.SPOOL
        if raw_type.is_audio_visual_outlet():
            return cls.AUDIO_VISUAL_OUTLET
        if raw_type.is_communications_outlet():
            return cls.COMMUNICATIONS_OUTLET
        if raw_type.is_power_outlet():
            return cls.POWER_OUTLET
        if raw_type.is_data_outlet():
            return cls.DATA_OUTLET
        if raw_type.is_telephone_outlet():
            return cls.TELEPHONE_OUTLET
        if raw_type.is_anchoring():
            return cls.ANCHORING
        if raw_type.is_edge():
            return cls.EDGE
        if raw_type.is_ligature():
            return cls.LIGATURE
        if raw_type.is_main():
            return cls.MAIN
        if raw_type.is_punching():
            return cls.PUNCHING
        if raw_type.is_ring():
            return cls.RING
        raise ValueError("Unknown Cadwork IFC predefined type")

    def to_cadwork(self) -> cadwork.ifc_predefined_type:
        """Convert value to Cadwork IFC predefined type.

        Returns
        -------
        cadwork.ifc_predefined_type
            Cadwork IFC predefined type.
        """
        raw_type = _get_cadwork_instance()
        match self:
            case IfcPredefinedType.NONE:
                raw_type.set_none()
            case IfcPredefinedType.CEILING:
                raw_type.set_ceiling()
            case IfcPredefinedType.CLADDING:
                raw_type.set_cladding()
            case IfcPredefinedType.FLOORING:
                raw_type.set_flooring()
            case IfcPredefinedType.INSULATION:
                raw_type.set_insulation()
            case IfcPredefinedType.MEMBRANE:
                raw_type.set_membrane()
            case IfcPredefinedType.ROOFING:
                raw_type.set_roofing()
            case IfcPredefinedType.SLEEVING:
                raw_type.set_sleeving()
            case IfcPredefinedType.WRAPPING:
                raw_type.set_wrapping()
            case IfcPredefinedType.FOOTING_BEAM:
                raw_type.set_footing_beam()
            case IfcPredefinedType.PAD_FOOTING:
                raw_type.set_pad_footing()
            case IfcPredefinedType.PILE_CAP:
                raw_type.set_pile_cap()
            case IfcPredefinedType.STRIP_FOOTING:
                raw_type.set_strip_footing()
            case IfcPredefinedType.COHESION:
                raw_type.set_cohesion()
            case IfcPredefinedType.FRICTION:
                raw_type.set_friction()
            case IfcPredefinedType.SUPPORT:
                raw_type.set_support()
            case IfcPredefinedType.BALUSTRADE:
                raw_type.set_balustrade()
            case IfcPredefinedType.GUARDRAIL:
                raw_type.set_guardrail()
            case IfcPredefinedType.HANDRAIL:
                raw_type.set_handrail()
            case IfcPredefinedType.BASESLAB:
                raw_type.set_baseslab()
            case IfcPredefinedType.FLOOR:
                raw_type.set_floor()
            case IfcPredefinedType.LANDING:
                raw_type.set_landing()
            case IfcPredefinedType.ROOF:
                raw_type.set_roof()
            case IfcPredefinedType.BEAM:
                raw_type.set_beam()
            case IfcPredefinedType.HOLLOWCORE:
                raw_type.set_hollowcore()
            case IfcPredefinedType.JOIST:
                raw_type.set_joist()
            case IfcPredefinedType.LINTEL:
                raw_type.set_lintel()
            case IfcPredefinedType.SPANDREL:
                raw_type.set_spandrel()
            case IfcPredefinedType.TBEAM:
                raw_type.set_tbeam()
            case IfcPredefinedType.COMPLEX:
                raw_type.set_complex()
            case IfcPredefinedType.ELEMENT:
                raw_type.set_element()
            case IfcPredefinedType.PARTIAL:
                raw_type.set_partial()
            case IfcPredefinedType.PROVISION_FOR_SPACE:
                raw_type.set_provision_for_space()
            case IfcPredefinedType.PROVISION_FOR_VOID:
                raw_type.set_provision_for_void()
            case IfcPredefinedType.COLUMN:
                raw_type.set_column()
            case IfcPredefinedType.PILASTER:
                raw_type.set_pilaster()
            case IfcPredefinedType.MOLDING:
                raw_type.set_molding()
            case IfcPredefinedType.SKIRTINGBOARD:
                raw_type.set_skirtingboard()
            case IfcPredefinedType.DOOR:
                raw_type.set_door()
            case IfcPredefinedType.GATE:
                raw_type.set_gate()
            case IfcPredefinedType.TRAP_DOOR:
                raw_type.set_trap_door()
            case IfcPredefinedType.CAISSON_FOUNDATION:
                raw_type.set_caisson_foundation()
            case IfcPredefinedType.BRACE:
                raw_type.set_brace()
            case IfcPredefinedType.CHORD:
                raw_type.set_chord()
            case IfcPredefinedType.COLLAR:
                raw_type.set_collar()
            case IfcPredefinedType.MEMBER:
                raw_type.set_member()
            case IfcPredefinedType.MULLION:
                raw_type.set_mullion()
            case IfcPredefinedType.PLATE:
                raw_type.set_plate()
            case IfcPredefinedType.POST:
                raw_type.set_post()
            case IfcPredefinedType.PURLIN:
                raw_type.set_purlin()
            case IfcPredefinedType.RAFTER:
                raw_type.set_rafter()
            case IfcPredefinedType.STRINGER:
                raw_type.set_stringer()
            case IfcPredefinedType.STRUT:
                raw_type.set_strut()
            case IfcPredefinedType.STUD:
                raw_type.set_stud()
            case IfcPredefinedType.BORED:
                raw_type.set_bored()
            case IfcPredefinedType.DRIVEN:
                raw_type.set_driven()
            case IfcPredefinedType.JETGROUTING:
                raw_type.set_jetgrouting()
            case IfcPredefinedType.CURTAIN_PANEL:
                raw_type.set_curtain_panel()
            case IfcPredefinedType.SHEET:
                raw_type.set_sheet()
            case IfcPredefinedType.HALF_TURN_RAMP:
                raw_type.set_half_turn_ramp()
            case IfcPredefinedType.QUARTER_TURN_RAMP:
                raw_type.set_quarter_turn_ramp()
            case IfcPredefinedType.SPIRAL_RAMP:
                raw_type.set_spiral_ramp()
            case IfcPredefinedType.STRAIGHT_RUN_RAMP:
                raw_type.set_straight_run_ramp()
            case IfcPredefinedType.TWO_QUARTER_TURN_RAMP:
                raw_type.set_two_quarter_turn_ramp()
            case IfcPredefinedType.TWO_STRAIGHT_RUN_RAMP:
                raw_type.set_two_straight_run_ramp()
            case IfcPredefinedType.BARREL_ROOF:
                raw_type.set_barrel_roof()
            case IfcPredefinedType.BUTTERFLY_ROOF:
                raw_type.set_butterfly_roof()
            case IfcPredefinedType.DOME_ROOF:
                raw_type.set_dome_roof()
            case IfcPredefinedType.FLAT_ROOF:
                raw_type.set_flat_roof()
            case IfcPredefinedType.FREEFORM:
                raw_type.set_freeform()
            case IfcPredefinedType.GABLE_ROOF:
                raw_type.set_gable_roof()
            case IfcPredefinedType.GAMBREL_ROOF:
                raw_type.set_gambrel_roof()
            case IfcPredefinedType.HIPPED_GABLE_ROOF:
                raw_type.set_hipped_gable_roof()
            case IfcPredefinedType.HIP_ROOF:
                raw_type.set_hip_roof()
            case IfcPredefinedType.MANSARD_ROOF:
                raw_type.set_mansard_roof()
            case IfcPredefinedType.PAVILION_ROOF:
                raw_type.set_pavilion_roof()
            case IfcPredefinedType.RAINBOW_ROOF:
                raw_type.set_rainbow_roof()
            case IfcPredefinedType.SHED_ROOF:
                raw_type.set_shed_roof()
            case IfcPredefinedType.CURVED_RUN_STAIR:
                raw_type.set_curved_run_stair()
            case IfcPredefinedType.DOUBLE_RETURN_STAIR:
                raw_type.set_double_return_stair()
            case IfcPredefinedType.HALF_TURN_STAIR:
                raw_type.set_half_turn_stair()
            case IfcPredefinedType.HALF_WINDING_STAIR:
                raw_type.set_half_winding_stair()
            case IfcPredefinedType.QUARTER_TURN_STAIR:
                raw_type.set_quarter_turn_stair()
            case IfcPredefinedType.QUARTER_WINDING_STAIR:
                raw_type.set_quarter_winding_stair()
            case IfcPredefinedType.SPIRAL_STAIR:
                raw_type.set_spiral_stair()
            case IfcPredefinedType.STRAIGHT_RUN_STAIR:
                raw_type.set_straight_run_stair()
            case IfcPredefinedType.THREE_QUARTER_TURN_STAIR:
                raw_type.set_three_quarter_turn_stair()
            case IfcPredefinedType.THREE_QUARTER_WINDING_STAIR:
                raw_type.set_three_quarter_winding_stair()
            case IfcPredefinedType.TWO_CURVED_RUN_STAIR:
                raw_type.set_two_curved_run_stair()
            case IfcPredefinedType.TWO_QUARTER_TURN_STAIR:
                raw_type.set_two_quarter_turn_stair()
            case IfcPredefinedType.TWO_QUARTER_WINDING_STAIR:
                raw_type.set_two_quarter_winding_stair()
            case IfcPredefinedType.TWO_STRAIGHT_RUN_STAIR:
                raw_type.set_two_straight_run_stair()
            case IfcPredefinedType.CURVED:
                raw_type.set_curved()
            case IfcPredefinedType.SPIRAL:
                raw_type.set_spiral()
            case IfcPredefinedType.STRAIGHT:
                raw_type.set_straight()
            case IfcPredefinedType.WINDER:
                raw_type.set_winder()
            case IfcPredefinedType.ELEMENTED_WALL:
                raw_type.set_elemented_wall()
            case IfcPredefinedType.MOVABLE:
                raw_type.set_movable()
            case IfcPredefinedType.PARAPET:
                raw_type.set_parapet()
            case IfcPredefinedType.PARTITIONING:
                raw_type.set_partitioning()
            case IfcPredefinedType.PLUMBING_WALL:
                raw_type.set_plumbing_wall()
            case IfcPredefinedType.POLYGONAL:
                raw_type.set_polygonal()
            case IfcPredefinedType.SHEAR:
                raw_type.set_shear()
            case IfcPredefinedType.SOLID_WALL:
                raw_type.set_solid_wall()
            case IfcPredefinedType.STANDARD:
                raw_type.set_standard()
            case IfcPredefinedType.LIGHTDOME:
                raw_type.set_lightdome()
            case IfcPredefinedType.SKYLIGHT:
                raw_type.set_skylight()
            case IfcPredefinedType.WINDOW:
                raw_type.set_window()
            case IfcPredefinedType.OPENING:
                raw_type.set_opening()
            case IfcPredefinedType.RECESS:
                raw_type.set_recess()
            case IfcPredefinedType.ANCHORBOLT:
                raw_type.set_anchorbolt()
            case IfcPredefinedType.BOLT:
                raw_type.set_bolt()
            case IfcPredefinedType.DOWEL:
                raw_type.set_dowel()
            case IfcPredefinedType.NAIL:
                raw_type.set_nail()
            case IfcPredefinedType.NAIL_PLATE:
                raw_type.set_nailplate()
            case IfcPredefinedType.RIVET:
                raw_type.set_rivet()
            case IfcPredefinedType.SCREW:
                raw_type.set_screw()
            case IfcPredefinedType.SHEAR_CONNECTOR:
                raw_type.set_shearconnector()
            case IfcPredefinedType.STAPLE:
                raw_type.set_staple()
            case IfcPredefinedType.STUD_SHEAR_CONNECTOR:
                raw_type.set_studshearconnector()
            case IfcPredefinedType.GLUE:
                raw_type.set_glue()
            case IfcPredefinedType.MORTAR:
                raw_type.set_mortar()
            case IfcPredefinedType.WELD:
                raw_type.set_weld()
            case IfcPredefinedType.EXTERNAL:
                raw_type.set_external()
            case IfcPredefinedType.GFA:
                raw_type.set_gfa()
            case IfcPredefinedType.INTERNAL:
                raw_type.set_internal()
            case IfcPredefinedType.PARKING:
                raw_type.set_parking()
            case IfcPredefinedType.SPACE:
                raw_type.set_space()
            case IfcPredefinedType.ACCESSORY_ASSEMBLY:
                raw_type.set_accessory_assembly()
            case IfcPredefinedType.ARCH:
                raw_type.set_arch()
            case IfcPredefinedType.BEAM_GRID:
                raw_type.set_beam_grid()
            case IfcPredefinedType.BRACED_FRAME:
                raw_type.set_braced_frame()
            case IfcPredefinedType.GIRDER:
                raw_type.set_girder()
            case IfcPredefinedType.REINFORCEMENT_UNIT:
                raw_type.set_reinforcement_unit()
            case IfcPredefinedType.RIGID_FRAME:
                raw_type.set_rigid_frame()
            case IfcPredefinedType.SLAB_FIELD:
                raw_type.set_slab_field()
            case IfcPredefinedType.TRUSS:
                raw_type.set_truss()
            case IfcPredefinedType.CABLE_LADDER_SEGMENT:
                raw_type.set_cable_ladder_segment()
            case IfcPredefinedType.CABLE_TRAY_SEGMENT:
                raw_type.set_cable_tray_segment()
            case IfcPredefinedType.CABLE_TRUNKING_SEGMENT:
                raw_type.set_cable_trunking_segment()
            case IfcPredefinedType.CONDUIT_SEGMENT:
                raw_type.set_conduit_segment()
            case IfcPredefinedType.BUSBAR_SEGMENT:
                raw_type.set_busbar_segment()
            case IfcPredefinedType.CABLE_SEGMENT:
                raw_type.set_cable_segment()
            case IfcPredefinedType.CONDUCTOR_SEGMENT:
                raw_type.set_conductor_segment()
            case IfcPredefinedType.CORE_SEGMENT:
                raw_type.set_core_segment()
            case IfcPredefinedType.FLEXIBLE_SEGMENT:
                raw_type.set_flexible_segment()
            case IfcPredefinedType.RIGID_SEGMENT:
                raw_type.set_rigid_segment()
            case IfcPredefinedType.CULVERT:
                raw_type.set_culvert()
            case IfcPredefinedType.GUTTER:
                raw_type.set_gutter()
            case IfcPredefinedType.SPOOL:
                raw_type.set_spool()
            case IfcPredefinedType.AUDIO_VISUAL_OUTLET:
                raw_type.set_audio_visual_outlet()
            case IfcPredefinedType.COMMUNICATIONS_OUTLET:
                raw_type.set_communications_outlet()
            case IfcPredefinedType.POWER_OUTLET:
                raw_type.set_power_outlet()
            case IfcPredefinedType.DATA_OUTLET:
                raw_type.set_data_outlet()
            case IfcPredefinedType.TELEPHONE_OUTLET:
                raw_type.set_telephone_outlet()
            case IfcPredefinedType.ANCHORING:
                raw_type.set_anchoring()
            case IfcPredefinedType.EDGE:
                raw_type.set_edge()
            case IfcPredefinedType.LIGATURE:
                raw_type.set_ligature()
            case IfcPredefinedType.MAIN:
                raw_type.set_main()
            case IfcPredefinedType.PUNCHING:
                raw_type.set_punching()
            case IfcPredefinedType.RING:
                raw_type.set_ring()
        return raw_type

    def __repr__(self) -> str:
        return f"<IfcPredefinedType.{self.name}>"
