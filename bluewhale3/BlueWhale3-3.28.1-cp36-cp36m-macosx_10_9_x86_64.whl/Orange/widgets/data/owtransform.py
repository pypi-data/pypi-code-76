from typing import Optional

from AnyQt.QtCore import Qt

from Orange.data import Table
from Orange.widgets import gui
from Orange.widgets.report.report import describe_data
from Orange.widgets.utils.sql import check_sql_input
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.utils.state_summary import format_multiple_summaries, \
    format_summary_details
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from Orange.i18n_config import *


def __(key):
    return i18n.t("widget.data.data.owtransform." + key)

class OWTransform(OWWidget):
    name = __("name")
    description = __("desc")
    icon = "icons/Transform.svg"
    priority = 2110
    keywords = ["transform"]

    class Inputs:
        data = Input("Data", Table, default=True, label=i18n.t("widget.data.data.common.data"))
        template_data = Input("Template Data", Table, label=i18n.t("widget.data.data.common.template_data"))

    class Outputs:
        transformed_data = Output("Transformed Data", Table, label=i18n.t("widget.data.data.common.transformed_data"))

    class Error(OWWidget.Error):
        error = Msg(__("msg_transform_error"))

    resizing_enabled = False
    want_main_area = False

    def __init__(self):
        super().__init__()
        self.data = None  # type: Optional[Table]
        self.template_data = None  # type: Optional[Table]
        self.transformed_info = describe_data(None)  # type: OrderedDict

        info_box = gui.widgetBox(self.controlArea, i18n.t("common.software.info"))
        self.input_label = gui.widgetLabel(info_box, "")
        self.template_label = gui.widgetLabel(info_box, "")
        self.output_label = gui.widgetLabel(info_box, "")
        self.set_input_label_text()
        self.set_template_label_text()

        self.info.set_input_summary(self.info.NoInput)
        self.info.set_output_summary(self.info.NoOutput)

    def set_input_label_text(self):
        text = i18n.t("common.software.no_data_on_input")
        if self.data:
            text = __("row_input_instance").format(
                len(self.data),
                len(self.data.domain.attributes))
        self.input_label.setText(text)

    def set_template_label_text(self):
        text = __("text.no_template")
        if self.data and self.template_data:
            text = __("text.template_domain_apply")
        elif self.template_data:
            text = __("row_include_feature").format(
                len(self.template_data.domain.attributes))
        self.template_label.setText(text)

    def set_output_label_text(self, data):
        text = ""
        if data:
            text = __("row_output_instance").format(
                len(data.domain.attributes))
        self.output_label.setText(text)

    @Inputs.data
    @check_sql_input
    def set_data(self, data):
        self.data = data
        self.set_input_label_text()

    @Inputs.template_data
    @check_sql_input
    def set_template_data(self, data):
        self.template_data = data

    def handleNewSignals(self):
        summary, details, kwargs = self.info.NoInput, "", {}
        if self.data or self.template_data:
            n_data = len(self.data) if self.data else 0
            n_template = len(self.template_data) if self.template_data else 0
            summary = f"{self.info.format_number(n_data)}, " \
                      f"{self.info.format_number(n_template)}"
            kwargs = {"format": Qt.RichText}
            details = format_multiple_summaries([
                (__("text.data"), self.data),
                (__("text.template_data"), self.template_data)
            ])
        self.info.set_input_summary(summary, details, **kwargs)
        self.apply()

    def apply(self):
        self.clear_messages()
        transformed_data = None
        if self.data and self.template_data:
            try:
                transformed_data = self.data.transform(self.template_data.domain)
            except Exception as ex:  # pylint: disable=broad-except
                self.Error.error(ex)

        data = transformed_data
        summary = len(data) if data else self.info.NoOutput
        details = format_summary_details(data) if data else ""
        self.info.set_output_summary(summary, details)
        self.transformed_info = describe_data(data)
        self.Outputs.transformed_data.send(data)
        self.set_template_label_text()
        self.set_output_label_text(data)

    def send_report(self):
        if self.data:
            self.report_data(__("report.data"), self.data)
        if self.template_data:
            self.report_domain(__("report.template_data"), self.template_data.domain)
        if self.transformed_info:
            self.report_items(__("report.transformed_data"), self.transformed_info)


if __name__ == "__main__":  # pragma: no cover
    from Orange.preprocess import Discretize

    table = Table("iris")
    WidgetPreview(OWTransform).run(
        set_data=table, set_template_data=Discretize()(table))
