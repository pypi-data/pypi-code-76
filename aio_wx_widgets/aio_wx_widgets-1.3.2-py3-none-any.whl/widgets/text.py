"""Text widgets."""

import logging
from typing import Optional, Union

import wx

from aio_wx_widgets.colors import GREEN
from aio_wx_widgets.const import is_debugging
from aio_wx_widgets.core.base_widget import BaseWidget
from aio_wx_widgets.core.binding import Binding, OneWayBindable

_LOGGER = logging.getLogger(__name__)

__all__ = ["Text"]


def _get_font_info(current_font: wx.Font, font_size: float = 1, bold=False) -> wx.Font:
    font = wx.Font()

    if font_size != 1:
        current_font_size = current_font.GetPointSize()
        new_font_size = int(font_size * current_font_size)
        _LOGGER.debug(
            "Debug ratio of %s results in absolute font size of %s",
            font_size,
            new_font_size,
        )
        font.SetPointSize(new_font_size)

    if bold:
        font.MakeBold()

    return font


class Text(BaseWidget):
    """Static text."""

    HOR_CENTER = wx.ALIGN_CENTRE_HORIZONTAL
    HOR_RIGHT = wx.ALIGN_RIGHT
    HOR_LEFT = wx.ALIGN_LEFT

    def __init__(
        self,
        text="",
        font_size: float = 1,
        color: Union[int, Binding, None] = None,
        enabled: Union[bool, Binding] = True,
        binding: Optional[Binding] = None,
        bold=False,
        wrap=False,
        min_width=-1,
        hor_align: Optional[int] = None,
    ):
        """Init.

        Args:
            text:
            font_size: Font size ratio.
        """
        value_binding = (
            OneWayBindable(binding, self._set_ui_value) if binding is not None else None
        )

        super().__init__(
            wx.StaticText(),
            min_width=min_width,
            value_binding=value_binding,
            enabled=enabled,
        )
        self._parent = None
        self._color = color
        self._text = text
        self._wrap = wrap

        self._font = _get_font_info(self.ui_item.GetFont(), font_size, bold=bold)
        self._color_binding = None
        self._previous_size = (0, 0)
        self._hor_align = hor_align

    def _set_ui_value(self, value):
        self.set_text(value)

    def _get_style(self) -> int:
        style = 0

        if self._hor_align:
            style = style | self._hor_align

        return style

    def init(self, parent):

        self._parent = parent
        self._parent.Bind(wx.EVT_SIZE, self._on_parent_size)

        self.ui_item.Create(parent, style=self._get_style())

        if self._font:
            self.ui_item.SetFont(self._font)

        if is_debugging():
            self.ui_item.SetBackgroundColour(GREEN)
        self._init()
        self._parent.PostSizeEvent()

    def __call__(self, parent):
        self.init(parent)
        return self

    def _on_parent_size(self, evt):
        container = self.ui_item.ContainingSizer
        _LOGGER.debug(container.Size)

        if container.Size[0] == 0:
            _LOGGER.debug("Not setting text.")
        elif self._previous_size[0] == container.Size[0]:
            _LOGGER.debug("Previous size is the same skipping.")
        else:
            self._previous_size = container.Size
            smaller_size = (self.ui_item.Size[0], -1)
            self._set_text(client_size=smaller_size)
            self.ui_item.Parent.Refresh()

        evt.Skip()

    def _set_text(self, color=None, client_size=None):

        self.ui_item.SetLabel(str(self._text))
        if self._wrap:
            if client_size:
                self.ui_item.Wrap(client_size[0])

    def set_text(self, text, color=None):
        """Set or change the text."""
        self._text = str(text)
        self._set_text(color)

    def _set_color(self, color):
        """Set text color when color binding changes."""
        _LOGGER.debug("Setting color to : %s", color)

        self.ui_item.SetForegroundColour(color)
        self._parent.Refresh()

    def _make_bindings(self):
        if self._color is not None and isinstance(self._color, Binding):
            self._color_binding = OneWayBindable(self._color, self._set_color)
            self._color_binding.make_binding()
        super()._make_bindings()
