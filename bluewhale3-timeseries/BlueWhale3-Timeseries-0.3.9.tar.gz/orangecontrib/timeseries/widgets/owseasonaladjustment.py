from AnyQt.QtWidgets import QListView
from AnyQt.QtCore import Qt

from Orange.data import Table, Domain
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.itemmodels import VariableListModel
from Orange.widgets.widget import Input, Output, Msg
from numpy import hstack

from orangecontrib.timeseries import Timeseries, seasonal_decompose
from orangecontrib.timeseries.i18n_config import *


def __(key):
    return i18n.t("timeseries.owseasonaladjustment." + key)


MAX_PERIODS = 1000


class OWSeasonalAdjustment(widget.OWWidget):
    name = __('name')
    description = __('desc')
    icon = 'icons/SeasonalAdjustment.svg'
    priority = 5500

    class Inputs:
        time_series = Input('Time Series', Table, label=i18n.t("timeseries.common.time_series"))

    class Outputs:
        time_series = Output('Time Series', Timeseries, label=i18n.t("timeseries.common.time_series"))

    want_main_area = False
    resizing_enabled = False

    n_periods = settings.Setting(12)
    decomposition = settings.Setting(0)
    selected = settings.Setting([])
    autocommit = settings.Setting(False)

    UserAdviceMessages = [
        widget.Message(__('msg.usage_method'),
                       'decomposition-model'),
        widget.Message(__('msg.season_period'),
                       'season-period'),
    ]

    DECOMPOSITION_MODELS = (__('btn.additive'), __('btn.multiplicative'))

    class Error(widget.OWWidget.Error):
        seasonal_decompose_fail = Msg("{}")
        not_enough_instances = Msg(__("msg.not_enough_instances"))

    def __init__(self):
        self.data = None
        box = gui.vBox(self.controlArea, __("box_seasonal_adjustment"))
        gui.spin(box, self, 'n_periods', 2, MAX_PERIODS,
                 label=__('row_season_period'),
                 callback=self.on_changed,
                 tooltip=__('row_season_period_tip'))
        gui.radioButtons(box, self, 'decomposition', self.DECOMPOSITION_MODELS,
                         label=__('btn.decomposition_model'),
                         orientation=Qt.Horizontal,
                         callback=self.on_changed)
        self.view = view = QListView(self,
                                     selectionMode=QListView.ExtendedSelection)
        self.model = model = VariableListModel(parent=self)
        view.setModel(model)
        view.selectionModel().selectionChanged.connect(self.on_changed)
        box.layout().addWidget(view)
        gui.auto_commit(box, self, 'autocommit', __('btn.apply'))

    @Inputs.time_series
    def set_data(self, data):
        self.Error.not_enough_instances.clear()
        self.data = None
        self.model.clear()
        data = None if data is None else Timeseries.from_data_table(data)
        if data is None:
            pass
        elif len(data) > 2:
            self.data = data
            self.model.wrap([var for var in data.domain.variables
                             if var.is_continuous and var is not data.time_variable])
            self.controls.n_periods.setMaximum(min(MAX_PERIODS, len(data) - 1))
        else:
            self.Error.not_enough_instances()
        self.on_changed()

    def on_changed(self):
        self.selected = [self.model[i.row()].name
                         for i in self.view.selectionModel().selectedIndexes()]
        self.commit()

    def commit(self):
        self.Error.seasonal_decompose_fail.clear()
        data = self.data
        if not data or not self.selected:
            self.Outputs.time_series.send(data)
            return

        selected_subset = Timeseries.from_table(Domain(self.selected,
                                                       source=data.domain), data)
        # FIXME: might not pass selected interpolation method

        with self.progressBar(len(self.selected)) as progress:
            try:
                adjusted_data = seasonal_decompose(
                    selected_subset,
                    self.DECOMPOSITION_MODELS[self.decomposition],
                    self.n_periods,
                    callback=lambda *_: progress.advance())
            except ValueError as ex:
                self.Error.seasonal_decompose_fail(str(ex))
                adjusted_data = None

        if adjusted_data is not None:
            new_domain = Domain(data.domain.attributes +
                                adjusted_data.domain.attributes,
                                data.domain.class_vars,
                                data.domain.metas)
            ts = Timeseries.from_numpy(new_domain, X=hstack((data.X,
                                                             adjusted_data.X)),
                                       Y=data.Y,
                                       metas=data.metas)
            ts.time_variable = data.time_variable
        else:
            ts = None
        self.Outputs.time_series.send(ts)


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication

    a = QApplication([])
    ow = OWSeasonalAdjustment()

    data = Timeseries.from_file('airpassengers')
    if not data.domain.class_var and 'Adj Close' in data.domain:
        # Make Adjusted Close a class variable
        attrs = [var.name for var in data.domain.attributes]
        attrs.remove('Adj Close')
        data = Timeseries.from_table(Domain(attrs, [data.domain['Adj Close']], None,
                                            source=data.domain),
                                     data)

    ow.set_data(data)

    ow.show()
    a.exec()
