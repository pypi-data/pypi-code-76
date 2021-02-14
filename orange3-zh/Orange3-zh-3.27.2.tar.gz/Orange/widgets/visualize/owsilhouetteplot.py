import itertools
import enum
from xml.sax.saxutils import escape
from types import SimpleNamespace as namespace

from typing import Optional, Union

import numpy as np
import sklearn.metrics

from AnyQt.QtWidgets import (
    QGraphicsScene, QGraphicsWidget, QGraphicsGridLayout,
    QGraphicsRectItem, QStyleOptionGraphicsItem, QSizePolicy, QWidget,
    QVBoxLayout, QGraphicsSimpleTextItem, QWIDGETSIZE_MAX,
)
from AnyQt.QtGui import QColor, QPen, QBrush, QPainter, QFontMetrics, QPalette
from AnyQt.QtCore import Qt, QEvent, QRectF, QSizeF, QSize, QPointF
from AnyQt.QtCore import pyqtSignal as Signal

import pyqtgraph as pg

import Orange.data
from Orange.data.util import get_unique_names
import Orange.distance
import Orange.misc
from Orange.data import Table, Domain
from Orange.misc import DistMatrix

from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.stickygraphicsview import StickyGraphicsView
from Orange.widgets.utils import itemmodels
from Orange.widgets.utils.annotated_data import (create_annotated_table,
                                                 ANNOTATED_DATA_SIGNAL_Chinese_NAME)
from Orange.widgets.utils.graphicstextlist import TextListWidget
from Orange.widgets.utils.graphicslayoutitem import SimpleLayoutItem
from Orange.widgets.utils.sql import check_sql_input
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.utils.state_summary import format_summary_details
from Orange.widgets.widget import Msg, Input, Output


ROW_NAMES_WIDTH = 200


class InputValidationError(ValueError):
    message: str


class NoGroupVariable(InputValidationError):
    message = "Input does not have any suitable labels"


