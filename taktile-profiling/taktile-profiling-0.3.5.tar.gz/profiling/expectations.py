from typing import Callable

import altair as alt
import numpy as np
import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

from profiling.utils import vega_sanitize


def condexp(
    func: Callable[[pd.DataFrame], pd.Series], x: pd.DataFrame, y: pd.Series, var: str
):
    """Plot conditional expectations"""
    if is_categorical_dtype(x[var]):
        return condexp_cat(func, x, y, var)
    elif is_bool_dtype(x[var]):
        return condexp_cat(func, x, y, var)
    elif is_object_dtype(x[var]):
        return condexp_cat(func, x, y, var)
    elif is_numeric_dtype(x[var]):
        return condexp_num(func, x, y, var)
    elif is_datetime64_any_dtype(x[var]):
        return condexp_datetime(func, x, y, var)
    else:
        pass


def condexp_num(
    func: Callable[[pd.DataFrame], pd.Series],
    x: pd.DataFrame,
    y: pd.Series,
    var: str,
    n_cut: int = 10,
) -> alt.Chart:
    """Conditional expectations plot for numerical variables"""

    non_missing = ~x[var].isna()
    x = x[non_missing]
    y = y[non_missing]
    pred = func(x).to_numpy()

    df = x.assign(pred=pred, y=y)
    if df[var].nunique() > n_cut:
        groupvar = df[var] + 1e-6 * np.random.uniform(size=len(df))
        df["groups"] = pd.qcut(groupvar, n_cut, duplicates="drop")
    else:
        df["groups"] = df[var]

    df_act = (
        df.groupby("groups")
        .agg({var: "mean", "y": "mean"})
        .assign(__taktile_profiling_value_type__="Actual Value")
        .rename(columns={"y": y.name})
    )

    df_pred = (
        df.groupby("groups")
        .agg({var: "mean", "pred": "mean"})
        .assign(__taktile_profiling_value_type__="Predicted Value")
        .rename(columns={"pred": y.name})
    )

    df = df_pred.append(df_act, ignore_index=True)

    # Create plot
    var_sanitized = vega_sanitize(var, datatype="Q")
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X(var_sanitized, scale=alt.Scale(zero=False)),
            y=alt.Y(y.name, scale=alt.Scale(zero=False)),
            color=alt.Color(
                "__taktile_profiling_value_type__:N", legend=alt.Legend(title="Type")
            ),
            tooltip=[
                alt.Tooltip("__taktile_profiling_value_type__:N", title="Type"),
                alt.Tooltip(var_sanitized, format=".2f"),
                alt.Tooltip(f"{y.name}:Q", format=".2f"),
            ],
        )
        .interactive()
    )

    return chart


def flatten_index(df):
    """Flatten hiearchical column index"""
    df.columns = df.columns.to_flat_index()
    return df


def condexp_cat(
    func: Callable[[pd.DataFrame], pd.Series],
    x: pd.DataFrame,
    y: pd.Series,
    var: str,
    n_max: int = 25,
) -> alt.Chart:
    """Conditional expectations plot for categorical variables"""
    pred = func(x)
    df = x.assign(pred=pred, y=y).astype({var: "category"})

    df_agg = (
        df.groupby(var, as_index=False, observed=True)
        .agg({"y": "mean", "pred": ["mean", "count"]})
        .pipe(flatten_index)
        .sort_values(("pred", "count"), ascending=False)
        .head(n_max)  # keep most frequent
        .sort_values(("pred", "mean"), ascending=False)
        .rename(
            columns={
                (var, ""): var,
                ("y", "mean"): "Actual Value",
                ("pred", "mean"): "Predicted Value",
                ("pred", "count"): "N",
            }
        )
    )

    df_agg[var] = df_agg[var].cat.remove_unused_categories()
    ordered_categories = list(df_agg[var].cat.categories)

    df_pred = df_agg.rename(columns={"Predicted Value": y.name}).assign(
        __taktile_profiling_value_type__="Predicted Value"
    )
    df_act = df_agg.rename(columns={"Actual Value": y.name}).assign(
        __taktile_profiling_value_type__="Actual Value"
    )

    # Create plot
    var_sanitized = vega_sanitize(var, datatype="N")

    chart_pred = (
        alt.Chart(df_pred)
        .mark_circle(opacity=0.9)
        .encode(
            x=alt.X(y.name, scale=alt.Scale(zero=False)),
            y=alt.Y(
                var_sanitized, sort=ordered_categories, scale=alt.Scale(zero=False),
            ),
            color=alt.Color(
                "__taktile_profiling_value_type__:N", legend=alt.Legend(title="Type")
            ),
            tooltip=[
                alt.Tooltip("__taktile_profiling_value_type__:N", title="Type"),
                var_sanitized,
                alt.Tooltip(f"{y.name}:Q", format=".2f"),
            ],
        )
        .interactive()
    )

    chart_act = (
        alt.Chart(df_act)
        .mark_circle(opacity=0.9)
        .encode(
            x=alt.X(y.name, scale=alt.Scale(zero=False)),
            y=alt.Y(var_sanitized, sort=ordered_categories),
            color=alt.Color(
                "__taktile_profiling_value_type__:N", legend=alt.Legend(title="Type")
            ),
            tooltip=[
                alt.Tooltip("__taktile_profiling_value_type__:N", title="Type"),
                var_sanitized,
                alt.Tooltip(f"{y.name}:Q", format=".2f"),
            ],
        )
        .interactive()
    )
    chart = chart_pred + chart_act

    return chart


def condexp_datetime(func, X, y, var, n_max=100):
    """Conditional expectations plot for datetime variables"""
    non_missing = ~X[var].isna()
    X = X[non_missing]
    y = y[non_missing]
    pred = func(X).to_numpy()

    df = X.assign(pred=pred, y=y)

    df_agg = (
        df.groupby(var, as_index=False, observed=True)
        .agg({"y": "mean", "pred": ["mean", "count"]})
        .pipe(flatten_index)
        .sort_values(("pred", "count"), ascending=False)
        .head(n_max)  # keep most frequent
        .rename(
            columns={
                (var, ""): var,
                ("y", "mean"): "Actual Value",
                ("pred", "mean"): "Predicted Value",
                ("pred", "count"): "N",
            }
        )
    )

    df_pred = df_agg.rename(columns={"Predicted Value": y.name}).assign(
        __taktile_profiling_value_type__="Predicted Value"
    )
    df_act = df_agg.rename(columns={"Actual Value": y.name}).assign(
        __taktile_profiling_value_type__="Actual Value"
    )

    df = df_pred.append(df_act, ignore_index=True)

    # Create plot
    var_sanitized = vega_sanitize(var, datatype="T")

    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=var_sanitized,
            y=alt.Y(y.name, scale=alt.Scale(zero=False)),
            color=alt.Color(
                "__taktile_profiling_value_type__:N", legend=alt.Legend(title="Type")
            ),
            tooltip=[
                alt.Tooltip("__taktile_profiling_value_type__:N", title="Type"),
                alt.Tooltip(var_sanitized, format=".2f"),
                alt.Tooltip(f"{y.name}:Q", format=".2f"),
            ],
        )
        .interactive()
    )

    return chart
