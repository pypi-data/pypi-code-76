


from napari_arnheim.widgets.dialogs.forms.fields.selectors.options_selector import OptionsSelector
from re import A
from napari_arnheim.widgets.tables.pandas_model import PandasModel
from napari_arnheim.widgets.utils import replaceWidgetInLayout
from napari_arnheim.widgets.dialogs.forms.fields.selectors.models.sample_selector import SampleSelector
from napari_arnheim.widgets.dialogs.forms.fields.selectors.models.experiment_selector import ExperimentSelector
from napari_arnheim.widgets.dialogs.forms.fields.text_field import TextField
from grunnlag.schema import Representation
from napari_arnheim.widgets.base import BaseMixin
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QSizePolicy, QTableView, QVBoxLayout, QWidget
from bergen.query import QueryList, AsyncQueryList
from napari_arnheim.widgets.items.representaiton import RepresentationItemWidget
from qasync import QtGui, asyncSlot




class RepresentationSelectorDialog(BaseMixin, QDialog):


    def __init__(self, *args, layer=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.representations = QueryList("""
            query {
                myrepresentations(ordering: "-time") {
                    id
                    name
                    store
                    tags
                }
            }
        """, Representation).run()

        self.sidebar = self.buildSidebar()
        self.list = self.buildList()


        mainLayout = QVBoxLayout(self)

        self.main_widget = QWidget()
        # Central Widget
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.sidebar)
        self.layout.setStretch(0, 30)
        self.layout.addWidget(self.list)
        self.layout.setStretch(1,300)
        self.main_widget.setLayout(self.layout)


        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.create)
        buttonBox.rejected.connect(self.reject)
        

        mainLayout.addWidget(self.main_widget)
        mainLayout.addWidget(buttonBox)
        self.setMinimumHeight(600)
        self.setMinimumWidth(1000)
        self.setLayout(mainLayout)

    def onPressFilter(self, *args):

        values = {
            "sample" : self.sampleSelector.getValue(),
            "experiment": self.experimentSelector.getValue(),
            "tags": self.tagsField.getValue(),
            "ordering": self.orderingSelector.getValue()
        }

        print(values)
        
        self.representations = QueryList("""
            query FilteredMyRepresentations($tags: String,
                $ordering: String,
                $sample: ID,
                $experiment: ID
                ){
                myrepresentations(tags: $tags, ordering:$ordering, sample: $sample, experiment: $experiment) {
                    id
                    name
                    store
                    tags  
                }
            }
        """, Representation).run(variables=values)


        newlist = self.buildList()
        self.layout.replaceWidget(self.list, newlist)
        self.list.close()
        self.list.setParent(None)
        self.list = newlist


    @asyncSlot()
    async def create(self):
        indices = [i.row() for i in self.list.selectedIndexes()]
        self.selected_reps = [self.representations[i] for i in indices]
        self.accept()

    def buildSidebar(self):

        # Filter
        self.filterBox = QGroupBox("Filter")

        self.sampleSelector = SampleSelector(parent=self, base=self.base, with_form=False, add_none=True, on_select=self.onPressFilter)
        self.experimentSelector = ExperimentSelector(parent=self, base=self.base, with_form=False, add_none=True, on_select=self.onPressFilter)
        self.orderingSelector = OptionsSelector(parent=self, base=self.base, options={"-time": "Time (Descending)", "time": "Time (Ascending)"}, on_select=self.onPressFilter)
        self.tagsField = TextField(initial=" ",parent=self, base=self.base, on_select=self.onPressFilter)

        layout = QFormLayout()
        layout.addRow(QLabel("Sample"), self.sampleSelector)
        layout.addRow(QLabel("Experiment"), self.experimentSelector)
        layout.addRow(QLabel("Tags"), self.tagsField)
        layout.addRow(QLabel("Ordering"), self.orderingSelector)
        self.filterBox.setLayout(layout)


        # Filter Button
        self.filterButton = QPushButton("Filter")
        self.filterButton.clicked.connect(self.onPressFilter)


        # The Sidebar
        sidebar = QWidget()

        sidebarlayout = QVBoxLayout()

        sidebarlayout.addWidget(self.filterBox)
        sidebarlayout.addStretch()
        sidebarlayout.addWidget(self.filterButton)

        sidebar.setLayout(sidebarlayout)

        return sidebar


    def buildList(self):
        list = QListWidget()
        list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        for rep in self.representations:

            item = QListWidgetItem(list)
            list.addItem(item)
            repwidget = RepresentationItemWidget(rep, base=self.base)
            item.setSizeHint(repwidget.minimumSizeHint())
            list.setItemWidget(item, repwidget)


        return list


