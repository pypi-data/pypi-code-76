import os
from typing import List, Union, Dict

from bson.objectid import ObjectId
from pymongo import InsertOne, DeleteMany, UpdateOne
from pymongo import MongoClient
from collections import namedtuple

# holds a cache of mongo clients so we only have to connect once
clientCache = {}

Insert = namedtuple('Insert', ['id', 'transactions'])
Update = namedtuple('Update', ['transactions'])
Remove = namedtuple('Remove', ['transactions'])

class Database:
    """
    Wrapper class around pyMongo::
        database = Database()
        Database('mongodb+srv://username:passsword@host/)

    class will set the database to the first one it has access to but you can
    change this with set_database function

    when the database is set the class will also update .collections which will
    give you all the collection names available in the selected database

    """
    client: MongoClient

    def __init__(self, uri: str) -> None:
        if not uri:
            raise ValueError('uri is required')
        if uri not in clientCache:
            clientCache[uri] = MongoClient(uri)
        self.client = clientCache[uri]
        self.databases = self.client.list_database_names()
        self.db_client = self.client[self.databases[0]]
        self._set_collections()

    def _set_collections(self) -> None:
        self.collections = self.db_client.list_collection_names()

    def set_database(self, database: str) -> None:
        if database not in self.databases:
            raise ValueError(f"{database} is not a valid database {self.databases}")
        self.db_client = self.client[database]
        self._set_collections()

    def get_collection(self, collection: str):
        return self.db_client[collection]

    def list_collections(self) -> List[str]:
        return self.collections

    def close(self):
        return self.client.close()


class Transaction:
    """
    Wrapper for mongo transactions
    https://docs.mongodb.com/manual/core/transactions/
    """

    def __init__(self, database: Database):
        self.database = database
        self.client = self.database.client
        self.transactions: Dict[str, List[Union[InsertOne, UpdateOne, DeleteMany]]] = {}  # empty transactions

    def insert(self, collection: str, document: dict):
        if collection not in self.transactions:
            self.transactions[collection] = []
        if '_id' not in document:
            document['_id'] = ObjectId()
        self.transactions[collection].append(InsertOne(document))
        return Insert(document['_id'], self.transactions)

    def update(self, collection: str, col_filter: dict, update: dict):
        if collection not in self.transactions:
            self.transactions[collection] = []
        self.transactions[collection].append(UpdateOne(col_filter, update))
        return Update(self.transactions)

    def remove(self, collection: str, col_filter: dict):
        if collection not in self.transactions:
            self.transactions[collection] = []
        self.transactions[collection].append(DeleteMany(col_filter))
        return Remove(self.transactions)

    def run(self):
        results = {}
        with self.client.start_session() as session:
            with session.start_transaction():
                for collection in list(self.transactions.keys()):
                    col = self.database.get_collection(collection)
                    results[collection] = col.bulk_write(self.transactions[collection])
        return results
