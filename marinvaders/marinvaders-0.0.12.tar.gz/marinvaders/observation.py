"""
Find all observation for species.

The species reported by OBIS are used to search in WoRMS, GISD and NatCon
observations sources and are merged if record was found as a alien means.
"""

import logging

import pandas as pd
import numpy as np

from marinvaders.api_calls import request_worms
from marinvaders.readers import ShapeFiles, read_shapefile, \
    eco_mrgid_link, read_gisd, \
    read_gisd_worms_link, read_natcon


def observations(obis: pd.DataFrame) -> pd.DataFrame:
    """
    The main function, calls all data sources and merge them together.

    Returns
    -------
    pd.DataFrame
    """
    logging.info('Processing observations.')

    worms_obs = worms(obis)
    gisd_obs = gisd(obis)
    natcon_obs = natcon(obis)

    if all([worms_obs.empty, gisd_obs.empty, natcon_obs.empty]):
        return pd.DataFrame()

    result = pd.concat([worms(obis), gisd(obis), natcon(obis)],
                       sort=True).reset_index(drop=True)

    # add ECOCODE column to result
    df_eco_mrgid = eco_mrgid_link()
    result['ECO_CODE'] = \
        result['ECO_CODE_X'].apply(lambda x:
                                   df_eco_mrgid[df_eco_mrgid['ECO_CODE_X']
                                                == x].iloc[0]['ECO_CODE'])

    result.drop_duplicates(subset=['ECO_CODE_X', 'aphiaID',
                                   'establishmentMeans', 'dataset'],
                           inplace=True)

    return result


def worms(obis: pd.DataFrame) -> pd.DataFrame:
    """
    Process WoRMS observations for the specified species.

    Returns
    -------
    pandas.DataFrame
    """
    logging.info('Processing WoRMS')
    df_worms = request_worms(obis['aphiaID'].unique())
    if df_worms.empty:
        return pd.DataFrame

    # The establishmentMeans is invasive if equal to Alien otherwise native

    # df_worms_invasive = df_worms[df_worms['establishmentMeans'] == 'Alien']
    df_worms['MRGID'] = \
        df_worms['locationID'].apply(lambda x: int(x.split('/')[-1]))

    df_worms.drop(['decimalLatitude', 'decimalLongitude', 'higherGeography',
                   'higherGeographyID', 'locality', 'locationID',
                   'qualityStatus', 'recordStatus', 'typeStatus'],
                  axis=1,
                  inplace=True)
    df_worms = pd.merge(df_worms, obis, on=['aphiaID'])
    df_worms.drop_duplicates(inplace=True)

    # link with mrgid using manual xlsx file
    link_df = read_gisd_worms_link()
    link_df.dropna(subset=['MRGID'], inplace=True)
    link_df['MRGID'] = link_df['MRGID'].astype('int64')

    link_df['ECO_CODE_X'] = link_df['ECO_CODE_X'].astype('str')
    df_split = pd.concat([pd.Series(row['MRGID'], row['ECO_CODE_X'].split(','))
                          for _, row in link_df.iterrows()]).reset_index()
    df_split.columns = ['ECO_CODE', 'MRGID']

    df_all = link_df.merge(df_split, on='MRGID')
    df_all.drop(['ECO_CODE_X'], axis=1, inplace=True)

    link_manfile = df_all[(df_all['Source'] == 'WoRMS')
                          & (df_all['Shapefile'] == 0)]
    link_manfile = link_manfile[['MRGID', 'ECO_CODE']]
    link_manfile['MRGID'] = link_manfile['MRGID'].astype(int)

    df_worms_link_man = df_worms.merge(link_manfile, on='MRGID')
    df_worms_link_man.drop('ECO_CODE_x', axis=1, inplace=True)
    df_worms_link_man['ECO_CODE'] = df_worms_link_man['ECO_CODE_y']
    df_worms_link_man.drop('ECO_CODE_y', axis=1, inplace=True)
    df_worms_link_man.replace('nan', np.nan, inplace=True)
    df_worms_link_man['ECO_CODE'].replace('-', np.nan, inplace=True)
    df_worms_link_man.dropna(subset=['ECO_CODE'], inplace=True)
    df_worms_link_man['ECO_CODE'] = \
        df_worms_link_man['ECO_CODE'].astype('int64')

    df_meow = pd.DataFrame(read_shapefile(ShapeFiles.MEOW_ECOS))
    df_meow = df_meow[['ECO_CODE_X', 'ECOREGION', 'geometry']]
    df_meow['ECO_CODE'] = df_meow['ECO_CODE_X']
    df_meow.drop('ECO_CODE_X', axis=1, inplace=True)
    df_meow['ECO_CODE'] = df_meow['ECO_CODE'].astype('int64')
    df_worms_link_man = df_worms_link_man.merge(df_meow, on='ECO_CODE')

    # link with mrgid using other shapefiles
    df_eco_mrgid = eco_mrgid_link()
    df_worms_link_aut = df_worms.merge(df_eco_mrgid, on='MRGID')
    df_worms_link_aut.drop('ECO_CODE_x', axis=1, inplace=True)
    df_worms_link_aut['ECO_CODE'] = \
        df_worms_link_aut['ECO_CODE_y'].apply(lambda x:
                                              df_eco_mrgid[
                                                  df_eco_mrgid['ECO_CODE']
                                                  == x].iloc[0]['ECO_CODE_X'])
    df_worms_link_aut.drop('ECO_CODE_y', axis=1, inplace=True)
    df_worms_link_aut = df_worms_link_aut[
        ['MRGID', 'ECO_CODE', 'ECOREGION', 'geometry', 'establishmentMeans',
         'aphiaID', 'species']]

    df_res = pd.concat([df_worms_link_man, df_worms_link_aut], sort=True)
    df_res.drop_duplicates(subset=df_res.columns.difference(['geometry']),
                           inplace=True)

    df_res['ECO_CODE_X'] = df_res['ECO_CODE']
    df_res.drop('ECO_CODE', axis=1, inplace=True)
    df_res['dataset'] = 'WoRMS'

    return df_res


