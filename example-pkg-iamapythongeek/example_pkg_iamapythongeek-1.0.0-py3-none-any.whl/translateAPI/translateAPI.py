import mysql.connector
import requests
import psycopg2


def mysql(url, username, password, table, database, key):
    """
            This method is for translating MySQL databases
            :param url: Connection url to database
            :param username: Your username for the database
            :param password: Your password for the database
            :param table: The table you want to translate
            :param database: The database that has the table you want to translate
            :param key: Your API key from RapidAPI
            :return: Returns query that you can insert into MySQL table
            """
    db = mysql.connector.connect(
        host=url,
        user=username,
        password=password,
        database=database
    )
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    columns_cursor = cursor.fetchall()
    columns = []
    for column in columns_cursor:
        columns.append(column[0])
    cursor.execute(f"SELECT * FROM {table}")
    result = cursor.fetchall()
    translated_final = {}
    for x in result:
        column_id = 0
        for y in x:
            translated_final.update({columns[column_id]: y})
            column_id += 1
    # print(translated_final)
    url = 'https://translation37.p.rapidapi.com/json'
    data = {'text': translated_final}
    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': key,
        'x-rapidapi-host': "translation37.p.rapidapi.com"
    }
    x = requests.post(url, data=data, headers=headers)

    # print(x.content)

    columns_sql = ()
    data_sql = ()

    for c in range(x.content):
        columns_sql.append(x.content.keys()[c])

    for k in range(x.content):
        data_sql.append(x.content.values()[k])

    to_return = f"INSERT INTO {table} ({list(columns_sql)}) VALUES ({data_sql})"
    return to_return


def postgres(url, username, password, table, database, key):
    """
                This method is for translating MySQL databases
                :param url: Connection url to database
                :param username: Your username for the database
                :param password: Your password for the database
                :param table: The table you want to translate
                :param database: The database that has the table you want to translate
                :param key: Your API key from RapidAPI
                :return: Returns query that you can insert into Postgres table
                """

    db = psycopg2.connect(
        host=url,
        database=database,
        user=username,
        password=password)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    columns_cursor = cursor.fetchall()
    columns = []
    for column in columns_cursor:
        columns.append(column[0])
    cursor.execute(f"SELECT * FROM {table}")
    result = cursor.fetchall()
    translated_final = {}
    for x in result:
        column_id = 0
        for y in x:
            translated_final.update({columns[column_id]: y})
            column_id += 1
    # print(translated_final)
    url = 'https://translation37.p.rapidapi.com//json'
    data = {'text': translated_final}
    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': key,
        'x-rapidapi-host': "translation37.p.rapidapi.com"
    }
    x = requests.post(url, data=data, headers=headers)

    # print(x.content)

    columns_sql = ()
    data_sql = ()

    for c in range(x.content):
        columns_sql.append(x.content.keys()[c])

    for k in range(x.content):
        data_sql.append(x.content.values()[k])

    to_return = f"INSERT INTO {table} ({list(columns_sql)}) VALUES ({data_sql})"
    return to_return


def json_request(doc_to_send, key):
    """
                    This method is for translating MySQL databases
                    :param key: Your API key
                    :param doc_to_send: The JSON document for translation
                    :return: Translated document
                    """
    url = "https://translation37.p.rapidapi.com/json/"

    payload = doc_to_send
    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': key,
        'x-rapidapi-host': "translation37.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    # print(response.text)
    return response.text


def text_request(text, key):
    """:param key: Your API key
       :param text: The text to be translated
       :return: Translated text
    """
    url = "https://translation37.p.rapidapi.com/text/"

    payload = {"text": text}
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': key,
        'x-rapidapi-host': "translation37.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text


def image_request(image, key):
    """:param key: Your API key
           :param image: Path to the image that will be translated
           :return: Translated text from image
        """
    url = "https://translation37.p.rapidapi.com/image/"

    payload = {"lang": "LANG IN IMAGE"}
    headers = {
        'content-type': "multipart/form-data; boundary=---011000010111000001101001",
        'x-rapidapi-key': key,
        'x-rapidapi-host': "translation37.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, files={'file': open(image, 'r')}, headers=headers)

    # print(response.text)
    return response.text
