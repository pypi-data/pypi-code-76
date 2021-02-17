"""GUI window for qalx-orcaflex batch overview"""

import os
import re
import sys
import traceback
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import (
    Qt,
    QObject,
    pyqtSignal,
    QRunnable,
    pyqtSlot,
    QThreadPool,
    QTimer,
)
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (
    QMessageBox,
    QWidget,
    QApplication,
    QStyleFactory,
    QFileDialog,
)
from tabulate import tabulate

from qalx_orcaflex.gui.batch.core import BatchOverview, date_format, pretty_time
from qalx_orcaflex.gui.batch.models.table import (
    TableModel,
    MultiFilterProxyModel,
    MultiFilterMode,
)
from qalx_orcaflex.gui.batch.overview_main_ui import Ui_MainWindow
from qalx_orcaflex.gui.batch.requeue_jobs_dialog import ReQueueDialog


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything
    """

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class BackgroundWorker(QRunnable):
    """
    Background worker thread.

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback:    The function callback to run on this worker thread.
                        Supplied args and kwargs will be passed through to the
                        runner.
    :type callback:     function
    :param args:        Arguments to pass to the callback function
    :param kwargs:      Keywords to pass to the callback function
    """

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as exc:
            traceback.print_exc()
            exc_type = sys.exc_info()[0]
            self.signals.error.emit((exc_type, exc, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class BatchOverviewMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    help_message = (
        "<strong>Qalx Orcaflex Batch Overview</strong>"
        + "<p>For further help visit the documentation page:</p>"
        + '<a href="https://orcaflex.qalx.net/quickstart.html">'
        + "https://orcaflex.qalx.net/quickstart.html</a>"
        + "<p>\N{COPYRIGHT SIGN} 2020, AgileTek Engineering Limited</p>"
    )

    def __init__(self, session, batch_name, batches):
        super().__init__()
        self.setupUi(self)
        self.home_dir = str(Path.home())
        self.batch_overview = BatchOverview(session, batch_name, batches)
        self.timer = QTimer(self)
        self.getUpdatesButton.clicked.connect(self.run_summary)
        self.helpButton.clicked.connect(self.print_help)
        self.downloadDatButton.clicked.connect(self.save_dat)
        self.downloadSimButton.clicked.connect(self.save_sim)
        self.requeueJobsButton.clicked.connect(self.requeue_jobs)
        self.autoUpdateCombo.currentIndexChanged.connect(self._update_interval_combo)
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        self.update_intervals = [
            (np.iinfo(int).max, "Off"),  # Just set to maximum possible val
            (15000, "15 sec"),
            (30000, "30 sec"),
            (120000, "2 min"),
        ]  # (sec, text) tuples
        self.thread_pool = QThreadPool()
        self.worker = None
        self.timer.timeout.connect(self.run_summary)
        self.interval = self.update_intervals[0][0]
        self.timer.start(self.interval)
        self.model = TableModel(pd.DataFrame(columns=BatchOverview.df_columns))
        self.proxy = MultiFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.detailsTable.setModel(self.proxy)
        # Allow sorting
        self.detailsTable.setSortingEnabled(True)
        # Set up the filtering
        self.filterRegexText.textChanged.connect(self.on_regexEdit_textChanged)
        self.filterColumnCombo.currentIndexChanged.connect(
            self.on_filterColCombo_currentIndexChanged
        )
        self.andOrFilterCombo.currentIndexChanged.connect(
            self.on_andOrFilterCombo_currentIndexChanged
        )
        self.stateFilterCombo.currentTextChanged.connect(
            self.on_stateFilterCombo_currentTextChanged
        )
        self.detailsTable.selectionModel().selectionChanged.connect(
            self.update_selected_jobs
        )
        self.hidable_widgets = [
            self.getUpdatesButton,
            self.revCombo,
            self.autoUpdateCombo,
            self.downloadDatButton,
            self.downloadSimButton,
            self.requeueJobsButton,
        ]
        self._initialise_ui()

    @QtCore.pyqtSlot(str)
    def on_regexEdit_textChanged(self, text):
        """Set the regex according to which the selected column is filtered"""
        if not text:
            self.proxy.regex = None
            self.filterPatternLabel.setToolTip("")
        else:
            try:
                self.proxy.regex = re.compile(text)
            except re.error as exc:
                self.proxy.regex = None
                self.filterPatternLabel.setToolTip(str(exc))
            else:
                self.filterPatternLabel.setToolTip("Regex OK")
        self.proxy.invalidateFilter()

    @QtCore.pyqtSlot(int)
    def on_filterColCombo_currentIndexChanged(self, index):
        """Set the column according to which the regex filter is happening"""
        self.proxy.column = index
        self.proxy.invalidateFilter()

    @QtCore.pyqtSlot(int)
    def on_andOrFilterCombo_currentIndexChanged(self, index):
        """Set the column according to which the regex filter is happening"""
        if index == 0:
            self.proxy.multi_filter_mode = MultiFilterMode.AND
        else:
            self.proxy.multi_filter_mode = MultiFilterMode.OR
        self.proxy.invalidateFilter()

    @QtCore.pyqtSlot(str)
    def on_stateFilterCombo_currentTextChanged(self, text):
        """Set the state according to which we filter"""
        if text == "All":
            self.proxy.state = None
        else:
            self.proxy.state = text
        self.proxy.invalidateFilter()

    @QtCore.pyqtSlot(object)
    def update_stateFilterCombo(self, result):
        self.stateFilterCombo.clear()
        self.stateFilterCombo.addItems(["All"] + [i for i in result])
        self.stateFilterCombo.setCurrentIndex(0)

    def update_selected_jobs(self, selected, deselected):
        """
        Update the selected jobs on the current batch. This method should be
        invoked once a selection changed signal is received from the table view
        """
        self.model.selected_jobs.update((_.row() for _ in selected.indexes()))
        for _ in deselected.indexes():
            self.model.selected_jobs.discard(_.row())

    def _initialise_ui(self):
        """Custom modifications to the UI that need to happen during init"""
        self.setWindowTitle(f"{self.windowTitle()} - {self.batch_overview.batch_name}")
        # Set table column width to always stretch
        header = self.detailsTable.horizontalHeader()
        for _ in range(len(BatchOverview.df_columns) - 1):
            header.setSectionResizeMode(_, QtWidgets.QHeaderView.Stretch)
        # Add the batch and revision details in the widgets
        self.update_rev_combo_box(self.batch_overview.batches)
        self.update_auto_refresh_combo_box()
        self.update_filter_combos()
        self.label_3.setText(self.batch_overview.batch_name)
        self.setup_icon()

    def update_filter_combos(self):
        self.filterColumnCombo.clear()
        self.filterColumnCombo.addItems([i for i in TableModel.header_labels])
        self.filterColumnCombo.setCurrentIndex(0)
        self.andOrFilterCombo.clear()
        self.andOrFilterCombo.addItems(["AND", "OR"])
        self.andOrFilterCombo.setCurrentIndex(0)

    def _update_interval_combo(self):
        """Run this when the combo-box for the auto-update value is updated"""
        self.timer.stop()
        self.interval = self.update_intervals[self.autoUpdateCombo.currentIndex()][0]
        self.timer.start(self.interval)

    def setup_icon(self):
        """
        Setup the app icon. Custom modification to make sure the icon is
        correctly shown in the taskbar in windows:
        https://stackoverflow.com/a/1552105
        """
        icon_path = (
            Path(__file__).parents[1].joinpath("icons", "qalx_32x32_favicon.png")
        )
        self.setWindowIcon(QtGui.QIcon(str(icon_path)))
        if sys.platform.startswith("win"):
            import ctypes

            myapp_id = "agiletek.qalx.qalx-orcaflex"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myapp_id)

    def deactivate_buttons_cursor_waits(self):
        """Deactivate the two action buttons and show the cursor as busy"""
        QApplication.setOverrideCursor(Qt.BusyCursor)
        for _ in self.hidable_widgets:
            _.setEnabled(False)

    def restore_after_update(self):
        """Reactivate all buttons and restore the cursor"""
        QApplication.restoreOverrideCursor()
        for _ in self.hidable_widgets:
            _.setEnabled(True)
        self.timer.start(self.interval)

    def run_worker(
        self,
        worker_function,
        worker_args,
        worker_kwargs,
        results_slots,
        finished_slots,
        error_slots,
    ):
        """
        Helper to run the background worker with a custom function arguments and
        keyword arguments
        """
        self.deactivate_buttons_cursor_waits()
        self.timer.stop()
        self.worker = BackgroundWorker(worker_function, *worker_args, **worker_kwargs)
        for results_slot in results_slots:
            self.worker.signals.result.connect(results_slot)
        for finished_slot in finished_slots:
            self.worker.signals.finished.connect(finished_slot)
        for error_slot in error_slots:
            self.worker.signals.error.connect(error_slot)
        self.thread_pool.start(self.worker)

    def render_text_summary(self, df, batch_index, table_data):
        """Helper to render text for the plain text widget"""
        result = [f"Batch: {self.batch_overview.batch_name} - rev: {batch_index}"]
        line_len = len(result[0])
        result.append(f"\nLast update: {date_format(datetime.now())}")
        result.insert(0, "#" * line_len + "\n")
        headers = ["State", "Count"]
        table = tabulate(table_data, headers, tablefmt="psql")
        result.append(f"\n{table}\n")
        result.append('"Running dynamics" cases summary\n')
        remaining = df[df.state == "Running dynamics"].remaining.to_numpy()
        r_max, r_mean, q1, q3 = self.batch_overview.get_summary_stats(remaining)
        table_data = [
            ["Count", remaining.size],
            ["Maximum time remaining", pretty_time(r_max)],
            ["Average time remaining", pretty_time(r_mean)],
            ["Q1", pretty_time(q1)],
            ["Q3", pretty_time(q3)],
        ]
        table = tabulate(table_data, tablefmt="psql")
        result.append(table)
        result.append("\n" + "#" * line_len + "\n" * 2)
        return "".join(result)

    def check_complete_label(self, complete_array):
        """
        Small helper to modify the complete flag label according to the
        completion boolean array for all jobs
        """
        if complete_array.size > 0 and complete_array.all():
            self.completeLabel.setText("Batch Complete!")
            self.autoUpdateCombo.setCurrentIndex(0)  # We do not need to auto-update
        else:
            self.completeLabel.setText("")

    def render_summary(self, result):
        """Action for the refresh button"""
        # Pure text
        df, batch_index = result
        table_data = []
        for state, count in df.state.value_counts().items():
            table_data.append([state, count])
        possible_states = self.batch_overview.possible_states
        table_data.sort(key=lambda x: possible_states.index(x[0]))
        text_summary = self.render_text_summary(df, batch_index, table_data)
        self.jobSummaryText.moveCursor(QTextCursor.End)
        self.jobSummaryText.insertPlainText(text_summary)
        # State filter combo box
        self.update_stateFilterCombo([_[0] for _ in table_data])
        self.check_complete_label(df.complete.to_numpy())

    def run_summary(self):
        """
        Runs the summary extraction process in a thread and then updates the
        widgets or throws an error according to the signal from the worker
        """
        self.run_worker(
            self.batch_overview.get_summary_df,
            (self.revCombo.currentIndex(),),
            {},
            (self.render_summary, self.model.update_df),
            (self.restore_after_update,),
            (self.throw_error_message_box,),
        )

    def throw_error_message_box(self, exc_tuple):
        """Throw an error message box"""
        _, exc, __ = exc_tuple
        w = QWidget(parent=self)
        message = f"There was an error: \n\n{exc}"
        QMessageBox.critical(w, "Error", message)

    def update_rev_combo_box(self, batches):
        """
        Updates the combo box with the different revisions of the target batch
        """
        self.revCombo.clear()
        self.revCombo.addItems(
            [f"{i} - {date_format(b.created_on)}" for i, b in enumerate(batches)]
        )
        self.revCombo.setCurrentIndex(self.revCombo.count() - 1)

    def update_auto_refresh_combo_box(self):
        """Updates the combo box with the options for automatic refresh"""
        self.autoUpdateCombo.clear()
        self.autoUpdateCombo.addItems([i for _, i in self.update_intervals])
        self.autoUpdateCombo.setCurrentIndex(0)

    def check_jobs_selected(self):
        """
        Check for selected jobs. If none are selected a message box is
        displayed. Returns True/False accordingly
        """
        if not self.model.selected_jobs:
            w = QWidget(parent=self)
            QMessageBox.critical(w, "Error", "No jobs are selected")
            return False
        return True

    def save_files(self, file_type):
        """
        Save files of the provided file type for the selected jobs. First checks
        that there are in fact selected jobs. In the case of sim files, at least
        one of the selected jobs must be complete and only sim files of complete
        jobs are downloaded
        """
        if not self.check_jobs_selected():
            return
        selected_jobs = self.model.selected_jobs
        selected_jobs = np.fromiter(selected_jobs, int, len(selected_jobs))
        df = self.model._data
        if file_type == "sim":
            should_download = df.complete.iloc[selected_jobs].to_numpy()
            if np.all(np.logical_not(should_download)):
                w = QWidget(parent=self)
                QMessageBox.critical(
                    w, "Error", "None of the selected jobs is complete"
                )
                return
            jobs_to_download = df.case.iloc[selected_jobs[should_download]]
            save_prompt = "Save .sim file"
            save_file_type = "OFX simulation files (*.sim)"
            save_dir_prompt = "Select .sim file save directory"
        else:
            jobs_to_download = df.case.iloc[selected_jobs]
            save_prompt = "Save .dat file"
            save_file_type = "OFX model files (*.dat)"
            save_dir_prompt = "Select .dat file save directory"
        # Case that only one job is selected. Flexibility allowed to rename file
        if selected_jobs.size == 1:
            default_name = df.case.iloc[selected_jobs[0]]
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                save_prompt,
                os.path.join(self.home_dir, f"{default_name}.{file_type}"),
                save_file_type,
            )
            if not file_name:
                return
            save_path = None
            self.home_dir = os.path.dirname(file_name)
        else:
            save_path = QFileDialog.getExistingDirectory(
                self, save_dir_prompt, self.home_dir
            )
            if not save_path:
                return
            file_name = None
            self.home_dir = save_path
        self.run_worker(
            self.batch_overview.download_files,
            (
                self.revCombo.currentIndex(),
                file_type,
                jobs_to_download,
                file_name,
                save_path,
            ),
            {},
            [],
            (self.restore_after_update,),
            (self.throw_error_message_box,),
        )

    def save_sim(self):
        """Save the simulation .sim file for the selected jobs"""
        self.save_files(file_type="sim")

    def save_dat(self):
        """Save the model .dat file for the selected jobs"""
        self.save_files(file_type="dat")

    def requeue_jobs(self):
        """Put selected jobs back on a specified queue"""
        if not self.check_jobs_selected():
            return
        selected_jobs = self.model.selected_jobs
        selected_jobs = np.fromiter(selected_jobs, int, len(selected_jobs))
        df = self.model._data
        unique_states = set(df.state[selected_jobs])
        batch = self.batch_overview.batches[self.revCombo.currentIndex()]
        existing_queue = self.batch_overview.get_existing_sim_queue(batch.guid)
        warn_states = unique_states.intersection(BatchOverview.warn_for_requeue)
        requeue_dialog = ReQueueDialog(self, existing_queue, warn_states)
        if requeue_dialog.should_requeue is False:
            return
        self.run_worker(
            self.batch_overview.requeue_jobs,
            (
                self.revCombo.currentIndex(),
                df.case.iloc[selected_jobs],
                requeue_dialog.queue_name,
            ),
            {},
            [],
            (self.restore_after_update,),
            (self.throw_error_message_box,),
        )

    def print_help(self):
        """Action to get help from the help button"""
        w = QWidget(parent=self)
        QMessageBox.information(w, "Help", self.help_message)


def run_gui(ofx_session, batch_name):
    """
    Main function to use for running a new instance of the batch overview
    window. Needs a qalx session and the batch name to instantiate
    """
    batches = BatchOverview.get_batches(ofx_session, batch_name)
    app = QtWidgets.QApplication(sys.argv)
    window = BatchOverviewMainWindow(ofx_session, batch_name, batches)
    window.activateWindow()
    window.show()
    app.exec_()
