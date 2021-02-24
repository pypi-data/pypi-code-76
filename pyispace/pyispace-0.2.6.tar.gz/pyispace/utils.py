from functools import reduce
from pathlib import Path

import numpy as np
import pandas as pd
from shapely import geometry

from .trace import FootprintOutput
from .train import Model


z_cols = ['z_1', 'z_2']
output_idx_name = 'Row'


def vstack_with_sep(a: np.ndarray, b: np.ndarray, sep=np.nan):
    assert a.shape[1] == b.shape[1]
    sep_arr = np.ones((1, a.shape[1])) * sep
    return np.vstack((a, sep_arr, b))


def join_polygons(poly):
    if isinstance(poly, geometry.Polygon):
        return np.array(poly.exterior.coords.xy).T[:-1, :]

    if poly.is_empty:
        return None
    poly_gen = (np.array(p.exterior.coords.xy).T[:-1, :] for p in poly)
    return reduce(vstack_with_sep, poly_gen)


def scriptcsv(container: Model, rootdir: Path):
    """
    Writes ISA model data to files.

    :param Model container: the ISA model
    :param pathlib.Path rootdir: path where the files will be saved
    """
    idx = pd.Index(list(range(1, container.pilot.Z.shape[0] + 1)), name=output_idx_name)
    algolabels = container.data.algolabels
    nalgos = len(algolabels)
    for i in range(nalgos):
        save_footprint(container.trace.good[i], rootdir, algolabels[i], 'good')
        save_footprint(container.trace.best[i], rootdir, algolabels[i], 'best')

    pd.DataFrame(container.pilot.Z, index=idx, columns=z_cols).to_csv(rootdir / 'coordinates.csv')
    pd.DataFrame(container.pilot.A, index=pd.Index(z_cols, name=output_idx_name),
                 columns=container.data.featlabels).to_csv(rootdir / 'projection_matrix.csv')
    container.trace.summary.to_csv(rootdir / 'footprint_performance.csv')


def save_footprint(footprint: FootprintOutput, rootdir: Path, name: str, suffix='good'):
    """
    Convenient function to save footprint polygons.

    :param trace.FootprintOutput footprint: footprint output object
    :param pathlib.Path rootdir: path where the files will be saved
    :param str name: the algorithm name
    :param str suffix: either 'good', 'best' or 'bad'
    """
    footprint_good = join_polygons(footprint.polygon)
    df_good = pd.DataFrame(footprint_good, columns=z_cols)
    df_good.index.name = output_idx_name
    df_good.to_csv(rootdir / f'footprint_{name}_{suffix}.csv')
