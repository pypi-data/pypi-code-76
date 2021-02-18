"""
user preferences widgets for your kivy app
==========================================

This namespace portion is providing a set of widgets to allow the user of your app to change the her/his personal
app settings/preferences, like the theme, the font size, the language and the used colors.

To use it in your app import this module, which can be done either in one of the modules of your app via::

    import ae.kivy_user_prefs

Alternatively and when you use the Kivy framework for your app, you can import it within your main KV file, like this::

    #: import _any_dummy_name ae.kivy_user_prefs

.. note::
    The i18n translation texts of the namespace portion get registered on importing. When you import this portion
    from the main KV file and your app is overwriting a translation text of this portion, then you have to make
    sure that the translation texts of your main app get registered after the import of this portion. For that reason
    :class:`~ae.gui_app.MainAppBase` is using the `on_app_build` event to load the application resources, which gets
    fired after Kivy has imported the main KV file.


The user preferences are implemented as a :class:`~ae.kivy_app.FlowDropDown` via the widget `UserPreferencesPopup`.

To integrate it in your app you simply add the `UserPreferencesButton` widget to the main KV file of your app.


user preferences debug mode
---------------------------

The user preferences are activating a debug mode when you click/touch the `UserPreferencesButton` button more than three
times within 6 seconds.

This debug mode activation is implemented in the :meth:`~ae.kivy_app.KivyMainApp.on_user_preferences_open`  event
handler method declared in the :mod:`ae.kivy_app` module. It can be disabled for your app by simply overriding this
method with an empty method in your main app class.

"""
from kivy.lang import Builder                                                       # type: ignore

from ae.gui_app import register_package_images                                      # type: ignore


__version__ = '0.1.20'


register_package_images()


