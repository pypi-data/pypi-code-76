#!/usr/bin/env python3
import os
import re
import base64
import traceback
import signal
from time import sleep
from subprocess import Popen
from mimetypes import MimeTypes
from dogtail.tree import root
from dogtail.utils import config
from dogtail.rawinput import keyCombo
from qecore.utility import run
from qecore.logger import QELogger
from qecore.application import Application
from qecore.flatpak import Flatpak
from qecore.icons import qecore_icons, QECoreIcon


log = QELogger()

class TestSandbox:
    def __init__(self, component, logging=False):
        """
        :type component: str
        :param component: Name of the component that is being tested.

        :type logging: bool
        :param logging: Turn on or off logging of this submodule.
        """

        self.logging = logging

        if self.logging:
            log.info(f"__init__(self, component={component}, logging={str(self.logging)})")

        self.component = component
        self.current_scenario = None
        self.background_color = None
        self.background_image_revert = False
        self.background_image_location = None

        self.enable_animations = None

        self.enable_close_yelp = True

        self.logging_start = None
        self.screenshot_run_result = None

        self.record_video = True
        self.record_video_pid = None

        self.attach_video = True
        self.attach_video_on_pass = False

        self.attach_journal = True
        self.attach_journal_on_pass = False

        self.attach_screenshot = True
        self.failed_test = False

        self.attach_faf = True
        self.attach_faf_on_pass = True
        self.logging_cursor = None

        self.workspace_return = False

        self.set_keyring = True
        self.keyring_process_pid = None

        self.wait_for_stable_video = True

        self.production = True

        self.timeout_handling = True

        self.after_scenario_hooks = []
        self.reverse_after_scenario_hooks = False

        self.change_title = True
        self.session_icon_to_title = True
        self.default_application_icon_to_title = False

        self.applications = []
        self.default_application = None
        self.retrieve_session_data()
        self.set_g_debug_environment_variable()
        self.wait_until_shell_becomes_responsive()

        self.shell = root.application("gnome-shell")


    def before_scenario(self, context, scenario):
        """
        Actions that are to be executed before every scenario.

        :type context: <behave.runner.Context>
        :param context: Pass this object from environment file.

        :type scenario: <Scenario>
        :param scenario: Pass this object from environment file.
        """

        if self.logging:
            log.info(f"before_scenario(self, context, scenario) test: {scenario.tags[-1]}")

        self.failed_test = False

        self.set_animations()

        self.current_scenario = scenario.tags[-1]
        self.set_log_start_time()
        self.overview_action("hide")
        self.set_typing_delay(0.2)
        self.set_debug_to_stdout_as(False)
        self.close_yelp()
        self.close_initial_setup()
        self.copy_data_folder()
        self.set_blank_screen_to_never()

        self.set_up_embedding(context)

        if self.change_title:
            self.set_title(context)

        if self.timeout_handling:
            self.set_timeout_handling()

        if self.record_video and self.production:
            self.start_recording()

        self.detect_keyring()
        self.return_to_home_workspace()


    def after_scenario(self, context, scenario):
        """
        Actions that are to be executed after every scenario.

        :type context: <behave.runner.Context>
        :param context: Pass this object from environment file.

        :type scenario: <Scenario>
        :param scenario: Pass this object from environment file.
        """

        if self.logging:
            log.info(f"after_scenario(self, context, scenario) test: {scenario.tags[0]}")

        if scenario.status == "failed":
            self.failed_test = True

        if self.attach_screenshot and self.failed_test:
            self.capture_image()

        if self.background_image_revert:
            self.revert_background_image()

        if self.record_video:
            self.stop_recording()

        self.overview_action("hide")

        for application in self.applications:
            application.kill_application()

        if self.attach_screenshot and self.failed_test:
            self.attach_screenshot_to_report(context)

        if self.attach_journal and (self.failed_test or self.attach_journal_on_pass):
            self.attach_journal_to_report(context)

        if self.attach_video and (self.failed_test or self.attach_video_on_pass):
            self.attach_video_to_report(context)

        if self.attach_faf and (self.failed_test or self.attach_faf_on_pass):
            self.attach_abrt_link_to_report(context)

        self.after_scenario_hooks_process(context)


    def gracefull_exit(self, signum, frame):
        """
        If killed externally, run user defined hooks not to break tests that will be executed next.

        .. note::

            Do **NOT** call this by yourself. This method is called when killed externally (timeout).
        """

        assert False, f"Timeout: received signal: '{signum}'"


    def start_recording(self):
        """
        Start recording the video.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`before_scenario`.
        """

        if self.logging:
            log.info("start_recording(self)")

        self.display_clock_seconds()
        self.set_max_video_length_to(600)


        leftover_recording_processes = run("pgrep -fla qecore_start_recording").strip("\n")
        if leftover_recording_processes:
            leftover_recording_process_list = leftover_recording_processes.split("\n")
            for process in leftover_recording_process_list:
                extracted_pid = process.split(" ", 1)[0]
                run(f"sudo kill -9 {extracted_pid}")

                absolute_path_to_video = os.path.expanduser("~/Videos")
                run(f"sudo rm -rf {absolute_path_to_video}/Screencast*")


        record_video_process = Popen("qecore_start_recording", shell=True)
        self.record_video_pid = record_video_process.pid


    def stop_recording(self):
        """
        Stop recording the video.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`after_scenario`.
        """

        if self.logging:
            log.info("stop_recording(self)")

        if self.record_video_pid is not None:
            run(f"sudo kill -9 {self.record_video_pid} > /dev/null")

        self.record_video_pid = None


    def get_app(self,
                name,
                a11yAppName=None,
                desktopFileExists=True,
                desktopFileName="",
                desktopFilePath="",
                appProcessName=""):
        """
        This function is a wrapper over :func:`get_application` to preserve the old api name.
        This is defined as an extra function because even the method parameters were renamed to
        comply with the snake_case naming style.
        """

        if self.logging:
            log.info(" ".join((
                f"get_app(self, name={name}, a11yAppName={a11yAppName},",
                f"desktopFileExists={desktopFileExists}, desktopFileName={desktopFileName},",
                f"desktopFilePath={desktopFilePath}, appProcessName={appProcessName})"
            )))

        return self.get_application(name,
                                    a11y_app_name=a11yAppName,
                                    desktop_file_exists=desktopFileExists,
                                    desktop_file_name=desktopFileName,
                                    desktop_file_path=desktopFilePath,
                                    app_process_name=appProcessName)


    def get_application(self,
                        name,
                        a11y_app_name=None,
                        desktop_file_exists=True,
                        desktop_file_name="",
                        desktop_file_path="",
                        app_process_name=""):
        """
        Return application to be used in test.

        :type name: str
        :param name: Name of the package that provides the application.

        :type a11y_app_name: str
        :param a11y_app_name: Application's name as it appears in the a11y tree.

        :type desktop_file_exists: bool
        :param desktop_file_exists: Does desktop file of the application exist?

        :type desktop_file_name: str
        :param desktop_file_name: Application's desktop file name.

        :type app_process_name: str
        :param app_process_name: Application's name as it appears in a running process.

        :return: Application class instance
        :rtype: <qecore.application.Application>

        This function is wrapped by :func:`get_app`.
        """

        if self.logging:
            log.info(" ".join((
                f"get_application(self, name={name}, a11y_app_name={a11y_app_name},",
                f"desktop_file_exists={desktop_file_exists},",
                f"desktop_file_name={desktop_file_name},",
                f"desktop_file_path={desktop_file_path},",
                f"app_process_name={app_process_name})"
            )))

        new_application = Application(name, a11y_app_name=a11y_app_name,
                                      desktop_file_exists=desktop_file_exists,
                                      desktop_file_name=desktop_file_name,
                                      desktop_file_path=desktop_file_path,
                                      app_process_name=app_process_name,
                                      shell=self.shell, session_type=self.session_type,
                                      session_desktop=self.session_desktop, logging=self.logging)

        self.applications.append(new_application)
        self.default_application = new_application \
            if self.default_application is None else self.default_application

        return new_application


    def get_flatpak(self, flatpak_id, **kwargs):
        """
        Return flatpak to be used in test.

        :type flatpak_id: str
        :param flatpak_id: Unique name of flatpak, mandatory format: org.flathub.app

        :return: Flatpak class instance
        :rtype: <qecore.flatpak.Flatpak>
        """

        if self.logging:
            log.info(f"get_flatpak(self, flatpak_id={flatpak_id}")

        flatpak = Flatpak(flatpak_id=flatpak_id, **kwargs)
        flatpak.shell = self.shell
        self.applications.append(flatpak)
        self.default_application = self.default_application or flatpak
        return flatpak


    def wait_until_shell_becomes_responsive(self):
        """
        Give some time if shell is not yet loaded fully.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`sandbox.TestSandbox.__init__`.
        """

        if self.logging:
            log.info("wait_until_shell_becomes_responsive(self)")

        if self.session_type == "x11":
            for _ in range(60):
                if not "gnome-shell" in [x.name for x in root.applications()]:
                    sleep(0.5)
                else:
                    break
        else:
            sleep(1) # in wayland there is no way to make sure the session is loaded, so just sleep


    def retrieve_session_data(self):
        """
        Get session/system data.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`__init__`.
        """

        if self.logging:
            log.info("retrieve_session_data(self)")

        self.architecture = run("uname -m").strip("\n")

        # Distributions expected for now: self.distribution = ["Red Hat Enterprise Linux", "Fedora"]
        self.distribution = run("cat /etc/os-release | grep ^NAME=")
        self.distribution = self.distribution.split("=")[-1].strip("\n").strip("\"")

        self.session_display = run("echo $DISPLAY").strip('\n')
        if not self.session_display:
            self.session_display = run("qecore_get_active_display").strip('\n')
            os.environ["DISPLAY"] = self.session_display

        try:
            self.resolution = [int(x) for x in \
                re.findall(r"\d+x\d+", run("xrandr | grep '*'"))[0].split("x")]
        except Exception as error:
            self.resolution = f"The resolution retrieval failed for: {error}"

        self.session_desktop = run("echo $XDG_SESSION_DESKTOP").strip('\n')

        self.session_type = "x11"
        if "XDG_SESSION_TYPE" in os.environ and "wayland" in os.environ["XDG_SESSION_TYPE"]:
            self.session_type = "wayland"


    def set_up_embedding(self, context):
        """
        Set up embeding to the behave html formatter.

        :type context: <behave.runner.Context>
        :param context: Passed object.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`before_scenario`.
        """

        def embed_data(mime_type, data, caption):
            # If data is empty we want to finish html tag by at least one character
            non_empty_data = " " if not data else data

            for formatter in context._runner.formatters:
                if "html" in formatter.name:
                    formatter.embedding(mime_type=mime_type, data=non_empty_data, caption=caption)
                    return

        def set_title(title, append=False, tag="span", **kwargs):
            for formatter in context._runner.formatters:
                if "html" in formatter.name and getattr(formatter, "set_title", None) is not None:
                    formatter.set_title(title=title, append=append, tag=tag, **kwargs)
                    return

        context.embed = embed_data
        context.set_title = set_title


    def add_after_scenario_hook(self, callback, *args, **kwargs):
        """
        Creates hook from callback function and its arguments.
        Hook will be called during :func:`sandbox.after_scenario`.

        :type callback: <function>
        :param callback: function to be called

        .. note::
            :func:`sandbox.after_scenario` should be called in :func:`after_scenario`,
            otherwise this function has no effect.

        .. note::
            Hooks are called in the order they were added. To reverse the order of execution
            set `sandbox.reverse_after_scenario_hooks` to `True` (default `False`).

        **Examples**::

            # already defined function
            def something():
                ...

            sandbox.add_after_scenario_hook(something)

            # generic function call
            sandbox.add_after_scenario_hook(function_name, arg1, arg2, kwarg1=val1, ...)

            # call command
            sandbox.add_after_scenario_hook(subprocess.call, "command to be called", shell=True)

            # embed data - if you want them embeded in the last step
            sandbox.add_after_scenario_hook(context.embed, "text/plain", data, caption="DATA")

            # embed data computed later (read log file)
            sandbox.add_after_scenario_hook(lambda context: context.embed("text/plain", open(log_file).read(), caption="LOG"), context)
        """

        self.after_scenario_hooks += [(callback, args, kwargs)]


    def set_timeout_handling(self):
        """
        Set up signal handling.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`before_scenario`.
        """

        signal.signal(signal.SIGTERM, self.gracefull_exit)
        run("touch /tmp/qecore_timeout_handler")



    def set_animations(self):
        """
        Set animations via gsettings command.
        Default value is None so the settings is not set unless user specifies otherwise.
        """

        if self.enable_animations is not None:
            run(" ".join((
                "gsettings",
                "set",
                "org.gnome.desktop.interface",
                "enable-animations",
                "true" if self.enable_animations else "false"
            )))


    def set_log_start_time(self):
        """
        Save time.
        Will be used to retrieve logs from journal.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`before_scenario`.
        """

        if self.logging:
            log.info("set_log_start_time(self)")

        initial_cursor_output = run("journalctl --lines=0 --show-cursor").strip()
        cursor_target = initial_cursor_output.split("cursor: ", 1)[-1]
        self.logging_cursor = f"\"--after-cursor={cursor_target}\""


    def close_yelp(self):
        """
        Close yelp application that is opened after fresh system installation.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`before_scenario`.
        """

        if self.logging:
            log.info("close_yelp(self)")

        # Attribute switch to allow not closing yelp in before_scenario.
        # Corner case was found in which we test yelp and do not close between scenarios.
        if not self.enable_close_yelp:
            return

        help_process_id = run("pgrep yelp").strip("\n")
        if help_process_id.isdigit():
            run(f"kill -9 {help_process_id}")


    def close_initial_setup(self):
        """
        Close initial setup window that is opened after the first login to the system.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`before_scenario`.
        """

        if self.logging:
            log.info("close_initial_setup(self)")

        run("echo yes > ~/.config/gnome-initial-setup-done")


    def set_blank_screen_to_never(self):
        """
        Set blank screen to never. For longer tests it is undesirable for screen to lock.

        .. note::

            This method is called by :func:`before_scenario`.
            There was never need to have other options,
            we do not want the system to sleep during the test.
        """

        if self.logging:
            log.info("set_blank_screen_to_never(self)")

        run("gsettings set org.gnome.desktop.session idle-delay 0")


    def set_max_video_length_to(self, number=600):
        """
        Set maximum allowed video length. With default value for 10 minutes.

        :type number: int
        :param number: Maximum video length.

        .. note::

            This method is called by :func:`before_scenario`. You can overwrite the setting.
        """

        if self.logging:
            log.info(f"set_max_video_length_to(self, number={number})")

        run(" ".join((
            "gsettings set",
            "org.gnome.settings-daemon.plugins.media-keys",
            f"max-screencast-length {number}"
        )))


    def display_clock_seconds(self):
        """
        Display clock seconds for better tracking test in video.

        .. note::

            This method is called by :func:`before_scenario`.
            There was never need to have other options,
            as we want to see the seconds ticking during the test.
        """

        if self.logging:
            log.info("display_clock_seconds(self)")

        run("gsettings set org.gnome.desktop.interface clock-show-seconds true")


    def return_to_home_workspace(self):
        """
        Return to home workspace.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`before_scenario`.
        """

        if self.logging:
            log.info("return_to_home_workspace(self)")

        if not self.workspace_return:
            return

        keyCombo("<Super><Home>")


    def set_typing_delay(self, number):
        """
        Set typing delay so slower machines will not lose characters on type.

        :type number: int
        :param number: Time in between accepted key strokes.

        .. note::

            This method is called by :func:`before_scenario`. You can overwrite the setting.
        """

        if self.logging:
            log.info(f"set_typing_delay(self, number={number})")

        config.typingDelay = number


    def set_debug_to_stdout_as(self, true_or_false=False):
        """
        Set debugging to stdout.

        :type true_or_false: bool
        :param true_or_false: Decision if debug to stdout or not.

        .. note::

            This method is called by :func:`before_scenario`. You can overwrite the setting.
        """

        if self.logging:
            log.info(f"set_debug_to_stdout_as(self, true_or_false={true_or_false})")

        config.logDebugToStdOut = true_or_false


    def copy_data_folder(self):
        """
        Copy data/ directory content to the /tmp/ directory.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`before_scenario`.
        """

        if self.logging:
            log.info("copy_data_folder(self)")

        if os.path.isdir("data/"):
            run("rsync -r data/ /tmp/")


    def detect_keyring(self):
        """
        Detect if keyring was setup. If not, setup the keyring with empty password.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`before_scenario`.
        """

        if self.logging:
            log.info("detect_keyring(self)")

        if not self.set_keyring:
            return

        current_user = os.path.expanduser("~")
        is_keyring_set = os.path.isfile("/tmp/keyring_set")
        is_keyring_in_place = os.path.isfile(f"{current_user}/.local/share/keyrings/default")

        if not is_keyring_set or not is_keyring_in_place:
            run(f"sudo rm -rf {current_user}/.local/share/keyrings/*")

            create_keyring_process = Popen("qecore_start_keyring", shell=True)
            self.keyring_process_pid = create_keyring_process.pid

            self.shell.child("Continue").click()
            self.shell.child("Continue").click()

            run("touch /tmp/keyring_set")

        run("killall qecore_start_keyring")


    def capture_image(self):
        """
        Capture screenshot after failed step.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`after_scenario`.
        """

        if self.logging:
            log.info("capture_image(self)")

        if not self.production:
            return

        self.screenshot_run_result = run("gnome-screenshot -f /tmp/screenshot.png", verbose=True)


    def set_g_debug_environment_variable(self):
        """
        Setup environment variable G_DEBUG as 'fatal-criticals'.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`__init__`.
        """

        if self.logging:
            log.info("set_g_debug_environment_variable(self)")

        # Environment value set upon checked field in Jenkins
        if os.path.isfile("/tmp/headless_enable_fatal_critical"):
            os.environ["G_DEBUG"] = "fatal-criticals"

        # Fatal_wanings has bigger priority than criticals.
        # Should both options be set in Jenkins the warning will overwrite the variable.
        if os.path.isfile("/tmp/headless_enable_fatal_warnings"):
            os.environ["G_DEBUG"] = "fatal-warnings"


    def set_title(self, context):
        """
        Append component name and session type to HTML title.

        :type context: <behave.runner.Context>
        :param context: Passed object.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`before_scenario`.
        """

        context.set_title("", tag="br", append=True)

        if self.default_application_icon_to_title:
            icon = self.get_default_application_icon()
            if icon is not None:
                context.set_title("", append=True, tag="img",
                                  alt=self.session_type[1],
                                  src=icon.to_src(),
                                  style="height:1.8rem; vertical-align:text-bottom;")

            context.set_title(f"{self.component} - ", append=True, tag="small")

        if self.session_icon_to_title:
            context.set_title("", append=True, tag="img",
                              alt=self.session_type[1],
                              src=qecore_icons[self.session_type].to_src(),
                              style="height:1.8rem; vertical-align:text-bottom;")

            context.set_title(self.session_type[1:], append=True, tag="small",
                              style="margin-left:-0.4em;")

        self.change_title = False


    def get_default_application_icon(self):
        """
        Get icon for default application.

        :return: icon or None
        :rtype: <icons.QECoreIcon>
        """

        # Importing here because of sphinx documentation generating issues.
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk

        if self.default_application and self.default_application.icon:
            icon_theme = Gtk.IconTheme.get_default()
            icon = icon_theme.lookup_icon(self.default_application.icon, 48, 0)
            if icon:
                icon_path = icon.get_filename()
                if icon_path:
                    mime = MimeTypes()
                    mime_type = mime.guess_type(icon_path)[0]
                    data_base64 = base64.b64encode(open(icon_path, "rb").read())
                    data_encoded = data_base64.decode("utf-8").replace("\n", "")
                    return QECoreIcon(mime_type, "base64", data_encoded)
        return None


    def attach_screenshot_to_report(self, context):
        """
        Attach screenshot to the html report upon failed test.

        :type context: <behave.runner.Context>
        :param context: Passed object.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`after_scenario`.
        """

        if self.logging:
            log.info("attach_screenshot_to_report(self, context)")

        if not self.production:
            return

        if self.screenshot_run_result[1] != 0:
            context.embed(mime_type="text/plain",
                          data=f"Screenshot capture failed: \n{self.screenshot_run_result}\n",
                          caption="Screenshot")
        else:
            data_base64 = base64.b64encode(open("/tmp/screenshot.png", "rb").read())
            data_encoded = data_base64.decode("utf-8").replace("\n", "")
            context.embed(mime_type="image/png",
                          data=data_encoded,
                          caption="Screenshot")


    def attach_image_to_report(self, context, image=None, caption="DefaultCaption"):
        """
        Attach image to the html report upon user request.

        :type context: <behave.runner.Context>
        :param context: Passed object.

        :type image: str
        :param image: Location of the image/png file.

        :type caption: str
        :param caption: Caption that is to be displayed in test html report.

        .. note::

            Use this to attach any image to report at any time.
        """

        if self.logging:
            log.info("attach_image_to_report(self, context)")

        if not self.production:
            return

        if os.path.isfile(image):
            data_base64 = base64.b64encode(open(image, "rb").read())
            data_encoded = data_base64.decode("utf-8").replace("\n", "")
            context.embed(mime_type="image/png",
                          data=data_encoded,
                          caption=caption)


    def attach_video_to_report(self, context):
        """
        Attach video to the html report upon failed test.

        :type context: <behave.runner.Context>
        :param context: Passed object.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`after_scenario`.
        """

        if self.logging:
            log.info("attach_video_to_report(self, context)")

        if not (self.production and self.record_video):
            return

        absolute_path_to_video = os.path.expanduser("~/Videos")
        screencast_list = [f"{absolute_path_to_video}/{file_name}" for file_name in \
            os.listdir(absolute_path_to_video) if "Screencast" in file_name]

        video_name = f"{self.component}_{self.current_scenario}"
        absolute_path_to_new_video = f"{absolute_path_to_video}/{video_name}.webm"

        if screencast_list == []:
            context.embed(mime_type="text/plain",
                          data="No video file found.",
                          caption="Video")
        else:
            if self.wait_for_stable_video:
                self.wait_for_video_encoding(screencast_list[0])

            data_base64 = base64.b64encode(open(screencast_list[0], "rb").read())
            data_encoded = data_base64.decode("utf-8").replace("\n", "")
            context.embed(mime_type="video/webm",
                          data=data_encoded,
                          caption="Video")
            run(f"mv {screencast_list[0]} {absolute_path_to_new_video}")
            run(f"sudo rm -rf {absolute_path_to_video}/Screencast*")


    def attach_journal_to_report(self, context):
        """
        Attach journal to the html report upon failed test.

        :type context: <behave.runner.Context>
        :param context: Passed object.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`after_scenario`.
        """

        if self.logging:
            log.info("attach_journal_to_report(self, context)")

        if not self.production:
            return

        journal_run = run(" ".join((
            "sudo journalctl --all",
            f"--output=short-precise {self.logging_cursor}",
            "> /tmp/journalctl_short.log"
        )), verbose=True)

        if journal_run[1] != 0:
            context.embed(mime_type="text/plain",
                          data=f"Creation of journalctl file failed: \n{journal_run}\n",
                          caption="journalctl")
        else:
            context.embed(mime_type="text/plain",
                          data=open("/tmp/journalctl_short.log", "r").read(),
                          caption="journalctl")

        run("rm /tmp/journalctl_short.log")


    def attach_abrt_link_to_report(self, context):
        """
        Attach abrt link to the html report upon detected abrt FAF report.

        :type context: <behave.runner.Context>
        :param context: Passed object.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`after_scenario`.
        """

        if self.logging:
            log.info("attach_abrt_link_to_report(self, context)")

        if not self.production:
            return

        faf_reports = set()
        abrt_directories = run("sudo ls /var/spool/abrt/ | grep ccpp-").strip("\n").split("\n")

        for abrt_directory in abrt_directories:
            try:
                reason_file = f"/var/spool/abrt/{abrt_directory}/reason"
                reported_to_file = f"/var/spool/abrt/{abrt_directory}/reported_to"

                abrt_faf_reason_run = run(f"sudo cat '{reason_file}'", verbose=True)
                abrt_faf_hyperlink_run = run(f"sudo cat '{reported_to_file}'", verbose=True)

                if abrt_faf_reason_run[1] == 0 and abrt_faf_hyperlink_run[1] == 0:
                    abrt_faf_reason = abrt_faf_reason_run[0].strip("\n")
                    abrt_faf_hyperlink = abrt_faf_hyperlink_run[0].split("ABRT Server: URL=")[-1].split("\n")[0]

                    faf_reports.add((abrt_faf_hyperlink, f"Reason: {abrt_faf_reason}"))

            except Exception as error:
                print(f"Exception caught: {error}")
                continue

        if faf_reports:
            context.embed("link", faf_reports, caption="FAF reports")


    def after_scenario_hooks_process(self, context):
        """
        Process attached after_scenario_hooks.

        :type context: <behave.runner.Context>
        :param context: Passed object.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`after_scenario`.
        """

        hook_error = False

        if self.reverse_after_scenario_hooks:
            self.after_scenario_hooks.reverse()

        for callback, args, kwargs in self.after_scenario_hooks:
            try:
                callback(*args, **kwargs)
            except Exception as error:
                hook_error = True
                error_trace = traceback.format_exc()
                context.embed("text/plain",
                              f"Hook Error: {error}\n{error_trace}",
                              caption="Hook Error")

        self.after_scenario_hooks = []

        assert not hook_error, "Exception during after_scenario hook"


    def revert_background_image(self):
        """
        Revert background image to the before-test state.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`after_scenario`.
        """

        run(" ".join((
            "gsettings",
            "set",
            "org.gnome.desktop.background",
            "picture-uri",
            self.background_image_location
        )))


    def wait_for_video_encoding(self, file_name):
        """
        Wait until the video is fully encoded.
        This is verified by video's changing size.
        Once the file is encoded the size will not change anymore.

        :type file_name: str
        :param file_name: Video location for size verification.

        .. note::

            Do **NOT** call this by yourself. This method is called by :func:`attach_video_to_report`.

        This fixes some issues with the video and most of the time the video will
        get passed with all data, in the testing this took between 2-5 seconds.
        But there still are situations when the encoding is not made in the trivial amount of time
        mostly on slower machines. Currently the hard cutoff is 60 seconds after that the wait will
        terminate and the video will get passed as is to the html report.

        This time loss is no issue with few failing tests and has huge advantage of
        having an entire video with all controling elements (sometimes the video cannot be moved
        to the middle, or does not have data abouts its length). With many failing tests this might
        add significant time to the testing time. To prevent waiting for the encoded video
        and therefore not waiting at all use::

            <qecore.sandbox.TestSandbox>.wait_for_stable_video = False
        """

        if self.logging:
            log.info(f"wait_for_video_encoding(self, file_name={file_name})")

        current_size = 0
        current_stability = 0

        iteration_cutoff = 0

        while current_stability < 30:
            new_size = os.path.getsize(file_name)
            if current_size == new_size:
                current_stability += 1
            else:
                current_stability = 0

            current_size = new_size
            sleep(0.1)

            iteration_cutoff += 1
            if iteration_cutoff > 600:
                break


    def set_background(self, color=None, background_image=None, background_image_revert=False):
        """
        Change background to a single color or an image.

        :type color: str
        :param color: String black/white to set as background color.

        :type background_image: str
        :param background_image: Image location to be set as background.

        :type background_image_revert: bool
        :param background_image_revert: Upon settings this attribute to True,
            the :func:`after_scenario` will return the background to the original state,
            after the test.

        To get the wanted color you can pass strings as follows::

            color="black"
            color="white"
            color="#FFFFFF" # or any other color represented by hexadecimal
        """

        if self.logging:
            log.info("".join((
                f"set_background(self, color={color}, ",
                f"background_image={background_image})."
            )))

        self.background_image_revert = background_image_revert

        if self.background_image_revert:
            self.background_image_location = run("gsettings get org.gnome.desktop.background picture-uri").strip("\n")

        if background_image:
            if "file://" in background_image:
                run(f"gsettings set org.gnome.desktop.background picture-uri {background_image}")
            else:
                run(f"gsettings set org.gnome.desktop.background picture-uri file://{background_image}")
        elif color == "white":
            run("gsettings set org.gnome.desktop.background picture-uri file://")
            run("gsettings set org.gnome.desktop.background primary-color \"#FFFFFF\"")
            run("gsettings set org.gnome.desktop.background secondary-color \"#FFFFFF\"")
            run("gsettings set org.gnome.desktop.background color-shading-type \"solid\"")
        elif color == "black":
            run("gsettings set org.gnome.desktop.background picture-uri file://")
            run("gsettings set org.gnome.desktop.background primary-color \"#000000\"")
            run("gsettings set org.gnome.desktop.background secondary-color \"#000000\"")
            run("gsettings set org.gnome.desktop.background color-shading-type \"solid\"")
        elif "#" in color:
            run("gsettings set org.gnome.desktop.background picture-uri file://")
            run(f"gsettings set org.gnome.desktop.background primary-color '{color}'")
            run(f"gsettings set org.gnome.desktop.background secondary-color '{color}'")
            run("gsettings set org.gnome.desktop.background color-shading-type \"solid\"")
        else:
            log.info(" ".join((
                f"Color '{color}' is not defined.",
                "You can define one yourself and submit merge request or"
                "email modehnal@redhat.com for support."
            )))


    def overview_action(self, action="hide"):
        """
        Hide or show application overview.

        :type action: str
        :param action: Hide or show application overview.

        This function takes only 'hide' and 'show' value.
        """

        if self.logging:
            log.info(f"overview_action(self, action={action})")

        if action == "hide":
            run(" ".join((
                "dbus-send",
                "--session",
                "--type=method_call",
                "--dest=org.gnome.Shell",
                "/org/gnome/Shell",
                "org.gnome.Shell.Eval",
                "string:'Main.overview.hide();'"
            )))
        elif action == "show":
            run(" ".join((
                "dbus-send",
                "--session",
                "--type=method_call",
                "--dest=org.gnome.Shell",
                "/org/gnome/Shell",
                "org.gnome.Shell.FocusSearch"
            )))
        else:
            assert False, "".join((
                "Unknown option, only defined ones are 'show' or 'hide'.",
                f"You tried to use: '{action}'"
            ))


    #Using properties to preserve old api of attributes
    @property
    def recordVideo(self):
        return self.record_video
    @recordVideo.setter
    def recordVideo(self, value):
        self.record_video = value


    @property
    def recordVideoPid(self):
        return self.record_video_pid
    @recordVideoPid.setter
    def recordVideoPid(self, value):
        self.record_video_pid = value


    @property
    def attachVideo(self):
        return self.attach_video
    @attachVideo.setter
    def attachVideo(self, value):
        self.attach_video = value


    @property
    def attachVideoOnPass(self):
        return self.attach_video_on_pass
    @attachVideoOnPass.setter
    def attachVideoOnPass(self, value):
        self.attach_video_on_pass = value


    @property
    def attachJournal(self):
        return self.attach_journal
    @attachJournal.setter
    def attachJournal(self, value):
        self.attach_journal = value


    @property
    def attachJournalOnPass(self):
        return self.attach_journal_on_pass
    @attachJournalOnPass.setter
    def attachJournalOnPass(self, value):
        self.attach_journal_on_pass = value


    @property
    def attachScreenshot(self):
        return self.attach_screenshot
    @attachScreenshot.setter
    def attachScreenshot(self, value):
        self.attach_screenshot = value


    @property
    def failedTest(self):
        return self.failed_test
    @failedTest.setter
    def failedTest(self, value):
        self.failed_test = value


    @property
    def attachFAF(self):
        return self.attach_faf
    @attachFAF.setter
    def attachFAF(self, value):
        self.attach_faf = value


    @property
    def attachFAFOnPass(self):
        return self.attach_faf_on_pass
    @attachFAFOnPass.setter
    def attachFAFOnPass(self, value):
        self.attach_faf_on_pass = value
