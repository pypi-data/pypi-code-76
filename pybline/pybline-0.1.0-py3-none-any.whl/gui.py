import argparse
import pathlib
import sys

import matplotlib.pyplot as plt

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas

from . import models


class TrimDialog(QtWidgets.QDialog):
    def __init__(self, timeseries, parent=None):
        super().__init__(parent)
        self._ts_orig = timeseries
        self._ts_trim = self._ts_orig

        time_max = timeseries.times[-1]

        layout = QtWidgets.QGridLayout()
        layout.setRowStretch(0, 1)
        layout.setColumnStretch(0, 1)

        self.canvas = TimeseriesCanvas(
            color='C0', parent=self, width=4, height=6, dpi=100)
        self.canvas.plot_timeseries(self._ts_orig)
        layout.addWidget(self.canvas, 0, 0)

        form = QtWidgets.QFormLayout()
        self.controls = {}
        for key, label in [
                ('time_start', 'Time start'),
                ('time_end', 'Time end')]:
            doubleSpinBox = QtWidgets.QDoubleSpinBox()
            doubleSpinBox.setDecimals(2)
            doubleSpinBox.setSingleStep(0.1)
            doubleSpinBox.setSuffix(' sec')
            doubleSpinBox.setRange(0, time_max)
            if key == 'time_end':
                doubleSpinBox.setValue(time_max)
            self.controls[key] = doubleSpinBox
            form.addRow(label, doubleSpinBox)

        doubleSpinBox = QtWidgets.QDoubleSpinBox()
        doubleSpinBox.setRange(0, 1)
        doubleSpinBox.setSuffix(' Hz')
        doubleSpinBox.setDecimals(3)
        doubleSpinBox.setSingleStep(0.01)
        doubleSpinBox.setValue(0.05)
        self.controls['high_pass'] = doubleSpinBox
        form.addRow('High pass', doubleSpinBox)

        spinBox = QtWidgets.QSpinBox()
        spinBox.setRange(0, 30)
        spinBox.setSuffix(' %')
        spinBox.setValue(5)
        self.controls['taper'] = spinBox
        form.addRow('Taper', spinBox)

        layout.addLayout(form, 0, 1)

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Apply
        )
        button_box.accepted.connect(self.accept)
        button_box.button(
            QtWidgets.QDialogButtonBox.Apply
        ).clicked.connect(self.apply)

        layout.addWidget(button_box, 1, 0, 1, 2, QtCore.Qt.AlignRight)

        self.setLayout(layout)
        self.apply()

        self.controls['time_start'].selectAll()

    def apply(self):
        values = {k: c.value() for k, c in self.controls.items()}
        self._ts_trim = self._ts_orig.trim(**values)
        self.canvas.plot_timeseries(self._ts_trim, time_offset=values['time_start'])

    def accept(self):
        self.apply()
        super().accept()

    @property
    def time_series(self):
        return self._ts_trim


class TimeseriesCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, color='C0', parent=None, width=7, height=4, dpi=100):
        self._color = color
        self._fig, self._axes = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self._fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def __del__(self):
        plt.close(self._fig)

    def plot_timeseries(self, ts, correction=None, time_offset=0):
        vels, disps = ts.integrate()
        for values, ax in zip([ts.accels, vels, disps], self._axes):
            ax.clear()
            ax.plot(time_offset + ts.times, values, color=self._color)
            if correction is not None and values is disps:
                ax.plot(correction.times, correction.disps_fit, color='C3')

        # Add labels
        for ax, label in zip(self._axes, ['Accel. (g)', 'Vel. (cm/s)', 'Disp (cm)']):
            ax.set_ylabel(label)
        self._axes[-1].set(xlabel='Time (sec)')
        self._fig.tight_layout()

        self.draw()


