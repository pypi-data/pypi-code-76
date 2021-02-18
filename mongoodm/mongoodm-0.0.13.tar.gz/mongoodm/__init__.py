from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from functools import partial
from urllib.parse import urlparse
from importlib.util import find_spec

try:
    from flask import _app_ctx_stack as stack
except ImportError:
        pass

_staticTypes = [str, list, tuple, dict, int, float, complex, bytes, bytearray]

def convert(name):
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class DocumentCursor(object):
    """ This document cursor simply abstracts the pymongo.cursor 
    and ensures that results returned from it are of a cls type of class """
    def __init__(self, cls, cursor):
        """ Accepts the class type and pymongo cufrsor as arguments """
        self.cursor = cursor
        self.cls = cls

    # The following are special attributes used in python to tell
    # the python world this class is an iterator
    def __iter__(self):
        return self

    def __next__(self):
        value = self.cursor.next()
        if not value:
            return value

        cls = self.cls
        return cls(saved=True, **value)

    # A passthrough is setup to make sure that any list like requests
    # are passed on to the pymongo cursor
    def __getitem__(self, index):
        cls = self.cls
        return cls(self.cursor.__getitem__(index))

    # Calls to any methods or properties the DocumentCursor
    # doesn't specifically have is also passed to the pymongo Cursor
    def __getattr__(self, name):
        return self.cursor.__getattribute__(name)

    def __len__(self):
        return self.cursor.count()

class DocumentMeta(type):
    _driver = {}

    def __new__(cls, name, bases, clsdct):
        if '_collection_name' not in clsdct:
            clsdct['_collection_name'] = convert(name)
        if '_restore_id' not in clsdct:
            clsdct['_restore_id'] = False
        if '_preserve_ids' not in clsdct:
            clsdct['_preserve_ids'] = False
        return super().__new__(cls, name, bases, clsdct)

    def __init__(cls, name, bases, clsdct):
        super().__init__(name, bases, clsdct)
        if hasattr(cls, '_driver') and hasattr(cls._driver, 'register_class'):
            cls._driver.register_class(name, cls)

    
