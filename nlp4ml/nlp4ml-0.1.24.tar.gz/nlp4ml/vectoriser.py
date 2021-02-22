import sys
import numpy as np
from collections import Counter
from collections import defaultdict
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import KeyedVectors
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class EmbeddingVectorizer(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self):
        return X

    def fit_transform(self, X, y=None):
        self.fit(X, y)

    def progressbar(self, iteration, prefix="", size=50, file=sys.stdout):
        count = len(iteration)
        def show(t):
            x = int(size*t/count)
            # file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), int(100*t/count), 100))
            file.write("{}[{}{}] {}%\r".format(prefix, "█"*x, "."*(size-x), int(100*t/count)))
            file.flush()
        show(0)
        for i, item in enumerate(iteration):
            yield item
            show(i+1)
        file.write("\n")
        file.flush()

class MeanEmbeddingVectorizer(EmbeddingVectorizer):
    """
    Parameters
    ----------
    word2vec: gensim.models.KeyedVectors()
        Word2Vec: https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz
        GloVe: https://nlp.stanford.edu/projects/glove/
        FastText: https://fasttext.cc/docs/en/crawl-vectors.html

    Examples
    --------
    >>> from gensim.scripts import glove2word2vec
    >>> from gensim.models import KeyedVectors
    >>> w2v_model = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)
    >>> glove2word2vec(glove_input_file=r"glove.840B.300d.txt", word2vec_output_file=r"gensim_glove_vectors.txt")
    >>> glove_model = KeyedVectors.load_word2vec_format("gensim_glove_vectors.txt", binary=False)
    >>> embedding_dict = KeyedVectors.load_word2vec_format(r"cc.en.300.vec", binary=False)
    >>> embedding_dict.save_word2vec_format(r"cc.en.300.bin", binary=True)
    >>> ft_model = KeyedVectors.load_word2vec_format("cc.en.300.bin", binary=True)
    >>> vectoriser = MeanEmbeddingVectorizer(word2vec=w2v_model)
    >>> feature = vectoriser.fit_transform(df["text"], None)
    """
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.dim = word2vec.vector_size

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in self.progressbar(X, prefix="Mean")
        ])

    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)

    def get_params(self, deep=True):
        return {"word2vec": self.word2vec}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

class TfidfEmbeddingVectorizer(EmbeddingVectorizer):
    """
    Parameters
    ----------
    word2vec: gensim.models.KeyedVectors()
        Word2Vec: https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz
        GloVe: https://nlp.stanford.edu/projects/glove/
        FastText: https://fasttext.cc/docs/en/crawl-vectors.html
    use_idf: boolean
        IDF stands for "Inverse Document Frequency", it is a measure of how much information
        the word provide.

    Examples
    --------
    >>> from gensim.scripts import glove2word2vec
    >>> from gensim.models import KeyedVectors
    >>> w2v_model = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)
    >>> glove2word2vec(glove_input_file=r"glove.840B.300d.txt", word2vec_output_file=r"gensim_glove_vectors.txt")
    >>> glove_model = KeyedVectors.load_word2vec_format("gensim_glove_vectors.txt", binary=False)
    >>> embedding_dict = KeyedVectors.load_word2vec_format(r"cc.en.300.vec", binary=False)
    >>> embedding_dict.save_word2vec_format(r"cc.en.300.bin", binary=True)
    >>> ft_model = KeyedVectors.load_word2vec_format("cc.en.300.bin", binary=True)
    >>> vectoriser = TfidfEmbeddingVectorizer(word2vec=w2v_model, use_idf=True)
    >>> feature = vectoriser.fit_transform(df["text"], None)
    """
    def __init__(self, word2vec, use_idf=True):
        self.word2vec = word2vec
        self.word2weight = None
        self.use_idf = use_idf
        self.dim = word2vec.vector_size

    def word2tf(self, term_list):
        term_freq = Counter(term_list)
        total_len = sum(term_freq.values())
        term_freq = [(term, term_freq[term]/total_len) for term, count in term_freq.items()]
        return dict(term_freq)

    def fit(self, X, y=None):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])
        return self

    def transform(self, X):
        transformed_X = []
        for doc in self.progressbar(X, prefix="TF-IDF"):
            weighted_array = []
            for term in doc:
                if term in self.word2vec:
                    if self.use_idf:
                        weighted_term = self.word2vec[term] * self.word2tf(doc)[term] * self.word2weight[term]
                    else:
                        weighted_term = self.word2vec[term] * self.word2tf(doc)[term]
                    weighted_array.append(weighted_term)
            weighted_array = np.mean(weighted_array or [np.zeros(self.dim)], axis=0)
            transformed_X.append(weighted_array)
        return np.array(transformed_X)

    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)

    def get_params(self, deep=True):
        return {"word2vec": self.word2vec, "use_idf": self.use_idf}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