class CorrectionWidget(QtWidgets.QWidget):
    def __init__(self, correction, parent=0):
        super().__init__()

        self.correction = correction
        self.controls = {}

        layout = QtWidgets.QFormLayout()

        spinBox = QtWidgets.QSpinBox()
        spinBox.setRange(0, 30)
        spinBox.setSuffix(' %')
        self.controls['padding'] = spinBox
        layout.addRow('Padding', spinBox)

        spinBox = QtWidgets.QSpinBox()
        spinBox.setRange(2, 12)
        self.controls['degree'] = spinBox
        layout.addRow('Degree', spinBox)

        for key, label in [
                ('select_start', 'Select start'),
                ('select_end', 'Select end')]:
            doubleSpinBox = QtWidgets.QDoubleSpinBox()
            doubleSpinBox.setDecimals(2)
            doubleSpinBox.setSingleStep(0.1)
            doubleSpinBox.setSuffix(' sec')
            self.controls[key] = doubleSpinBox
            layout.addRow(label, doubleSpinBox)

        spinBox = QtWidgets.QSpinBox()
        spinBox.setRange(1, 30)
        spinBox.setSuffix(' %')
        self.controls['taper'] = spinBox
        layout.addRow('Taper', spinBox)

        checkBox = QtWidgets.QCheckBox('Force zero displacement')
        self.controls['force_zero_disp'] = checkBox
        layout.addRow(checkBox)

        self.reset()

        self.setLayout(layout)

    def save(self):
        for k, widget in self.controls.items():
            if isinstance(widget, QtWidgets.QCheckBox):
                value = widget.isChecked()
            else:
                value = widget.value()

            setattr(self.correction, k, value)

    def set_select_limits(self, time_max):
        for key in ['select_start', 'select_end']:
            self.controls[key].setRange(0, time_max)

    def reset(self):
        defaults = [
            ('padding', 10),
            ('degree', 5),
            ('select_start', 0.0),
            ('select_end', 0.0),
            ('taper', 5),
            ('force_zero_disp', True),
        ]
        for key, value in defaults:
            widget = self.controls[key]
            if isinstance(widget, QtWidgets.QCheckBox):
                widget.setChecked(value)
            else:
                widget.setValue(value)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self._time_max = 0
        self._ts_orig = None
        self._ts_mod = None
        self._fpath = None
        self._corrections = []

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Save', self.file_save, self.tr('Ctrl+S'))
        self.file_menu.addAction('&Open', self.file_open, self.tr('Ctrl+O'))
        self.file_menu.addAction('&Quit', self.file_quit, self.tr('Ctrl+Q'))
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        layout = QtWidgets.QGridLayout()
        layout.setRowStretch(0, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        self.canvas_orig = self._create_canvas('C0')
        layout.addWidget(self.canvas_orig, 0, 0, 2, 1)

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self._create_canvas('C1'), 'Step 0')
        layout.addWidget(self.tab_widget, 0, 1, 2, 1)

        self.toolbox = QtWidgets.QToolBox()
        layout.addWidget(self.toolbox, 0, 2)

        layout_buttons = QtWidgets.QHBoxLayout()

        for name, func in [
                ('Add step', self._add_correction),
                ('Remove step', self._remove_correction),
                ('Reset', self._reset),
                ('Apply', self._apply),
        ]:
            button = QtWidgets.QPushButton(name)
            button.clicked.connect(func)
            layout_buttons.addWidget(button)

        layout.addLayout(layout_buttons, 1, 2)

        self._add_correction()

        self.main_widget.setLayout(layout)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def _create_canvas(self, color):
        canvas = TimeseriesCanvas(
            color=color, parent=self.main_widget, width=4, height=6, dpi=100)
        return canvas

    def open_motion(self, fpath):
        self._fpath = pathlib.Path(fpath)

        ts = models.TimeSeries.read(self._fpath)

        dialog = TrimDialog(ts)
        dialog.exec_()

        self._ts_orig = dialog.time_series

        self.canvas_orig.plot_timeseries(self._ts_orig)
        self.time_max = self._ts_orig.times[-1]
        self._apply()
        self.statusBar().showMessage(self._fpath.name)

    def _add_correction(self):
        i = 1 + self.toolbox.count()
        name = f'Step {i}'
        self.toolbox.addItem(
            CorrectionWidget(models.BaselineCorrection()), name)
        self.tab_widget.addTab(self._create_canvas('C1'), name)

        self.toolbox.setCurrentIndex(self.toolbox.count() - 1)
        self._apply()

    def _remove_correction(self):
        i = self.toolbox.count()

        if i < 2:
            return

        self.toolbox.removeItem(i - 1)
        self.toolbox.setCurrentIndex(i - 2)

        plt.close(self.tab_widget.widget(i)._fig)

        self.tab_widget.removeTab(i)
        self.tab_widget.setCurrentIndex(i - 1)

    def _reset(self):
        while self.tab_widget.count() > 2:
            self.tab_widget.removeTab(2)
        while self.toolbox.count() > 1:
            self.toolbox.removeItem(1)

        for i in range(self.toolbox.count()):
            self.toolbox.widget(i).reset()

        self._apply()

    def _apply(self):
        if self._ts_orig is None:
            return

        for i in range(self.toolbox.count()):
            cw = self.toolbox.widget(i)
            cw.save()

            if i == 0:
                ts_in = self._ts_orig
            else:
                ts_in = self.toolbox.widget(i - 1).correction.time_series
            ts_out = cw.correction(ts_in)
            self.tab_widget.widget(i).plot_timeseries(
                ts_in, cw.correction)
            self.tab_widget.widget(i + 1).plot_timeseries(ts_out)

    @property
    def time_max(self):
        return self._time_max

    @time_max.setter
    def time_max(self, value):
        self._time_max = value

        for i in range(self.toolbox.count()):
            self.toolbox.widget(i).set_select_limits(self._time_max)

    def _save(self):
        cw = self.toolbox.widget(self.toolbox.count() - 1)
        ts_mod = cw.correction.time_series
        if ts_mod:
            fpath = self._fpath.with_name(
                self._fpath.stem + '-pb.acc')

            with fpath.open('wt') as fp:
                ts_mod.write(fp, ncols=1)

    def file_quit(self):
        self.close()

    def file_save(self):
        self._apply()
        self._save()

    def file_open(self):
        if self._fpath:
            dirPath = str(self._fpath.parent)
        else:
            dirPath = QtCore.QStandardPaths.displayName(
                QtCore.QStandardPaths.HomeLocation)

        fileName = QtWidgets.QFileDialog.getOpenFileName(
            self, self.tr("Open File"), dirPath,
            self.tr("RSPMatch Time Series (*.acc)")
        )[0]
        if fileName:
            self.open_motion(fileName)

    def closeEvent(self, ce):
        self.file_quit()

    def about(self):
        # FIXME
        QtWidgets.QMessageBox.about(
            self,
            "About",
            "An about..."
        )


def main():
    parser = argparse.ArgumentParser(
        description='Post process RSPMatch output')
    parser.add_argument('fpath', type=str, nargs='?',
                        help='File of time series.')

    args = parser.parse_args()

    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    if args.fpath:
        aw.open_motion(args.fpath)
    # FIXME: Dynamic?
    aw.setWindowTitle('pybline')
    aw.show()

    return qApp.exec_()


if __name__ == '__main__':
    main()
