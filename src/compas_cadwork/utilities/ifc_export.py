import logging
import os
from dataclasses import dataclass
from typing import List

import bim_controller as bc
import utility_controller as uc

from compas_cadwork.datamodel import ElementGroupingType

LOG = logging.getLogger(__name__)


@dataclass
class IFCExportSettings:
    """Represents settings for the ifc export.

    Attributes
    ----------
    grouping_type : :class:`ElementGroupingType`, optional
        Which element grouping type should be considered when exporting (e.g. group, subgroup)
    export_cover_geometry : bool, optional
        True if cover geometry should be exported, False otherwise.
    translate_local_frame : bool, optional
        If True, the local frame of the elements will be translated on export
        to the global frame set with `utility_controller.set_global_origin`.

    """

    grouping_type: ElementGroupingType = ElementGroupingType.NONE
    export_cover_geometry: bool = False
    translate_local_frame: bool = False

    def get_ifc_options(self):
        options = bc.get_ifc_options()
        aggregation = options.get_ifc_options_aggregation()
        aggregation.set_export_cover_geometry(self.export_cover_geometry)
        aggregation.set_element_aggregation_attribute(self.grouping_type.to_cadwork())
        aggregation.set_consider_element_aggregation(self.grouping_type != ElementGroupingType.NONE)

        properties = options.get_ifc_options_properties()
        properties.set_export_bim_wood_property(True)

        lod_settings = options.get_ifc_options_level_of_detail()
        lod_settings.set_export_endtype_materialization(False)
        lod_settings.set_export_vba_drillings(False)
        lod_settings.set_export_vba_components(False)
        lod_settings.set_cut_drillings(True)
        lod_settings.set_export_vba_components(True)
        lod_settings.set_cut_installation_round(False)
        lod_settings.set_export_installation_rectangular_materialization(True)
        lod_settings.set_cut_installation_rectangular(False)
        return options


class IFCExporter:
    """Used to export elements to ifc files.

    Sets the required global settings for the export and restores them after the export.

    """

    def __init__(self, settings: IFCExportSettings = None) -> None:
        self.settings = settings or IFCExportSettings()
        self._translate_local_frame = None

    def export_elements_to_ifc(self, element_ids: List[int], filepath: str) -> None:
        """Exports elements to ifc file.

        Parameters
        ----------
        element_ids : list(int)
            List of element ids to export.
        filepath : str
            Path to the resulting ifc file.
        settings : :class:`IFCExportSettings`, optional
            Settings for the ifc export.

        """
        self.initialize()
        filepath = os.path.abspath(filepath)
        options = self.settings.get_ifc_options()
        try:
            LOG.debug(f"""export_ifc4_silently_with_options(element_i_ds={type(element_ids)}({type(element_ids[0])}), file_path={type(filepath)}, options={type(options)})""")
            success = bc.export_ifc4_silently_with_options(element_ids, filepath, options)
            LOG.debug(f"export_ifc4_silently_with_options: {success}")
        except Exception as ex:
            LOG.exception(f"Failed to export elements to ifc. {str(ex)}")
        finally:
            self.cleanup()

    def initialize(self):
        """Sets any global settings that are required for the export."""
        self._translate_local_frame = uc.get_use_of_global_coordinates()
        uc.set_use_of_global_coordinates(self.settings.translate_local_frame)

    def cleanup(self):
        """Restores any global settings that were changed during the export."""
        uc.set_use_of_global_coordinates(self._translate_local_frame)
