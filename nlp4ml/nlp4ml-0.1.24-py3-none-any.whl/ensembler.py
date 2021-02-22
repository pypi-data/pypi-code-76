import numpy as np
import pandas as pd
from sklearn.tree import ExtraTreeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network.multilayer_perceptron import MLPClassifier
from sklearn.neighbors.classification import KNeighborsClassifier
from sklearn.linear_model.stochastic_gradient import SGDClassifier
from sklearn.linear_model.ridge import RidgeClassifier
from sklearn.linear_model.passive_aggressive import PassiveAggressiveClassifier
from sklearn.gaussian_process.gpc import GaussianProcessClassifier
from sklearn.ensemble.weight_boosting import AdaBoostClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from sklearn.ensemble.bagging import BaggingClassifier
from sklearn.ensemble.forest import ExtraTreesClassifier
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.semi_supervised import LabelPropagation
from sklearn.semi_supervised import LabelSpreading
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestCentroid
from sklearn.linear_model import Perceptron
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.svm import SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn import metrics
from collections import defaultdict
from functools import partial
from hyperopt import hp, fmin, tpe, Trials
from hyperopt.pyll.base import scope
from sklearn import model_selection
from sklearn import ensemble


from nlp4ml.preprocessing import KFold


class HyperOptimiser:
    """
    Parameters
    ----------
    param_space: dict
        Parameters distribution.
    X: np.array
        Feature matrix.
    y: np.array
        Labels
    n_splits: int
        The value for k-fold cross validation.
    scoring: str
        Optimise objective.

    Examples
    --------
    >>> param_space = {
            "n_estimators": scope.int(hp.quniform("n_estimators", 100, 1500, 1)), 
            "max_depth": scope.int(hp.quniform("max_depth", 1, 15, 1))
        }
    >>> optimiser = HyperOptimiser(param_space, X_train, y_train, n_splits=10)
    >>> optimiser.run()
    """
    def __init__(self, param_space, X, y, n_splits=5, scoring="accuracy"):
        self.param_space = param_space
        self.X = X
        self.y = y
        self.n_splits = n_splits
        self.scoring = scoring
        self.hopt = None

    def optimise(self, params, X, y):
        model = XGBClassifier(**params)
        splitter = model_selection.StratifiedKFold(n_splits=self.n_splits)
        accuracies, f1_scores = [], []
        for train_idx, valid_idx in splitter.split(X=X, y=y):
            X_train, y_train = X[train_idx], y[train_idx]
            X_valid, y_valid = X[valid_idx], y[valid_idx]
            model.fit(X_train, y_train, eval_metric='logloss')
            valid_prediction = model.predict(X_valid)
            fold_accuracy = metrics.accuracy_score(y_valid, valid_prediction)
            fold_f1_score = metrics.f1_score(y_valid, valid_prediction)
            accuracies.append(fold_accuracy)
            f1_scores.append(fold_f1_score)
        if self.scoring == "accuracy":
            return -1 * np.mean(accuracies)
        elif self.scoring == "f1":
            return -1 * np.mean(f1_scores)

    def run(self, num_evals=15):
        optimisation_function = partial(self.optimise, X=self.X, y=self.y)
        trials = Trials()
        self.hopt = fmin(
            fn=optimisation_function, 
            space=self.param_space, 
            algo=tpe.suggest, 
            max_evals=num_evals, 
            trials=trials
        )
        print(self.hopt)


