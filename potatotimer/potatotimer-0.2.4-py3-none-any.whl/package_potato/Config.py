import yaml
from appdirs import AppDirs
from pathlib import Path


class Config:
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __init__(self, config_file=None):
        self._alarm_type = "beep"
        self._use_colors = True
        self._prefer_terminal_colors = False
        self._alarm_repeat = 1

        self._timers = [
            {"type": "work", "duration": 0.2},
            {"type": "short break", "duration": 0.1},
            {"type": "long break", "duration": 0.3},
            {"type": "custom timer", "duration": 0.4}
        ]

        self._possible_files = [
            "~/.config/potato-timer/config.yml",
            "~/.potato-timer-config.yml",
            "./config.yml",
        ]

        if config_file is not None:
            self._possible_files.insert(0, config_file)

        self.insert_xdg_conf_location()

        self._selected_config = self.find_config()
        if self._selected_config is not None:
            try:
                self.read_config()
            except:
                print(f'Error reading config: {self._selected_config}')
                print("Please check that the file is formatted correctly.")
                exit()

    def find_config(self):
        """Try to find config file"""
        for possibility in self._possible_files:
            p = Path(possibility)
            expanded = p.expanduser()
            if expanded.is_file():
                return expanded
        return None

    def insert_xdg_conf_location(self):
        """Insert XDG config file location"""
        dirs = AppDirs("potato-timer")
        xdg_config = dirs.user_config_dir
        p = Path(xdg_config).joinpath('config.yml')
        self._possible_files.insert(1, str(p))

    def read_config(self):
        """Load the config file"""
        with open(self._selected_config, 'r') as stream:
            settings_yaml = yaml.safe_load(stream)
            self.load_alarm_type(settings_yaml)
            self.load_alarm_repeat(settings_yaml)
            self.load_use_colors(settings_yaml)
            self.load_timers(settings_yaml)

    def load_alarm_type(self, settings_yaml):
        """Try to load alarm type setting"""
        if "alarm_type" in settings_yaml:
            if settings_yaml["alarm_type"] == "beep":
                self._alarm_type = "beep"
            elif settings_yaml["alarm_type"] == "flash":
                self._alarm_type = "flash"

    def load_alarm_repeat(self, settings_yaml):
        """Try to load alarm count"""
        if "alarm_repeat" in settings_yaml:
            if settings_yaml["alarm_repeat"] >= 1:
                self._alarm_repeat = settings_yaml["alarm_repeat"]

    def load_use_colors(self, settings_yaml):
        """Try to load color use setting"""
        if "use_colors" in settings_yaml:
            if settings_yaml["use_colors"]:
                self._use_colors = True
            else:
                self._use_colors = False

        if "prefer_terminal_colors" in settings_yaml:
            if settings_yaml["prefer_terminal_colors"]:
                self._prefer_terminal_colors = True
            else:
                self._prefer_terminal_colors = False

    def load_timers(self, settings_yaml):
        """Try to load timers"""
        loaded_timers = []
        if "timers" in settings_yaml:
            for timer in settings_yaml["timers"]:
                if "type" in timer and "duration" in timer:
                    if timer["duration"] > 0:
                        loaded_timers.append({
                            "type": timer["type"],
                            "duration": timer["duration"]
                        })
        if loaded_timers:
            self._timers = loaded_timers

    def get_timer(self, timer_id):
        """Get timer by id"""
        if timer_id < len(self._timers):
            return self._timers[timer_id]
        else:
            raise IndexError("Timer not found")

    @property
    def selected_config(self):
        return self._selected_config

    @property
    def timers(self):
        return self._timers

    @property
    def use_colors(self):
        return self._use_colors

    @property
    def prefer_terminal_colors(self):
        return self._prefer_terminal_colors

    @property
    def alarm_repeat(self):
        return self._alarm_repeat

    @property
    def alarm_type(self):
        return self._alarm_type
