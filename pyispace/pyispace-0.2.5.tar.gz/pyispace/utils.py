import numpy as np
import pandas as pd
from functools import reduce
from pathlib import Path
from shapely import geometry
from .train import Model
from .trace import FootprintOutput


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
    z_cols = ['z_1', 'z_2']
    idx = pd.Index(list(range(1, container.pilot.Z.shape[0] + 1)), name='Row')
    algolabels = container.data.algolabels
    nalgos = len(algolabels)
    for i in range(nalgos):
        footprint_good = join_polygons(container.trace.good[i].polygon)
        footprint_best = join_polygons(container.trace.best[i].polygon)
        df_good = pd.DataFrame(footprint_good, columns=z_cols)
        df_best = pd.DataFrame(footprint_best, columns=z_cols)
        df_good.index.name = 'Row'
        df_best.index.name = 'Row'
        df_good.to_csv(rootdir / f'footprint_{algolabels[i]}_good.csv')
        df_best.to_csv(rootdir / f'footprint_{algolabels[i]}_best.csv')

    pd.DataFrame(container.pilot.Z, index=idx, columns=z_cols).to_csv(rootdir / 'coordinates.csv')
    container.trace.summary.to_csv(rootdir / 'footprint_performance.csv')


def save_footprint(footprint: FootprintOutput, rootdir: Path, name: str):
    z_cols = ['z_1', 'z_2']
    footprint_good = join_polygons(footprint.polygon)
    df_good = pd.DataFrame(footprint_good, columns=z_cols)
    df_good.index.name = 'Row'
    df_good.to_csv(rootdir / f'footprint_{name}_good.csv')
