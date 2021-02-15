import logging
import os.path
import sys

import pandas as pd
import pyodbc
import validators

import inforion.ionapi.model.inforlogin as inforlogin
from inforion.helper.urlsplit import spliturl
from inforion.helper.util import get_db_credentials
from inforion.helper.validations import validate_db_credentials
from inforion.ionapi.controller import *
from inforion.ionapi.model import *
from inforion.merging.merging import merge_files
from inforion.transformation.transform import parallelize_tranformation

from inforion.logger.logger import get_logger

logger = get_logger("inforion-init", True)

# Codee Junaid

def main_load(
    url=None,
    ionfile=None,
    program=None,
    method=None,
    dataframe=None,
    outputfile=None,
    start=None,
    end=None,
    on_progress=None,
):

    if validators.url(url) != True:
        logging.info("Error: URL is not valid")
        return "Error: URL is not valid"

    if os.path.exists(ionfile) == False:
        logging.info("Error: File does not exist")
        return "Error: File does not exist"
    else:
        inforlogin.load_config(ionfile)

    result = spliturl(url)

    if "Call" in result:
        if len(result["Call"]) > 0:
            if result["Call"] == "execute":
                inforlogin.load_config(ionfile)
                token = inforlogin.login()

                headers = inforlogin.header()
                if "Bearer" not in headers["Authorization"]:
                    return "Error: InforION Login is not working"
                if start is None or end is None:
                    return execute(
                        url,
                        headers,
                        program,
                        method,
                        dataframe,
                        outputfile,
                        on_progress,
                    )

                else:
                    return execute(
                        url,
                        headers,
                        program,
                        method,
                        dataframe,
                        outputfile,
                        start,
                        end,
                        on_progress,
                    )

            if result["Call"] == "executeSnd":

                config = inforlogin.load_config(ionfile)
                token = inforlogin.login()

                headers = inforlogin.header()
                if "Bearer" not in headers["Authorization"]:
                    return "InforION Login is not working"
                return executeSnd(
                    url, headers, program, method, dataframe, outputfile, start, end
                )

    if method == "checklogin":
        token = inforlogin.login()
        headers = inforlogin.header()
        return headers["Authorization"]


def main_transformation(
    mappingfile=None, mainsheet=None, stagingdata=None, outputfile=None
):

    if mappingfile is None:
        return "Error: Mapping file path missing"

    if os.path.exists(mappingfile) == False:
        return "Error: Mapping file does not exist"

    if mainsheet is None:
        return "Error: Main sheet name is empty"

    if stagingdata.empty:
        return "Error: Data frame is empty"

    try:
        return parallelize_tranformation(
            mappingfile, mainsheet, stagingdata, outputfile
        )
    except Exception as ex:
        logger.exception(ex)
        if hasattr(ex, "message"):
            return "There is an error while transforming the records. " + ex.message
        else:
            return "There is an unknown error while transforming the records. "
        sys.exit(1)

def main_transformation_from_db(
    mappingfile=None, mainsheet=None, db_config=None, table_name=None, outputfile=None
):

    if mappingfile is None:
        return "Error: Mapping file path missing"

    if os.path.exists(mappingfile) == False:
        return "Error: Mapping file does not exist"

    if os.path.exists(db_config) == False:
        return "Error: DB Configurations does not exist."
    else:
        is_valid, code, message = validate_db_credentials(db_config)
        if not is_valid:
            return message

    if table_name is None:
        return "Error: Table name is missing."

    db_cred = get_db_credentials(db_config)
    conn_string = (
        "DRIVER={"
        + db_cred["driver"]
        + "};"
        + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(
            db_cred["servername"],
            db_cred["database"],
            db_cred["username"],
            db_cred["password"],
        )
    )
    sql_conn = pyodbc.connect(conn_string)

    query = "SELECT * FROM {0}".format(table_name)
    data = pd.read_sql(query, sql_conn)

    try:
        return parallelize_tranformation(mappingfile, mainsheet, data, outputfile)
    except Exception as ex:
        logger.exception(ex)
        if hasattr(ex, "message"):
            return "There is an error while transforming the records. " + ex.message
        else:
            return "There is an unknown error while transforming the records. "
        sys.exit(1)


def main_merge(
    mergesheet1=None,
    mergesheet2=None,
    mergeoutput=None,
    mergecol=None,
    mergetype="outer",
):

    if mergecol is None:
        return "Error: Merging column criteria not defined"

    if mergesheet1.empty:
        return "Error: First merge sheet frame is empty"

    if mergesheet2.empty:
        return "Error: Second merge sheet frame is empty"

    return merge_files(mergesheet1, mergesheet2, mergeoutput, mergecol, mergetype)
