class BaseGraphDatabase:

    def exists(self, node_type, **kwargs):
        pass

    def execute_query(self, query, **kwargs):
        pass

    def find_node(self, node_type, **kwargs):
        pass

    def add_node(self, node_type, **kwargs):
        pass

    def delete_nodes(self, id_list):
        pass

    def delete_all_nodes(self):
        pass

    