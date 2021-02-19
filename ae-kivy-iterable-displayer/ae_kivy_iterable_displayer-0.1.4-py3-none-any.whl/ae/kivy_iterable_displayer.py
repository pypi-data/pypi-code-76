"""
iterable displayer widget
=========================

The popup widget provided by this ae namespace portion can be used to display the items of any type of iterable,
like dicts, lists and tuples.

Additionally it will recursively display any sub-item of the types dict, list or tuple.


iterable displayer usage
------------------------

To open a popup displaying the keys/indexes and values of an iterable simple instantiate
:class:`IterableDisplayerPopup`. You can specify a popup window title string via the `title` kwarg and pass the iterable
to the `data` kwarg (or property)::

    dict_displayer = IterableDisplayerPopup(title="popup window title", data=iterable_data)

A widget will be automatically instantiated for each sub-item of `iterable_data` to display the item key and value.
The used widget class is depending on the type of the sub-item. For non-iterable sub-items the `IterableDisplayerLabel`
widget will be used. If instead a sub-item is containing another iterable then :class:`IterableDisplayerPopup` will use
the `IterableDisplayerButton` class, which when tapped displays another instance of :class:`IterableDisplayerPopup`
with the sub-sub-items.

.. note::
    The string in the :attr:`~kivy.uix.popup.Popup.title` property may be shortened automatically by
    :class:`~ae.kivy_app.FlowPopup`, depending on the width of the popup layout and the `font_size` app state.

"""
from typing import Any, Dict, Union

from kivy.lang import Builder                               # type: ignore
from kivy.properties import ObjectProperty                  # type: ignore # pylint: disable=no-name-in-module

from ae.files import file_transfer_progress                 # type: ignore
from ae.gui_app import id_of_flow                           # type: ignore
from ae.kivy_app import FlowPopup                           # type: ignore


__version__ = '0.1.4'


KEY_VAL_SEPARATOR = ": "


Builder.load_string('''#: set KEY_VAL_SEPARATOR "''' + KEY_VAL_SEPARATOR + '''"

<IterableDisplayerPopup>
    child_data_maps: self.compile_data_maps(self.data)
    size_hint_y: None
    # minimum_height is to small:: height: self.ids.container.minimum_height
    height: min(self.title_size * 3 + sum(chi.height for chi in self.ids.container.children), Window.height - sp(69))

<IterableDisplayerLabel@ScrollView>
    size_hint: 1, None
    height: int(app.app_states['font_size'] * 1.5)
    text: "." + KEY_VAL_SEPARATOR + "."
    do_scroll_y: False
    BoxLayout:
        size_hint: None, 1
        width: key.width + val.width
        ImageLabel:
            id: key
            size_hint_x: None
            width: root.width * .3
            text_size: root.width * .3, self.height
            halign: 'left'
            shorten: True
            shorten_from: 'right'
            text: root.text[:root.text.index(KEY_VAL_SEPARATOR)]
        ImageLabel:
            id: val
            text: root.text[root.text.index(KEY_VAL_SEPARATOR) + len(KEY_VAL_SEPARATOR):]
            text_size: None, self.height
            size: self.texture_size

<IterableDisplayerButton@BoxLayout>
    size_hint: 1, None
    height: int(app.app_states['font_size'] * 1.5)
    text: "-" + KEY_VAL_SEPARATOR + "-"
    tap_flow_id: ""
    tap_kwargs: {}
    ImageLabel:
        size_hint_x: 0.3
        text_size: self.size
        halign: 'left'
        shorten: True
        shorten_from: 'right'
        text: root.text[:root.text.index(KEY_VAL_SEPARATOR)]
    FlowButton:
        size_hint_x: 0.69
        text_size: self.size
        halign: 'left'
        shorten: True
        shorten_from: 'right'
        text: root.text[root.text.index(KEY_VAL_SEPARATOR) + len(KEY_VAL_SEPARATOR):]
        tap_flow_id: root.tap_flow_id
        tap_kwargs: root.tap_kwargs
        square_fill_ink: app.main_app.flow_path_ink[:3] + (0.18, )
        square_fill_pos: self.pos
''')


class IterableDisplayerPopup(FlowPopup):
    """ FlowPopup displaying iterable data - useful for quick prototyping and debugging. """
    data = ObjectProperty()                 #: the iterable (dict, list, tuple) from which the items will be shown

    @staticmethod
    def compile_data_maps(data: Union[dict, list, tuple]):
        """ re-create data maps if self.data changes.

        :param data:            dict/list/tuple data to display (==self.data binding).
        :return:                list of dicts to be assigned to self.child_data_maps.
        """
        if isinstance(data, dict):
            items = data.items()
        else:                               # if isinstance(data, (list, tuple)):
            items = enumerate(data)         # type: ignore # we treat tuple/lists like dicts with the index as the key

        cdm = list()
        for key, val in items:
            text = str(key) + KEY_VAL_SEPARATOR + str(val)
            if key in ('transferred_bytes', 'total_bytes') and val > 1024:
                text += " (" + file_transfer_progress(val) + ")"
            kwargs: Dict[str, Any] = dict(text=text)
            if isinstance(val, (dict, list, tuple)):
                cls = 'IterableDisplayerButton'
                kwargs['tap_flow_id'] = id_of_flow('open', 'iterable_displayer', 'iterable sub item info')
                kwargs['tap_kwargs'] = dict(popup_kwargs=dict(title=text, data=val))
            else:
                cls = 'IterableDisplayerLabel'
            cdm.append(dict(cls=cls, attributes=kwargs))

        return cdm
