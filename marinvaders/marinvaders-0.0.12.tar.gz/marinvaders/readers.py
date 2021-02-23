"""
Read different data sources and combine them.

Data sources are specified at README.md
"""


import os
from enum import Enum
from functools import lru_cache

import pandas as pd
import geopandas as gpd


def data_path() -> os.path:
    """
    Path to data source files.

    Returns
    -------
    os path
    """
    this_dir, _ = os.path.split(__file__)
    return os.path.join(this_dir, "data")


class ShapeFiles(Enum):
    """
    Enum of shape files directory.
    """
    MEOW_ECOS: os.path = os.path.join('meow_ecos', 'meow_ecos.shp')
    EEZ: os.path = os.path.join('eez_low_res', 'eez_lr.shp')
    EEZ_IHO_UNION: os.path = \
        os.path.join('EEZ_IHO_union_v2', 'EEZ_IHO_union_v2.shp')
    IHO_SEA_AREAS: os.path = \
        os.path.join('IHO Sea Areas', 'World_Seas_IHO_v3.shp')


@lru_cache(None)
def read_shapefile(shape_name: ShapeFiles) -> gpd.GeoDataFrame:
    """
    Read shapefiles.

    Parameters
    ----------
    shape_name
        name of the shapefile defined in ShapeFile class

    Returns
    -------
    GeoPandas
    """
    gdf = gpd.read_file(os.path.join(data_path(), shape_name.value))

    if shape_name == ShapeFiles.MEOW_ECOS:
        for colname in ['ECO_CODE', 'PROV_CODE', 'RLM_CODE',
                        'ALT_CODE', 'ECO_CODE_X']:
            gdf[colname] = gdf[colname].astype('int')
    else:
        gdf['MRGID'] = gdf['MRGID'].astype('int')

    return gdf


@lru_cache(None)
def read_gisd_worms_link() -> pd.DataFrame:
    """
    Reads GISD and WoRMS qualitative distribution linked to MEOW.

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_excel(os.path.join(data_path(),
                                    'GISD_and_WoRMS_qualitative_distributions_'
                                    'linked_to_MEOWs.xlsx'),
                       skiprows=5, engine='openpyxl')
    df['ECO_CODE_X'] = df['ECO_CODE_X'].str.replace('.', ',')

    return df


@lru_cache(None)
def read_natcon() -> pd.DataFrame:
    """
    Reads NatCon dataset.

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_excel(os.path.join(data_path(), 'natcon.xlsx'),
                       sheet_name='Species_distribution',
                       engine='openpyxl')

    return df


@lru_cache(None)
def read_gisd() -> pd.DataFrame:
    """
    Reads GISD dataset.

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_json(os.path.join(data_path(), 'gisd.json'))

    return df


@lru_cache(None)
def eco_mrgid_link() -> pd.DataFrame:
    """
    Reads ECO regions code from MEOW merged with other shapefiles.
    This file maps ECO regions code wit MRGID

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_hdf(os.path.join(data_path(), 'eco_mrgid.h5'))
    df['MRGID'] = df['MRGID'].astype('int64')

    return df


@lru_cache(None)
def read_taxonomy() -> pd.DataFrame:
    """
    Reads taxonomy data which describes species affected by invasive species.

    Returns
    -------
    Pandas DataFrame
    """
    df = pd.read_csv(os.path.join(data_path(), 'taxonomy.csv'))
    df = df[['scientificName']]
    df['species'] = df['scientificName']
    df.drop(['scientificName'], axis=1, inplace=True)
    return df
