
from io import StringIO
import csv

def read_file(path):
    result = ""
    with open(path, "r", encoding="utf-8") as fp:
        result = fp.read()
    return result

def json_to_csv(json_data):
    result = ""
    if not isinstance(json_data, list):
        raise ValueError("json data's type must be list.")
    line = StringIO()
    writer = csv.writer(line)

    if len(json_data) > 0:
        csv_rows = []
        csv_rows.append(list(json_data[0].keys()))
        for row in json_data:
            csv_rows.append(row.values())
        writer.writerows(csv_rows)
        result = line.getvalue()

    return result
