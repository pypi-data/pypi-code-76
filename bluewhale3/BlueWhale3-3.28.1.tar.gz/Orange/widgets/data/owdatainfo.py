from collections import OrderedDict
import threading
import textwrap

from Orange.widgets import widget, gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.utils.state_summary import format_summary_details
from Orange.widgets.widget import Input
from Orange.data.table import Table
from Orange.data import StringVariable, DiscreteVariable, ContinuousVariable
from Orange.widgets import report
from Orange.i18n_config import *

try:
    from Orange.data.sql.table import SqlTable
except ImportError:
    SqlTable = None


def __(key):
    return i18n.t("widget.data.data.owdatainfo." + key)


class OWDataInfo(widget.OWWidget):
    name = __("name")
    id = "orange.widgets.data.info"
    description = __("desc")
    icon = "icons/DataInfo.svg"
    priority = 80
    category = "Data"
    keywords = ["information", "inspect"]

    class Inputs:
        data = Input("Data", Table, label=i18n.t("widget.data.data.common.data"))

    want_main_area = False
    resizing_enabled = False

    def __init__(self):
        super().__init__()

        self._clear_fields()

        for box in (
                ("data_set_name", __("box.set_name")), ("data_set_size", __("box.set_size")), ("features", i18n.t("common.general.features")),
                ("targets", __("box.target")),
                ("meta_attributes", __("box.meta_attr")), ("location", __("box.location")),
                ("data_attributes", __("box.data_attr"))):
            name = box[0]
            bo = gui.vBox(self.controlArea, box[1],
                          addSpace=False and box[0] != "meta_attributes")
            gui.label(bo, self, "%%(%s)s" % name)

        self.info.set_input_summary(self.info.NoInput)

        # ensure the widget has some decent minimum width.
        self.targets = "Categorical outcome with 123 values"
        self.layout().activate()
        # NOTE: The minimum width is set on the 'contained' widget and
        # not `self`. The layout will set a fixed size to `self` taking
        # into account the minimum constraints of the children (it would
        # override any minimum/fixed size set on `self`).
        self.targets = ""
        self.controlArea.setMinimumWidth(self.controlArea.sizeHint().width())

    @Inputs.data
    def data(self, data):
        if data is None:
            self._clear_fields()
            self.info.set_input_summary(self.info.NoInput)
        else:
            self._set_fields(data)
            self._set_report(data)
            self.info.set_input_summary(data.approx_len(),
                                        format_summary_details(data))

    def _clear_fields(self):
        self.data_set_name = ""
        self.data_set_size = ""
        self.features = self.targets = self.meta_attributes = ""
        self.location = ""
        self.data_desc = None
        self.data_attributes = ""

    @staticmethod
    def _count(s, tpe):
        return sum(isinstance(x, tpe) for x in s)

    def _set_fields(self, data):
        # Attributes are defined in a function called from __init__
        # pylint: disable=attribute-defined-outside-init
        def n_or_none(n):
            return n or "-"

        def pack_table(info):
            return '<table>\n' + "\n".join(
                '<tr><td align="right" width="90">{}:</td>\n'
                '<td width="40">{}</td></tr>\n'.format(
                    d,
                    textwrap.shorten(str(v), width=30, placeholder="..."))
                for d, v in info
            ) + "</table>\n"

        def pack_counts(s, include_non_primitive=False):
            if not s:
                return i18n.t("common.software.none")
            return pack_table(
                (name, n_or_none(self._count(s, type_)))
                for name, type_ in (
                                       (__("row.categorical"), DiscreteVariable),
                                       (__("row.numeric"), ContinuousVariable),
                                       (i18n.t("common.software.text"), StringVariable))[:2 + include_non_primitive]
            )

        domain = data.domain
        class_var = domain.class_var

        sparseness = [s for s, m in (("features", data.X_density),
                                     ("meta attributes", data.metas_density),
                                     ("targets", data.Y_density)) if m() > 1]
        if sparseness:
            sparseness = __("row.sparseness") \
                .format(", ".join(sparseness))
        else:
            sparseness = ""
        self.data_set_size = pack_table((
            (i18n.t("common.general.row"), '~{}'.format(data.approx_len())),
            (i18n.t("common.general.column"), len(domain) + len(domain.metas)))) + sparseness

        def update_size():
            self.data_set_size = pack_table((
                (i18n.t("common.general.row"), len(data)),
                (i18n.t("common.general.column"), len(domain) + len(domain.metas)))) + sparseness

        threading.Thread(target=update_size).start()

        self.data_set_name = getattr(data, "name", "N/A")

        self.features = pack_counts(domain.attributes)
        self.meta_attributes = pack_counts(domain.metas, True)
        if class_var:
            if class_var.is_continuous:
                self.targets = __("row.num_var")
            else:
                self.targets = __("row.categorical_value") \
                    .format(len(class_var.values))
        elif domain.class_vars:
            disc_class = self._count(domain.class_vars, DiscreteVariable)
            cont_class = self._count(domain.class_vars, ContinuousVariable)
            if not cont_class:
                self.targets = __("row.categorical_targets") \
                    .format(n_or_none(disc_class))
            elif not disc_class:
                self.targets = __("row.numeric_targets") \
                    .format(n_or_none(cont_class))
            else:
                self.targets = __("row.targets") + \
                               pack_counts(domain.class_vars)
        else:
            self.targets = i18n.t("common.software.none")

        if data.attributes:
            self.data_attributes = pack_table(data.attributes.items())
        else:
            self.data_attributes = ""

    def _set_report(self, data):
        # Attributes are defined in a function called from __init__
        # pylint: disable=attribute-defined-outside-init
        domain = data.domain
        count = self._count

        self.data_desc = dd = OrderedDict()
        dd["Name"] = self.data_set_name

        if SqlTable is not None and isinstance(data, SqlTable):
            connection_string = ' '.join(
                '{}={}'.format(key, value)
                for key, value in data.connection_params.items()
                if value is not None and key != 'password')
            self.location = __("row.location") \
                .format(data.table_name, connection_string)
            dd["Rows"] = data.approx_len()
        else:
            self.location = __("row.data_stored")
            dd["Rows"] = len(data)

        def join_if(items):
            return ", ".join(s.format(n) for s, n in items if n)

        dd["Features"] = len(domain.attributes) > 0 and join_if((
            (__("row.categorical_num"), count(domain.attributes, DiscreteVariable)),
            (__("row.numeric_num"), count(domain.attributes, ContinuousVariable))
        ))
        if domain.class_var:
            name = domain.class_var.name
            if domain.class_var.is_discrete:
                dd["Target"] = __("row.categorical_outcome").format(name)
            else:
                dd["Target"] = __("row.numeric_target").format(name)
        elif domain.class_vars:
            disc_class = count(domain.class_vars, DiscreteVariable)
            cont_class = count(domain.class_vars, ContinuousVariable)
            tt = ""
            if disc_class:
                tt += report.plural(__("report.categorical_outcome"), disc_class)
            if cont_class:
                tt += report.plural(__("report.numeric_target"), cont_class)
        dd["Meta attributes"] = len(domain.metas) > 0 and join_if((
            (__("report.categorical"), count(domain.metas, DiscreteVariable)),
            (__("report.numeric"), count(domain.metas, ContinuousVariable)),
            (__("report.text"), count(domain.metas, StringVariable))
        ))

    def send_report(self):
        if self.data_desc:
            self.report_items(self.data_desc)


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWDataInfo).run(Table("iris"))