class Document(metaclass=DocumentMeta):
    """
    The Document class is the base class for all other document types
    and defines a common subset of functionality needed for all document
    actions
    """    

    def __init__(self, *args, saved=False, **kwargs):
        super().__init__()
        if '_id' in kwargs: 
            if type(kwargs['_id']) != ObjectId:
                if type(kwargs['_id']) != str:
                    raise Exception("_id must be either a valid ObjectId or string hex representation")
                if not ObjectId.is_valid(kwargs['_id']):
                    raise Exception("_id was a string but not a valid ObjectId")

                kwargs['_id'] = ObjectId(kwargs['_id'])
            kwargs['id'] = kwargs['_id']
            del kwargs['_id']

        self._unsavedItems = {}
        
        for key, value in kwargs.items():
            if not saved:
                if not value == None and type(value) in _staticTypes:
                    self._unsavedItems[key] = type(value)()
                else:
                    self._unsavedItems[key] = None
            
            self[key] = value
        self._saved = saved

    @classmethod
    def _collection(cls):
        return cls._db()[cls._collection_name]

    @classmethod
    def _db(cls):
        if not cls._driver:
            raise Exception("Database hasn't been initialised yet")

        return cls._driver.connection[cls._driver.db]

    def update(self, updates : dict):
        if not isinstance(updates, dict):
            raise TypeError("updates must be a dict")

        for key, value in updates.items():
            self.__setattr__(key, value)

        return None
        

    def save(self, create_new: bool = True, replace: bool = False) -> bool:
        """ Saves the relevant document in the correct collection """
        attributes = self._filtered_attributes(ignore_settings=True)
        # If there's no _id or the id is None
        if ("id" not in attributes or not attributes['id']) and create_new:
            if 'id' in attributes: del attributes['id']
            result = type(self)._collection().insert_one(attributes)
            self.id = result.inserted_id
            self._saved = True
            self._unsavedItems = {}
            return True

        # If we're entirely replacing the document
        if replace:
            values = self._filtered_attributes(ignore_settings=True)
            if 'id' in values:
                values['_id'] = values['id']
                del values['id']
                
            result = type(self)._collection().replace_one({"_id": self.id}, values, upsert=create_new)
            if result.upserted_id:
                self.id = result.upserted_id
                self._saved = True
                self._unsavedItems = {}
                return True

            if result.modified_count > 0:
                self._saved = True
                self._unsavedItems = {}
                return True
            
            return False
            

        values = {}
        for key, value in self._unsavedItems.items():
            values[key] = self[key]

        if 'id' in values:
            values['_id'] = values['id']
            del values['id']

        result = type(self)._collection().update_one({"_id": self.id}, {"$set":values}, upsert=create_new)
        if result.matched_count > 0:
            self._saved = True
            self._unsavedItems = {}
            return True

        return False

    def discard(self):
        if self._saved:
            return True

        if not self._unsavedItems:
            return False

        for key, value in self._unsavedItems:
            self.__dict__[key] = value
        
        self._unsavedItems = {}
        self._saved = True
        return True

    def get(self, key, value=None):
        if key in self.__dict__:
            return self[key]

        return value

    def delete(self):
        result = type(self)._collection().delete_one({"_id": self.id})
        if result.deleted_count > 0:
            return True

        return False

    def __iter__(self):
        return iter(self._filtered_attributes().items())

    def __getitem__(self, key):
        # If the current document has an id and we're looking for _id
        if 'id' in self.__dict__ and self.__dict__["id"] and key == "_id":
            # Check to see if preserve_id is set
            if self._preserve_ids or self._restore_id:
                return self.__dict__["id"]
        try:
            return self.__dict__[key]
        except KeyError:
            raise AttributeError
        
    
    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        self.__dict__["_saved"] = False
        if "_unsavedItems" in self.__dict__:
            if not key.startswith("_") and not self._unsavedItems.get(key, None):
                self._unsavedItems[key] = value
        self.__dict__[key] = value

    def __setitem__(self, key, value):
        self.__setattr__(key, value)
        
    def _filtered_attributes(self, ignore_settings=False) -> dict:
        """ Filters all the instance attributes if they start with two underscores """
        attr = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        # If the current document has an id
        if hasattr(self, 'id') and self.id and ignore_settings == False:
            # Check to see if preserve_id is set
            if self._preserve_ids or self._restore_id:
                attr['_id'] = attr['id']
                # If it's restore id that's set we don't need the self.id attr so remove it
                if self._restore_id:
                    del attr['id']
        return attr

    def __json__(self):
        return self._filtered_attributes()

    def __len__(self):
        return len(self._filtered_attributes().keys())

    def keys (self):
        return self._filtered_attributes().keys()

    def to_dict(self):
        return self._filtered_attributes()

    def __str__(self):
        return "<{}.{} {}>".format(type(self).__module__, type(self).__qualname__, self._filtered_attributes())

    def __contains__(self, key):
        return key in self._filtered_attributes()

    @classmethod
    def set_db(cls, db):
        cls._driver.set_db(db)

    @classmethod
    def find(cls, *args, **kwargs):
        """ Helper function to more easily run finds """
        result = cls._collection().find(*args, **kwargs)
        if not result:
            return result

        return cls._make_iterator(result)

    @classmethod
    def find_one(cls, *args, **kwargs):
        """ Helper function to more easily run finds """
        result = cls._collection().find_one(*args, **kwargs)
        if not result:
            return result

        return cls(**result)
    
    @classmethod
    def all(cls):
        return cls.find({})

    @classmethod
    def get_by_id(cls, Id):
        """ Using a string or ObjectId, grabs a relevant document """
        if isinstance(Id, str) and ObjectId.is_valid(Id):
            Id = ObjectId(Id)
        elif not isinstance(Id, ObjectId):
            raise Exception('Id was not a valid objectid')

        record = cls._collection().find_one({'_id': Id})

        if not record:
            return None

        return cls(**record)

    @classmethod
    def _make_iterator(cls, iterator):
        return DocumentCursor(cls, iterator)


