import logging
import os
from enum import Enum
from typing import List

from list_controller import export_cover_list
from list_controller import export_part_list
from list_controller import export_production_list

LOG = logging.getLogger(__name__)


class ExportOption(Enum):
    PART_LIST = "part_list"
    COVER_LIST = "cover_list"
    FASTENER_LIST = "fastener_list"

    def __str__(self):
        return self.value


class CSVExporter:
    """Used to export elements to CSV files.

    Sets the required global settings for the export and restores them after the export.

    """

    def __init__(self):
        pass

    def export_elements_to_CSV(self, element_ids: List[int], list_type: ExportOption, filepath: str):
        """Exports elements to CSV file.

        Parameters
        ----------
        element_ids : list(int)
            List of element ids to export.
        list_type : str
            Type of list to export (e.g., "part_list", "cover_list", "fastener_list").
        filepath : str
            Path to the resulting CSV file.

        """
        filepath = os.path.abspath(filepath)
        try:
            LOG.debug(f"Exporting CSV: element_ids={element_ids}, list_type={list_type}, filepath={filepath}")
            export_function = self.get_export_function(list_type)
            success = export_function(element_ids, filepath)
            LOG.debug(f"Export successful: {success}")
        except FileNotFoundError as ex:
            LOG.exception(f"File not found: {ex}")
        except Exception as ex:
            LOG.exception(f"Failed to export elements to CSV: {ex}")

    def get_export_function(self, list_type: str):
        """Returns the export function based on the list type."""
        export_functions = {
            ExportOption.PART_LIST: export_part_list,
            ExportOption.COVER_LIST: export_cover_list,
            ExportOption.FASTENER_LIST: export_production_list,
        }
        return export_functions.get(list_type, None)
