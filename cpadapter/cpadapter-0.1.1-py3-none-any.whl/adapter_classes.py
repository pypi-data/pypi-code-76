from nonconformist.base import ClassifierAdapter
from nonconformist.base import RegressorAdapter
import numpy as np

class MyClassifierAdapter(ClassifierAdapter):
    r"""Class to adapt classifiers to use them with the nonconformist package

    This class adapts the LGBMClassifier, XGBClassifier and CatBoostClassifier
    models, so they can be used with the nonconformist package. The model must
    be trained with the fit method.

    Examples
    --------
    >>> model = lightgbm.LGBMClassifier()
    >>> adapted_model = MyClassifierAdapter(model)
    """

    def __init__(self, model, fit_params=None):
        r""" __init__ method.

        This method is used for creating a MyClassifierAdapter object with
        a given `model`

        Parameters
        ----------
        model:
            Model we want to adapt to use with nonconformist.
        """
        super(MyClassifierAdapter, self).__init__(model, fit_params)

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        r""" Method for fitting the underlying model.

        This function adapts the fitting method so `model` can be used as
        an underlying model with the nonconformist package.

        Parameters
        ----------
        x: numpy.ndarray
            Array of features used to fit the model
        y: numpy.ndarray
            Array of target fetures used to fit the model

        Returns
        -------
        None
        """
        self.model.fit(x, y)

    def predict(self, x: np.ndarray):
        r"""Method for generating predictions from the underlying model

        This function adapts the predicting method so the `model`can be used as an
        underlying model with the nonconformist package.

        Parameters
        ----------
        x: numpy.ndarray
            Array of features used to predict the target feature

        Returns
        -------
        model.predict_proba: np.ndarray
            Array of predicted features
        """
        return self.model.predict_proba(x)

class MyRegressorAdapter(RegressorAdapter):
    r"""Class to adapt regressors to use them with the nonconformist package

    This class adapts the LGBMRegressor, XGBRegressor and CatBoostRegressor
    models, so they can be used with the nonconformist package. The model used
    must be trained with the fit method.

    """

    def __init__(self, model, fit_params=None):
        r""" __init__ method.

        This method is used for creating a MyRegressorAdapter object with
        a given `model`

        Parameters
        ----------
        model:
            Model we want to adapt to use with nonconformist.
        """
        super(MyRegressorAdapter, self).__init__(model, fit_params)

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        r""" Method for fitting the underlying model.

        This function adapts the fitting method so `model` can be used as
        an underlying model with the nonconformist package.

        Parameters
        ----------
        x: numpy.ndarray
            Array of features used to fit the model
        y: numpy.ndarray
            Array of target fetures used to fit the model

        Returns
        -------
        None
        """
        self.model.fit(x, y)

    def predict(self, x: np.ndarray):
        r"""Method for generating predictions from the underlying model

        This function adapts the predicting method so the `model`can be used as an
        underlying model with the nonconformist package.

        Parameters
        ----------
        x: numpy.ndarray
            Array of features used to predict the target feature

        Returns
        -------
        model.predict: np.ndarray
            Array of predicted features
        """
        return self.model.predict(x)

class MyPreTrainedRegressorAdapter(RegressorAdapter):
    r"""Class to adapt pre-trained regressors to use them with the nonconformist package

    This class adapts pre-trained LGBMRegressor models, which must be loaded with the
    lightgbm.Booster fuction.

    """

    def __init__(self, model, fit_params=None):
        r""" __init__ method.

        This method is used for creating a MyRegressorAdapter object with
        a given `model`

        Parameters
        ----------
        model:
            Pre-trained LGBMRegressor model we want to adapt to use with nonconformist.
        """
        super(MyRegressorAdapter, self).__init__(model, fit_params)

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        r""" Method for fitting the underlying model.

        This function adapts the fitting method so `model` can be used as
        an underlying model with the nonconformist package. In this case, since
        the model has been fitted, the method does nothing.

        Parameters
        ----------
        x: numpy.ndarray
            Array of features used to fit the model
        y: numpy.ndarray
            Array of target fetures used to fit the model

        Returns
        -------
        None
        """
        pass
    
    def predict(self, x: np.ndarray):
        r"""Method for generating predictions from the underlying model

        This function adapts the predicting method so the `model`can be used as an
        underlying model with the nonconformist package.

        Parameters
        ----------
        x: numpy.ndarray
            Array of features used to predict the target feature

        Returns
        -------
        model.predict: np.ndarray
            Array of predicted features
        """
        return self.model.predict(x)
