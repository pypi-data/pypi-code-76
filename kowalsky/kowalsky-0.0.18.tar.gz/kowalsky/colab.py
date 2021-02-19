import pandas as pd


def csv(id):
    return pd.read_csv(path(id))


def path(id):
    return f'https://drive.google.com/uc?export=download&id={id}'
