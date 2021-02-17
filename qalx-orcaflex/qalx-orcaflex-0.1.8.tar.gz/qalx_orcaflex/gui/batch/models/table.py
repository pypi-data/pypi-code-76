import re

import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSortFilterProxyModel

from qalx_orcaflex.gui.batch.core import pretty_time, BatchOverview


class TableModel(QtCore.QAbstractTableModel):
    """Custom table model. Uses a dataframe to hold and manipulate the data"""

    header_labels = ["Job", "State", "Est. Rem. Time", "Last Checked On"]
    rem_time_ind = 2
    complete_col_ind = 4

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.selected_jobs = set()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role=None):
        row, col = index.row(), index.column()
        # Values
        if role == Qt.DisplayRole:
            value = self._data.iloc[row, col]
            if col == 2:
                value = pretty_time(value)
            return str(value)
        # Background color
        if role == Qt.BackgroundRole:
            complete = bool(self._data.iloc[row, self.complete_col_ind])
            if complete is True:
                return QtGui.QColor(169, 245, 182)  # green pastel-ish
        # Alignment
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1] - 1

    @QtCore.pyqtSlot(object)
    def update_df(self, result):
        """Update the underlying data from the provided result"""
        df, _ = result
        self.layoutAboutToBeChanged.emit()
        self._data = df
        self.layoutChanged.emit()


class MultiFilterMode:
    AND = 0
    OR = 1


class MultiFilterProxyModel(QSortFilterProxyModel):
    """
    Filter on the states column as well as any additional column with a regex
    """

    possible_states_arr = np.asarray(BatchOverview.possible_states)
    sorted_states = np.argsort(possible_states_arr)
    sort_job_regex = re.compile(r"^\[(\d+)].+")

    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filters = {}
        self.multi_filter_mode = None
        self.regex = None
        self.column = None

    @classmethod
    def sort_job_names(cls, job_name_series):
        """
        Custom sorter for job names. They are expected to come in the form:
        "[<num>] <Job_name>" where <num> is an integer which is extracted from a
        regex and sorted on. If <num> cannot be extracted, such jobs are sorted
        last and according to the full job name
        """
        regex = job_name_series.str.extract(cls.sort_job_regex, expand=False).to_numpy(
            dtype=np.float64
        )
        nans = np.isnan(regex)
        indices = np.zeros(shape=regex.size, dtype=np.int64)
        indices[~nans] = np.argsort(np.argsort(regex[~nans]))
        indices[nans] = (
            np.argsort(np.argsort(job_name_series.array[nans])) + regex[~nans].size
        )
        return indices

    @classmethod
    def sort_states(cls, x):
        """
        Custom sorter for states according to the order they appear in the
        relevant enum
        """
        return cls.sorted_states[
            np.searchsorted(cls.possible_states_arr[cls.sorted_states], x)
        ]

    def filterAcceptsRow(self, p_int, q_model_index):
        """
        Custom filter implementation. AND/OR logic between regex filtering of a
        column and the selected states
        """
        # Check for edge case first
        if (self.regex is None) and (self.state is None):
            return True
        # Check for the regex
        if self.regex is None:
            regex_match = True
        else:
            index = self.sourceModel().index(p_int, self.column, q_model_index)
            text = self.sourceModel().data(index, Qt.DisplayRole)
            regex_match = self.regex.match(text) is not None
        # Check for state
        if self.state is None:
            state_match = True
        else:
            # State is column 1
            index = self.sourceModel().index(p_int, 1, q_model_index)
            text = self.sourceModel().data(index, Qt.DisplayRole)
            state_match = self.state == text
        if self.multi_filter_mode == MultiFilterMode.AND:
            return regex_match and state_match
        return regex_match or state_match

    def sort(self, p_int, order=None):
        """
        Implement the sort method because the state and the remaining time are
        special cases. State should be sorted according to the order states
        appear in the JobState enum, while for the remaining time, the
        underlying data is needed and not the pretty-time string
        """
        df = self.sourceModel()._data
        if p_int == 0:  # Job is the first column
            key = self.sort_job_names
        elif p_int == 1:  # State is the second column
            key = self.sort_states
        else:
            key = None
        self.sourceModel().layoutAboutToBeChanged.emit()
        df.sort_values(
            df.columns[p_int],
            ascending=order == QtCore.Qt.AscendingOrder,
            inplace=True,
            key=key,
        )
        df.reset_index(inplace=True, drop=True)
        self.sourceModel().layoutChanged.emit()
