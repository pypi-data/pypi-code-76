"""
kivy mixin and widgets to integrate a sideloading server in your app
====================================================================

This namespace portion provides widgets and a mixin class for you main app instance to easily integrate and control
the `ae sideloading server <ae.sideloading_server>` into your :mod:`Kivy app <ae.kivy_app>`.


kivy sideloading integration into your main app class
-----------------------------------------------------

Add the :class:`SideloadingMainAppMixin` mixin provided by this ae namespace portion to your main app class::

    class MyMainAppClass(SideloadingMainAppMixin, KivyMainApp):

The sub app of the sideloading server will then automatically be instantiated when your app starts and will initialize
the :attr:`~SideloadingMainAppMixin.sideloading_app` attribute with this sub app instance.

.. hint::
    If you prefer to instantiate the sideloading server sub app manually then specify :class:`SideloadingMainAppMixin`
    after :class:`~ae.kivy_app.KivyMainApp` in the declaration of your main app class.

Adding `sideloading_active` to the `:ref:`app state variables` of your app's :ref:`config files` will ensure that the
running status of the sideloading server gets automatically stored persistent on pause or stop of the app for the next
app start.

The running status of the sideloading server will be restored in the app start event handler method
(:meth:`~SideloadingMainAppMixin.on_app_start).

To manually start it to offer the APK of the embedding app call the
:meth:`#SideloadingMainAppMixin.on_sideloading_server_start` method passing an empty string and dict::

    self.on_sideloading_server_start("", dict())

.. hint:: when you pass the dict with a number in a 'port' key then this number will be used as server listening port.

If no 'port' gets passed then :class:`SideloadingMainAppMixin` will calculate an individual port number from the
first character of the :attr:`~ae.core.AppBase.app_name` of the app mixing in this class. This is to prevent
the server socket error `[Errno 98] Address already in use` if two different applications with sideloading are
running on the same device and want to offer sideloading.

To manually pause the sideloading server call the
:meth:`#SideloadingMainAppMixin.on_sideloading_server_stop` method passing an empty string and dict::

    self.on_sideloading_server_stop("", dict())


usage of the sideloading button
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This ae namespace portion is additionally providing the `SideloadingButton` flow button widget to integrate it in
your Kivy app. This button can be used to:

* start or stop the sideloading server,
* select a file for sideloading via the :class:`~ae.kivy_file_chooser.FileChooserPopup`.
* display file info like full file path and file length.
* display the URL of your sideloading server as QR code to allow connections from other devices.

To optionally integrate this `SideloadingButton` into your app add it to the root layout in your app's main kv file
with the `id` `sideloading_button`::

    MyRootLayout:
        ...
        SideloadingButton:
            id: sideloading_button

If the sideloading server is not active and the user is clicking the `SideloadingButton` then this portion will
first check if the `Downloads` folder of the device is containing a APK file for the running app and if yes then the
sideloading server will be started providing the found APK file.

If the sideloading server is instead already running/active and the user is tapping on the `SideloadingButton` then a
drop down menu will be shown with options to (1) display info of the sideloading file, (2) select a new file, (3)
display the sideloading server URL as QR code or (4) stop the sideloading server.


dependencies/requirements in buildozer.spec
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To build a Android APK with the kivy sideloading server integrated, make sure that the following external packages
are specified in the `requirements` setting of the `[app]` section of your buildozer.spec file.

* ae.kivy_file_chooser
* ae.kivy_iterable_displayer
* ae.kivy_qr_displayer
* ae.kivy_sideloading
* ae.sideloading_server
* kivy_garden.qrcode
* qrcode

Additionally all the packages and ae namespace portions required by the above packages have to be included. E.g. the
`GlslTester demo app <https://gibhub.com/AndiEcker/GlslTester>`_ includes the following packages::

requirements = android, hostpython3==3.7.5, python3==3.7.5, kivy==2.0.0,
    plyer, qrcode, kivy_garden.qrcode,
    ae.base, ae.files, ae.paths, ae.deep, ae.droid, ae.inspector, ae.i18n,
    ae.updater, ae.core, ae.literal, ae.console, ae.parse_date, ae.gui_app,
    ae.gui_help, ae.kivy_auto_width, ae.kivy_dyn_chi, ae.kivy_help,
    ae.kivy_relief_canvas, ae.kivy_app, ae.kivy_user_prefs, ae.kivy_glsl,
    ae.kivy_file_chooser, ae.sideloading_server, ae.kivy_sideloading,
    ae.kivy_iterable_displayer, ae.kivy_qr_displayer


sideloading server life cycle
-----------------------------

To activate the sideloading server to offer a different file, specify the path (or glob file mask) of the file to be
offered/available via sideloading in the :attr:`~SideloadingMainAppMixin.sideloading_file_mask` attribute and then call
the method :meth:`~SideloadingMainAppMixin.on_sideloading_server_start`. This method will check if the specified file
exists and if yes then it will start the sideloading server. If you specify a file mask instead of a concrete file path
then this method will check if exists exactly one file matching the file mask.

After the start of the sideloading server the :attr:`~SideloadingMainAppMixin.sideloading_file_ext` attribute will
contain the file extension of the file available via sideloading.

The sideloading server will automatically be shut down on quit/close of the embedding app. You can alternatively stop
the sideloading server manually at any time by calling the :meth:`~SideloadingMainAppMixin.on_sideloading_server_stop`
method.
"""
import os

