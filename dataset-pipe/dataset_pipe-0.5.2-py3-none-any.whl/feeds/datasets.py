from dataset_pipe.feeds.base import BaseDataSet
from dataset_pipe.readers.csv_reader import csv_reader
from dataset_pipe.readers.json_reader import json_reader


class FileDataset(BaseDataSet):

    def __init__(self, content):

        if content == 'json':
            reader = json_reader
        elif content == 'csv':
            reader = csv_reader
        else:
            raise ValueError("Unknown or not supported content type.")

        super().__init__(reader)


class NumpyDataset(BaseDataSet):

    def __init__(self):

        def _numpy_reader(source):
            for x in source:
                yield x

        super().__init__(_numpy_reader)




# class FileDataset(BaseDataSet):
#
#     def __init__(self, train_file, eval_file, batch,
#                  input_encoder, output_encoder,
#                  skip=0):
#         super().__init__(batch)
#         self.skip = skip
#         self.output_encoder = output_encoder
#         self.input_encoder = input_encoder
#         self.train_file = train_file
#         self.eval_file = eval_file
#         self.train_dataset, self.eval_dataset, self.input_shapes, self.output_shapes = self._get_data()
#
#     def _get_readers(self):
#
#         def _data_reader(file):
#             record = 0
#             while True:
#                 for data in json_reader(file):
#
#                     if self.skip:
#                         record += 1
#                         if record < self.skip:
#                             continue
#
#                     true_title_1 = data[0]
#                     true_title_2 = data[1]
#                     false_title_1 = data[2]
#
#                     """
#                     title,        - trafi do input encoderów
#                     (title, tags) - trafi do outinput encoderów
#                     """
#
#                     yield OrderedDict({
#                         'a': true_title_1,
#                     }), OrderedDict({
#                         'a': 0,
#                     })
#
#         return _data_reader(self.train_file), _data_reader(self.eval_file)
#
#     def _get_data_generators(self):
#         inputs = self.input_encoder
#         outputs = self.output_encoder
#
#         encoders = (inputs, outputs)
#         readers = self._get_readers()
#         return self._get_generators(readers, encoders)