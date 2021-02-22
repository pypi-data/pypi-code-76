from mysql.connector import connect
from pydoge import ConnectionDbCursor, chunks


class MysqlClient:
    def __init__(self, options, auto_commit=True):
        self.connection_options = options
        self.auto_commit = auto_commit

    def __enter__(self):
        try:
            self.connection = connect(
                **self.connection_options
            )
            return self
        except Exception as e:
            raise Exception(f'ERROR: Cannot connect to RDS: {str(e)}')

    def __exit__(self, exc_type, exc_value, traceback):
        if self.auto_commit:
            self.connection.commit()
        self.connection.close()

    def execute_query(self, query, params=(), fetch=True):
        with ConnectionDbCursor(self.connection) as cursor:
            cursor.execute(query, params=params)
            if fetch:
                rows = cursor.fetchall()
                return rows

    def execute_procedure(self, procedure_name, params=(), return_rows=False):
        with ConnectionDbCursor(self.connection) as cursor:
            cursor.callproc(procedure_name, args=params)
            if return_rows:
                for result in cursor.stored_results():
                    rows = result.fetchall()
                    return rows

    def generate_truncate_statement(self,
                                    schema, table): return f'truncate {schema}.{table};'

    def generate_string_placeholders(
        self, i): return ','.join(['%s' for x in range(i)])

    def generate_insert_statement(
        self, schema, table, cols
    ): return f'insert into {schema}.{table}({",".join(cols)}) values({self.generate_string_placeholders(len(cols))})'

    def insert_rows(self, schema, table, rows, chunk_size=10000, truncate=False):
        if truncate:
            sql = self.generate_truncate_statement(schema, table)
            self.execute_query(sql, fetch=False)

        total_rows = len(rows)
        if (total_rows > 0):
            cols = rows[0].keys()

            insert_query = self.generate_insert_statement(
                schema=schema,
                table=table,
                cols=cols
            )

            with ConnectionDbCursor(self.connection) as cursor:
                new_list = list(chunks(rows, chunk_size))
                for batch in new_list:
                    data = list(map(lambda item: tuple(item.values()), batch))
                    cursor.executemany(insert_query, data)