from typing import Callable, Optional

from kivy.app import App                                                                        # type: ignore
from kivy.clock import mainthread                                                               # type: ignore
from kivy.lang import Builder                                                                   # type: ignore
from kivy.uix.widget import Widget                                                              # type: ignore

from ae.files import file_transfer_progress                                                     # type: ignore
from ae.i18n import register_package_translations                                               # type: ignore
from ae.gui_app import EventKwargsType, id_of_flow, register_package_images, update_tap_kwargs  # type: ignore
from ae.kivy_app import FlowDropDown, get_txt                                                   # type: ignore
from ae.sideloading_server import (                                                             # type: ignore
    DEFAULT_FILE_MASK, FILE_COUNT_MISMATCH, server_factory, update_handler_progress, SideloadingServerApp)


__version__ = '0.1.8'


register_package_images()
register_package_translations()


Builder.load_string('''\
#: import _f_ ae.kivy_file_chooser
#: import _i_ ae.kivy_iterable_displayer
#: import _q_ ae.kivy_qr_displayer

<SideloadingMenuPopup>

<SideloadingButton@FlowButton>
    tap_flow_id:
        id_of_flow('open', 'sideloading_menu') if app.app_states['sideloading_active'] else \
        id_of_flow('start', 'sideloading_server')
    tap_kwargs: update_tap_kwargs(self)
    on_alt_tap: app.main_app.change_flow(id_of_flow('open', 'sideloading_menu'), **update_tap_kwargs(self))
    text: app.main_app.sideloading_file_ext if app.app_states['sideloading_active'] else ""
    source:
        "" if app.app_states['sideloading_active'] else \
        app.main_app.img_file('sideloading_activate', app.app_states['font_size'], \
        app.app_states['light_theme'])
    size_hint_x: None
    width: self.height * (3.3 if app.landscape else 2.1)
    _progress: app.app_states['sideloading_active']
    ellipse_fill_ink: app.font_color[:3] + (0.69, )
    ellipse_fill_pos: self.x, self.top - app.app_states['font_size'] / 3.0
    ellipse_fill_size: self.width * (self._progress and self._progress[0] or 0), app.app_states['font_size'] / 3.0
    square_fill_ink: app.font_color[:3] + (0.69, )
    square_fill_pos: self.pos
    square_fill_size: self.width * (self._progress and self._progress[1] or 0), app.app_states['font_size'] / 3.0
    relief_square_inner_colors:
        relief_colors((1.0, 1.0, 0.3) if app.app_states['sideloading_active'] else (1.0, 1.0, 1.0))
    relief_square_inner_lines: int(self.height / (3.6 if app.app_states['sideloading_active'] else 2.1))
''')


