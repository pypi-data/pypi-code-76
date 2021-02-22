import swifter
import pandas as pd
import numpy as np
from pprint import pprint
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.datasets import make_classification
from gensim.models import KeyedVectors

from preprocessing import clean_tweet, augment_text, KFold
from ensembler import nested_cross_validation, fetch_models
from statistics import under_sampling
from vectoriser import SifEmbeddingVectorizer
from utils import seed_everything
seed_everything(seed=914)


def main():
    df = pd.read_csv("./data/train.csv")
    print(df)


if __name__ == "__main__":
    main()
