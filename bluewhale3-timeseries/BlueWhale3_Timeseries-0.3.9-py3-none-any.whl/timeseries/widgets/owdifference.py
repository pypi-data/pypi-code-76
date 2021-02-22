from enum import Enum

import numpy as np

from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QListView, QButtonGroup, QRadioButton

from Orange.data import Table, Domain, ContinuousVariable
from Orange.widgets import widget, gui, settings
from Orange.widgets.settings import DomainContextHandler, ContextSetting
from Orange.widgets.utils.itemmodels import VariableListModel, select_rows, \
    signal_blocking
from Orange.widgets.widget import Input, Output

from orangecontrib.timeseries import Timeseries
from orangecontrib.timeseries.widgets.utils import available_name
from orangecontrib.timeseries.i18n_config import *


def __(key):
    return i18n.t("timeseries.owdifference." + key)


class OWDifference(widget.OWWidget):
    name = __('name')
    description = __('desc')
    icon = 'icons/Difference.svg'
    priority = 570
    keywords = ['difference', 'derivative', 'quotient', 'percent change']

    class Inputs:
        time_series = Input('Time Series', Table, label=i18n.t("timeseries.common.time_series"))

    class Outputs:
        time_series = Output('Time Series', Timeseries, label=i18n.t("timeseries.common.time_series"))

    settingsHandler = DomainContextHandler()
    selected = ContextSetting([], schema_only=True)

    class Operation(str, Enum):
        DIFF = __('gbox.difference')
        QUOT = __('gbox.quotient')
        PERC = __('gbox.percentage_change')

    want_main_area = False
    resizing_enabled = False

    chosen_operation = settings.Setting(Operation.DIFF)
    diff_order = settings.Setting(1)
    shift_period = settings.Setting(1)
    invert_direction = settings.Setting(False)
    autocommit = settings.Setting(True)

    UserAdviceMessages = [
        widget.Message(__('msg_series_order'),
                       'diff-shift')
    ]

    def __init__(self):
        self.data = None

        box = gui.vBox(self.controlArea, __('box_difference'))

        gui.comboBox(box, self, 'chosen_operation',
                     orientation=Qt.Horizontal,
                     items=[el.value for el in self.Operation],
                     label=__('label.compute'),
                     callback=self.on_changed,
                     sendSelectedValue=True)

        self.order_spin = gui.spin(
            box, self, 'diff_order', 1, 2,
            label=__('label.difference_order'),
            callback=self.on_changed,
            tooltip=__('label.difference_order_tip'))
        gui.spin(box, self, 'shift_period', 1, 100,
                 label=__('label.shift'),
                 callback=self.on_changed,
                 tooltip=__('label.shift_tip'))
        gui.checkBox(box, self, 'invert_direction',
                     label=__('checkbox_invert_direction'),
                     callback=self.on_changed,
                     tooltip=__('checkbox_invert_difference_direction_tip'))
        self.view = view = QListView(self,
                                     selectionMode=QListView.ExtendedSelection)
        self.model = model = VariableListModel(parent=self)
        view.setModel(model)
        view.selectionModel().selectionChanged.connect(self.on_changed)
        box.layout().addWidget(view)
        gui.auto_commit(box, self, 'autocommit', i18n.t('timeseries.common_btn.apply'))

    @Inputs.time_series
    def set_data(self, data):
        self.closeContext()
        self.data = data = None if data is None else \
                           Timeseries.from_data_table(data)
        if data is not None:
            self.model[:] = [var for var in data.domain.variables
                             if var.is_continuous and var is not
                             data.time_variable]
            self.select_default_variable()
            self.openContext(self.data)
            self._restore_selection()
        else:
            self.reset_model()
        self.on_changed()

    def _restore_selection(self):
        def restore(view, selection):
            with signal_blocking(view.selectionModel()):
                # gymnastics for transforming variable names back to indices
                var_list = [var for var in self.data.domain.variables
                            if var.is_continuous and var is not
                            self.data.time_variable]
                indices = [var_list.index(i) for i in selection]
                select_rows(view, indices)

        restore(self.view, self.selected)

    def select_default_variable(self):
        self.selected = [0]
        select_rows(self.view, self.selected)

    def reset_model(self):
        self.model.wrap([])

    def on_changed(self):
        var_names = [i.row()
                     for i in self.view.selectionModel().selectedRows()]
        self.order_spin.setEnabled(
            self.shift_period == 1
            and self.chosen_operation == self.Operation.DIFF)
        self.selected = [self.model[v] for v in var_names]
        self.commit()

    def commit(self):
        data = self.data
        if not data or not len(self.selected):
            self.Outputs.time_series.send(None)
            return

        X = []
        attrs = []
        invert = self.invert_direction
        shift = self.shift_period
        order = self.diff_order
        op = self.chosen_operation

        for var in self.selected:
            col = np.ravel(data[:, var])

            if invert:
                col = col[::-1]

            out = np.empty(len(col))
            if op == self.Operation.DIFF and shift == 1:
                out[order:] = np.diff(col, order)
                out[:order] = np.nan
            else:
                if op == self.Operation.DIFF:
                    out[shift:] = col[shift:] - col[:-shift]
                else:
                    out[shift:] = np.divide(col[shift:], col[:-shift])
                    if op == self.Operation.PERC:
                        out = (out - 1) * 100
                out[:shift] = np.nan

            if invert:
                out = out[::-1]

            X.append(out)

            if op == self.Operation.DIFF and shift == 1:
                details = f'order={order}'
            else:
                details = f'shift={shift}'

            template = f'{var} ({op[:4].lower()}; {details})'
            name = available_name(data.domain, template)
            attrs.append(ContinuousVariable(name))

        ts = Timeseries.from_numpy(Domain(data.domain.attributes + tuple(attrs),
                                          data.domain.class_vars,
                                          data.domain.metas),
                                   np.column_stack((data.X, np.column_stack(X))),
                                   data.Y, data.metas)
        ts.time_variable = data.time_variable
        self.Outputs.time_series.send(ts)


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication

    a = QApplication([])
    ow = OWDifference()

    data = Timeseries.from_file('airpassengers')
    # Make Adjusted Close a class variable
    attrs = [var.name for var in data.domain.attributes]
    if 'Adj Close' in attrs:
        attrs.remove('Adj Close')
        data = Timeseries.from_table(Domain(attrs,
                                            [data.domain['Adj Close']],
                                            None,
                                            source=data.domain),
                                     data)

    ow.set_data(data)

    ow.show()
    a.exec()