class SideloadingMenuPopup(FlowDropDown):
    """ dropdown menu to control sideloading server. """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        app = App.get_running_app()
        main_app = app.main_app
        sideloading_button = app.root.ids.sideloading_button

        self.child_data_maps = list()

        file_path = main_app.sideloading_app.file_path
        if file_path or main_app.debug:
            data = dict(mask=main_app.sideloading_file_mask or DEFAULT_FILE_MASK,
                        extension=main_app.sideloading_file_ext, path=file_path)
            if file_path:
                file_size = os.path.getsize(file_path)
                data['size'] = file_transfer_progress(file_size) + (f" ({file_size} bytes)" if main_app.debug else "")
            self.child_data_maps.append(dict(kwargs=dict(
                text=get_txt("sideloading file info"),
                tap_flow_id=id_of_flow('open', 'iterable_displayer'),
                tap_kwargs=dict(popups_to_close=(self, ),
                                popup_kwargs=dict(title=os.path.basename(file_path), data=data),
                                tap_widget=sideloading_button))))

        self.child_data_maps.append(dict(kwargs=dict(
            text=get_txt("select file for sideloading"),
            tap_flow_id=id_of_flow('open', 'file_chooser'),
            tap_kwargs=dict(popups_to_close=(self, ),
                            popup_kwargs=dict(submit_to='sideloading_file_mask'),
                            tap_widget=sideloading_button))))

        self.child_data_maps.append(dict(kwargs=dict(
            text=get_txt("display sideloading address/QR code"),
            tap_flow_id=id_of_flow('open', 'qr_displayer'),
            tap_kwargs=dict(popups_to_close=(self, ),
                            popup_kwargs=dict(title=main_app.sideloading_app.server_url(),
                                              qr_content=get_txt("sideloading url")),
                            tap_widget=sideloading_button))))

        action = 'stop' if main_app.sideloading_active else 'start'
        self.child_data_maps.append(dict(kwargs=dict(
            text=get_txt(action + " sideloading server"),
            tap_flow_id=id_of_flow(action, 'sideloading_server'),
            tap_kwargs=dict(popups_to_close=(self, ),
                            tap_widget=sideloading_button))))


