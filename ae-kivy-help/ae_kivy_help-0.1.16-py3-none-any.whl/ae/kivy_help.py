"""
context help system for your kivy apps
======================================

The mixin class :class:`HelpBehavior` provided by this namespace portion is extending and preparing any Kivy widget for
to show an individual help text for it. The widget :class:`HelpToggler` is a toggle button to switch the help mode
on and off. Finally the widget :class:`HelpLayout` of this portion displays the translatable help texts within your app.

This namespace portion is a requirement of the :mod:`ae.kivy_app` module and is tight coupled to it. To keep the
module size small it got extracted into its own namespace portion.

:mod:`ae.kivy_app` is automatically importing/integrating this module for you. For android apps built with buildozer you
only need to add it to the requirements list in your `buildozer.spec` file.


help behaviour mixin
--------------------

To show a i18n translatable help text for a Kivy widget create either a sub-class of the widget. The following example
allows to attach a help text to a Kivy :class:`~kivy.uix.button.Button`::

    from kivy.uix.button import Button
    from ae.kivy_help import HelpBehavior

    class ButtonWithHelpText(HelpBehavior, Button):
        ...

Alternatively you can archive this via a kv-lang rule::

    <ButtonWithHelpText@HelpBehavior+Button>


.. note::
    To automatically lock and mark the widget you want to add help texts for, this mixin class has to be specified
    as the first class in the list of classes your widget get inherited from.

The correct identification of each help-aware widget presuppose that the attribute :attr:`~HelpBehavior.help_id` has a
unique value for each widget instance. This is done automatically for the widgets provided by the module
:mod:`~ae.kivy_app` to change the app flow or app states (like e.g. :class:`~ae.kivy_app.FlowButton`).

The :attr:`~HelpBehavior.help_vars` is a dict which can be used to provide extra context data to dynamically generate,
translate and display individual help texts.


help activation and de-activation
---------------------------------

Use the widget :class:`HelpToggler` provided by this namespace portion in your app to toggle the active state of the
help mode.

.. hint::
    The :class:`HelpToggler` is using the low-level touch events to prevent the dispatch of the Kivy events `on_press`,
    `on_release` and `on_dismiss` to allow to show help texts for opened dropdowns and popups.


layout widget to display help text
----------------------------------

The layout widget :class:`HelpLayout` of this module is displaying the help texts prepared by the method
:meth:`~ae.gui_help.HelpAppBase.help_display` of the namespace portion :mod:`ae.gui_help`.
"""
from typing import Callable

from kivy.input import MotionEvent                                                          # type: ignore
from kivy.lang import Builder                                                               # type: ignore
# pylint: disable=no-name-in-module
from kivy.properties import BooleanProperty, DictProperty, ObjectProperty, StringProperty   # type: ignore
from kivy.uix.image import Image                                                            # type: ignore
from kivy.uix.scrollview import ScrollView                                                  # type: ignore
from kivy.app import App                                                                    # type: ignore

from ae.kivy_relief_canvas import ReliefCanvas                                              # type: ignore


__version__ = '0.1.16'


