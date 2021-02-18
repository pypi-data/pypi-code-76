from .DataExporter import DataExporter
from .ObjectExporter import ObjectExporter
import keras
import h5py
from keras.utils.io_utils import load_from_binary_h5py, H5Dict
from keras.engine.saving import _serialize_model, _deserialize_model
from keras.models import model_from_yaml

from ..util.FileWrapper import wrapRead, wrapWrite


from ..storage import Storage

class KerasExporter(ObjectExporter):
    """ An Exporter for keras models"""
    def checkType(self, type):
        return issubclass(type, keras.Model)

    def importData(self, data, options = {}):
        # modelYaml, modelWeights = super(KerasExporter, self).importData(data)
        # model = model_from_yaml(modelYaml)
        # model.set_weights(modelWeights)
        # print(modelWeights)

        # load_model


        def read(path):
            return keras.models.load_model(path)

        return wrapRead(read, data)


    def export(self, model : keras.Model, options = {}):
        # modelYaml = model.to_yaml()
        # modelWeights = model.get_weights()
        # model.save()
        # with H5Dict({}, mode='w') as h5dict:
            # _serialize_model(model, h5dict, True)
        # return super(KerasExporter, self).export(h5dict)
        # def saveToStorage(storage : Storage, path : str):
        #     storage.writeToPath = storage.write
        #     # storage.basePath = path
        #     def saveWrap(data):
        #         storage.write(path, data)
        #     storage.write = saveWrap

        # h5dict = H5Dict({}, mode='w')
        # h5dict = h5py._hl.Group
        def write(path):
            model.save(path)

        return wrapWrite(write)