def gisd(obis: pd.DataFrame) -> pd.DataFrame:
    """
    Process observations from GISD source.

    Returns
    -------
    pandas.DataFrame
    """
    logging.info('Processing GISD')
    try:
        gisd_df = read_gisd()
        gisd_df['species'] = gisd_df['Species']
        # gisd_df.drop(['Species'], axis=1, inplace=True)

        merged = obis.merge(gisd_df, on='species', how='inner')
        xls = read_gisd_worms_link()
        eco_mrgi = eco_mrgid_link()
        eco_mrgi['MarRegion'].fillna('', inplace=True)

        alien = []
        for row in merged.iterrows():
            alien_locations = row[1]['alien_range']
            alien = []
            for alien_loc in alien_locations:
                distr = xls[xls['Distribution'].str.contains(
                    alien_loc['location_name'],
                    case=False)]
                auto_eez_iho = eco_mrgi[pd.notna(eco_mrgi['MarRegion'])
                                        & eco_mrgi['MarRegion'].str.contains(
                    alien_loc['location_name'], case=False)]
                auto_eez = eco_mrgi[pd.notna(eco_mrgi['Territory1'])
                                    & eco_mrgi['Territory1'].str.contains(
                    alien_loc['location_name'], case=False)]
                auto_iho = eco_mrgi[pd.notna(eco_mrgi['NAME'])
                                    & eco_mrgi['NAME'].str.contains(
                    alien_loc['location_name'], case=False)]
                res_tmp = pd.concat([distr, auto_iho, auto_eez, auto_eez_iho],
                                    sort=True)
                res_tmp['location'] = alien_loc['location_name']
                res_tmp['aphiaID'] = row[1]['aphiaID']
                res_tmp['ECO_CODE'] = row[1]['ECO_CODE']
                res_tmp['species'] = row[1]['species']
                alien.append(res_tmp)

        if not alien:
            return pd.DataFrame()
        alien = pd.concat(alien)
        alien['establishmentMeans'] = 'Alien'

        for row in merged.iterrows():
            native_locations = row[1]['native_range']
            native = []
            for native_loc in native_locations:
                distr = xls[xls['Distribution'].str.contains(native_loc,
                                                             case=False)]
                auto_eez_iho = eco_mrgi[pd.notna(eco_mrgi['MarRegion'])
                                        & eco_mrgi['MarRegion'].str.contains(
                    native_loc, case=False)]
                auto_eez = eco_mrgi[pd.notna(eco_mrgi['Territory1'])
                                    & eco_mrgi['Territory1'].str.contains(
                    native_loc, case=False)]
                auto_iho = eco_mrgi[pd.notna(eco_mrgi['NAME'])
                                    & eco_mrgi['NAME'].str.contains(
                    native_loc, case=False)]
                df_tmp = pd.concat([distr, auto_iho, auto_eez, auto_eez_iho],
                                   sort=True)
                df_tmp['location'] = native_loc
                df_tmp['aphiaID'] = row[1]['aphiaID']
                df_tmp['ECO_CODE'] = row[1]['ECO_CODE']
                df_tmp['species'] = row[1]['species']

                native.append(df_tmp)

        native = pd.concat(native)
        native['establishmentMeans'] = None

        result = pd.concat([alien, native])
        result['dataset'] = 'GISD'
        result = result[['aphiaID', 'species', 'establishmentMeans',
                         'MRGID', 'dataset']]
        eco_mrgi = eco_mrgi[['ECOREGION', 'ECO_CODE_X', 'MRGID', 'geometry']]

        result = result.merge(eco_mrgi, on='MRGID', how='inner')

    except Exception as e:
        logging.info('No data found in GISD. Exception: {}'.format(e))
        result = pd.DataFrame()

    return result


def natcon(obis: pd.DataFrame) -> pd.DataFrame:
    """
    Process observations for alien range from NatCon source.

    Returns
    -------
    pandas.DataFrame
    """
    logging.info('Processing NatCon')
    natcon = read_natcon()
    natcon['species'] = natcon['SPECIES_NAME']
    merged = obis.merge(natcon, on='species', how='inner')
    merged = merged[['aphiaID', 'species', 'ECOREGION', 'ECO_CODE_X']]
    merged['establishmentMeans'] = 'Alien'
    merged['dataset'] = 'NatCon'
    map_eco_mrgid = eco_mrgid_link()
    map_eco_mrgid = map_eco_mrgid[['MRGID', 'ECO_CODE_X', 'geometry']]

    result = merged.merge(map_eco_mrgid, on='ECO_CODE_X')

    return result
