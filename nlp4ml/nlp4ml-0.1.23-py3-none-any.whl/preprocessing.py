import re
import string
import warnings
import preprocessor
import numpy as np
import pandas as pd
import nlpaug.augmenter.word as naw
from sklearn import model_selection
from wordcloud import STOPWORDS
from gensim.parsing.preprocessing import remove_stopwords
warnings.filterwarnings("ignore")


from nlp4ml.utils import progressbar


class KFold:
    """
    Parameters
    ----------
    n_splits: int
    task: str {"regression", "classification"}

    Examples
    --------
    >>> splitter = KFold(n_splits=5)
    >>> dfx = splitter.split(dfx, target_col="label")
    """
    def __init__(self, n_splits, task="classification"):
        self.n_splits = n_splits
        self.task = task

    def split_df(self, df, target_col, shuffle=True):
        if self.task == "regression":
            df = self.create_folds_for_regression(df, target_col, shuffle=shuffle)
        elif self.task == "classification":
            df = self.create_folds_for_classification(df, target_col, shuffle=shuffle)
        return df

    def create_folds_for_regression(self, df, target_col, shuffle=True):
        df["kfold"] = -1
        if shuffle:
            df = df.sample(frac=1).reset_index(drop=True)
        num_bins = np.floor(1+np.log2(len(df)))
        df.loc[:, "bins"] = pd.cut(df[target_col], bins=num_bins, labels=False)
        kf = model_selection.StratifiedKFold(n_splits=self.n_splits)
        for f, (t_, v_) in enumerate(kf.split(X=df, y=df.bins.values)):
            df.loc[v_, 'kfold'] = f
        df = df.drop("bins", axis=1)
        return df

    def create_folds_for_classification(self, df, target_col, shuffle=True):
        df["kfold"] = -1
        if shuffle:
            df = df.sample(frac=1).reset_index(drop=True)
        y = df[target_col].values
        kf = model_selection.StratifiedKFold(n_splits=self.n_splits)
        for f, (t_, v_) in enumerate(kf.split(X=df, y=y)):
            df.loc[v_, 'kfold'] = f
        return df

    def split_X_y(self, X, y, shuffle=True):
        if self.task == "regression":
            df = self.create_X_y_folds_for_regression(X, y, shuffle=shuffle)
        elif self.task == "classification":
            df = self.create_X_y_folds_for_classification(X, y, shuffle=shuffle)
        return df

    def create_X_y_folds_for_regression(self, X, y, shuffle=True):
        col_names = [f"col_{i}" for i in range(X.shape[1])]
        X = pd.DataFrame(X, columns=col_names)
        y = pd.DataFrame(y, columns=["label"])
        df = pd.concat([X, y], axis=1)

        df["kfold"] = -1
        if shuffle:
            df = df.sample(frac=1).reset_index(drop=True)
        num_bins = np.floor(1+np.log2(len(df)))
        df.loc[:, "bins"] = pd.cut(y.label, bins=num_bins, labels=False)
        kf = model_selection.StratifiedKFold(n_splits=self.n_splits)
        for f, (t_, v_) in enumerate(kf.split(X=df, y=df.bins.values)):
            df.loc[v_, 'kfold'] = f
        df = df.drop("bins", axis=1)
        return df

    def create_X_y_folds_for_classification(self, X, y, shuffle=True):
        col_names = [f"col_{i}" for i in range(X.shape[1])]
        X = pd.DataFrame(X, columns=col_names)
        y = pd.DataFrame(y, columns=["label"])
        df = pd.concat([X, y], axis=1)

        df["kfold"] = -1
        if shuffle:
            df = df.sample(frac=1).reset_index(drop=True)
        kf = model_selection.StratifiedKFold(n_splits=self.n_splits)
        for f, (t_, v_) in enumerate(kf.split(X=df, y=y.label.values)):
            df.loc[v_, 'kfold'] = f
        return df


def augment_text(df, text_col, label_col, samples=300):
    aug = naw.SynonymAug(aug_src='wordnet')
    aug_text = []
    
    # Selecting the minority class samples
    df_minority = df[df[label_col]==1].reset_index(drop=True)

    # Data augmentation loop
    for i in progressbar(np.random.randint(0, len(df_minority), samples)):
        text = df_minority.iloc[i][text_col]
        augmented_text = aug.augment(text)
        aug_text.append(augmented_text)
    
    df_aug = pd.DataFrame({text_col: aug_text, label_col: 1})
    df = pd.concat([df, df_aug], axis=0)
    df = df.reset_index(drop=True)

    return df


