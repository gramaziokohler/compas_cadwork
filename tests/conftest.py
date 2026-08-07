import sys
from collections.abc import Generator
from collections.abc import Iterator
from enum import IntEnum
from unittest.mock import MagicMock

import pytest
from compas.geometry import Point


class MockMultiLayerType(IntEnum):
    undefined = 0
    structure = 1
    panel = 2
    lathing = 3
    air = 4
    covering = 5


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
        self.mc = MagicMock()
        self.mlc = MagicMock()
        self.uc = MagicMock()
        self.vc = MagicMock()

        # Apply custom patches
        self._apply_custom_patches()

        # Register mocks as modules
        sys.modules["cadwork"] = self.cadwork
        sys.modules["attribute_controller"] = self.ac
        sys.modules["bim_controller"] = self.bc
        sys.modules["element_controller"] = self.ec
        sys.modules["geometry_controller"] = self.gc
        sys.modules["material_controller"] = self.mc
        sys.modules["multi_layer_cover_controller"] = self.mlc
        sys.modules["utility_controller"] = self.uc
        sys.modules["visualization_controller"] = self.vc

    def reset(self) -> None:
        self.cadwork.reset_mock(return_value=True, side_effect=True)
        self.ac.reset_mock(return_value=True, side_effect=True)
        self.bc.reset_mock(return_value=True, side_effect=True)
        self.ec.reset_mock(return_value=True, side_effect=True)
        self.gc.reset_mock(return_value=True, side_effect=True)
        self.mc.reset_mock(return_value=True, side_effect=True)
        self.mlc.reset_mock(return_value=True, side_effect=True)
        self.uc.reset_mock(return_value=True, side_effect=True)
        self.vc.reset_mock(return_value=True, side_effect=True)
        self._apply_custom_patches()

    def _apply_custom_patches(self) -> None:
        self.cadwork.element_grouping_type.group = 1
        self.cadwork.element_grouping_type.subgroup = 2
        self.ac.get_element_type.side_effect = lambda _: self.cadwork.element_type()
        self.bc.get_ifc2x3_element_type.side_effect = lambda _: self.cadwork.ifc_2x3_element_type()
        self.bc.get_ifc_predefined_type.side_effect = lambda _: self.cadwork.ifc_predefined_type()

        self.cadwork.element_type.return_value.is_additional_element.return_value = False
        self.cadwork.element_type.return_value.is_auxiliary.return_value = False
        self.cadwork.element_type.return_value.is_cadwork.return_value = False
        self.cadwork.element_type.return_value.is_circular_axis.return_value = False
        self.cadwork.element_type.return_value.is_circular_beam.return_value = False
        self.cadwork.element_type.return_value.is_connector_axis.return_value = False
        self.cadwork.element_type.return_value.is_connector_node.return_value = False
        self.cadwork.element_type.return_value.is_container.return_value = False
        self.cadwork.element_type.return_value.is_dimension.return_value = False
        self.cadwork.element_type.return_value.is_drilling_axis.return_value = False
        self.cadwork.element_type.return_value.is_eave_axis.return_value = False
        self.cadwork.element_type.return_value.is_export_solid.return_value = False
        self.cadwork.element_type.return_value.is_export_solid_scene.return_value = False
        self.cadwork.element_type.return_value.is_floor.return_value = False
        self.cadwork.element_type.return_value.is_global_cut.return_value = False
        self.cadwork.element_type.return_value.is_line.return_value = False
        self.cadwork.element_type.return_value.is_nesting_parent.return_value = False
        self.cadwork.element_type.return_value.is_none.return_value = False
        self.cadwork.element_type.return_value.is_normal_node.return_value = False
        self.cadwork.element_type.return_value.is_opening.return_value = False
        self.cadwork.element_type.return_value.is_panel.return_value = False
        self.cadwork.element_type.return_value.is_rectangular_axis.return_value = False
        self.cadwork.element_type.return_value.is_rectangular_beam.return_value = False
        self.cadwork.element_type.return_value.is_roof.return_value = False
        self.cadwork.element_type.return_value.is_room.return_value = False
        self.cadwork.element_type.return_value.is_rotation_element.return_value = False
        self.cadwork.element_type.return_value.is_section_trace.return_value = False
        self.cadwork.element_type.return_value.is_surface.return_value = False
        self.cadwork.element_type.return_value.is_text_document.return_value = False
        self.cadwork.element_type.return_value.is_wall.return_value = False
        self.cadwork.element_type.return_value.is_wire_axis.return_value = False

        self.cadwork.ifc_2x3_element_type.return_value.is_none.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_beam.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_column.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_curtain_wall.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_door.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_member.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_plate.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_railing.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_ramp.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_ramp_flight.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_roof.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_slab.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_stair.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_stair_flight.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_wall.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_wall_standard_case.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_window.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_building_element_proxy.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_chimney.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_covering.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_footing.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_furnishing_element.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_opening_element.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_space.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_flow_segment.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_building_element_part.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_discrete_accessory.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_fastener.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_mechanical_fastener.return_value = False
        self.cadwork.ifc_2x3_element_type.return_value.is_ifc_element_assembly.return_value = False

        self.cadwork.ifc_predefined_type.return_value.is_none.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_ceiling.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_cladding.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_flooring.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_insulation.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_membrane.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_roofing.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_sleeving.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_wrapping.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_footing_beam.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_pad_footing.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_pile_cap.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_strip_footing.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_cohesion.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_friction.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_support.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_balustrade.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_guardrail.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_handrail.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_baseslab.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_floor.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_landing.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_beam.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_spandrel.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_tbeam.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_complex.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_element.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_partial.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_provision_for_space.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_provision_for_void.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_column.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_pilaster.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_molding.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_skirtingboard.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_door.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_gate.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_trap_door.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_caisson_foundation.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_brace.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_chord.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_collar.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_member.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_mullion.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_plate.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_post.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_purlin.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_rafter.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_stringer.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_strut.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_stud.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_bored.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_driven.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_jetgrouting.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_curtain_panel.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_sheet.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_half_turn_ramp.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_quarter_turn_ramp.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_spiral_ramp.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_straight_run_ramp.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_two_quarter_turn_ramp.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_two_straight_run_ramp.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_barrel_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_butterfly_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_dome_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_flat_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_freeform.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_gable_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_gambrel_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_hipped_gable_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_hip_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_mansard_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_pavilion_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_rainbow_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_shed_roof.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_curved_run_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_double_return_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_half_turn_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_half_winding_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_quarter_turn_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_quarter_winding_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_spiral_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_straight_run_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_three_quarter_turn_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_three_quarter_winding_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_two_curved_run_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_two_quarter_turn_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_two_quarter_winding_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_two_straight_run_stair.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_curved.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_spiral.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_straight.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_winder.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_elemented_wall.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_movable.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_parapet.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_partitioning.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_plumbing_wall.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_polygonal.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_shear.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_solid_wall.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_standard.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_lightdome.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_skylight.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_window.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_opening.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_recess.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_anchorbolt.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_bolt.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_dowel.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_nail.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_nail_plate.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_rivet.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_screw.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_shear_connector.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_staple.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_stud_shear_connector.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_glue.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_mortar.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_weld.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_external.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_gfa.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_internal.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_parking.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_space.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_accessory_assembly.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_arch.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_beam_grid.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_braced_frame.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_girder.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_reinforcement_unit.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_rigid_frame.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_slab_field.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_truss.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_cable_ladder_segment.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_cable_tray_segment.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_cable_trunking_segment.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_conduit_segment.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_busbar_segment.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_cable_segment.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_conductor_segment.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_core_segment.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_flexible_segment.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_rigid_segment.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_culvert.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_gutter.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_spool.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_audio_visual_outlet.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_communications_outlet.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_power_outlet.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_data_outlet.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_telephone_outlet.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_anchoring.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_edge.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_ligature.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_main.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_punching.return_value = False
        self.cadwork.ifc_predefined_type.return_value.is_ring.return_value = False

        self.cadwork.multi_layer_type = MockMultiLayerType
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
