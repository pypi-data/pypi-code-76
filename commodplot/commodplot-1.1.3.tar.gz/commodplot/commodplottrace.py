from commodutil import dates
from commodutil import transforms
from commodplot import commodplotutil as cpu
from commodplot import commodplottransform as cpt
import plotly.graph_objects as go
import pandas as pd
import numpy as np


default_line_col = 'khaki'
hist_hover_temp = '<i>%{text}</i>: %{y:.2f}'

# try to put deeper colours for recent years, lighter colours for older years
year_col_map = {
    -10: 'wheat',
    -9: 'burlywood',
    -8: 'steelblue',
    -7: 'aquamarine',
    -6: 'orange',
    -5: 'yellow',
    -4: 'saddlebrown',
    -3: 'mediumblue',
    -2: 'darkgreen',
    -1: 'coral',
    0: 'black',
    1: 'red',
    2: 'firebrick',
    3: 'darkred',
    4: 'crimson',
}


def get_year_line_col(year):
    """
    Given a year, calculate a consistent line colour across charts
    """
    delta = get_year_line_delta(year)
    return year_col_map.get(delta, default_line_col)


def line_visible(year):
    delta = get_year_line_delta(year)
    return None if -5 <= delta <= 3 else "legendonly"


def get_year_line_delta(year):
    if isinstance(year, str):
        year = int(year)

    delta = year - dates.curyear
    return delta


def get_year_line_width(year):
    delta = get_year_line_delta(year)
    if delta == 0:
        return 3

    return 2


def std_yr_col(df, asdict=False):
    """
    Given a dataframe with yearly columns, determine the line colour to use
    """

    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)

    yearmap = dates.find_year(df, use_delta=True)
    colmap = {}
    for colname, delta in yearmap.items():
        colmap[colname] = year_col_map.get(delta, default_line_col)

    if asdict:
        return colmap

    # return array of colours to use - this can be passed into cufflift iplot method
    return [colmap[x] for x in df]


def min_max_range(seas, shaded_range):
    """
    Calculate min and max for seas
    If an int eg 5, then do curyear -1 and curyear -6
    If list then do the years in that list eg 2012-2019
    :param seas:
    :param shaded_range:
    :return:
    """
    seas = seas.dropna(how='all', axis=1)
    seasf = seas.rename(columns=dates.find_year(seas))

    # only consider when we have full(er) data for a given range
    fulldata = pd.DataFrame(seasf.isna().sum()) # count non-na values
    if not (fulldata == 0).all().iloc[0]: # line below doesn't apple when we have full data for all columns
        fulldata = fulldata[fulldata.apply(lambda x: np.abs(x - x.mean()) / x.std() < 1.5).all(axis=1)] # filter columns with high emtply values
    seasf = seasf[fulldata.index] # use these column names only

    if isinstance(shaded_range, int):
        end_year = dates.curyear - 1
        start_year = end_year - (shaded_range - 1)
    else:
        start_year, end_year = shaded_range[0], shaded_range[1]

    r = seasf[[x for x in seasf.columns if x >= start_year and x <= end_year]]
    res = r.copy()
    res['min'] = res.min(1)
    res['max'] = res.max(1)
    res = res[['min', 'max']]

    if len(r.columns) >= 2:
        rangeyr = int(len(r.columns)) # end_year - start_year
    else:
        rangeyr = None
    return res, rangeyr


def shaded_range_traces(seas, shaded_range, showlegend=True):
    """
    Given a dataframe, calculate the min/max for every day of the year
    and return this as a trace for the min/max shaded area
    :param seas:
    :param shaded_range:
    :param showlegend:
    :return:
    """
    r, rangeyr = min_max_range(seas, shaded_range)
    if rangeyr is not None:
        traces = []
        max_trace = go.Scatter(x=r.index,
                               y=r['max'].values,
                               fill=None,
                               name='%syr Max' % rangeyr,
                               mode='lines',
                               line_color='lightsteelblue',
                               line_width=0.1,
                               showlegend=showlegend,
                               legendgroup='min')
        traces.append(max_trace)
        min_trace = go.Scatter(x=r.index,
                               y=r['min'].values,
                               fill='tonexty',
                               name='%syr Min' % rangeyr,
                               mode='lines',
                               line_color='lightsteelblue',
                               line_width=0.1,
                               showlegend=showlegend,
                               legendgroup='max')
        traces.append(min_trace)
    return traces


    traces = []
    for col in seas.columns:
        trace = go.Scatter(x=seas.index,
                           y=seas[col],
                           hoverinfo='y',
                           name=col,
                           hovertemplate=hist_hover_temp,
                           text=text,
                           visible=cptr.line_visible(col),
                           line=dict(color=cptr.get_year_line_col(col),
                                     dash=dash,
                                     width=cptr.get_year_line_width(col)),
                           showlegend=showlegend,
                           legendgroup=col)
        traces.append(trace)

    return traces


