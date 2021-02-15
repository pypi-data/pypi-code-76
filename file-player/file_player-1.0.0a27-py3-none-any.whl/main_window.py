"""
Abbreviations:
TL: track list
FD: files and dirs

"""

import enum
import sys
import logging
import os
import subprocess
import functools
import time
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import QtMultimedia
from fileplayer import widgets, timer, globa, config
# -Please note that we are using "from fileplayer import" which is "absolute import".
# If we just write import widgets for example there could be problems, for example after installing with pip
# More info here: https://stackoverflow.com/q/27365273/2525237

logging.basicConfig(level=logging.DEBUG)

supported_track_suffixes_list = [".ogg", ".mp3", ".flac", ".wav"]
supported_playlist_suffixes_list = [".m3u"]


def get_media_from_path(i_file_path: str) -> QtMultimedia.QMediaContent:
    file_qurl = QtCore.QUrl.fromLocalFile(i_file_path)
    qmediacontent = QtMultimedia.QMediaContent(file_qurl)
    return qmediacontent


def user_interaction_dr(func):
    @functools.wraps(func)
    def wrapper_func(self, *args, **kwargs):
        if self.updating_gui_bool:
            logging.debug(f"GUI update ongoing, exiting user interaction function {func.__name__}")
            return
        ret_val = func(self, *args, **kwargs)
        return ret_val
    return wrapper_func


def gui_update_dr(func):
    @functools.wraps(func)
    def wrapper_func(self, *args, **kwargs):
        self.updating_gui_bool = True
        # logging.debug(f"Calling function {func.__name__} through the gui_update_dr decoractor")
        ret_val = func(self, *args, **kwargs)
        self.updating_gui_bool = False
        return ret_val
    return wrapper_func


class FDTypeEnum(enum.Enum):
    music_file = enum.auto()
    directory = enum.auto()
    hidden_fd = enum.auto()
    other_file = enum.auto()
    playlist_file = enum.auto()


def get_fd_type(i_path: str) -> FDTypeEnum:
    name_str = os.path.basename(i_path)
    if name_str.startswith("."):
        return FDTypeEnum.hidden_fd
    elif os.path.isdir(i_path):
        return FDTypeEnum.directory
    elif name_str.lower().endswith(tuple(supported_track_suffixes_list)):
        return FDTypeEnum.music_file
    elif name_str.lower().endswith(tuple(supported_playlist_suffixes_list)):
        return FDTypeEnum.playlist_file
    else:
        return FDTypeEnum.other_file


class GuiAreasEnum(enum.Enum):
    fd_list = enum.auto()
    fd_controls = enum.auto()
    tl_list = enum.auto()
    tl_controls = enum.auto()