class SifEmbeddingVectorizer(EmbeddingVectorizer):
    """
    Parameters
    ----------
    word2vec: gensim.models.KeyedVectors()
        Word2Vec: https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz
        GloVe: https://nlp.stanford.edu/projects/glove/
        FastText: https://fasttext.cc/docs/en/crawl-vectors.html
    smoothing_constant: float (default: 1e-3)
        Default value of smoothing constant suggested in the paper is 0.001.
        The range of a suggested in the paper: [1e−4, 1e−3]

    Examples
    --------
    >>> from gensim.scripts import glove2word2vec
    >>> from gensim.models import KeyedVectors
    >>> w2v_model = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)
    >>> glove2word2vec(glove_input_file=r"glove.840B.300d.txt", word2vec_output_file=r"gensim_glove_vectors.txt")
    >>> glove_model = KeyedVectors.load_word2vec_format("gensim_glove_vectors.txt", binary=False)
    >>> embedding_dict = KeyedVectors.load_word2vec_format(r"cc.en.300.vec", binary=False)
    >>> embedding_dict.save_word2vec_format(r"cc.en.300.bin", binary=True)
    >>> ft_model = KeyedVectors.load_word2vec_format("cc.en.300.bin", binary=True)
    >>> vectoriser = SifEmbeddingVectorizer(word2vec=w2v_model)
    >>> feature = vectoriser.fit_transform(df["text"], None)
    """
    def __init__(self, word2vec, smoothing_constant=1e-3):
        self.word2vec = word2vec
        self.word2weight = None
        self.dim = word2vec.vector_size
        self.smoothing_constant = smoothing_constant
        self.term_freq = None

    def fit(self, X, y=None):
        X_list = [item for sublist in X for item in sublist]
        term_freq = Counter(X_list)
        total_len = sum(term_freq.values())
        term_freq = [(term, term_freq[term]/total_len) for term, count in term_freq.items()]
        self.term_freq = dict(term_freq)
        return self

    def transform(self, X):
        transformed_X = []
        for doc in self.progressbar(X, prefix="SIF"):
            weighted_array = []
            for term in doc:
                if term in self.word2vec:
                    # Compute smooth inverse frequency (SIF)
                    weight = self.smoothing_constant / (self.smoothing_constant + self.term_freq.get(term, 0))
                    weighted_term = self.word2vec[term] * weight
                    weighted_array.append(weighted_term)
            weighted_array = np.mean(weighted_array or [np.zeros(self.dim)], axis=0)
            transformed_X.append(weighted_array)
        transformed_X = np.array(transformed_X)

        # Common component removal: remove the projections of the average vectors on their first singular vector
        svd = TruncatedSVD(n_components=1, n_iter=20, random_state=0)
        svd.fit(transformed_X)
        pc = svd.components_
        transformed_X = transformed_X - transformed_X.dot(pc.T).dot(pc)
        return transformed_X

    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)

    def get_params(self, deep=True):
        return {"word2vec": self.word2vec, "smoothing_constant": self.smoothing_constant}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self
