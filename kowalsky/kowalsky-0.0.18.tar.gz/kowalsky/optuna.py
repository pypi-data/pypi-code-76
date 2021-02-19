import optuna
import pandas as pd
from lightgbm import LGBMRegressor
from lightgbm import LGBMClassifier
from xgboost import XGBRegressor
from xgboost import XGBClassifier
from optuna.samplers import TPESampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import ExtraTreeRegressor
from sklearn.tree import ExtraTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from mlens.ensemble import SuperLearner
from sklearn.svm import SVR
from sklearn.svm import SVC
from catboost import CatBoostClassifier
from catboost import CatBoostRegressor
from .metrics import get_score_fn


def rf_params(trial):
    return {
        'min_samples_leaf': trial.suggest_int("min_samples_leaf", 1, 15),
        'min_samples_split': trial.suggest_uniform("min_samples_split", 0.05, 1.0),
        'n_estimators': trial.suggest_int("n_estimators", 2, 300),
        'max_depth': trial.suggest_int("max_depth", 2, 15),
        'random_state': 666
    }


def xgboost_params(trial):
    return {
        'learning_rate': trial.suggest_uniform("learning_rate", 0.0000001, 2),
        'n_estimators': trial.suggest_int("n_estimators", 2, 800),
        'max_depth': trial.suggest_int("max_depth", 2, 20),
        'gamma': trial.suggest_uniform('gamma', 0.0000001, 1),
        'random_state': 666
    }


def lgb_params(trial):
    return {
        'learning_rate': trial.suggest_uniform('learning_rate', 0.0000001, 1),
        'n_estimators': trial.suggest_int("n_estimators", 1, 800),
        'max_depth': trial.suggest_int("max_depth", 2, 25),
        'num_leaves': trial.suggest_int("num_leaves", 2, 3000),
        'min_child_samples': trial.suggest_int('min_child_samples', 3, 200),
        'random_state': 666
    }


def dt_params(trial):
    return {
        'max_depth': trial.suggest_int("max_depth", 2, 15),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
        'min_weight_fraction_leaf': trial.suggest_uniform('min_weight_fraction_leaf', 0.0, 0.5),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 15),
        'random_state': 666
    }


def et_params(trial):
    return {
        'min_samples_leaf': trial.suggest_int("min_samples_leaf", 1, 15),
        'min_samples_split': trial.suggest_uniform("min_samples_split", 0.05, 1.0),
        'max_depth': trial.suggest_int("max_depth", 2, 25),
        'random_state': 666
    }


def bagg_params(trial):
    return {
        'n_estimators': trial.suggest_int('n_estimators', 2, 300),
        'max_samples': trial.suggest_int('max_samples', 1, 200),
        'random_state': 666
    }


def kn_params(trial):
    return {
        'n_neighbors': trial.suggest_int("n_neighbors", 2, 100)
    }


def ada_params(trial):
    return {
        'n_estimators': trial.suggest_int("n_estimators", 2, 800),
        'learning_rate': trial.suggest_uniform('learning_rate', 0.0001, 1.0)
    }


def svm_params(trial):
    return {
        'kernel': trial.suggest_categorical('kernel', ['linear', 'poly', 'rbf', 'sigmoid']),
        'tol': trial.suggest_uniform('tol', 1e-5, 1),
        'C': trial.suggest_loguniform('C', 1e-10, 1e10)
    }


def cb_params(trial):
    return {
        'learning_rate': trial.suggest_uniform('learning_rate', 0.0001, 1.0),
        'depth': trial.suggest_int("max_depth", 2, 16)
    }


models = {

    # Gradient Boosts
    'XGBR': lambda trial: XGBRegressor(**xgboost_params(trial)),
    'XGBC': lambda trial: XGBClassifier(**xgboost_params(trial)),
    'LGBR': lambda trial: LGBMRegressor(**lgb_params(trial)),
    'LGBC': lambda trial: LGBMClassifier(**lgb_params(trial)),

    # Trees
    'RFR': lambda trial: RandomForestRegressor(**rf_params(trial)),
    'RFC': lambda trial: RandomForestClassifier(**rf_params(trial)),
    'DTR': lambda trial: DecisionTreeRegressor(**dt_params(trial)),
    'DTC': lambda trial: DecisionTreeClassifier(**dt_params(trial)),
    'ETR': lambda trial: ExtraTreeRegressor(**et_params(trial)),
    'ETC': lambda trial: ExtraTreeClassifier(**et_params(trial)),

    # Ensemble
    'BC': lambda trial: BaggingClassifier(**bagg_params(trial)),
    'BR': lambda trial: BaggingRegressor(**bagg_params(trial)),
    'ADAR': lambda trial: AdaBoostRegressor(**ada_params(trial)),
    'ADAC': lambda trial: AdaBoostClassifier(**ada_params(trial)),
    'CBR': lambda trial: CatBoostRegressor(**cb_params(trial)),
    'CBC': lambda trial: CatBoostClassifier(**cb_params(trial)),

    # KNeighbors
    'KNC': lambda trial: KNeighborsClassifier(**kn_params(trial)),
    'KNR': lambda trial: KNeighborsRegressor(**kn_params(trial)),

    # SVM
    'SVR': lambda trial: SVR(**svm_params(trial)),
    'SVC': lambda trial: SVC(**svm_params(trial)),
}


def optimize(model_name, path, scorer, y_label, trials=30, sampler=TPESampler(seed=666), direction='maximize'):
    ds = pd.read_csv(path)
    X_ds, y_ds = ds.drop(y_label, axis=1), ds[y_label]
    X_train, X_val, y_train, y_val = train_test_split(X_ds, y_ds)

    def objective(trial):
        model = models[model_name](trial)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        return get_score_fn(scorer)(y_val, preds)

    study = optuna.create_study(direction=direction, sampler=sampler)
    study.optimize(objective, n_trials=trials)
    return study.best_params


def create_super_learner(trial, models, head_models):
    selected_model_names = []
    n_models = trial.suggest_int('n_models', 1, min(6, len(models)))
    names = list(models.keys())
    for i in range(n_models):
        model_item = trial.suggest_categorical('model_{}'.format(i), names)
        if model_item not in selected_model_names:
            selected_model_names.append(model_item)

    folds = trial.suggest_int('folds', 2, 6)
    model = SuperLearner(folds=folds)

    selected_models = [models[item] for item in selected_model_names]
    model.add(selected_models)

    head_names = list(head_models.keys())
    head = trial.suggest_categorical('head', head_names)
    model.add_meta(head_models[head])
    print(f"Try: {selected_model_names}, {head}")
    return model


def optimize_super_learner(models, head_models, path, scorer, y_label, trials=30, sampler=TPESampler(seed=666),
                           direction='maximize'):
    ds = pd.read_csv(path)
    X_ds, y_ds = ds.drop(y_label, axis=1), ds[y_label]
    X_train, X_val, y_train, y_val = train_test_split(X_ds, y_ds)

    def objective(trial):
        model = create_super_learner(trial, models, head_models)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        return get_score_fn(scorer)(y_val, preds)

    study = optuna.create_study(direction=direction, sampler=sampler)
    study.optimize(objective, n_trials=trials, n_jobs=-1)
    return study.best_params
