# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logic_settings_window.ui'
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


class Ui_LogicSettingsWindow(object):
    def setupUi(self, LogicSettingsWindow):
        if not LogicSettingsWindow.objectName():
            LogicSettingsWindow.setObjectName(u"LogicSettingsWindow")
        LogicSettingsWindow.resize(765, 702)
        self.verticalLayout = QVBoxLayout(LogicSettingsWindow)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 4, 0, 0)
        self.menuBar = QMenuBar(LogicSettingsWindow)
        self.menuBar.setObjectName(u"menuBar")

        self.verticalLayout.addWidget(self.menuBar)

        self.name_layout = QHBoxLayout()
        self.name_layout.setSpacing(6)
        self.name_layout.setObjectName(u"name_layout")
        self.name_label = QLabel(LogicSettingsWindow)
        self.name_label.setObjectName(u"name_label")

        self.name_layout.addWidget(self.name_label)

        self.name_edit = QLineEdit(LogicSettingsWindow)
        self.name_edit.setObjectName(u"name_edit")

        self.name_layout.addWidget(self.name_edit)


        self.verticalLayout.addLayout(self.name_layout)

        self.main_tab_widget = QTabWidget(LogicSettingsWindow)
        self.main_tab_widget.setObjectName(u"main_tab_widget")
        self.logic_tab = QWidget()
        self.logic_tab.setObjectName(u"logic_tab")
        self.logic_tab_layout = QVBoxLayout(self.logic_tab)
        self.logic_tab_layout.setSpacing(6)
        self.logic_tab_layout.setContentsMargins(11, 11, 11, 11)
        self.logic_tab_layout.setObjectName(u"logic_tab_layout")
        self.logic_tab_layout.setContentsMargins(0, 0, 0, 0)
        self.logic_tab_widget = QTabWidget(self.logic_tab)
        self.logic_tab_widget.setObjectName(u"logic_tab_widget")
        self.trick_level_tab = QWidget()
        self.trick_level_tab.setObjectName(u"trick_level_tab")
        self.trick_level_top_layout = QVBoxLayout(self.trick_level_tab)
        self.trick_level_top_layout.setSpacing(6)
        self.trick_level_top_layout.setContentsMargins(11, 11, 11, 11)
        self.trick_level_top_layout.setObjectName(u"trick_level_top_layout")
        self.trick_level_top_layout.setContentsMargins(0, 0, 0, 0)
        self.trick_level_scroll = QScrollArea(self.trick_level_tab)
        self.trick_level_scroll.setObjectName(u"trick_level_scroll")
        self.trick_level_scroll.setFrameShape(QFrame.NoFrame)
        self.trick_level_scroll.setFrameShadow(QFrame.Plain)
        self.trick_level_scroll.setWidgetResizable(True)
        self.trick_level_scroll_contents = QWidget()
        self.trick_level_scroll_contents.setObjectName(u"trick_level_scroll_contents")
        self.trick_level_scroll_contents.setGeometry(QRect(0, 0, 757, 559))
        self.trick_level_layout = QVBoxLayout(self.trick_level_scroll_contents)
        self.trick_level_layout.setSpacing(6)
        self.trick_level_layout.setContentsMargins(11, 11, 11, 11)
        self.trick_level_layout.setObjectName(u"trick_level_layout")
        self.trick_level_layout.setContentsMargins(4, 8, 4, 0)
        self.logic_description_label = QLabel(self.trick_level_scroll_contents)
        self.logic_description_label.setObjectName(u"logic_description_label")
        self.logic_description_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.logic_description_label.setWordWrap(True)

        self.trick_level_layout.addWidget(self.logic_description_label)

        self.trick_level_line_1 = QFrame(self.trick_level_scroll_contents)
        self.trick_level_line_1.setObjectName(u"trick_level_line_1")
        self.trick_level_line_1.setFrameShape(QFrame.HLine)
        self.trick_level_line_1.setFrameShadow(QFrame.Sunken)

        self.trick_level_layout.addWidget(self.trick_level_line_1)

        self.trick_level_minimal_logic_check = QCheckBox(self.trick_level_scroll_contents)
        self.trick_level_minimal_logic_check.setObjectName(u"trick_level_minimal_logic_check")

        self.trick_level_layout.addWidget(self.trick_level_minimal_logic_check)

        self.trick_level_minimal_logic_label = QLabel(self.trick_level_scroll_contents)
        self.trick_level_minimal_logic_label.setObjectName(u"trick_level_minimal_logic_label")
        self.trick_level_minimal_logic_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.trick_level_minimal_logic_label.setWordWrap(True)

        self.trick_level_layout.addWidget(self.trick_level_minimal_logic_label)

        self.trick_level_line_2 = QFrame(self.trick_level_scroll_contents)
        self.trick_level_line_2.setObjectName(u"trick_level_line_2")
        self.trick_level_line_2.setFrameShape(QFrame.HLine)
        self.trick_level_line_2.setFrameShadow(QFrame.Sunken)

        self.trick_level_layout.addWidget(self.trick_level_line_2)

        self.trick_level_help_label = QLabel(self.trick_level_scroll_contents)
        self.trick_level_help_label.setObjectName(u"trick_level_help_label")
        self.trick_level_help_label.setWordWrap(True)

        self.trick_level_layout.addWidget(self.trick_level_help_label)

        self.trick_level_scroll.setWidget(self.trick_level_scroll_contents)

        self.trick_level_top_layout.addWidget(self.trick_level_scroll)

        self.logic_tab_widget.addTab(self.trick_level_tab, "")
        self.logic_damage_tab = QWidget()
        self.logic_damage_tab.setObjectName(u"logic_damage_tab")
        self.logic_damage_layout = QVBoxLayout(self.logic_damage_tab)
        self.logic_damage_layout.setSpacing(6)
        self.logic_damage_layout.setContentsMargins(11, 11, 11, 11)
        self.logic_damage_layout.setObjectName(u"logic_damage_layout")
        self.logic_damage_layout.setContentsMargins(0, 0, 0, 0)
        self.damage_strictness_group = QGroupBox(self.logic_damage_tab)
        self.damage_strictness_group.setObjectName(u"damage_strictness_group")
        self.damage_strictness_layout = QVBoxLayout(self.damage_strictness_group)
        self.damage_strictness_layout.setSpacing(6)
        self.damage_strictness_layout.setContentsMargins(11, 11, 11, 11)
        self.damage_strictness_layout.setObjectName(u"damage_strictness_layout")
        self.damage_strictness_label = QLabel(self.damage_strictness_group)
        self.damage_strictness_label.setObjectName(u"damage_strictness_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.damage_strictness_label.sizePolicy().hasHeightForWidth())
        self.damage_strictness_label.setSizePolicy(sizePolicy)
        self.damage_strictness_label.setWordWrap(True)

        self.damage_strictness_layout.addWidget(self.damage_strictness_label)

        self.damage_strictness_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.damage_strictness_layout.addItem(self.damage_strictness_spacer)

        self.damage_strictness_combo = QComboBox(self.damage_strictness_group)
        self.damage_strictness_combo.addItem("")
        self.damage_strictness_combo.addItem("")
        self.damage_strictness_combo.addItem("")
        self.damage_strictness_combo.setObjectName(u"damage_strictness_combo")

        self.damage_strictness_layout.addWidget(self.damage_strictness_combo)


        self.logic_damage_layout.addWidget(self.damage_strictness_group)

        self.damage_strictness_spacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.logic_damage_layout.addItem(self.damage_strictness_spacer_2)

        self.logic_tab_widget.addTab(self.logic_damage_tab, "")
        self.location_pool_tab = QWidget()
        self.location_pool_tab.setObjectName(u"location_pool_tab")
        self.location_pool_layout = QVBoxLayout(self.location_pool_tab)
        self.location_pool_layout.setSpacing(6)
        self.location_pool_layout.setContentsMargins(11, 11, 11, 11)
        self.location_pool_layout.setObjectName(u"location_pool_layout")
        self.location_pool_layout.setContentsMargins(0, 0, 0, 0)
        self.randomization_mode_group = QGroupBox(self.location_pool_tab)
        self.randomization_mode_group.setObjectName(u"randomization_mode_group")
        self.verticalLayout_2 = QVBoxLayout(self.randomization_mode_group)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.randomization_mode_label = QLabel(self.randomization_mode_group)
        self.randomization_mode_label.setObjectName(u"randomization_mode_label")
        self.randomization_mode_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.randomization_mode_label)

        self.randomization_mode_combo = QComboBox(self.randomization_mode_group)
        self.randomization_mode_combo.addItem("")
        self.randomization_mode_combo.addItem("")
        self.randomization_mode_combo.setObjectName(u"randomization_mode_combo")

        self.verticalLayout_2.addWidget(self.randomization_mode_combo)


        self.location_pool_layout.addWidget(self.randomization_mode_group)

        self.excluded_locations_group = QGroupBox(self.location_pool_tab)
        self.excluded_locations_group.setObjectName(u"excluded_locations_group")
        self.verticalLayout_5 = QVBoxLayout(self.excluded_locations_group)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(2, 3, 2, 0)
        self.excluded_locations_label = QLabel(self.excluded_locations_group)
        self.excluded_locations_label.setObjectName(u"excluded_locations_label")

        self.verticalLayout_5.addWidget(self.excluded_locations_label)

        self.excluded_locations_area = QScrollArea(self.excluded_locations_group)
        self.excluded_locations_area.setObjectName(u"excluded_locations_area")
        self.excluded_locations_area.setWidgetResizable(True)
        self.excluded_locations_area_contents = QWidget()
        self.excluded_locations_area_contents.setObjectName(u"excluded_locations_area_contents")
        self.excluded_locations_area_contents.setGeometry(QRect(0, 0, 745, 356))
        self.excluded_locations_area_layout = QHBoxLayout(self.excluded_locations_area_contents)
        self.excluded_locations_area_layout.setSpacing(6)
        self.excluded_locations_area_layout.setContentsMargins(11, 11, 11, 11)
        self.excluded_locations_area_layout.setObjectName(u"excluded_locations_area_layout")
        self.excluded_locations_area_layout.setContentsMargins(0, 0, 0, 0)
        self.excluded_locations_area.setWidget(self.excluded_locations_area_contents)

        self.verticalLayout_5.addWidget(self.excluded_locations_area)


        self.location_pool_layout.addWidget(self.excluded_locations_group)

        self.logic_tab_widget.addTab(self.location_pool_tab, "")

        self.logic_tab_layout.addWidget(self.logic_tab_widget)

        self.main_tab_widget.addTab(self.logic_tab, "")
        self.patches_tab = QWidget()
        self.patches_tab.setObjectName(u"patches_tab")
        self.patches_tab_layout = QVBoxLayout(self.patches_tab)
        self.patches_tab_layout.setSpacing(6)
        self.patches_tab_layout.setContentsMargins(11, 11, 11, 11)
        self.patches_tab_layout.setObjectName(u"patches_tab_layout")
        self.patches_tab_layout.setContentsMargins(0, 0, 0, 0)
        self.patches_tab_widget = QTabWidget(self.patches_tab)
        self.patches_tab_widget.setObjectName(u"patches_tab_widget")
        self.energy_tab = QWidget()
        self.energy_tab.setObjectName(u"energy_tab")
        self.energy_layout = QVBoxLayout(self.energy_tab)
        self.energy_layout.setSpacing(6)
        self.energy_layout.setContentsMargins(11, 11, 11, 11)
        self.energy_layout.setObjectName(u"energy_layout")
        self.energy_layout.setContentsMargins(0, 0, 0, 0)
        self.energy_tank_box = QGroupBox(self.energy_tab)
        self.energy_tank_box.setObjectName(u"energy_tank_box")
        self.gridLayout_2 = QGridLayout(self.energy_tank_box)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.dangerous_tank_check = QCheckBox(self.energy_tank_box)
        self.dangerous_tank_check.setObjectName(u"dangerous_tank_check")

        self.gridLayout_2.addWidget(self.dangerous_tank_check, 4, 0, 1, 2)

        self.energy_tank_capacity_description = QLabel(self.energy_tank_box)
        self.energy_tank_capacity_description.setObjectName(u"energy_tank_capacity_description")
        self.energy_tank_capacity_description.setWordWrap(True)

        self.gridLayout_2.addWidget(self.energy_tank_capacity_description, 0, 0, 1, 3)

        self.energy_tank_capacity_spin_box = QSpinBox(self.energy_tank_box)
        self.energy_tank_capacity_spin_box.setObjectName(u"energy_tank_capacity_spin_box")
        self.energy_tank_capacity_spin_box.setMinimum(2)
        self.energy_tank_capacity_spin_box.setMaximum(1000)

        self.gridLayout_2.addWidget(self.energy_tank_capacity_spin_box, 2, 2, 1, 1)

        self.energy_tank_capacity_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.energy_tank_capacity_spacer, 1, 1, 1, 1)

        self.line = QFrame(self.energy_tank_box)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line, 3, 0, 1, 3)

        self.energy_tank_capacity_label = QLabel(self.energy_tank_box)
        self.energy_tank_capacity_label.setObjectName(u"energy_tank_capacity_label")

        self.gridLayout_2.addWidget(self.energy_tank_capacity_label, 2, 0, 1, 1)


        self.energy_layout.addWidget(self.energy_tank_box)

        self.safe_zone_box = QGroupBox(self.energy_tab)
        self.safe_zone_box.setObjectName(u"safe_zone_box")
        self.gridLayout = QGridLayout(self.safe_zone_box)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.safe_zone_regen_spin = QDoubleSpinBox(self.safe_zone_box)
        self.safe_zone_regen_spin.setObjectName(u"safe_zone_regen_spin")
        self.safe_zone_regen_spin.setMaximum(100.000000000000000)
        self.safe_zone_regen_spin.setSingleStep(0.100000000000000)
        self.safe_zone_regen_spin.setValue(1.000000000000000)

        self.gridLayout.addWidget(self.safe_zone_regen_spin, 2, 1, 1, 1)

        self.safe_zone_regen_label = QLabel(self.safe_zone_box)
        self.safe_zone_regen_label.setObjectName(u"safe_zone_regen_label")

        self.gridLayout.addWidget(self.safe_zone_regen_label, 2, 0, 1, 1)

        self.safe_zone_logic_heal_check = QCheckBox(self.safe_zone_box)
        self.safe_zone_logic_heal_check.setObjectName(u"safe_zone_logic_heal_check")
        self.safe_zone_logic_heal_check.setEnabled(False)
        self.safe_zone_logic_heal_check.setChecked(True)

        self.gridLayout.addWidget(self.safe_zone_logic_heal_check, 1, 0, 1, 2)

        self.safe_zone_description = QLabel(self.safe_zone_box)
        self.safe_zone_description.setObjectName(u"safe_zone_description")

        self.gridLayout.addWidget(self.safe_zone_description, 0, 0, 1, 2)


        self.energy_layout.addWidget(self.safe_zone_box)

        self.dark_aether_box = QGroupBox(self.energy_tab)
        self.dark_aether_box.setObjectName(u"dark_aether_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dark_aether_box.sizePolicy().hasHeightForWidth())
        self.dark_aether_box.setSizePolicy(sizePolicy1)
        self.dark_aether_layout_2 = QGridLayout(self.dark_aether_box)
        self.dark_aether_layout_2.setSpacing(6)
        self.dark_aether_layout_2.setContentsMargins(11, 11, 11, 11)
        self.dark_aether_layout_2.setObjectName(u"dark_aether_layout_2")
        self.varia_suit_spin_box = QDoubleSpinBox(self.dark_aether_box)
        self.varia_suit_spin_box.setObjectName(u"varia_suit_spin_box")
        self.varia_suit_spin_box.setMaximum(60.000000000000000)
        self.varia_suit_spin_box.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.varia_suit_spin_box.setValue(6.000000000000000)

        self.dark_aether_layout_2.addWidget(self.varia_suit_spin_box, 2, 1, 1, 1)

        self.varia_suit_label = QLabel(self.dark_aether_box)
        self.varia_suit_label.setObjectName(u"varia_suit_label")

        self.dark_aether_layout_2.addWidget(self.varia_suit_label, 2, 0, 1, 1)

        self.dark_suit_label = QLabel(self.dark_aether_box)
        self.dark_suit_label.setObjectName(u"dark_suit_label")

        self.dark_aether_layout_2.addWidget(self.dark_suit_label, 3, 0, 1, 1)

        self.dark_suit_spin_box = QDoubleSpinBox(self.dark_aether_box)
        self.dark_suit_spin_box.setObjectName(u"dark_suit_spin_box")
        self.dark_suit_spin_box.setMaximum(60.000000000000000)
        self.dark_suit_spin_box.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.dark_suit_spin_box.setValue(1.200000000000000)

        self.dark_aether_layout_2.addWidget(self.dark_suit_spin_box, 3, 1, 1, 1)

        self.dark_aether_label = QLabel(self.dark_aether_box)
        self.dark_aether_label.setObjectName(u"dark_aether_label")
        sizePolicy.setHeightForWidth(self.dark_aether_label.sizePolicy().hasHeightForWidth())
        self.dark_aether_label.setSizePolicy(sizePolicy)
        self.dark_aether_label.setWordWrap(False)

        self.dark_aether_layout_2.addWidget(self.dark_aether_label, 0, 0, 1, 2)

        self.dark_aether_box_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.dark_aether_layout_2.addItem(self.dark_aether_box_spacer, 1, 0, 1, 2)


        self.energy_layout.addWidget(self.dark_aether_box)

        self.energy_tank_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.energy_layout.addItem(self.energy_tank_spacer)

        self.patches_tab_widget.addTab(self.energy_tab, "")
        self.elevator_tab = QWidget()
        self.elevator_tab.setObjectName(u"elevator_tab")
        self.elevator_layout = QVBoxLayout(self.elevator_tab)
        self.elevator_layout.setSpacing(6)
        self.elevator_layout.setContentsMargins(11, 11, 11, 11)
        self.elevator_layout.setObjectName(u"elevator_layout")
        self.elevator_layout.setContentsMargins(4, 8, 4, 0)
        self.elevators_description_label = QLabel(self.elevator_tab)
        self.elevators_description_label.setObjectName(u"elevators_description_label")
        self.elevators_description_label.setWordWrap(True)

        self.elevator_layout.addWidget(self.elevators_description_label)

        self.elevators_combo = QComboBox(self.elevator_tab)
        self.elevators_combo.addItem("")
        self.elevators_combo.addItem("")
        self.elevators_combo.addItem("")
        self.elevators_combo.addItem("")
        self.elevators_combo.addItem("")
        self.elevators_combo.setObjectName(u"elevators_combo")

        self.elevator_layout.addWidget(self.elevators_combo)

        self.patches_tab_widget.addTab(self.elevator_tab, "")
        self.starting_area_tab = QWidget()
        self.starting_area_tab.setObjectName(u"starting_area_tab")
        self.starting_area_layout = QVBoxLayout(self.starting_area_tab)
        self.starting_area_layout.setSpacing(6)
        self.starting_area_layout.setContentsMargins(11, 11, 11, 11)
        self.starting_area_layout.setObjectName(u"starting_area_layout")
        self.starting_area_layout.setContentsMargins(4, 8, 4, 0)
        self.startingarea_description = QLabel(self.starting_area_tab)
        self.startingarea_description.setObjectName(u"startingarea_description")
        self.startingarea_description.setWordWrap(True)

        self.starting_area_layout.addWidget(self.startingarea_description)

        self.starting_area_quick_fill_layout = QHBoxLayout()
        self.starting_area_quick_fill_layout.setSpacing(6)
        self.starting_area_quick_fill_layout.setObjectName(u"starting_area_quick_fill_layout")
        self.starting_area_quick_fill_label = QLabel(self.starting_area_tab)
        self.starting_area_quick_fill_label.setObjectName(u"starting_area_quick_fill_label")

        self.starting_area_quick_fill_layout.addWidget(self.starting_area_quick_fill_label)

        self.starting_area_quick_fill_ship = QPushButton(self.starting_area_tab)
        self.starting_area_quick_fill_ship.setObjectName(u"starting_area_quick_fill_ship")

        self.starting_area_quick_fill_layout.addWidget(self.starting_area_quick_fill_ship)

        self.starting_area_quick_fill_save_station = QPushButton(self.starting_area_tab)
        self.starting_area_quick_fill_save_station.setObjectName(u"starting_area_quick_fill_save_station")

        self.starting_area_quick_fill_layout.addWidget(self.starting_area_quick_fill_save_station)


        self.starting_area_layout.addLayout(self.starting_area_quick_fill_layout)

        self.starting_locations_area = QScrollArea(self.starting_area_tab)
        self.starting_locations_area.setObjectName(u"starting_locations_area")
        self.starting_locations_area.setWidgetResizable(True)
        self.starting_locations_contents = QWidget()
        self.starting_locations_contents.setObjectName(u"starting_locations_contents")
        self.starting_locations_contents.setGeometry(QRect(0, 0, 76, 16))
        self.starting_locations_layout = QGridLayout(self.starting_locations_contents)
        self.starting_locations_layout.setSpacing(6)
        self.starting_locations_layout.setContentsMargins(11, 11, 11, 11)
        self.starting_locations_layout.setObjectName(u"starting_locations_layout")
        self.starting_locations_layout.setContentsMargins(4, 4, 4, 4)
        self.starting_locations_area.setWidget(self.starting_locations_contents)

        self.starting_area_layout.addWidget(self.starting_locations_area)

        self.patches_tab_widget.addTab(self.starting_area_tab, "")

        self.patches_tab_layout.addWidget(self.patches_tab_widget)

        self.main_tab_widget.addTab(self.patches_tab, "")

        self.verticalLayout.addWidget(self.main_tab_widget)

        self.button_box = QDialogButtonBox(LogicSettingsWindow)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(LogicSettingsWindow)

        self.main_tab_widget.setCurrentIndex(0)
        self.logic_tab_widget.setCurrentIndex(0)
        self.patches_tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(LogicSettingsWindow)
    # setupUi

    def retranslateUi(self, LogicSettingsWindow):
        LogicSettingsWindow.setWindowTitle(QCoreApplication.translate("LogicSettingsWindow", u"Customize Preset", None))
        self.name_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"Name:", None))
        self.logic_description_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"<html><head/><body><p align=\"justify\">Randovania has rules in place which guarantees that the game is completable regardless of the modifications made to the game. Here you can also configure which kind of game knowledge or skill it expects you to have, allowing for even more varied games.</p><p align=\"justify\">No matter the level, it is always possible to softlock when you enter a room or area that you're unable to leave. For example, vanilla beam rooms without the necessary beam to escape, Dark World without Light Beam/Anihhilator Beam, Torvus Bog without Super Missile.</p><p align=\"justify\">However, it may be <span style=\" font-style:italic;\">necessary</span> to enter Dark World without a way to escape if that item is located in the Dark World.</p></body></html>", None))
        self.trick_level_minimal_logic_check.setText(QCoreApplication.translate("LogicSettingsWindow", u"Use minimal logic instead", None))
        self.trick_level_minimal_logic_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"<html><head/><body><p>Randovania will only check that Screw Attack, Dark Visor and Light Suit won't all be behind Ing Caches and Dark Water, removing the biggest reasons for a pure random layout to be impossible.</p><p>There are no guarantees that a seed will be possible in this case.</p><p><br/></p></body></html>", None))
        self.trick_level_help_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"<html><head/><body><p>If you want to tweak the knowledge or skill needed expected in a game, you can configure the level used for each of the tweaks listed below by moving the slider to the apropriate level.</p><p>Press the ? button to see which rooms use that trick on the selected level.</p></body></html>", None))
        self.logic_tab_widget.setTabText(self.logic_tab_widget.indexOf(self.trick_level_tab), QCoreApplication.translate("LogicSettingsWindow", u"Logic Level", None))
        self.damage_strictness_group.setTitle(QCoreApplication.translate("LogicSettingsWindow", u"Logic damage strictness", None))
        self.damage_strictness_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"<html><head/><body><p>Certain locations, such as rooms without safe zones in Dark Aether or bosses, requires a certain number of energy tanks (or suits).</p><p>This setting controls how much energy the logic will expect you to have to reach these locations.</p></body></html>", None))
        self.damage_strictness_combo.setItemText(0, QCoreApplication.translate("LogicSettingsWindow", u"Strict (1\u00d7)", None))
        self.damage_strictness_combo.setItemText(1, QCoreApplication.translate("LogicSettingsWindow", u"Medium (1.5\u00d7)", None))
        self.damage_strictness_combo.setItemText(2, QCoreApplication.translate("LogicSettingsWindow", u"Lenient (2\u00d7)", None))

        self.damage_strictness_combo.setCurrentText(QCoreApplication.translate("LogicSettingsWindow", u"Strict (1\u00d7)", None))
        self.logic_tab_widget.setTabText(self.logic_tab_widget.indexOf(self.logic_damage_tab), QCoreApplication.translate("LogicSettingsWindow", u"Damage", None))
        self.randomization_mode_group.setTitle(QCoreApplication.translate("LogicSettingsWindow", u"Randomization Mode", None))
        self.randomization_mode_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"<html><head/><body><p>This setting controls how Randovania will shuffle items.</p><p><span style=\" font-weight:600;\">Full:</span> All items can be placed in any location.</p><p><span style=\" font-weight:600;\">Major/minor split:</span> Major items (i.e., major upgrades, Energy Tanks, Dark Temple Keys, and Energy Transfer Modules) and minor items (i.e, expansions) will be shuffled separately. Major items in excess of the number of major locations will be placed in minor locations, and vice versa.</p></body></html>", None))
        self.randomization_mode_combo.setItemText(0, QCoreApplication.translate("LogicSettingsWindow", u"Full", None))
        self.randomization_mode_combo.setItemText(1, QCoreApplication.translate("LogicSettingsWindow", u"Major/minor split", None))

        self.excluded_locations_group.setTitle(QCoreApplication.translate("LogicSettingsWindow", u"Available Locations", None))
        self.excluded_locations_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"<html><head/><body><p>Choose which locations are considered for placing items.</p></body></html>", None))
        self.logic_tab_widget.setTabText(self.logic_tab_widget.indexOf(self.location_pool_tab), QCoreApplication.translate("LogicSettingsWindow", u"Location Pool", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.logic_tab), QCoreApplication.translate("LogicSettingsWindow", u"Randomizer Logic", None))
        self.energy_tank_box.setTitle(QCoreApplication.translate("LogicSettingsWindow", u"Energy tank", None))
        self.dangerous_tank_check.setText(QCoreApplication.translate("LogicSettingsWindow", u"1 HP mode. In this mode, Energy Tanks and Save Stations leave you at 1 HP instead", None))
        self.energy_tank_capacity_description.setText(QCoreApplication.translate("LogicSettingsWindow", u"<html><head/><body><p>Configure how much energy each Energy Tank you collect will provide. Your base energy is always this quantity, minus 1.</p><p>While logic will respect this value, only the original value (100) has been tested.</p></body></html>", None))
        self.energy_tank_capacity_spin_box.setSuffix(QCoreApplication.translate("LogicSettingsWindow", u" energy", None))
        self.energy_tank_capacity_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"Energy per tank", None))
        self.safe_zone_box.setTitle(QCoreApplication.translate("LogicSettingsWindow", u"Safe zone", None))
        self.safe_zone_regen_spin.setSuffix(QCoreApplication.translate("LogicSettingsWindow", u" energy/s", None))
        self.safe_zone_regen_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"Safe Zone healing rate", None))
        self.safe_zone_logic_heal_check.setText(QCoreApplication.translate("LogicSettingsWindow", u"Logic considers fully healing at every safe zone. This is currently always on.", None))
        self.safe_zone_description.setText(QCoreApplication.translate("LogicSettingsWindow", u"<html><head/><body><p>Configure how Dark Aether safe zones operate and how logic uses them.</p></body></html>", None))
        self.dark_aether_box.setTitle(QCoreApplication.translate("LogicSettingsWindow", u"Dark Aether", None))
        self.varia_suit_spin_box.setSuffix(QCoreApplication.translate("LogicSettingsWindow", u" energy/s", None))
        self.varia_suit_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"Varia Suit", None))
        self.dark_suit_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"Dark Suit", None))
        self.dark_suit_spin_box.setSuffix(QCoreApplication.translate("LogicSettingsWindow", u" energy/s", None))
        self.dark_aether_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"<html><head/><body><p>Configure how much damage per second you take in Dark Aether, per suit.<br/>Light Suit is always imune.</p><p>Logic always use the default value for checking, so higher values may cause impossible games.</p></body></html>", None))
        self.patches_tab_widget.setTabText(self.patches_tab_widget.indexOf(self.energy_tab), QCoreApplication.translate("LogicSettingsWindow", u"Energy", None))
        self.elevators_description_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"<html><head/><body><p>Controls where each elevator connects to.</p><p><span style=\" font-weight:600;\">Original Connections</span>: all elevators are connected to where they do in the original game.</p><p><span style=\" font-weight:600;\">Two-way, between areas</span>: after taking an elevator, the elevator in the room you are in will bring you back to where you were. An elevator will never connect to another in the same area.</p><p><span style=\" font-weight:600;\">Two-way, unchecked</span>: after taking an elevator, the elevator in the room you are in will bring you back to where you were. <span style=\" font-style:italic;\">Experimental, can cause incompletable matches.</span></p><p><span style=\" font-weight:600;\">One-way, elevator room</span>: all elevators bring you to another elevator room, but going backwards can go somewhere else. <span style=\" font-style:italic;\">Experimental, can cause incompletable matches.</span></p><p><span style=\" font-weight:600;\">One-way, anywhere</span>: elevators are c"
                        "onnected to any room from the game. <span style=\" font-style:italic;\">Experimental, can cause incompletable matches.</span><br/><span style=\" font-style:italic;\">Warning:</span> there's an audio bug whenever you take an elevator. This bug lasts until you restart the game.</p></body></html>", None))
        self.elevators_combo.setItemText(0, QCoreApplication.translate("LogicSettingsWindow", u"Original Connections", None))
        self.elevators_combo.setItemText(1, QCoreApplication.translate("LogicSettingsWindow", u"Random: Two-way, between areas", None))
        self.elevators_combo.setItemText(2, QCoreApplication.translate("LogicSettingsWindow", u"Random: Two-way, unchecked", None))
        self.elevators_combo.setItemText(3, QCoreApplication.translate("LogicSettingsWindow", u"Random: One-way, elevator room", None))
        self.elevators_combo.setItemText(4, QCoreApplication.translate("LogicSettingsWindow", u"Random: One-way, anywhere", None))

        self.patches_tab_widget.setTabText(self.patches_tab_widget.indexOf(self.elevator_tab), QCoreApplication.translate("LogicSettingsWindow", u"Elevators", None))
        self.startingarea_description.setText(QCoreApplication.translate("LogicSettingsWindow", u"<html><head/><body><p>The area where the game starts at can be customized, being selected randomly from a list.</p><p>For ease of use, you can select some pre-defined list of locations. They are:<br/>Ship: Just Temple Grounds - Landing Site, the vanilla location.<br/>Save Stations: All areas with Save Stations.</p><p><span style=\" font-weight:600;\">WARNING</span>: depending on the starting items that are configured, it may be impossible to start at the chosen place. In that case, the generation will fail.</p></body></html>", None))
        self.starting_area_quick_fill_label.setText(QCoreApplication.translate("LogicSettingsWindow", u"Quick Fill with:", None))
        self.starting_area_quick_fill_ship.setText(QCoreApplication.translate("LogicSettingsWindow", u"Ship (Default)", None))
        self.starting_area_quick_fill_save_station.setText(QCoreApplication.translate("LogicSettingsWindow", u"Save Station", None))
        self.patches_tab_widget.setTabText(self.patches_tab_widget.indexOf(self.starting_area_tab), QCoreApplication.translate("LogicSettingsWindow", u"Starting Area", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.patches_tab), QCoreApplication.translate("LogicSettingsWindow", u"Game Modifications", None))
    # retranslateUi

