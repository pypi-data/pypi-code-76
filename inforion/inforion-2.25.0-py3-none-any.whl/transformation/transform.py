# Transformation of Staging Data into M3 format via mapping file
import datetime
import decimal
import logging
from functools import partial
from multiprocessing import Pool

import inforion.transformation.transform_special as ts
import numpy as np
import pandas as pd
from inforion.logger.logger import get_logger
from inforion.transformation.transform_error import TransformationError

logger = get_logger("transform", True)


def parallelize_tranformation(
    mappingfile, mainsheet, stagingdata, outputfile=None, n_cores=4
):

    # Read the file from given location
    xls = pd.ExcelFile(mappingfile)

    # to read all sheets to a map
    sheet_to_df_map = {}
    for sheet_name in xls.sheet_names:
        sheet_to_df_map[sheet_name] = xls.parse(sheet_name)

    # caching main sheet data
    main_cache = getMainSheetCache(sheet_to_df_map, mainsheet)
    # caching tab sheets data
    tabs_cache = getTabsMappingCache(sheet_to_df_map, main_cache)
    # getting a list of tabs containg wildcard characters
    wildcard_tabs = get_wild_card_tabs(tabs_cache)

    # Checking for special cases. e.g. Artikel-Lageort
    if mainsheet in ts.special_sheets:
        stagingdata = ts.handle_special_pre_transformations(
            sheet_to_df_map, mainsheet, stagingdata
        )

    # Transforming data in parallel
    if n_cores == 1:
        df = transform_data(
            sheet_to_df_map,
            mainsheet,
            main_cache,
            tabs_cache,
            wildcard_tabs,
            stagingdata,
        )
    else:
        df_split = np.array_split(stagingdata, n_cores)
        func = partial(
            transform_data,
            sheet_to_df_map,
            mainsheet,
            main_cache,
            tabs_cache,
            wildcard_tabs,
        )
        pool = Pool(n_cores)
        df = pd.concat(pool.map(func, df_split))
        pool.close()
        pool.join()

    logger.debug("Transformed data farme:")
    logger.debug(df)

    # Saving output file
    if outputfile is not None:
        logging.info("Save to file: " + outputfile)
        writer = pd.ExcelWriter(outputfile, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Log Output", index=False)
        writer.save()
    return df


def getMainSheetCache(sheet_to_df_map, mainsheet):
    mapping_cache = []

    for index, row in sheet_to_df_map[mainsheet].iterrows():
        if index >= 9:
            row = row.replace(np.nan, "", regex=True)

            map = {}
            map["API_FIELD"] = row[15]

            if row[33] and not row[33] is np.nan:
                map["SOURCE"] = row[33]
            else:
                map["SOURCE"] = None

            map["FUNC_TYPE"] = row[36].strip().lower()

            map["FUNC_VAL"] = row[37]
            map["FUNC_ARG"] = row[38]

            mapping_cache.append(map)

    return mapping_cache


def getTabsMappingCache(sheet_to_df_map, mapping_cache):
    mapping_sheets_cache = {}

    for map in mapping_cache:
        if map["FUNC_TYPE"] == "tbl":
            index_val_col = 1  # index for the value column
            key_cols_count = 0  # no of key columns

            tab_key = map["FUNC_VAL"].strip()  # tab name for excel tab sheet
            tab_sub_keys = map["FUNC_ARG"].split("|")  # tab key columns information

            tab = {}  # tab containing all dictonaries for single excel tab sheet
            field_dict = {}  # dictionary for a single field

            for sub_val in tab_sub_keys:
                if "#:" in sub_val:
                    index_val_col = int(sub_val[2:])
                else:
                    key_cols_count = key_cols_count + 1

            index_val_col = key_cols_count + index_val_col - 1
            if tab_key in sheet_to_df_map:
                for i, val in sheet_to_df_map[tab_key].iterrows():
                    multi_val_key = ""
                    if i >= 7:
                        if str(val[0]) == "nan":
                            val[0] = ""
                        if key_cols_count > 1:
                            for index, sub_val in enumerate(tab_sub_keys):
                                if "#:" not in sub_val:
                                    if multi_val_key == "":
                                        multi_val_key = str(val[index])
                                    else:
                                        multi_val_key = (
                                            multi_val_key + "_" + str(val[index])
                                        )
                            field_dict[multi_val_key] = str(val[index_val_col])
                        else:
                            field_dict[str(val[0])] = str(val[int(index_val_col)])
                tab[str(map["API_FIELD"])] = field_dict
                if tab_key not in mapping_sheets_cache:
                    mapping_sheets_cache[tab_key] = tab
                else:
                    mapping_sheets_cache[tab_key].update(tab)
            else:
                raise TransformationError(
                    "Tab '{}' mentioned in mapping sheet is not found.".format(tab_key)
                )

    return mapping_sheets_cache


def transform_data(
    _sheet_to_df_map, _mainsheet, sheet_cache, tabs_cache, wildcard_tabs, stagingdata
):
    rows_list = []

    for _, tb_row in stagingdata.iterrows():
        row_dict = {}
        for map in sheet_cache:
            if map["SOURCE"]:
                transform_source_column(
                    row_dict, map["API_FIELD"], tb_row, map["SOURCE"], map["FUNC_TYPE"], map["FUNC_VAL"]
                )
            else:
                if map["FUNC_TYPE"] == "tbl":
                    tab = tabs_cache[map["FUNC_VAL"].strip()]
                    transform_sheet_table_mapping_column(
                        row_dict,
                        map["API_FIELD"],
                        tb_row,
                        tab,
                        map["FUNC_ARG"],
                        wildcard_tabs,
                    )
                elif map["FUNC_TYPE"] == "func":
                    transform_function_column(
                        row_dict,
                        map["API_FIELD"],
                        tb_row,
                        map["FUNC_VAL"],
                        map["FUNC_ARG"],
                    )
                elif map["FUNC_TYPE"] == "const":
                    transform_const_column(
                        row_dict, map["API_FIELD"], tb_row, map["FUNC_VAL"]
                    )

        rows_list.append(row_dict)

    df = pd.DataFrame(rows_list).replace("nan", "", regex=True)

    return df


def transform_source_column(map_row, map_col, tb_row, source_col, func_type, func_value):
    """Reads the value from source table against source col, and maps it to map_col in map_row"""
    source = clean(source_col)
    if source in tb_row:
        if func_type == "truncate":
            txt = str(tb_row[source])
            func_value = int(func_value)
            map_row[map_col] = txt[:func_value]
        else:
            map_row[map_col] = str(tb_row[source])
    else:
        raise TransformationError(
            "Field '{}' mentioned in mapping sheet is not found.".format(source)
        )


def transform_sheet_table_mapping_column(
    map_row, map_col, tb_row, tab_sheet, tab_sheet_key, wildcard_tabs
):
    if tab_sheet_key and not tab_sheet_key is np.nan:
        db_key = ""  # actual key against which we lookup in sheet_tab

        # converting sheet_tab_key to db_key.
        sub_keys = tab_sheet_key.split("|")
        for sub_key in sub_keys:
            if "#:" not in sub_key:
                sub_key = clean(sub_key)
                if sub_key in tb_row:
                    if db_key == "":
                        db_key = str(tb_row[sub_key])
                    else:
                        db_key = db_key + "_" + str(tb_row[sub_key])
                else:
                    raise TransformationError(
                        "Field '{}' mentioned in mapping sheet is not found.".format(
                            sub_key
                        )
                    )

        if db_key in tab_sheet[map_col]:
            # assigning the values if key simply matches
            map_row[map_col] = str(tab_sheet[map_col][db_key])
        elif map_col in wildcard_tabs and wildcardcomparison_has_key(
            tab_sheet[map_col], db_key
        ):
            # checking if key matches with any wildcard entry in tab_sheet
            map_row[map_col] = wildcardcomparison_get_value(tab_sheet[map_col], db_key)
        elif "*" in tab_sheet[map_col]:
            # checking tab_sheet has '*' key, then we assign that values
            map_row[map_col] = str(tab_sheet[map_col]["*"])
        else:
            # if nothing matches, return the new converted key
            map_row[map_col] = str(db_key)


def transform_function_column(map_row, map_col, tb_row, func_name, func_args):
    """Reads the value from source table against source col, and maps it to map_col in map_row"""
    if func_name.strip().lower() == "div":
        data_values = func_args.split("|")
        with decimal.localcontext() as ctx:
            result = decimal.Decimal(tb_row[clean(data_values[0])]) / decimal.Decimal(
                clean(data_values[1])
            )
            if data_values[2] != "":
                result = round(result, int(data_values[2]))

    map_row[map_col] = result


def transform_const_column(map_row, map_col, tb_row, func_val):
    if isinstance(func_val, datetime.datetime):
        val = func_val.strftime("%Y%m%d")
        map_row[map_col] = str(val)
    else:
        map_row[map_col] = str(func_val)


def get_wild_card_tabs(tabs_cache):
    wildcard_tabs = []
    for key, tab_dict in tabs_cache.items():
        for key2, tab_dict2 in tab_dict.items():
            keys = list(
                filter(lambda x: len(x) > 1 and x.endswith("*"), tab_dict2.keys())
            )
            if len(keys) > 0:
                wildcard_tabs.append(key)
                break
    return wildcard_tabs


def wildcardcomparison_has_key(tab_dict, db_key):
    keys = list(filter(lambda x: len(x) > 1 and x.endswith("*"), tab_dict.keys()))
    for key in keys:
        skey = key[:-1]
        sdb_key = db_key[: len(skey)]
        if skey == sdb_key:
            return True
    return False


def wildcardcomparison_get_value(tab_dict, db_key):
    keys = list(filter(lambda x: len(x) > 1 and x.endswith("*"), tab_dict.keys()))
    for key in keys:
        skey = key[:-1]
        sdb_key = db_key[: len(skey)]
        if skey == sdb_key:
            return tab_dict[key]
    return db_key


def clean(string):
    str = string
    if str.startswith("["):
        str = str[1:]

    if str.endswith("]"):
        str = str[:-1]
    return str