Builder.load_string("""\
#: import anchor_points ae.gui_help.anchor_points
#: import layout_x ae.gui_help.layout_x
#: import layout_y ae.gui_help.layout_y
#: import layout_ps_hints ae.gui_help.layout_ps_hints

<HelpBehavior>:
    help_id: ''
    # 'help_layout is not None' is needed because None is not allowed for bool help_lock attribute/property
    help_lock: app.help_layout is not None and app.displayed_help_id != self.help_id
    help_vars: dict()
    canvas.after:
        Color:
            rgba: app.font_color[:3] + (0.24 if self.help_lock and self.width and self.height else 0, )
        Ellipse:
            pos: self.x + sp(9), self.y + sp(9)
            size: self.width - sp(18), self.height - sp(18)
        Color:
            rgba: app.font_color[:3] + (0.51 if self.help_lock and self.width and self.height else 0, )
        Line:
            width: sp(3)
            rounded_rectangle: self.x + sp(3), self.y + sp(3), self.width - sp(6), self.height - sp(6), sp(12)


<HelpLayout>:
    size_hint: None, None
    ps_hints: layout_ps_hints(*root.target.to_window(*root.target.pos), *root.target.size, Window.width, Window.height)
    width: min(help_label.width, Window.width)
    height: min(help_label.height, Window.height)
    x: layout_x(root.ps_hints['anchor_x'], root.ps_hints['anchor_dir'], root.width, Window.width)
    y: layout_y(root.ps_hints['anchor_y'], root.ps_hints['anchor_dir'], root.height, Window.height)
    ani_value: 0.99
    canvas.before:
        Color:
            rgba: Window.clearcolor[:3] + (root.ani_value, )
        RoundedRectangle:
            pos: root.pos
            size: root.size
    canvas.after:
        Color:
            rgba: app.font_color[:3] + (root.ani_value, )
        Line:
            width: sp(3)
            rounded_rectangle: root.x + sp(1), root.y + sp(1), root.width - sp(2), root.height - sp(2), sp(12)
        Triangle:
            points:
                anchor_points(app.main_app.font_size * 0.69, root.ps_hints['anchor_x'], root.ps_hints['anchor_y'], \
                root.ps_hints['anchor_dir'])
        Color:
            rgba: Window.clearcolor[:3] + (root.ani_value, )
        Line:
            width: sp(1)
            rounded_rectangle: root.x + sp(1), root.y + sp(1), root.width - sp(2), root.height - sp(2), sp(12)
    Label:
        id: help_label
        text: root.help_text
        color: app.font_color[:3] + (root.ani_value, )
        background_color: Window.clearcolor[:3] + (root.ani_value, )
        font_size: app.main_app.font_size * 0.81
        markup: True
        padding: sp(12), sp(9)
        size_hint: None, None
        size: self.texture_size


<HelpToggler>:
    icon_name: 'help_icon' if app.help_layout or 'app_icon' not in app.main_app.image_files else 'app_icon'
    ani_value: 0.99
    size_hint_x: None
    width: self.height
    source: app.main_app.img_file(self.icon_name, app.app_states['font_size'], app.app_states['light_theme'])
    canvas.before:
        Color:
            rgba: min(self.ani_value * 1.5, 1), min(self.ani_value * 1.5, 1), 1 - self.ani_value, 1 - self.ani_value / 2
        Ellipse:
            pos: self.pos
            size: self.size
""")


class HelpBehavior:
    """ behaviour mixin class for widgets having help texts. """
    help_id = StringProperty()      #: unique help id of the widget
    help_lock = BooleanProperty()   #: True if the help mode is active and this widget is not the help target
    help_vars = DictProperty()      #: dict of extra data to displayed/render the help text of this widget

    # abstract attributes and methods provided by the class to be mixed into
    collide_point: Callable

    def on_touch_down(self, touch: MotionEvent) -> bool:                                    # pragma: no cover
        """ prevent any processing if touch is done on the help activator widget or in active help mode.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        main_app = App.get_running_app().main_app

        if main_app.help_activator.collide_point(*touch.pos):
            return False        # allow help activator button to process this touch down event

        if self.help_lock and self.collide_point(*touch.pos):  # main_app.help_layout is not None
            if main_app.help_display(self.help_id, self.help_vars):
                return True

        # noinspection PyUnresolvedReferences
        return super().on_touch_down(touch)                 # type: ignore # pylint: disable=no-member # false positive


class HelpLayout(ScrollView):                                                           # pragma: no cover
    """ semi-transparent and click-through container to display help texts. """
    target = ObjectProperty()           #: target widget to display help text for
    ps_hints = ObjectProperty()         #: pos- and size-hints for the layout window widget
    help_text = StringProperty()        #: help text string to display

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ check for additional events added by this class.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        return False            # let user click through this transparent help text widget


class HelpToggler(ReliefCanvas, Image):                                                               # pragma: no cover
    """ widget to activate and deactivate the help mode.

    To prevent the dismiss of opened popups and dropdowns at help mode activation, this singleton instance has to:

    * be registered in its __init__ to the :attr:`~ae.gui_help.HelpAppBase.help_activator` attribute and
    * have a :meth:`~HelpToggler.on_touch_down` method that is eating the activation touch event (returning True) and
    * a :meth:`~HelpToggler.on_touch_down` method not passing a activation touch in all DropDown/Popup widgets.

    """
    def __init__(self, **kwargs):
        """ initialize an instance of this class and also :attr:`~ae.gui_help.HelpAppBase.help_activator`. """
        App.get_running_app().main_app.help_activator = self
        super().__init__(**kwargs)

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ touch down event handler to toggle help mode while preventing dismiss of open dropdowns/popups.

        :param touch:           touch event.
        :return:                True if touch happened on this button (and will get no further processed => eaten).
        """
        if self.collide_point(*touch.pos):
            App.get_running_app().main_app.help_activation_toggle()
            return True
        return False
