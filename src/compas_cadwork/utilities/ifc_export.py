from dataclasses import dataclass
from typing import List

import cadwork
from bim_controller import export_ifc2x3_silently_with_options
from bim_controller import export_ifc2x3_silently
from bim_controller import export_ifc

from compas_cadwork.datamodel import ElementGroupingType


@dataclass
class IFCExportSettings:
    """Represents settings for the ifc export.

    Attributes
    ----------
    grouping_type : :class:`ElementGroupingType`, optional
        Which element grouping type should be considered when exporting (e.g. group, subgroup)
    export_cover_geometry : bool, optional
        True if cover geometry should be exported, False otherwise.

    """
    grouping_type: ElementGroupingType = ElementGroupingType.NONE
    export_cover_geometry: bool = False

    def get_ifc_options(self):
        options = cadwork.ifc_options()
        aggregation = options.get_ifc_options_aggregation()
        aggregation.set_export_cover_geometry(self.export_cover_geometry)
        aggregation.set_element_aggregation_attribute(self.grouping_type.value)


def export_elements_to_ifc(element_ids: List[int], filepath: str, settings: IFCExportSettings = None) -> None:
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
    options = settings.get_ifc_options() if settings else None
    try:
        if options:
            export_ifc2x3_silently_with_options(element_ids, filepath, options)
        else:
            export_ifc2x3_silently(element_ids, filepath)
    except AttributeError:
        export_ifc(element_ids, filepath)