def timeseries_to_seas_trace(seas, text, dash=None, showlegend=True):
    """
    Given a dataframe of reindexed data, generate traces for every year
    :param seas:
    :param text:
    :param dash:
    :param showlegend:
    :return:
    """
    traces = []
    for col in seas.columns:
        trace = go.Scatter(x=seas.index,
                           y=seas[col],
                           hoverinfo='y',
                           name=col,
                           hovertemplate=hist_hover_temp,
                           text=text,
                           visible=line_visible(col),
                           line=dict(color=get_year_line_col(col),
                                     dash=dash,
                                     width=get_year_line_width(col)),
                           showlegend=showlegend,
                           legendgroup=col)
        traces.append(trace)

    return traces


def timeseries_to_reindex_year_trace(dft, text, dash=None, current_select_year=None, showlegend=True):
    traces = []
    colyearmap = cpu.dates.find_year(dft)

    for col in dft.columns:
        colyear = colyearmap[col]
        width = 1.2
        if current_select_year: # for current year+ makes lines bolder
            if isinstance(current_select_year, str):
                current_select_year = colyearmap[current_select_year]
            if colyear >= current_select_year:
                width = 2.2
        trace = go.Scatter(x=dft.index,
                           y=dft[col],
                           hoverinfo='y',
                           name=col,
                           hovertemplate=hist_hover_temp,
                           text=text,
                           visible=line_visible(colyear),
                           line=dict(color=get_year_line_col(colyear),
                                     dash=dash,
                                     width=width),
                           showlegend=showlegend,
                           legendgroup=col)
        traces.append(trace)

    return traces


def seas_plot_traces(df, fwd=None, **kwargs):
    """
    Generate traces for a timeseries that is being turned into a seasonal plot.
    Gererate yearlines for both historical and forward (if provided) and the shaded range
    :param df:
    :param fwd:
    :param kwargs:
    :return:
    """
    res = {}
    histfreq = kwargs.get('histfreq', None)
    if histfreq is None:
        histfreq = cpu.infer_freq(df)
    seas = cpt.seasonalise(df, histfreq=histfreq)

    text = seas.index.strftime('%b')
    if histfreq in ['B', 'D', 'W']:
        text = seas.index.strftime('%d-%b')

    showlegend = kwargs.get('showlegend', None)

    # shaded range
    shaded_range = kwargs.get('shaded_range', None)
    if shaded_range is not None:
        res['shaded_range'] = shaded_range_traces(seas, shaded_range, showlegend=showlegend)

    # historical / solid lines
    res['hist'] = timeseries_to_seas_trace(seas, text, showlegend=showlegend)

    # fwd / dotted lines
    if fwd is not None:
        fwdfreq = pd.infer_freq(fwd.index)
        # for charts which are daily, resample the forward curve into a daily series
        if histfreq in ['B', 'D'] and fwdfreq in ['MS', 'ME']:
            fwd = transforms.format_fwd(fwd, df.index[-1])  # only applies for forward curves
        fwdseas = cpt.seasonalise(fwd, histfreq=fwdfreq)

        res['fwd'] = timeseries_to_seas_trace(fwdseas, text, showlegend=showlegend, dash='dot')

    return res


def reindex_plot_traces(df, **kwargs):
    """
    Generate traces for a timeseries that is being turned into a reindex year plot.
    Gererate yearlines for both historical and the shaded range
    :param df:
    :param kwargs:
    :return:
    """
    res = {}
    showlegend = kwargs.get('showlegend', None)
    current_select_year = kwargs.get('current_select_year', None)

    text = df.index.strftime('%d-%b')

    shaded_range = kwargs.get('shaded_range', None)
    if shaded_range is not None:
        res['shaded_range'] = shaded_range_traces(df, shaded_range, showlegend=showlegend)

    # historical / solid lines
    res['hist'] = timeseries_to_reindex_year_trace(df, text, current_select_year=current_select_year, showlegend=showlegend)

    return res


