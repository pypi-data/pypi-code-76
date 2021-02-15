import json
import os
import sys

import inforion.excelexport as ex
import inforion.helper.sqllite as sql

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

dir_path = os.path.join(dir_path, "../")

table_name = r"M3PorgramsFields"
database = os.path.join(dir_path, "m3_fields_info.db")

if getattr(sys, '_MEIPASS', False):
    bundle_dir = getattr(sys, '_MEIPASS')
    database = os.path.abspath(os.path.join(bundle_dir, "m3_fields_info.db"))


def __create_and_clean_table__(conn):
    sql_create_table = r"""CREATE TABLE IF NOT EXISTS {}(
                                        id integer PRIMARY KEY,
                                        program TEXT NOT NULL,
                                        method TEXT NOT NULL,
                                        field_name TEXT NOT NULL,
                                        description TEXT,
                                        type TEXT NOT NULL,
                                        required BOOLEAN,
                                        length INTEGER
                                    );""".format(
        table_name
    )

    sql.create_table(conn, sql_create_table)
    sql.truncate_table(conn, table_name)


def __insert_field__(conn, param):
    query = "INSERT INTO {0}(program, method, field_name, description, type,required,length ) VALUES('{1}','{2}','{3}','{4}','{5}',{6},'{7}')".format(
        table_name,
        param["program"],
        param["method"],
        param["name"],
        sql.escape_field(param["description"]),
        param["type"],
        param["required"],
        param["length"],
    )

    sql.execute_query(conn, query, 0)


def __insert_fields__(conn, fields):
    for field in fields:
        __insert_field__(conn, field)
    conn.commit()


def __get_fields_list_from_api_files__(api_file_dir):
    fields_list = []
    files = os.listdir(api_file_dir)
    for filename in files:
        if filename.endswith(".json"):
            file_path = os.path.join(api_file_dir, filename)
            with open(file_path) as json_file:
                data = json.load(json_file)
                program = data["info"]["title"].split()[0]
                prog_fields_list = __get_program_fields_list__(program, data)
                fields_list = fields_list + prog_fields_list
    return fields_list


def __get_program_fields_list__(program, data):
    parameters_list = []
    for (k, v) in data["paths"].items():
        key = k.replace("/", "")
        if key.startswith("Add") or key.startswith("Chg") or key.startswith("Crt"):
            for jparam in v["get"]["parameters"]:
                org_description = jparam["description"]
                ind = org_description.rfind("(")

                jparam["program"] = program
                jparam["method"] = key
                if ind >= 0:
                    jparam["description"] = org_description[0:ind]
                    jparam["length"] = org_description[ind + 1 : -1]
                else:
                    jparam["description"] = org_description
                    jparam["length"] = ""

                parameters_list.append(jparam)
    return parameters_list


def create_update_api_fields_db(api_file_dir):

    if not os.path.isdir(api_file_dir):
        print("Invalid api files directory.")
        return

    fields = __get_fields_list_from_api_files__(api_file_dir)
    print("Extracted all api fields. Exporting fields now...")

    conn = sql.create_connection(database)
    # create tables
    if conn is not None:
        __create_and_clean_table__(conn)

        __insert_fields__(conn, fields)
        print("All fields exported to db successfully.")
    else:
        print("Error! cannot create the database connection.")


def get_numeric_fields_list_from_db(program):

    if not os.path.isfile(database):
        raise Exception("API Fields DB not found.")

    query = "Select field_name from {0} Where type like 'number' and program like '{1}'".format(
        table_name, program
    )
    conn = sql.create_connection(database)
    if conn is not None:
        field_rows = sql.execute_query_for_results(conn, query)
        fields = [field[0] for field in field_rows]
        return fields
    else:
        raise Exception("Error creating connection to database.")


def get_fields_list_from_db(program):

    if not os.path.isfile(database):
        raise Exception("API Fields DB not found.")

    query = "Select program, method, field_name, description, type, required, length from {0} Where program like '{1}' \
    order by method, field_name".format(
        table_name, program
    )
    conn = sql.create_connection(database)
    if conn is not None:
        fields = sql.execute_query_for_results(conn, query)
        return fields
    else:
        raise Exception("Error creating connection to database.")


def get_program_name_from_db():

    if not os.path.isfile(database):
        raise Exception("API Fields DB not found.")

    query = "Select distinct(program) from {0}".format(table_name)
    conn = sql.create_connection(database)
    if conn is not None:
        field_rows = sql.execute_query_for_results(conn, query)
        fields = [field[0] for field in field_rows]
        return fields
    else:
        raise Exception("Error creating connection to database.")


if __name__ == "__main__":
    create_update_api_fields_db(ex.getAPIFileDir())
    # get_numeric_fields_list_from_db('CRS610MI')

    # print(get_program_name_from_db())
