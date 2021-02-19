# -*- coding: utf-8 -*-

from rdflib import Namespace, Graph
import os
import pathlib

import logging
logger = logging.getLogger(__name__)


class Convert(object):
    """docstring for Convert"""

    def __init__(self):
        super(Convert, self).__init__()
        self.nif_namespace = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
        self.itsrdf_namespace = Namespace("http://www.w3.org/2005/11/its/rdf#")
        self.rdf_namespace = Namespace("<http://www.w3.org/1999/02/22-rdf-syntax-ns#>")
        self.void_namespace = Namespace("http://rdfs.org/ns/void#")  # ????

    def convert(self, download_destination, corpus_dir, download_name, corpus_url, download_time):
        with open(os.path.join(corpus_dir, "source.txt"), "w") as open_file:
            open_file.write(f"Downloaded from {corpus_url} at {download_time}")

        print("Building graph")
        g = Graph()
        g.parse(download_destination, format="turtle")

        print("Extracting documents from nif")
        self.extract_files_from_nif_corpus(g, os.path.join(corpus_dir, "corpus"))

        print("Extracting entities from nif")
        self.extract_entities_from_nif_corpus(g, os.path.join(corpus_dir, "gold"), f"{download_name}.gs")

    def extract_files_from_nif_corpus(self, g, folder):
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

        for subject, predicate, object_ in g.triples((None, self.nif_namespace.isString, None)):
            document_number = (subject.split("/")[-1]).split("#")[0]
            filename = os.path.join(folder, document_number + ".txt")

            if not os.path.exists(filename):
                with open(filename, "w", encoding="utf-8") as open_file:
                    open_file.write(object_)

    def extract_entities_from_nif_corpus(self, g, folder, file_name):
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

        # Deactivating type detection
        type_ = "notfound"

        with open(os.path.join(folder, file_name), "w") as open_file:
            lines = set()

            for subject, predicate, object_ in g.triples((None, self.nif_namespace.anchorOf, None)):

                subject_id = subject.split("/")[-1]
                document_number, postition = subject_id.split("#")
                start, end = postition.split("=")[-1].split(",")
                surfaceForm = object_

                for subject_2, predicate_2, object_2 in g.triples((subject, self.itsrdf_namespace.taIdentRef, None)):

                    line = "\t".join([document_number, start, end, object_2.strip(), "1", type_, surfaceForm])
                    lines.add(line)

                for subject_2, predicate_2, object_2 in g.triples((subject, self.itsrdf_namespace.taClassRef, None)):

                    for subject_3, predicate_3, object_3 in g.triples((subject_2, self.nif_namespace.taMsClassRef, None)):

                        types = ['http://dbpedia.org/ontology/Person', 'http://xmlns.com/foaf/0.1/Person', 'http://dbpedia.org/ontology/Organisation', 'http://dbpedia.org/class/yago/Organization108008335', 'http://dbpedia.org/ontology/PopulatedPlace', 'http://dbpedia.org/ontology/Place', 'http://dbpedia.org/ontology/TelevisionShow', 'http://dbpedia.org/ontology/Work', 'http://dbpedia.org/ontology/Work', 'http://www.w3.org/2002/07/owl#Thing']
                        if object_2.strip() in types:

                            line = "\t".join([document_number, start, end, object_3.strip(), "1", type_, surfaceForm])
                            lines.add(line)
            for line in lines:
                open_file.write(line + "\n")

    def write_entity_to_file(self, open_file, document_number, start, end, object_2, type_, surfaceForm, separator="\t"):
        line = "\t".join([document_number, start, end, object_2.strip(), "1", type_, surfaceForm])
        open_file.write(line + "\n")
        return line

    def define_type(self, object_):

        types = {
            'http://dbpedia.org/ontology/Person': 'Person',
            'http://xmlns.com/foaf/0.1/Person': 'Person',
            'http://dbpedia.org/ontology/Organisation': 'Organization',
            'http://dbpedia.org/class/yago/Organization108008335': 'Organization',
            'http://dbpedia.org/ontology/PopulatedPlace': 'Location',
            'http://dbpedia.org/ontology/Place': 'Location',
            'http://dbpedia.org/ontology/TelevisionShow': 'TV',
            'http://dbpedia.org/ontology/Work': 'TV',
            'http://dbpedia.org/ontology/Work': 'Work',
        }

        return types.get(object_.strip(), 'http://www.w3.org/2002/07/owl#Thing')
