import re
import itertools


def flatten_invoice(invoice):
    return_dict = dict()
    entities = invoice["entities"]
    probabilities = invoice.get("probabilities")

    def traverse_items(entities, probabilities, _dict, *prefix):
        for k, v in entities.items():
            if isinstance(v, dict):
                traverse_items(
                    entities[k],
                    probabilities[k] if probabilities else None,
                    return_dict,
                    k,
                )
            elif isinstance(v, list):
                # items, taxes, terms
                if all(isinstance(list_item, dict) for list_item in v):
                    for counter, list_item in enumerate(v):
                        temp_dict = {}
                        for item, value in list_item.items():
                            temp_dict[f"{k}_{item}_{counter}"] = value
                        traverse_items(
                            temp_dict,
                            probabilities[k][counter] if probabilities else None,
                            return_dict,
                        )
                # ibanAll enc
                elif all(isinstance(list_item, str) for list_item in v):
                    if v:
                        _dict[k] = []
                        for _, list_item in enumerate(v):
                            _dict[k].append(list_item)
                        _dict[k] = (", ".join(_dict[k]), None, None)
                    else:
                        _dict[k] = ("", None, None)
                # Undefined datastructure
                else:
                    pass
            else:
                try:
                    # dirty solution, assumes no invoice extractor response field got underscore
                    original_k = k.split("_")[-2]
                except IndexError:
                    original_k = k

                if prefix:
                    field_name = f"{prefix[0]}_{k}"
                else:
                    field_name = k

                if probabilities and original_k in probabilities:
                    if probabilities[original_k]:
                        _dict[field_name] = (
                            v if v else "",
                            probabilities[original_k],
                            None,
                        )
                    else:
                        _dict[field_name] = (v if v else "", None, None)
                else:
                    _dict[field_name] = (v if v else "", None, None)

    traverse_items(entities, probabilities, return_dict)
    return return_dict


def structure_sheets(response: dict, header_sheetname="header"):
    """Structure the extracted invoices in different sheets.

    Arguments:
        response {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    single_cardinality = {header_sheetname: []}
    multi_cardinality = {}

    for idx, document in response.items():
        single_cardinality[header_sheetname].append(
            {
                "file_name": document["file_name"],
                "error_message": document.get("error_message", (None, None, None)),
            }
        )
        multi_items = {}

        for col, value in document.items():
            if col[-1].isdigit():
                item_num = int(col.split("_")[-1])
                label = col.split("_")[1]
                category = col.split("_")[0]
                multi_items.setdefault(category, [])

                if len(multi_items[category]) == item_num:
                    multi_items[category].append(
                        {
                            "file_name": document["file_name"],
                            "row_number": (item_num + 1, None, None),
                        }
                    )

                multi_items[category][item_num][label] = document[col]
            else:
                single_cardinality[header_sheetname][idx][col] = document[col]

        for category, rows in multi_items.items():
            for row in rows:
                multi_cardinality.setdefault(category, []).append(row)

    return {**single_cardinality, **multi_cardinality}


def structure_sheet(records):
    columns = set()

    # Collect all column names
    for record in records:
        columns = columns.union(set(record.keys()))

    for idx, record in enumerate(records.copy()):
        # Insert all missing columns into record
        record.update(
            {k: (None, None, None) for k in columns if k not in record.keys()}
        )

        # All snake_case keys
        record = {
            re.sub(r"(?<!^)(?=[A-Z])", "_", k).lower(): v for k, v in record.items()
        }

        # Reorder column order
        if "error_message" in record or "row_number" in record:
            records[idx] = {
                **dict(itertools.islice(record.items(), 2)),
                **dict(sorted(itertools.islice(record.items(), 2, None))),
            }
        else:
            records[idx] = {
                **dict(itertools.islice(record.items(), 1)),
                **dict(sorted(itertools.islice(record.items(), 1, None))),
            }

    return records
