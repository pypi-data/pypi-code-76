import pandas as pd


def calculate_improvements(comparison_1: object, comparison_2: object) -> pd.DataFrame:
    def _rename_columns_for_evaluation():
        """
        This function is used internally for editing names from somename_y_model_2  to somename_model_2
        as well as replacing somename_x to somename_ground_truth
        """

        evaluation.columns = [
            column.replace("_y_", "_") for column in evaluation.columns
        ]
        evaluation.columns = [
            column.replace(column[-2:], "_ground_truth")
            if column[-2:] in ["_x"]
            else column
            for column in evaluation.columns
        ]

    def _calculate_improvements():
        """ Takes two diff_ columns and calculates difference between them """
        for column in evaluation.columns:
            if column.lower().startswith("diff_"):
                category = column.lower().split("diff_")[1]
                if category.find("_model_1") > -1:
                    contr_category = category[:-2] + "_2"
                    evaluation["improvement_" + contr_category] = (
                        evaluation["diff_" + category]
                        - evaluation["diff_" + contr_category]
                    )

    def _set_total_calulations(df):
        total = evaluation.sum(numeric_only=True)
        total.name = "Total"

        # Assign sum of all rows of DataFrame as a new Row
        df = df.append(total.transpose())
        count = evaluation.count(numeric_only=True)

        # Assign improvement in percentege as a new Row
        total_percent = total / count
        total_percent.name = "Total percent"
        df = df.append(total_percent.transpose())

        df = df.fillna("")
        return df

    def _sort_columns():
        """Use this function to sort columns with order: name, diff_name_model_1, diff_name_model_2,
        improvement_name_model_2"""
        arr = ["file_name", "distance"]
        for col in evaluation.columns:

            if "_ground_truth" in col:
                arr.append(col)
                arr.append(col.replace("_ground_truth", "_model_1"))
                arr.append(col.replace("_ground_truth", "_model_2"))
                arr.append("diff_" + col.replace("_ground_truth", "_model_1"))
                arr.append("diff_" + col.replace("_ground_truth", "_model_2"))
                arr.append("improvement_" + col.replace("_ground_truth", "_model_2"))

        return arr

    # This columns should be excluded from comparison

    exclude = [
        "Total difference",
        "Total difference in percent",
        "Number of documents",
        "Number of compared columns",
        "Compared data points",
        "Overall difference in percent",
        "Overall accuracy in percent",
    ]

    def _get_header_df(df) -> pd.DataFrame:
        header_df = [elem for elem in df.values()][0]
        return header_df

    df_1_header = _get_header_df(comparison_1)[
        ~_get_header_df(comparison_1).file_name.isin(exclude)
    ]
    df_2_header = _get_header_df(comparison_2)[
        ~_get_header_df(comparison_2).file_name.isin(exclude)
    ]

    # In a second dataframe we are only interested to the columns which are not the ground truth

    specific_columns = [
        column
        for column in df_2_header.columns
        if column in ["file_name"] or column[-2:] in ["_y"] or column[:5] == "diff_"
    ]
    df_2_header_selected_columns = _get_header_df(comparison_2)[specific_columns]

    # Here we are merging two dataframes based on "file_name"
    evaluation = df_1_header.merge(
        df_2_header_selected_columns,
        how="left",
        on="file_name",
        suffixes=["_model_1", "_model_2"],
    )

    _rename_columns_for_evaluation()
    _calculate_improvements()
    evaluation = _set_total_calulations(evaluation)
    evaluation = pd.DataFrame(evaluation, columns=_sort_columns())

    return evaluation
