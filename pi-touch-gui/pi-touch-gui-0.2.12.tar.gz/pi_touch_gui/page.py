# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Graphical User Interface objects

    A `Page` is a set of widgets that define the interaction and display
    surface of the GUI

    The `GUI` manages the hardware and runs the Pages
"""
import importlib
import json
import logging
import math
from pathlib import Path
from typing import List, Optional

import pygame

from pi_touch_gui._utilities import backlog_error
from pi_touch_gui._widget_bases import IWidget, IWidgetInterface
from pi_touch_gui.colors import BLACK
from pi_touch_gui.multitouch.raspberrypi_ts import TS_RELEASE

LOG = logging.getLogger(__name__)


class Page(object):
    WALL = 'wall'
    GO_WALL = -1
    GO_UP = 0
    GO_DOWN = 1
    GO_LEFT = 2
    GO_RIGHT = 3

    GO_NEIGHBORLESS = [-1, 1, -1, 1]
    GO_NAMES = ["Up", "Down", "Left", "Right"]

    LCARS = 'lcars'

    def __init__(self, name, widgets=None, background=None, function=None):
        """ A collection of widgets that make up an interaction page.

        Parameters
        ----------
        name : String
            Name of the page for internal and callback reference
        widgets : List[IWidget]
        background : str
            Background image resource filepath for this Page
        function : Callable[[Page], Optional[Type['Page']]]
            Function to call if none of the widgets consume
            an event.
        """
        # If no widgets added on init, they can be added with `add_widgets()`
        # later.
        self.name = name
        self.widgets = widgets or []

        if background == Page.LCARS:
            background = str(Path(Path(__file__).parent,
                                       "assets/lcars_screen.png"))
        self.background = background
        self._bg_image = None

        self.function = function

        self._focus_widget = None
        if widgets is None:
            self.widgets = []
            self._prev_focus_widget = None
        else:
            self.widgets = widgets
            self._prev_focus_widget = widgets[0]

        self._last_adjustment = pygame.time.get_ticks()
        self._adjustment_rate = 100

    def set_background(self, filepath):
        self.background = filepath
        self._bg_image = pygame.image.load(filepath).convert()

    def add_widgets(self, widgets):
        """ Add widgets to the Page.

        Parameters
        ----------
        widgets : List[IWidget]
        """
        self.widgets += widgets
        # Set or reset the base focus widget to the top
        self._prev_focus_widget = self.widgets[0]

    def find_widget(self, widget_or_id):
        """ Given a widget ID, find that widget.

        Parameters
        ----------
        widget_or_id : Union[IWidgetInterface, String]
            If a widget is passed in, return it directly. Otherwise search
            for the id and return the widget.

        Returns
        -------
        IWidgetInterface
        """
        # Deal with the WALL case, where we _know_ there isn't a widget
        if widget_or_id == Page.WALL:
            return None
        if not isinstance(widget_or_id, str):
            return widget_or_id

        return self._scan_for_widget_by_id(self.widgets, widget_or_id)

    def _scan_for_widget_by_id(self, widgets, widget_id):
        """ Recursively scan for a widget ID, returning the widget.

        Parameters
        ----------
        widgets : List[IWidgetInterface]
            A list of widgets, some of which may container lists of widgets
        widget_id : String
            The widget ID to search for

        Returns
        -------
        IWidgetInterface
        """
        for widget in widgets:
            # See if this is a widget container...
            found_widget = None
            sub_widgets = widget.sub_widgets
            if sub_widgets:
                # Assume the widget is a widget container and assert if not
                found_widget = self._scan_for_widget_by_id(sub_widgets,
                                                           widget_id)
            else:
                if widget.id == widget_id:
                    found_widget = widget
            if found_widget is not None:
                return found_widget
        return None

    def find_next_widget(self, widget_or_id, direction):
        """ Given a widget ID, find the widget AFTER that widget.

        Parameters
        ----------
        widget_or_id : Union[IWidgetInterface, String]
        direction : Integer
            Direction of scan, sign(direction)

        Returns
        -------
        IWidgetInterface
        """
        # Deal with the WALL case, where we _know_ there isn't a widget
        if widget_or_id == Page.WALL:
            return None
        try:
            widget_or_id = widget_or_id.id
        except AttributeError:
            pass

        return self._scan_for_next_widget_by_id(self.widgets,
                                                widget_or_id,
                                                math.copysign(1, direction))

    def _scan_for_next_widget_by_id(self, widgets, widget_id, step):
        """ Recursively scan for a widget ID, returning the widget AFTER the
        widget found.

        Parameters
        ----------
        widgets : List[IWidgetInterface]
            A list of widgets, some of which may container lists of widgets
        widget_id : String
            The widget ID to search for
        step : Integer
            The step (+1, -1) we are scanning next for.

        Returns
        -------
        IWidgetInterface
        """
        step = int(step)
        for idx, widget in enumerate(widgets):
            # See if this is a widget container...
            found_widget = None
            sub_widgets = widget.sub_widgets
            if sub_widgets:
                # Assume the widget is a widget container and assert if not
                found_widget = self._scan_for_widget_by_id(sub_widgets,
                                                           widget_id)
            else:
                if widget.id == widget_id:
                    try:
                        found_widget = widgets[idx + step]
                    except Exception as e:
                        LOG.error(f"Unmanaged Exception {type(e)}: {e}")
                        return None
            if found_widget is not None:
                return found_widget
        return None

    def touch_handler(self, event, touch) -> Optional['Page']:
        """ Update all widgets with a touch event.

            The first widget to consume the touch wins, and downstream
            widgets won't be tested.

            If no widget consumes the event, we call `function(self) -> Page`

        Parameters
        ----------
        event : int
            Event code defined for the interface; e.g. _widget_bases.py imports
            TS_PRESS, TS_RELEASE, and TS_MOVE
        touch : Touch
            The Touch object for the event.

        Returns
        -------
        Optional[Page]
            If the widget function names a new page, it is returned here
        """
        for widget in self.widgets:
            consumed, new_page = widget.event(event, touch)
            if consumed:
                return new_page

        if event == TS_RELEASE and self.function:
            return self.function(self, False)
        return None

    def render(self, surface: pygame.Surface):
        """Redraw all widgets to screen.

        Call `render()` for all widgets in the Page, once per frame.

        Parameters
        ----------
        surface : pygame.Surface
            Surface (screen) to draw to
        """
        # Lazy loading to avoid pygame initialization issues
        if self._bg_image is None and self.background is not None:
            self._bg_image = pygame.image.load(self.background).convert()

        if self._bg_image is not None:
            surface.blit(self._bg_image, (0, 0))
        else:
            surface.fill(BLACK)
        for widget in self.widgets:
            try:
                widget.render(surface)
            except Exception as e:
                backlog_error(e, f"Problem rendering widget {widget}")
                raise

    def focus_widget(self, enable):
        """ Wake up the focus system for gesture control.

        Will always restart on the last widget that had focus.

        Parameters
        ----------
        enable : Bool
            If True, then focus; else de-focus
        """
        if self.is_focused() == enable:
            return

        prev_widget = self._prev_focus_widget
        self._focus_widget = self._prev_focus_widget
        if enable:
            if not prev_widget.can_focus():
                # This will walk the down chain until it finds a widget
                # that can take focus.  Skips starting labels and stuff.
                self.shift_widget_focus(Page.GO_DOWN)
            else:
                prev_widget.focus(True)
        else:
            self._focus_widget = None
            prev_widget.focus(False)

    def is_focused(self):
        """ Determine if we are in widget focus mode.

        Returns
        -------
        Bool
        """
        return self._focus_widget is not None

    def shift_widget_focus(self, direction):
        """ Shift focus one way or the other, wrapping at the boundaries.

        Parameters
        ----------
        direction : int
            Direction of motion; Page.WALL (no motion),
        """
        if direction == Page.GO_WALL:
            return
        if not self.is_focused():
            return

        start_widget = test_widget = self._focus_widget
        while True:
            next_widget = test_widget.neighbors[direction]

            # We have an IWidgetInterface, ID string, or 'wall'
            if next_widget == Page.WALL:
                # Hit a wall
                return
            elif next_widget is None:
                # No neighbor specified, so use a generic direction
                next_widget = self.find_next_widget(
                    test_widget,
                    Page.GO_NEIGHBORLESS[direction])
            else:
                # Neighbor as a widget ID or index
                next_widget = self.find_widget(next_widget)

            # In case we instantiated a neighbor, store it
            test_widget.neighbors[direction] = next_widget

            if next_widget == Page.GO_WALL:
                return
            elif next_widget == start_widget:
                return
            elif next_widget is None:
                return

            # Take the tentative next widget and make it current
            test_widget = next_widget
            if test_widget.can_focus():
                break

        try:
            if self._focus_widget is not None:
                self._focus_widget.focus(False)
            next_widget.focus(True)
        except Exception as e:
            LOG.error(f"Unmanaged Exception {type(e)}: {e}")
        self._focus_widget = next_widget
        self._prev_focus_widget = next_widget

    def adjust_widget(self, direction):
        """ Send an up/down value adjustment to the control widget.
        """
        time = pygame.time.get_ticks()
        if time - self._last_adjustment < self._adjustment_rate:
            return

        if self._focus_widget._adjust is not None:
            self._focus_widget._adjust(direction)
            self._last_adjustment = time

    def press_widget(self):
        """ Activate the function of the widget.
        """
        if self._focus_widget.press is not None:
            self._focus_widget.press()

    def release_widget(self):
        """ Activate the function of the widget.
        """
        if self._focus_widget.release is not None:
            return self._focus_widget.release()
        return None

    def iter_widgets(self):
        """ Iterate over the widgets in the page.

        Returns
        -------
        iter(IWidget)
        """
        return iter(self.widgets)

    def serialize(self, readable=False):
        """ Serialize this page and return it as a JSON string, suitable
        to be deserialized()
        """
        indent = 4 if readable else None
        return json.dumps(self._do_serialize(self),
                          indent=indent,
                          sort_keys=True)

    def _do_serialize(self, entity):
        if entity is None:
            return None
        if type(entity) in [str, int, float, complex, bool]:
            return entity
        elif type(entity) in [list, tuple, set]:
            # JSON doesn't distinguish list-equivalent types
            return [self._do_serialize(v) for v in entity]
        elif type(entity) is dict:
            return {k: self._do_serialize(v) for k, v in entity.items()}
        elif callable(entity):
            pause = True
            path = '.'.join([entity.__module__,
                             entity.__qualname__]).split('.')
            context = '.'.join(path[:-1])
            name = path[-1]

            if '<locals>' in context:
                raise ValueError(f'Can not serialize local function '
                                 f'{context}.{name}')
            if '<lambda>' in context:
                raise ValueError(f'Can not serialize lambda function '
                                 f'{context}.{name}')
            elif 'builtins' in context:
                raise ValueError(f'Can not serialize builtin function '
                                 f'{context}.{name}')
            return {'__Function': {'context': context,
                                   'name': name}}
        elif issubclass(type(entity), Page):
            return self._do_serialize_object(entity)
        elif issubclass(type(entity), IWidgetInterface):
            return self._do_serialize_object(entity)
        else:
            raise TypeError(f"Unsupported type {type(entity)!r}")

    def _do_serialize_object(self, entity):
        ent_type = type(entity)
        kwargs = {k: self._do_serialize(v) for k, v in vars(entity).items()
                  if not k.startswith('_')}
        return {'__Object': {'module': ent_type.__module__,
                             'class': ent_type.__name__,
                             'kwargs': kwargs}}

    @classmethod
    def deserialize(cls, serial):
        """ Deserialize the data and return the Page it started as.
        """
        data = json.loads(serial)
        return Page._do_deserialize(data)
        pass

    @classmethod
    def _do_deserialize(cls, entity):
        if entity is None:
            return None
        if type(entity) in [str, int, float, complex, bool]:
            return entity
        if type(entity) is list:
            return [Page._do_deserialize(v) for v in entity]
        elif type(entity) is dict:
            content = {}
            for key in entity.keys():
                if key == '__Function':
                    value = entity[key]
                    context = value['context']
                    func_name = value['name']
                    return Page._get_context(context, func_name)
                elif key == '__Object':
                    value = entity[key]
                    module = value['module']
                    class_name = value['class']
                    kwargs = Page._do_deserialize(value['kwargs'])
                    c = Page._get_context(module, class_name)
                    return c(**kwargs)
                else:
                    content.update({key: Page._do_deserialize(entity[key])})
            return content
        else:
            raise TypeError(f"Unsupported type {type(entity)!r}")

    @classmethod
    def _get_context(cls, module, item):
        path = module.split('.')
        imp = path[0]
        try:
            m = importlib.import_module(imp)
        except Exception as e:
            raise ImportError(f"Unable to import {imp!r}: {e}")
        for part in path[1:]:
            m = getattr(m, part)
        return getattr(m, item)
