from datetime import datetime
from pathlib import Path

import numpy
from mosaik_api import Simulator
import hdf5storage

from mosaik_hdf5_storage.hdf5_storage.library.ensure_path import ensure_path
from mosaik_hdf5_storage.hdf5_storage.library.get_options_module import \
    get_options
from mosaik_hdf5_storage.hdf5_storage.library.get_hdf5_filepath_module import \
    get_hdf5_filepath
from mosaik_hdf5_storage.hdf5_storage.reader import Hdf5Reader


class Hdf5Writer:
    @classmethod
    def write(
        cls,
        *,
        base_path: Path,
        simulator: Simulator,
        datetime_object: datetime,
        metric_name: str,
        data: dict,
    ) -> None:
        """
        Write some data to the HDF5 database.

        Note that this function is idempotent. This means that one call to
        this function has the same effect as multiple calls with the same
        parameters. In other words, this overwrites values in the database,
        but this does not overwrite the whole database. As a user of this
        function, you can write data whenever you like, resting assured that
        you will find it once in the result database, even if it was written
        multiple times.

        :param base_path: The path to create the HDF5 database in.
        :param simulator: The simulator to create a HDF5 database for.
        :param datetime_object: The datetime object to store the data for.
        :param metric_name: The metric name to store the data for.
        :param data: The data to store.

        :return: None
        """
        path: str = datetime_object.isoformat() + '/' + metric_name
        filename: str = \
            str(
                get_hdf5_filepath(
                    base_path=base_path,
                    simulator=simulator,
                )
            )
        options = get_options()

        # Do not write data already in the database
        try:
            data_read = Hdf5Reader.read(
                base_path=base_path,
                simulator=simulator,
                datetime_object=datetime_object,
                metric_name=metric_name,
            )

            try:
                numpy.testing.assert_equal(data, data_read)
                # Data is already readable from the database.
                # So do not write it again.
                return
            except AssertionError:
                # Data is not readable from the database.
                # So proceed to writing it.
                pass
        except KeyError:
            # The key to write the data to did not exist.
            # So proceed with creating it.
            pass
        except OSError:
            # File did not exist.
            # So proceed with creating it.
            pass

        ensure_path(
            path=base_path,
        )

        hdf5storage.write(
            data=data,
            path=path,
            filename=filename,
            options=options,
        )