class StateEnum(enum.Enum):
    stopped = 0  # -inactive, start state
    playing = 2
    paused = 3
    # -these are comparable to https://doc.qt.io/qt-5/qmediaplayer.html#State-enum

    stop_after_current = 7  # -cmp with "playing" state

    pausing_fade = 4
    stopping_fade = 5
    switching_fade = 6
    # -please note that we only fade out


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, i_cmd_arg_file: str = "", i_testing: bool = False):
        super().__init__()

        first_started: bool = not os.path.isfile(config.get_config_path(config.SETTINGS_FILE_NAME_STR))
        if first_started and not i_testing:
            music_path: str = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.MusicLocation)[0]
            config.add_to_favs(music_path)
            download_path: str = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.DownloadLocation)[0]
            config.add_to_favs(download_path)

        globa.testing_bool = i_testing
        self.state_enum = StateEnum.stopped
        self.updating_position_bool = False
        logging.debug(f"{globa.get_appl_path()=}")
        logging.debug(f"{globa.get_project_path()=}")
        logging.debug(f"{config.get_config_path()=}")
        self.tl_playing_row_int = -1

        self.media_playlist = QtMultimedia.QMediaPlaylist()  # -only used for saving and loading playlist files
        self.media_playlist.loadFailed.connect(self.on_load_playlist_failed)
        self.media_playlist.loaded.connect(self.on_playlist_loaded)

        self.updating_gui_bool = False
        self.updating_playlist_bool = False
        self.active_dir_path_str = ""

        self.fade_timer = timer.FadeTimer()
        self.fade_timer.update_signal.connect(self.on_fade_timer_updated)
        self.media_player = None

        # noinspection PyArgumentList
        self.media_player = QtMultimedia.QMediaPlayer(parent=self)
        self.media_player.setAudioRole(QtMultimedia.QAudio.MusicRole)
        self.media_player.positionChanged.connect(self.on_media_pos_changed)
        self.media_player.durationChanged.connect(self.on_duration_changed)
        self.media_player.currentMediaChanged.connect(self.on_current_media_changed)
        self.media_player.mediaStatusChanged.connect(self.on_media_status_changed)
        """
        except NameError:
            logging.debug("NameError - Cannot play audio since QtMultimedia has not been imported")
            sys.exit(1)
        """

        self.setWindowTitle(globa.APPLICATION_NAME_STR)

        self.central_widget = QtWidgets.QWidget(parent=self)
        self.setCentralWidget(self.central_widget)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(vbox_l2)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)

        self.fd_qgb = QtWidgets.QGroupBox("Files and dirs")
        hbox_l3.addWidget(self.fd_qgb)

        vbox_l4 = QtWidgets.QVBoxLayout()
        self.fd_qgb.setLayout(vbox_l4)

        hbox_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(hbox_l5)

        self.active_dir_path_qll = QtWidgets.QLabel()
        hbox_l5.addWidget(self.active_dir_path_qll, stretch=1)
        self.active_dir_path_qll.setWordWrap(True)

        hbox_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(hbox_l5)

        self.dir_up_qpb = QtWidgets.QPushButton("Up")
        hbox_l5.addWidget(self.dir_up_qpb)
        self.dir_up_qpb.setFixedWidth(50)
        self.dir_up_qpb.clicked.connect(self.on_dir_up_clicked)

        self.fd_fav_dirs_qpb = QtWidgets.QPushButton("Favs")
        hbox_l5.addWidget(self.fd_fav_dirs_qpb)

        self.fd_fav_dirs_menu = QtWidgets.QMenu()
        self.fd_fav_dirs_menu.triggered.connect(self.on_fav_dir_menu_action_triggered)
        self.fd_fav_dirs_qpb.setMenu(self.fd_fav_dirs_menu)

        hbox_l5.addStretch(1)

        self.fd_actions_qpb = QtWidgets.QPushButton("Actions")
        hbox_l5.addWidget(self.fd_actions_qpb)

        self.fd_actions_menu = QtWidgets.QMenu()
        self.fd_actions_qpb.setMenu(self.fd_actions_menu)
        # self.fd_actions_menu.triggered.connect(self.on_fd_actions_menu_triggered)

        self.is_fav_action = QtWidgets.QAction("Favorite")
        self.is_fav_action.setCheckable(True)
        self.is_fav_action.toggled.connect(self.on_is_fav_toggled)
        self.fd_actions_menu.addAction(self.is_fav_action)

        self.open_dir_qa = QtWidgets.QAction("Open dir")
        self.open_dir_qa.triggered.connect(self.on_open_dir_triggered)
        self.fd_actions_menu.addAction(self.open_dir_qa)

        self.set_as_start_dir_qa = QtWidgets.QAction("Set as start dir")
        # self.set_as_start_dir_qa.triggered.connect(lambda x: config.set_start_dir(x))
        self.set_as_start_dir_qa.triggered.connect(lambda: config.set_start_dir(self.active_dir_path_str))
        self.fd_actions_menu.addAction(self.set_as_start_dir_qa)
        # config.set_start_dir(self.active_dir_path_str)

        self.set_as_playlist_dir_qa = QtWidgets.QAction("Set as playlist dir")
        self.set_as_playlist_dir_qa.triggered.connect(lambda: config.set_playlist_dir(self.active_dir_path_str))
        self.fd_actions_menu.addAction(self.set_as_playlist_dir_qa)

        # hbox_l5.addWidget(QtWidgets.QLabel("Show dirs: "))
        # self.show_dirs_first_last_qbg = QtWidgets.QButtonGroup()

        self.fd_view_qpb = QtWidgets.QPushButton("View")
        hbox_l5.addWidget(self.fd_view_qpb)
        self.fd_view_menu = QtWidgets.QMenu()
        self.fd_view_qpb.setMenu(self.fd_view_menu)
        # self.fd_view_menu.triggered.connect(self.on_fd_view_menu_triggered)

        self.fd_view_qag = QtWidgets.QActionGroup(self)
        self.fd_view_qag.setExclusive(True)
        self.fd_view_qag.triggered.connect(self.on_fd_view_triggered)
        self.show_dirs_first_qa = QtWidgets.QAction("Show dirs first")
        self.show_dirs_first_qa.setCheckable(True)
        self.fd_view_qag.addAction(self.show_dirs_first_qa)
        self.fd_view_menu.addAction(self.show_dirs_first_qa)
        self.show_dirs_last_qa = QtWidgets.QAction("Show dirs last")
        self.show_dirs_last_qa.setCheckable(True)
        self.fd_view_qag.addAction(self.show_dirs_last_qa)
        self.fd_view_menu.addAction(self.show_dirs_last_qa)
        self.show_dirs_first_qa.setChecked(True)

        """
        self.set_playlist_start_dir_qaction = QtWidgets.QAction("Set playlist dir")
        self.playlists_menu.addAction(self.set_playlist_start_dir_qaction)
        self.set_playlist_start_dir_qaction.triggered.connect(self.on_set_playlist_start_dir_triggered)

        self.favorites_menu_qpb = QtWidgets.QPushButton("Favorite dirs")
        hbox_l5.addWidget(self.favorites_menu_qpb)
        self.fav_menu = QtWidgets.QMenu()
        self.fav_menu.triggered.connect(self.on_fav_dir_menu_triggered)
        self.favorites_menu_qpb.setMenu(self.fav_menu)
        """

        self.fd_qlw = QtWidgets.QListWidget(parent=self)
        vbox_l4.addWidget(self.fd_qlw)
        self.fd_qlw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.fd_qlw.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.fd_qlw.setDragEnabled(True)
        self.fd_qlw.currentRowChanged.connect(self.on_fd_current_row_changed)
        # self.fd_qlw.setSortingEnabled(True)
        self.fd_qlw.itemDoubleClicked.connect(self.on_fd_item_double_clicked)

        hbox_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(hbox_l5)

        self.add_to_playlist_qpb = QtWidgets.QPushButton("Add")
        hbox_l5.addWidget(self.add_to_playlist_qpb)
        self.add_to_playlist_qpb.clicked.connect(self.on_add_to_playlist_clicked)

        self.add_to_playlist_as_next_qpb = QtWidgets.QPushButton("Add as next")
        hbox_l5.addWidget(self.add_to_playlist_as_next_qpb)
        self.add_to_playlist_as_next_qpb.clicked.connect(self.on_add_to_playlist_as_next_clicked)

        self.add_to_playlist_as_next_and_play_qpb = QtWidgets.QPushButton("Add as next + play")
        hbox_l5.addWidget(self.add_to_playlist_as_next_and_play_qpb)
        self.add_to_playlist_as_next_and_play_qpb.clicked.connect(self.on_add_to_playlist_as_next_and_play_clicked)

        self.track_list_qgb = QtWidgets.QGroupBox("Track list")
        hbox_l3.addWidget(self.track_list_qgb)

        vbox_l4 = QtWidgets.QVBoxLayout()
        self.track_list_qgb.setLayout(vbox_l4)

        hbox_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(hbox_l5)

        """
        self.fav_playlist_menu_qpb = QtWidgets.QPushButton("Playlists")
        hbox_l5.addWidget(self.fav_playlist_menu_qpb)
        self.fav_playlists_menu = QtWidgets.QMenu()
        self.fav_playlists_menu.triggered.connect(self.on_fav_playlists_menu_triggered)
        self.fav_playlist_menu_qpb.setMenu(self.fav_playlists_menu)

        self.save_playlist_qpb = QtWidgets.QPushButton("Save")
        hbox_l5.addWidget(self.save_playlist_qpb)

        self.playlists_in_start_dir_qmenu = QtWidgets.QMenu("Playlists in start dir")
        self.playlists_menu.addMenu(self.playlists_in_start_dir_qmenu)
        self.playlists_in_start_dir_qmenu.aboutToShow.connect(self.on_playlists_in_start_dir_about_to_show)
        # Maybe move this into it's own menu, or into a combobox placed over the playlist area?
        """
        hbox_l5.addStretch(1)

        self.tq_actions_qpb = QtWidgets.QPushButton("Actions")
        hbox_l5.addWidget(self.tq_actions_qpb)
        self.tq_actions_menu = QtWidgets.QMenu()
        self.tq_actions_qpb.setMenu(self.tq_actions_menu)

        self.open_playlist_dir_qaction = QtWidgets.QAction("Open playlist dir")
        self.tq_actions_menu.addAction(self.open_playlist_dir_qaction)
        self.open_playlist_dir_qaction.triggered.connect(self.on_open_playlist_directory_qaction)

        self.save_to_playlist_qaction = QtWidgets.QAction("Save to playlist")
        self.tq_actions_menu.addAction(self.save_to_playlist_qaction)
        self.save_to_playlist_qaction.triggered.connect(self.on_save_playlist_qaction)

        self.load_from_playlist_qaction = QtWidgets.QAction("Load from playlist")
        self.tq_actions_menu.addAction(self.load_from_playlist_qaction)
        self.load_from_playlist_qaction.triggered.connect(self.on_load_playlist_qaction)

        self.tq_playlist_load_qpb = QtWidgets.QPushButton("Playlist load")
        hbox_l5.addWidget(self.tq_playlist_load_qpb)
        self.tq_playlist_load_menu = QtWidgets.QMenu()
        self.tq_playlist_load_menu.triggered.connect(self.on_playlist_load_menu_triggered)
        self.tq_playlist_load_qpb.setMenu(self.tq_playlist_load_menu)

        self.playlist_qlw = widgets.ListWidget(self)
        vbox_l4.addWidget(self.playlist_qlw)
        self.playlist_qlw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.playlist_qlw.itemDoubleClicked.connect(self.on_playlist_item_dc)
        self.playlist_qlw.item_dropped_signal.connect(self.on_playlist_item_dropped)
        # self.playlist_qlw.rowsInserted.connect(self.on_pl_rows_inserted)

        hbox_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(hbox_l5)

        self.remove_from_playlist_qpb = QtWidgets.QPushButton("Remove from playlist")
        hbox_l5.addWidget(self.remove_from_playlist_qpb)
        self.remove_from_playlist_qpb.clicked.connect(self.on_remove_from_playlist_clicked)

        self.duplicate_track_qpb = QtWidgets.QPushButton("Duplicate")
        hbox_l5.addWidget(self.duplicate_track_qpb)
        self.duplicate_track_qpb.clicked.connect(self.on_duplicate_track_clicked)

        self.clear_playlist_qpb = QtWidgets.QPushButton("Clear all")
        hbox_l5.addWidget(self.clear_playlist_qpb)
        self.clear_playlist_qpb.clicked.connect(self.on_clear_playlist_clicked)

        self.now_playing_qgb = QtWidgets.QGroupBox("Now playing")
        vbox_l2.addWidget(self.now_playing_qgb)

        size_policy = self.now_playing_qgb.sizePolicy()
        size_policy.setVerticalPolicy(QtWidgets.QSizePolicy.Maximum)
        self.now_playing_qgb.setSizePolicy(size_policy)

        self.now_playing_qsl = QtWidgets.QStackedLayout()
        self.now_playing_qgb.setLayout(self.now_playing_qsl)

        self.btm_controls_qw = QtWidgets.QWidget()

        self.fade_out_qw = QtWidgets.QWidget()
        self.fade_out_qw.setContentsMargins(35, 10, 35, 10)
        fade_out_vbox = QtWidgets.QVBoxLayout()

        self.fade_out_qw.setLayout(fade_out_vbox)
        self.fade_out_qpb = QtWidgets.QProgressBar()
        fade_out_vbox.addWidget(self.fade_out_qpb)
        self.fade_out_qpb.setFormat("")
        # state_hbox_l4.addWidget(self.state_qpb)
        # self.state_qpb.setFormat("fading out")
        # -possible bug: The progress bar is not updated as often if we set an empty or custom text format

        self.now_playing_qsl.addWidget(self.fade_out_qw)
        self.now_playing_qsl.addWidget(self.btm_controls_qw)

        btm_vbox_l3 = QtWidgets.QVBoxLayout()
        self.btm_controls_qw.setLayout(btm_vbox_l3)

        hbox_l4 = QtWidgets.QHBoxLayout()
        btm_vbox_l3.addLayout(hbox_l4)

        self.track_title_qll = QtWidgets.QLabel()
        hbox_l4.addWidget(self.track_title_qll)

        hbox_l4.addStretch(1)

        self.share_qpb = QtWidgets.QPushButton("Share")
        self.share_qpb.clicked.connect(self.on_share_clicked)
        hbox_l4.addWidget(self.share_qpb)

        self.next_qpb = QtWidgets.QPushButton("Next")
        self.next_qpb.clicked.connect(self.on_next_clicked)
        hbox_l4.addWidget(self.next_qpb)

        hbox_l4 = QtWidgets.QHBoxLayout()
        btm_vbox_l3.addLayout(hbox_l4)

        self.play_qpb = QtWidgets.QPushButton("Play")
        self.play_qpb.clicked.connect(self.on_play_clicked)
        hbox_l4.addWidget(self.play_qpb, stretch=2)

        self.pause_qpb = QtWidgets.QPushButton("Pause")
        self.pause_qpb.clicked.connect(self.on_pause_clicked)
        hbox_l4.addWidget(self.pause_qpb, stretch=2)

        self.stop_qpb = QtWidgets.QPushButton("Stop")
        self.stop_qpb.clicked.connect(self.on_stop_clicked)
        hbox_l4.addWidget(self.stop_qpb, stretch=2)

        self.stop_after_this_qpb = QtWidgets.QPushButton("Stop after this")
        self.stop_after_this_qpb.clicked.connect(self.on_stop_after_current_clicked)
        hbox_l4.addWidget(self.stop_after_this_qpb, stretch=2)

        hbox_l4.addStretch(3)

        self.state_qll = QtWidgets.QLabel()
        hbox_l4.addWidget(self.state_qll)

        # Prev?

        hbox_l4 = QtWidgets.QHBoxLayout()
        btm_vbox_l3.addLayout(hbox_l4)

        self.volume_qll = QtWidgets.QLabel("Volume:")
        hbox_l4.addWidget(self.volume_qll)
        start_vol_int = config.get_start_volume()
        # vbox_l2.addWidget(QtWidgets.QLabel("lowering the volume for the next iteration"))
        self.volume_qsr = QtWidgets.QSlider()
        # self.volume_qsr.setInvertedAppearance(True)
        self.volume_qsr.valueChanged.connect(self.on_volume_slider_changed)
        self.volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.volume_qsr.setMinimum(0)
        self.volume_qsr.setMaximum(100)
        self.volume_qsr.setMaximumWidth(150)
        self.volume_qsr.setValue(start_vol_int)
        hbox_l4.addWidget(self.volume_qsr)

        self.fade_qll = QtWidgets.QLabel("Fade:")
        hbox_l4.addWidget(self.fade_qll)

        start_fade_int = config.get_start_fade()
        self.fade_qsb = QtWidgets.QSpinBox()
        hbox_l4.addWidget(self.fade_qsb)
        self.fade_qsb.setValue(start_fade_int)

        hbox_l4.addSpacing(25)

        self.seek_qsr = QtWidgets.QSlider()
        self.seek_qsr.setTracking(False)
        self.seek_qsr.setSingleStep(5000)
        self.seek_qsr.setPageStep(30000)
        self.seek_qsr.valueChanged.connect(self.on_seek_changed)
        self.seek_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.seek_qsr.setMinimum(0)
        hbox_l4.addWidget(self.seek_qsr)

        self.duration_qll = QtWidgets.QLabel()
        hbox_l4.addWidget(self.duration_qll)

        # icon_path_str = fileplayer.config.get_appl_path("icons", "icon.png")
        self.pixmap = QtGui.QPixmap(globa.XPM_ICON_DATA)
        # https://doc.qt.io/qt-5/qpixmap.html#QPixmap-3
        # Constructs a pixmap from the given xpm data, which must be a valid XPM image.
        self.icon = QtGui.QIcon(self.pixmap)

        self.setWindowIcon(self.icon)

        self.quit_qaction = QtWidgets.QAction("Quit")
        self.quit_qaction.triggered.connect(self.on_quit_action_triggered)
        self.gentle_quit_action = QtWidgets.QAction("Gentle Quit")
        self.gentle_quit_action.triggered.connect(self.on_gentle_quit_triggered)
        self.tray_restore_action = QtWidgets.QAction("Restore")
        self.tray_restore_action.triggered.connect(self.showNormal)

        # System tray

        self.tray_icon = QtWidgets.QSystemTrayIcon()
        self.tray_icon.setIcon(self.icon)
        self.tray_menu = QtWidgets.QMenu()
        self.tray_menu.addAction(self.tray_restore_action)
        self.tray_menu.addAction(self.quit_qaction)
        self.tray_menu.addAction(self.gentle_quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        # Main menu

        self.menu_bar = self.menuBar()

        self.main_menu = QtWidgets.QMenu("Main")
        self.menu_bar.addMenu(self.main_menu)

        self.main_menu.addAction(self.quit_qaction)

        self.main_menu.addAction(self.gentle_quit_action)

        self.settings_menu = QtWidgets.QMenu("Settings")
        self.menu_bar.addMenu(self.settings_menu)

        self.use_current_win_geometry_at_start_qaction = QtWidgets.QAction("Use current win geometry at start")
        self.settings_menu.addAction(self.use_current_win_geometry_at_start_qaction)
        self.use_current_win_geometry_at_start_qaction.triggered.connect(
            self.on_use_current_win_geometry_at_start_triggered)

        self.dark_mode_qaction = QtWidgets.QAction("Dark mode")
        self.settings_menu.addAction(self.dark_mode_qaction)
        self.dark_mode_qaction.setCheckable(True)
        self.dark_mode_qaction.toggled.connect(self.on_dark_mode_toggled)

        # self.playlists_menu = QtWidgets.QMenu("Playlists")
        # self.menu_bar.addMenu(self.playlists_menu)

        self.help_menu = QtWidgets.QMenu("Help")
        self.menu_bar.addMenu(self.help_menu)

        self.about_qaction = QtWidgets.QAction("About")
        self.help_menu.addAction(self.about_qaction)
        self.about_qaction.triggered.connect(self.on_about_triggered)

        self.user_guide_qaction = QtWidgets.QAction("User Guide")
        self.help_menu.addAction(self.user_guide_qaction)
        self.user_guide_qaction.triggered.connect(self.on_user_guide_triggered)

        # Setup

        start_dir = config.get_start_dir()
        self._change_active_dir(start_dir)
        all_areas = [e for e in GuiAreasEnum]
        self.update_gui(all_areas)
        # self.show_dirs_first_qrb.click()

        if i_cmd_arg_file:
            fd_type_enum = get_fd_type(i_cmd_arg_file)
            is_file_bool = os.path.isfile(i_cmd_arg_file)
            if is_file_bool and fd_type_enum == FDTypeEnum.music_file:
                cmd_arg_dir_path_str = os.path.dirname(i_cmd_arg_file)
                self._change_active_dir(cmd_arg_dir_path_str)
                self._add_file_to_playlist(i_cmd_arg_file)
                self._play()

        self.setGeometry(
            config.get_win_x(), config.get_win_y(),
            config.get_win_width(), config.get_win_height()
        )

        self.update_palette()

    def on_user_guide_triggered(self):
        markdown_dialog = QtWidgets.QDialog(self)
        vbox = QtWidgets.QVBoxLayout()
        markdown_dialog.setLayout(vbox)
        markdown_dialog.setMinimumWidth(500)
        markdown_dialog.setMinimumHeight(600)
        # markdown_dialog.setBaseSize(700, 500)

        text_edit = QtWidgets.QTextEdit()
        vbox.addWidget(text_edit)
        text_edit.setReadOnly(True)
        text_edit.zoomIn(2)

        with open(globa.get_project_path("README.md")) as f:
            readme_contents: str = f.read()
            text_edit.setMarkdown(readme_contents)

        markdown_dialog.show()

    def on_gentle_quit_triggered(self):
        if self.state_enum in (StateEnum.playing, StateEnum.stop_after_current):
            fade_ms_int = 1000 * self.fade_qsb.value()
            start_vol_int = self.volume_qsr.value()
            self.fade_timer.start(fade_ms_int, start_vol_int, self.gentle_quit_triggered_callback)
            self.state_enum = StateEnum.stopping_fade
            self.update_gui()
        else:
            self.gentle_quit_triggered_callback()

    def gentle_quit_triggered_callback(self):
        sys.exit(0)

    def on_dark_mode_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        config.set_dark_mode(i_checked)
        self.update_palette()

    def update_palette(self):
        # Integrating this into update_gui()?
        self.updating_gui_bool = True
        dark_mode_bl = config.get_dark_mode()
        self.dark_mode_qaction.setChecked(dark_mode_bl)
        if dark_mode_bl:
            dark_qp = globa.get_palette(globa.PaletteTypeEnum.dark)
            QtGui.QGuiApplication.setPalette(dark_qp)
        else:
            light_qp = globa.get_palette(globa.PaletteTypeEnum.light)
            QtGui.QGuiApplication.setPalette(light_qp)
        self.updating_gui_bool = False

    def on_fd_actions_menu_triggered(self, i_action: QtWidgets.QAction):
        pass

    def on_fav_dir_menu_action_triggered(self, i_action: QtWidgets.QAction):
        """
        This is called when one of the actions in the menu is clicked
        :param i_action: The action clicked
        """
        fav_dir_path: str = i_action.text()
        self._change_active_dir(fav_dir_path)
        self.update_gui([GuiAreasEnum.fd_controls])

    def on_about_triggered(self):
        caption_str = f"About {globa.APPLICATION_NAME_STR}"
        text_str = f"""{globa.APPLICATION_NAME_STR} version {globa.VERSION_STR}

{globa.SHORT_DESCRIPTION_STR}

Written in Python, and using Qt (through PyQt)

Created by {globa.AUTHOR_NAME_STR}

Application website: {globa.APPLICATION_WEBSITE_STR}"""
        QtWidgets.QMessageBox.about(self, caption_str, text_str)

    def on_fd_view_triggered(self):
        self.update_gui([GuiAreasEnum.fd_list])

    def on_quit_action_triggered(self):
        sys.exit()

    def on_use_current_win_geometry_at_start_triggered(self):
        config.set_win_x(self.x())
        config.set_win_y(self.y())
        config.set_win_width(self.width())
        config.set_win_height(self.height())

    def on_open_dir_triggered(self):
        globa.open_fd(self.active_dir_path_str)

    ##### PLAYLISTS #####

    def on_playlist_load_menu_triggered(self, i_action: QtWidgets.QAction):
        """
        This is called when one of the actions in the menu is clicked
        :param i_action: The action clicked
        """
        playlist_name: str = i_action.text()
        playlist_path = os.path.join(config.get_playlist_dir(), playlist_name)
        self._load_playlist(playlist_path)
        # self._change_active_dir(fav_dir_path)
        self.update_gui([GuiAreasEnum.tl_list])

    def _load_playlist(self, i_file_path_str):
        qurl = QtCore.QUrl.fromLocalFile(i_file_path_str)
        playlist_format_str = "m3u"
        self.media_playlist.clear()
        self.media_playlist.load(qurl, playlist_format_str)
        for i in range(self.media_playlist.mediaCount()):
            media = self.media_playlist.media(i)
            qurl = media.canonicalUrl()
            file_path_str = qurl.path()
            self._add_file_to_playlist(file_path_str)

    @globa.debug_dr
    def on_load_playlist_failed(self):
        """
        Have not been able to trigger this: Writing bug report about it?
        Qt docs: https://doc.qt.io/qt-5/qmediaplaylist.html#loadFailed
        :return:
        """
        logging.debug(f"self.media_player.errorString()=")
        QtWidgets.QMessageBox.warning(self,
            "Error loading playlist",
            "There was an error while trying to load the playlist"
        )

    @globa.debug_dr
    def on_playlist_loaded(self):
        pass

    def on_load_playlist_qaction(self):
        dir_path_str = config.get_playlist_dir()
        (file_path_str, ok) = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Please select playlist to load",
            directory=dir_path_str, filter="*.m3u"
        )
        if ok:
            self._load_playlist(file_path_str)

    def on_save_playlist_qaction(self):
        dir_path_str = config.get_playlist_dir()
        (save_file_path_str, ok_bool) = QtWidgets.QFileDialog.getSaveFileName(
            parent=self, caption="Please choose a place and name for your playlist file",
            directory=dir_path_str, filter="*.m3u"
        )
        if ok_bool:
            media_playlist = QtMultimedia.QMediaPlaylist()
            for i in range(self.playlist_qlw.count()):
                qlwi = self.playlist_qlw.item(i)
                path_str = qlwi.data(QtCore.Qt.UserRole)
                media = get_media_from_path(path_str)
                media_playlist.addMedia(media)
            if not save_file_path_str.lower().endswith(".m3u"):
                save_file_path_str += ".m3u"
            qurl = QtCore.QUrl.fromLocalFile(save_file_path_str)
            playlist_format_str = "m3u"
            success_bool = media_playlist.save(qurl, playlist_format_str)
            if not success_bool:
                error_str = media_playlist.errorString()
                logging.warning(f"{error_str=}")

    def on_open_playlist_directory_qaction(self):
        dir_path_str = config.get_playlist_dir()
        globa.open_fd(dir_path_str)

    def on_set_playlist_start_dir_triggered(self):
        old_dir_path_str = config.get_playlist_dir()
        dir_path_str = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self, caption="Please select the start dir for playlists",
            directory=old_dir_path_str
        )
        if dir_path_str:
            config.set_playlist_dir(dir_path_str)

    #####

    @globa.debug_dr
    def on_playlist_item_dropped(self):
        # Updating the currently playing track
        for row_int in range(self.playlist_qlw.count()):
            tl_qlwi = self.playlist_qlw.item(row_int)
            tl_font = tl_qlwi.font()
            if tl_font.bold():  # -using the fact that the currently playing track is shown in bold!
                self.tl_playing_row_int = row_int
                break
        self.update_gui([GuiAreasEnum.tl_list])
        # self.mpl_qmp.moveMedia(0, 2)

    @user_interaction_dr
    def on_fav_activated(self, i_index: int):
        # i_dir: str
        dir_str = self.favorites_menu_qpb.itemText(i_index)
        self._change_active_dir(dir_str)
        self.update_gui([GuiAreasEnum.fd_controls])

    @user_interaction_dr
    def on_is_fav_toggled(self, i_checked: bool):
        if i_checked:
            config.add_to_favs(self.active_dir_path_str)
        else:
            return_value_bool = config.pop_from_favs(self.active_dir_path_str)
            if return_value_bool:
                pass
            else:
                logging.warning("Tried to remove nonexisting key from fav_dirs_dict")
        self.update_gui([GuiAreasEnum.fd_controls])

    @globa.debug_dr
    def on_share_clicked(self):
        media = self.media_player.currentMedia()
        qurl = media.canonicalUrl()
        path_of_file_str = qurl.path()
        name_of_file_str = os.path.basename(path_of_file_str)
        logging.debug(f"{path_of_file_str=}")
        # path_of_file_str = "/home/sunyata/Downloads/fågelsång-mobil/storlom.mp3"

        if path_of_file_str:
            subject_email_str = f"A song i want to share with you! --- {name_of_file_str}"
            body_email_str = f"Shared using SunyataZero's mediaplayer - {globa.APPLICATION_WEBSITE_STR}"
            message_composition_str = (
                    "to=''," +
                    "subject='" + subject_email_str + "'," +
                    "body='" + body_email_str + "'," +
                    "attachment='" + path_of_file_str + "'"
            )
            subprocess.Popen(["thunderbird", "-compose", message_composition_str])

    def on_dir_up_clicked(self):
        parent_dir_path_str = os.path.dirname(self.active_dir_path_str)
        self._change_active_dir(parent_dir_path_str)

    def _change_active_dir(self, i_new_dir: str):
        self.active_dir_path_str = i_new_dir
        self.active_dir_path_qll.setText(i_new_dir)
        self.update_gui([GuiAreasEnum.fd_list])

    #####

    def on_fd_item_double_clicked(self, i_fd_qlwi: QtWidgets.QListWidgetItem):
        path_str = i_fd_qlwi.data(QtCore.Qt.UserRole)
        fd_type = get_fd_type(path_str)
        if fd_type == FDTypeEnum.music_file:
            self.on_add_to_playlist_as_next_and_play_clicked()
        elif fd_type == FDTypeEnum.directory:
            pass
        elif fd_type == FDTypeEnum.playlist_file:
            self._load_playlist(path_str)
        elif fd_type == FDTypeEnum.other_file:
            globa.open_fd(path_str)

    def on_fd_current_row_changed(self, i_fd_row: int):
        if i_fd_row == -1:
            return
        fd_qlwi = self.fd_qlw.item(i_fd_row)
        fd_path_str = fd_qlwi.data(QtCore.Qt.UserRole)
        type_enum = get_fd_type(fd_path_str)
        if type_enum == FDTypeEnum.directory:
            self._change_active_dir(fd_path_str)

    ##### Adding/inserting/removing from the playlist widget

    def on_clear_playlist_clicked(self):
        self.on_stop_clicked()
        self.playlist_qlw.clear()

    def on_duplicate_track_clicked(self):
        tl_selected_indexes_list = self.playlist_qlw.selectedIndexes()
        tl_selected_rows_list = []
        for model_index in tl_selected_indexes_list:
            tl_source_row_int = model_index.row()
            tl_selected_rows_list.append(tl_source_row_int)
        tl_selected_rows_list = sorted(tl_selected_rows_list)
        for tl_source_row_int in tl_selected_rows_list:
            tl_source_qlwi = self.playlist_qlw.item(tl_source_row_int)
            path_str = tl_source_qlwi.data(QtCore.Qt.UserRole)
            name_str = tl_source_qlwi.text()
            tl_dest_qlwi = QtWidgets.QListWidgetItem(name_str)
            tl_dest_qlwi.setData(QtCore.Qt.UserRole, path_str)
            self.playlist_qlw.addItem(tl_dest_qlwi)

    def on_remove_from_playlist_clicked(self):
        tl_selected_indexes_list = self.playlist_qlw.selectedIndexes()
        tl_selected_rows_list = []
        for model_index in tl_selected_indexes_list:
            tl_row_int = model_index.row()
            tl_selected_rows_list.append(tl_row_int)
        tl_selected_rows_list = sorted(tl_selected_rows_list, reverse=True)
        # -so that the last rows are removed first
        if self.tl_playing_row_int in tl_selected_rows_list:
            self.on_stop_clicked()
        for tl_row_int in tl_selected_rows_list:
            self.playlist_qlw.takeItem(tl_row_int)

    def on_add_to_playlist_as_next_clicked(self):
        fd_selected_indexes_list = self.fd_qlw.selectedIndexes()
        tl_pos_int = self.tl_playing_row_int + 1
        for fd_model_index in fd_selected_indexes_list:
            fd_row_int = fd_model_index.row()
            fd_qlwi = self.fd_qlw.item(fd_row_int)
            path_str = fd_qlwi.data(QtCore.Qt.UserRole)
            self._add_file_to_playlist(path_str, i_pos=tl_pos_int)
            tl_pos_int += 1
        self.fd_qlw.clearSelection()

    def _add_file_to_playlist(self, i_file_path: str, i_pos: int=-1):
        if not os.path.exists(i_file_path):
            return
        file_name_str = os.path.basename(i_file_path)
        qlwi = QtWidgets.QListWidgetItem(file_name_str)
        qlwi.setData(QtCore.Qt.UserRole, i_file_path)
        if i_pos == -1:  # -adding to the end of the list
            self.playlist_qlw.addItem(qlwi)
        else:  # -inserting at the specified position
            self.playlist_qlw.insertItem(i_pos, qlwi)
        """
        if self.media_player.isMetaDataAvailable():
            meta_data_keys_strlist = self.media_player.availableMetaData()
            logging.debug(f"{meta_data_keys_strlist=}")
            for meta_data_key_str in meta_data_keys_strlist:
                meta_data_value_str = self.media_player.metaData(meta_data_key_str)
                logging.debug(f"key: {meta_data_key_str}, value: {meta_data_value_str}")
        else:
            logging.debug("no meta data available")
        """

    ##### STATE CHANGES #####

    def _play(self):
        if self.playlist_qlw.count() == 0:
            logging.warning("No files to play")
            return
        if self.tl_playing_row_int == -1 and self.playlist_qlw.count() >= 1:
            self.tl_playing_row_int = 0
        tl_qlwi = self.playlist_qlw.item(self.tl_playing_row_int)
        if tl_qlwi is None:
            return
        """
        if self.state_enum == StateEnum.switching_fade:
            return  # -wait for the fade timer to send the signal

        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.fade_timer.reset()
            self.fade_timer.stop()
            self.media_player.stop()
        """
        path_str = tl_qlwi.data(QtCore.Qt.UserRole)
        media = get_media_from_path(path_str)
        self.media_player.setMedia(media)
        self.media_player.play()
        self.state_enum = StateEnum.playing
        self.update_gui([GuiAreasEnum.tl_list])

    def on_play_clicked(self):
        if self.state_enum in (StateEnum.paused,):
            self.media_player.play()  # -resuming
        elif self.state_enum in (StateEnum.stop_after_current,):
            self.state_enum = StateEnum.playing
            self.update_gui()
        elif self.state_enum in (StateEnum.stopped,):
            self._play()
        elif self.state_enum in (StateEnum.playing,):
            pass

    def on_playlist_item_dc(self, i_qlwi: QtWidgets.QListWidgetItem):
        next_track_row_int = self.playlist_qlw.currentRow()
        dc_callback_with_cur_row_func = functools.partial(self.playlist_item_dc_callback, next_track_row_int)
        if self.state_enum == StateEnum.playing:
            fade_ms_int = 1000 * self.fade_qsb.value()
            start_vol_int = self.volume_qsr.value()
            self.fade_timer.start(fade_ms_int, start_vol_int, dc_callback_with_cur_row_func)
            self.state_enum = StateEnum.switching_fade
            self.update_gui()
        else:
            dc_callback_with_cur_row_func()

    def playlist_item_dc_callback(self, i_new_track_tl_row: int):
        self.media_player.stop()
        self.tl_playing_row_int = i_new_track_tl_row
        self._play()

        error_enum = self.media_player.error()
        if error_enum != QtMultimedia.QMediaPlayer.NoError:
            error_str = self.media_player.errorString()
            logging.warning(f"{error_str=}")

    def on_next_clicked(self):
        fade_ms_int = 1000 * self.fade_qsb.value()
        start_vol_int = self.volume_qsr.value()
        self.fade_timer.start(fade_ms_int, start_vol_int, self.next_clicked_callback)
        self.state_enum = StateEnum.switching_fade
        self.update_gui([GuiAreasEnum.tl_list])

    def next_clicked_callback(self):
        self._next()

    def _next(self):
        if self.tl_playing_row_int < self.playlist_qlw.count() - 1:
            self.tl_playing_row_int += 1
            self._play()
        else:
            self._stop()

    def on_stop_clicked(self):
        if self.state_enum in (StateEnum.playing, StateEnum.stop_after_current):
            fade_ms_int = 1000 * self.fade_qsb.value()
            start_vol_int = self.volume_qsr.value()
            self.fade_timer.start(fade_ms_int, start_vol_int, self.stop_clicked_callback)
            self.state_enum = StateEnum.stopping_fade
            self.update_gui()
        elif self.state_enum in (StateEnum.paused,):
            self.stop_clicked_callback()
        elif self.state_enum in (StateEnum.stopped,):
            pass

    def stop_clicked_callback(self):
        self._stop()

    def _stop(self):
        self.tl_playing_row_int = -1
        self.state_enum = StateEnum.stopped
        self.seek_qsr.setValue(0)
        self.media_player.stop()
        self.update_gui([GuiAreasEnum.tl_list])

    def on_stop_after_current_clicked(self):
        if self.state_enum in (StateEnum.playing,):
            self.state_enum = StateEnum.stop_after_current
            self.update_gui()
        elif self.state_enum in (StateEnum.stop_after_current, StateEnum.stopped, StateEnum.paused):
            pass

    def on_pause_clicked(self):
        if self.state_enum in (StateEnum.playing, StateEnum.stop_after_current):
            fade_ms_int = 1000 * self.fade_qsb.value()
            start_vol_int = self.volume_qsr.value()
            self.fade_timer.start(fade_ms_int, start_vol_int, self.pause_clicked_callback)
            self.state_enum = StateEnum.pausing_fade
            self.update_gui()
        elif self.state_enum in (StateEnum.stopped, StateEnum.paused):
            pass

    def pause_clicked_callback(self):
        self.state_enum = StateEnum.paused
        self.media_player.pause()
        self.update_gui()

    def on_fade_timer_updated(self, i_is_done: bool, i_new_volume: int):
        percent_done_int = self.fade_timer.get_percent_done()
        self.fade_out_qpb.setValue(percent_done_int)
        self.volume_qsr.setValue(i_new_volume)
        if i_is_done:
            self.fade_timer.callback_func()

    def on_add_to_playlist_as_next_and_play_clicked(self):
        # tricky to use a decortor on this since the signal will send the checked state along with self:
        # "TypeError: on_add_to_playlist_as_next_and_play_clicked() takes 1 positional argument but 2 were given"
        self.on_add_to_playlist_as_next_clicked()
        if self.media_player.state() == QtMultimedia.QMediaPlayer.StoppedState:
            self._play()
        elif self.media_player.state() in (QtMultimedia.QMediaPlayer.PlayingState,
                QtMultimedia.QMediaPlayer.PausedState):
            self.on_next_clicked()

    def on_add_to_playlist_clicked(self):
        selected_indexes_list = self.fd_qlw.selectedIndexes()
        for model_index in selected_indexes_list:
            row_int = model_index.row()
            qlwi = self.fd_qlw.item(row_int)
            path_str = qlwi.data(QtCore.Qt.UserRole)
            self._add_file_to_playlist(path_str)
        self.fd_qlw.clearSelection()
        self.update_gui([GuiAreasEnum.tl_list])

    def on_media_status_changed(self, i_media_status):
        # See also on_current_media_changed
        # Many values: https://doc.qt.io/qt-5/qmediaplayer.html#MediaStatus-enum
        if i_media_status == QtMultimedia.QMediaPlayer.EndOfMedia:
            if self.state_enum == StateEnum.stop_after_current:
                self._stop()
            else:
                self.fade_timer.reset()
                self._next()

    def on_current_media_changed(self, i_media: QtMultimedia.QMediaContent):
        # See also on_media_status_changed
        qurl = i_media.canonicalUrl()
        file_name_str = qurl.fileName()
        logging.debug(f"on_current_media_changed, {file_name_str=}")
        self.track_title_qll.setText(file_name_str)
        self.update_gui([GuiAreasEnum.tl_list])

    def on_duration_changed(self, i_new_duration_ms: int):
        # if self.media_player.isSeekable():
        # currentmediachanged durationchanged signal
        # duration_ms_int = self.media_player.duration()
        logging.debug(f"on_duration_changed, {i_new_duration_ms=}")
        self.seek_qsr.setMaximum(i_new_duration_ms)

        durations_secs_int = i_new_duration_ms // 1000
        duration_minutes_int = durations_secs_int // 60
        duration_remaining_secs_int = durations_secs_int % 60
        duration_remaining_secs_str = str(duration_remaining_secs_int).zfill(2)
        duration_str = f"{duration_minutes_int}:{duration_remaining_secs_str}"
        self.duration_qll.setText(duration_str)

    def on_media_pos_changed(self, i_new_pos_ms: int):
        self.updating_position_bool = True
        self.seek_qsr.setValue(i_new_pos_ms)
        self.updating_position_bool = False

    def on_seek_changed(self, i_new_value: int):
        if self.updating_position_bool:
            return
        self.media_player.setPosition(i_new_value)

    @user_interaction_dr
    def on_volume_slider_changed(self, i_new_volume):
        self.media_player.setVolume(i_new_volume)

    def on_about_to_quit(self):
        logging.debug("on_about_to_quit")
        # config.set_fav_dict(self.fav_dirs_dict)

    @gui_update_dr
    def update_gui(self, i_gui_areas: [GuiAreasEnum] = None):
        if i_gui_areas is None:
            i_gui_areas = []

        if self.state_enum in (StateEnum.switching_fade, StateEnum.stopping_fade, StateEnum.pausing_fade):
            self.now_playing_qsl.setCurrentWidget(self.fade_out_qw)
        else:
            self.now_playing_qsl.setCurrentWidget(self.btm_controls_qw)

        state_str = self.state_enum.name
        self.state_qll.setText("State: " + state_str)
        # self.fade_out_qpb.setFormat("State: " + state_str)

        if GuiAreasEnum.fd_list in i_gui_areas:
            if not self.active_dir_path_str:
                return
            """
            if not os.path.isdir(self.active_dir_path_str):
                self.active_dir_path_str = config.get_start_dir()
                return
            """
            self.fd_qlw.clear()
            fd_name_list = os.listdir(self.active_dir_path_str)
            fd_name_list = sorted(fd_name_list)
            dir_name_list = []
            music_file_name_list = []
            playlist_file_name_list = []
            other_file_name_list = []
            for fd_name_str in fd_name_list:
                fd_path_str = os.path.join(self.active_dir_path_str, fd_name_str)
                fd_type = get_fd_type(fd_path_str)
                if fd_type == FDTypeEnum.hidden_fd:
                    continue  # -skipped
                elif fd_type == FDTypeEnum.directory:
                    dir_name_list.append(fd_name_str)
                elif fd_type == FDTypeEnum.music_file:
                    music_file_name_list.append(fd_name_str)
                elif fd_type == FDTypeEnum.playlist_file:
                    playlist_file_name_list.append(fd_name_str)
                elif fd_type == FDTypeEnum.other_file:
                    other_file_name_list.append(fd_name_str)

            def add_directories():
                for name_str in sorted(dir_name_list):
                    path_str = os.path.join(self.active_dir_path_str, name_str)
                    qlwi = QtWidgets.QListWidgetItem(parent=self.fd_qlw)
                    qlwi.setFlags(QtCore.Qt.ItemIsEnabled)
                    color = QtGui.QColor(230, 230, 230)
                    start_color = QtGui.QColor(240, 240, 240)
                    stop_color = QtGui.QColor(255, 255, 255)
                    gradient = QtGui.QLinearGradient()
                    gradient.setSpread(QtGui.QLinearGradient.PadSpread)
                    gradient.setStart(0, 0)
                    gradient.setFinalStop(0, 20)
                    gradient.setColorAt(0, start_color)
                    gradient.setColorAt(1, stop_color)
                    brush = QtGui.QBrush(color)
                    # qlwi.setBackground(brush)
                    qlwi.setText("> " + name_str)
                    # qlwi.setText(name_str)
                    qlwi.setData(QtCore.Qt.UserRole, path_str)
                    self.fd_qlw.addItem(qlwi)
            if self.show_dirs_first_qa.isChecked():
                add_directories()
            for name_str in sorted(music_file_name_list):
                path_str = os.path.join(self.active_dir_path_str, name_str)
                tl_qlwi = QtWidgets.QListWidgetItem(parent=self.fd_qlw)
                # self.fd_ref_list.append(tl_qlwi)
                tl_qlwi.setText(name_str)
                tl_qlwi.setData(QtCore.Qt.UserRole, path_str)
                self.fd_qlw.addItem(tl_qlwi)

            for name_str in sorted(playlist_file_name_list):
                path_str = os.path.join(self.active_dir_path_str, name_str)
                tl_qlwi = QtWidgets.QListWidgetItem(parent=self.fd_qlw)
                # self.fd_ref_list.append(tl_qlwi)
                tl_qlwi.setFlags(QtCore.Qt.ItemIsEnabled)
                # tl_qlwi.setFlags(QtCore.Qt.NoItemFlags)
                color = QtGui.QColor(100, 100, 100)
                brush = QtGui.QBrush(color)
                tl_qlwi.setForeground(brush)
                tl_qlwi.setText(name_str)
                new_font = tl_qlwi.font()
                new_font.setItalic(True)
                tl_qlwi.setFont(new_font)
                tl_qlwi.setData(QtCore.Qt.UserRole, path_str)
                self.fd_qlw.addItem(tl_qlwi)

            for name_str in sorted(other_file_name_list):
                path_str = os.path.join(self.active_dir_path_str, name_str)
                tl_qlwi = QtWidgets.QListWidgetItem(parent=self.fd_qlw)
                # self.fd_ref_list.append(tl_qlwi)
                tl_qlwi.setFlags(QtCore.Qt.ItemIsEnabled)
                # tl_qlwi.setFlags(QtCore.Qt.NoItemFlags)
                color = QtGui.QColor(100, 100, 100)
                brush = QtGui.QBrush(color)
                tl_qlwi.setForeground(brush)
                tl_qlwi.setText(name_str)
                tl_qlwi.setData(QtCore.Qt.UserRole, path_str)
                self.fd_qlw.addItem(tl_qlwi)
            if self.show_dirs_last_qa.isChecked():
                add_directories()

        if GuiAreasEnum.fd_controls in i_gui_areas:
            pass

        if GuiAreasEnum.fd_list in i_gui_areas:
            fav_dict = config.get_fav_dirs_dict()
            if self.active_dir_path_str in fav_dict.keys():
                self.is_fav_action.setChecked(True)
            else:
                self.is_fav_action.setChecked(False)

        if GuiAreasEnum.tl_list in i_gui_areas:
            for i in range(0, self.playlist_qlw.count()):
                tl_qlwi = self.playlist_qlw.item(i)
                font = QtGui.QFont()
                tl_qlwi.setFont(font)
            if self.tl_playing_row_int != -1:
                tl_qlwi = self.playlist_qlw.item(self.tl_playing_row_int)
                font = tl_qlwi.font()
                font.setBold(True)
                tl_qlwi.setFont(font)

        self.tq_playlist_load_menu.clear()
        dir_path_str = config.get_playlist_dir()
        for file_name_str in os.listdir(dir_path_str):
            if file_name_str.lower().endswith(tuple(supported_playlist_suffixes_list)):
                qaction = QtWidgets.QAction(file_name_str, parent=self)
                self.tq_playlist_load_menu.addAction(qaction)


        fav_dict = config.get_fav_dirs_dict()
        self.fd_fav_dirs_menu.clear()
        for key, value in fav_dict.items():
            qaction = QtWidgets.QAction(key, parent=self)
            self.fd_fav_dirs_menu.addAction(qaction)
        ##### self.favorites_qcb.setCurrentIndex(-1)

        """
        self.fav_playlists_menu.clear()
        dir_path_str = config.get_playlist_dir()
        for file_name_str in os.listdir(dir_path_str):
            if file_name_str.lower().endswith(tuple(supported_playlist_suffixes_list)):
                file_path_str = os.path.join(dir_path_str, file_name_str)
                logging.debug(f"on_fav_playlists_menu_triggered, {file_path_str=}")
                load_this_playlist_func = functools.partial(self._load_playlist, file_path_str)
                load_this_playlist_qaction = QtWidgets.QAction(
                    text=file_name_str,
                    parent=self.playlists_in_start_dir_qmenu
                )
                load_this_playlist_qaction.triggered.connect(load_this_playlist_func)
                self.fav_playlists_menu.addAction(load_this_playlist_qaction)
        """
