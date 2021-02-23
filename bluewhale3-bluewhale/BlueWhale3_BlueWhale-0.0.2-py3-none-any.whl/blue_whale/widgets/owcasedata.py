import re
import logging
import sqlite3
from itertools import chain
from warnings import catch_warnings
from typing import List

import numpy as np
from AnyQt.QtWidgets import \
    QComboBox, QGridLayout, QLabel, QPushButton, QButtonGroup, QSizePolicy as Policy, QSizePolicy, \
    QAbstractItemView
from AnyQt.QtCore import Qt, QTimer, QSize, QStringListModel
from AnyQt.QtGui import QBrush
from orangewidget.utils.listview import ListViewSearch
from orangecontrib.blue_whale.widgets.utils import get_sample_datasets_dir, SqliteTabel, Server
from orangecontrib.blue_whale.i18n_config import *

from Orange.data.table import Table
from Orange.data.io import FileFormat, class_from_qualified_name
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting, ContextSetting, PerfectDomainContextHandler, SettingProvider
from Orange.widgets.utils.domaineditor import DomainEditor
from Orange.widgets.utils.filedialogs import RecentPathsWComboMixin

from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.utils.state_summary import format_summary_details
from Orange.widgets.widget import Output, Msg
from collections import OrderedDict

# Backward compatibility: class RecentPath used to be defined in this module,
# and it is used in saved (pickled) settings. It must be imported into the
# module's namespace so that old saved settings still work
from Orange.widgets.utils.filedialogs import RecentPath

log = logging.getLogger(__name__)


def __(key):
    return i18n.t("bluewhale.owcasedata." + key)


def add_origin(examples, filename):
    """
    Adds attribute with file location to each string variable
    Used for relative filenames stored in string variables (e.g. pictures)
    TODO: we should consider a cleaner solution (special variable type, ...)
    """
    if not filename:
        return
    strings = [var
               for var in examples.domain.variables + examples.domain.metas
               if var.is_string]
    dir_name, _ = os.path.split(filename)
    for var in strings:
        if "type" in var.attributes and "origin" not in var.attributes:
            var.attributes["origin"] = dir_name


