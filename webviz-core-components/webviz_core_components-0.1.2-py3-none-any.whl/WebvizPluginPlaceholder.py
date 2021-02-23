# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class WebvizPluginPlaceholder(Component):
    """A WebvizPluginPlaceholder component.
WebvizPluginPlaceholder is a fundamental webviz dash component.
It takes a property, `label`, and displays it.
It renders an input with the property `value` which is editable by the user.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; default "some-id"): The ID used to identify this component in Dash callbacks
- buttons (list; default [
    "screenshot",
    "expand",
    "download",
    "guided_tour",
    "contact_person",
]): Array of strings, representing which buttons to render. Full set is
['download', 'contact_person', 'guided_tour', 'screenshot', 'expand']
- contact_person (dict with strings as keys and values of type string; optional): A dictionary of information regarding contact person for the data content.
Valid keys are 'name', 'email' and 'phone'.
- download (dict with strings as keys and values of type string; optional): A dictionary with information regarding the resource file the plugin requested.
Dictionary keys are 'filename', 'content' and 'mime_type'.
The 'content' value should be a base64 encoded ASCII string.
- screenshot_filename (string; default "webviz-screenshot.png"): File name used when saving a screenshot of the plugin.
- tour_steps (list; optional): Tour steps. List of dictionaries, each with two keys ('selector' and 'content').
- data_requested (number; default 0): An integer that represents the number of times
that the data download button has been clicked."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, buttons=Component.UNDEFINED, contact_person=Component.UNDEFINED, download=Component.UNDEFINED, screenshot_filename=Component.UNDEFINED, tour_steps=Component.UNDEFINED, data_requested=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'buttons', 'contact_person', 'download', 'screenshot_filename', 'tour_steps', 'data_requested']
        self._type = 'WebvizPluginPlaceholder'
        self._namespace = 'webviz_core_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'buttons', 'contact_person', 'download', 'screenshot_filename', 'tour_steps', 'data_requested']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(WebvizPluginPlaceholder, self).__init__(children=children, **args)
