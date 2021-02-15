import configparser
import os
import logging
from PyQt5 import QtCore
from fileplayer import globa
import time

SETTINGS_FILE_NAME_STR = "settings.ini"

configuration_parser = None


def _update_and_get_config_parser() -> configparser.ConfigParser:
    """
    1. If the config parser has not been initialized this will create a ConfigParser
    2. The settings file will used to update the ConfigParser object
    :return: ConfigParser (see Python docs for info)
    """
    global configuration_parser
    if configuration_parser is None:
        configuration_parser = configparser.ConfigParser()
        configuration_parser.optionxform = str
    config_file_path_str = get_config_path(SETTINGS_FILE_NAME_STR)
    configuration_parser.read(config_file_path_str)
    return configuration_parser


def get_config_path(*args) -> str:
    if globa.testing_bool:
        config_dir = globa.get_project_path("tests", "temp-files")
    else:
        config_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.ConfigLocation)[0]
    appl_config_dir = os.path.join(config_dir, "file-player")
    full_path_str = appl_config_dir
    for arg in args:
        full_path_str = os.path.join(full_path_str, arg)
    os.makedirs(os.path.dirname(full_path_str), exist_ok=True)
    return full_path_str


def _add_string(i_section: str, i_key: str, i_value: str) -> None:
    config_parser = _update_and_get_config_parser()
    if not config_parser.has_section(i_section):
        config_parser.add_section(i_section)
    config_parser.set(i_section, i_key, i_value)
    config_file_path_str = get_config_path(SETTINGS_FILE_NAME_STR)
    with open(config_file_path_str, "w") as file:
        config_parser.write(file)


def _get_string(i_section: str, i_key: str, i_default_value: str) -> str:
    config_parser = _update_and_get_config_parser()

    def set_default_value():
        config_parser.set(i_section, i_key, i_default_value)
        config_file_path_str = get_config_path(SETTINGS_FILE_NAME_STR)
        with open(config_file_path_str, "w") as file:
            config_parser.write(file)

    if not config_parser.has_section(i_section):
        config_parser.add_section(i_section)
    if not config_parser.has_option(i_section, i_key):
        set_default_value()

    ret_value_str = config_parser[i_section][i_key]
    if not ret_value_str:
        # -possible addition for files and dirs: or os.path.exists(ret_value_str):
        logging.warning("Looking in the config file a key was found but the value was empty, using a default value")
        set_default_value()
        ret_value_str = config_parser[i_section][i_key]

    return ret_value_str


def _get_dictionary(i_section: str) -> dict:
    config_parser = _update_and_get_config_parser()
    if not config_parser.has_section(i_section):
        config_parser.add_section(i_section)
        config_file_path_str = get_config_path(SETTINGS_FILE_NAME_STR)
        with open(config_file_path_str, "w") as file:
            config_parser.write(file)
    ret_value_str = dict(config_parser.items(i_section))
    return ret_value_str


def _set_dictionary(i_section: str, i_dict: dict) -> None:
    config_parser = _update_and_get_config_parser()
    config_file_path_str = get_config_path(SETTINGS_FILE_NAME_STR)
    config_parser.read(config_file_path_str)
    if not config_parser.has_section(i_section):
        config_parser.remove_section(i_section)
    config_parser[i_section] = i_dict
    with open(config_file_path_str, "w") as file:
        config_parser.write(file)


def _add_to_dictionary(i_section: str, i_key: str, i_value) -> None:
    dictionary = _get_dictionary(i_section)
    dictionary[i_key] = i_value
    _set_dictionary(i_section, dictionary)


def _pop_from_dictonary(i_section: str, i_key: str) -> str:
    dictonary = _get_dictionary(i_section)
    value = dictonary.pop(i_key, False)
    _set_dictionary(i_section, dictonary)
    return value


def _get_string_from_bool(i_value: bool) -> str:
    string_from_bool_str = "false"
    if i_value:
        string_from_bool_str = "true"
    return string_from_bool_str


def _get_bool_from_string(i_value: str) -> bool:
    if i_value == "false":
        return False
    elif i_value == "true":
        return True
    else:
        raise Exception(f'Case not covered: argument given must be "false" or "true"')


def _get_boolean(i_section: str, i_key: str, i_default_value: bool) -> bool:
    value_str = _get_string(i_section, i_key, _get_string_from_bool(i_default_value))
    value_bool = _get_bool_from_string(value_str)
    return value_bool


def _add_boolean(i_section: str, i_key: str, i_value: bool) -> None:
    _add_string(i_section, i_key, _get_string_from_bool(i_value))


#######
# API #
#######

GENERAL_SECTION_STR = "general"
FAVORITES_SECTION_STR = "favorites"
GUI_LAYOUT_SECTION_STR = "gui-layout"