def meta_feature(df, text_col):
    df.loc[:, 'word_count'] = df.loc[:, text_col].apply(lambda x: len(str(x).split()))
    df.loc[:, 'unique_word_count'] = df.loc[:, text_col].apply(lambda x: len(set(str(x).split())))
    df.loc[:, 'stop_word_count'] = df.loc[:, text_col].apply(lambda x: len([w for w in str(x).lower().split() if w in STOPWORDS]))
    df.loc[:, 'url_count'] = df.loc[:, text_col].apply(lambda x: len([w for w in str(x).lower().split() if 'http' in w or 'https' in w]))
    df.loc[:, 'mean_word_length'] = df.loc[:, text_col].apply(lambda x: np.mean([len(w) for w in str(x).split()]))
    df.loc[:, 'char_count'] = df.loc[:, text_col].apply(lambda x: len(str(x)))
    df.loc[:, 'punctuation_count'] = df.loc[:, text_col].apply(lambda x: len([c for c in str(x) if c in string.punctuation]))
    df.loc[:, 'hashtag_count'] = df.loc[:, text_col].apply(lambda x: len([c for c in str(x) if c == '#']))
    df.loc[:, 'mention_count'] = df.loc[:, text_col].apply(lambda x: len([c for c in str(x) if c == '@']))
    return df


