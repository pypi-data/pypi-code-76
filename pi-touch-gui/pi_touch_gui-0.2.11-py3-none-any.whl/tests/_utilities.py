# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Testing utility functions that don't fit in any particular class or module.
"""
import math

import pygame

from colors import LCARS_PINK, LCARS_BLUE, WHITE

fake_data_1 = None
fake_data_2 = None
fake_num_samples = 1000
last_update = pygame.time.get_ticks()


def pulsing_light_func(light):
    """ Provide a dynamic light for testing.

    Specify a `rate` attribute on the Light calling me to change pulse rate.

    Parameters
    ----------
    light : Light

    Returns
    -------
    Tuple(Color, Color)
        The ring, fill colors of the light.
    """
    rate = getattr(light, '_rate', 200)
    ring = WHITE

    time = pygame.time.get_ticks()
    red = math.sin(time / rate) + 1.0  # sets to range 0..2
    fill = (red * 127, 0, 0)

    return ring, fill


def fake_data_graph_function(graph, size):
    """ Generate two traces of randomized fake data.

    This is a Graph update function.

    Parameters
    ----------
    graph : Graph
    size : int
        The number of samples to return

    Returns
    -------
    List(Dict)
        A list of data dictionaries, where each dict takes the form:
            {"color": <Color>, "data": [<float>]}
    """
    import random
    global fake_data_1, fake_data_2
    global last_update
    global fake_num_samples

    if fake_data_1 is None:
        fake_data_1 = [5 + random.random()]
        fake_data_2 = [5 + random.random()]
    else:
        time = pygame.time.get_ticks()
        # Update twice per second, to show some life
        if (time - last_update) > 50:
            fake_data_1.append(fake_data_1[-1] + (1.0 * random.random() - 0.5))
            fake_data_2.append(fake_data_2[-1] + (1.0 * random.random() - 0.5))
            last_update = time

    # Truncate to the maximum size to prevent memory crash
    if len(fake_data_1) > fake_num_samples:
        fake_data_1 = fake_data_1[-fake_num_samples:]
        fake_data_2 = fake_data_2[-fake_num_samples:]

    # Return what was asked for
    return [{"color": LCARS_PINK, "data": fake_data_1[-size:]},
            {"color": LCARS_BLUE, "data": fake_data_2[-size:]}, ]


def go_to_page(pages, name):
    for page in pages:
        if page.name == name:
            return page
    print(f"Page {name!r} not found.")
    return None