from elasticsearch import Elasticsearch
from elasticsearch_dsl import Keyword, Mapping, Nested, DenseVector
import face_recognition
import os


DEFAULT_ES_URL = os.getenv("TEXTA_FACE_ANALYZER_ES_URL", "http://localhost:9200")
DEFAULT_ES_INDEX = os.getenv("TEXTA_FACE_ANALYZER_ES_INDEX", "texta_fugitivus")


class FaceAnalyzer:

    def __init__(
            self,
            es_url=DEFAULT_ES_URL,
            es_index=DEFAULT_ES_INDEX,
            es_vector_field="vector",
            es_name_field="name",
            es_nested_field_name="texta_face_vectors"
        ):
        self.es = Elasticsearch(DEFAULT_ES_URL)
        self.es_index = es_index
        self.es_vector_field = es_vector_field
        self.es_name_field = es_name_field
        self.es_nested_field_name = es_nested_field_name


    def delete_index(self):
        self.es.indices.delete(self.es_index)


    def _create_index(self):
        """
        Creates ES index with proper mapping to store facial vectors.
        """
        created = self.es.indices.create(self.es_index, ignore=[400, 404])
        # if status not defined, we had a successful put!
        if not "status" in created:
            m = Mapping()
            texta_face_vectors = Nested(
                properties={
                    self.es_name_field: Keyword(),
                    self.es_vector_field: DenseVector(dims=128),
                }
            )
            # Set the name of the field along with its mapping body
            m.field(self.es_nested_field_name, texta_face_vectors)
            m.save(index=self.es_index, using=self.es)


    def _generate_vector_query(self, face_vector, min_score):
        vector_field_name = f"{self.es_nested_field_name}.{self.es_vector_field}"
        query = {
            "query": {
                "nested": {
                    "path": self.es_nested_field_name,
                    "query": {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                # we add 1.0 because Elastic dislikes negative scores
                                "source": f"1.0 + cosineSimilarity(params.query_vector, '{vector_field_name}')",
                                "params": {
                                    "query_vector": face_vector
                                }
                            },
                            "min_score": min_score
                        }
                    }
                }
            }
        }
        return query   


    def vectors_to_facts(self, face_vectors, name):
        """
        Converts the face vectros to TEXTA format.
        """
        for face_vector in face_vectors:
            vector_fact = {self.es_name_field: name, self.es_vector_field: face_vector.tolist()}
            yield vector_fact


    def add_photo(self, file_path, name="UNKOWN"):
        """
        Adds photo to Elastic index.
        """
        # create index if necessary
        self._create_index()
        # find facial vectors
        face_vectors = self.vectorize_photo(file_path)
        # store facial vectors
        if face_vectors:
            vector_facts = self.vectors_to_facts(face_vectors, name)
            doc = {self.es_nested_field_name: list(vector_facts)}
            self.es.index(index=self.es_index, body=doc)
        return True


    def analyze_photo(self, file_path, score=1.93):
        """
        Finds similar faces from Elasticsearch index.
        """
        combined_hits = []
        face_encodings = self.vectorize_photo(file_path)

        for face_encoding in face_encodings:
            face_vector = face_encoding.tolist()
            query = self._generate_vector_query(face_vector, score)
            result = self.es.search(index=self.es_index, body=query)
            for hit in result["hits"]["hits"]:
                if self.es_nested_field_name in hit["_source"]:
                    for hit_fact in hit["_source"][self.es_nested_field_name]:
                        # remove vector from fact
                        del hit_fact["vector"]
                        combined_hits.append(hit_fact)

        return combined_hits


    def vectorize_photo(self, file_path):
        """
        Vectorizes faces found on a photo.
        """
        image = face_recognition.load_image_file(file_path)
        face_encodings = face_recognition.face_encodings(image)
        return face_encodings        