class ValidationError(InputValidationError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class OWSilhouettePlot(widget.OWWidget):
    name = "轮廓图(Silhouette Plot)"
    description = "视觉评估聚类质量和聚类成员的程度。"
    category = 'visualize'

    icon = "icons/SilhouettePlot.svg"
    priority = 300
    keywords = []

    class Inputs:
        data = Input("数据(Data)", (Orange.data.Table, Orange.misc.DistMatrix), replaces=['Data'])

    class Outputs:
        selected_data = Output("选定的数据(Selected Data)", Orange.data.Table, default=True, replaces=['Selected Data'])
        annotated_data = Output(ANNOTATED_DATA_SIGNAL_Chinese_NAME, Orange.data.Table, replaces=['Data'])

    replaces = [
        "orangecontrib.prototypes.widgets.owsilhouetteplot.OWSilhouettePlot",
        "Orange.widgets.unsupervised.owsilhouetteplot.OWSilhouettePlot"
    ]

    settingsHandler = settings.PerfectDomainContextHandler()

    #: Distance metric index
    distance_idx = settings.Setting(0)
    #: Group/cluster variable index
    cluster_var_idx = settings.ContextSetting(0)
    #: Annotation variable index
    annotation_var_idx = settings.ContextSetting(0)
    #: Group the (displayed) silhouettes by cluster
    group_by_cluster = settings.Setting(True)
    #: A fixed size for an instance bar
    bar_size = settings.Setting(3)
    #: Add silhouette scores to output data
    auto_commit = settings.Setting(True)

    pending_selection = settings.Setting(None, schema_only=True)

    Distances = [("欧几里德", Orange.distance.Euclidean),
                 ("曼哈顿", Orange.distance.Manhattan),
                 ("余弦", Orange.distance.Cosine)]

    graph_name = "scene"
    buttons_area_orientation = Qt.Vertical

    class Error(widget.OWWidget.Error):
        need_two_clusters = Msg("Need at least two non-empty clusters")
        singleton_clusters_all = Msg("All clusters are singletons")
        memory_error = Msg("Not enough memory")
        value_error = Msg("Distances could not be computed: '{}'")
        input_validation_error = Msg("{}")

    class Warning(widget.OWWidget.Warning):
        missing_cluster_assignment = Msg(
            "{} instance{s} omitted (missing cluster assignment)")
        nan_distances = Msg("{} instance{s} omitted (undefined distances)")
        ignoring_categorical = Msg("Ignoring categorical features")

    def __init__(self):
        super().__init__()
        #: The input data
        self.data = None         # type: Optional[Orange.data.Table]
        #: The input distance matrix (if present)
        self.distances = None  # type: Optional[Orange.misc.DistMatrix]
        #: The effective distance matrix (is self.distances or computed from
        #: self.data depending on input)
        self._matrix = None      # type: Optional[Orange.misc.DistMatrix]
        #: An bool mask (size == len(data)) indicating missing group/cluster
        #: assignments
        self._mask = None        # type: Optional[np.ndarray]
        #: An array of cluster/group labels for instances with valid group
        #: assignment
        self._labels = None      # type: Optional[np.ndarray]
        #: An array of silhouette scores for instances with valid group
        #: assignment
        self._silhouette = None  # type: Optional[np.ndarray]
        self._silplot = None     # type: Optional[SilhouettePlot]

        self.info.set_input_summary(self.info.NoInput)
        self.info.set_output_summary(self.info.NoOutput)

        controllayout = self.controlArea.layout()
        assert isinstance(controllayout, QVBoxLayout)
        self._distances_gui_box = distbox = gui.widgetBox(
            None, "距离"
        )
        self._distances_gui_cb = gui.comboBox(
            distbox, self, "distance_idx",
            items=[name for name, _ in OWSilhouettePlot.Distances],
            orientation=Qt.Horizontal, callback=self._invalidate_distances)
        controllayout.addWidget(distbox)

        box = gui.vBox(self.controlArea, "聚类标签")
        self.cluster_var_cb = gui.comboBox(
            box, self, "cluster_var_idx", contentsLength=14, addSpace=4,
            searchable=True, callback=self._invalidate_scores
        )
        gui.checkBox(
            box, self, "group_by_cluster", "按聚类分组(Group by cluster)",
            callback=self._replot)
        self.cluster_var_model = itemmodels.VariableListModel(parent=self)
        self.cluster_var_cb.setModel(self.cluster_var_model)

        box = gui.vBox(self.controlArea, "条")
        gui.widgetLabel(box, "条宽度:")
        gui.hSlider(
            box, self, "bar_size", minValue=1, maxValue=10, step=1,
            callback=self._update_bar_size, addSpace=6)
        gui.widgetLabel(box, "注释:")
        self.annotation_cb = gui.comboBox(
            box, self, "annotation_var_idx", contentsLength=14,
            callback=self._update_annotations)
        self.annotation_var_model = itemmodels.VariableListModel(parent=self)
        self.annotation_var_model[:] = ["无"]
        self.annotation_cb.setModel(self.annotation_var_model)
        ibox = gui.indentedBox(box, 5)
        self.ann_hidden_warning = warning = gui.widgetLabel(
            ibox, "(增加要显示的宽度)")
        ibox.setFixedWidth(ibox.sizeHint().width())
        warning.setVisible(False)

        gui.rubber(self.controlArea)

        box = gui.vBox(self.buttonsArea, box=True)
        gui.auto_send(box, self, "auto_commit", box=False)
        # Ensure that the controlArea is not narrower than buttonsArea
        self.controlArea.layout().addWidget(self.buttonsArea)

        self.scene = QGraphicsScene(self)
        self.view = StickyGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing, True)
        self.view.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.mainArea.layout().addWidget(self.view)

        self.settingsAboutToBePacked.connect(self.pack_settings)

    def sizeHint(self):
        sh = self.controlArea.sizeHint()
        return sh.expandedTo(QSize(600, 720))

    def pack_settings(self):
        if self.data and self._silplot is not None:
            self.pending_selection = list(self._silplot.selection())
        else:
            self.pending_selection = None

    @Inputs.data
    @check_sql_input
    def set_data(self, data: Union[Table, DistMatrix, None]):
        """
        Set the input dataset or distance matrix.
        """
        self.closeContext()
        self.clear()
        try:
            if isinstance(data, Orange.misc.DistMatrix):
                self._set_distances(data)
            elif isinstance(data, Orange.data.Table):
                self._set_table(data)
            else:
                self.distances = None
                self.data = None
        except InputValidationError as err:
            self.Error.input_validation_error(err.message)
            self.distances = None
            self.data = None

    def _set_table(self, data: Table):
        self._setup_control_models(data.domain)
        self.data = data
        self.distances = None

    def _set_distances(self, distances: DistMatrix):
        if isinstance(distances.row_items, Orange.data.Table) and \
                distances.axis == 1:
            data = distances.row_items
        else:
            raise ValidationError("Input matrix does not have associated data")

        if data is not None:
            self._setup_control_models(data.domain)
            self.distances = distances
            self.data = data

    def handleNewSignals(self):
        summary = len(self.data) if self.data else self.info.NoInput
        details = format_summary_details(self.data) if self.data else ""
        self.info.set_input_summary(summary, details)
        if not self._is_empty():
            self._update()
            self._replot()
            if self.pending_selection is not None and self._silplot is not None:
                # If selection contains indices that are too large, the data
                # file must had been modified, so we ignore selection
                if max(self.pending_selection, default=-1) < len(self.data):
                    self._silplot.setSelection(np.array(self.pending_selection))
                self.pending_selection = None

        # Disable/enable the Distances GUI controls if applicable
        self._distances_gui_box.setEnabled(self.distances is None)

        self.unconditional_commit()

    def _setup_control_models(self, domain: Domain):
        groupvars = [
            v for v in domain.variables + domain.metas
            if v.is_discrete and len(v.values) >= 2]
        if not groupvars:
            raise NoGroupVariable()
        self.cluster_var_model[:] = groupvars
        if domain.class_var in groupvars:
            self.cluster_var_idx = groupvars.index(domain.class_var)
        else:
            self.cluster_var_idx = 0
        annotvars = [var for var in domain.metas if var.is_string]
        self.annotation_var_model[:] = ["None"] + annotvars
        self.annotation_var_idx = 1 if annotvars else 0
        self.openContext(Orange.data.Domain(groupvars))

    def _is_empty(self) -> bool:
        # Is empty (does not have any input).
        return (self.data is None or len(self.data) == 0) \
               and self.distances is None

    def clear(self):
        """
        Clear the widget state.
        """
        self.data = None
        self.distances = None
        self._matrix = None
        self._mask = None
        self._silhouette = None
        self._labels = None
        self.cluster_var_model[:] = []
        self.annotation_var_model[:] = ["None"]
        self._clear_scene()
        self.Error.clear()
        self.Warning.clear()

    def _clear_scene(self):
        # Clear the graphics scene and associated objects
        self.scene.clear()
        self.scene.setSceneRect(QRectF())
        self.view.setSceneRect(QRectF())
        self.view.setHeaderSceneRect(QRectF())
        self.view.setFooterSceneRect(QRectF())
        self._silplot = None

    def _invalidate_distances(self):
        # Invalidate the computed distance matrix and recompute the silhouette.
        self._matrix = None
        self._invalidate_scores()

    def _invalidate_scores(self):
        # Invalidate and recompute the current silhouette scores.
        self._labels = self._silhouette = self._mask = None
        self._update()
        self._replot()
        if self.data is not None:
            self.commit()

    def _ensure_matrix(self):
        # ensure self._matrix is computed if necessary
        if self._is_empty():
            return
        if self._matrix is None:
            if self.distances is not None:
                self._matrix = np.asarray(self.distances)
            elif self.data is not None:
                data = self.data
                _, metric = self.Distances[self.distance_idx]
                if not metric.supports_discrete and any(
                        a.is_discrete for a in data.domain.attributes):
                    self.Warning.ignoring_categorical()
                    data = Orange.distance.remove_discrete_features(data)
                try:
                    self._matrix = np.asarray(metric(data))
                except MemoryError:
                    self.Error.memory_error()
                    return
                except ValueError as err:
                    self.Error.value_error(str(err))
                    return
            else:
                assert False, "invalid state"

    def _update(self):
        # Update/recompute the effective distances and scores as required.
        self._clear_messages()
        if self._is_empty():
            self._reset_all()
            return

        self._ensure_matrix()
        if self._matrix is None:
            return

        labelvar = self.cluster_var_model[self.cluster_var_idx]
        labels, _ = self.data.get_column_view(labelvar)
        labels = np.asarray(labels, dtype=float)
        cluster_mask = np.isnan(labels)
        dist_mask = np.isnan(self._matrix).all(axis=0)
        mask = cluster_mask | dist_mask
        labels = labels.astype(int)
        labels = labels[~mask]

        labels_unq = np.unique(labels)

        if len(labels_unq) < 2:
            self.Error.need_two_clusters()
            labels = silhouette = mask = None
        elif len(labels_unq) == len(labels):
            self.Error.singleton_clusters_all()
            labels = silhouette = mask = None
        else:
            silhouette = sklearn.metrics.silhouette_samples(
                self._matrix[~mask, :][:, ~mask], labels, metric="precomputed")
        self._mask = mask
        self._labels = labels
        self._silhouette = silhouette

        if mask is not None:
            count_missing = np.count_nonzero(cluster_mask)
            if count_missing:
                self.Warning.missing_cluster_assignment(
                    count_missing, s="s" if count_missing > 1 else "")
            count_nandist = np.count_nonzero(dist_mask)
            if count_nandist:
                self.Warning.nan_distances(
                    count_nandist, s="s" if count_nandist > 1 else "")

    def _reset_all(self):
        self._mask = None
        self._silhouette = None
        self._labels = None
        self._matrix = None
        self._clear_scene()

    def _clear_messages(self):
        self.Error.clear()
        self.Warning.clear()

    def _set_bar_height(self):
        visible = self.bar_size >= 5
        self._silplot.setBarHeight(self.bar_size)
        self._silplot.setRowNamesVisible(visible)
        self.ann_hidden_warning.setVisible(
            not visible and self.annotation_var_idx > 0)

    def _replot(self):
        # Clear and replot/initialize the scene
        self._clear_scene()
        if self._silhouette is not None and self._labels is not None:
            var = self.cluster_var_model[self.cluster_var_idx]
            self._silplot = silplot = SilhouettePlot()
            self._set_bar_height()

            if self.group_by_cluster:
                silplot.setScores(self._silhouette, self._labels, var.values,
                                  var.colors)
            else:
                silplot.setScores(
                    self._silhouette,
                    np.zeros(len(self._silhouette), dtype=int),
                    [""], np.array([[63, 207, 207]])
                )

            self.scene.addItem(silplot)
            self._update_annotations()
            silplot.selectionChanged.connect(self.commit)
            silplot.layout().activate()
            self._update_scene_rect()
            silplot.geometryChanged.connect(self._update_scene_rect)

    def _update_bar_size(self):
        if self._silplot is not None:
            self._set_bar_height()

    def _update_annotations(self):
        if 0 < self.annotation_var_idx < len(self.annotation_var_model):
            annot_var = self.annotation_var_model[self.annotation_var_idx]
        else:
            annot_var = None
        self.ann_hidden_warning.setVisible(
            self.bar_size < 5 and annot_var is not None)

        if self._silplot is not None:
            if annot_var is not None:
                column, _ = self.data.get_column_view(annot_var)
                if self._mask is not None:
                    assert column.shape == self._mask.shape
                    # pylint: disable=invalid-unary-operand-type
                    column = column[~self._mask]
                self._silplot.setRowNames(
                    [annot_var.str_val(value) for value in column])
            else:
                self._silplot.setRowNames(None)

    def _update_scene_rect(self):
        geom = self._silplot.geometry()
        self.scene.setSceneRect(geom)
        self.view.setSceneRect(geom)

        header = self._silplot.topScaleItem()
        footer = self._silplot.bottomScaleItem()

        def extend_horizontal(rect):
            # type: (QRectF) -> QRectF
            rect = QRectF(rect)
            rect.setLeft(geom.left())
            rect.setRight(geom.right())
            return rect

        margin = 3
        if header is not None:
            self.view.setHeaderSceneRect(
                extend_horizontal(header.geometry().adjusted(0, 0, 0, margin)))
        if footer is not None:
            self.view.setFooterSceneRect(
                extend_horizontal(footer.geometry().adjusted(0, -margin, 0, 0)))

    def commit(self):
        """
        Commit/send the current selection to the output.
        """
        selected = indices = data = None
        if self.data is not None:
            selectedmask = np.full(len(self.data), False, dtype=bool)
            if self._silplot is not None:
                indices = self._silplot.selection()
                assert (np.diff(indices) > 0).all(), "strictly increasing"
                if self._mask is not None:
                    # pylint: disable=invalid-unary-operand-type
                    indices = np.flatnonzero(~self._mask)[indices]
                selectedmask[indices] = True

            if self._mask is not None:
                scores = np.full(shape=selectedmask.shape,
                                 fill_value=np.nan)
                # pylint: disable=invalid-unary-operand-type
                scores[~self._mask] = self._silhouette
            else:
                scores = self._silhouette

            var = self.cluster_var_model[self.cluster_var_idx]
            
            domain = self.data.domain
            proposed = "Silhouette ({})".format(escape(var.name))
            names = [var.name for var in itertools.chain(domain.attributes,
                                                         domain.class_vars,
                                                         domain.metas)]
            unique = get_unique_names(names, proposed)
            silhouette_var = Orange.data.ContinuousVariable(unique)
            domain = Orange.data.Domain(
                domain.attributes,
                domain.class_vars,
                domain.metas + (silhouette_var, ))
            data = self.data.transform(domain)

            if np.count_nonzero(selectedmask):
                selected = self.data.from_table(
                    domain, self.data, np.flatnonzero(selectedmask))

            if selected is not None:
                selected[:, silhouette_var] = np.c_[scores[selectedmask]]
            data[:, silhouette_var] = np.c_[scores]

        summary = len(selected) if selected else self.info.NoOutput
        details = format_summary_details(selected) if selected else ""
        self.info.set_output_summary(summary, details)
        self.Outputs.selected_data.send(selected)
        self.Outputs.annotated_data.send(create_annotated_table(data, indices))

    def send_report(self):
        if not len(self.cluster_var_model):
            return

        self.report_plot()
        caption = "Silhouette plot ({} distance), clustered by '{}'".format(
            self.Distances[self.distance_idx][0],
            self.cluster_var_model[self.cluster_var_idx])
        if self.annotation_var_idx and self._silplot.rowNamesVisible():
            caption += ", annotated with '{}'".format(
                self.annotation_var_model[self.annotation_var_idx])
        self.report_caption(caption)

    def onDeleteWidget(self):
        self.clear()
        super().onDeleteWidget()


