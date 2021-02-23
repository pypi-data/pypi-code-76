import logging
import numbers
import copy
import traceback

from xml.sax.saxutils import escape
from concurrent.futures import ThreadPoolExecutor, Future

from types import SimpleNamespace
from typing import Optional, Dict, Tuple, List
from collections import namedtuple

from AnyQt.QtWidgets import (
    QLabel, QLineEdit, QTextBrowser, QSplitter, QTreeView, QGridLayout, QSizePolicy, QAbstractItemView,
    QStyleOptionViewItem, QStyledItemDelegate, QStyle, QApplication, QSizePolicy as Policy, QComboBox
)
from AnyQt.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from AnyQt.QtCore import (
    Qt, QSize, QObject, QThread, QModelIndex, QSortFilterProxyModel,
    QItemSelectionModel, QStringListModel,
    pyqtSlot as Slot, pyqtSignal as Signal
)

from orangecontrib.blue_whale.widgets.utils import get_sample_datasets_dir, Server, LocalFiles
from orangecontrib.blue_whale.i18n_config import *

import Orange.data
from Orange.widgets import settings, gui
from Orange.widgets.utils.signals import Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Msg
from orangewidget.utils.listview import ListViewSearch

log = logging.getLogger(__name__)


def __(key):
    return i18n.t("bluewhale.datasets." + key)


def format_exception(error):
    # type: (BaseException) -> str
    return "\n".join(traceback.format_exception_only(type(error), error))


class UniformHeightDelegate(QStyledItemDelegate):
    """
    Item delegate that always includes the icon size in the size hint.
    """

    def sizeHint(self, option, index):
        # type: (QStyleOptionViewItem, QModelIndex) -> QSize
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(option, index)
        opt.features |= QStyleOptionViewItem.HasDecoration
        widget = option.widget
        style = widget.style() if widget is not None else QApplication.style()
        sh = style.sizeFromContents(
            QStyle.CT_ItemViewItem, opt, QSize(), widget)
        return sh


class NumericalDelegate(UniformHeightDelegate):
    def initStyleOption(self, option, index):
        # type: (QStyleOptionViewItem, QModelIndex) -> None
        super().initStyleOption(option, index)
        data = index.data(Qt.DisplayRole)
        align = index.data(Qt.TextAlignmentRole)
        if align is None and isinstance(data, numbers.Number):
            # Right align if the model does not specify otherwise
            option.displayAlignment = Qt.AlignRight | Qt.AlignVCenter


class UniformHeightIndicatorDelegate(
    UniformHeightDelegate, gui.IndicatorItemDelegate):
    pass


class Namespace(SimpleNamespace):
    def __init__(self, **kwargs):
        self.file_path = None
        self.prefix = None
        self.filename = None
        self.islocal = None
        self.outdated = None

        # tags from JSON info file
        self.title = None
        self.description = None
        self.instances = None
        self.variables = None
        self.target = None
        self.size = None
        self.source = None
        self.year = None
        self.file_suffix = None
        self.file_type = None
        self.references = []
        self.seealso = []
        self.tags = []

        super(Namespace, self).__init__(**kwargs)

        if not self.title and self.name:
            self.title = self.name


class TreeViewWithReturn(QTreeView):
    returnPressed = Signal()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.returnPressed.emit()
        else:
            super().keyPressEvent(e)


