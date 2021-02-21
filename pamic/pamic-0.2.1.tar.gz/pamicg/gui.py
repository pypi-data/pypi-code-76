from enum import Enum
import os
import sys

try:
    import gi
except ImportError:
    print("Can't import 'gi' module. Please make sure pygobject is installed \
           from your package manager (e.g. apt, dnf, ...).")
    sys.exit(1)


gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk  # noqa: E402

# ------------------------------------------------------------------------------


class PamicMode(Enum):
    ECHO_CANCELLATION = 0
    NOISE_SUPPRESSION = 1


# ------------------------------------------------------------------------------


class Handler:
    def __init__(self, gui):
        self.gui = gui

    def onDestroy(self, *args):
        self.gui.quit()

    def on_windowMain_destroy(self, *args):
        self.gui.quit()

    def on_rbEC_toggled(self, button):
        if button.get_active():
            self.gui.tabBox.set_current_page(0)
            self.gui.mode = PamicMode.ECHO_CANCELLATION
            self.gui.msg("")
            self.gui.update_apply_button()

    def on_rbNS_toggled(self, button):
        if button.get_active():
            self.gui.tabBox.set_current_page(1)
            self.gui.mode = PamicMode.NOISE_SUPPRESSION
            self.gui.msg("")
            self.gui.update_apply_button()

    def on_btnApply_clicked(self, button):
        self.gui.apply()

    def on_btnOptions_clicked(self, button):
        self.gui.run_options()

    def on_btnRefresh_clicked(self, button):
        self.gui.refresh()

    def on_btnAbout_clicked(self, button):
        self.gui.run_about()

    def on_miApply_activate(self, mi):
        self.gui.apply()

    def on_miUnload_activate(self, mi):
        self.gui.unload()


# ------------------------------------------------------------------------------


def msg_timer(gui):
    del gui.msg_timer
    gui.msg_timer = None
    gui.lblMsg.set_text("")


# ------------------------------------------------------------------------------


