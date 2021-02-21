"""
main app base class with context help for flow and app state changes
====================================================================

The class :class:`HelpAppBase` provided by this namespace portion is extending your application with a context-sensitive
help functionality.

The data-driven approach allows to add, edit and remove help texts without the need to change a single line of code or
to recompile your app. This gets achieved within :class:`HelpAppBase` by overriding the main app class methods
:meth:`~ae.gui_app.MainAppBase.change_flow` and :meth:`~ae.gui_app.MainAppBase.change_app_state`.

So to add help support to the widgets of your app you only need to add/provide the help texts with a help id that is
matching the value of the :attr:`help_id` attribute of the widget you need help for.

Additionally you can provide a separate i18n translation message file for each of the supported languages to make your
help texts multi-lingual.


help layout implementation example
----------------------------------

:class:`HelpAppBase` inherits from :class:`~ae.gui_app.MainAppBase` while still being independent from the used GUI
framework/library.

.. note::
    The user interface for this help system has to be provided externally on top of this module. It can either be
    implemented directly in your app project or in a separate framework-specific module.

Use :class:`HelpAppBase` as base class of the GUI framework specific main application class and implement the abstract
methods :meth:`~ae.gui_app.MainAppBase.init_app` and :meth:`~HelpAppBase.ensure_top_most_z_index`::

    from ae.gui_help import HelpAppBase

    class MyMainApp(HelpAppBase):
        def init_app(self, framework_app_class=None):
            self.framework_app = framework_app_class()
            ...
            return self.framework_app.run, self.framework_app.stop

        def ensure_top_most_z_index(self, widget):
            framework_method_to_push_widget_to_top_most(widget)
            ...

For to activate the help mode the widget to display the help texts have to be assigned to the property/attribute
:attr:`~HelpAppBase.help_layout`::

    main_app.help_layout = HelpScreenContainerOrWindow()

The :attr:`~HelpAppBase.help_layout` property is also used as a flag of the help mode activity. By assigning `None` to
this attribute the help mode will be deactivated::

    main_app.help_layout = None

Use the attribute :attr:`~HelpAppBase.help_activator` to provide and store a widget that allows the user to toggle the
help mode activation. The :meth:`~HelpAppBase.help_display` is using it as fallback widget if no help target widget got
found.

.. hint::
    An example implementation of an de-/activation method is :meth:`~ae.kivy_app.KivyMainApp.help_activation_toggle`
    situated in the :mod:`ae.kivy_app` namespace portion.

    This more complete example is also demonstrating the implementation and usage of the help activator and layout
    widgets (in the classes :class:`~ae.kivy_help.HelpBehavior`, :class:`~ae.kivy_help.HelpToggler` and
    :class:`~ae.kivy_help.HelpLayout`).


additional helper functions
---------------------------

The helper functions :func:`anchor_points`, :func:`layout_ps_hints`, :func:`layout_x` and :func:`layout_y`, provided
by this module, are providing a framework-independent calculation of the position and size of the help layout and the
anchor.


flow change context message id
------------------------------

The message id to identify the help texts for each flow button is composed by the :meth:`~HelpAppBase.help_flow_id`,
using the prefix marker string defined by the module variable :data:`HELP_ID_PREFIX_FLOW` followed by the flow id of the
flow widget.

For example the message id for a flow button with the flow action `'open'`, the object `'item'` and the (optional)
flow key `'123456'` is resulting in the following help text message id::

    'help_flow#open_item:123456'

If there is no need for a detailed message id that is taking the flow key into account, then simply create a help text
message id without the flow key.

The method :meth:`~HelpAppBase.help_display` does first search for a message id including the flow key in the available
help text files and if not found it will automatically fallback to use a message id without the flow key::

    'help_flow#open_item'

.. hint::
    More information regarding the flow id you find in the doc string of the module :mod:`ae.gui_app` in the section
    :ref:`application flow`.


application state change context message id
-------------------------------------------

The message ids for app state change help texts are using the prefix marker string defined by the module variable
:data:`HELP_ID_PREFIX_STATE`, followed by the name of the app state and are composed via the method
:meth:`~HelpAppBase.help_app_state_id`.


pluralize-able help texts
-------------------------

Each message id can optionally have several different help texts for their pluralization. For that simply add a `count`
item to the `help_vars` property of the help target widget and then define a help text for the all the possible count
cases in your message text file like shown in the following example::

    {
        'message_id': {
                       'zero':      "help text if {count} == 0",    # {count} will be replaced with `'0'`
                       'one':       "help text if count == 1",
                       'many':      "help text if count > 1",
                       'negative':  "help text if count < 0",
                       '':          "fallback help text if count is None",
                       },
       ...
    }

The provided `count` value can also be included/displayed in the help text, like shown in the `'zero'` count case of
the example.


pre- and post-change help texts
-------------------------------

For to display a different help message before and after the change of the flow id or the app state define a message
dict with the keys `''` (an empty string) and `'after'` like shown in the following example::

    {
        'message_id': {
                       '':      "help text displayed before the flow/app-state change.",
                       'after': "help text displayed after the flow/app-state change",
                       },
       ...
    }


If you want to move/change the help target to another widget after a change, then use instead of `'after'` the
'`next_help_id'` message dict key::

    {
        'message_id': {
                       '':              "help text before the change",
                       'next_help_id':  "help_flow#next_flow_id",
                       },
       ...
    }

In this case the help target will automatically change to the widget specified by the flow id in the '`next_help_id'`
key, if the user was tapping the second time on the first/initial help target widget.


i18n help texts
---------------

The displayed help messages related to the message id will automatically get translated into the default language of the
current system/environment.

The declaration and association of message ids and their related help messages is done with the help of the namespace
portion :mod:`ae.i18n`.


further examples
----------------

More details on these and other features of this help system, e.g. the usage of f-strings in the help texts, is
documented in the doc string of the :mod:`ae.i18n` module.

A more complex example app demonstrating the features of this context help system can be found in the repository of the
`kivy lisz demo app <https://gitlab.com/ae-group/kivy_lisz>`_.
"""
from abc import abstractmethod, ABC
from typing import Any, Dict, Optional, Tuple, Union

