from pathlib import Path


def get_hdf5_filepath(
    *,
    base_path, simulator,
) -> Path:
    simulator_name: str = simulator.__class__.__name__
    hdf5_file_path: Path = base_path / f'{simulator_name}.h5'

    return hdf5_file_path
