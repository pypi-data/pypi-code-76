from visualife.data import ScoreFile, filter_score_file


# -------------------- General-purpose server side utilities (to be moved to a separate file)
def scorefile_to_json_dictionary(score_file_data, **kwargs):
    """Reads data in scorefile format and returns it as a dictionary

    :param score_file_data: score file data: ScoreFile object, file name to load a score file
        or the actual data as a multiline string / bytes
    :param kwargs: configure what to send, see below

    :Keyword Arguments:
        * *send_rows* (``bool``) --
          if ``True`` (which is the default), data will be stored row-wise; note that setting also ``send_columns=True``
          will send the data both as rows and columns
        * *send_columns* (``bool``) --
          if ``True`` (which is the default), data will be stored column-wise; note that setting also ``send_rows=True``
          will send the data both as rows and columns
        * *relevant_only* (``bool``) --
          if ``True`` (which is the default), irrelevant columns will be removed
        * *selected_columns* (``list[string]``) --
          list of requested column names to be included in the output; all other columns will be discarded

    :return: a json-like dictionary that holds the silent file data
    """
    if not isinstance(score_file_data, ScoreFile):
        sc_file = ScoreFile()
        if len(score_file_data) > 512:
            good_data = score_file_data.decode('ASCII')
            sc_file.read_score_file(good_data)
        else:
            sc_file.read_score_file(score_file_data)
    else:
        sc_file = score_file_data

    # ---------- Filter score file if requested
    filter = kwargs.get('filter', None)
    filter_by = kwargs.get('filter_by', None)
    if filter and filter_by:
        sc_file = filter_score_file(sc_file, filter, filter_by)

    column_names = []
    columns = {}
    rows = []
    output = {"result": "OK"}
    selected_columns = kwargs.get("selected_columns", None)
    # ---------- Extract data as columns and column names
    if_relevant = kwargs.get("relevant_only", True)  # --- keep only the "relevant" columns, i.e. these that contain non-trivial data
    for column_name in sc_file.column_names():
        if selected_columns and column_name in selected_columns:    # --- copy only selected columns, if such a list was given
            column_names.append(column_name)
            columns[column_name] = sc_file.column(column_name)
        else:                                       # --- otherwise copy only relevant columns or just all columns
            if not if_relevant or sc_file.is_relevant_column(column_name):
                column_names.append(column_name)
                columns[column_name] = sc_file.column(column_name)
    if selected_columns:
        output["column_names"] = [col_name for col_name in selected_columns if col_name in column_names]
    else:
        output["column_names"] = column_names

    # ---------- Send data column-wise
    if kwargs.get("send_columns", True):
            output["columns"] = columns

    # ---------- Extract data as rows
    if kwargs.get("send_rows", True):
        for i in range(sc_file.n_rows):
            row = []
            for j in output["column_names"]:
                row.append(sc_file.column(j)[i])
            rows.append(row)
        output["rows"] = rows
    return output
