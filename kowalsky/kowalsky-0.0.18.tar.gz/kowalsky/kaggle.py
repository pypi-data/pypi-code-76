import pandas as pd


def make_sub(preds, path, sample_path, y_column):
    sub = pd.read_csv(sample_path)
    sub[y_column] = preds
    sub.to_csv(path, index=False)