class OWCaseData(widget.OWWidget, RecentPathsWComboMixin):
    name = __("name")
    description = __("desc")
    icon = "icons/data.svg"
    priority = 30
    category = "Data"
    keywords = ["file", "load", "read", "open"]
    autocommit = Setting(True)

    class Outputs:
        data = Output("Data", Table, label=i18n.t("bluewhale.common.data"),
                      doc=__("desc_text.output_doc"))

    want_main_area = False

    SEARCH_PATHS = [("sample-datasets", get_sample_datasets_dir())]

    SIZE_LIMIT = 1e7
    LOCAL_FILE = 0

    settingsHandler = PerfectDomainContextHandler(
        match_values=PerfectDomainContextHandler.MATCH_VALUES_ALL
    )

    # pylint seems to want declarations separated from definitions
    recent_paths: List[RecentPath]
    category_dict: OrderedDict
    variables: list

    # Overload RecentPathsWidgetMixin.recent_paths to set defaults
    recent_paths = Setting([])
    source = Setting(LOCAL_FILE)
    sheet_names = Setting({})
    table_news = Setting(())
    user_power = Setting({})
    category_dict = Setting({})

    variables = ContextSetting([])

    domain_editor = SettingProvider(DomainEditor)

    class Warning(widget.OWWidget.Warning):
        file_too_big = Msg(__("msg.file_too_big"))
        load_warning = Msg(__("msg.load_warning"))
        performance_warning = Msg(__("msg.performance_warning"))
        renamed_vars = Msg(__("msg.renamed_vars"))

    class Error(widget.OWWidget.Error):
        file_not_found = Msg(__("msg.file_not_found"))
        missing_reader = Msg(__("msg.missing_reader"))
        sheet_error = Msg(__("msg.sheet_error"))
        unknown = Msg(__("msg.unknown"))

    class NoFileSelected:
        pass

    def __init__(self):
        super().__init__()
        data = Server().open('userinfo')
        if not data:
            return

        self.user_id = data['userId']
        RecentPathsWComboMixin.__init__(self)
        self.reader = None
        self.data = None
        self.domain = None
        self.loaded_file = ""
        self.recent_paths = []

        self.box = gui.hBox(self.controlArea, addToLayout=True)
        self.box_1 = gui.hBox(self.box)
        self.box_1.setSizePolicy(Policy.Expanding, Policy.Fixed)

        self.filter_buttons = QButtonGroup(exclusive=False)
        self.filter_buttons.setExclusive(True)
        self.filter_buttons.buttonClicked.connect(self.category_list)

        btn = QPushButton(__("btn.all_info"), enabled=True, autoDefault=False)
        btn.setCheckable(True)
        btn.setChecked(True)
        btn.setSizePolicy(Policy.Expanding, Policy.Fixed)
        self.filter_buttons.addButton(btn, id=0)
        self.box_1.layout().addWidget(btn)

        self.delete_no_exist()
        self.get_activate_id()
        self.button_group()
        gui.button(self.box, self, __("btn.more"), callback=self.update_table_name)

        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        self.listModel = QStringListModel(self.controlArea)
        self.set_list_model()

        self.group_view = gui.listView(
            self.controlArea, self,
            model=self.listModel,
            sizeHint=QSize(150, 100),
            viewType=ListViewSearch,
            sizePolicy=(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        )
        self.group_view.clicked.connect(self.check_item)
        self.group_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        displaybox = gui.widgetBox(self.controlArea, __("title.datasets"))
        displaybox.setMaximumWidth(200)
        displaybox.layout().addWidget(self.group_view)
        layout.addWidget(displaybox, 1, 0)

        box = gui.vBox(self.controlArea, __("title.table"), addToLayout=False)
        box.setMaximumWidth(400)
        box.setSizePolicy(Policy.Maximum, Policy.Expanding)
        self.file_combo.activated[int].connect(self.select_file)
        box.layout().addWidget(self.file_combo)

        self.sheet_box = gui.vBox(box, addToLayout=False, margin=0)
        self.sheet_combo = QComboBox()
        self.sheet_combo.activated[str].connect(self.select_sheet)
        self.sheet_label = QLabel()
        self.sheet_label.setText('Sheet')
        self.sheet_label.setAutoFillBackground(False)
        self.sheet_box.layout().addWidget(self.sheet_label, Qt.AlignTop)
        self.sheet_box.layout().addWidget(self.sheet_combo, Qt.AlignTop)
        self.sheet_box.hide()

        box_2 = gui.vBox(box, __("title.info"), addToLayout=False, margin=0)
        box_2.setMinimumWidth(200)
        box_2.setSizePolicy(Policy.MinimumExpanding, Policy.MinimumExpanding)

        self.infolabel = gui.widgetLabel(box_2, label=__("tip.no_load"))
        self.infolabel.setWordWrap(True)
        self.infolabel.setAlignment(Qt.AlignTop)
        box.layout().addWidget(box_2)
        layout.addWidget(box, 1, 1)

        box_3 = gui.widgetBox(self.controlArea, __("title.columns"))
        self.domain_editor = DomainEditor(self)
        self.editor_model = self.domain_editor.model()
        box_3.setSizePolicy(Policy.Expanding, Policy.MinimumExpanding)
        box_3.layout().addWidget(self.domain_editor)
        layout.addWidget(box_3, 1, 2)

        box = gui.hBox(self.controlArea, margin=5)

        gui.button(box, self, __("btn.reset"), callback=self.reset_domain_edit)
        self.apply_button = gui.button(box, self, __("btn.apply"), callback=self.apply_domain_edit)
        self.apply_button.setEnabled(False)
        self.editor_model.dataChanged.connect(
            lambda: self.apply_button.setEnabled(True))

        self.info.set_output_summary(self.info.NoOutput)
        self.set_file_list()

        self.setAcceptDrops(True)

        if self.source == self.LOCAL_FILE:
            last_path = self.last_path()
            if last_path and os.path.exists(last_path) and \
                    os.path.getsize(last_path) > self.SIZE_LIMIT:
                self.Warning.file_too_big()
                return

        QTimer.singleShot(0, self.load_data)

    @staticmethod
    def sizeHint():
        return QSize(600, 550)

    def button_group(self):
        btn_all_name = [btn.text() for btn in self.filter_buttons.buttons()]
        for idx, btn_name, in enumerate(self.category_dict):
            if btn_name in btn_all_name:
                continue

            btn = QPushButton(btn_name, enabled=True, autoDefault=False)
            btn.setCheckable(True)
            btn.setSizePolicy(Policy.Expanding, Policy.Fixed)
            self.filter_buttons.addButton(btn)
            self.box_1.layout().addWidget(btn)

    def category_list(self, a):
        if not Server().req.cookies.get('SESSION'):
            return

        self.get_activate_id()
        category_id = a.text()
        if self.category_dict.get(category_id):
            path = os.path.join(get_sample_datasets_dir(), '..', 'user')
            if not path:
                return FileNotFoundError
            conn = sqlite3.connect(path)
            sql = """SELECT DISTINCT d.resource_id FROM `resource_download` d INNER JOIN `resource_category` c on d.resource_id = c.resource_id WHERE c.category_id in (?) and d.user_id=?;"""
            c = conn.cursor()
            c.execute(sql, self.category_dict[category_id] + (self.user_id,))
            category_list = c.fetchall()
            conn.close()
            self.set_list_model(category_list)
        else:
            self.set_list_model()

        self.get_all_id()
        self.button_group()
        # self.category_list(self.filter_buttons.checkedButton())

        self.recent_paths.clear()
        self.load_data()

    def set_list_model(self, category=None):
        if category:
            self.recent_paths_data = [(os.path.join(get_sample_datasets_dir(), name[0] + '.bw'), name[0]) for
                                      name in
                                      category]
            self.listModel.setStringList([self.user_power.get(name) for name in category])
        else:
            self.recent_paths_data = [(os.path.join(get_sample_datasets_dir(), name[0] + '.bw'), name[0]) for
                                      name in
                                      self.user_power.keys()]
            self.listModel.setStringList([name for name in self.user_power.values()])

    def get_all_id(self):
        conn = SqliteTabel()
        conn.select_sql_query(['resource_id'], 'resource_download', ['user_id=?'])
        self.info_list = conn.execute_sql_query((self.user_id,))
        conn.connection.close()
        if not self.info_list:
            self.user_power = {}
            self.category_dict = OrderedDict()
            self.resource_dict = {}
        else:
            self.user_power, self.category_dict, self.resource_dict = Server(
                params={"resourceIds": [i[0] for i in self.info_list]}).post_remote()

    def get_activate_id(self):
        self.get_all_id()
        from orangecontrib.blue_whale.widgets.utils.local_file import save_record
        save_record(self.resource_dict)
        delete_record = set(self.info_list) - set(self.user_power)
        if delete_record:
            conn = SqliteTabel()
            conn.delete_sql_query('resource_download', ['user_id=?', 'resource_id=?'])
            conn.execute_query(self.user_id, delete_record)  # 剩下有权限的数据
            conn.connection.close()

    def delete_no_exist(self):
        self.get_all_id()
        local_name_list = []
        for root, dirs, files in os.walk(get_sample_datasets_dir()):
            rule = re.compile(r'(.*)\.bw')
            local_name_list.extend([(rule.findall(name)[0],) for name in files if name.endswith('.bw')])

        conn = SqliteTabel()
        useless = set(self.info_list) - set(local_name_list)
        if useless:
            for id in useless:
                conn.delete_sql_query('resource_download', ['resource_id=?'])
                conn.execute_sql_query(id)
        conn.connection.close()

    def check_item(self, index):
        self.table_name = index.data()
        data = self.recent_paths_data[index.row()]
        if not os.path.exists(data[0]):
            self.data = None
            self.sheet_box.hide()
            self.Outputs.data.send(None)
            self.infolabel.setText(__("tip.no_data"))
            self.info.set_output_summary(self.info.NoOutput)
            from PyQt5.QtWidgets import QMessageBox
            msg_box = QMessageBox(QMessageBox.Warning, __("msg.warn"), __("msg.warn_text"))
            msg_box.exec_()
            self.delete_no_exist()
            return None

        con = sqlite3.connect(data[0])
        c = con.cursor()
        c.execute('''SELECT Alias, Table_name from bwds_meta WHERE Type = 'TAB';''')
        self.table_news = c.fetchall()
        con.close()
        self.recent_paths.clear()
        self.recent_paths.extend(
            [RecentPath(abspath='', prefix='sample-datasets', relpath=data[0], title=name[0], table_name=name[1],
                        resource_id=data[1]) for name in self.table_news])
        self._relocate_recent_files()
        self.load_data()

    def set_file_list(self):
        """
        Sets the items in the file list combo
        """
        self._check_init()
        self.file_combo.clear()

        if not self.recent_paths:
            self.file_combo.addItem(__("none"))
            self.file_combo.model().item(0).setEnabled(False)
        else:
            for i, recent in enumerate(self.recent_paths):
                self.file_combo.addItem(recent.title)
                self.file_combo.model().item(i).setToolTip(recent.abspath)
                if not os.path.exists(recent.abspath):
                    self.file_combo.setItemData(i, QBrush(Qt.red), Qt.TextColorRole)

    def update_table_name(self):
        if not Server().req.cookies.get('SESSION'):
            return

        from orangecontrib.blue_whale.widgets.owcase import OWCase
        window = OWCase(data_type='DATA')
        window.exec_()
        self.get_all_id()
        self.button_group()
        self.category_list(self.filter_buttons.checkedButton())

    def select_file(self, n):
        assert n < len(self.recent_paths)
        recent = self.recent_paths[n]
        del self.recent_paths[n]
        self.recent_paths.insert(0, recent)
        self.set_file_list()
        if self.recent_paths:
            self.source = self.LOCAL_FILE
            self.load_data()
            self.set_file_list()

    def select_sheet(self):
        self.recent_paths[0].sheet = self.sheet_combo.currentText()
        self.load_data()

    # Open a file, create data from it and send it over the data channel
    def load_data(self):
        self.closeContext()
        self.domain_editor.set_domain(None)
        self.apply_button.setEnabled(False)
        self.clear_messages()
        self.set_file_list()

        error = self._try_load()
        if error:
            error()
            self.data = None
            self.sheet_box.hide()
            self.Outputs.data.send(None)
            self.infolabel.setText(__("tip.no_data"))
            self.info.set_output_summary(self.info.NoOutput)

    def _try_load(self):
        # pylint: disable=broad-except
        if self.last_path() and not os.path.exists(self.last_path()):
            return self.Error.file_not_found

        try:
            self.reader = self._get_reader()
            assert self.reader is not None
        except Exception:
            return self.Error.missing_reader

        if self.reader is self.NoFileSelected:
            self.Outputs.data.send(None)
            self.infolabel.setText(__("tip.no_data"))
            self.info.set_output_summary(self.info.NoOutput)
            return None

        try:
            self._update_sheet_combo()
        except Exception:
            return self.Error.sheet_error

        name = self.recent_paths[0].table_name
        with catch_warnings(record=True) as warnings:
            try:
                data = self.reader.read(name=name)
                data.name = self.recent_paths[0].title
            except Exception as ex:
                log.exception(ex)
                return lambda x=ex: self.Error.unknown(str(x))
            if warnings:
                self.Warning.load_warning(warnings[-1].message.args[0])

        self.infolabel.setText(self._describe(data))

        self.loaded_file = self.last_path()
        add_origin(data, self.loaded_file)
        self.data = data
        self.openContext(data.domain)
        self.apply_domain_edit()  # sends data
        return None

    def _get_reader(self) -> FileFormat:
        if self.source == self.LOCAL_FILE:
            path = self.last_path()
            if path is None:
                return self.NoFileSelected
            if self.recent_paths and self.recent_paths[0].file_format:
                qname = self.recent_paths[0].file_format
                reader_class = class_from_qualified_name(qname)
                reader = reader_class(path)
            else:
                reader = FileFormat.get_reader(path)
            if self.recent_paths and self.recent_paths[0].sheet:
                reader.select_sheet(self.recent_paths[0].sheet)

            return reader

    def _update_sheet_combo(self):
        if len(self.reader.sheets) < 2:
            self.sheet_box.hide()
            self.reader.select_sheet(None)
            return

        self.sheet_combo.clear()
        self.sheet_combo.addItems(self.reader.sheets)
        self._select_active_sheet()
        self.sheet_box.show()

    def _select_active_sheet(self):
        if self.reader.sheet:
            try:
                idx = self.reader.sheets.index(self.reader.sheet)
                self.sheet_combo.setCurrentIndex(idx)
            except ValueError:
                # Requested sheet does not exist in this file
                self.reader.select_sheet(None)
        else:
            self.sheet_combo.setCurrentIndex(0)

    @staticmethod
    def _describe(table):
        def missing_prop(prop):
            if prop:
                return __("number_miss_value").format(prop * 100)
            else:
                return __("no_missing_value")

        domain = table.domain
        text = ""

        attrs = getattr(table, "attributes", {})
        descs = [attrs[desc]
                 for desc in ("Name", "Description") if desc in attrs]
        if len(descs) == 2:
            descs[0] = f"<b>{descs[0]}<br/></b>"
        if descs:
            text += f"<p>{'<br/>'.join(descs)}</p>"

        text += __("desc_text.number_instance").format(len(table))

        missing_in_attr = missing_prop(table.has_missing_attribute()
                                       and table.get_nan_frequency_attribute())
        missing_in_class = missing_prop(table.has_missing_class()
                                        and table.get_nan_frequency_class())
        text += __("desc_text.feature").format(len(domain.attributes), missing_in_attr)
        if domain.has_continuous_class:
            text += __("desc_text.regression_numerical_class").format(missing_in_class)
        elif domain.has_discrete_class:
            text += __("desc_text.classification_categorical_class").format(len(domain.class_var.values),
                                                                            missing_in_class)
        elif table.domain.class_vars:
            text += __("desc_text.target_variable").format(len(table.domain.class_vars), missing_in_class)
        else:
            text += __("desc_text.data_no_target_variable")
        text += __("desc_text.meta_attribute").format(len(domain.metas))
        text += "</p>"

        if 'Timestamp' in table.domain:
            # Google Forms uses this header to timestamp responses
            text += __("desc_text.entry").format(table[0, 'Timestamp'], table[-1, 'Timestamp'])
        return text

    def storeSpecificSettings(self):
        self.current_context.modified_variables = self.variables[:]

    def retrieveSpecificSettings(self):
        if hasattr(self.current_context, "modified_variables"):
            self.variables[:] = self.current_context.modified_variables

    def reset_domain_edit(self):
        self.domain_editor.reset_domain()
        self.apply_domain_edit()

    def _inspect_discrete_variables(self, domain):
        for var in chain(domain.variables, domain.metas):
            if var.is_discrete and len(var.values) > 100:
                self.Warning.performance_warning()

    def apply_domain_edit(self):
        self.Warning.performance_warning.clear()
        self.Warning.renamed_vars.clear()
        if self.data is None:
            table = None
        else:
            domain, cols, renamed = \
                self.domain_editor.get_domain(self.data.domain, self.data,
                                              deduplicate=True)
            if not (domain.variables or domain.metas):
                table = None
            elif domain is self.data.domain:
                table = self.data
            else:
                X, y, m = cols
                table = Table.from_numpy(domain, X, y, m, self.data.W)
                table.name = self.data.name
                table.ids = np.array(self.data.ids)
                table.attributes = getattr(self.data, 'attributes', {})
                self._inspect_discrete_variables(domain)
            if renamed:
                self.Warning.renamed_vars(f"Renamed: {', '.join(renamed)}")

        summary = len(table) if table else self.info.NoOutput
        details = format_summary_details(table) if table else ""
        self.info.set_output_summary(summary, details)
        self.Outputs.data.send(table)
        self.apply_button.setEnabled(False)

    def get_widget_name_extension(self):
        _, name = os.path.split(self.loaded_file)
        return os.path.splitext(name)[0]

    def send_report(self):
        def get_ext_name(filename):
            try:
                return FileFormat.names[os.path.splitext(filename)[1]]
            except KeyError:
                return __("report.unknown")

        if self.data is None:
            self.report_paragraph(__("report.file"), __("report.no_file"))
            return

        if self.source == self.LOCAL_FILE:
            home = os.path.expanduser("~")
            if self.loaded_file.startswith(home):
                # os.path.join does not like ~
                name = "~" + os.path.sep + \
                       self.loaded_file[len(home):].lstrip("/").lstrip("\\")
            else:
                name = self.loaded_file
            if self.sheet_combo.isVisible():
                name += f" ({self.sheet_combo.currentText()})"
            self.report_items(__("report.file"), [(__("report.file_name"), name),
                                                  (__("report.format"), get_ext_name(name))])

        self.report_data(__("report.data"), self.data)

    def workflowEnvChanged(self, key, value, oldvalue):
        """
        Function called when environment changes (e.g. while saving the scheme)
        It make sure that all environment connected values are modified
        (e.g. relative file paths are changed)
        """
        self.update_file_list(key, value, oldvalue)


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWCaseData).run()
