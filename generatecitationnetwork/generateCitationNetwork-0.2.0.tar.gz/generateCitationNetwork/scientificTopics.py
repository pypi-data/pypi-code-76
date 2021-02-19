#! /usr/bin/env python

# Copyright (C) 2020 GMPG, MPI for History of Science

import tempfile
import textacy
from textacy.vsm.vectorizers import Vectorizer
import textacy.tm
import numpy as np
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import wordnet


class GenerateScienceTopics:
    """Generates a list of topics contained in a dataframe.

    The input is assumed to be from the GenerateCitationNetwork class.
    """

    def __init__(self, dataframe):
        self.resList = ""
        self.df = dataframe
        self.corpus = ""
        self.doc_term_matrix = ""
        self.vectorizer = ""
        self.topics = ""
        self.tempfile = ""
        self.lang = textacy.load_spacy_lang("en_core_web_md")

    def makeCorpus(self):
        """Create the corpus."""
        citTexts = (
            self.df[self.df.type == "citation"][["sourceDOI", "titleStr"]]
            .set_index("sourceDOI")
            .to_dict()["titleStr"]
        )
        refTexts = (
            self.df[self.df.type == "reference"][["targetDOI", "titleStr"]]
            .set_index("targetDOI")
            .to_dict()["titleStr"]
        )
        citTexts.update(refTexts)
        records = [
            textacy.make_spacy_doc((text, {"doi": doi}), lang=self.lang)
            for doi, text in citTexts.items()
        ]
        self.corpus = textacy.Corpus(self.lang, data=records)
        return self

    def createDocTermMatrix(self):
        """Create the doc term matrix."""
        tokenized_docs = (
            [
                tok.lemma_.lower()
                for tok in spacy_doc
                if tok.is_stop is False and tok.is_punct is False
            ]
            for spacy_doc in self.corpus
        )
        self.vectorizer = Vectorizer(
            tf_type="linear",
            apply_idf=True,
            idf_type="smooth",
            norm="l2",
            min_df=2,
            max_df=0.9,
            max_n_terms=100000,
        )
        self.doc_term_matrix = self.vectorizer.fit_transform(tokenized_docs)
        return self

    def model(self, NTOPIC=30, NTOPWORDS=20, ALGORITHM="nmf"):
        """Run model for titles."""
        model = textacy.tm.TopicModel(ALGORITHM, n_topics=NTOPIC)
        model.fit(self.doc_term_matrix)
        self.topics = {}
        for topic_idx, top_terms in model.top_topic_terms(
            self.vectorizer.id_to_term, topics=-1, top_n=NTOPWORDS
        ):
            self.topics[topic_idx] = top_terms
        self.tempfile = tempfile.NamedTemporaryFile(mode="w")
        with open(self.tempfile.name, "w") as file:
            for line in self.df.titleStr.values:
                file.write(line + ".\n\n")
        return self

    def topicSynsets(self):
        """Generate information content corpus and compute word synsets.

        For each topic, the synsets for all words are calculated. Based on
        the information content of the corpus of all titles, the mutual
        distances between all synsets in a topic are calculated based on the
        Lin similarity. If the similarity reaches a threshold, it is added
        as a description of the topic.
        """
        rootPath = "/".join(self.tempfile.split("/")[:-1])
        fileid = self.tempfile.split("/")[-1]
        corpus = PlaintextCorpusReader(rootPath, fileid)
        wordnet_crossref = wordnet.ic(corpus)
        resDict = {}
        for key, val in self.topics.items():
            synsTop1 = [wordnet.synsets(x) for x in val]
            allSyns = list({x for y in synsTop1 for x in y})
            nSyns = []
            for x in allSyns:
                if x.name().split(".")[1] == "n":
                    nSyns.append(x)
            tmpDict = {}
            for elem in [nSyns]:
                for idx, x in enumerate(elem):
                    current = elem[idx]
                    tmplist = [x.lin_similarity(y, wordnet_crossref) for y in elem if y != current]
                    resList = []
                    for res in tmplist:
                        if res is None:
                            resList.append(0)
                        else:
                            resList.append(res)
                    median = np.median(resList)
                    if median > 0.072:
                        tmpDict[current.name()] = median
            resDict[str(key)] = tmpDict
        return resDict

    def run(self):
        """Run full topic chain."""
        res = self.makeCorpus().createDocTermMatrix().model().topicSynsets()
        return res
