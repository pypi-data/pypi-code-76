"""
qr code displayer widget
========================

The popup widget :class:`QrDisplayerPopup` provided by this ae namespace portion is displaying QR codes.

The :class:`QrDisplayerPopup` is inherited from :class:`ae.kivy_app.FlowPopup` and is embedding the
Kivy Garden :mod:`kivy_garden.qrcode` module.

qr displayer popup usage
------------------------

To display a QR code instantiate :class:`QrDisplayerPopup` specifying in the `title` property of the popup the
string to encode to a QR image and in the `qr_content` property a short string describing the content of the string
to encode. After that call the `open` method::

    qr_displayer = QrDisplayerPopup(title="string to encode", qr_content="what to encode")
    qr_displayer.open()

Alternatively you can simply :meth:`change the application flow <ae.gui_app.change_flow>` to
`id_of_flow('open', 'qr_displayer')` (see also :ref:`application flow`)::

     main_app.change_flow(id_of_flow('open', 'qr_displayer'),
                          popup_kwargs=dict(title="string to encode",
                                            qr_content="what to encode"))

The label texts used by this popup widget are automatically translated into the german and spanish language via the
translation texts provided in the resources of this ae namespace portion.

.. note::
    If your app is providing i18n translations then the `qr_content` string has to be translated (e.g. by using
    :meth:`~ae.kivy_app.get_txt` or :meth:`~ae.i18n.get_text`) before it gets passed to the popup kwargs.

To support additional languages simply add the translations texts to your app's translation texts resources or
submit a PR to add them to this ae namespace portion.
"""
from kivy.lang import Builder                       # type: ignore
from kivy.properties import StringProperty          # type: ignore # pylint: disable=no-name-in-module

from ae.i18n import register_package_translations   # type: ignore
from ae.kivy_app import FlowPopup                   # type: ignore


__version__ = '0.1.3'


register_package_translations()

Builder.load_string('''\
#: import _q_ kivy_garden.qrcode

<QrDisplayerPopup>
    title: "string to codify"
    size_hint: 0.69 if app.landscape else 0.96, 0.96 if app.landscape else 0.69
    BoxLayout:
        orientation: 'vertical'
        spacing: '18sp'
        padding: '18sp'
        ImageLabel:
            text:
                # duplicate backslash (in \\n) prevents Kivy rule parsing exception
                _("The {root.qr_content} shown in the window title is underneath encoded as QR code.") \
                + _("\\nEither manually type/copy the window title string or use a QR code reader.") \
                + _("\\n\\nTap outside of this window to close it.")
            text_size: root.width - self.parent.padding[0] * 2.1, None
            size_hint_y: None
            height: self.texture_size[1] or self.height     # `or self.height` needed else height->42 w/ sideloading url
        QRCodeWidget:
            data: root.title
            show_border: False      # QRCodeWidget border bug (if root window pos of QR image is not at 0, 0); issue #13
''')


class QrDisplayerPopup(FlowPopup):
    """ qr code displayer. """
    qr_content = StringProperty()       #: string to name the content that get displayed as QR code
