from datetime import date, datetime
from itertools import permutations

import numpy as np
import pandas as pd
import pytest

from profiling.shap import (
    ShapExplainer,
    comb,
    fast_object_mode,
    n_choose_k,
    reduce_func,
    update_columns,
)


@pytest.mark.parametrize("n_cols", [1, 2, 3, 4])
def test_coalitions(n_cols):
    """Test construction of coalitions"""
    np.random.seed(1986)
    X = pd.DataFrame(np.random.normal(size=(1, n_cols)))

    def func(x):
        coef = np.ones(len(x))
        return x @ coef

    shap_explainer = ShapExplainer(func, X)
    coalitions = shap_explainer._sample_coalitions(len(X.columns))
    coalitions_expected = set(permutations([False, True] * (n_cols - 1), r=n_cols))
    assert coalitions == coalitions_expected


@pytest.mark.parametrize("coef", [[0], [1], [0.25, 0.5, 0, 0]])
def test_coefficient_recovery(coef):
    """Test that SHAP converges to coefficients in linear model"""
    np.random.seed(1986)
    X = pd.DataFrame(np.zeros(shape=(1, len(coef))))
    intercept = 5.23

    def func(X):
        return X.values @ coef + intercept

    shap_explainer = ShapExplainer(func, X)
    test_row = pd.DataFrame(np.ones((1, len(X.columns))), columns=X.columns)
    ref, shap = shap_explainer.explain(test_row)
    assert np.allclose(ref, intercept)  # reference
    assert np.allclose(shap, coef)  # shapley values
    assert np.allclose(ref + shap.sum(axis=1), func(test_row))  # bookkeeping


def test_large_df():
    """Test that SHAP runs smoothly on large dataframes"""
    np.random.seed(1986)
    n_col = 10
    n_row = 10000
    coef = np.random.randn(n_col)
    X = pd.DataFrame(np.zeros((n_row, n_col)))
    intercept = 5.23

    def func(X):
        return X.values @ coef + intercept

    shap_explainer = ShapExplainer(func, X)
    test_row = pd.DataFrame(np.ones((1, len(X.columns))), columns=X.columns)
    ref, shap = shap_explainer.explain(test_row)
    assert np.allclose(ref, intercept)  # reference
    assert np.allclose(shap, coef)  # shapley values
    assert np.allclose(ref + shap.sum(axis=1), func(test_row))  # bookkeeping


def test_batch():
    """Test that SHAP works in batch mode"""
    np.random.seed(1986)
    coef = [0.5, 0.5, 0, 0]
    X = pd.DataFrame(np.random.randn(10000, len(coef)))
    intercept = 5.23

    def func(X):
        return X.values @ coef + intercept

    shap_explainer = ShapExplainer(func, X)
    n_row = 10
    test_df = X.iloc[:n_row]
    ref, shap = shap_explainer.explain(test_df)
    assert isinstance(ref, pd.Series)
    assert isinstance(shap, pd.DataFrame)
    assert ref.shape == (n_row,)
    assert shap.shape == (n_row, len(coef))
    assert np.allclose(ref + shap.sum(axis=1), func(test_df))  # bookkeeping


def test_various_coltypes():
    # Generate test data
    X = pd.DataFrame.from_dict(
        {
            "Integer": [1, 2, 3],
            "Float": [None, 2.0, 3.0],
            "Object": [None, "", "c"],
            "Categorical": ["a", "b", "c"],
            "Date": [date(2020, 1, 1), date(2020, 1, 2), date(2020, 1, 3)],
            "Datetime": [datetime(2020, 1, 1), None, datetime(2020, 1, 3)],
        }
    )
    X = X.astype({"Categorical": "category"})

    def regression(x: pd.DataFrame) -> pd.Series:
        return pd.Series(np.random.uniform(size=len(x)))

    shap_explainer = ShapExplainer(func=regression, x=X)
    _, _ = shap_explainer.explain(X)


def test_fast_object_mode():
    """Test string mode calculation"""
    assert fast_object_mode(pd.Series([1, 2, 1])) == 1
    assert fast_object_mode(pd.Series([1.0, 2.0, 3.0])) == 1.0
    assert fast_object_mode(pd.Series([1.0, 1.0, None])) == 1.0
    assert fast_object_mode(pd.Series(["a", "a", None])) == "a"
    assert fast_object_mode(pd.Series([{"a": 1}, {"b": 1}, {"a": 1}])) == {"a": 1}
    assert fast_object_mode(pd.Series([["a"], ["a"], None])) == ["a"]
    assert fast_object_mode(pd.Series([["a"], ["a"], None], index=[5, 6, 7])) == ["a"]
    assert pd.isna(fast_object_mode(pd.Series([["a"], None, None])))


def test_comb():
    """Test n_choose_k and comb function"""
    assert n_choose_k(1, 1) == 1
    assert n_choose_k(2, 1) == 2
    assert n_choose_k(2, 2) == 1
    assert n_choose_k(4, 2) == 6
    assert n_choose_k(100, 50) == 100891344545564193334812497256
    assert np.array_equal(comb(3, np.array([1, 2, 3])), np.array([3, 3, 1]))