DARK_MODE_KEY_STR = "dark-mode"
START_DIR_KEY_STR = "start-dir"
START_VOL_KEY_STR = "start-volume"
START_FADE_KEY_STR = "start-fade"
PLAYLIST_DIR_KEY_STR = "playlist-dir"
WIN_WIDTH_KEY_STR = "win-width"
WIN_HEIGHT_KEY_STR = "win-height"
WIN_X_KEY_STR = "win-x"
WIN_Y_KEY_STR = "win-y"

DEFAULT_WIN_WIDTH_INT = 750
DEFAULT_WIN_HEIGHT_INT = 600
DEFAULT_WIN_X_INT = 100
DEFAULT_WIN_Y_INT = 50

DEFAULT_START_VOL_INT = 40
DEFAULT_FADE_SECS_INT = 5


def get_dark_mode() -> bool:
    ret_val_bool = _get_boolean(GENERAL_SECTION_STR, DARK_MODE_KEY_STR, False)
    return ret_val_bool


def set_dark_mode(i_value: bool) -> None:
    _add_boolean(GENERAL_SECTION_STR, DARK_MODE_KEY_STR, i_value)


def get_start_dir() -> str:
    default_str = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.MusicLocation)[0]
    start_dir_str = _get_string(GENERAL_SECTION_STR, START_DIR_KEY_STR, default_str)
    if globa.testing_bool:
        start_dir_str = globa.get_project_path("tests", "files")
    elif not os.path.isdir(start_dir_str):
        start_dir_str = globa.get_appl_path()
    return start_dir_str


def set_start_dir(i_start_dir: str) -> None:
    _add_string(GENERAL_SECTION_STR, START_DIR_KEY_STR, i_start_dir)


def get_fav_dirs_dict() -> dict:
    fav_dict = _get_dictionary(FAVORITES_SECTION_STR)
    return fav_dict


def set_start_volume(i_vol: int) -> None:
    _add_string(GENERAL_SECTION_STR, START_VOL_KEY_STR, str(i_vol))


def get_start_volume() -> int:
    vol_str = _get_string(GENERAL_SECTION_STR, START_VOL_KEY_STR, str(DEFAULT_START_VOL_INT))
    vol_int = int(vol_str)
    return vol_int


def set_start_fade(i_fade_secs: int) -> None:
    _add_string(GENERAL_SECTION_STR, START_FADE_KEY_STR, str(i_fade_secs))


def get_start_fade() -> int:
    fade_secs_str = _get_string(GENERAL_SECTION_STR, START_FADE_KEY_STR, str(DEFAULT_FADE_SECS_INT))
    fade_secs_int = int(fade_secs_str)
    return fade_secs_int


def add_to_favs(i_key: str) -> None:
    now_unix_ts_int = int(time.time())
    _add_to_dictionary(FAVORITES_SECTION_STR, i_key, now_unix_ts_int)


def pop_from_favs(i_key: str) -> str:
    value = _pop_from_dictonary(FAVORITES_SECTION_STR, i_key)
    return value


def set_playlist_dir(i_dir: str) -> None:
    _add_string(GENERAL_SECTION_STR, PLAYLIST_DIR_KEY_STR, i_dir)


def get_playlist_dir() -> str:
    default_str = get_start_dir()
    playlist_dir_str = _get_string(GENERAL_SECTION_STR, PLAYLIST_DIR_KEY_STR, default_str)
    return playlist_dir_str


def set_win_width(i_width_px: int) -> None:
    _add_string(GUI_LAYOUT_SECTION_STR, WIN_WIDTH_KEY_STR, str(i_width_px))


def get_win_width() -> int:
    win_width_str = _get_string(GUI_LAYOUT_SECTION_STR, WIN_WIDTH_KEY_STR, str(DEFAULT_WIN_WIDTH_INT))
    win_width_int = int(win_width_str)
    return win_width_int


def set_win_height(i_height_px: int) -> None:
    _add_string(GUI_LAYOUT_SECTION_STR, WIN_HEIGHT_KEY_STR, str(i_height_px))


def get_win_height() -> int:
    win_height_str = _get_string(GUI_LAYOUT_SECTION_STR, WIN_HEIGHT_KEY_STR, str(DEFAULT_WIN_HEIGHT_INT))
    win_height_int = int(win_height_str)
    return win_height_int


def get_win_x() -> int:
    win_x_str = _get_string(GUI_LAYOUT_SECTION_STR, WIN_X_KEY_STR, str(DEFAULT_WIN_X_INT))
    win_x_int = int(win_x_str)
    return win_x_int


def set_win_x(i_x: int) -> None:
    _add_string(GUI_LAYOUT_SECTION_STR, WIN_X_KEY_STR, str(i_x))


def get_win_y() -> int:
    win_y_str = _get_string(GUI_LAYOUT_SECTION_STR, WIN_Y_KEY_STR, str(DEFAULT_WIN_Y_INT))
    win_y_int = int(win_y_str)
    return win_y_int


def set_win_y(i_y: int):
    _add_string(GUI_LAYOUT_SECTION_STR, WIN_Y_KEY_STR, str(i_y))
