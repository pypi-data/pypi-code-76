class AggregateConnector:
    def __init__(self, name, state, connectors):
        self.name = name
        self._state = state
        self._connectors = connectors

    def state(self):
        # return self._state
        state = {}
        for connector_id, connector_obj in self._connectors.items():
            state[connector_id] = connector_obj.state()
        return state
 
    def insert(self):
        insert_dict = {}
        for connector in self._connectors.values():
            connector_insert = connector.insert()
            for table, records in connector_insert.items():
                if table in insert_dict:
                    insert_dict[table].extend(records)
                else:
                    insert_dict[table] = []
                    insert_dict[table].extend(records)
        return insert_dict

    def delete(self):
        delete_dict = {}
        for connector in self._connectors.values():
            connector_delete = connector.delete()
            for table, records in connector_delete.items():
                if table in delete_dict:
                    delete_dict[table].extend(records)
                else:
                    delete_dict[table] = []
                    delete_dict[table].extend(records)
        return delete_dict

    def schema(self):
        schema_dict = {}
        for connector in self._connectors.values():
            connector_schema = connector.schema()
            for table, schema in connector_schema.items():
                if table not in schema_dict:
                    schema_dict[table] = schema
        return schema_dict

    def has_more(self):
        for connector in self._connectors.values():
            if connector.has_more():
                return True
        return False

    def get_records(self):
        for connector in self._connectors.values():
            connector.get_records()

    def reset_state(self):
        for connector in self._connectors.values():
            connector.reset_state()