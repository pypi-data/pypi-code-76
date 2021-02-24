# Imports
import numpy as np
from nonconformist.cp import IcpRegressor
from nonconformist.cp import IcpClassifier
from nonconformist.nc import NcFactory
from nonconformist.base import ClassifierAdapter
from nonconformist.nc import ClassifierNc
from nonconformist.base import RegressorAdapter
from nonconformist.nc import RegressorNc
from sklearn.base import is_classifier, is_regressor
import lightgbm as lgbm
from .adapter_classes import MyClassifierAdapter, MyRegressorAdapter, MyPreTrainedRegressorAdapter

# non sklearn adapter funtion
def NonConformistAdapter(model):
    r""" Function for adapting non Scikit Learn model so they can be used with nonconformist

    This funcitons adapts a lightgbm, xgboost or catboost `model` in order to use it
    with the nonconformist package and create confidence intervals. It's compatible
    with: LGBMRegressor (this model can be trained with the nonconformist fit method
    or it can be a pre-trained model loaded using lightgbm.Booster), LGBMClassifier, 
    XGBRegressor, XGBClassifier, CatBoostRegressor and CatBoostClassifier (these must
    trained with the nonconformist fit method).

    Parameters
    ----------
    model:
        Model we want to adapt in order to use it with nonconformist.

    Returns
    -------
    adapted_model: obj: MyClassifierAdapter, MyRegressorAdapter or MyPreTrainedRegressorAdapter
        The class of the adapted model so it can be used to create conformal prediction intervals.

    Raises
    ------
    ValueError
        The model isn't one of the specified classes.

    Examples:
    --------
    >>> model = lightgbm.LGBMRegressor()
    >>> adapted_model = NonConformistAdapter(model)
    """
    classifiers = ["LGBMClassifier", "XGBClassifier", "CatBoostClassifier"]
    regressors = ["LGBMRegressor","XGBRegressor", "CatBoostRegressor"]
    cbr_quant_50 = "Booster"
    if model.__class__.__name__ in classifiers:
        return MyClassifierAdapter(model)
    elif model.__class__.__name__ in regressors:
        return MyRegressorAdapter(model)
    elif model.__class__.__name__ == cbr_quant_50:
        return MyPreTrainedRegressorAdapter(model)
    else:
        raise ValueError(f"Model type should be {classifiers} for classifiers or {regressors} or {cbr_quant_50} for regressors")

