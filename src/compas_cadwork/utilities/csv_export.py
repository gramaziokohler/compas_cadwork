import logging
import os
from typing import List

from list_controller import export_part_list

LOG = logging.getLogger(__name__)


class CSVExporter:
    """Used to export elements to csv files.

    Sets the required global settings for the export and restores them after the export.

    """

    def __init__(self):
        pass

    def export_elements_to_CSV(self, element_ids: List[int], filepath: str):
        """Exports elements to CSV file.

        Parameters
        ----------
        element_ids : list(int)
            List of element ids to export.
        filepath : str
            Path to the resulting CSV file.

        """
        filepath = os.path.abspath(filepath)
        try:
            LOG.debug(
                f"""export_CSV_silently(element_i_ds={type(element_ids)}({type(element_ids[0])}), file_path={type(filepath)})"""
            )
            success = export_part_list(element_ids, filepath)
            LOG.debug(f"export_CSV_silently: {success}")
        except Exception as ex:
            LOG.exception(f"Failed to export elements to CSV. {str(ex)}")