class MongoODM(object):
    _supported_providers = ['mongomock', 'pymongo']
    _db = None
    

    def __init__(self, app=None, **config):
        # Save the application config
        self._registry = {}
        self.config = config

        # For working as a flask extension
        self.app = app
        if app != None:
            from flask import _app_ctx_stack as stack
            self.stack = stack
            self.init_app(app)

        self.Document = type(
            'Document',
            Document.__mro__,
            dict(Document.__dict__, _driver=self)
        )

    def __call__(self, document):
        """
        Allows a document or Document class to access the database
        without setting what connection to use earlier.

        @param document The document or collection on which to inject the connection
        @type document Document|Document()
        """

        if isinstance(document, type):
            # We're dealing with a class so lets copy it and add a ref to this connection
            return type(
                document.__name__,
                document.__mro__,
                dict(document.__dict__, _driver=self)
            )

        # Disclaimer: I HATE THIS
        # We create a copy of the class as per usual
        # Instantiate a new variable of the new class
        # Copy the state of the old var to the new one
        # Return the new variable which has a ref to this connection
        # I'm sorry.
        newclass = type(
                type(document).__name__,
                type(document).__mro__,
                dict(type(document).__dict__, _driver=self)
            )()
        newclass.__dict__.update(document.__dict__)
        return newclass
        

    def __enter__(self):
        return self.connection

    def __exit__(self, *args):
        pass

    def __getattr__(self, name):
        if name not in self.__dict__:
            return self._registry[name]

        return self.__getattribute__(name)

    def register_class(self, name, cls):
        self._registry[name] = cls

    def init_app(self, app):
        driver_config = app.config.get(
            'MONGOODM_DRIVER_OPTIONS',
            self.config.get('driver_config', {})
        )

        uri = app.config.get(
            'MONGOODM_URI',
            self.config.get('uri', 'mongodb://localhost:27017/test')
        )
        provider = app.config.get(
            'MONGOODM_PROVIDER',
            self.config.get('provider', 'pymongo')
        )

        parsed_url = urlparse(uri)

        db_name = app.config.get(
            'MONGOODM_DB',
            self.config.get('db_name', parsed_url.path.split('/')[0])
        )

        self.config.update({
            'uri': uri,
            'provider': provider,
            'db_name': db_name or 'test'
        })
        app.teardown_appcontext(self.teardown)

    def setup_connection(self):
        provider = self.config.get('provider', 'pymongo')
        if provider not in self._supported_providers:
            raise Exception('Specified provider is not supported')

        if not find_spec(provider):
            raise Exception('Specified provider is not installed')
        
        options = self.config.get('driver_options', {})

        uri = self.config.get('uri')
        if provider == 'mongomock':
            import mongomock
            self._db = mongomock.MongoClient(self.config.get('uri'), **options)
        elif provider == 'pymongo':
            import pymongo
            self._db = pymongo.MongoClient(self.config.get('uri'), **options)

        return self._db


    def teardown(self, exc):
        if 'stack' in globals():
            ctx = stack.top
            if hasattr(ctx, 'mongoodm_connection'):
                ctx.mongoodm_connection.close()

    def set_db(self, name):
        self.config.db_name = name

    @property
    def connection(self):
        if self.app and 'stack' in globals():
            ctx = stack.top
            if ctx != None:
                if not hasattr(ctx, 'mongoodm_connection'):
                    ctx.mongoodm_connection = self.setup_connection()
                return ctx.mongoodm_connection
        else:
            if not self._db:
                self.setup_connection()
            return self._db

        return None

    @property
    def db(self):
        return self.config.get('db_name', 'test')