# Adapter class
class Adapt_to_CP():
    r""" Class to adapt models so the produce predictions with confidence intervals

    This class transforms sklearn, lightgbm, xgboost and catboost models so they can 
    perform conformal prediction. In order to initiate this class the `model` must be
    given as an input. In adition to the `model`, a boolean variable `sklearn_model`
    must be given, indicating if the model belongs to scikit learn (True) or
    not (False).
    """

    def __init__(self, model, sklearn_model: bool):
        r"""__init__ method

        This method is used to adapt the input `model` so it can be used for creating 
        confidente intervals with conformal prediction.

        Parameters
        ----------
        model:
            Model we want to use as the underlying model to generate predictions and the
            confidence interval. This model can only be a scikit learn model, LGBMRegressor,
            LGBMClassifier, XGBRegressor, XGBClassifier, CatBoostRegressor or CatBoostClassifier.
        sklearn_model: bool
            This variable indicates if the model belongs to scikit learn or not.

        Returns
        -------
        cp: obj: Adapt_to_CP
            The class of the adapted model.

        Examples
        --------
        >>> model = lightgbm.LGBMRegressor()
        >>> cp = Adapt_to_CP(model)
        """
        self.model = model
        if sklearn_model:
            if is_classifier(model):
                self.icp = IcpClassifier(NcFactory.create_nc(model))
            elif is_regressor(model):
                self.icp = IcpRegressor(NcFactory.create_nc(model))
        else:
            model_adapter = NonConformistAdapter(model)
            if is_classifier(model):
                self.icp = IcpClassifier(ClassifierNc(model_adapter))
            elif is_regressor(model):
                self.icp = IcpRegressor(RegressorNc(model_adapter))
            elif model.__class__.__name__ == "Booster":
                self.icp = IcpRegressor(RegressorNc(model_adapter))

    def fit(self, x_train: np.ndarray, y_train: np.ndarray):
        r"""Method used to fit the underlying model

        In order to create the prediction and the confidence interval the underlying
        model must be fitted first. This fuction trains the model using the data features
        `x_train` and the target features `y_train`.

        Parameters
        ----------
        x_train: numpy.ndarray
            Array of data fetures the model will be trained with.
        y_train: numpy.ndarray
            Array of target features the model is trained to predict.

        Returns
        -------
        None
        """
        self.icp.fit(x_train, y_train)

    def calibrate(self, x_cal: np.ndarray, y_cal: np.ndarray):
        r"""Method used to calculate the nonconformity scores

        To create the confidence intervals we need a set of nonconformity scores,
        and, in classification cases, their probability distribution. This method
        uses the fitted underlying model and calculates de scores, thus calibrating
        the inductive conformal predictor.

        Parameters
        ----------
        x_cal: numpy.ndarray
            Array of data features used for calibrating the inductive conformal predictor.
        y_cal: numpy.ndarray
            Array of target features used for calibrating the inductive conformal predictor

        Returns
        -------
        None

        Notes
        -----
        It's very important to make sure the calibration data is different from the training data.
        """
        self.icp.calibrate(x_cal, y_cal)

    def predict(self, x_test: np.ndarray, confidence: float):
        r"""Method that returns the prediction and the confidence interval

        This method returns the interval with a confidence level of `confidence` and the target
        predictions for `x_test`. The information returned for classification is different from the
        one returned for regression. In classification cases the tuple returned has two elements: a
        numpy.ndarray with a matrix of boolean values and a numpy.ndarray that contains the class
        predictions. On the other hand, in regression cases the tuple returned has 3 elements: a numpy.ndarray
        with the lower bound values, a numpy.ndarray with the predicted target values and a numpy.ndarray
        with the upper bound values.

        Parameters
        ----------
        x_test: numpy.ndarray
            Array of data features used to predict the target values and the confidence interval
        confidence: float
            Float between 0 and 1 that represent the percentage of observations we want to be
            inside the predicted interval.

        Returns
        -------
        prediction: Tuple[numpy.ndarray, numpy.ndarray] or Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]
            Tuple containing the confidence interval and the target prediction

        Notes
        -----
        The `x_test` data must have the same features as the data used for training and calibration,
        and they must be in the same order.
        The level of confidence has to be a fraction between 0 and 1.
        """
        sig = 1 - confidence
        if is_classifier(self.model):
            return self.icp.predict(x_test, significance=sig), self.model.predict(x_test)
        elif is_regressor(self.model):
            return self.icp.predict(x_test, significance=sig)[:, 0], self.model.predict(x_test), self.icp.predict(x_test, significance=sig)[:, 1]
        elif type(self.model) == lgbm.basic.Booster:
            return self.icp.predict(x_test, significance=sig)[:, 0], self.model.predict(x_test), self.icp.predict(x_test, significance=sig)[:, 1]

    def calibrate_and_predict(self, x_cal: np.ndarray, y_cal: np.ndarray, x_test: np.ndarray, confidence: bool):
        r"""Method used for calibrating the conformal predictor and predicting target values and the confidence interval

        This method is equal to running the calibrate and the predict methods consecutively. 
        Accordingly, the inputs are the calibration data `x_cal` and targets `y_cal`, the test data `x_test` and the
        confidence level `confidence` desired for the predicted interval. The tuple returned contains
        the predicted values and the confidence interval.

        Parameters
        ----------
        x_cal: numpy.ndarray
            Array of data features used for calibrating the inductive conformal predictor.
        y_cal: numpy.ndarray
            Array of target features used for calibrating the inductive conformal predictor
        x_test: numpy.ndarray
            Array of data features used to predict the target values and the confidence interval
        confidence: float
            Float between 0 and 1 that represent the percentage of observations we want to be
            inside the predicted interval.

        Returns
        -------
        prediction: Tuple[numpy.ndarray, numpy.ndarray] or Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]
            Tuple containing the confidence interval and the target prediction

        Notes
        -----
        Both the calibration and the test data must have the same features (scale and order) as the data
        used for training the underlying model.
        The level of confidence has to be a decimal between 0 and 1.
        """
        sig = 1 - confidence
        self.icp.calibrate(x_cal, y_cal)
        if is_classifier(self.model):
            return self.icp.predict(x_test, significance=sig), self.model.predict(x_test)
        elif is_regressor(self.model):
            return self.icp.predict(x_test, significance=sig)[:, 0], self.model.predict(x_test), self.icp.predict(x_test, significance=sig)[:, 1]
        elif type(self.model) == lgbm.basic.Booster:
            return self.icp.predict(x_test, significance=sig)[:, 0], self.model.predict(x_test), self.icp.predict(x_test, significance=sig)[:, 1]