class SelectAction(enum.IntEnum):
    NoUpdate, Clear, Select, Deselect, Toogle, Current = 1, 2, 4, 8, 16, 32


class SilhouettePlot(QGraphicsWidget):
    """
    A silhouette plot widget.
    """
    #: Emitted when the current selection has changed
    selectionChanged = Signal()

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.setAcceptHoverEvents(True)
        self.__groups = []
        self.__rowNamesVisible = True
        self.__barHeight = 3
        self.__selectionRect = None
        self.__selection = np.asarray([], dtype=int)
        self.__selstate = None
        self.__pen = QPen(Qt.NoPen)
        self.__layout = QGraphicsGridLayout()
        self.__hoveredItem = None
        self.__topScale = None     # type: Optional[pg.AxisItem]
        self.__bottomScale = None  # type: Optional[pg.AxisItem]
        self.__layout.setColumnSpacing(0, 1.)
        self.setLayout(self.__layout)
        self.setFocusPolicy(Qt.StrongFocus)

    def setScores(self, scores, labels, values, colors, rownames=None):
        """
        Set the silhouette scores/labels to for display.

        Arguments
        ---------
        scores : (N,) ndarray
            The silhouette scores.
        labels : (N,) ndarray
            A ndarray (dtype=int) of label/clusters indices.
        values : list of str
            A list of label/cluster names.
        colors : (N, 3) ndarray
            A ndarray of RGB values.
        rownames : list of str, optional
            A list (len == N) of row names.
        """
        scores = np.asarray(scores, dtype=float)
        labels = np.asarray(labels, dtype=int)
        if rownames is not None:
            rownames = np.asarray(rownames, dtype=object)

        if not scores.ndim == labels.ndim == 1:
            raise ValueError("scores and labels must be 1 dimensional")
        if scores.shape != labels.shape:
            raise ValueError("scores and labels must have the same shape")
        if rownames is not None and rownames.shape != scores.shape:
            raise ValueError("rownames must have the same size as scores")

        Ck = np.unique(labels)
        if not Ck[0] >= 0 and Ck[-1] < len(values):
            raise ValueError(
                "All indices in `labels` must be in `range(len(values))`")
        cluster_indices = [np.flatnonzero(labels == i)
                           for i in range(len(values))]
        cluster_indices = [indices[np.argsort(scores[indices])[::-1]]
                           for indices in cluster_indices]
        groups = [
            namespace(scores=scores[indices], indices=indices, label=label,
                      rownames=(rownames[indices] if rownames is not None
                                else None),
                      color=color)
            for indices, label, color in zip(cluster_indices, values, colors)
        ]
        self.clear()
        self.__groups = groups
        self.__setup()

    def setRowNames(self, names):
        if names is not None:
            names = np.asarray(names, dtype=object)

        layout = self.__layout
        assert layout is self.layout()

        font = self.font()
        font.setPixelSize(self.__barHeight)

        for i, grp in enumerate(self.__groups):
            grp.rownames = names[grp.indices] if names is not None else None
            item = layout.itemAt(i + 1, 3)
            assert isinstance(item, TextListWidget)
            if grp.rownames is not None:
                metrics = QFontMetrics(self.font())
                rownames = [metrics.elidedText(rowname, Qt.ElideRight, ROW_NAMES_WIDTH)
                            for rowname in grp.rownames]
                item.setItems(rownames)
                item.setVisible(self.__rowNamesVisible)
            else:
                item.setItems([])
                item.setVisible(False)

            barplot = list(self.__plotItems())[i]
            baritems = barplot.items()

            if grp.rownames is None:
                tooltips = itertools.repeat("")
            else:
                tooltips = grp.rownames

            for baritem, tooltip in zip(baritems, tooltips):
                baritem.setToolTip(tooltip)

        layout.activate()

    def setRowNamesVisible(self, visible):
        if self.__rowNamesVisible != visible:
            self.__rowNamesVisible = visible
            for item in self.__textItems():
                item.setVisible(visible)
            self.updateGeometry()

    def rowNamesVisible(self):
        return self.__rowNamesVisible

    def setBarHeight(self, height):
        """
        Set silhouette bar height (row height).
        """
        if height != self.__barHeight:
            self.__barHeight = height
            for item in self.__plotItems():
                item.setPreferredBarSize(height)
            font = self.font()
            font.setPixelSize(height)
            for item in self.__textItems():
                item.setFont(font)

    def barHeight(self):
        """
        Return the silhouette bar (row) height.
        """
        return self.__barHeight

    def clear(self):
        """
        Clear the widget state
        """
        scene = self.scene()
        for child in self.childItems():
            child.setParentItem(None)
            scene.removeItem(child)
        self.__groups = []
        self.__topScale = None
        self.__bottomScale = None

    def __setup(self):
        # Setup the subwidgets/groups/layout
        smax = max((np.nanmax(g.scores) for g in self.__groups
                    if g.scores.size),
                   default=1)
        smax = 1 if np.isnan(smax) else smax

        smin = min((np.nanmin(g.scores) for g in self.__groups
                    if g.scores.size),
                   default=-1)
        smin = -1 if np.isnan(smin) else smin
        smin = min(smin, 0)

        font = self.font()
        font.setPixelSize(self.__barHeight)
        axispen = QPen(Qt.black)

        ax = pg.AxisItem(parent=self, orientation="top", maxTickLength=7,
                         pen=axispen)
        ax.setRange(smin, smax)
        self.__topScale = ax
        layout = self.__layout
        assert layout is self.layout()
        layout.addItem(ax, 0, 2)

        for i, group in enumerate(self.__groups):
            silhouettegroup = BarPlotItem(parent=self)
            silhouettegroup.setBrush(QBrush(QColor(*group.color)))
            silhouettegroup.setPen(self.__pen)
            silhouettegroup.setDataRange(smin, smax)
            silhouettegroup.setPlotData(group.scores)
            silhouettegroup.setPreferredBarSize(self.__barHeight)
            silhouettegroup.setData(0, group.indices)
            layout.addItem(silhouettegroup, i + 1, 2)

            if group.label:
                layout.addItem(Line(orientation=Qt.Vertical), i + 1, 1)
                label = QGraphicsSimpleTextItem(
                    "{} ({})".format(group.label, len(group.scores)), self
                )
                label.setRotation(-90)
                item = SimpleLayoutItem(
                    label,
                    anchor=(0., 1.0),
                    anchorItem=(0., 0.),
                )
                item.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                layout.addItem(item, i + 1, 0, Qt.AlignCenter)

            textlist = TextListWidget(self, font=font)
            sp = textlist.sizePolicy()
            sp.setVerticalPolicy(QSizePolicy.Ignored)
            textlist.setSizePolicy(sp)
            textlist.setParent(self)
            if group.rownames is not None:
                textlist.setItems(group.items)
                textlist.setVisible(self.__rowNamesVisible)
            else:
                textlist.setVisible(False)

            layout.addItem(textlist, i + 1, 3)

        ax = pg.AxisItem(parent=self, orientation="bottom", maxTickLength=7,
                         pen=axispen)
        ax.setRange(smin, smax)
        self.__bottomScale = ax
        layout.addItem(ax, len(self.__groups) + 1, 2)

    def topScaleItem(self):
        # type: () -> Optional[QGraphicsWidget]
        return self.__topScale

    def bottomScaleItem(self):
        # type: () -> Optional[QGraphicsWidget]
        return self.__bottomScale

    def __updateTextSizeConstraint(self):
        # set/update fixed height constraint on the text annotation items so
        # it matches the silhouette's height
        for silitem, textitem in zip(self.__plotItems(), self.__textItems()):
            height = silitem.effectiveSizeHint(Qt.PreferredSize).height()
            textitem.setMaximumHeight(height)
            textitem.setMinimumHeight(height)

    def event(self, event):
        # Reimplemented
        if event.type() == QEvent.LayoutRequest and \
                self.parentLayoutItem() is None:
            self.__updateTextSizeConstraint()
            self.resize(self.effectiveSizeHint(Qt.PreferredSize))
        return super().event(event)

    def __setHoveredItem(self, item):
        # Set the current hovered `item` (:class:`QGraphicsRectItem`)
        if self.__hoveredItem is not item:
            if self.__hoveredItem is not None:
                self.__hoveredItem.setPen(QPen(Qt.NoPen))
            self.__hoveredItem = item
            if item is not None:
                item.setPen(QPen(Qt.lightGray))

    def hoverEnterEvent(self, event):
        # Reimplemented
        event.accept()

    def hoverMoveEvent(self, event):
        # Reimplemented
        event.accept()
        item = self.itemAtPos(event.pos())
        self.__setHoveredItem(item)

    def hoverLeaveEvent(self, event):
        # Reimplemented
        self.__setHoveredItem(None)
        event.accept()

    def mousePressEvent(self, event):
        # Reimplemented
        if event.button() == Qt.LeftButton:
            if event.modifiers() & Qt.ControlModifier:
                saction = SelectAction.Toogle
            elif event.modifiers() & Qt.AltModifier:
                saction = SelectAction.Deselect
            elif event.modifiers() & Qt.ShiftModifier:
                saction = SelectAction.Select
            else:
                saction = SelectAction.Clear | SelectAction.Select
            self.__selstate = namespace(
                modifiers=event.modifiers(),
                selection=self.__selection,
                action=saction,
                rect=None,
            )
            if saction & SelectAction.Clear:
                self.__selstate.selection = np.array([], dtype=int)
                self.setSelection(self.__selstate.selection)
            event.accept()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Up, Qt.Key_Down):
            if event.key() == Qt.Key_Up:
                self.__move_selection(self.selection(), -1)
            elif event.key() == Qt.Key_Down:
                self.__move_selection(self.selection(), 1)
            event.accept()
            return
        super().keyPressEvent(event)

    def mouseMoveEvent(self, event):
        # Reimplemented
        if event.buttons() & Qt.LeftButton:
            assert self.__selstate is not None
            if self.__selectionRect is None:
                self.__selectionRect = QGraphicsRectItem(self)

            rect = (QRectF(event.buttonDownPos(Qt.LeftButton),
                           event.pos()).normalized())

            if not rect.width():
                rect = rect.adjusted(-1e-7, -1e-7, 1e-7, 1e-7)

            rect = rect.intersected(self.contentsRect())
            self.__selectionRect.setRect(rect)
            self.__selstate.rect = rect
            self.__selstate.action |= SelectAction.Current

            self.__setSelectionRect(rect, self.__selstate.action)
            event.accept()

    def mouseReleaseEvent(self, event):
        # Reimplemented
        if event.button() == Qt.LeftButton:
            if self.__selectionRect is not None:
                self.__selectionRect.setParentItem(None)
                if self.scene() is not None:
                    self.scene().removeItem(self.__selectionRect)
                self.__selectionRect = None
            event.accept()

            rect = (QRectF(event.buttonDownPos(Qt.LeftButton), event.pos())
                    .normalized())

            if not rect.isValid():
                rect = rect.adjusted(-1e-7, -1e-7, 1e-7, 1e-7)

            rect = rect.intersected(self.contentsRect())
            action = self.__selstate.action & ~SelectAction.Current
            self.__setSelectionRect(rect, action)
            self.__selstate = None

    def __move_selection(self, selection, offset):
        ids = np.asarray([pi.data(0) for pi in self.__plotItems()]).ravel()
        indices = [np.where(ids == i)[0] for i in selection]
        indices = np.asarray(indices) + offset
        if min(indices) >= 0 and max(indices) < len(ids):
            self.setSelection(ids[indices])

    def __setSelectionRect(self, rect, action):
        # Set the current mouse drag selection rectangle
        if not rect.isValid():
            rect = rect.adjusted(-0.01, -0.01, 0.01, 0.01)

        rect = rect.intersected(self.contentsRect())

        indices = self.__selectionIndices(rect)

        if action & SelectAction.Clear:
            selection = []
        elif self.__selstate is not None:
            # Mouse drag selection is in progress. Update only the current
            # selection
            selection = self.__selstate.selection
        else:
            selection = self.__selection

        if action & SelectAction.Toogle:
            selection = np.setxor1d(selection, indices)
        elif action & SelectAction.Deselect:
            selection = np.setdiff1d(selection, indices)
        elif action & SelectAction.Select:
            selection = np.union1d(selection, indices)

        self.setSelection(selection)

    def __selectionIndices(self, rect):
        items = [item for item in self.__plotItems()
                 if item.geometry().intersects(rect)]
        selection = [np.array([], dtype=int)]
        for item in items:
            indices = item.data(0)
            itemrect = item.geometry().intersected(rect)
            crect = item.contentsRect()
            itemrect = (item.mapFromParent(itemrect).boundingRect()
                        .intersected(crect))
            assert itemrect.top() >= 0
            rowh = crect.height() / item.count()
            indextop = np.floor(itemrect.top() / rowh)
            indexbottom = np.ceil(itemrect.bottom() / rowh)
            selection.append(indices[int(indextop): int(indexbottom)])
        return np.hstack(selection)

    def itemAtPos(self, pos):
        items = [item for item in self.__plotItems()
                 if item.geometry().contains(pos)]
        if not items:
            return None
        else:
            item = items[0]
        crect = item.contentsRect()
        pos = item.mapFromParent(pos)
        if not crect.contains(pos):
            return None

        assert pos.x() >= 0
        rowh = crect.height() / item.count()
        index = int(np.floor(pos.y() / rowh))
        index = min(index, item.count() - 1)
        if index >= 0:
            return item.items()[index]
        else:
            return None

    def indexAtPos(self, pos):
        items = [item for item in self.__plotItems()
                 if item.geometry().contains(pos)]
        if not items:
            return -1
        else:
            item = items[0]
        indices = item.data(0)
        assert (isinstance(indices, np.ndarray) and
                indices.shape == (item.count(),))
        crect = item.contentsRect()
        pos = item.mapFromParent(pos)
        if not crect.contains(pos):
            return -1

        assert pos.x() >= 0
        rowh = crect.height() / item.count()
        index = np.floor(pos.y() / rowh)
        index = min(index, indices.size - 1)

        if index >= 0:
            return indices[index]
        else:
            return -1

    def __selectionChanged(self, selected, deselected):
        for item, grp in zip(self.__plotItems(), self.__groups):
            select = np.flatnonzero(
                np.in1d(grp.indices, selected, assume_unique=True))
            items = item.items()
            if select.size:
                for i in select:
                    color = np.hstack((grp.color, np.array([130])))
                    items[i].setBrush(QBrush(QColor(*color)))

            deselect = np.flatnonzero(
                np.in1d(grp.indices, deselected, assume_unique=True))
            if deselect.size:
                for i in deselect:
                    items[i].setBrush(QBrush(QColor(*grp.color)))

    def __plotItems(self):
        for i in range(len(self.__groups)):
            item = self.layout().itemAt(i + 1, 2)
            if item is not None:
                assert isinstance(item, BarPlotItem)
                yield item

    def __textItems(self):
        for i in range(len(self.__groups)):
            item = self.layout().itemAt(i + 1, 3)
            if item is not None:
                assert isinstance(item, TextListWidget)
                yield item

    def setSelection(self, indices):
        indices = np.unique(np.asarray(indices, dtype=int))
        select = np.setdiff1d(indices, self.__selection)
        deselect = np.setdiff1d(self.__selection, indices)

        self.__selectionChanged(select, deselect)

        self.__selection = indices

        if deselect.size or select.size:
            self.selectionChanged.emit()

    def selection(self):
        return np.asarray(self.__selection, dtype=int)


