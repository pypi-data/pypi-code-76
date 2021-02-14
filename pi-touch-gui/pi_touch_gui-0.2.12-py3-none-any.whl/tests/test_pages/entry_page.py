# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Test - An entry page with pulsing lights
"""

# ---- Pulsing light test function (light)

from colors import RED
from page import Page
from tests._utilities import pulsing_light_func
from widget_buttons import Button
from widget_displays import Light, Label

_entry_label = Label((0, 0), (800, 50), label="ENTER")

_pulse1_light = Light((0, 0), (50, 50), function=pulsing_light_func)
_pulse1_light._rate = 400

_pulse2_light = Light((750, 0), (50, 50), function=pulsing_light_func)
_pulse2_light._rate = 300

_pulse3_light = Light((0, 430), (50, 50), function=pulsing_light_func)
_pulse3_light._rate = 200

_pulse4_light = Light((750, 430), (50, 50), pulsing_light_func)
_pulse4_light._rate = 100

def go_to_page_sampler(button, state):
    from tests.test_pages.pages import get_pages
    from tests._utilities  import go_to_page
    return go_to_page(get_pages(), 'sampler')

_touch_me_button = Button((200, 150), (400, 100), font_size=100,
                          label_color1=RED, label="Touch Me",
                          function=go_to_page_sampler)


def entry_page():
    # Tests dynamic Light functions, Label, and default Page function
    _entry_page = Page('entry', [
        _entry_label,
        _pulse1_light,
        _pulse2_light,
        _pulse3_light,
        _pulse4_light,
        _touch_me_button
    ])
    return _entry_page