def clean_tweet(tweet, strip_stopwords=False, strip_punctuation=False):
    """
    Parameters
    ----------
    tweet: str

    References
    ----------
    [1] https://www.kaggle.com/gunesevitan/nlp-with-disaster-tweets-eda-cleaning-and-bert
    """
    tweet = preprocessor.clean(tweet)

    # Contractions
    tweet = re.sub(r"he's", "he is", tweet)
    tweet = re.sub(r"there's", "there is", tweet)
    tweet = re.sub(r"We're", "We are", tweet)
    tweet = re.sub(r"That's", "That is", tweet)
    tweet = re.sub(r"won't", "will not", tweet)
    tweet = re.sub(r"they're", "they are", tweet)
    tweet = re.sub(r"Can't", "Cannot", tweet)
    tweet = re.sub(r"wasn't", "was not", tweet)
    tweet = re.sub(r"don\x89Ûªt", "do not", tweet)
    tweet = re.sub(r"aren't", "are not", tweet)
    tweet = re.sub(r"isn't", "is not", tweet)
    tweet = re.sub(r"What's", "What is", tweet)
    tweet = re.sub(r"haven't", "have not", tweet)
    tweet = re.sub(r"hasn't", "has not", tweet)
    tweet = re.sub(r"There's", "There is", tweet)
    tweet = re.sub(r"He's", "He is", tweet)
    tweet = re.sub(r"It's", "It is", tweet)
    tweet = re.sub(r"You're", "You are", tweet)
    tweet = re.sub(r"I'M", "I am", tweet)
    tweet = re.sub(r"shouldn't", "should not", tweet)
    tweet = re.sub(r"wouldn't", "would not", tweet)
    tweet = re.sub(r"i'm", "I am", tweet)
    tweet = re.sub(r"I\x89Ûªm", "I am", tweet)
    tweet = re.sub(r"I'm", "I am", tweet)
    tweet = re.sub(r"Isn't", "is not", tweet)
    tweet = re.sub(r"Here's", "Here is", tweet)
    tweet = re.sub(r"you've", "you have", tweet)
    tweet = re.sub(r"you\x89Ûªve", "you have", tweet)
    tweet = re.sub(r"we're", "we are", tweet)
    tweet = re.sub(r"what's", "what is", tweet)
    tweet = re.sub(r"couldn't", "could not", tweet)
    tweet = re.sub(r"we've", "we have", tweet)
    tweet = re.sub(r"it\x89Ûªs", "it is", tweet)
    tweet = re.sub(r"doesn\x89Ûªt", "does not", tweet)
    tweet = re.sub(r"It\x89Ûªs", "It is", tweet)
    tweet = re.sub(r"Here\x89Ûªs", "Here is", tweet)
    tweet = re.sub(r"who's", "who is", tweet)
    tweet = re.sub(r"I\x89Ûªve", "I have", tweet)
    tweet = re.sub(r"y'all", "you all", tweet)
    tweet = re.sub(r"can\x89Ûªt", "cannot", tweet)
    tweet = re.sub(r"would've", "would have", tweet)
    tweet = re.sub(r"it'll", "it will", tweet)
    tweet = re.sub(r"we'll", "we will", tweet)
    tweet = re.sub(r"wouldn\x89Ûªt", "would not", tweet)
    tweet = re.sub(r"We've", "We have", tweet)
    tweet = re.sub(r"he'll", "he will", tweet)
    tweet = re.sub(r"Y'all", "You all", tweet)
    tweet = re.sub(r"Weren't", "Were not", tweet)
    tweet = re.sub(r"Didn't", "Did not", tweet)
    tweet = re.sub(r"they'll", "they will", tweet)
    tweet = re.sub(r"they'd", "they would", tweet)
    tweet = re.sub(r"DON'T", "DO NOT", tweet)
    tweet = re.sub(r"That\x89Ûªs", "That is", tweet)
    tweet = re.sub(r"they've", "they have", tweet)
    tweet = re.sub(r"i'd", "I would", tweet)
    tweet = re.sub(r"should've", "should have", tweet)
    tweet = re.sub(r"You\x89Ûªre", "You are", tweet)
    tweet = re.sub(r"where's", "where is", tweet)
    tweet = re.sub(r"Don\x89Ûªt", "Do not", tweet)
    tweet = re.sub(r"we'd", "we would", tweet)
    tweet = re.sub(r"i'll", "I will", tweet)
    tweet = re.sub(r"weren't", "were not", tweet)
    tweet = re.sub(r"They're", "They are", tweet)
    tweet = re.sub(r"Can\x89Ûªt", "Cannot", tweet)
    tweet = re.sub(r"you\x89Ûªll", "you will", tweet)
    tweet = re.sub(r"I\x89Ûªd", "I would", tweet)
    tweet = re.sub(r"let's", "let us", tweet)
    tweet = re.sub(r"it's", "it is", tweet)
    tweet = re.sub(r"can't", "cannot", tweet)
    tweet = re.sub(r"don't", "do not", tweet)
    tweet = re.sub(r"you're", "you are", tweet)
    tweet = re.sub(r"i've", "I have", tweet)
    tweet = re.sub(r"that's", "that is", tweet)
    tweet = re.sub(r"i'll", "I will", tweet)
    tweet = re.sub(r"doesn't", "does not", tweet)
    tweet = re.sub(r"i'd", "I would", tweet)
    tweet = re.sub(r"didn't", "did not", tweet)
    tweet = re.sub(r"ain't", "am not", tweet)
    tweet = re.sub(r"you'll", "you will", tweet)
    tweet = re.sub(r"I've", "I have", tweet)
    tweet = re.sub(r"Don't", "do not", tweet)
    tweet = re.sub(r"I'll", "I will", tweet)
    tweet = re.sub(r"I'd", "I would", tweet)
    tweet = re.sub(r"Let's", "Let us", tweet)
    tweet = re.sub(r"you'd", "You would", tweet)
    tweet = re.sub(r"It's", "It is", tweet)
    tweet = re.sub(r"Ain't", "am not", tweet)
    tweet = re.sub(r"Haven't", "Have not", tweet)
    tweet = re.sub(r"Could've", "Could have", tweet)
    tweet = re.sub(r"youve", "you have", tweet)
    tweet = re.sub(r"donå«t", "do not", tweet)

    # Character entity references
    tweet = re.sub(r"&gt;", ">", tweet)
    tweet = re.sub(r"&lt;", "<", tweet)
    tweet = re.sub(r"&amp;", "&", tweet)

    # Typos, slang and informal abbreviations
    tweet = re.sub(r"w/e", "whatever", tweet)
    tweet = re.sub(r"w/", "with", tweet)
    tweet = re.sub(r"USAgov", "USA government", tweet)
    tweet = re.sub(r"recentlu", "recently", tweet)
    tweet = re.sub(r"Ph0tos", "Photos", tweet)
    tweet = re.sub(r"amirite", "am I right", tweet)
    tweet = re.sub(r"exp0sed", "exposed", tweet)
    tweet = re.sub(r"<3", "love", tweet)
    tweet = re.sub(r"lol", "laugh out loud", tweet)
    tweet = re.sub(r"amageddon", "armageddon", tweet)
    tweet = re.sub(r"Trfc", "Traffic", tweet)
    tweet = re.sub(r"8/5/2015", "2015-08-05", tweet)
    tweet = re.sub(r"WindStorm", "Wind Storm", tweet)
    tweet = re.sub(r"8/6/2015", "2015-08-06", tweet)
    tweet = re.sub(r"10:38PM", "10:38 PM", tweet)
    tweet = re.sub(r"10:30pm", "10:30 PM", tweet)
    tweet = re.sub(r"16yr", "16 year", tweet)
    tweet = re.sub(r"lmao", "laughing my ass off", tweet)
    tweet = re.sub(r"TRAUMATISED", "traumatized", tweet)

    # Urls
    tweet = re.sub(r"https?:\/\/t.co\/[A-Za-z0-9]+", "", tweet)

    # Words with punctuations and special characters
    punctuations = '@#!?+&*[]-%.:/();$=><|{}^' + "'`"
    for p in punctuations:
        tweet = tweet.replace(p, f' {p} ')

    # Remove stopwords
    if strip_stopwords:
        tweet = remove_stopwords(tweet)

    # Remove punctuation
    if strip_punctuation:
        tweet = re.sub(r'[^\w\s]', '', tweet)

    # Remove multiple spaces in a string
    tweet = re.sub(' +', ' ', tweet)
    tweet = tweet.strip()

    return tweet
