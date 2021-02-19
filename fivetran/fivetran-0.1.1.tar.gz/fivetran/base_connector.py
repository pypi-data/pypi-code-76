class Table:
    def __init__(self, name, primary_key=['id']):
        self.name         = name
        self.insert       = []
        self.delete       = []
        self._primary_key = primary_key
        
    def insert_record(self, record):
        self.insert.append(record)

    def insert_records(self, records):
        self.insert.extend(records)

    def delete_record(self, record):
        self.delete.append(record)

    def delete_records(self, records):
        self.delete.extend(records)

    def primary_key(self):
        return { "primary_key": self._primary_key }

class BaseConnector:
    def __init__(self, name, state, tables):
        self.name    = name
        self._state  = state or self._default_state()
        self._tables = self._register_tables(tables)

    def state(self):
        return self._state

    def insert(self):
        insert = {}
        for table in self._tables:
            insert[table.name] = table.insert
        return insert

    def delete(self):
        delete = {}
        for table in self._tables:
            delete[table.name] = table.delete
        return delete

    def schema(self):
        schema = {}
        for table in self._tables:
            schema[table.name] = table.primary_key()
        return schema

    def has_more(self):
        try:
            return self._state['has_more']
        except:
            raise KeyError(f'has_more missing from the state of {self.name}')

    def reset_state(self):
        raise NotImplementedError(f'reset_state() not implemented for {self.name}')

    def _default_state(self):
        raise NotImplementedError(f'_default_state not implemented for {self.name}')

    def _register_tables(self, tables):
        tables_dict = {}
        for table_obj in tables:
            tables_dict[table_obj.name] = table_obj
        return tables_dict

    def _get_table(self, table_name):
        try:
            return self._tables[table_name]
        except:
            raise KeyError(f'Invalid table name in _get_table() in Connector: {self.name}')

    def _insert_record(self, table_name, record):
        table = self._get_table(table_name)
        table.insert_record(record)
        
    def _insert_records(self, table_name, records):
        table = self._get_table(table_name)
        table.insert_records(records)

    def _delete_record(self, table_name, record):
        table = self._get_table(table_name)
        table.delete_record(record)

    def _delete_records(self, table_name, records):
        table = self._get_table(table_name)
        table.delete_records(records)