import pandas as pd


def rg_case(value, arc, units, case):
    return f"{value:3.3}{units} @ {arc:3.3}"


def generate_rg_summary_dataframe(summary_rg_data):
    range_graphs = []
    row_styles = []
    for _, (name, data) in enumerate(summary_rg_data.items()):
        name = data.result_meta.name
        style = {
            "Range Graph": name,
            "Max": None,
            "Min": None,
            "Static Max": None,
            "Static Min": None,
        }
        units = data.result_meta.get("var_details", {"units": ""})["units"]
        max_limit = data.result_meta.limits.max
        min_limit = data.result_meta.limits.min

        max_value = data.max_value
        arc_of_max = data.arc_max_value
        max_case = data.max_case_info.case_guid
        if max_limit is not None:
            if max_value < max_limit:
                style["Max"] = "background: lightgreen"
            elif max_value >= max_limit:
                style["Max"] = "background: lightred"

        max_link = rg_case(max_value, arc_of_max, units, max_case)

        min_value = data.min_value
        arc_of_min = data.arc_min_value
        min_case = data.min_case_info.case_guid
        if min_limit is not None:
            if min_value < min_limit:
                style["Min"] = "background: lightgreen"
            elif min_value >= min_limit:
                style["Min"] = "background: lightred"
        min_link = rg_case(min_value, arc_of_min, units, min_case)

        static_max_value = data.static_max_value
        arc_of_static_max = data.arc_static_max_value
        static_max_case = data.static_max_case_info.case_guid
        static_max_link = rg_case(
            static_max_value, arc_of_static_max, units, static_max_case
        )

        static_min_value = data.static_min_value
        arc_of_static_min = data.arc_static_min_value
        static_min_case = data.static_min_case_info.case_guid
        static_min_link = rg_case(
            static_min_value, arc_of_static_min, units, static_min_case
        )

        range_graphs.append(
            {
                "Range Graph": name,
                "Max": max_link,
                "Min": min_link,
                "Static Max": static_max_link,
                "Static Min": static_min_link,
            }
        )
        row_styles.append(style)

    frame = pd.DataFrame(range_graphs)

    def highlight_exceed(data):
        return pd.DataFrame(row_styles, index=range(len(row_styles)))

    return frame, frame.style.apply(highlight_exceed)
