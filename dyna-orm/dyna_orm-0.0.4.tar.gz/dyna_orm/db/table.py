"""

This module holds the class for communicating with a dynamodb table.

The class Table acts as a facilitator to communicate with a dynamodb table
using only python code, very similar to what an ORM does.

"""

import boto3
from utils.exceptions import InstanceNotFound

dynamo = boto3.client('dynamodb')


class Table:
    def __init__(self, name, schema, pk_name='id'):
        """Class constructor

        Args:
            name (string): Table name as defined in the DB
            schema (tuple): Tuple with elements representing the table name's columns
        """                
        self.name = name
        self.schema = schema
        self.pk_name = pk_name
        self.valid_conditions = ['__eq', '__gt', '__lt']
        self.condition_mapper = {
            '__eq': "=",
            '__gt': ">",
            '__lt': "<"
        }
        # TODO: implement a better schema strategy (add type value)

    def _paginated_query(self, query):
        """Searh an or multiple instances withing a table

        Args:
            query (string): Dynamo PartiQL query

        Returns:
            list: a list of DynamoBaseInstance elements
        """        
        items = []
        next_token = None

        while True:
            if not next_token:
                res = dynamo.execute_statement(Statement=query)
            else:
                res = dynamo.execute_statement(Statement=query, NextToken=next_token)
            
            next_token = res.get('NextToken', None)
            
            for item in res.get("Items", []):
                items.append(DynamoBaseInstance(item))

            if not next_token:
                break
            
        return items

        
    def _validate_fields(self, fields):
        """Check if field keys follow the schema

        Args:
            fields (dict): Dictionary with key names representing a table's column names

        Raises:
            ValueError: If key not in schema
        """
        print(f"_validate_fields -> fields: {fields}")
        for field in fields:
            if field not in self.schema:
                if not self._valid_field_condition(field):
                    raise ValueError("Error: Field '{field}' not in schema.".format(field=field))
    
    def _valid_field_condition(self, field):
        temp_schema = []
        for schema_field in self.schema:
            for condition in self.valid_conditions:
                temp_schema.append(schema_field+condition)
        
        print(f"_valid_field_condition -> temp_schema: {temp_schema}")
        print(f"_valid_field_condition -> field: {field}")
        if field in temp_schema:
            return True
        return False
        

    def get(self, _id):
        """Get an instance from a table name by id

        Args:
            _id (string): Table instance id

        Returns:
            DynamoBaseInstance: An instance from the table
        """        
        query = "SELECT * FROM {table_name} WHERE {pk_name} = '{id}'"
        query = query.format(table_name=self.name, id=_id, pk_name=self.pk_name)
        print("Get Query formed:", query)
        items = self._paginated_query(query)
        if not items:
            raise InstanceNotFound("The instance with id: '{id}' was not found".format(id=_id))
        return items[0]


    def update(self, _id, **fields):
        """ Update an element from a dynamodb table.
        **fields should be anything from the schema

        Args:
            _id (text): the id of the element to update
        """
        # schema validate
        self._validate_fields(fields)

        items = fields.items()
        parameters = []
        for (key, value) in items:
            if type(value) == str:
                parameters.append({'S': value})
            elif type(value) == bool:
                parameters.append({'BOOL': value})
            elif type(value) == int:
                parameters.append({'N': value})

        # build query
        # keys_values = fields.items()
        query = "UPDATE {table_name} SET ".format(table_name=self.name)
        for i, (key, value) in enumerate(items):
            query += "{key} = ?".format(key=key)
            # last item?
            if i == (len(items)-1):
                query += " "
            else:
                query += ", "
        query += "WHERE {pk_name} = '{id}'".format(id=_id, pk_name=self.pk_name)
        
        print("Update Query formed:", query)
        res = dynamo.execute_statement(Statement=query, Parameters=parameters)
        # res = self._query_db(query)

        print("Result of updating event in db:", res)


    def delete(self, _id):
        """Delete an instance from a table using the id

        Args:
            _id (string): Instance id
        """
        query = "DELETE FROM {table_name} WHERE {pk_name} = '{id}'".format(table_name=self.name, id=_id, pk_name=self.pk_name)
        print("Delete Query formed:", query)
        res = dynamo.execute_statement(Statement=query)
        print("Event deleted:", res)

    def _create_condition(self, key):
        """Defines a numeric operator based on a key definition name
        i.e.: key__gt gets a '>'

        Args:
            key (string): table column name with a potential embedded condition
        
        Returns:
            string: A numeric operator such as =, > or <
        """        
        condition = self._get_key_condition(key) # __eq
        # for valid_condition in self.valid_conditions:
        #     if condition == valid_condition:
        return self.condition_mapper[condition]
        

    def _get_key_condition(self, key):
        """Find a condition embedded in a key ie: key__gt

        Args:
            key (string): table column name
        """        
        # valid_conditions = ['__gt', '__lt']
        for condition in self.valid_conditions:
            if condition in key:
                return condition
        return '__eq'
        

    def filter(self, **fields):
        """Find instances that match the corresponding field values

        Returns:
            list: A list of DynamoBaseInstance objects
        """        
        # schema validate
        self._validate_fields(fields)
        # build query
        keys_values = fields.items()
        query = "SELECT * FROM {table_name} WHERE ".format(table_name=self.name)
        for i, (key, value) in enumerate(keys_values):
            
            condition = self._create_condition(key)
            # remove condition string ('__gt', '__lt', '__eq') from key
            for str_condition in self.valid_conditions:
                if str_condition in key:
                    key = key.replace(str_condition, "")
            
            if type(value) == str:
                query += "{key} {condition} '{value}'".format(key=key, condition=condition, value=value)
            else:
                query += "{key} {condition} {value}".format(key=key, condition=condition, value=str(value))
            # last item?
            if i != (len(keys_values)-1):
                query += " AND "

        print("Filter Query formed:", query)
        items = self._paginated_query(query)
        return items
                
        
    def exists(self, _id):
        """Check wether or not an event item exists 
        in the events database

        Returns:
            bool: true/false indicator
        """
        print("Checking if event exists in db")
        query = "SELECT * FROM {table_name} WHERE {pk_name} = '{id}'".format(table_name=self.name, pk_name=self.pk_name, id=_id)
        print("Exists Query formed:", query)
        res = dynamo.execute_statement(Statement=query)

        items = res.get('Items', [])
        if len(items) > 0:
            print("Found existing item: ", items)
            return True
        return False


    def insert(self, **fields):
        """Create a new instance in a table with a set of given value fields
        """        
        # schema validation
        self._validate_fields(fields)
        
        items = fields.items()

        parameters = []
        for (key, value) in items:
            if type(value) == str:
                parameters.append({'S': value})
            elif type(value) == bool:
                parameters.append({'BOOL': value})
            elif type(value) == int:
                parameters.append({'N': value})

        # build query    
        query = "INSERT INTO {table_name} VALUE {{".format(table_name=self.name)
        for i, (key, value) in enumerate(items):
            query += "'{key}' : ?".format(key=key)
            if i == (len(items)-1):
                query += "}"
            else:
                query += ", "
        
        print("Insert Query formed:", query)
        res = dynamo.execute_statement(Statement=query, Parameters=parameters)
        print("Result of inserting event in db:", res)
        

    def delete_events(self, **fields):
        """Delete all found events given a set of column values defined in 
        the fields argument
        """        
        events = self.filter(**fields)
        if events:
            print("Amount of events to delete:", len(events))
        for event in events:
            self.delete(event.id)



class DynamoBaseInstance:
    def __init__(self, response):
        """Class constructor

        Args:
            response (dynamo instance): A dictionary with the following format: 
            {
                'column_name':{
                    'column_type': 'column_value'
                },
            }
        """
        # print("Dynamo Base Instance Response:", response)        
        
        for field in response:
            if "S" in response.get(field, {}):
                setattr(self, field, response.get(field, {}).get("S", None))
            elif "BOOL" in response.get(field, {}):
                setattr(self, field, response.get(field, {}).get("BOOL", None))
            elif "N" in response.get(field, {}):
                setattr(self, field, response.get(field, {}).get("N", None))


# # Example:
# events_schema = ('id', 'content', 'created_at', 'ends', 'starts', 'synced_at', 
#     'updated_at', 'info', 'event_type', 'user_id', 'provider',
#     'ical_uid', 'is_deleted', 'series_master_id', 'title')
# events_table = Table('events', schema=events_schema)