def nested_cross_validation(model, 
                            space, 
                            df=None, 
                            X=None, y=None, 
                            inner_n_splits=3, 
                            outer_n_splits=5, 
                            mode="grid", 
                            scoring="accuracy"):
    """
    Parameters
    ----------
    model: estimator object
        This is assumed to implement the scikit-learn estimator interface.
    space: dict
        Parameters distribution dictionary.
    df: pd.DataFrame
        A pd.DataFrame contains features and label. 
        Target column should be named "label."
    inner_n_splits: int
        The value for the inner loop (for parameter search).
    outer_n_splits: int
        The value for the outer loop (for k-fold cross validation).
    mode: str {"grid", "random"}
        Utilise GridSearchCV() or RandomizedSearchCV()
    scoring: str {"accuracy", "balanced_accuracy", "f1", "roc_auc", ...}
        https://scikit-learn.org/stable/modules/model_evaluation.html

    Returns
    -------
    results: defaultdict

    Examples
    --------
    >>> # Case 1. if input is X and y
    >>> X, y = make_classification(n_features=2, n_clusters_per_class=1)
    >>> model = DecisionTreeClassifier()
    >>> space = {
            "max_depth": range(3, 5), 
            "min_samples_split": range(2, 4)
        }
    >>> results = nested_cross_validation(model, 
                                          space, 
                                          X, y, 
                                          inner_n_splits=5, 
                                          outer_n_splits=3)

    >>> # Case 2. if input is df, then the name of target column should be "label."
    >>> X, y = make_classification(n_features=2, n_clusters_per_class=1)
    >>> col_names = [f"col_{i}" for i in range(X.shape[1])]
    >>> X = pd.DataFrame(X, columns=col_names)
    >>> y = pd.DataFrame(y, columns=["label"])
    >>> df = pd.concat([X, y], axis=1)
    >>> model = DecisionTreeClassifier()
    >>> space = {
            "max_depth": range(3, 5), 
            "min_samples_split": range(2, 4)
        }
    >>> results = nested_cross_validation(model, 
                                          space, 
                                          X, y, 
                                          inner_n_splits=5, 
                                          outer_n_splits=3)  
    """
    results = defaultdict(list)
    target_col = "label"
    splitter = KFold(outer_n_splits, task="classification")
    if (X is None) and (y is None):
        df = splitter.split_df(df, target_col, shuffle=True)
    else:
        df = splitter.split_X_y(X, y, shuffle=True)

    for fold in range(outer_n_splits):
        df_train = df[df["kfold"]!=fold]
        df_valid = df[df["kfold"]==fold]
        X_train = df_train.loc[:, df_train.columns!=target_col]
        X_valid = df_valid.loc[:, df_valid.columns!=target_col]
        y_train = df_train.loc[:, df_train.columns==target_col]
        y_valid = df_valid.loc[:, df_valid.columns==target_col]

        assert isinstance(space, dict), "Space must be a dictionary!"
        if mode == "grid":
            search = GridSearchCV(model, 
                                  space, 
                                  scoring=scoring, 
                                  cv=inner_n_splits, 
                                  refit=True)
        elif mode == "random":
            search = RandomizedSearchCV(model, 
                                        space, 
                                        scoring=scoring, 
                                        cv=inner_n_splits, 
                                        refit=True)
        elif mode == "bayes":
            "Bayes mode has not been implemented yet..."

        result = search.fit(X_train, y_train)
        best_model = result.best_estimator_
        y_hat = best_model.predict(X_valid)

        acc = metrics.accuracy_score(y_valid, y_hat)
        f1 = metrics.f1_score(y_valid, y_hat)
        precision = metrics.precision_score(y_valid, y_hat)
        recall = metrics.recall_score(y_valid, y_hat)
        results["acc"].append(acc)
        results["f1"].append(f1)
        results["precision"].append(precision)
        results["recall"].append(recall)

        print("="*50)
        print(f"Fold {fold+1}")
        print("Accuracy={:.4f}\nF1={:.4f}\nPrecision={:.4f}\nRecall={:.4f}".format(
            acc, f1, precision, recall))
        print("Best Score={:.4f}\nParams={}".format(
            result.best_score_, result.best_params_))
        print("="*50)

    print('\nAccuracy: %.4f (±%.4f)' % (np.mean(results["acc"]), np.std(results["acc"])))
    return results