class Gui:
    def __init__(self, app, title, gladefile):
        self.app = app
        self.mode = PamicMode.ECHO_CANCELLATION
        self.msg_timer = None

        self.persisted_ecSource = None
        self.persisted_ecSink = None
        self.persisted_nsSource = None

        self.display_names = False
        self.display_monitors = False

        self.old_rbNS_tooltip = None

        self.builder = Gtk.Builder()
        self.builder.add_from_file(gladefile)
        self.builder.connect_signals(Handler(self))

        self.wMain = self.builder.get_object("windowMain")
        self.wMain.set_title(title)

        self.dlgOptions = self.builder.get_object("windowOptions")
        self.dlgOptions.set_title(f"{title} - Preferences")

        self.dlgAbout = self.builder.get_object("dlgAbout")
        self.dlgAbout.set_comments(self.app.description)
        self.dlgAbout.set_version(self.app.version)

        self.rbNS = self.builder.get_object("rbNS")

        self.cbECSource = self.builder.get_object("cbECSource")
        self.cbECSink = self.builder.get_object("cbECSink")
        self.cbNSSource = self.builder.get_object("cbNSSource")

        self.btnApply = self.builder.get_object("btnApply")
        self.lblMsg = self.builder.get_object("lblMsg")
        self.tabBox = self.builder.get_object("tabBox")

    # --------------------------------------------------------------------------

    def msg(self, msg, timeout=False):
        self.lblMsg.set_text(msg)
        if len(msg):
            print(msg)
        if timeout:
            if self.msg_timer is not None:
                del self.msg_timer
            self.msg_timer = GLib.timeout_add(20000, msg_timer, self)

    # --------------------------------------------------------------------------

    def err(self, msg, timeout=False):
        self.msg(f"ERR: {msg}", timeout)

    # --------------------------------------------------------------------------

    def msgbox_response(self, widget, response_id):
        self.quit()

    # --------------------------------------------------------------------------

    def msgbox_exit_app(self, msg):
        print(msg)
        msgbox = Gtk.MessageDialog(
            parent=None,
            flags=Gtk.DialogFlags.MODAL,
            type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.CLOSE,
            message_format=msg,
        )
        msgbox.set_title("pamic")
        msgbox.connect("response", self.msgbox_response)
        msgbox.show()
        Gtk.main()
        sys.exit()

    # --------------------------------------------------------------------------

    def run(self, sources, sinks):
        self.check_librnnoise()
        self.load_sources_and_sinks(sources, sinks)
        self.set_active_devices(
            self.persisted_ecSource, self.persisted_ecSink, self.persisted_nsSource
        )
        self.wMain.show_all()
        Gtk.main()

    # --------------------------------------------------------------------------

    def quit(self):
        Gtk.main_quit()

    # --------------------------------------------------------------------------

    def update_apply_button(self):
        self.msg("")
        sink_okay = True
        source_okay = True

        if self.mode == PamicMode.ECHO_CANCELLATION and 0 == len(self.app.sinks):
            sink_okay = False

        if 0 == len(self.app.sources):
            source_okay = False

        if not sink_okay or not source_okay:
            if not sink_okay:
                if not source_okay:
                    devs = "source or sink"
                else:
                    devs = "sink"
            else:
                devs = "source"
            self.msg(f"Can't apply: no {devs} available")

        self.btnApply.set_sensitive(sink_okay and source_okay)

    # --------------------------------------------------------------------------

    def check_librnnoise(self):
        found = False
        libname = "librnnoise_ladspa.so"
        url = "https://github.com/werman/noise-suppression-for-voice"
        libpath = os.getenv("LD_LIBRARY_PATH")
        if libpath is None:
            libpath = "/usr/local/lib:/usr/lib:/lib"

        for dir in libpath.split(":"):
            if os.path.isfile(os.path.join(dir, libname)):
                found = True
                break

        if not found:
            self.old_rbNS_tooltip = self.rbNS.get_tooltip_markup()
            self.rbNS.set_tooltip_markup(
                "To enable high quality, standalone Noise suppression, install"
                f" '{libname}' from:\n\n\t{url}\n\nand Refresh or restart"
            )
        elif self.old_rbNS_tooltip is not None:
            self.rbNS.set_tooltip_markup(self.old_rbNS_tooltip)
            self.old_rbNS_tooltip = None

        self.rbNS.set_sensitive(found)

    # --------------------------------------------------------------------------

    def load_sources_and_sinks(self, sources, sinks, force=False):
        for (cb, arrs) in [
            (self.cbECSource, sources),
            (self.cbECSink, sinks),
            (self.cbNSSource, sources),
        ]:
            # Load/refresh data
            model = cb.get_model()

            if force or len(model) == 0:
                if force and len(model) > 0:
                    model.clear()

                for (name, desc) in zip(arrs[0], arrs[1]):
                    if name[0:6] != "pamic_" and (
                        self.display_monitors or name[-8:] != ".monitor"
                    ):
                        model.append([desc, f"[ {name} ]"])

            cb.set_model(model)

            # Reset view
            cb.clear()

            cell = Gtk.CellRendererText()
            cb.pack_start(cell, True)
            cb.add_attribute(cell, "text", 0)

            if self.display_names:
                cell = Gtk.CellRendererText()
                cb.pack_start(cell, True)
                cb.add_attribute(cell, "text", 1)

        self.update_apply_button()

    # --------------------------------------------------------------------------

    def get_cb_index(self, cb):
        index = cb.get_active()
        if index < 0:
            print("No item selected")
            cb.grab_focus()
            return None
        return index

    # --------------------------------------------------------------------------

    def get_active_devices(self):
        ecSource = self.cbECSource.get_active()
        ecSink = self.cbECSink.get_active()
        nsSource = self.cbNSSource.get_active()
        return (
            self.app.sources[0][ecSource] if ecSource >= 0 else None,
            self.app.sinks[0][ecSink] if ecSink >= 0 else None,
            self.app.sources[0][nsSource] if nsSource >= 0 else None,
        )

    # --------------------------------------------------------------------------

    def set_active_devices(self, ec_source, ec_sink, ns_source):
        found = 0
        for (dev, devices, cb) in [
            (ec_source, self.app.sources[0], self.cbECSource),
            (ec_sink, self.app.sinks[0], self.cbECSink),
            (ns_source, self.app.sources[0], self.cbNSSource),
        ]:
            if dev is None:
                cb.set_active(-1)
                found += 1
            else:
                for (idx, item) in enumerate(devices):
                    if item == dev:
                        cb.set_active(idx)
                        found += 1
                        break

        return True if found == 3 else False

    def config_persist(self, config):
        config["gui"] = {}
        config["gui"]["display_monitors"] = "True" if self.display_monitors else "False"
        config["gui"]["display_names"] = "True" if self.display_names else "False"

        (ecSource, ecSink, nsSource) = self.get_active_devices()
        config["devices"] = {}
        config["devices"]["ecSource"] = ecSource if ecSource else "None"
        config["devices"]["ecSink"] = ecSink if ecSink else "None"
        config["devices"]["nsSource"] = nsSource if nsSource else "None"

    # --------------------------------------------------------------------------

    def config_restore(self, config):
        if config.has_section("gui"):
            if config.has_option("gui", "display_monitors"):
                self.display_monitors = config.getboolean("gui", "display_monitors")

            if config.has_option("gui", "display_names"):
                self.display_names = config.getboolean("gui", "display_names")

        if config.has_section("devices"):
            ecSource, ecSink, nsSource = (None, None, None)

            if config.has_option("devices", "ecSource"):
                ecSource = config["devices"]["ecSource"]
                if ecSource == "None":
                    ecSource = None
            if config.has_option("devices", "ecSink"):
                ecSink = config["devices"]["ecSink"]
                if ecSink == "None":
                    ecSink = None
            if config.has_option("devices", "nsSource"):
                nsSource = config["devices"]["nsSource"]
                if nsSource == "None":
                    nsSource = None

            self.persisted_ecSource = ecSource
            self.persisted_ecSink = ecSink
            self.persisted_nsSource = nsSource

    # --------------------------------------------------------------------------

    def refresh(self):
        self.check_librnnoise()
        (ec_source, ec_sink, ns_source) = self.get_active_devices()
        if self.app.parse_sources_and_sinks():
            self.load_sources_and_sinks(self.app.sources, self.app.sinks, True)
            all_ok = self.set_active_devices(ec_source, ec_sink, ns_source)
            self.msg("Refreshed", True)
            return all_ok
        else:
            self.msg("Failed to parse pactl. See console output(?)", True)
        return False

    # --------------------------------------------------------------------------

    def run_about(self):
        self.msg("")
        response = self.dlgAbout.run()
        if response != Gtk.ResponseType.DELETE_EVENT:
            self.msg(f"erk: {response}")
        self.dlgAbout.hide()

    # --------------------------------------------------------------------------

    def run_options(self):
        # Setup widgets with current values
        chkForceLoad = self.builder.get_object("chkForceLoad")
        chkForceLoad.set_active(self.app.force_load)
        chkDisplayMonitors = self.builder.get_object("chkDisplayMonitors")
        chkDisplayMonitors.set_active(self.display_monitors)
        chkDisplayDevNames = self.builder.get_object("chkDisplayDevNames")
        chkDisplayDevNames.set_active(self.display_names)

        autostart_status = self.app.get_autostart_status()
        old_autostart_pamic = autostart_status["pamic"]
        old_autostart_pamicg = autostart_status["pamicg"]

        chkAutostartPamic = self.builder.get_object("chkAutostartPamic")
        chkAutostartPamic.set_active(old_autostart_pamic)

        chkAutostartPamicg = self.builder.get_object("chkAutostartPamicg")
        chkAutostartPamicg.set_active(old_autostart_pamicg)

        response = self.dlgOptions.run()

        if response == Gtk.ResponseType.OK:
            # Set values to widget indication
            refresh_sources_and_sinks = False

            self.app.force_load = chkForceLoad.get_active()

            new_display_names = chkDisplayDevNames.get_active()
            if new_display_names != self.display_names:
                self.display_names = new_display_names
                refresh_sources_and_sinks = True

            new_display_monitors = chkDisplayMonitors.get_active()
            if new_display_monitors != self.display_monitors:
                self.display_monitors = new_display_monitors
                refresh_sources_and_sinks = True

            if refresh_sources_and_sinks:
                self.refresh()

            new_autostart_pamic = chkAutostartPamic.get_active()
            new_autostart_pamicg = chkAutostartPamicg.get_active()
            if new_autostart_pamic != old_autostart_pamic or new_autostart_pamicg != old_autostart_pamicg:
                self.app.set_autostart(new_autostart_pamic, not new_autostart_pamicg)

        self.dlgOptions.hide()

    # --------------------------------------------------------------------------

    def get_ec_options(self):
        return None

    # --------------------------------------------------------------------------

    def get_ns_options(self):
        return None

    # --------------------------------------------------------------------------

    def apply(self):
        applied = False
        msg = None

        disappeared = not self.refresh()

        if self.mode == PamicMode.NOISE_SUPPRESSION:
            source = self.get_cb_index(self.cbNSSource)
            if source is not None:
                options = self.get_ns_options()
                applied = self.app.apply_noise_suppression(source, options)
            else:
                msg = "A source needs to be selected."
        else:
            sink = self.get_cb_index(self.cbECSink)
            source = self.get_cb_index(self.cbECSource)

            if source is None and sink is None:
                msg = "A source and sink need to be selected."
            elif source is None:
                msg = "A source needs to be selected."
            elif sink is None:
                msg = "A sink needs to be selected."
            else:
                options = self.get_ec_options()
                applied = self.app.apply_echo_cancellation(source, sink, options)

        if msg:
            disappeared = "Available devices changed. " if disappeared else ""
            self.msg(f"{disappeared}{msg}")

        if applied:
            self.app.config_persist()

    # --------------------------------------------------------------------------

    def unload(self):
        self.app.unload()


# ------------------------------------------------------------------------------
