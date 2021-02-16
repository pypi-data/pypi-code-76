import sqlite3


class Store(object):
    def __init__(self, path) -> None:
        self.conn = sqlite3.connect(path)

    def get_table(self, name: str) -> "Table":
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS {} (key TEXT PRIMARY KEY, value TEXT)".format(
                name
            )
        )
        self.conn.commit()
        return Table(self.conn, name)

    def close(self):
        self.conn.close()

    def remove_table(self, name: str):
        self.conn.execute("DROP TABLE IF EXISTS {};".format(name))


class Table(object):
    def __init__(self, conn: sqlite3.Connection, name: str) -> None:
        self.conn = conn
        self.name = name

    def set(self, key: str, value: str):
        if value == None:
            self.conn.execute("DELETE FROM {} WHERE key=?".format(self.name), (key,))
        else:
            self.conn.execute(
                "REPLACE INTO {} (key, value) VALUES (?, ?)".format(self.name),
                (key, value),
            )
        self.conn.commit()

    def get(self, key: str):
        cursor = self.conn.execute(
            "SELECT value FROM {} WHERE key=?".format(self.name), (key,)
        )
        value = cursor.fetchone()
        if value:
            return value[0]
        else:
            return None
