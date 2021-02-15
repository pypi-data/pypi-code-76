import calendar
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import math

from colourutils import populate_colour_map
from dateutils import count_months, get_week_of_month

__scale = 20


def _num_to_day(num):
    # Midpoint of a polygon is at n - scale/4
    # Divide this by scale to find out how many days along we are
    return (num - (__scale / 4)) / __scale


def _day_to_num(day):
    # Inverse of num_to_day
    return (day * __scale) + (__scale / 4)


def _get_date_square_coordinates(day_of_week, week_of_month):
    x_start = __scale * day_of_week
    x_end = (__scale * day_of_week) + (__scale / 2)
    y_start = __scale * week_of_month
    y_end = (__scale * week_of_month) + (__scale / 2)

    bottom_left = (x_start, y_start)
    top_left = (x_start, y_end)
    top_right = (x_end, y_end)
    bottom_right = (x_end, y_start)

    centre = (((x_start + x_end) / 2), ((y_start + y_end) / 2))

    return [bottom_left, top_left, top_right, bottom_right], centre


def _draw_date_square(square_date, data, ax, text_colour):
    day_of_week = square_date.weekday()
    week_of_month = get_week_of_month(square_date)

    corners, centre = _get_date_square_coordinates(day_of_week, week_of_month)

    shape = plt.Polygon(corners, color=data[square_date])
    ax.add_patch(shape)
    ax.annotate(str(square_date.day), centre, color=text_colour, weight='bold', fontsize=__scale * 0.75, ha='center', va='center')


def _setup_weekday_axis(ax):
    secax = ax.secondary_xaxis('top', functions=(_num_to_day, _day_to_num))
    secax.set_xticks(range(7))
    secax.set_xticklabels(['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'], fontsize=__scale)


def draw_month_calendar(data, year, month, ax, text_colour):
    """
    Draw a calendar for a given year-month on a given axis, using a provided Series of dates and colours.

    :param data: A Series which must contain a colour value for every date in the month.
    :param year: The year (YYYY).
    :param month: The month (MM).
    :param ax: The axis to plot on.
    :param text_colour: The text colour for the date numbers.
    :return: None
    """
    month_start_day, month_num_days = calendar.monthrange(year, month)
    for day in range(1, month_num_days+1):
        current_date = datetime(year, month, day)
        _draw_date_square(current_date, data, ax, text_colour)

    _setup_weekday_axis(ax)
    ax.axis('scaled')
    ax.set_title(calendar.month_name[month] + ' ' + str(year), pad=20, fontsize=__scale)
    ax.axis('off')
    ax.plot()


def _apply_colours(data, colour_map, date_colour, exclude_colour, strict_exclude, min_date, max_date):
    data = data.map(colour_map)  # Convert event values to colours

    # Apply the exclude_colour to dates outside the date ranges
    strict_exclude = strict_exclude | pd.isna(data)  # Whether to exclude events that fall out of date range
    if max_date is not None:
        data.loc[(data.index < min_date) & strict_exclude] = exclude_colour
    if min_date is not None:
        data.loc[(data.index > max_date) & strict_exclude] = exclude_colour

    data = data.fillna(date_colour)  # Fill remaining na values with default square colour
    return data


def _extend_data(data, first_date, last_date):
    first_month_start = datetime(first_date.year, first_date.month, 1)
    _, max_day = calendar.monthrange(last_date.year, last_date.month)
    last_month_end = datetime(last_date.year, last_date.month, max_day)
    if first_month_start not in data:
        data[first_month_start] = None
    if last_month_end not in data.index:
        data[last_month_end] = None
    data = data.sort_index().asfreq('D')
    return data


def _draw_legend(fig, colour_map):
    markers = [plt.Line2D([0,0], [0,0], color=c, marker='o', linestyle='') for c in colour_map.values()]
    fig.legend(markers, colour_map.keys(), numpoints=1, markerscale=__scale/3, fontsize=__scale*2, loc='lower center',
               bbox_to_anchor=(0, -0.1, 1, 1), bbox_transform=fig.transFigure, ncol=int(math.sqrt(len(colour_map))))


def draw_colour_calendar(data,
                         colour_map=None,
                         generate_colours=True,
                         months_per_row=3,
                         date_colour=None,
                         text_colour='w',
                         exclude_colour='grey',
                         strict_exclude=False,
                         min_date=None,
                         max_date=None,
                         legend=True):
    """
    Draw monthly calendar(s) with dates from the provided data highlighted as distinct events. Optional parameters
    control the appearance of the resultant figure.

    :param data: A Series of events with a datetime index.
    :param colour_map: A dictionary mapping events to colours.
    :param generate_colours: Whether to generate colours for events which don't have a mapping provided in
        colour_map.
    :param months_per_row: When displaying more than one month, how many to fit per row.
    :param date_colour: The default colour for a date square with no events. If not specified, a colour will be
        generated in the same spectrum as those for missing events.
    :param text_colour: The colour for the date numbers on the date squares.
    :param exclude_colour: The colour to shade dates which fall outside of min_date or max_date.
    :param strict_exclude: Whether to exclude events which fall outside of min_date or max_date.
    :param min_date: Dates before the min_date are coloured with the exclude_colour.
    :param max_date: Dates after the max_date are coloured with the exclude_colour.
    :param legend: Whether to display the event-to-colour legend.
    :return: The Matplotlib fig and axes array.
    """
    data.index = pd.to_datetime(data.index)

    min_date = pd.to_datetime(min_date)
    max_date = pd.to_datetime(max_date)

    if colour_map is None:
        colour_map = {}
    if generate_colours:
        colour_map, date_colour = populate_colour_map(data, colour_map, min_date, max_date, strict_exclude, date_colour)

    first_date = data.index.min()
    last_date = data.index.max()
    data = _extend_data(data, first_date, last_date)

    data = _apply_colours(data, colour_map, date_colour, exclude_colour, strict_exclude, min_date, max_date)

    num_months = count_months(first_date, last_date)

    fig, axs = plt.subplots(math.ceil(num_months/months_per_row), min(num_months, months_per_row), sharex=True, sharey=True, squeeze=False)

    total_axs = len(axs) * len(axs[0])
    unused_axs = total_axs - num_months
    for u in range(unused_axs):
        axs[len(axs)-1][(months_per_row-1)-u].remove()

    month_counter = 0
    for year in range(first_date.year, last_date.year + 1):
        start_month = 1
        end_month = 12
        if year == first_date.year:
            start_month = first_date.month
        if year == last_date.year:
            end_month = last_date.month

        for month in range(start_month, end_month+1):
            axs_x = int(month_counter / months_per_row)
            axs_y = month_counter % months_per_row
            draw_month_calendar(data, year, month, axs[axs_x][axs_y], text_colour)
            month_counter = month_counter + 1

    axs[0][0].invert_yaxis()

    fig.set_size_inches(10*min(num_months, months_per_row), 10*len(axs))
    if legend:
        _draw_legend(fig, colour_map)
    fig.set_dpi(200)
    fig.tight_layout()
    plt.show()
    return fig, axs
