from elasticsearch import Elasticsearch
import face_recognition
import os


DEFAULT_ES_URL = os.getenv("TEXTA_FACE_ANALYZER_ES_URL", "http://localhost:9200")
DEFAULT_ES_INDEX = os.getenv("TEXTA_FACE_ANALYZER_ES_INDEX", "texta_fugitivus")


class FaceAnalyzer:

    def __init__(self, es_url=DEFAULT_ES_URL, es_index=DEFAULT_ES_INDEX, es_vector_field="face_vector", es_name_field="name"):
        self.es = Elasticsearch(DEFAULT_ES_URL)
        self.es_index = es_index
        self.es_vector_field = es_vector_field
        self.es_name_field = es_name_field


    def delete_index(self):
        self.es.indices.delete(self.es_index)


    def _generate_mapping(self):
        mapping = {
            "mappings": {
                "properties": {
                    self.es_vector_field: {
                        "type": "dense_vector",
                        "dims": 128
                    },
                    self.es_name_field : {
                        "type" : "keyword"
                    }
                }
            }
        }
        return mapping


    def _generate_vector_query(self, face_vector):
        query = {
            "query": {
                "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": f"cosineSimilarity(params.query_vector, '{self.es_vector_field}') + 1.0",
                    "params": {
                        "query_vector": face_vector
                    }
                }
                }
            }
        }
        return query   


    def add_photo(self, file_path, name="John Doe"):
        """
        Adds photo to Elastic index.
        """
        # create index if necessary
        self.es.indices.create(index=self.es_index, body=self._generate_mapping(), ignore=[400, 404])
        # find facial vectors
        face_encodings = self.vectorize_photo(file_path)
        # store facial vectors
        for face_encoding in face_encodings:
            doc = {self.es_name_field: name, self.es_vector_field: face_encoding.tolist()}
            self.es.index(index=self.es_index, body=doc)
        return True


    def analyze_photo(self, file_path, score=1.93):
        """
        Finds similar faces from Elasticsearch index.
        """
        face_encodings = self.vectorize_photo(file_path)

        for face_encoding in face_encodings:
            face_vector = face_encoding.tolist()
            query = self._generate_vector_query(face_vector)
            result = self.es.search(index=self.es_index, body=query)
            hits = [(hit["_score"], hit["_source"]["name"]) for hit in result["hits"]["hits"] if hit["_score"] > score]
            return hits


    def vectorize_photo(self, file_path):
        """
        Vectorizes faces found on a photo.
        """
        image = face_recognition.load_image_file(file_path)
        face_encodings = face_recognition.face_encodings(image)
        return face_encodings        
