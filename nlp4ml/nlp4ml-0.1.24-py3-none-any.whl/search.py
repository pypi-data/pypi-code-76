import time
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from utils import seed_everything
seed_everything()


def hyperparameters(model,
                    space,
                    X,
                    y,
                    n_iter,
                    kfold,
                    shuffle=False,
                    refit=True,
                    n_jobs=-1,
                    scoring='f1'):
    start = time.time()
    cv = StratifiedKFold(n_splits=kfold, shuffle=shuffle)
    opt = RandomizedSearchCV(model,
                             param_distributions=space,
                             n_iter=n_iter,
                             cv=cv,
                             n_jobs=n_jobs,
                             refit=refit,
                             scoring=scoring)
    opt.fit(X, y)
    end = time.time()
    scores = cross_val_score(opt, X, y, cv=cv, scoring=scoring)

    print("Elapsed: {}".format(time.strftime("%H:%M:%S", time.gmtime(end-start))))
    print("-"*50)
    print("Cross Validation MEAN: {}".format(scores.mean()))
    print("Cross Validation STD: {}".format(scores.std()))
    print("Best Score: {}".format(opt.best_score_))
    print("Best Parameters: {}".format(opt.best_params_))

    return opt.best_params_