class Line(QGraphicsWidget):
    """
    A line separator graphics widget
    """
    def __init__(self, parent=None, orientation=Qt.Horizontal, **kwargs):
        sizePolicy = kwargs.pop("sizePolicy", None)
        super().__init__(None, **kwargs)
        self.__orientation = Qt.Horizontal
        if sizePolicy is None:
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sizePolicy.setControlType(QSizePolicy.Frame)
            self.setSizePolicy(sizePolicy)
        else:
            self.setSizePolicy(sizePolicy)

        self.setOrientation(orientation)

        if parent is not None:
            self.setParentItem(parent)

    def setOrientation(self, orientation):
        if self.__orientation != orientation:
            self.__orientation = orientation
            sp = self.sizePolicy()
            if orientation == Qt.Vertical:
                sp.setVerticalPolicy(QSizePolicy.Expanding)
                sp.setHorizontalPolicy(QSizePolicy.Fixed)
            else:
                sp.setVerticalPolicy(QSizePolicy.Fixed)
                sp.setHorizontalPolicy(QSizePolicy.Expanding)
            self.setSizePolicy(sp)
            self.updateGeometry()

    def sizeHint(self, which, constraint=QRectF()):
        # type: (Qt.SizeHint, QSizeF) -> QSizeF
        pw = 1.
        sh = QSizeF()
        if which == Qt.MinimumSize:
            sh = QSizeF(pw, pw)
        elif which == Qt.PreferredSize:
            sh = QSizeF(pw, 30.)
        elif which == Qt.MaximumSize:
            sh = QSizeF(pw, QWIDGETSIZE_MAX)

        if self.__orientation == Qt.Horizontal:
            sh.transpose()  # Qt4 compatible
        return sh

    def paint(self, painter, option, widget=None):
        # type: (QPainter, QStyleOptionGraphicsItem, Optional[QWidget]) -> None
        palette = option.palette  # type: QPalette
        role = QPalette.WindowText
        if widget is not None:
            role = widget.foregroundRole()
        color = palette.color(role)
        painter.setPen(QPen(color, 1))
        rect = self.contentsRect()
        center = rect.center()
        if self.__orientation == Qt.Vertical:
            p1 = QPointF(center.x(), rect.top())
            p2 = QPointF(center.x(), rect.bottom())
        elif self.__orientation == Qt.Horizontal:
            p1 = QPointF(rect.left(), center.y())
            p2 = QPointF(rect.right(), center.y())
        else:
            assert False
        painter.drawLine(p1, p2)