from ae.inspector import stack_vars                                                             # type: ignore
from ae.i18n import default_language, get_f_string, register_package_translations, translation  # type: ignore
from ae.gui_app import FLOW_KEY_SEP, flow_action, id_of_flow, module_globals, MainAppBase       # type: ignore


__version__ = '0.1.23'


register_package_translations()


HELP_ID_PREFIX_FLOW = 'help_flow#'                                  #: message id prefix for flow change help texts
HELP_ID_PREFIX_STATE = 'help_app_state#'                            #: message id prefix for app state change help texts

IGNORED_HELP_FLOWS = (id_of_flow('close', 'flow_popup'), )          #: tuple of flow ids never search/show help text for
IGNORED_HELP_STATES = ('flow_id', 'flow_path', 'win_rectangle')     #: tuple of app state names never searched help for

HIDDEN_GLOBALS = ('__builtins__', '__doc__', 'module_globals')      #: globals that get removed from help_variables


def anchor_points(radius: float, anchor_x: float, anchor_y: float, anchor_dir: str) -> Tuple[float, ...]:
    """ recalculate points of the anchor triangle drawing.

    :param radius:          radius of anchor triangle.
    :param anchor_x:        anchor x coordinate in window.
    :param anchor_y:        anchor y coordinate in window.
    :param anchor_dir:      anchor direction: 'r'=right, 'i'=increase-y, 'l'=left, 'd'=decrease-y

                            .. note:
                                the direction in the y axis got named increase for higher y values
                                and `decrease` for lower y values to support different coordinate
                                systems of the GUI frameworks.

                                For example in `kivy` the zero value of the y axis is at the bottom
                                of the app window, whereas in enaml/qt it is at the top.

    :return:                tuple of the x and y coordinates of the anchor triangle edges.
    """
    return (anchor_x - (radius if anchor_dir in 'id' else 0),
            anchor_y - (radius if anchor_dir in 'lr' else 0),
            anchor_x + (0 if anchor_dir in 'id' else radius * (-1 if anchor_dir == 'r' else 1)),
            anchor_y + (0 if anchor_dir in 'lr' else radius * (-1 if anchor_dir == 'i' else 1)),
            anchor_x + (radius if anchor_dir in 'id' else 0),
            anchor_y + (radius if anchor_dir in 'lr' else 0),
            )


