# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Test - Page with poweroff button
"""
import os

from colors import RED
from page import Page
from tests._utilities import pulsing_light_func
from widget_buttons import Button
from widget_displays import Label, Light


def poweroff_button_func(button, pushed):
    os.system('sudo poweroff')
    return None


_exit_label_1 = Label((0, 0), (800, 50), label="Nothing to see here")
_exit_label_2 = Label((0, 50), (800, 430), font_size=100,
                      label_color1=RED, label="... move along!")

_pulse1_light = Light((0, 0), (50, 50), function=pulsing_light_func)
_pulse1_light.rate = 100

_pulse2_light = Light((750, 0), (50, 50), function=pulsing_light_func)
_pulse2_light.rate = 105

_pulse3_light = Light((0, 430), (50, 50), function=pulsing_light_func)
_pulse3_light.rate = 110

_pulse4_light = Light((750, 430), (50, 50), pulsing_light_func)
_pulse4_light.rate = 115

_off_button = Button((200, 320), (400, 150),
                     style=Button.OBROUND,
                     label="-~= OFF =~-",
                     function=poweroff_button_func)


def _configure_page(go_to_page):
    """ Custom configuration on the entry page - sets the page and
    button functions.

    Parameters
    ----------
    go_to_page : Callable[[IWidget, bool], Optional['Page']]
    """
    # _poweroff_page.function = go_to_page


def poweroff_page():

    # Tests dynamic Light functions, Label, and default Page function
    _poweroff_page = Page('power_off',
                          [
                              _exit_label_1, _exit_label_2,
                              _pulse1_light, _pulse2_light, _pulse3_light,
                              _pulse4_light,
                              _off_button
                          ],
                          )
    _poweroff_page._config = _configure_page

    return _poweroff_page
