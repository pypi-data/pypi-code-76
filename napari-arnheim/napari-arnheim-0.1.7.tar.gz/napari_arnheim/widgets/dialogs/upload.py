from napari_arnheim.widgets.dialogs.forms.fields.selectors.models.sample_selector import SampleSelector
from re import A

from PyQt5.QtGui import QStandardItem, QStandardItemModel
from napari_arnheim.widgets.base import BaseMixin, BaseWidget
from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSpinBox, QVBoxLayout, QWidget
from bergen.query import AsyncQuery, QueryList
from grunnlag.schema import Experiment, Representation, RepresentationVariety, Sample
import namegenerator
from qasync import asyncSlot
import xarray as xr
import numpy as np
from napari_arnheim.widgets.dialogs.forms.fields.text_field import TextField
from napari_arnheim.widgets.dialogs.forms.fields.tags_field import TagsField




def createDataArrayFromLayer(layer):

    data = layer.data
    ndim = layer.ndim

    if ndim == 2:
        # first two dimensions is x,y and then channel
        if layer.rgb:
            # We are dealing with an rgb image
            stack = xr.DataArray(data, dims=list("xyc")).expand_dims("z").expand_dims("t").transpose(*list("xyczt"))
        else:
            stack = xr.DataArray(data, dims=list("xy")).expand_dims("c").expand_dims("z").expand_dims("t").transpose(*list("xyczt"))

    if ndim == 3:
        # first three dimensios is z,x,y and then channel?
        if len(data.shape) == 3:
            stack = xr.DataArray(data, dims=list("zxy")).expand_dims("c").expand_dims("t").transpose(*list("xyczt"))
        else:
            raise NotImplementedError("Dont know")

    return stack



class UploadFileDialog(BaseMixin, QDialog):


    def __init__(self, *args, layer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer = layer


        self.representation_name = TextField(parent=self, base=self.base)
        self.tags = TagsField(parent=self, base=self.base, initial=" ")
        self.sample_selector = SampleSelector(parent=self, base=self.base)

        self.formGroupBox = QGroupBox("New Representation")
        layout = QFormLayout()
        layout.addRow(QLabel("Name:"), self.representation_name)
        layout.addRow(QLabel("Tags:"), self.tags)
        layout.addRow(QLabel("Sample:"), self.sample_selector)
        self.formGroupBox.setLayout(layout)


        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.create)
        buttonBox.rejected.connect(self.reject)
        

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        self.setWindowTitle("Create a new Representation")

              

    @asyncSlot()
    async def create(self):
        sampleid = self.sample_selector.getValue()
        name = self.representation_name.getValue()
        tags = self.tags.getValue()

        newarray = createDataArrayFromLayer(self.layer)
        self.created_rep = await Representation.asyncs.from_xarray(newarray, name=name, sample=sampleid, tags=tags, variety=RepresentationVariety.VOXEL)

        self.accept()

    
        




