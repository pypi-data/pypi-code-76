import pandas as pd
import plotly.graph_objects as go
import plotly as pl
import base64
from commodutil import transforms
from commodutil import dates


# margin to use in HTML charts - make charts bigger but leave space for title
narrow_margin = {'l':2, 'r':2, 't':30, 'b':10}


def gen_title(df, **kwargs):
    title = kwargs.get('title', '')
    inc_change_sum = kwargs.get('inc_change_sum', True)
    if inc_change_sum:
        title = '{}   {}'.format(title, delta_summary_str(df))

    return title


def seas_table(hist, fwd=None):
    hist = hist.resample('MS').mean()

    if fwd is not None and fwd.index[0] == hist.index[-1]:
        hist = hist[:-1]
        df = pd.concat([hist, fwd], sort=False)
    else:
        df = hist

    df = transforms.seasonailse(df)

    summary = df.resample('Q').mean()
    winter = summary.iloc[[0, 3], :].mean()
    winter.name = 'Q1+Q4'
    summer = summary.iloc[[1, 2], :].mean()
    summer.name = 'Q2+Q3'
    summary.index = ['Q1', 'Q2', 'Q3', 'Q4']
    summary = summary.append(winter)
    summary = summary.append(summer)
    cal = df.resample('Y').mean().iloc[0]
    cal.name = 'Year'
    summary = summary.append(cal)
    summary = summary.round(2)

    df.index = df.index.strftime('%b')
    df = pd.concat([df, summary], sort=False).round(2)
    return df


def delta_summary_str(df):
    """
    Given a timeseries, produce a string which shows the latest change
    For example if T-1 value is 50 and T-2 is 45, return 50.00  △: +5
    """
    if isinstance(df, pd.DataFrame):
        df = pd.Series(df[df.columns[0]])

    df = df.dropna()
    val1 = df.iloc[-1]
    val2 = df.iloc[-2]
    delta = (val1-val2).round(2)
    symb = '+' if delta > 0.0 else ''

    s = '{}   △: {}{}'.format(val1.round(2), symb,delta)
    return s


def format_date_col(col, date_format='%d-%b'):
    """
    Format a column heading as a data
    :param col:
    :param date_format:
    :return:
    """
    try:
        if isinstance(col, str):

            col = pd.to_datetime(col).strftime(date_format)
        if isinstance(col, pd.Timestamp):
            col = col.strftime(date_format)
    except Exception:
        pass # ignore - just return original

    return col


def reindex_year_df_rel_col(df):
    """
    Given a reindexed year dataframe, figure out which column to use for change summary
    Basic algorithm is use current year, unless you are 10 days from end of dataframe
    :param df:
    :return:
    """
    res_col = df.columns[0]

    years = dates.find_year(df)
    last_val_date = df.index[-1]

    colyears = [x for x in df if str(dates.curyear) in str(x)]
    if len(colyears) > 0:
        res_col = colyears[0]
        relyear = (pd.to_datetime('{}-01-01'.format(years.get(res_col)))) # year of this column

        dft = df[colyears].dropna()
        if len(dft) > 0:
            relcol_date = df[res_col].dropna().index[-1] # last date of this column

            delta = last_val_date - relcol_date
            if delta.days < 10:
                relyear1 = (relyear + pd.DateOffset(years=1)).year
                relyear1 = [x for x in df.columns if str(relyear1) == str(x)]
                if len(relyear1) > 0:
                    return relyear1[0]
            else:
                return res_col

    return res_col


def infer_freq(df):
    histfreq = 'D' # sometimes infer_freq returns null - assume mostly will be a daily series
    if df is not None:
        histfreq = pd.infer_freq(df.index)

    return histfreq


def plhtml(fig, margin=narrow_margin, **kwargs):
    """
    Given a plotly figure, return it as a div
    """
    # if 'margin' in kwargs:
    if fig is not None:
        fig.update_layout(margin=margin)

        fig.update_xaxes(automargin=True)
        fig.update_yaxes(automargin=True)
        return pl.offline.plot(fig, include_plotlyjs=False, output_type='div')

    return ''


def convert_dict_plotly_fig_html_div(d):
    """
    Given a dict (that might be passed to jinja), convert all plotly figures of html divs
    """
    for k, v in d.items():
        if isinstance(d[k], go.Figure):
            d[k] = plhtml(d[k])
        if isinstance(d[k], dict):
            convert_dict_plotly_fig_html_div(d[k])

    return d


def plpng(fig):
    """
    Given a plotly figure, return it as a png
    """
    image = base64.b64encode(pl.io.to_image(fig)).decode("ascii")
    res = '<img src="data:image/png;base64,{image}">'.format(image=image)

    return res


def convert_dict_plotly_fig_png(d):
    """
    Given a dict (that might be passed to jinja), convert all plotly figures png
    """
    for k, v in d.items():
        if isinstance(d[k], go.Figure):
            d[k] = plpng(d[k])
        if isinstance(d[k], dict):
            convert_dict_plotly_fig_png(d[k])

    return d


def jinja_finalize(value):
    """
    Finalize for jinja which makes empty entries show as blank rather than none
    and converts plotly charts to html divs
    :param value:
    :return:
    """
    if value is None:
        return ''
    if isinstance(value, go.Figure):
        return plhtml(value)

    return value
