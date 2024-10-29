import logging
from typing import Dict

from compas.data import Data
from compas.data import json_dump
from compas.data import json_dumps
from compas.data import json_load
from compas.data import json_loads
from utility_controller import get_project_data
from utility_controller import set_project_data

LOG = logging.getLogger(__name__)


class StorageError(Exception):
    """Indicates a failed save operation to persistent storage."""

    pass


class Storage:
    """Base class for storage implementations."""

    def save(self, data: Dict | Data):
        """Save the data to the storage."""
        raise NotImplementedError

    def load(self) -> Dict | Data:
        """Load the data from the storage."""
        raise NotImplementedError


class ProjectStorage(Storage):
    """Saves stuff to persistency using the project data storage.

    This will store said stuff inside the currently open cadwork 3d project file.

    Parameters
    ----------
    key : str
        A project-wide unique key to store the data under.
    """

    def __init__(self, key: str):
        self._key = key

    def save(self, data: Dict | Data):
        """Save the data to the project storage.

        Note
        ----
        The data is not really saved until the project file is saved.

        Parameters
        ----------
        data : dict or :class:`compas.data.Data`
            The data to save.

        """
        data_str = json_dumps(data)
        LOG.debug(f"save to key:{self._key} data: {data_str}")
        set_project_data(self._key, data_str)
        # TODO: should we trigger a file save here? otherwise the data is not really saved

    def load(self) -> Dict | Data:
        """Load the data from the project storage.

        Raises
        ------
        StorageError
            If no data is found for the key.

        Returns
        -------
        dict or :class:`compas.data.Data`
            The loaded data.
        """
        data_str = get_project_data(self._key)
        LOG.debug(f"load from key:{self._key} data: {data_str}")
        if not data_str:
            raise StorageError(f"No data found for key: {self._key}")
        return json_loads(data_str)


class FileStorage(Storage):
    """Saves stuff to a local file.

    Parameters
    ----------
    filepath : str
        The path to the file to save to.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath

    def save(self, data: Dict | Data):
        """Save the data to the file.

        Raises
        ------
        StorageError
            If the save operation fails.

        Parameters
        ----------
        data : dict or :class:`compas.data.Data`
            The data to save.
        """
        try:
            json_dump(data, self.filepath, pretty=True)
            LOG.debug("Data saved successfully to file.")
        except Exception as e:
            raise StorageError(f"Failed to save data to file: {e}")

    def load(self) -> Dict | Data:
        """Load the data from the file.

        Raises
        ------
        StorageError
            If the load operation fails.

        Returns
        -------
        dict or :class:`compas.data.Data`
            The loaded data.
        """
        try:
            return json_load(self.filepath)
        except Exception as e:
            raise StorageError(f"Failed to load data from file: {e}")
