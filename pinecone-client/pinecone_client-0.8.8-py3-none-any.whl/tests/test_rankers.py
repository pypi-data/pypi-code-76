from pinecone.functions.ranker import Ranker
from pinecone.functions.ranker.cosine import CosineRanker
from pinecone.functions.ranker.dotproduct import DotProductRanker
from pinecone.functions.ranker.euclidean import EuclideanRanker

import numpy as np


def common_ranker_tests(ranker: Ranker):
    n = 10
    d = 50
    vectors = np.array([np.random.rand(d).astype(np.float32) for i in range(n)])
    query = np.array([np.random.rand(d).astype(np.float32)])

    """
    Ranker random vectors
    """
    scores = ranker.score(query, vectors, None)
    assert(len(scores)) == n

    """
    Rank identical vectors
    """
    for i in range(n):
        vectors[i] = query
    scores = ranker.score(query, vectors, None)
    assert all(np.abs(score - scores[0]) < 1E-3 for score in scores)

    """
    Rank single vector
    """
    scores = ranker.score(query, vectors[:1], None)
    assert(len(scores)) == 1

    """
    Rank with zero vector
    """
    vectors[0] = np.zeros(d).astype(np.float32)
    scores = ranker.score(query, vectors, None)
    assert(len(scores)) == n
    assert all(not np.isnan(score) for score in scores)

    """
    Rank zero query
    """
    query = np.array([np.zeros(d).astype(np.float32)])
    scores = ranker.score(query, vectors, None)
    assert(len(scores)) == n


def two_values_test(ranker: Ranker, a: int, b: int, d: int):
    n = 10
    vectors = np.array([a * np.ones(d).astype(np.float32) for i in range(n)])
    query = np.array([b * np.ones(d).astype(np.float32)])
    scores = ranker.score(query, vectors, None)
    assert all(np.abs(score - scores[0]) < 1E-2 for score in scores)
    return scores[0]


def test_cosine_ranker():
    ranker = CosineRanker()
    common_ranker_tests(ranker)
    assert two_values_test(ranker, 1, 2, 10) == 1
    assert two_values_test(ranker, 0, 1, 10) == 0



def test_euclidean_ranker():
    ranker = EuclideanRanker()
    common_ranker_tests(ranker)
    assert two_values_test(ranker, 2, 5, 10) == - 10 * (5-2)**2
    assert two_values_test(ranker, 0, 4, 10) == - 10 * (4**2)


def test_dot_product_ranker():
    ranker = DotProductRanker()
    common_ranker_tests(ranker)
    assert two_values_test(ranker, 2, 7, 10) == (2*7) * 10
    assert two_values_test(ranker, 0, 7, 10) == 0


if __name__ == '__main__':
    test_cosine_ranker()
    test_euclidean_ranker()
    test_dot_product_ranker()




