# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_session.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_GameSessionWindow(object):
    def setupUi(self, GameSessionWindow):
        if not GameSessionWindow.objectName():
            GameSessionWindow.setObjectName(u"GameSessionWindow")
        GameSessionWindow.resize(699, 489)
        self.action_add_player = QAction(GameSessionWindow)
        self.action_add_player.setObjectName(u"action_add_player")
        self.action_add_row = QAction(GameSessionWindow)
        self.action_add_row.setObjectName(u"action_add_row")
        self.central_widget = QWidget(GameSessionWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setMaximumSize(QSize(16777215, 16777215))
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(6)
        self.main_layout.setContentsMargins(11, 11, 11, 11)
        self.main_layout.setObjectName(u"main_layout")
        self.title_layout = QHBoxLayout()
        self.title_layout.setSpacing(6)
        self.title_layout.setObjectName(u"title_layout")
        self.session_name_label = QLabel(self.central_widget)
        self.session_name_label.setObjectName(u"session_name_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.session_name_label.sizePolicy().hasHeightForWidth())
        self.session_name_label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.session_name_label.setFont(font)

        self.title_layout.addWidget(self.session_name_label)

        self.advanced_options_tool = QToolButton(self.central_widget)
        self.advanced_options_tool.setObjectName(u"advanced_options_tool")
        self.advanced_options_tool.setPopupMode(QToolButton.InstantPopup)

        self.title_layout.addWidget(self.advanced_options_tool)


        self.main_layout.addLayout(self.title_layout)

        self.players_box = QGroupBox(self.central_widget)
        self.players_box.setObjectName(u"players_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.players_box.sizePolicy().hasHeightForWidth())
        self.players_box.setSizePolicy(sizePolicy1)
        self.players_layout = QGridLayout(self.players_box)
        self.players_layout.setSpacing(6)
        self.players_layout.setContentsMargins(11, 11, 11, 11)
        self.players_layout.setObjectName(u"players_layout")
        self.new_row_button = QPushButton(self.players_box)
        self.new_row_button.setObjectName(u"new_row_button")

        self.players_layout.addWidget(self.new_row_button, 0, 0, 1, 2)

        self.title_connection_state_label = QLabel(self.players_box)
        self.title_connection_state_label.setObjectName(u"title_connection_state_label")

        self.players_layout.addWidget(self.title_connection_state_label, 0, 5, 1, 1)

        self.players_vertical_line = QFrame(self.players_box)
        self.players_vertical_line.setObjectName(u"players_vertical_line")
        self.players_vertical_line.setFrameShape(QFrame.VLine)
        self.players_vertical_line.setFrameShadow(QFrame.Sunken)

        self.players_layout.addWidget(self.players_vertical_line, 0, 2, 2, 1)

        self.title_player_name_label = QLabel(self.players_box)
        self.title_player_name_label.setObjectName(u"title_player_name_label")

        self.players_layout.addWidget(self.title_player_name_label, 0, 4, 1, 1)

        self.presets_line = QFrame(self.players_box)
        self.presets_line.setObjectName(u"presets_line")
        self.presets_line.setFrameShape(QFrame.HLine)
        self.presets_line.setFrameShadow(QFrame.Sunken)

        self.players_layout.addWidget(self.presets_line, 1, 0, 1, 2)

        self.team_line = QFrame(self.players_box)
        self.team_line.setObjectName(u"team_line")
        self.team_line.setFrameShape(QFrame.HLine)
        self.team_line.setFrameShadow(QFrame.Sunken)

        self.players_layout.addWidget(self.team_line, 1, 4, 1, 3)


        self.main_layout.addWidget(self.players_box)

        self.observer_group = QGroupBox(self.central_widget)
        self.observer_group.setObjectName(u"observer_group")
        sizePolicy1.setHeightForWidth(self.observer_group.sizePolicy().hasHeightForWidth())
        self.observer_group.setSizePolicy(sizePolicy1)
        self.observer_layout = QGridLayout(self.observer_group)
        self.observer_layout.setSpacing(6)
        self.observer_layout.setContentsMargins(11, 11, 11, 11)
        self.observer_layout.setObjectName(u"observer_layout")

        self.main_layout.addWidget(self.observer_group)

        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setObjectName(u"tab_widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tab_widget.sizePolicy().hasHeightForWidth())
        self.tab_widget.setSizePolicy(sizePolicy2)
        self.tab_generate = QWidget()
        self.tab_generate.setObjectName(u"tab_generate")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tab_generate.sizePolicy().hasHeightForWidth())
        self.tab_generate.setSizePolicy(sizePolicy3)
        self.gridLayout = QGridLayout(self.tab_generate)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.view_game_details_button = QPushButton(self.tab_generate)
        self.view_game_details_button.setObjectName(u"view_game_details_button")

        self.gridLayout.addWidget(self.view_game_details_button, 1, 4, 1, 1)

        self.generate_game_label = QLabel(self.tab_generate)
        self.generate_game_label.setObjectName(u"generate_game_label")

        self.gridLayout.addWidget(self.generate_game_label, 1, 0, 1, 3)

        self.progress_label = QLabel(self.tab_generate)
        self.progress_label.setObjectName(u"progress_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.progress_label.sizePolicy().hasHeightForWidth())
        self.progress_label.setSizePolicy(sizePolicy4)
        self.progress_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.progress_label.setWordWrap(True)

        self.gridLayout.addWidget(self.progress_label, 4, 1, 1, 4)

        self.background_process_button = QToolButton(self.tab_generate)
        self.background_process_button.setObjectName(u"background_process_button")
        self.background_process_button.setMinimumSize(QSize(140, 0))
        self.background_process_button.setPopupMode(QToolButton.MenuButtonPopup)

        self.gridLayout.addWidget(self.background_process_button, 4, 0, 1, 1)

        self.customize_user_preferences_button = QPushButton(self.tab_generate)
        self.customize_user_preferences_button.setObjectName(u"customize_user_preferences_button")

        self.gridLayout.addWidget(self.customize_user_preferences_button, 1, 6, 1, 1)

        self.line_generate = QFrame(self.tab_generate)
        self.line_generate.setObjectName(u"line_generate")
        self.line_generate.setFrameShape(QFrame.HLine)
        self.line_generate.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_generate, 3, 0, 1, 7)

        self.progress_bar = QProgressBar(self.tab_generate)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)
        self.progress_bar.setInvertedAppearance(False)

        self.gridLayout.addWidget(self.progress_bar, 4, 5, 1, 2)

        self.save_iso_button = QToolButton(self.tab_generate)
        self.save_iso_button.setObjectName(u"save_iso_button")
        self.save_iso_button.setMinimumSize(QSize(100, 0))
        self.save_iso_button.setPopupMode(QToolButton.MenuButtonPopup)

        self.gridLayout.addWidget(self.save_iso_button, 1, 5, 1, 1)

        self.tab_widget.addTab(self.tab_generate, "")
        self.tab_history = QWidget()
        self.tab_history.setObjectName(u"tab_history")
        sizePolicy3.setHeightForWidth(self.tab_history.sizePolicy().hasHeightForWidth())
        self.tab_history.setSizePolicy(sizePolicy3)
        self.history_layout = QVBoxLayout(self.tab_history)
        self.history_layout.setSpacing(6)
        self.history_layout.setContentsMargins(11, 11, 11, 11)
        self.history_layout.setObjectName(u"history_layout")
        self.history_layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.history_layout.setContentsMargins(4, 4, 4, 4)
        self.history_table_widget = QTableWidget(self.tab_history)
        if (self.history_table_widget.columnCount() < 2):
            self.history_table_widget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.history_table_widget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.history_table_widget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.history_table_widget.setObjectName(u"history_table_widget")
        self.history_table_widget.horizontalHeader().setVisible(False)
        self.history_table_widget.horizontalHeader().setDefaultSectionSize(200)
        self.history_table_widget.verticalHeader().setVisible(False)

        self.history_layout.addWidget(self.history_table_widget)

        self.tab_widget.addTab(self.tab_history, "")

        self.main_layout.addWidget(self.tab_widget)

        self.connection_group = QGroupBox(self.central_widget)
        self.connection_group.setObjectName(u"connection_group")
        self.connection_group.setFlat(False)
        self.connection_layout = QHBoxLayout(self.connection_group)
        self.connection_layout.setSpacing(6)
        self.connection_layout.setContentsMargins(11, 11, 11, 11)
        self.connection_layout.setObjectName(u"connection_layout")
        self.connection_layout.setContentsMargins(-1, 4, -1, 4)
        self.game_connection_tool = QToolButton(self.connection_group)
        self.game_connection_tool.setObjectName(u"game_connection_tool")
        self.game_connection_tool.setPopupMode(QToolButton.InstantPopup)

        self.connection_layout.addWidget(self.game_connection_tool)

        self.game_connection_label = QLabel(self.connection_group)
        self.game_connection_label.setObjectName(u"game_connection_label")

        self.connection_layout.addWidget(self.game_connection_label)

        self.connection_line_1 = QFrame(self.connection_group)
        self.connection_line_1.setObjectName(u"connection_line_1")
        self.connection_line_1.setFrameShape(QFrame.VLine)
        self.connection_line_1.setFrameShadow(QFrame.Sunken)

        self.connection_layout.addWidget(self.connection_line_1)

        self.server_connection_button = QPushButton(self.connection_group)
        self.server_connection_button.setObjectName(u"server_connection_button")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.server_connection_button.sizePolicy().hasHeightForWidth())
        self.server_connection_button.setSizePolicy(sizePolicy5)
        self.server_connection_button.setMaximumSize(QSize(60, 16777215))

        self.connection_layout.addWidget(self.server_connection_button)

        self.server_connection_label = QLabel(self.connection_group)
        self.server_connection_label.setObjectName(u"server_connection_label")

        self.connection_layout.addWidget(self.server_connection_label)

        self.connection_line_2 = QFrame(self.connection_group)
        self.connection_line_2.setObjectName(u"connection_line_2")
        self.connection_line_2.setFrameShape(QFrame.VLine)
        self.connection_line_2.setFrameShadow(QFrame.Sunken)

        self.connection_layout.addWidget(self.connection_line_2)

        self.session_status_tool = QToolButton(self.connection_group)
        self.session_status_tool.setObjectName(u"session_status_tool")
        self.session_status_tool.setMaximumSize(QSize(80, 16777215))
        self.session_status_tool.setPopupMode(QToolButton.MenuButtonPopup)

        self.connection_layout.addWidget(self.session_status_tool)

        self.session_status_label = QLabel(self.connection_group)
        self.session_status_label.setObjectName(u"session_status_label")

        self.connection_layout.addWidget(self.session_status_label)


        self.main_layout.addWidget(self.connection_group)

        GameSessionWindow.setCentralWidget(self.central_widget)
        self.menuBar = QMenuBar(GameSessionWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 699, 21))
        GameSessionWindow.setMenuBar(self.menuBar)

        self.retranslateUi(GameSessionWindow)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(GameSessionWindow)
    # setupUi

    def retranslateUi(self, GameSessionWindow):
        GameSessionWindow.setWindowTitle(QCoreApplication.translate("GameSessionWindow", u"Game Session", None))
        self.action_add_player.setText(QCoreApplication.translate("GameSessionWindow", u"Add player", None))
        self.action_add_row.setText(QCoreApplication.translate("GameSessionWindow", u"Add row", None))
        self.session_name_label.setText(QCoreApplication.translate("GameSessionWindow", u"Session name!", None))
        self.advanced_options_tool.setText(QCoreApplication.translate("GameSessionWindow", u"Advanced options...", None))
        self.players_box.setTitle("")
        self.new_row_button.setText(QCoreApplication.translate("GameSessionWindow", u"New Row", None))
        self.title_connection_state_label.setText(QCoreApplication.translate("GameSessionWindow", u"Connection state", None))
        self.title_player_name_label.setText(QCoreApplication.translate("GameSessionWindow", u"Players", None))
