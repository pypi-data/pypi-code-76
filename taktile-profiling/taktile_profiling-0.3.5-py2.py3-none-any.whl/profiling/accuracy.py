from typing import Callable, List

import altair as alt
import numpy as np
import pandas as pd

from profiling.metrics import getloss
from profiling.utils import df_to_json_table


def metrics(
    func: Callable[[pd.DataFrame], pd.Series], x: pd.DataFrame, y: pd.Series, kind: str
) -> str:
    if kind == "regression":
        loss_list = ["Rmse", "Mae", "TrimmedRmse", "MeanPrediction", "MeanActual"]
    elif kind == "binary":
        loss_list = ["Accuracy", "AUC", "MeanPrediction", "MeanActual"]
    else:
        raise NotImplementedError(f"Unknown endpoint kind: {kind}")

    pred = func(x)
    losses = [getloss(ll) for ll in loss_list]
    loss_names = [loss.name for loss in losses]
    loss_values = [loss.metric(pred, y) for loss in losses]
    table = pd.DataFrame({"Metric": loss_names, "Value": loss_values})

    return df_to_json_table(table, date_format="iso", date_unit="s", double_precision=2)


def largest_errors(
    func: Callable[[pd.DataFrame], pd.Series],
    x: pd.DataFrame,
    y: pd.Series,
    profile_columns: List[str],
    n: int = 25,
) -> str:
    """Return observations with largest errors in predictions"""
    pred = func(x).to_numpy()

    df = (
        x[profile_columns]
        .assign(y=y, pred=pred)  # to numpy is needed to help time inference
        .astype({"y": float, "pred": float})  # account for boolean output/predictions
        .assign(Delta=lambda k: np.abs(k["y"] - k["pred"]))
    )

    df = df.sort_values("Delta", ascending=False).head(n)
    df = df.rename(columns={"pred": "Predicted Value", "y": "Actual Value"})

    # Move new columns to the beginning
    cols = df.columns.to_list()
    first = ["Predicted Value", "Actual Value", "Delta"]
    last = [c for c in cols if c not in first]
    df = df.reindex(columns=first + last)

    return df_to_json_table(df, date_format="iso", date_unit="s", double_precision=2)


def calibration(
    func: Callable[[pd.DataFrame], pd.Series],
    x: pd.DataFrame,
    y: pd.Series,
    bins: int = 10,
) -> alt.Chart:
    """Plot calibration"""
    preds = func(x).to_numpy()
    pred_grp = pd.qcut(preds, q=bins, duplicates="drop")

    df = pd.DataFrame(
        # conversion to numpy is required so booleans are handled correctly
        {"Actual Value": y.to_numpy(), "Predicted Value": preds, "Group": pred_grp}
    )
    df = df.groupby("Group").agg("mean").reset_index().drop(columns=["Group"])

    # Set aspect ratio to 1
    min_val = df[["Predicted Value", "Actual Value"]].min().min()
    max_val = df[["Predicted Value", "Actual Value"]].max().max()
    line_length = max_val - min_val
    domain = (min_val - 0.1 * line_length, max_val + 0.1 * line_length)
    df_diagonal = pd.DataFrame({"Predicted Value": domain, "Actual Value": domain})

    diagonal_line = (
        alt.Chart(df_diagonal)
        .mark_line(strokeDash=[1, 1])
        .encode(
            x=alt.X("Predicted Value:Q", scale=alt.Scale(domain=domain)),
            y=alt.Y("Actual Value:Q", scale=alt.Scale(domain=domain)),
        )
    )

    points = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Predicted Value:Q", scale=alt.Scale(domain=domain)),
            y=alt.Y("Actual Value:Q", scale=alt.Scale(domain=domain)),
            tooltip=[
                alt.Tooltip("Predicted Value:Q", format=".2f"),
                alt.Tooltip("Actual Value:Q", format=".2f"),
            ],
        )
        .interactive()
    )

    return diagonal_line + points