def help_id_has_translation(help_id: str) -> Tuple[Optional[Union[str, Dict[str, str]]], str]:
    """ check if a help text exists for the passed help id.

    :param help_id:         help id to check if a translation/help texts exists.
    :return:                tuple of translation text (if help text exists) and maybe shortened help id(removed detail).
    """
    trans_text_or_dict = translation(help_id)
    short_help_id = help_id
    if not trans_text_or_dict and FLOW_KEY_SEP in help_id:
        short_help_id = help_id[:help_id.index(FLOW_KEY_SEP)]  # remove detail (e.g. flow key or app state value)
        trans_text_or_dict = translation(short_help_id)
    return trans_text_or_dict, short_help_id


def layout_ps_hints(wid_x: float, wid_y, wid_width, wid_height, win_width, win_height) -> Dict[str, Union[str, float]]:
    """ recalculate anchor and max width/height on change of widget pos/size or window size.

    :param wid_x:           x coordinate in app window of help target flow widget.
    :param wid_y:           y coordinate in app window of help target flow widget.
    :param wid_width:       width of help target flow widget.
    :param wid_height:      height of help target flow widget.
    :param win_width:       app window width.
    :param win_height:      app window height.
    :return:                dict with position and size hints, like e.g.:

                            * anchor_dir:       direction of the anchor triangle (pointing from help layout
                                                to the help target widget):
                                                'r'=right, 'i'=increase-y, 'l'=left, 'd'=decrease-y(kivy:bottom/qt:top).
                            * anchor_x:         x coordinate of the anchor center.
                            * anchor_y:         y coordinate of the anchor center.
                            * max_width:        maximum width of the layout.
                            * max_height:       maximum height of the layout.

    """
    max_width = win_width - wid_x - wid_width
    if max_width < wid_x:
        max_width = wid_x
        anchor_dir_x = 'l'
    else:
        anchor_dir_x = 'r'
    max_height = win_height - wid_y - wid_height
    if max_height < wid_y:
        max_height = wid_y
        anchor_dir_y = 'd'
    else:
        anchor_dir_y = 'i'
    if max_width > max_height:
        anchor_dir = anchor_dir_x
        anchor_x = wid_x + (0 if anchor_dir_x == 'l' else wid_width)
        anchor_y = wid_y + wid_height / 2
        max_height = win_height
    else:
        anchor_dir = anchor_dir_y
        anchor_x = wid_x + wid_width / 2
        anchor_y = wid_y + (0 if anchor_dir_y == 'd' else wid_height)
        max_width = win_width

    return locals().copy()


def layout_x(anchor_x: float, anchor_dir: str, width: float, win_width: float) -> float:
    """ recalculate help layout x position.

    :param anchor_x:        anchor x coordinate in window.
    :param anchor_dir:      anchor direction: 'r'=right, 'i'=increase-y, 'l'=left, 'd'=decrease-y (kivy:bottom, qt:top).
    :param width:           help layout width.
    :param win_width:       app window width.
    :return:                x coordinate of help layout within the app window.
    """
    if anchor_dir == 'l':
        return anchor_x - width
    if anchor_dir == 'r':
        return anchor_x
    return min(max(0.0, anchor_x - width / 2), win_width - width)


def layout_y(anchor_y: float, anchor_dir: str, height: float, win_height: float) -> float:
    """ recalculate help layout y position.

    :param anchor_y:        anchor y coordinate in window.
    :param anchor_dir:      anchor direction: 'r'=right, 'i'=increase-y, 'l'=left, 'd'=decrease-y (kivy:bottom, qt:top).
    :param height:          help layout height.
    :param win_height:      app window height.
    :return:                y coordinate of help layout in the app window.
    """
    if anchor_dir == 'i':
        return anchor_y
    if anchor_dir == 'd':
        return anchor_y - height
    return min(max(0.0, anchor_y - height / 2), win_height - height)


