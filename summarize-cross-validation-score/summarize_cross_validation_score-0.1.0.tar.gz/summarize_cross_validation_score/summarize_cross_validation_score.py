import pandas as pd
import numpy as np

def summarize_cv_scores(X, classifier_name):
    """
    This function summarizes the output of cross_validate function 
    from sklearn.model_selection and provides the mean and 
    standard deviation of all columns.

    Parameters
    ----------
    X : dict
        The output of cross_validate function from sklearn.model_selection.

    classifier_name : string
        Name of the classifier

    Examples
    --------
    Constructing toy example for X dictionary.

    >>> toy_score = {
        "fit_time": np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
        "score_time": np.array([1, 2, 3, 4, 5]),
        "test_accuracy": np.array([0.5, 0.5, 0.5, 0.5, 0.5]),
        "train_accuracy": np.array([0.5, 0.5, 0.5, 0.5, 0.5]),
        "test_f1": np.array([0.1, 0.1, 0.2, 0.1, 0.1]),
        "train_f1": np.array([0.1, 0.3, 0.1, 0.1, 0.1]),
    }
    
    Using the function
    
    >>> summarize_cv_scores(toy_score, "toy_test")
    """
    X_df = pd.DataFrame(X)
    col_names = (
        pd.Series(X_df.columns.tolist()).str.replace("test_", "validation_").tolist()
    )
    col_names = [f"{t}_{i}" for t in ["mean", "std"] for i in col_names]
    X_df = pd.DataFrame(pd.concat([X_df.mean(), X_df.std()])).T
    X_df.columns = col_names
    X_df["classifier_name"] = classifier_name
    col_names = ["classifier_name"] + col_names
    return X_df[col_names]
