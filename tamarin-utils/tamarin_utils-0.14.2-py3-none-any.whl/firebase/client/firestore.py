from ...connections.client import Client
from firebase_admin import firestore, initialize_app, credentials
from google.cloud.firestore import SERVER_TIMESTAMP, ArrayUnion, ArrayRemove, Increment, DELETE_FIELD
from uuid import uuid4
import os
from django.conf import settings

_DEFAULT_APP_NAME = 'FIRESTORE_DEFAULT'


class FirestoreClient(Client):
    __client__ = None

    __firestore_client__ = None

    __credential__ = credentials.Certificate(
        os.environ.get(
            'GOOGLE_APPLICATION_CREDENTIALS',
            getattr(
                settings,
                'GOOGLE_APPLICATION_CREDENTIALS'
            )
        )
    )

    @staticmethod
    def get_instance():
        return FirestoreClient.__firestore_client__ or FirestoreClient()

    def __init__(self):
        if FirestoreClient.__firestore_client__:
            raise Exception("Firestore is singleton, just one instance")
        else:
            credential = FirestoreClient.__credential__
            options = getattr(settings, 'FIREBASE_APP_OPTIONS', None)
            name = getattr(settings, 'FIREBASE_APP_NAME', _DEFAULT_APP_NAME)
            app = initialize_app(credential=credential, options=options, name=name)
            FirestoreClient.__client__ = firestore.client(app=app)
            FirestoreClient.__firestore_client__ = self

    def request(self, method, url, data=None, json=None, query_params=None, **kwargs):
        raise PermissionError("Firestore client request method not allowed")

    @property
    def client(self):
        return self.__client__

    def send(self, collection, data, document_id=None):
        client = self.client
        collection = client.collection(collection)
        if document_id is None:
            document_id = str(uuid4())
        document = collection.document(document_id)
        document.set(data)

    def update(self, collection, document_id, data):
        client = self.client
        collection = client.collection(collection)
        document = collection.document(document_id)
        document.update(data)

    def list(self, collection):
        client = self.client
        collection = client.collection(collection)
        documents = collection.stream()
        response = [{document.id: document.to_dict()} for document in documents]
        return response

    def delete(self, collection, document_id):
        client = self.client
        collection = client.collection(collection)
        document = collection.document(document_id)
        document.delete()

    @property
    def timestamp(self):
        return SERVER_TIMESTAMP

    @staticmethod
    def add_or_update_array_item(array_field, item):
        return {
            array_field: ArrayUnion([item])
        }

    @staticmethod
    def remove_array_item(array_field, item):
        return {
            array_field: ArrayRemove([item])
        }

    @staticmethod
    def increment_numeric_value(field, increment):
        return {
            field: Increment(increment)
        }

    @staticmethod
    def delete_field(field):
        return {
            field: DELETE_FIELD
        }