class HelpAppBase(MainAppBase, ABC):
    """ main app help base class. """

    # additional instance attributes
    displayed_help_id: str = ''         #: message id of the currently explained/focused target widget in help mode
    help_activator: Any = None          #: help mode de-/activator button widget
    help_layout: Optional[Any] = None   #: container/popup/dropdown/window widget in active help mode else None

    _next_help_id: str = ''             #: last app state or flow change to show help text on help mode activation

    @abstractmethod
    def ensure_top_most_z_index(self, widget: Any):
        """ ensure visibility of the passed widget to be the top most in the z index/order.

        :param widget:          the popup/dropdown/container widget to be moved to the top.
        """

    # overwritten methods

    def change_app_state(self, state_name: str, state_value: Any, send_event: bool = True):
        """ change app state via :meth:`~ae.gui_app.MainAppBase.change_app_state`, show help text in active help mode.

        All parameters are documented in the overwritten method :meth:`~ae.gui_app.MainAppBase.change_app_state`.
        """
        help_vars = dict(state_name=state_name, state_value=state_value, send_event=send_event)
        if not self.help_app_state_display(help_vars):
            super().change_app_state(state_name, state_value, send_event=send_event)
            self.help_app_state_display(help_vars, changed=True)

    def change_flow(self, new_flow_id: str, **event_kwargs) -> bool:
        """ change/switch flow id - overriding :meth:`~ae.gui_app.MainAppBase.change_flow`.

        More detailed documentation of the parameters you find in the overwritten method
        :meth:`~ae.gui_app.MainAppBase.change_app_state`.

        This method returns True if flow changed and got confirmed by a declared custom event handler
        (either event method or Popup class) of the app
        AND if the help mode is *not* active or the calling widget is selected
        in active help mode, else False.
        """
        count = event_kwargs.pop('count', None)
        help_vars = dict(new_flow_id=new_flow_id, event_kwargs=event_kwargs)
        if count is not None:
            help_vars['count'] = count

        if not self.help_flow_display(help_vars):
            if super().change_flow(new_flow_id, **event_kwargs):
                self.help_flow_display(help_vars, changed=True)
                return True
        return False

    # help specific methods

    def help_app_state_display(self, help_vars: Dict[str, Any], changed: bool = False) -> bool:
        """ actualize the help layout if active, before and after the change of the app state.

        :param help_vars:       locals (args/kwargs) of overwritten :meth:`~ae.gui_app.MainAppBase.change_flow` method.

                                items passed to the help text renderer:
                                    * `count`: optional number used to render a pluralized help text
                                      for this app state change.

        :param changed:         False before change of the app state, pass True if app state got just/already changed.
        :return:                True if help mode and layout is active and found target widget is locked, else False.
        """
        state_name = help_vars.get('state_name')
        if not state_name or state_name in IGNORED_HELP_STATES:
            return False

        help_id = self.help_app_state_id(state_name)

        hlw = self.help_layout
        if hlw is None:
            if help_id_has_translation(help_id)[0]:
                self._next_help_id = help_id
            return False            # inactive help layout

        ret = self.help_display(help_id, help_vars, key_suffix='after' if changed else '')
        if help_id == self.displayed_help_id and not changed:
            ret = False             # allow to execute app state change
        return ret

    @staticmethod
    def help_app_state_id(state_name: str) -> str:
        """ compose help id for app state changes.

        :param state_name:      name of the app state variable.
        :return:                help id for the specified app state.
        """
        return f'{HELP_ID_PREFIX_STATE}{state_name}'

    def help_display(self, help_id: str, help_vars: Dict[str, Any], key_suffix: str = '', must_have: bool = False
                     ) -> bool:
        """ display help text to the user in activated help mode.

        :param help_id:         help id to show help text for.
        :param help_vars:       variables used in the conversion of the f-string expression to a string.
                                optional items passed to the help text renderer:
                                * `count`: optional number used to render a pluralized help text.
                                * `self`: target widget to show help text for.
        :param key_suffix:      suffix to the key used if the translation is a dict.
        :param must_have:       pass True to display error help text and console output if no help text exists.
        :return:                True if help text got found and displayed.
        """
        has_trans, short_help_id = help_id_has_translation(help_id)
        if not has_trans:
            if not must_have:
                return False
            if self.debug:
                help_id = f"No translation found for help id [b]'{help_id}/{key_suffix}'[/b] in '{default_language()}'"
            else:
                help_id = ''        # show at least initial help text as fallback
            short_help_id = help_id
            key_suffix = ''
            self.play_beep()
        elif key_suffix == 'after' and 'next_help_id' in has_trans:
            help_id = short_help_id = has_trans['next_help_id']     # type: ignore # silly mypy, Pycharm is more clever
            key_suffix = ''

        hlw: Any = self.help_layout
        hlw.target = self.help_widget(help_id, help_vars)
        self.change_observable('displayed_help_id', help_id)

        glo_vars, help_vars = self.help_variables(help_vars)
        hlw.help_text = get_f_string(short_help_id, key_suffix=key_suffix, glo_vars=glo_vars, loc_vars=help_vars)

        self.ensure_top_most_z_index(hlw)
        self.call_method('on_help_displayed')

        return True

    def help_flow_display(self, help_vars: Dict[str, Any], changed: bool = False) -> bool:
        """ actualize the help layout if active, exclusively called by :meth:`~ae.gui_app.MainAppBase.change_flow`.

        :param help_vars:       locals (args/kwargs) of overwritten :meth:`~ae.gui_app.MainAppBase.change_flow` method.
        :param changed:         False before change to new flow, pass True if flow got changed already.
        :return:                True if help layout is active and found target widget is locked, else False.
        """
        nfi = help_vars.get('new_flow_id')
        if not nfi or nfi in IGNORED_HELP_FLOWS:
            return False

        help_id = self.help_flow_id(nfi)

        hlw = self.help_layout
        if hlw is None:
            if help_id_has_translation(help_id)[0]:
                self._next_help_id = help_id
            return False            # inactive help layout

        ret = self.help_display(help_id, help_vars, key_suffix='after' if changed else '', must_have=not changed)
        if not changed and (help_id == self.displayed_help_id or flow_action(nfi) == 'open'):
            # allow to execute flow change of currently explained flow button or if open flow action with no help text
            ret = False
        return ret

    @staticmethod
    def help_flow_id(flow_id: str) -> str:
        """ compose help id for flow changes.

        :param flow_id:         flow id to show help text for.
        :return:                help id for the specified flow id and suffix.
        """
        return f'{HELP_ID_PREFIX_FLOW}{flow_id}'

    def help_id_flow(self) -> str:
        """ determine flow id of the current help id. """
        hid = self.displayed_help_id
        if hid.startswith(HELP_ID_PREFIX_FLOW):
            return hid[len(HELP_ID_PREFIX_FLOW):]
        return ''

    def help_target_and_id(self, help_vars: Dict[str, Any]) -> Tuple[Any, str]:
        """ find help widget/target and help id on help mode activation.

        :param help_vars:       optional help vars.
        :return:                tuple of help target widget and help id.
        """
        activator = self.help_activator
        if self._next_help_id:
            help_id = self._next_help_id
        elif self.flow_id:
            help_id = self.help_flow_id(self.flow_id)
        else:
            return activator, ''

        target = self.help_widget(help_id, help_vars)
        if target is activator:
            help_id = ''
        return target, help_id

    def help_variables(self, help_vars: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """ determine globals and extend help vars for help text evaluation/translation

        :param help_vars:       initial help variable locals that will be extended and returned.
        :return:                global and local variable dicts.
        """
        glo_vars = {k: v for k, v in module_globals.items() if k not in HIDDEN_GLOBALS}
        glo_vars.update((k, v) for k, v in globals().items() if k not in HIDDEN_GLOBALS)
        glo_vars['_add_base_globals'] = True        # instruct ae.inspector.try_eval to add ae.core globals

        help_vars['app'] = self.framework_app
        help_vars['main_app'] = self

        return glo_vars, help_vars

    def help_widget(self, help_id: str, help_vars: Dict[str, Any]) -> Any:
        """ ensure/find help target widget via attribute name/value and extend :paramref:`~help_widget.help_vars`.

        :param help_id:         widget.help_id attribute value to detect widget and call stack locals.
        :param help_vars:       help env variables, to be extended with event activation stack frame locals
                                and a 'self' key with the help target widget.
        :return:                found help target widget or self.help_activator if not found.
        """
        wid = help_vars.get('self')
        if not wid:
            if help_id:
                # first look for widget with help_id attr in kv/enaml rule call stack frame for translation text context
                depth = 1
                while depth <= 15:
                    _gfv, lfv, _deep = stack_vars("", min_depth=depth, max_depth=depth)  # "" to not skip ae.kivy_help
                    widget = lfv.get('self')
                    if getattr(widget, 'help_id', None) == help_id:
                        help_vars.update(lfv)
                        return widget
                    depth += 1

                # then search the widget tree
                wid = self.widget_by_attribute('help_id', help_id)
                if not wid:
                    self.vpo(f"HelpAppBase.help_widget(): widget with help_id '{help_id}' not found")

            if not wid:
                wid = self.help_activator
            help_vars['self'] = wid

        return wid

    def on_flow_popup_close(self, _flow_key: str, _popup_args: Dict[str, Any]) -> bool:
        """ overwritten popup close handler of FlowPopup widget to reset help widget/text. """
        if self.help_layout and self.help_widget(self.displayed_help_id, dict()) is self.help_activator:
            self.help_display('', dict())
        return True