def fetch_models():
    models = dict()

    models["extra_tree"] = {}
    models["extra_tree"]["model"] = ExtraTreeClassifier()
    models["extra_tree"]["space"] = {
        'max_depth': range(3, 10),
        'min_samples_leaf': range(1, 10),
        'min_samples_split': range(2, 10)
    }

    models["decision_tree"] = {}
    models["decision_tree"]["model"] = DecisionTreeClassifier()
    models["decision_tree"]["space"] = {
        'max_depth': range(3, 10),
        'min_samples_split': range(2, 10), 
        'min_samples_leaf': range(1, 10),
        'criterion': ['gini', "entropy"]
    }

    models["mlp"] = {}
    models["mlp"]["model"] = MLPClassifier()
    models["mlp"]["space"] = {
        'hidden_layer_sizes': [(100, ), (200, ), (300, )],
        'momentum': np.arange(0.5, 1.0, 0.1), 
        'nesterovs_momentum': [True, False],
        'activation': ['logistic', "tanh", 'relu']
    }

    models["k_neighbors"] = {}
    models["k_neighbors"]["model"] = KNeighborsClassifier()
    models["k_neighbors"]["space"] = {
        'n_neighbors': range(5, 15),
        'leaf_size': range(30, 50), 
        'weights': ['uniform', 'distance'],
        'p': [1, 2]
    }

    models["sgd"] = {}
    models["sgd"]["model"] = SGDClassifier()
    models["sgd"]["space"] = {
        'alpha': np.arange(0.0001, 0.01, 0.001), 
        'penalty': ['l1', 'l2'], 
        'warm_start': [True, False]
    }

    models["ridge"] = {}
    models["ridge"]["model"] = RidgeClassifier()
    models["ridge"]["space"] = {
        'alpha': np.arange(0.1, 10.0, 0.2), 
        'normalize': [True, False]
    }

    models["passive_aggresive"] = {}
    models["passive_aggresive"]["model"] = PassiveAggressiveClassifier()
    models["passive_aggresive"]["space"] = {
        'C': np.arange(0.1, 10.0, 0.2), 
        'warm_start': [True, False]
    }

    models["gaussian_process"] = {}
    models["gaussian_process"]["model"] = GaussianProcessClassifier()
    models["gaussian_process"]["space"] = {
        'n_restarts_optimizer': range(0, 10), 
        'warm_start': [True, False]
    }

    models["adaboost"] = {}
    models["adaboost"]["model"] = AdaBoostClassifier()
    models["adaboost"]["space"] = {
        'n_estimators': range(100, 1000, 50), 
        'learning_rate': np.arange(0.01, 1.0, 0.01)
    }

    models["gradient_boosting"] = {}
    models["gradient_boosting"]["model"] = GradientBoostingClassifier()
    models["gradient_boosting"]["space"] = {
        'n_estimators': range(100, 1000, 50), 
        'learning_rate': np.arange(0.01, 1.0, 0.01), 
        'subsample': np.arange(0.1, 1.0, 0.1), 
        'min_samples_split': range(2, 5), 
        'min_samples_leaf': range(1, 10), 
        'max_depth': range(3, 15), 
        'ccp_alpha': np.arange(0.0, 1.0, 0.1), 
        'warm_start': [True, False]
    }

    models["bagging"] = {}
    models["bagging"]["model"] = BaggingClassifier()
    models["bagging"]["space"] = {
        'n_estimators': range(100, 1000, 50), 
        'max_samples': range(1, 10), 
        'warm_start': [True, False]
    }

    models["extra_trees"] = {}
    models["extra_trees"]["model"] = ExtraTreesClassifier()
    models["extra_trees"]["space"] = {
        'n_estimators': range(100, 1000, 50), 
        'max_depth': range(2, 15), 
        'min_samples_split': range(2, 10), 
        'min_samples_leaf': range(1, 15), 
        'ccp_alpha': np.arange(0.0, 1.0, 0.1), 
        'warm_start': [True, False]
    }

    models["random_forest"] = {}
    models["random_forest"]["model"] = RandomForestClassifier()
    models["random_forest"]["space"] = {
        'n_estimators': range(100, 1000, 50), 
        'max_depth': range(2, 15), 
        'min_samples_split': range(2, 10), 
        'min_samples_leaf': range(1, 15), 
        'ccp_alpha': np.arange(0.0, 1.0, 0.1), 
        'warm_start': [True, False]
    }

    models["bernoulli_nb"] = {}
    models["bernoulli_nb"]["model"] = BernoulliNB()
    models["bernoulli_nb"]["space"] = {
        'alpha': np.arange(0.1, 1.0), 
        'fit_prior': [True, False]
    }

    models["gaussian_nb"] = {}
    models["gaussian_nb"]["model"] = GaussianNB()
    models["gaussian_nb"]["space"] = {
        'var_smoothing': np.arange(1e-9, 1e-7)
    }

    models["label_propagation"] = {}
    models["label_propagation"]["model"] = LabelPropagation()
    models["label_propagation"]["space"] = {
        'kernel': ['knn', 'rbf'], 
        'gamma': range(10, 30), 
        'n_neighbors': range(5, 15)
    }

    models["label_spreading"] = {}
    models["label_spreading"]["model"] = LabelSpreading()
    models["label_spreading"]["space"] = {
        'kernel': ['knn', 'rbf'], 
        'gamma': range(10, 30), 
        'n_neighbors': range(5, 15), 
        'alpha': np.arange(0.1, 1.0, 0.1)
    }

    models["linear_discriminant_analysis"] = {}
    models["linear_discriminant_analysis"]["model"] = LinearDiscriminantAnalysis()
    models["linear_discriminant_analysis"]["space"] = {
        'solver': ['svd', 'lsqr', 'eigen']
    }

    models["linear_svc"] = {}
    models["linear_svc"]["model"] = LinearSVC()
    models["linear_svc"]["space"] = {
        'penalty': ['l1', 'l2'], 
        'C': np.arange(0.1, 1.5, 0.1)
    }

    models["logistic_regression"] = {}
    models["logistic_regression"]["model"] = LogisticRegression()
    models["logistic_regression"]["space"] = {
        'penalty': ['l1', 'l2'], 
        'C': np.arange(0.1, 1.5, 0.1), 
        'warm_start': [True, False]
    }

    models["nearest_centroid"] = {}
    models["nearest_centroid"]["model"] = NearestCentroid()
    models["nearest_centroid"]["space"] = {
        'shrink_threshold': np.arange(0.1, 1.0, 0.1)
    }

    models["perceptron"] = {}
    models["perceptron"]["model"] = Perceptron()
    models["perceptron"]["space"] = {
        'alpha': np.arange(0.0001, 1.0, 0.01), 
        'penalty': ['elasticnet', 'l2', 'l1'], 
        'warm_start': [True, False]
    }

    models["qda"] = {}
    models["qda"]["model"] = QuadraticDiscriminantAnalysis()
    models["qda"]["space"] = {
        'reg_param': np.arange(0.0001, 1.0, 0.01)
    }

    models["svc"] = {}
    models["svc"]["model"] = SVC()
    models["svc"]["space"] = {
        'C': np.arange(0.1, 1.0, 0.01)
    }

    models["xgboost"] = {}
    models["xgboost"]["model"] = XGBClassifier(verbosity=0)
    models["xgboost"]["space"] = {
        'n_estimators': range(50, 1000, 50), 
        'max_depth': range(3, 20), 
        'learning_rate': np.arange(0.001, 0.1, 0.01), 
        'subsample': np.arange(0.1, 1.0, 0.01), 
        'gamma': np.arange(0.0, 1.0, 0.005)
    }

    models["lgbm"] = {}
    models["lgbm"]["model"] = LGBMClassifier(silent=True)
    models["lgbm"]["space"] = {
        'n_estimators': range(50, 1000, 50), 
        'max_depth': range(3, 20), 
        'learning_rate': np.arange(0.001, 0.1, 0.01), 
        'num_leaves': range(32, 50), 
        'min_child_samples': range(20, 40), 
        'reg_alpha': np.arange(0.0, 1.0, 0.1), 
        'reg_lambda': np.arange(0.0, 1.0, 0.1)
    }

    models["catboost"] = {}
    models["catboost"]["model"] = CatBoostClassifier(verbose=0, allow_writing_files=False)
    models["catboost"]["space"] = {
        'n_estimators': range(50, 1000, 50), 
        'depth': range(3, 7), 
        'learning_rate': np.arange(0.001, 0.1, 0.01), 
        'l2_leaf_reg': range(1, 100, 5), 
        'border_count': range(5, 200, 10), 
        'bootstrap_type': ["Bernoulli"]
    }

    return models