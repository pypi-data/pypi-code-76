import argparse
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QCoreApplication, QAbstractListModel
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5 import QtCore

import homcloud.view_index_ui
from homcloud.version import __version__
from homcloud.diagram import PD
from homcloud.argparse_common import add_arguments_for_load_diagrams


class MainWindow(QMainWindow):
    def __init__(self, pictname, pd, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = homcloud.view_index_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionQuit.triggered.connect(self.quit)

        self.pairs_positions = pd.pairs_positions()
        self.indices_model = Indices(self.pairs_positions, self)
        self.ui.listView_Pairs.setModel(self.indices_model)
        self.ui.listView_Pairs.clicked.connect(self.on_click_pair)
        self.selected_pair = None

        self.ui.spinBox_Scale.valueChanged.connect(self.draw_picture)

        self.pict = QPixmap(pictname)
        self.ui.label_Pict.setPixmap(self.pict)

        self.ui.button_Filter.clicked.connect(self.update_filter)
        self.ui.statusbar.showMessage("Red: Birth, Blue: Death")

    @staticmethod
    def quit():
        QCoreApplication.instance().quit()

    def on_click_pair(self, index):
        self.selected_pair = self.indices_model.filtered_pairs[index.row()]
        self.draw_picture()

    def draw_picture(self):
        if self.selected_pair is None:
            return

        pair = self.selected_pair
        pict = QPixmap(self.pict)
        painter = QPainter()
        size = pict.size()
        painter.begin(pict)
        painter.setPen(QtCore.Qt.red)
        painter.drawLine(0, pair.birth_pos[0], size.width(), pair.birth_pos[0])
        painter.drawLine(pair.birth_pos[1], 0, pair.birth_pos[1], size.height())
        painter.setPen(QtCore.Qt.blue)
        painter.drawLine(0, pair.death_pos[0], size.width(), pair.death_pos[0])
        painter.drawLine(pair.death_pos[1], 0, pair.death_pos[1], size.height())
        painter.end()
        scale = self.get_scale()
        self.ui.label_Pict.setPixmap(pict.scaled(size.width() * scale,
                                                 size.height() * scale))

    def get_scale(self):
        return self.ui.spinBox_Scale.value()

    @staticmethod
    def none_or_int(string):
        if string == "":
            return None
        else:
            return int(string)

    def retrieve_filter_params(self):
        try:
            min_birth = self.none_or_int(self.ui.edit_MinBirth.text())
            max_birth = self.none_or_int(self.ui.edit_MaxBirth.text())
            min_death = self.none_or_int(self.ui.edit_MinDeath.text())
            max_death = self.none_or_int(self.ui.edit_MaxDeath.text())
            min_lifetime = self.none_or_int(self.ui.edit_MinLifetime.text())
            max_lifetime = self.none_or_int(self.ui.edit_MaxLifetime.text())
        except ValueError:
            self.error_message("Filter params format error")
            return
        self.indices_model.set_filter_params(
            min_birth, max_birth, min_death, max_death, min_lifetime, max_lifetime
        )

    def update_filter(self):
        self.retrieve_filter_params()


class Indices(QAbstractListModel):
    def __init__(self, pairs_positions_, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.pairs_positions = pairs_positions_
        self.filtered_pairs = pairs_positions_

    def rowCount(self, unused_parent=QtCore.QModelIndex()):
        return len(self.filtered_pairs)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        if index.row() >= len(self.filtered_pairs):
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(
                self.filtered_pairs[index.row()].display_str()
            )

        else:
            return QtCore.QVariant()

    def set_filter_params(self, min_birth, max_birth, min_death, max_death, min_lifetime, max_lifetime):
        self.beginResetModel()
        self.filtered_pairs = self.pairs_positions
        if min_birth is not None:
            self.filtered_pairs = [pair for pair in self.filtered_pairs
                                   if pair.birth >= min_birth]
        if max_birth is not None:
            self.filtered_pairs = [pair for pair in self.filtered_pairs
                                   if pair.birth <= max_birth]
        if min_death is not None:
            self.filtered_pairs = [pair for pair in self.filtered_pairs
                                   if pair.death >= min_death]
        if max_death is not None:
            self.filtered_pairs = [pair for pair in self.filtered_pairs
                                   if pair.death <= max_death]
        if min_lifetime is not None:
            self.filtered_pairs = [pair for pair in self.filtered_pairs
                                   if pair.lifetime >= min_lifetime]
        if max_lifetime is not None:
            self.filtered_pairs = [pair for pair in self.filtered_pairs
                                   if pair.lifetime <= max_lifetime]
        self.endResetModel()


def argument_parser():
    p = argparse.ArgumentParser(description="View indices of PD")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_arguments_for_load_diagrams(p)
    p.add_argument("picture", help="input Picture file name")
    p.add_argument("diagram", help="persistence diagram file name")
    return p


def main():
    app = QApplication(sys.argv)
    args = argument_parser().parse_args(app.arguments()[1:])

    pd = PD.load_diagrams(args.type, [args.diagram], args.degree, args.negate)
    if not pd.filtration_type:
        sys.stderr.write("No index information\n")
        exit(1)

    main_window = MainWindow(args.picture, pd)

    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
