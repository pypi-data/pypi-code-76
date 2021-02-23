import tensorflow as tf

from dataset_pipe.encoder_list import EncoderList
from dataset_pipe.generator import Generator
from collections import OrderedDict


class Dataset:

    def __init__(self, dataset, input_shape, output_shape):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.dataset = dataset

    def __iter__(self):
        return self.dataset.__iter__()

    def batch(self, batch):
        return self.dataset.batch(batch)


class BaseDataSet:

    def __init__(self, reader):

        def _filter(data):
            return {
                       'input': data,
                   }, {
                       'output': data,
                   }

        self.reader = reader
        self.map_lambda = _filter
        self.input_encoder_list = None
        self.output_encoder_list = None

    @staticmethod
    def _get_generator(reader, encoders):
        inputs, outputs = encoders

        return Generator(
            data=reader,
            input_encoders=inputs,
            output_encoders=outputs
        )

    @staticmethod
    def _get_tf_data(generator):
        return tf.data.Dataset.from_generator(
            generator,
            output_types=generator.types(),
            output_shapes=generator.shapes()
        ).repeat().prefetch(-1)

    def feed(self, file) -> Dataset:
        generator = self._get_data_generators(file)

        if self.input_encoder_list and self.output_encoder_list:
            dataset = self._get_tf_data(generator)
        else:
            dataset = generator

        input_shapes, output_shapes = generator.shapes()

        return Dataset(dataset, input_shapes, output_shapes)

    def map(self, map_lambda):
        self.map_lambda = map_lambda
        return self

    def encode(self, input: dict, output: dict):
        self.input_encoder_list = EncoderList(OrderedDict(input))
        self.output_encoder_list = EncoderList(OrderedDict(output))

    def _get_reader(self, file, skip=None):

        def _data_reader(dataset_file):
            record = 0
            while True:
                for data in self.reader(dataset_file):

                    if skip:
                        record += 1
                        if record < skip:
                            continue

                    if self.map_lambda:
                        # yields data via filter
                        filtered_data = self.map_lambda(data)
                        if not isinstance(filtered_data, tuple) or len(filtered_data) != 2:
                            raise ValueError("Filter function must return tuple with 2 arguments: input and output")
                        x, y = filtered_data
                        yield OrderedDict(x), OrderedDict(y)
                    else:
                        yield data

        return _data_reader(file)

    def _get_data_generators(self, file):
        encoders = (self.input_encoder_list, self.output_encoder_list)
        reader = self._get_reader(file)
        return self._get_generator(reader, encoders)
