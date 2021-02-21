
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flatten_dict import flatten
import os


class Kraken_db:

    def __init__(self):

        # Initialize batch cache
        self.batch = []
        self.search_query = []
        self.update_list = []
        self.search_list = []
        self.post_list = []
        self.delete_list = []
        

        # Initialize parameters
        self.doc_path = None
        self.offset = None
        self.limit = None
        self.order_by = None
        self.direction = None



        # Initialize database
        project_id = 'kraken-v1'

        if (not len(firebase_admin._apps)):

            try:

                print(os.getenv("DB_USERNAME"))


                # Initialize from  google
                cred = credentials.Certificate("key.json")
                firebase_admin.initialize_app(cred, {
                    'projectId': project_id,
                })
                self.db = firestore.client()
            except:

                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred, {
                    'projectId': project_id,
                })
                self.db = firestore.client()
        else:
            self.db = firestore.client()




    def get(self, doc_path = None):

        if not doc_path:
            return None

        if doc_path:
            self.doc_path = doc_path

        query = self.db.document(self.doc_path)

        # Find document by document name
        doc = query.get()

        if doc: 
            record = doc.to_dict()

            # Remove fs prexif from records
            record = self.un_scrub_record(record)
            

            if record:
                if record.get('@id', None) != doc.id:   
                    record['@id'] = doc.id

        
        else:
            record = None


        return record


    def get_docs2(self, doc_path, order_by = 'createdDate', direction = "DESCENDING", offset = 0, limit = 100):

        query = self.db.collection(doc_path)

        if order_by:
            query = query.order_by(order_by, direction=direction)
        
        if offset and limit:
            query = query.offset(offset).limit(limit)

        # Get documents
        docs = query.stream()

        # Convert to dict
        records = []
        for doc in docs:
            record = doc.to_dict()

            # Remove fs prexif from records
            record = self.un_scrub_record(record)

            record['id'] = doc.id
            records.append(record)

        return records



    def add_to_search(self, doc_path, key, ops, value):

        record = {
            'doc_path': doc_path,
            'key': key,
            'ops': ops,
            'value': value
        }

        self.search_list.append(record)


    def get_docs(self, doc_path = None, order_by = None, direction = None, offset = 0, limit = 100):
        
        # Direction : ASCENDING, DESCENDING


        # Search based on query added by add_to_search

        if doc_path:
            self.doc_path = doc_path
        if offset:
            self.offset = offset
        if limit:
            self.limit = limit
        if order_by:
            self.order_by = order_by
        if direction:
            self.direction = direction

        # Set defaults if empty
        if not self.order_by and not self.search_list:
            self.order_by = 'createdDate'
            self.direction = 'DESCENDING'


        # Initialize query
        query = self.db.collection(self.doc_path)

        # Add search parameters
        for i in self.search_list:
            
            key = i.get('key')
            ops = i.get('ops')
            value = i.get('value')


            
            # Convert . notation
            # Get field_path by converting dot notation to individual field_path and adding them
            new_key = None
            for path_item in key.split('.'):
                if not new_key:
                    new_key = self.db.field_path(path_item)
                else:
                    new_key = self.db.field_path(new_key, path_item)
            
            # Add field path to query
            query = query.where(new_key, ops, value)


        # Add Order
        if self.order_by:
            if not self.direction:
                self.direction = "ASCENDING"
            query = query.order_by(self.order_by, direction=self.direction)
        
        # Add offset, limit
        if offset:
            query = query.offset(self.offset)

        if limit:
            query = query.limit(self.limit)


        # Run query to retrieve docs
        docs = query.stream()


        # Convert docs to dict
        records = []
        for doc in docs:
            record = doc.to_dict()
            # Remove fs prexif from records
            record = self.un_scrub_record(record)

            if record:
                record['id'] = doc.id
                records.append(record)


        


        return records


    def add_to_post(self, doc_path, record):
        # Add a single record to batch Write
        
        new_record = { 
            'doc_path': doc_path,
            'data': record
        }

        self.post_list.append(new_record)



    def post(self, doc_path = None, record = None):
        

        # If parameters, add to list
        if doc_path and record:
            self.add_to_post(doc_path, record)


        # Initialize batch operation
        batch = self.db.batch()

        if not self.post_list:
            return


        for item in self.post_list:

            doc_path = item.get('doc_path', None)
            record = item.get('data', None)
            
            # Add prefix to field key name for firestore
            record = self.scrub_record(record)

            doc = self.db.document(doc_path)

            # Add to batch
            batch.set(doc, record)

        # Write batch
        batch.commit()

        return 


    def un_scrub_record(self, record): 

        def un_scrub(record):

            if isinstance(record, str):
                new_record = record

            elif isinstance(record, dict):
                new_record = {}
                for i in record:
                    new_i = i
                    new_i = new_i.replace( '__dot__', ':')
                    new_i = new_i.replace( '__at__', '@')
                    new_i = new_i.replace('__slash__', '/')

                    
                    new_record[new_i] = un_scrub(record[i])

            elif isinstance(record, list):
                new_record = []
                for i in record:
                    new_record.append(un_scrub(i))

            else:
                new_record = record
        
            return new_record

        return un_scrub(record)


    def scrub_record(self, record):


        def scrub(record):

            if isinstance(record, str):
                new_record = record

            elif isinstance(record, dict):
                new_record = {}
                for i in record:
                    new_i = i
                    #new_i = new_i.replace(':', '__dot__')
                    #new_i = new_i.replace('@', '__at__')
                    #new_i = new_i.replace('/', '__slash__')
                    
                    new_record[new_i] = scrub(record[i])

            elif isinstance(record, list):
                new_record = []
                for i in record:
                    new_record.append(scrub(i))

            else:
                new_record = record
        
            return new_record

        return scrub(record)


    def add_to_update(self, doc_path, record):

        record = {
            'doc_path': doc_path,
            'data': record
        }
        self.update_list.append(record)


    def update(self, doc_path = None, record = None):
        
        # Process if parameters
        if doc_path and record:
            self.add_to_update(doc_path, record)


        batch = self.db.batch()

        if not self.update_list:
            return


        # Iterate through records in update_list
        for item in self.update_list:

            doc_path = item.get('doc_path', None)
            record = item.get('data', None)

            # Add prefix to field key name for firestore
            record = self.scrub_record(record)  

            # Flatten record, required for update in firestore (doesn't take nested dict)
            flat_record = flatten(record, reducer='dot')

            # Transform record before posting
            new_flat = {}
            for i in flat_record:

                # Skip identifiers
                if i in ['@type', '@id']:
                    continue

                # Only add if value exist
                if flat_record[i]:
                    new_flat[i] = flat_record[i]

            # Add doc to batch update 
            doc = self.db.document(doc_path)
            batch.update(doc, new_flat)



        batch.commit()


        return 

    
    def add_to_delete(self, doc_path):

        record = {
            'doc_path': doc_path
        }

        self.delete_list.append(record)


    def delete(self, doc_path = None):

        if doc_path:
            self.add_to_delete(doc_path)
        
        # Error handling empty list
        if not self.delete_list:
            return


        # Initialize batch operation
        batch = self.db.batch()




        for item in self.delete_list:

            doc_path = item.get('doc_path', None)

            doc = self.db.document(doc_path)

            # Add to batch
            batch.delete(doc)

        # Write batch
        batch.commit()

        return

