import sqlite3
from datetime import datetime
from typing import NoReturn

from MyVault.src.utils import queries


class Database:
    def __init__(self, db_path: str):
        self.__conn = sqlite3.connect(database=db_path)
        self.__cur = self.__conn.cursor()
        self.__create_table()

    def __create_table(self) -> NoReturn:
        self.execute(queries.CREATE_SQLITE_DB)
        self.__commit()

    def insert_secret(self, folder: str, name: str, secret: str) -> NoReturn:
        time_now = self.get_current_datetime()
        self.execute(queries.INSERT_SECRET, (folder, name, secret, time_now, time_now))
        self.__commit()

    @staticmethod
    def get_current_datetime() -> datetime:
        return datetime.now()

    def execute(self, *args) -> NoReturn:
        self.__cur.execute(*args)

    def update_secret(self, folder: str, name: str, new_secret: str) -> NoReturn:
        time_now = self.get_current_datetime()
        self.execute(queries.UPDATE_SECRET, (new_secret, time_now, folder, name))
        self.__commit()

    def select_all(self) -> tuple:
        self.execute(queries.SELECT_ALL)
        for row in self.__cur:
            yield row

    def select_folder_and_names(self) -> tuple:
        self.execute(queries.SELECT_FOLDER_NAME)
        for row in self.__cur:
            yield row

    def select_secret(self, folder: str, name: str) -> str:
        self.execute(queries.SELECT_SECRET, (folder, name))
        selected_row = self.__cur.fetchone()
        return selected_row[0] if isinstance(selected_row, tuple) else None

    def delete_secret(self, folder: str, name: str) -> NoReturn:
        self.execute(queries.DELETE_SECRET, (folder, name))
        self.__commit()

    def execute_many(self, *args) -> NoReturn:
        self.__cur.executemany(*args)
        self.__commit()

    def __commit(self) -> NoReturn:
        self.__conn.commit()

    def close(self) -> NoReturn:
        self.__conn.close()
