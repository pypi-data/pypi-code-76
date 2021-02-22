import numpy as np
from AnyQt.QtCore import QSize
from sklearn.preprocessing import scale

from Orange.data import ContinuousVariable, Domain, Table
from Orange.statistics.util import nanmax, nanmean, nanmedian
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Output, Input
from Orange.widgets.utils.sql import check_sql_input
from Orange.widgets.widget import OWWidget, Msg

from orangecontrib.bioinformatics.widgets.utils.data import (
    GENE_ID_ATTRIBUTE, GENE_ID_COLUMN, GENE_AS_ATTRIBUTE_NAME, TAX_ID
)
from orangecontrib.single_cell.i18n_config import *


def __(key):
    return i18n.t('single_cell.owscorecells.' + key)


def percent_nonzero(x, axis=1):
    return np.ravel(np.mean(x > 0, axis=axis))


def mean_normalized(x, axis=1):
    return np.mean(scale(x, with_mean=False), axis=axis)


class OWScoreCells(widget.OWWidget):
    name = __('name')
    description = __('desc')
    icon = "icons/ScoreCells.svg"
    priority = 320

    auto_apply = Setting(True)
    aggregation = Setting(__('gbox.mean_expression'))
    score_variable_name = Setting(__('gbox.score'), schema_only=True)
    want_main_area = False

    class Warning(OWWidget.Warning):
        no_genes = Msg(__('msg.no_genes'))
        some_genes = Msg(__('msg.some_genes'))

    class Error(OWWidget.Error):
        organism_mismatch = Msg(
            __('msg.organism_mismatch'))

        # for input data
        missing_annotation_input = Msg(__('msg.missing_annotation_input'))
        missing_gene_id_input = Msg(__('msg.missing_gene_id_input'))
        missin_organism_input = Msg(__('msg.missin_organism_input'))

        # for marker data
        missing_annotation_marker = Msg(__('msg.missing_annotation_marker'))
        missing_gene_id_marker = Msg(__('msg.missing_gene_id_marker'))
        missin_organism_marker = Msg(__('msg.missin_organism_marker'))

    class Inputs:
        data = Input('Data', Table, label=i18n.t("single_cell.common.data"))
        genes = Input("Genes", Table, label=i18n.t("single_cell.common.genes"))

    class Outputs:
        data = Output('Data', Table, label=i18n.t("single_cell.common.data"))

    aggregation_functions = {
        __('gbox.mean_expression'): nanmean,
        __('gbox.mean_normalized'): mean_normalized,
        __('gbox.nanmedian'): nanmedian,
        __('gbox.nanmax'): nanmax,
        __('gbox.percent_nonzero'): percent_nonzero,
    }

    def __init__(self):
        super().__init__()

        # Input data attributes
        self.input_data = None
        self.input_genes = None
        self.tax_id = None
        self.use_attr_names = None
        self.gene_id_attribute = None
        self.gene_id_column = None

        # Marker data attributes
        self.marker_data = None
        self.marker_genes = None
        self.marker_tax_id = None
        self.marker_use_attr_names = None
        self.marker_gene_id_attribute = None
        self.marker_gene_id_column = None

        info_box = gui.vBox(self.controlArea, __('box.input_info'))
        self.info_text = gui.widgetLabel(info_box)

        box = gui.vBox(self.controlArea, __("box.aggregation"))
        gui.comboBox(box, self, 'aggregation', sendSelectedValue=True,
                     items=list(self.aggregation_functions.keys()),
                     callback=lambda: self.commit())

        box = gui.vBox(self.controlArea, __('box.column_name_output'))
        self.line_edit = gui.lineEdit(box, self, 'score_variable_name',
                                      callback=lambda: self.commit())
        self.line_edit.setPlaceholderText(__('placeholder_column_name'))

        self.apply_button = gui.auto_commit(
            self.controlArea, self, "auto_apply", __("btn_apply"), box=False)

        self.sizeHint()

    def sizeHint(self):
        return QSize(320, 240)

    def handleNewSignals(self):
        self.update_info_box()
        self.commit()

    def __check_organism_mismatch(self):
        """ Check if organisms from different inputs match.

        :return: True if there is a mismatch
        """
        if self.tax_id and self.marker_tax_id:
            return self.tax_id != self.marker_tax_id
        return False

    def __clear_widget_state(self):
        self.Warning.clear()
        self.Error.clear()

    @Inputs.data
    @check_sql_input
    def set_data(self, data):
        self.__clear_widget_state()
        self.input_genes = None
        self.input_data = data

        if self.input_data:
            self.tax_id = str(self.input_data.attributes.get(TAX_ID, None))
            self.use_attr_names = self.input_data.attributes.get(GENE_AS_ATTRIBUTE_NAME, None)
            self.gene_id_attribute = self.input_data.attributes.get(GENE_ID_ATTRIBUTE, None)
            self.gene_id_column = self.input_data.attributes.get(GENE_ID_COLUMN, None)

            if not (self.use_attr_names is not None
                    and ((self.gene_id_attribute is None) ^ (self.gene_id_column is None))):

                if self.tax_id is None:
                    self.Error.missing_annotation_input()
                    return

                self.Error.missing_gene_id_input()
                return

            elif self.tax_id is None:
                self.Error.missin_organism_input()
                return

            if self.__check_organism_mismatch():
                self.Error.organism_mismatch()
                return

            self.__get_input_genes()

    @Inputs.genes
    @check_sql_input
    def set_genes(self, data):
        self.__clear_widget_state()
        self.marker_genes = None
        self.marker_data = data

        if self.marker_data:
            self.marker_tax_id = str(self.marker_data.attributes.get(TAX_ID, None))
            self.marker_use_attr_names = self.marker_data.attributes.get(GENE_AS_ATTRIBUTE_NAME, None)
            self.marker_gene_id_attribute = self.marker_data.attributes.get(GENE_ID_ATTRIBUTE, None)
            self.marker_gene_id_column = self.marker_data.attributes.get(GENE_ID_COLUMN, None)

            if not (self.marker_use_attr_names is not None
                    and ((self.marker_gene_id_attribute is None) ^ (self.marker_gene_id_column is None))):

                if self.marker_tax_id is None:
                    self.Error.missing_annotation_marker()
                    return

                self.Error.missing_gene_id_marker()
                return

            elif self.marker_tax_id is None:
                self.Error.missin_organism_marker()
                return

            if self.__check_organism_mismatch():
                self.Error.organism_mismatch()
                return

            self.__get_marker_genes()

    def __score_cells(self):
        scores = np.ones(len(self.input_data))

        if self.marker_data and self.marker_genes and \
                self.input_data and self.input_genes:

            matched_ids = [gene_id for gene_id in self.input_genes if gene_id in self.marker_genes]
            matched_columns = [column for column in self.input_data.domain.attributes
                               if self.gene_id_attribute in column.attributes and
                               str(column.attributes[self.gene_id_attribute]) in matched_ids]

            self.Warning.no_genes.clear()
            self.Warning.some_genes.clear()

            if not matched_ids:
                self.Warning.no_genes()
            else:
                self.update_info_box(matched_genes=matched_ids)
                if len(matched_ids) < len(self.marker_genes):
                    self.Warning.some_genes(len(self.marker_genes) - len(matched_ids),
                                            len(self.marker_genes))

                values = self.input_data[:, matched_columns].X
                aggregator = self.aggregation_functions[self.aggregation]
                scores = aggregator(values, axis=1)

        return scores

    def __get_input_genes(self):
        self.input_genes = []

        if self.use_attr_names:
            for variable in self.input_data.domain.attributes:
                self.input_genes.append(str(variable.attributes.get(self.gene_id_attribute, '?')))
        else:
            genes, _ = self.input_data.get_column_view(self.gene_id_column)
            self.input_genes = [str(g) for g in genes]

        self.input_genes = set(filter(None, self.input_genes))

    def __get_marker_genes(self):
        self.marker_genes = []

        if self.marker_use_attr_names:
            for variable in self.marker_data.domain.attributes:
                self.marker_genes.append(str(variable.attributes.get(self.marker_gene_id_attribute, '?')))
        else:
            genes, _ = self.marker_data.get_column_view(self.marker_gene_id_column)
            self.marker_genes = [str(g) for g in genes]

        self.marker_genes = set(filter(None, self.marker_genes))

    def commit(self):
        table = None

        if self.input_data:
            score = self.__score_cells()

            score_var = ContinuousVariable(self.score_variable_name)
            domain = Domain(self.input_data.domain.attributes,
                            self.input_data.domain.class_vars,
                            self.input_data.domain.metas + (score_var,))

            table = self.input_data.transform(domain)
            col, sparse = table.get_column_view(score_var)
            col[:] = score

        self.Outputs.data.send(table)

    def send_report(self):
        gene = None
        if self.marker_data is not None:
            gene = self.gene
            if gene in self.marker_data.domain:
                gene = self.marker_data.domain[gene]
        self.report_items((
            (__("report_gene"), gene),
        ))

    def update_info_box(self, matched_genes=None):
        info_string = ''
        if self.input_data and self.input_genes:
            info_string += __('info.data').format(len(self.input_data), len(self.input_genes))

        if self.marker_genes:
            info_string += __('info.markers').format(len(self.marker_genes))

        if not info_string:
            info_string = __('info.missing_data')

        if matched_genes:
            info_string += __('info.gene_matching').format(len(matched_genes))

        self.info_text.setText(info_string)


if __name__ == "__main__":
    def test():
        from AnyQt.QtWidgets import QApplication
        app = QApplication([])

        w = OWScoreCells()
        data = Table("iris")
        w.set_data(data)
        w.handleNewSignals()
        w.show()
        app.exec_()


    test()