class OWCase(OWWidget):
    name = __("name")
    description = __("desc")
    icon = "icons/case.svg"
    priority = 20
    keywords = ["online", "data sets"]

    want_control_area = False

    holder: list

    INDEX_URL = "http://onion-ring.uat.dashenglab.com/api/client/"

    HEADER_SCHEMA = [
        ['islocal', {'label': ''}],
        ['name', {'label': __("label.name")}],
        ['type', {'label': __("label.type")}],
        ['stars', {'label': __("label.stars")}],
        ['size', {'label': __("label.size")}],
        ['createdDate', {'label': __("label.create_date")}],
        ['tags', {'label': __("label.tags")}]
    ]  # type: List[str, dict]

    IndicatorBrushes = (QBrush(Qt.darkGray), QBrush(QColor(0, 192, 0)))

    class Error(OWWidget.Error):
        no_remote_datasets = Msg(__("msg_cannot_fetch_data"))

    class Warning(OWWidget.Warning):
        only_local_datasets = Msg(__("msg_not_fetch_data"))

    class Outputs:
        data = Output("Data", Orange.data.Table, label=i18n.t("bluewhale.common.data"))

    #: Selected dataset id
    selected_id = settings.Setting(None)  # type: Optional[str]

    #: main area splitter state
    splitter_state = settings.Setting(b'')  # type: bytes
    header_state = settings.Setting(b'')  # type: bytes

    def __init__(self, data_type='CASE'):
        super().__init__()
        self.__awaiting_state = None  # type: Optional[_FetchState]
        self.free = [{"id": '', 'name': __("all_info")}]
        self.allinfo_local = {}
        self.allinfo_remote = {}
        self.type = {'type': data_type}
        self.server = Server(data_type=self.type)

        self.local_cache_path = get_sample_datasets_dir()
        self.current_output = None

        self._header_labels = [
            header['label'] for _, header in self.HEADER_SCHEMA]
        self._header_index = namedtuple(
            '_header_index', [info_tag for info_tag, _ in self.HEADER_SCHEMA])
        self.Header = self._header_index(
            *[index for index, _ in enumerate(self._header_labels)])

        layout = QGridLayout()

        gui.widgetBox(self.mainArea, orientation=layout)

        data = self.server.open('spaces')
        if not data:
            self.close()
            return

        self.holder = self.free + data

        self.file_combo = QComboBox(self, sizeAdjustPolicy=QComboBox.AdjustToContents)
        self.file_combo.activated[int].connect(self.select_file)
        self.set_file_list()

        layout.addWidget(self.file_combo, 0, 0, 1, 1)

        display_box = gui.widgetBox(self.mainArea)
        display_box.setMaximumWidth(200)

        self.listModel = QStringListModel(self.mainArea)
        self.get_data_categories()

        self.group_view = gui.listView(
            self.mainArea, self,
            model=self.listModel,
            sizeHint=QSize(150, 400),
            viewType=ListViewSearch,
            sizePolicy=(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)  # 设置延伸
        )
        self.group_view.clicked.connect(self.get_datasets)
        self.group_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        display_box.layout().addWidget(self.group_view)
        layout.addWidget(display_box, 1, 0, 3, 1)

        self.filterLineEdit = QLineEdit(
            textChanged=self.filter, placeholderText=__("tip.search_for")
        )

        self.splitter = QSplitter(self.mainArea, orientation=Qt.Vertical)
        self.splitter.setSizePolicy(Policy.MinimumExpanding, Policy.MinimumExpanding)
        self.view = TreeViewWithReturn(
            sortingEnabled=True,
            selectionMode=QTreeView.SingleSelection,
            alternatingRowColors=True,
            rootIsDecorated=False,
            editTriggers=QTreeView.NoEditTriggers,
            uniformRowHeights=True,
            toolTip=__("tip.tree_view")
        )

        self.view.doubleClicked.connect(self.commit)
        self.view.returnPressed.connect(self.commit)

        download_button = gui.button(None, self, __("btn.down"), callback=self.commit, autoDefault=False)
        download_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))
        download_button.setSizePolicy(Policy.Expanding, Policy.Fixed)

        box = gui.widgetBox(self.splitter, __("title.desc"), addToLayout=False)
        self.descriptionlabel = QLabel(
            wordWrap=True,
            textFormat=Qt.RichText,
        )
        self.descriptionlabel = QTextBrowser(
            openExternalLinks=True,
            textInteractionFlags=(Qt.TextSelectableByMouse |
                                  Qt.LinksAccessibleByMouse)
        )
        self.descriptionlabel.setFrameStyle(QTextBrowser.NoFrame)
        self.descriptionlabel.viewport().setAutoFillBackground(False)

        box.layout().addWidget(self.descriptionlabel)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(download_button)
        self.splitter.addWidget(box)
        vbox = gui.vBox(self.mainArea, addToLayout=True)
        vbox.layout().addWidget(self.filterLineEdit)
        vbox.layout().addWidget(self.splitter)
        layout.addWidget(vbox, 1, 1, 3, 2)

        self.info.set_output_summary(self.info.NoOutput)

        self.splitter.splitterMoved.connect(
            lambda:
            setattr(self, "splitter_state", bytes(self.splitter.saveState()))
        )

        proxy = QSortFilterProxyModel()
        proxy.setFilterKeyColumn(-1)
        proxy.setFilterCaseSensitivity(False)
        self.view.setModel(proxy)

        if self.splitter_state:
            self.splitter.restoreState(self.splitter_state)

        self.assign_delegates()

        self.setBlocking(True)
        self.setStatusMessage(__("status.initialize"))

        self.get_datasets()

    def assign_delegates(self):
        # NOTE: All columns must have size hinting delegates.
        # QTreeView queries only the columns displayed in the viewport so
        # the layout would be different depending in the horizontal scroll
        # position
        self.view.setItemDelegate(UniformHeightDelegate(self))
        self.view.setItemDelegateForColumn(
            self.Header.islocal,
            UniformHeightIndicatorDelegate(self, role=Qt.DisplayRole, indicatorSize=4)
        )
        self.view.resizeColumnToContents(self.Header.islocal)

    def select_file(self, n):
        assert n < len(self.holder)
        holder_info = self.holder[n]
        del self.holder[n]
        self.holder.insert(0, holder_info)
        self.get_datasets()

        self.set_file_list()
        self.get_data_categories()

    def set_file_list(self):
        """
        Sets the items in the file list combo
        """
        self.file_combo.clear()

        if not self.holder:
            self.file_combo.addItem(__("all_info"))
            self.file_combo.model().item(0).setEnabled(False)
        else:
            for holder_info in self.holder:
                self.file_combo.addItem(holder_info['name'])

    def get_data_categories(self):
        data_category_info = self.server.open('categories')
        self.data_category = {i['categoryName']: i['id'] for i in data_category_info}
        self.listModel.setStringList(self.data_category.keys())

    def get_datasets(self, n=None):
        if Server().req.cookies.get('SESSION'):
            self.executor = ThreadPoolExecutor(max_workers=5)
            f = self.executor.submit(self.list_remote_category, n)
            w = FutureWatcher(f, parent=self)
            w.done.connect(self.__set_index)
        else:
            return None

    def list_remote_category(self, n=None):
        # type: () -> Dict[Tuple[str, ...], dict]
        """
        #  点击免费： 加载全部免费数据库   d为None   n 没有
        #  点击团队，加载全部团队信息    d 有  n 没有
        # 团队加上类型 团队有两种情况   d为Non类型有值    d有类型n也有
        :param n: 代表类型类型
        :return: 返回包装好的 server
        """
        d = {'Holder': self.holder[0]['id']}
        server = Server(data_type=copy.deepcopy(self.type))

        if not d['Holder'] and not n:
            return server.allinfo()

        if not d['Holder'] and n:
            params = {"categories": self.data_category[n.data()]}
            server.params = params
        elif not n and d:
            server.req.headers.update(d)
        else:
            params = {"categories": self.data_category[n.data()]}
            server.req.headers.update(d)
            server.params = params

        return server.allinfo()

    def ensure_local(self, file_path, local_cache_path, progress_advance=None):
        """

        :param file_path: 文件的路径
        :param local_cache_path: 文件本地下载包
        :param progress_advance:
        :return:
        """
        localfiles = LocalFiles(local_cache_path, serverfiles=self.server)
        file_path_id = file_path[0]

        if self.server.data_type['type'] == "CASE":
            data = self.server.open('resource', file_path_id, 'cascade_data')
            for resource_id in data:
                download_data = (resource_id, resource_id+'.bw')
                if download_data not in self.allinfo_local:
                    localfiles.download(*download_data)
                    localfiles.localpath_download(*download_data)

            localfiles.download(*file_path, callback=progress_advance)
            return localfiles.localpath_download(*file_path, callback=progress_advance)
        else:
            localfiles.download(*file_path, callback=progress_advance)
            return localfiles.localpath_download(*file_path, callback=progress_advance)

    def _parse_info(self, file_path):
        if file_path in self.allinfo_remote:
            info = self.allinfo_remote[file_path]
        else:
            info = self.allinfo_local[file_path]

        islocal = file_path in self.allinfo_local
        prefix = ''
        filename = file_path[-1]
        file_type = info['type']
        file_suffix = '.bws' if file_type == 'CASE' else '.bw'

        return Namespace(file_path=file_path, prefix=prefix, filename=filename,
                         islocal=islocal, file_type=file_type, file_suffix=file_suffix, **info)

    def create_model(self):
        allkeys = sorted(self.allinfo_remote)

        model = QStandardItemModel(self)
        model.setHorizontalHeaderLabels(self._header_labels)

        current_index = -1
        for i, file_path in enumerate(allkeys):
            datainfo = self._parse_info(file_path)
            item1 = QStandardItem()
            item1.setData(" " if datainfo.islocal else "", Qt.DisplayRole)
            item1.setData(self.IndicatorBrushes[0], Qt.ForegroundRole)
            item1.setData(datainfo, Qt.UserRole)
            item2 = QStandardItem(datainfo.name)
            item3 = QStandardItem()
            item3.setData(datainfo.type, Qt.DisplayRole)
            item4 = QStandardItem()
            item4.setData(datainfo.stars, Qt.DisplayRole)
            item5 = QStandardItem()
            item5.setData(datainfo.size, Qt.DisplayRole)
            item6 = QStandardItem()
            item6.setData(datainfo.createdDate.split(' ')[0], Qt.DisplayRole)
            item7 = QStandardItem()
            item7.setData(", ".join(datainfo.tags) if datainfo.tags else "",
                          Qt.DisplayRole)
            row = [item1, item2, item3, item4, item5, item6, item7]
            model.appendRow(row)

            if os.path.join('', file_path[-1]) == self.selected_id:
                current_index = i

        return model, current_index

    @Slot(object)
    def __set_index(self, f):
        # type: (Future) -> None
        assert QThread.currentThread() is self.thread()
        assert f.done()
        self.setBlocking(False)
        self.setStatusMessage("")
        self.allinfo_local = self.list_local()

        try:
            self.allinfo_remote = f.result()
        except Exception:  # anytying can happen, pylint: disable=broad-except
            log.exception("Error while fetching updated index")
            if not self.allinfo_local:
                self.Error.no_remote_datasets()
            else:
                self.Warning.only_local_datasets()
            self.allinfo_remote = {}

        self.selected_id = None
        model, current_index = self.create_model()

        self.view.model().setSourceModel(model)
        self.view.selectionModel().selectionChanged.connect(
            self.__on_selection
        )

        self.view.resizeColumnToContents(0)
        self.view.setColumnWidth(
            1, min(self.view.sizeHintForColumn(1),
                   self.view.fontMetrics().width("X" * 37)))

        header = self.view.header()
        header.restoreState(self.header_state)

        if current_index != -1:
            selmodel = self.view.selectionModel()
            selmodel.select(
                self.view.model().mapFromSource(model.index(current_index, 0)),
                QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
            self.commit()

    def __update_cached_state(self):
        model = self.view.model().sourceModel()
        localinfo = self.list_local()
        assert isinstance(model, QStandardItemModel)
        allinfo = []
        for i in range(model.rowCount()):
            item = model.item(i, 0)
            info = item.data(Qt.UserRole)
            is_local = info.file_path in localinfo
            is_current = (is_local and
                          os.path.join(self.local_cache_path, *info.file_path)
                          == self.current_output)
            item.setData(" " * (is_local + is_current), Qt.DisplayRole)
            item.setData(self.IndicatorBrushes[is_current], Qt.ForegroundRole)
            allinfo.append(info)

    def selected_dataset(self):
        """
        Return the current selected dataset info or None if not selected

        Returns
        -------
        info : Optional[Namespace]
        """
        rows = self.view.selectionModel().selectedRows(0)
        assert 0 <= len(rows) <= 1
        current = rows[0] if rows else None  # type: Optional[QModelIndex]
        if current is not None:
            info = current.data(Qt.UserRole)

            assert isinstance(info, Namespace)
        else:
            info = None
        return info

    def filter(self):
        filter_string = self.filterLineEdit.text().strip()
        proxyModel = self.view.model()
        if proxyModel:
            proxyModel.setFilterFixedString(filter_string)

    def __on_selection(self):
        # Main datasets view selection has changed
        rows = self.view.selectionModel().selectedRows(0)
        assert 0 <= len(rows) <= 1
        current = rows[0] if rows else None  # type: Optional[QModelIndex]
        if current is not None:
            current = self.view.model().mapToSource(current)
            di = current.data(Qt.UserRole)
            text = self.description_html(di)
            self.descriptionlabel.setText(text)
            self.selected_id = os.path.join(di.prefix, di.filename)
        else:
            self.descriptionlabel.setText("")
            self.selected_id = None

    def commit(self):
        """
        Commit a dataset to the output immediately (if available locally) or
        schedule download background and an eventual send.

        During the download the widget is in blocking state
        (OWWidget.isBlocking)
        """
        di = self.selected_dataset()
        user = Server().open('userinfo')
        if di is not None and user is not None:
            self.Error.clear()

            if self.__awaiting_state is not None:
                # disconnect from the __commit_complete
                self.__awaiting_state.watcher.done.disconnect(
                    self.__commit_complete)
                # .. and connect to update_cached_state
                # self.__awaiting_state.watcher.done.connect(
                #     self.__update_cached_state)
                # TODO: There are possible pending __progress_advance queued
                self.__awaiting_state.pb.advance.disconnect(
                    self.__progress_advance)
                self.progressBarFinished()
                self.__awaiting_state = None

            if not di.islocal:
                pr = progress()
                callback = lambda pr=pr: pr.advance.emit()
                pr.advance.connect(self.__progress_advance, Qt.QueuedConnection)

                self.progressBarInit()
                self.setStatusMessage(__("status.fetch"))
                self.setBlocking(True)

                f = self.executor.submit(self.ensure_local, di.file_path, self.local_cache_path,
                                          progress_advance=callback)
                w = FutureWatcher(f, parent=self)
                w.done.connect(self.__commit_complete)
                self.__awaiting_state = _FetchState(f, w, pr)
            else:
                self.setStatusMessage("")
                self.setBlocking(False)
                self.commit_cached(di.file_path)
        else:
            return None

    @Slot(object)
    def __commit_complete(self, f):
        # complete the commit operation after the required file has been
        # downloaded
        assert QThread.currentThread() is self.thread()
        assert self.__awaiting_state is not None
        assert self.__awaiting_state.future is f

        if self.isBlocking():
            self.progressBarFinished()
            self.setBlocking(False)
            self.setStatusMessage("")

        self.__awaiting_state = None

        try:
            path = f.result()
        # anything can happen here, pylint: disable=broad-except
        except Exception as ex:
            log.exception("Error:")
            self.error(format_exception(ex))
            path = None
        self.load_and_output(path)

        _, ext = os.path.splitext(path)
        if ext == '.bws':
            from orangecontrib.blue_whale.canvasmain import BWCanvasMainWindow
            BWCanvasMainWindow().open_case(path)

    def commit_cached(self, file_path):
        path = LocalFiles(self.local_cache_path).localpath(*file_path)
        self.load_and_output(path)

    @Slot()
    def __progress_advance(self):
        assert QThread.currentThread() is self.thread()
        self.progressBarAdvance(1)

    def onDeleteWidget(self):
        super().onDeleteWidget()
        if self.__awaiting_state is not None:
            self.__awaiting_state.watcher.done.disconnect(self.__commit_complete)
            self.__awaiting_state.pb.advance.disconnect(self.__progress_advance)
            self.__awaiting_state = None

    @staticmethod
    def sizeHint():
        return QSize(1100, 500)

    def closeEvent(self, event):
        if hasattr(self, 'splitter') and hasattr(self, 'view'):
            self.splitter_state = bytes(self.splitter.saveState())
            self.header_state = bytes(self.view.header().saveState())

        super().closeEvent(event)

    def load_and_output(self, path):  # 用户下载完成有个标志
        self.current_output = path
        self.__update_cached_state()

    def list_local(self):
        # type: () -> Dict[Tuple[str, ...], dict]
        return LocalFiles(self.local_cache_path).allinfo(suffix='.bw')

    def make_html_list(self, items):
        if items is None:
            return ''
        style = '"margin: 5px; text-indent: -40px; margin-left: 40px;"'

        def format_item(i):
            return '<p style={}><small>{}</small></p>'.format(style, i)

        return '\n'.join([format_item(i) for i in items])

    def description_html(self, datainfo):
        # type: (Namespace) -> str
        """
        Summarize a data info as a html fragment.
        """
        html = []
        year = " ({})".format(str(datainfo.year)) if datainfo.year else ""
        source = ", from {}".format(datainfo.source) if datainfo.source else ""

        html.append("<b>{}</b>{}{}".format(escape(datainfo.title), year, source))
        description = self.server.open('resource', datainfo.id)
        # http://onion-ring.uat.dashenglab.com/api/client/resource/60012f0452eddb11973b6ece"
        html.append("{}".format(description.get('description')))
        seealso = self.make_html_list(datainfo.seealso)
        if seealso:
            html.append(__("see_also") + seealso + "</small>")
        refs = self.make_html_list(datainfo.references)
        if refs:
            html.append(__("reference") + refs + "</small>")
        return "\n".join(html)


class FutureWatcher(QObject):
    done = Signal(object)
    _p_done_notify = Signal(object)

    def __init__(self, future, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.__future = future
        self._p_done_notify.connect(self.__on_done, Qt.QueuedConnection)
        future.add_done_callback(self._p_done_notify.emit)

    @Slot(object)
    def __on_done(self, f):
        assert f is self.__future
        self.done.emit(self.__future)


class progress(QObject):
    advance = Signal()


class _FetchState:
    def __init__(self, future, watcher, pb):
        self.future = future
        self.watcher = watcher
        self.pb = pb


def variable_icon(name):
    if name == "categorical":
        return gui.attributeIconDict[Orange.data.DiscreteVariable("x")]
    elif name == "numeric":  # ??
        return gui.attributeIconDict[Orange.data.ContinuousVariable("x")]
    else:
        return gui.attributeIconDict[-1]


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWCase).run()