class BarPlotItem(QGraphicsWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.__barsize = 5
        self.__spacing = 1
        self.__pen = QPen(Qt.NoPen)
        self.__brush = QBrush(QColor("#3FCFCF"))
        self.__range = (0., 1.)
        self.__data = np.array([], dtype=float)
        self.__items = []

    def count(self):
        return self.__data.size

    def items(self):
        return list(self.__items)

    def setGeometry(self, geom):
        super().setGeometry(geom)
        self.__layout()

    def event(self, event):
        if event.type() == QEvent.GraphicsSceneResize:
            self.__layout()
        return super().event(event)

    def sizeHint(self, which, constraint=QSizeF()):
        return QSizeF(300, (self.__barsize + self.__spacing) * self.count())

    def setPreferredBarSize(self, size):
        if self.__barsize != size:
            self.__barsize = size
            self.updateGeometry()

    def spacing(self):
        return self.__spacing

    def setPen(self, pen):
        pen = QPen(pen)
        if self.__pen != pen:
            self.__pen = pen
            for item in self.__items:
                item.setPen(pen)

    def pen(self):
        return QPen(self.__pen)

    def setBrush(self, brush):
        brush = QBrush(brush)
        if self.__brush != brush:
            self.__brush = brush
            for item in self.__items:
                item.setBrush(brush)

    def brush(self):
        return QBrush(self.__brush)

    def setPlotData(self, values):
        self.__data = np.array(values, copy=True)
        self.__update()
        self.updateGeometry()

    def setDataRange(self, rangemin, rangemax):
        if self.__range != (rangemin, rangemax):
            self.__range = (rangemin, rangemax)
            self.__layout()

    def __clear(self):
        for item in self.__items:
            item.setParentItem(None)
        scene = self.scene()
        if scene is not None:
            for item in self.__items:
                scene.removeItem(item)
        self.__items = []

    def __update(self):
        self.__clear()

        pen = self.pen()
        brush = self.brush()
        for _ in range(self.count()):
            item = QGraphicsRectItem(self)
            item.setPen(pen)
            item.setBrush(brush)
            self.__items.append(item)

        self.__layout()

    def __layout(self):
        (N, ) = self.__data.shape
        if not N:
            return

        spacing = self.__spacing
        rect = self.contentsRect()
        w = rect.width()
        if rect.height() - (spacing * (N - 1)) <= 0:
            spacing = 0

        h = (rect.height() - (spacing * (N - 1))) / N
        xmin, xmax = self.__range
        span = xmax - xmin
        if span < 1e-9:
            span = 1
        scalef = w * 1 / span

        base = 0
        base = (base - xmin) * scalef
        datascaled = (self.__data - xmin) * scalef

        for i, (v, item) in enumerate(zip(datascaled, self.__items)):
            item.setRect(QRectF(base, rect.top() + i * (h + spacing),
                                v - base, h).normalized())


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWSilhouettePlot).run(Orange.data.Table("iris"))
