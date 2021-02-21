import configparser
import errno
import gi
import os
from pathlib import Path
import psutil
import re
from shutil import which
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import GLib  # noqa: E402

from .gui import Gui # noqa E402

# ------------------------------------------------------------------------------


PAMIC_ERR_OK = 0
PAMIC_ERR_GENERIC_ERR = 1
PAMIC_ERR_MODULE_EXISTS = 2
PAMIC_ERR_NOT_ACTIVE = 3


# ------------------------------------------------------------------------------

PAMIC_CONFIG_DIR = f"{GLib.get_user_config_dir()}/pamic"
PAMIC_CONFIG_FILE = f"{PAMIC_CONFIG_DIR}/pamicg.conf"

# ------------------------------------------------------------------------------


class App:
    def __init__(self, setup):
        self.description = setup["description"]
        self.version = setup["version"]

        if "load-cl" in setup and setup["load-cl"] is True:
            self.load_cl = True
            self.no_gui = True if "no-gui" in setup and setup["no-gui"] is True else False
        else:
            self.load_cl = False
            self.no_gui = False

        self.gui = Gui(self, title=setup["name"], gladefile=setup["gladefile"])
        self.force_load = True
        self.config_restore()
        self.autostart_dir = f"{str(Path.home())}/.config/autostart"

    # --------------------------------------------------------------------------

    def run(self):
        path = [os.path.dirname(__file__)] + os.getenv("PATH").split(":")
        os.environ["PATH"] = ":".join(path)

        self.exit_if_missing_prog(["pactl", "pamic"])
        self.exit_if_not_running("pulseaudio")

        if self.parse_sources_and_sinks():
            if self.load_cl:
                self.reinstate_saved_cl()

            if not self.no_gui:
                self.gui.run(self.sources, self.sinks)
        else:
            self.gui.msgbox_exit_app("Pamic needs at least one source and one sink to work.")

    # --------------------------------------------------------------------------

    def exit_if_missing_prog(self, progs):
        missing_progs = [f"'{prog}'" for prog in progs if not which(prog)]

        if len(missing_progs) > 0:
            plural = "(s)" if len(missing_progs) > 1 else ""
            self.gui.msgbox_exit_app(
                f"Can't run pamicg without executable{plural}:"
                f" {' '.join(missing_progs)}"
            )

    # --------------------------------------------------------------------------

    def exit_if_not_running(self, prog):
        found = False
        for p in psutil.process_iter():
            try:
                if p.name() == prog:
                    found = True
                    break
            except psutil.NoSuchProcess:
                pass

        if not found:
            self.gui.msgbox_exit_app(f"Can't run pamicg: '{prog}' isn't running")

    # --------------------------------------------------------------------------

    def config_persist(self):
        print("saving config")
        config = configparser.ConfigParser()

        config["app"] = {}
        config["app"]["force_load"] = "True" if self.force_load else "False"

        self.gui.config_persist(config)

        try:
            os.mkdir(PAMIC_CONFIG_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            pass
        finally:
            with open(PAMIC_CONFIG_FILE, "w") as configfile:
                config.write(configfile)

    # --------------------------------------------------------------------------

    def config_restore(self):
        print("loading config")
        config = configparser.ConfigParser()
        config.read(PAMIC_CONFIG_FILE)

        if len(config):
            if config.has_section("app"):
                if config.has_option("app", "force_load"):
                    self.force_load = config.getboolean("app", "force_load")

            self.gui.config_restore(config)

    # --------------------------------------------------------------------------

    def parse_pactl_list(self, type):
        cmd = f"pactl list {type}"
        proc = subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE)
        out = proc.stdout.readlines()

        if len(out):
            grabname = re.compile("^Name: (.*)$")
            grabdesc = re.compile("^Description: (.*)$")

            stores = ([], [])

            grabbers = (grabname, grabdesc)
            grabber_index = 0

            for line in out:
                line = line.decode("utf-8").strip()
                m = grabbers[grabber_index].match(line)
                if m:
                    stores[grabber_index].append(m.group(1))

                    grabber_index += 1
                    if grabber_index > 1:
                        grabber_index = 0

            if len(stores[0]) is not len(stores[1]):
                print(
                    "Mismatch in the number of name and descriptions in 'pactl list"
                    f" {type}'"
                )
            elif len(stores[0]) == 0:
                print(f"pactl: No {type} found.")
            else:
                return (stores[0], stores[1])

        else:
            print(f"No output from 'pactl list {type}'")

        return None

    # --------------------------------------------------------------------------

    def parse_sources_and_sinks(self):
        sources = self.parse_pactl_list("sources")
        sinks = self.parse_pactl_list("sinks")

        if sources is None or sinks is None:
            return False

        self.sources = sources
        self.sinks = sinks

        return True

    # --------------------------------------------------------------------------

    def write_autostart_desktop_file(self, name, content):
        try:
            os.mkdir(self.autostart_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            pass
        finally:
            filename = f"{self.autostart_dir}/{name}.desktop"
            with open(filename, "w") as fh:
                fh.write("[Desktop Entry]")
                fh.write(content)

    # --------------------------------------------------------------------------

    def remove_autostart_desktop_file(self, name):
        filename = f"{self.autostart_dir}/{name}.desktop"
        filepath = Path(filename)
        if filepath.exists():
            try:
                filepath.unlink(missing_ok=True)
            except Exception as e:
                self.gui.msgbox(f"Can't remove '{filename}' ({e})")

    # --------------------------------------------------------------------------

    def set_autostart(self, reinstate, no_gui):
        if reinstate or not no_gui:
            reinstate_flag = "--load-cl" if reinstate else ""
            no_gui_flag = "--no-gui" if no_gui else ""
            content = f"""
Name=Pamicg
Comment=Run the Pamic Gui
Exec=pamicg {reinstate_flag} {no_gui_flag}
Icon=
StartupNotify=false
Terminal=false
Type=Application
"""
            self.write_autostart_desktop_file("pamic", content)
        else:
            self.remove_autostart_desktop_file("pamic")

    # --------------------------------------------------------------------------

    def get_autostart_status(self):
        retval = {"pamic": False, "pamicg": False}

        filename = f"{self.autostart_dir}/pamic.desktop"

        try:
            with open(filename, "r") as fh:
                for line in fh.readlines():
                    if line[0:5] == "Exec=":
                        retval["pamic"] = True if "--load-cl" in line else False
                        retval["pamicg"] = False if "--no-gui" in line else True
                        break
        except Exception:
            pass

        return retval

    # --------------------------------------------------------------------------

    def msg(self, msg, timeout=False):
        self.gui.msg(msg, timeout)

    # --------------------------------------------------------------------------

    def err(self, msg, timeout=False):
        self.gui.err(msg, timeout)

    # --------------------------------------------------------------------------

    def pamic(self, cmd, okay_msg):
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        out, _ = proc.communicate()

        print(cmd)

        if len(out):
            for line in out.decode("utf-8").splitlines():
                print(f"stdout> {line}")

        if proc.returncode == PAMIC_ERR_OK:
            self.msg(okay_msg, True)
        elif proc.returncode == PAMIC_ERR_NOT_ACTIVE:
            self.msg("pamic wasn't active", True)
        elif proc.returncode == PAMIC_ERR_MODULE_EXISTS:
            self.err(
                "pamic is already active. Maybe enable 'Force load' in Preferences?"
            )
        else:
            self.err(f"'{cmd}' returned {proc.returncode}'")

        return proc.returncode

    # --------------------------------------------------------------------------

    def reinstate_saved_cl(self):
        force = "--force" if self.force_load else ""
        return PAMIC_ERR_OK == self.pamic(
            f"pamic {force} --load-cl", "Re-instated saved configuration")

    # --------------------------------------------------------------------------

    def apply_echo_cancellation(self, source_index, sink_index, options):
        source = self.sources[0][source_index]
        sink = self.sinks[0][sink_index]
        force = "--force" if self.force_load else ""
        return PAMIC_ERR_OK == self.pamic(
            f"pamic {force} --save-cl -s {source} -S {sink} -l", "Applied echo cancellation"
        )

    # --------------------------------------------------------------------------

    def apply_noise_suppression(self, source_index, options):
        source = self.sources[0][source_index]
        force = "--force" if self.force_load else ""
        return PAMIC_ERR_OK == self.pamic(
            f"pamic {force} --save-cl -s {source} -l", "Applied noise suppression"
        )

    # --------------------------------------------------------------------------

    def unload(self):
        self.pamic("pamic -u", "pamic unloaded")
        return True


# ------------------------------------------------------------------------------
# vi sw=2:ts=2:et
