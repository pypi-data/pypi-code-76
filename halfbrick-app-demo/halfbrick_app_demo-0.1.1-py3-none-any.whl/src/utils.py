import csv
import json
import os

def lower(s):
    if type(s) is str:
        return s.lower()
    return s

def csv_to_json(csvFilePath, jsonFilePath):
    data = dict()
    idx = 1
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 
        for row in csvReader: 
            data[idx] = row
            idx += 1
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonf.write(json.dumps(data, indent=4)) 

def sql_input_statement(csvFilePath, tableName, outputFilePath, one_statement=True, max_sql_size=31000):
    if not one_statement:
        out = open(outputFilePath, 'a', encoding='utf-8')
        csvReader = csv.DictReader(open(csvFilePath, encoding='utf-8'))
        row_count = 0
        for row in csvReader: 
            row_count += 1
        csvReader = csv.DictReader(open(csvFilePath, encoding='utf-8'))
        while row_count > 0:
            original_size = os.path.getsize(outputFilePath)
            sql_insert = "INSERT INTO " + tableName
            for row in csvReader: 
                row_count -= 1
                cols = " (" 
                data = " ('"
                for k, v in row.items():
                    cols = cols + k + ", "
                    if k == "timestamp_raw" or k == "table_date":
                        data = data + v[:-4] + "', '"
                    else:
                        data = data + v.replace("'","''") + "', '"
                sql_insert = sql_insert + cols[:-2] + ") " + "\nVALUES" + data[:-3] + "),"
                out.write(sql_insert) 
                break
            for row in csvReader: 
                sql_insert = ""
                row_count -= 1
                data = " ('"
                for k, v in row.items():
                    if k == "timestamp_raw" or k == "table_date":
                        data = data + v[:-4] + "', '"
                    else:
                        data = data + v.replace("'","''") + "', '"
                    sql_insert = sql_insert + data[:-3] + "),"
                    out.write(sql_insert) 
                # SQL statements have a maximum length.
                if (os.path.getsize(outputFilePath)-original_size) > max_sql_size:
                    out.close()
                    with open(outputFilePath, 'rb+') as out: 
                        out.seek(-1, os.SEEK_END)
                        out.truncate()
                    out = open(outputFilePath, 'a', encoding='utf-8')
                    out.write(';\n\n')
                    break
    else:
        out = open(outputFilePath, 'a', encoding='utf-8')
        with open(csvFilePath, encoding='utf-8') as csvf: 
            csvReader = csv.DictReader(csvf)
            sql_insert = "INSERT INTO " + tableName
            for row in csvReader:
                cols = " (" 
                data = " ('"
                for k, v in row.items():
                    cols = cols + k + ", "
                    if k == "timestamp_raw" or k == "table_date":
                        data = data + v[:-4] + "', '"
                    else:
                        data = data + v.replace("'","''") + "', '"
                sql_insert = sql_insert + cols[:-2] + ") " + "\nVALUES" + data[:-3] + "),"
                out.write(sql_insert) 
                break
            for row in csvReader: 
                sql_insert = ""
                data = " ('"
                for k, v in row.items():
                    if k == "timestamp_raw" or k == "table_date":
                        data = data + v[:-4] + "', '"
                    else:
                        data = data + v.replace("'","''") + "', '"
                    sql_insert = sql_insert + data[:-3] + "),"
                out.write(sql_insert) 
            out.close()
            with open(outputFilePath, 'rb+') as out: 
                out.seek(-1, os.SEEK_END)
                out.truncate()
            out = open(outputFilePath, 'a', encoding='utf-8')
            out.write(';')

