# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Test - Widget Sample, all the widgets, configured for keyboard grid.
"""

import pygame

from colors import (WHITE, MEDIUM_GRAY, BLUE, RED, BLACK, DARK_RED, GREEN,
                    CYAN, MAGENTA)
from page import Page
from tests._utilities import fake_data_graph_function
from widget_buttons import Button, ButtonGroup
from widget_controls import Dial, Slider
from widget_displays import Indicator, Label, Graph

_boop_count = 4

_up_down_flag = 0

_max_track_samples = 1000
_last_track_update = pygame.time.get_ticks()
_track_1_data = []
_track_2_data = []
_track_3_data = []
_dial_value = 50
_slider_h_value = 40
_slider_v_value = 60


# =========================================================
# Hold-behavior buttons and indicator
# =========================================================

def _up_dn_button_func(button, pushed):
    global _up_down_flag
    direction = button._direction
    if pushed:
        _up_down_flag = direction
    else:
        _up_down_flag = 0


def _up_dn_indicator_func(indicator):
    global _up_down_flag
    if _up_down_flag == 0:
        return False, ''
    elif _up_down_flag == 1:
        return True, "UP"
    else:
        return True, "DN"


_up_button = Button((115, 105), (60, 50),
                    label="^",
                    behavior=Button.HOLD,
                    style=Button.OBROUND,
                    function=_up_dn_button_func)
_up_button._direction = 1

_up_dn_indicator = Indicator((115, 160), (60, 50),
                             label_color2=WHITE,
                             function=_up_dn_indicator_func)

_dn_button = Button((115, 215), (60, 50),
                    label="v",
                    behavior=Button.HOLD,
                    style=Button.OBROUND,
                    function=_up_dn_button_func)
_dn_button._direction = -1


# =========================================================
# Rounded Button styles
# =========================================================
def go_to_page_entry(button, state):
    from tests.test_pages.pages import get_pages
    from tests._utilities import go_to_page
    return go_to_page(get_pages(), 'entry')


_back_button = Button((110, 400), (75, 50),
                      label="Back",
                      style=Button.LEFT_ROUND,
                      function=go_to_page_entry)

_do_nothing_button = Button((190, 400), (150, 50),
                            label="Do Nothing",
                            style=Button.RECTANGLE,
                            color1=MEDIUM_GRAY, color2=WHITE,
                            label_color1=BLUE, label_color2=RED)


def go_to_page_poweroff(button, state):
    from tests.test_pages.pages import get_pages
    from tests._utilities import go_to_page
    return go_to_page(get_pages(), 'power_off')


_next_button = Button((345, 400), (75, 50),
                      label="Next",
                      style=Button.RIGHT_ROUND,
                      function=go_to_page_poweroff)


# ---- Boop button, for some amusement

def _boop_button_func(button, pushed):
    global _boop_count
    _boop_count -= 1
    return None


def _boop_indicator_func(indicator):
    """ Countdown; when we reach 0, we exit the program.
    """
    if _boop_count == 4:
        return False, ''
    if _boop_count == 0:
        exit(0)
    return True, f"{_boop_count}"


_boop_button = Button((430, 400), (50, 50),
                      label="X",
                      style=Button.OBROUND,
                      function=_boop_button_func)

_boop_indicator = Indicator((485, 400), (50, 50),
                            color1=BLACK, color2=RED,
                            label_color1=WHITE, label_color2=BLACK,
                            function=_boop_indicator_func)


# =========================================================
# Toggle-behavior Buttons with reset
# =========================================================

def _reset_count_buttons(button, pressed):
    _one_button.clear()
    _two_button.clear()
    _three_button.clear()


_count_buttons_label = Label((190, 105), (100, 25),
                             label="Pick Several")
_one_button = Button((190, 130), (100, 50),
                     label="One",
                     behavior=Button.TOGGLE)
_two_button = Button((190, 185), (100, 50),
                     label="Two",
                     behavior=Button.TOGGLE)
_three_button = Button((190, 240), (100, 50),
                       label="Three",
                       behavior=Button.TOGGLE)
_count_reset_button = Button((190, 295), (100, 50),
                             label='RESET',
                             label_color1=DARK_RED,
                             function=_reset_count_buttons)

# =========================================================
# Button Group
# =========================================================

_color_buttons_label = Label((300, 105), (100, 25),
                             label="Pick One")

_red_button = Button((300, 130), (100, 50),
                     label="Red",
                     color2=RED,
                     behavior=Button.TOGGLE)
_green_button = Button((300, 185), (100, 50),
                       label="Green",
                       color2=GREEN,
                       behavior=Button.TOGGLE)
_blue_button = Button((300, 240), (100, 50), label="Blue",
                      color2=BLUE,
                      behavior=Button.TOGGLE)

_color_group = ButtonGroup([_red_button, _green_button, _blue_button])


# =========================================================
# Controls and Graphs
# =========================================================

# ---- Graph and Control Functions

def _dial_control_func(dial, value):
    global _dial_value
    _dial_value = value


def _slider_h_control_func(slider, value):
    global _slider_h_value
    _slider_h_value = value


def _slider_v_control_func(slider, value):
    global _slider_v_value
    _slider_v_value = value


def _graph_button_update(graph, size):
    global _dial_value, _slider_h_value, _slider_v_value
    global _max_track_samples
    global _track_1_data, _track_2_data, _track_3_data
    global _last_track_update

    # Update the graph
    time = pygame.time.get_ticks()
    # Update twice per second, to show some life
    if (time - _last_track_update) > 250:
        _track_1_data.append(_dial_value)
        _track_2_data.append(_slider_h_value)
        _track_3_data.append(_slider_v_value)
        _last_track_update = time

    # Truncate to the maximum size to prevent memory crash
    if len(_track_1_data) > _max_track_samples:
        _track_1_data = _track_1_data[-_max_track_samples:]
        _track_2_data = _track_2_data[-_max_track_samples:]
        _track_3_data = _track_3_data[-_max_track_samples:]

    # Return what was asked for
    return [{"color": CYAN, "data": _track_1_data[-size:]},
            {"color": BLUE, "data": _track_2_data[-size:]},
            {"color": MAGENTA, "data": _track_3_data[-size:]}, ]


# ---- Graph and Control Widgets

_control_graph = Graph((410, 130), (390, 100),
                       min_max=(0, 100), function=_graph_button_update)
_control_dial = Dial((450, 240), (150, 150),
                     min_max=(0, 100), start_value=_dial_value,
                     snap_value=1,
                     color2=CYAN,
                     dynamic=True, function=_dial_control_func)
_h_slider = Slider((620, 400), (150, 50),
                   min_max=(25, 75), start_value=_slider_h_value,
                   snap_value=5,
                   label_color1=BLACK, color1=MEDIUM_GRAY, color2=MAGENTA,
                   dynamic=True, function=_slider_v_control_func)
_v_slider = Slider((620, 240), (50, 150),
                   min_max=(0, 100), start_value=_slider_v_value,
                   snap_value=.1,
                   label_color1=BLACK, color1=MEDIUM_GRAY, color2=BLUE,
                   dynamic=False, function=_slider_h_control_func)
_fake_graph = Graph((680, 240), (110, 150), min_max=(-100, 100),
                    quiet=True, function=fake_data_graph_function)

# =========================================================
# Define keyboard navigation grid
# This could probably be automated someday, or bake in
# some kind of layout manager
# =========================================================

_up_button._neighbors = [Page.WALL, _dn_button, Page.WALL, _one_button]
_dn_button._neighbors = [_up_button, _back_button, Page.WALL, _three_button]

_back_button._neighbors = [_dn_button, Page.WALL,
                           Page.WALL, _do_nothing_button]
_do_nothing_button._neighbors = [_count_reset_button, Page.WALL,
                                 _back_button, _next_button]

_next_button._neighbors = [_blue_button, Page.WALL,
                           _do_nothing_button, _boop_button]

_boop_button._neighbors = [_control_dial, Page.WALL,
                           _next_button, _h_slider]

_one_button._neighbors = [Page.WALL, _two_button,
                          _up_button, _red_button]
_two_button._neighbors = [_one_button, _three_button,
                          _up_button, _green_button]
_three_button._neighbors = [_two_button, _count_reset_button,
                            _dn_button, _blue_button]
_count_reset_button._neighbors = [_three_button, _do_nothing_button,
                                  _dn_button, _control_dial]

_red_button._neighbors = [Page.WALL, _green_button,
                          _one_button, Page.WALL]
_green_button._neighbors = [_red_button, _blue_button,
                            _two_button, Page.WALL]
_blue_button._neighbors = [_green_button, _next_button,
                           _three_button, _control_dial]

_control_dial._neighbors = [Page.WALL, _boop_button,
                            _count_reset_button, _v_slider]
_v_slider._neighbors = [Page.WALL, _h_slider, _control_dial, Page.WALL]
_h_slider._neighbors = [_v_slider, Page.WALL, _boop_button, Page.WALL]


# =========================================================
# Page configuration and definition
# =========================================================


def sampler_page(background):
    # Tests background image, Button, RoundedButton, DynamicButton,
    # ToggleButton, ButtonGroup, Label, Indicator, ...
    _sampler_page = Page('sampler',
                         background=background,
                         widgets=[
                             # Putting a non-focus element first to test
                             # that case in keyboard control
                             _up_dn_indicator, _up_button, _dn_button,
                             _back_button, _do_nothing_button, _next_button,
                             _boop_button, _boop_indicator,

                             _count_buttons_label,
                             _one_button, _two_button, _three_button,
                             _count_reset_button,

                             _color_buttons_label,
                             _red_button, _green_button, _blue_button,
                             _color_group,

                             _control_graph, _control_dial, _v_slider,
                             _h_slider,
                             _fake_graph
                         ])

    return _sampler_page