def test_background_data():
    data = pd.DataFrame(
        {
            "Float": [1, 2.1, 2.3],
            "Repeated Values": [1, 1, 1],
            "Float with Nones": [None, 1.0, None],
            "Object": ["a", "c", "c"],
            "Object with Nones": [None, None, "c"],
        }
    )

    expected = pd.DataFrame(
        {
            "Float": [2.1],
            "Repeated Values": [1],
            "Float with Nones": [1.0],
            "Object": ["c"],
            "Object with Nones": [None],
        }
    )

    result = ShapExplainer._create_background_data(data)
    assert result.equals(expected)


def test_mapping():
    X = pd.DataFrame.from_dict({"Integer": [1, 2, 2], "Categorical": ["a", "a", "b"]})
    X = X.astype({"Categorical": "category"})

    def regression(x):
        return pd.Series(np.random.uniform(size=len(x)))

    shap_explainer = ShapExplainer(func=regression, x=X)
    test_row = pd.DataFrame({"Integer": [5], "Categorical": ["d"]}).astype(X.dtypes)

    # full coalition
    coalition = {(True, True)}
    mapped_features = shap_explainer._map_features(coalition, test_row)
    expected = test_row
    assert mapped_features.equals(expected)

    # empty coalition
    coalition = {(False, False)}
    mapped_features = shap_explainer._map_features(coalition, test_row)
    expected = shap_explainer.x  # background dataset
    assert mapped_features.equals(expected)

    # mixed coalitions
    coalition = {(False, True)}
    mapped_features = shap_explainer._map_features(coalition, test_row)
    expected = pd.DataFrame({"Integer": [2], "Categorical": ["d"]}).astype(X.dtypes)
    assert mapped_features.equals(expected)

    coalition = {(True, False)}
    mapped_features = shap_explainer._map_features(coalition, test_row)
    expected = pd.DataFrame({"Integer": [5], "Categorical": ["a"]}).astype(X.dtypes)
    assert mapped_features.equals(expected)


def test_axioms():
    """Test Missingness, Local Accuracy, and Consistency properties of Shapley values"""
    np.random.seed(1986)
    n_col = 3
    X = pd.DataFrame(np.random.normal(size=(10000, n_col)))

    def func0(x):
        return x.loc[:, 0] * x.loc[:, 1] ** 2

    def func1(x):
        return x.loc[:, 0] * x.loc[:, 1] ** 2 + x.loc[:, 0].abs()

    explainer0 = ShapExplainer(func0, X)
    explainer1 = ShapExplainer(func1, X)

    test_row = pd.DataFrame(np.ones(shape=(1, n_col)))
    ref0, shap0 = explainer0.explain(test_row)
    ref1, shap1 = explainer1.explain(test_row)

    # missingness
    assert np.isclose(shap0[2], 0)
    assert np.isclose(shap1[2], 0)

    # local accuracy
    assert np.isclose(ref0 + np.sum(shap0, axis=1), func0(test_row))
    assert np.isclose(ref1 + np.sum(shap1, axis=1), func1(test_row))

    # consistency
    assert np.all(shap0[0] < shap1[0])
    assert np.all(shap0 < shap1 + 1e-9)


def test_profile_columns():
    """Test Shapley value calculation for a subset of columns"""
    np.random.seed(1986)
    n_col = 10
    n_row = 1000
    coef = np.random.randn(n_col)
    X = pd.DataFrame(np.zeros(shape=(n_row, n_col)))
    intercept = 5.23

    def func(x):
        return x.values @ coef + intercept

    profile_columns = X.columns[:-1]
    shap_explainer = ShapExplainer(func, X, profile_columns=profile_columns)
    test_row = pd.DataFrame(
        np.ones(shape=(1, len(profile_columns))), columns=profile_columns
    )
    ref, shap = shap_explainer.explain(test_row)
    assert np.allclose(ref, intercept)  # reference
    assert np.allclose(shap, coef[:-1])  # shapley values
    assert np.allclose(
        ref + shap.sum(axis=1), shap_explainer.func(test_row)
    )  # bookkeeping


def test_update_columns():
    # base case
    base = pd.DataFrame({"a": [1]})
    update = pd.DataFrame({"a": [2]})
    expected = pd.DataFrame({"a": [2]})
    result = update_columns(base, update)
    assert result.equals(expected)

    # broadcasting
    base = pd.DataFrame({"a": [1], "b": [True]})
    update = pd.DataFrame({"a": [2, 3]})
    expected = pd.DataFrame({"a": [2, 3], "b": [True, True]})
    result = update_columns(base, update)
    assert result.equals(expected)

    # index mismatch handled gracefully
    base = pd.DataFrame({"a": [1], "b": [True]}, index=[0])
    update = pd.DataFrame({"a": [2, 3]}, index=[1, 2])
    expected = pd.DataFrame({"a": [2, 3], "b": [True, True]}, index=[1, 2])
    result = update_columns(base, update)
    assert result.equals(expected)

    # column mismatch
    with pytest.raises(KeyError):
        base = pd.DataFrame({"a": [1]})
        update = pd.DataFrame({"b": [2, 3]})
        result = update_columns(base, update)


def test_reduce_func():
    X_orig = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    X_subset = X_orig.drop(columns=["a"])

    def predict(x: pd.DataFrame) -> pd.Series:
        assert list(x.columns) == ["a", "b"]
        return pd.Series([0] * len(x))

    with pytest.raises(AssertionError):
        predict(X_subset)

    predict_subset = reduce_func(func=predict, x=X_orig)
    pred = predict_subset(X_subset)
    pd.testing.assert_series_equal(pred, pd.Series([0, 0]))