Builder.load_string("""\
#: import DEF_LANGUAGE ae.i18n.DEF_LANGUAGE
#: import INSTALLED_LANGUAGES ae.i18n.INSTALLED_LANGUAGES

#: import DEBUG_LEVELS ae.core.DEBUG_LEVELS

#: import MIN_FONT_SIZE ae.gui_app.MIN_FONT_SIZE
#: import MAX_FONT_SIZE ae.gui_app.MAX_FONT_SIZE
#: import THEME_DARK_BACKGROUND_COLOR ae.gui_app.THEME_DARK_BACKGROUND_COLOR
#: import THEME_DARK_FONT_COLOR ae.gui_app.THEME_DARK_FONT_COLOR
#: import THEME_LIGHT_BACKGROUND_COLOR ae.gui_app.THEME_LIGHT_BACKGROUND_COLOR
#: import THEME_LIGHT_FONT_COLOR ae.gui_app.THEME_LIGHT_FONT_COLOR

<UserPreferencesButton@FlowButton>
    tap_flow_id: id_of_flow('open', 'user_preferences')
    ellipse_fill_ink: app.mixed_back_ink

<UserPreferencesPopup@FlowDropDown>
    canvas.before:
        Color:
            rgba: app.mixed_back_ink
        RoundedRectangle:
            pos: self.pos
            size: self.size
    ChangeColorButton:
        color_name: 'flow_id_ink'
    ChangeColorButton:
        color_name: 'flow_path_ink'
    ChangeColorButton:
        color_name: 'selected_item_ink'
    ChangeColorButton:
        color_name: 'unselected_item_ink'
    AppStateSlider:
        app_state_name: 'sound_volume'
        cursor_image: 'atlas://data/images/defaulttheme/audio-volume-high'
        min: 0.0
        max: 1.0
        step: 0.03
    AppStateSlider:    # current kivy module vibrator.py does not support amplitudes arg of android api
        app_state_name: 'vibration_volume'
        cursor_image: app.main_app.img_file('vibration', app.app_states['font_size'], app.app_states['light_theme'])
        min: 0.0
        max: 1.0
        step: 0.1
    AppStateSlider:
        app_state_name: 'font_size'
        cursor_image: app.main_app.img_file('font_size', app.app_states['font_size'], app.app_states['light_theme'])
        min: MIN_FONT_SIZE
        max: MAX_FONT_SIZE
        step: 1
    BoxLayout:
        size_hint_y: None
        height: app.app_states['font_size'] * 1.5 if INSTALLED_LANGUAGES else 0
        opacity: 1 if INSTALLED_LANGUAGES else 0
        OptionalButton:
            lang_code: DEF_LANGUAGE
            tap_flow_id: id_of_flow('change', 'lang_code', self.lang_code)
            tap_kwargs: dict(popups_to_close=(root, ))
            square_fill_ink:
                app.app_states['selected_item_ink'] if app.main_app.lang_code in ('', self.lang_code) else \
                Window.clearcolor
            text: _(self.lang_code)
            visible: DEF_LANGUAGE not in INSTALLED_LANGUAGES
        LangCodeButton:
            lang_idx: 0
        LangCodeButton:
            lang_idx: 1
        LangCodeButton:
            lang_idx: 2
        LangCodeButton:
            lang_idx: 3
    BoxLayout:
        size_hint_y: None
        height: app.app_states['font_size'] * 1.5
        FlowButton:
            tap_flow_id: id_of_flow('change', 'light_theme')
            tap_kwargs: dict(light_theme=False)
            text: _("dark")
            color: THEME_DARK_FONT_COLOR or self.color
            square_fill_ink: THEME_DARK_BACKGROUND_COLOR or self.square_fill_ink
        FlowButton:
            tap_flow_id: id_of_flow('change', 'light_theme')
            tap_kwargs: dict(light_theme=True)
            text: _("light")
            color: THEME_LIGHT_FONT_COLOR or self.color
            square_fill_ink: THEME_LIGHT_BACKGROUND_COLOR or self.square_fill_ink
    BoxLayout:
        size_hint_y: None
        height: app.main_app.font_size * 1.5 if app.main_app.debug else 0
        opacity: 1 if app.main_app.debug else 0
        DebugLevelButton:
            level_idx: 0
        DebugLevelButton:
            level_idx: 1
        DebugLevelButton:
            level_idx: 2
        DebugLevelButton:
            level_idx: 3
    BoxLayout:
        size_hint_y: None
        height: app.main_app.font_size * 1.5 if app.main_app.debug else 0
        opacity: 1 if app.main_app.debug else 0
        KbdInputModeButton:
            text: 'below_target'
        KbdInputModeButton:
            text: 'pan'
        KbdInputModeButton:
            text: 'scale'
        KbdInputModeButton:
            text: 'resize'
        KbdInputModeButton:
            text: ''
    OptionalButton:
        square_fill_ink: Window.clearcolor
        size_hint_x: 1
        text: "kivy settings"
        visible: app.main_app.verbose
        on_release: app.open_settings()
    OptionalButton:
        tap_flow_id: id_of_flow('open', 'iterable_displayer')
        tap_kwargs: dict(popup_kwargs=dict(title=self.text, data=app.main_app.app_env_dict()))
        square_fill_ink: Window.clearcolor
        size_hint_x: 1
        text: "app and system info"
        visible: app.main_app.debug
    OptionalButton:
        tap_flow_id: id_of_flow('open', 'f_string_evaluator')
        tap_kwargs: dict(popup_kwargs=dict(title=self.text))
        square_fill_ink: Window.clearcolor
        size_hint_x: 1
        text: "help message f-string evaluator"
        visible: app.main_app.debug
    OptionalButton:
        square_fill_ink: Window.clearcolor
        size_hint_x: 1
        text: "backup configs/resources"
        visible: app.main_app.debug
        on_release:
            app.main_app.show_message("at: " + app.main_app.backup_config_resources(), title="cfg/res backup stored"); \
            root.close()

<ChangeColorButton@FlowButton>
    color_name: 'flow_id_ink'
    tap_flow_id: id_of_flow('open', 'color_editor', self.color_name)
    square_fill_ink: Window.clearcolor
    ellipse_fill_ink: app.app_states[self.color_name]
    text: _(self.color_name)

<ColorEditorPopup@FlowDropDown>
    auto_width_anim_duration: 0.3
    fully_opened: False
    on_complete_opened: self.fully_opened = True; color_editor.color = app.app_states[root.attach_to.color_name]
    ColorPicker:
        id: color_editor
        on_color: root.fully_opened and app.main_app.change_app_state(root.attach_to.color_name, tuple(args[1]))
        size_hint_y: None
        height: self.width
        canvas.before:
            Color:
                rgba: Window.clearcolor
            RoundedRectangle:
                pos: self.pos
                size: self.size

<LangCodeButton@OptionalButton>
    lang_idx: 0
    lang_code: INSTALLED_LANGUAGES[min(self.lang_idx, len(INSTALLED_LANGUAGES) - 1)]
    tap_flow_id: id_of_flow('change', 'lang_code', self.lang_code)
    tap_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_ink:
        app.app_states['selected_item_ink'] if app.main_app.lang_code == self.lang_code else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    text: _(self.lang_code)
    visible: len(INSTALLED_LANGUAGES) > self.lang_idx

<DebugLevelButton@OptionalButton>
    level_idx: 0
    tap_flow_id: id_of_flow('change', 'debug_level', self.text)
    tap_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_ink:
        app.app_states['selected_item_ink'] if app.main_app.debug_level == self.level_idx else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    text: DEBUG_LEVELS[min(self.level_idx, len(DEBUG_LEVELS) - 1)]
    visible: app.main_app.debug and self.level_idx < len(DEBUG_LEVELS)

<KbdInputModeButton@OptionalButton>
    tap_flow_id: id_of_flow('change', 'kbd_input_mode', self.text)
    tap_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_ink:
        app.app_states['selected_item_ink'] if app.main_app.kbd_input_mode == self.text else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    visible: app.main_app.debug

<FStringEvaluatorPopup@FlowPopup>
    BoxLayout:
        orientation: 'vertical'
        FlowInput:
            id: eval_text
            size_hint_y: None
            height: app.main_app.font_size * 1.8
            focus: True
            auto_complete_texts: file_lines(norm_path("{ado}/FStringEvalSuggestions.txt"))
            on_auto_complete_texts:
                write_file_text(self.auto_complete_texts, norm_path("{ado}/FStringEvalSuggestions.txt"))
            on_text_validate:
                result_label.text = str(_(eval_text.text, \
                **dict(zip(('glo_vars', 'loc_vars'), app.main_app.help_variables(dict(self=self, tap_widget=self))))))
        FlowButton:
            text: "evaluate '" + eval_text.text + "'"
            size_hint_y: None
            height: app.main_app.font_size * 1.5
            square_fill_ink: app.app_states['selected_item_ink']
            on_release:
                result_label.text = str(_(eval_text.text, \
                **dict(zip(('glo_vars', 'loc_vars'), app.main_app.help_variables(dict(self=self, tap_widget=self))))))
        ScrollView:
            do_scroll_x: False
            Label:
                id: result_label
                text_size: self.width, None
                size_hint: 1, None
                height: self.texture_size[1]
                color: app.font_color
                font_size: app.main_app.font_size * 0.75
""")
