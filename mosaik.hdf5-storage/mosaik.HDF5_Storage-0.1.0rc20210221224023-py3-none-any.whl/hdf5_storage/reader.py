import datetime
from pathlib import Path
from typing import Any

import hdf5storage
from mosaik_api import Simulator

from mosaik_hdf5_storage.hdf5_storage.library.get_path_module import get_path
from mosaik_hdf5_storage.hdf5_storage.library.get_hdf5_filepath_module import \
    get_hdf5_filepath


class Hdf5Reader:
    @classmethod
    def read(
        cls,
        *,
        base_path: Path,
        datetime_object: datetime,
        simulator: Simulator,
        metric_name: str,
    ) -> Any:
        """
        Read some data from the HDF5 database.

        :param base_path: The path to read the HDF5 database from.
        :param simulator: The simulator to read the HDF5 database for.
        :param datetime_object: The datetime object to read the data for.
        :param metric_name: The metric name to read the data for.

        :return: The data read by the given parameters.
        """
        path: str = get_path(
            datetime_object=datetime_object,
            metric_name=metric_name,
        )
        hdf5_file_path_string: str = \
            str(
                get_hdf5_filepath(
                    base_path=base_path,
                    simulator=simulator,
                )
            )

        data: Any = hdf5storage.read(
            path=path,
            filename=hdf5_file_path_string,
        )

        return data
