import dtale
import numpy as np
import pandas as pd
import pandas_profiling


def dataframe_repr_html_(
    df: pd.DataFrame,
    max_rows=None,
    max_cols=None,
    justify="left",
):
    if pd.get_option("display.notebook_repr_html"):
        if max_rows is None:
            max_rows = pd.get_option("display.max_rows")
        if max_cols is None:
            max_cols = pd.get_option("display.max_columns")
    pd.set_option("display.max_rows", 10)
    pd.set_option("display.max_columns", 50)

    return df.to_html(
        justify=justify,
        max_cols=max_cols,
        max_rows=max_rows,
        show_dimensions=True,
    )


def dataframe_view(df: pd.DataFrame, r=50, c=50):
    pd.set_option("display.max_rows", r)
    pd.set_option("display.max_columns", c)
    return df


def series__repr__(series: pd.Series, max_rows=None) -> str:
    if pd.get_option("display.notebook_repr_html"):
        if max_rows is None:
            max_rows = pd.get_option("display.max_rows")
    pd.set_option("display.max_rows", 10)
    pd.set_option("display.max_columns", 50)
    return series.to_string(
        name=True,
        length=True,
        dtype=True,
        max_rows=max_rows,
    )


def series_view(series: pd.Series, r=50):
    pd.set_option("display.max_rows", r)
    return series


def _style_base(df, r=50, c=50, na_rep="-"):
    if r > len(df):
        _df = df.iloc[:, :c].copy()
    else:
        _df = df.iloc[np.r_[0 : int(r / 2), -int(r / 2) : 0], :c].copy()
    _df_numeric = _df.select_dtypes(include=np.number)
    column_format = {k: "{:0,.2f}" for k in _df_numeric.columns}
    return _df.style.format(column_format, na_rep=na_rep)


def style_heatmap(df, r=50, c=50, na_rep="-", colormap="YlOrRd"):
    base = _style_base(df, r=r, c=c, na_rep=na_rep)
    return base.background_gradient(cmap=colormap)


def style_bar(df, r=50, c=50, na_rep="-", width=80, bar_color="#d65f5f"):
    base = _style_base(df, r=r, c=c, na_rep=na_rep)
    return base.bar(color=bar_color, align="left", width=width)


pd.DataFrame._repr_html_ = dataframe_repr_html_
pd.Series.__repr__ = series__repr__

pd.DataFrame.sh = style_heatmap
pd.DataFrame.sb = style_bar
pd.DataFrame.v = dataframe_view
pd.Series.v = series_view

pd.DataFrame.dt = dtale.show
pd.DataFrame.pp = pd.DataFrame.profile_report
