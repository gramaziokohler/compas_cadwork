import logging
from typing import Dict
from compas.data import Data
from compas.data import json_dumps
from compas.data import json_loads
from compas.data import json_dump
from compas.data import json_load

from utility_controller import set_project_data
from utility_controller import get_project_data

LOG = logging.getLogger(__name__)


class StorageError(Exception):
    pass


class Storage:
    def save(self, data: Dict | Data):
        raise NotImplementedError

    def load(self) -> Dict | Data:
        raise NotImplementedError


class ProjectStorage(Storage):
    """Saves stuff to persistency using the project data storage.

    This will store said stuff inside the currently open cadwork 3d project file.

    Parameters
    ----------
    key : str
        The key to store the data under.
    """

    def __init__(self, key: str):
        self._key = key

    def save(self, data: Dict | Data):
        data_str = json_dumps(data)
        set_project_data(self._key, data_str)

    def load(self) -> Dict | Data:
        data_str = get_project_data(self._key)
        if not data_str:
            raise StorageError(f"No data found for key: {self._key}")
        return json_loads(data_str)


class FileStorage(Storage):
    """Saves stuff to a local file."""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def save(self, data: Dict | Data):
        try:
            json_dump(data, self.filepath, pretty=True)
            LOG.debug("Data saved successfully to file.")
        except Exception as e:
            raise StorageError(f"Failed to save data to file: {e}")

    def load(self) -> Dict | Data:
        try:
            return json_load(self.filepath)
        except Exception as e:
            raise StorageError(f"Failed to load data from file: {e}")
