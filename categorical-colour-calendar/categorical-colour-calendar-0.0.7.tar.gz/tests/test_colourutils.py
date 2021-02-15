from datetime import datetime

import pandas as pd

from colourutils import get_n_colours, populate_colour_map

# https://matplotlib.org/gallery/color/named_colors.html
colours = [
    'w',  # base colors
    'tab:red',  # tableau palette
    'lime',  # css colors
    'xkcd:azure',  # xkcd colors
    (59 / 255, 22 / 255, 23 / 255),  # rgb
    '#f284ff',  # hex
    (255 / 255, 0 / 255, 255 / 255, 0.3),  # rgba
]

hex_output_expectation = {'w': '#ffffff', 'tab:red': '#d62728', 'lime': '#00ff00', 'xkcd:azure': '#069af3',
                          (0.23137254901960785, 0.08627450980392157, 0.09019607843137255): '#3b1617',
                          '#f284ff': '#f284ff',
                          (1.0, 0.0, 1.0, 0.3): '#ff00ff'}


def test_get_n_colours():
    for n in range(10):
        assert len(get_n_colours(n)) == n


def test_populate_colour_map():
    colour_map = {f'event_{i}': colours[i] for i in range(len(colours))}

    dates = pd.date_range(start='2021-01-01', periods=len(colour_map), freq='2D')
    s = pd.Series(colour_map.keys(), index=dates)
    s[datetime(2021, 1, 15)] = 'event_7'
    s[datetime(2021, 1, 17)] = 'event_8'

    new_colour_map, new_date_colour = populate_colour_map(s, colour_map, min_date=dates.min(), max_date=dates.max(),
                                                          strict_exclude=False,
                                                          date_colour=None)
    original_to_converted = {orig_col: new_colour_map[ev] for ev, orig_col in colour_map.items()}

    assert len(new_colour_map) == len(s)
    assert all([e in new_colour_map for e in ['event_7', 'event_8']])  # Assert colours generated for unmapped events
    assert new_date_colour is not None  # Assert new colour generated for default colour
    assert original_to_converted == hex_output_expectation  # Assert provided colours convert to correct hex values
    assert len(set(new_colour_map.values())) == len(new_colour_map)  # Assert colours are unique


def test_populate_colour_map_exclude():
    colour_map = {f'event_{i}': colours[i] for i in range(len(colours))}

    dates = pd.date_range(start='2021-01-01', periods=len(colour_map), freq='2D')
    s = pd.Series(colour_map.keys(), index=dates)
    s[datetime(2021, 1, 15)] = 'event_7'
    s[datetime(2021, 1, 17)] = 'event_8'

    new_colour_map, new_date_colour = populate_colour_map(s, colour_map, min_date=dates.min(), max_date=dates.max(),
                                                          strict_exclude=True,
                                                          date_colour=None)
    original_to_converted = {orig_col: new_colour_map[ev] for ev, orig_col in colour_map.items()}

    assert len(new_colour_map) == len(s) - 2  # events 7 and 8 are outside of max_date and strict_exclude is True
    assert 'event_7' not in new_colour_map
    assert 'event_8' not in new_colour_map
    assert new_date_colour is not None
    assert original_to_converted == hex_output_expectation


def test_populate_colour_map_no_new_date_colour():
    colour_map = {f'event_{i}': colours[i] for i in range(len(colours))}

    dates = pd.date_range(start='2021-01-01', periods=len(colour_map), freq='2D')
    s = pd.Series(colour_map.keys(), index=dates)
    s[datetime(2021, 1, 15)] = 'event_7'
    s[datetime(2021, 1, 17)] = 'event_8'

    new_colour_map, new_date_colour = populate_colour_map(s, colour_map, min_date=dates.min(), max_date=dates.max(),
                                                          strict_exclude=False,
                                                          date_colour='black')
    original_to_converted = {orig_col: new_colour_map[ev] for ev, orig_col in colour_map.items()}

    assert len(new_colour_map) == len(s)
    assert all([e in new_colour_map for e in ['event_7', 'event_8']])
    assert new_date_colour == '#000000'
    assert original_to_converted == hex_output_expectation