class SideloadingMainAppMixin:
    """ mixin class with default methods for the main app class. """
    # abstract attributes/properties and methods provided by the main app instance where this get mixed into
    app_name: str
    change_app_state: Callable
    change_flow: Callable
    dpo: Callable
    framework_root: Widget
    show_message: Callable
    vpo: Callable

    # implemented attributes
    sideloading_active: tuple                           #: app state flag if sideloading server is running
    sideloading_app: SideloadingServerApp               #: http sideloading server console app
    sideloading_file_ext: str = "."                     #: extension of selected sideloading file
    sideloading_file_mask: str = ""                     #: file mask of sideloading file

    def on_app_start(self):
        """ app start event. """
        self.vpo("SideloadingMainAppMixin.on_app_start")

        # instantiate sideloading sub app and optionally simple http server for apk sideloading
        self.sideloading_app = server_factory(task_id_func=id_of_flow)
        self.sideloading_app.run_app()

        super_method: Optional[Callable] = getattr(super(), 'on_app_start', None)
        if callable(super_method):
            super_method()                      # pylint: disable=not-callable

    def on_app_started(self):
        """ initialize and start renderers after kivy app, window and widget root got initialized. """
        super_method: Optional[Callable] = getattr(super(), 'on_app_started', None)
        if callable(super_method):
            super_method()                      # pylint: disable=not-callable

        if self.sideloading_active:
            self.on_sideloading_server_start("", dict())

    def on_file_chooser_submit(self, file_path: str, chooser_popup: Widget):
        """ event callback from FileChooserPopup.on_submit() on selection of file.

        :param file_path:       path string of selected file.
        :param chooser_popup:   file chooser popup/container widget.
        """
        pre = "SideloadingMainAppMixin.on_file_chooser_submit: "
        self.vpo(f"{pre}file={file_path}; popup={chooser_popup}")

        if chooser_popup.submit_to != 'sideloading_file_mask':
            self.dpo(f"{pre}called with submit_to='{chooser_popup.submit_to}'")
            return
        if not os.path.isfile(file_path):
            self.show_message(get_txt("folders can't be send via sideloading"), title=get_txt("select single file"))
            return

        self.sideloading_file_mask = file_path
        if self.sideloading_active:
            self.on_sideloading_server_stop("", dict())
        self.on_sideloading_server_start("", dict())
        chooser_popup.dismiss()

    def on_sideloading_server_start(self, _flow_key: str, event_kwargs: EventKwargsType) -> bool:
        """ start the sideloading server.

        :param _flow_key:       unused/empty flow key.
        :param event_kwargs:    event kwargs:
                                * 'port': TCP/IP server listening port.
                                * 'tap_widget': button instance that initiated the start of the server.
        :return:                always True to confirm change of flow id.
        """
        @mainthread
        def _upd_pr(client_ip: str = "", transferred_bytes: int = -6, total_bytes: int = 0, **kwargs):
            """ update handler attributes for sideloading_app.client_progress and sideloading progress bars. """
            update_handler_progress(
                client_ip=client_ip, transferred_bytes=transferred_bytes, total_bytes=total_bytes, **kwargs)
            client_ips = list(sap.client_handlers.keys())
            if client_ips and total_bytes:
                fore_last, last = self.sideloading_active
                if client_ip == client_ips[-1]:
                    last = transferred_bytes / total_bytes
                elif len(client_ips) > 1 and client_ip == client_ips[-2]:
                    fore_last = transferred_bytes / total_bytes
                self.change_app_state('sideloading_active', (fore_last, last))

        pre = "SideloadingMainAppMixin.on_sideloading_server_start: "
        self.vpo(f"{pre}event_kwargs={event_kwargs}")

        if self.sideloading_active:
            self.vpo(f"{pre}stop running sideloading server to restart")
            self.on_sideloading_server_stop("", dict())

        sap = self.sideloading_app

        sap.set_opt('port', event_kwargs.get('port', 33300 + ord(self.app_name[0])), save_to_config=False)

        err = sap.start_server(file_mask=self.sideloading_file_mask, progress=_upd_pr, threaded=True)
        if err:
            self.show_message(err, title=get_txt("server start error"))
            if FILE_COUNT_MISMATCH in err and 'tap_widget' in event_kwargs:  # let user select APK if match-count != 1
                self.change_flow(id_of_flow('open', 'file_chooser'),
                                 **update_tap_kwargs(event_kwargs['tap_widget'],
                                                     popup_kwargs=dict(submit_to='sideloading_file_mask')))
            return False

        self.sideloading_file_ext = os.path.splitext(sap.file_path)[1][1:]
        if event_kwargs:    # only display qr code if called from sideloading_button
            url = sap.server_url()
            self.change_flow(id_of_flow('open', 'qr_displayer'),
                             popup_kwargs=dict(title=url, qr_content=get_txt("sideloading url")))
        self.change_app_state('sideloading_active', (0.0, 0.0))

        return True

    def on_sideloading_server_stop(self, _flow_key: str, _event_kwargs: EventKwargsType) -> bool:
        """ stop a running sideloading http server.

        :param _flow_key:       unused/empty flow key.
        :param _event_kwargs:   unused event kwargs.
        :return:                always True to confirm change of flow id.
        """
        self.vpo("SideloadingMainAppMixin.on_sideloading_server_stop")

        self.sideloading_app.stop_server()
        self.change_app_state('sideloading_active', ())

        return True
