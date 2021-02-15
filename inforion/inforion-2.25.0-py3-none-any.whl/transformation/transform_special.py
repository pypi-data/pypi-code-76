from inforion.logger.logger import get_logger
from inforion.transformation.transform_error import TransformationError


logger = get_logger("transform-special", True)

special_sheets = ["Artikel-Lagerort"]


def handle_special_pre_transformations(sheet_to_df_map, mainsheet, data):
    """This functions handles all specical transformation scenarios."""
    if (
        mainsheet == "Artikel-Lagerort"
        and "SUWH" in sheet_to_df_map
        and "ITTY" in sheet_to_df_map
    ):
        try:
            logger.info(f"Doing special tranformation for {mainsheet}")
            suwh_df = get_suwh_dataframe(sheet_to_df_map)

            if not 'ItemType' in data:
                raise TransformationError(
                    f"Error doing special transformation for {mainsheet}. Column 'ItemType' is missing from main mapping sheet."
                )

            mergedframe = data.merge(suwh_df, on="ItemType", how="inner")
        except TransformationError as tex:
            raise tex
        except Exception as ex:
            logger.exception(ex)
            raise Exception(
                "Error doing special transformation for {0}.".format(mainsheet)
            )
        return mergedframe


def get_suwh_dataframe(sheet_to_df_map):

    df_itty = get_dataframe_from_sheet(sheet_to_df_map, "ITTY", 4, 8)
    df_itty = rename_columns(df_itty, ["ItemType", "M3ITTY", "M3SALE", "M3SPUC"])

    logger.debug("Data Frame ITTY")
    logger.debug(df_itty)

    df_suwh = get_dataframe_from_sheet(sheet_to_df_map, "SUWH", 5, 8)
    df_suwh = rename_columns(
        df_suwh, ["M3ITTY", "M3WHLO", "M3SUWH", "M3PUIT", "M3ORTY"]
    )

    logger.debug("Data Frame SUWH")
    logger.debug(df_suwh)

    df_merged = df_itty.merge(df_suwh, on="M3ITTY")

    logger.debug("Data Frame SUWH and ITTY merged")
    logger.debug(df_merged)

    return df_merged


def get_dataframe_from_sheet(sheet_to_df_map, sheet_name, column_count=-1, row_skip=0):
    df = sheet_to_df_map[sheet_name][row_skip:]
    if column_count > 1:
        df = df.drop(df.columns[column_count:], axis=1)
    return df


def rename_columns(df, column_names):
    cloumns1 = {}
    for index, col in enumerate(column_names):
        cloumns1[df.columns[index]] = col
    df.rename(columns=cloumns1, inplace=True)
    return df