#if QT_CONFIG(tooltip)
        self.observer_group.setToolTip(QCoreApplication.translate("GameSessionWindow", u"<html><head/><body><p>These users won't participate on the match, but they can be admins and follow trackers.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.observer_group.setTitle(QCoreApplication.translate("GameSessionWindow", u"Observers", None))
        self.view_game_details_button.setText(QCoreApplication.translate("GameSessionWindow", u"View Spoiler", None))
        self.generate_game_label.setText(QCoreApplication.translate("GameSessionWindow", u"<Game not generated>", None))
        self.progress_label.setText("")
        self.background_process_button.setText(QCoreApplication.translate("GameSessionWindow", u"Stop", None))
        self.customize_user_preferences_button.setText(QCoreApplication.translate("GameSessionWindow", u"Customize in-game settings", None))
        self.save_iso_button.setText(QCoreApplication.translate("GameSessionWindow", u"Save ISO", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_generate), QCoreApplication.translate("GameSessionWindow", u"Game", None))
        ___qtablewidgetitem = self.history_table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("GameSessionWindow", u"Message", None));
        ___qtablewidgetitem1 = self.history_table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("GameSessionWindow", u"Time", None));
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_history), QCoreApplication.translate("GameSessionWindow", u"History", None))
        self.connection_group.setTitle("")
        self.game_connection_tool.setText(QCoreApplication.translate("GameSessionWindow", u"Connect to game", None))
        self.game_connection_label.setText(QCoreApplication.translate("GameSessionWindow", u"Game: Disconnected", None))
        self.server_connection_button.setText(QCoreApplication.translate("GameSessionWindow", u"Connect", None))
        self.server_connection_label.setText(QCoreApplication.translate("GameSessionWindow", u"Server: Disconnected", None))
        self.session_status_tool.setText(QCoreApplication.translate("GameSessionWindow", u"Start", None))
        self.session_status_label.setText(QCoreApplication.translate("GameSessionWindow", u"Session: Not Started", None))
    # retranslateUi

