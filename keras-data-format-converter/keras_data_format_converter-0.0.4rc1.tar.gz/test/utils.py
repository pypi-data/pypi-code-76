from typing import Callable

import numpy as np
import pytest
import tensorflow as tf
from tensorflow.keras import backend as K

from keras_data_format_converter import convert_channels_first_to_last, convert_channels_last_to_first


def convert_and_assert(model_generator: Callable, data_format: str, test_infer: bool):
    if test_infer and not tf.test.gpu_device_name():
        pytest.skip("Skip! tensorflow supports the channels first format only on the GPU")
    # Arrange model and input sample
    K.set_image_data_format(data_format)
    model = model_generator()
    input_shape = model.input_shape
    input_shape = [1, *input_shape[1:]]
    input_np = np.random.uniform(0, 1, input_shape)
    transposed_inputs = [inp.name for inp in model.inputs]

    axes = list(range(len(input_shape)))
    # Action: Convert data_format of model
    if data_format == "channels_last":
        converted_model = convert_channels_last_to_first(model, transposed_inputs, verbose=False)
        axes = [axes[0], axes[-1], *axes[1:-1]]
        converted_input = np.transpose(input_np, axes)
    else:
        converted_model = convert_channels_first_to_last(model, transposed_inputs, verbose=False)
        axes = [axes[0], *axes[2:], axes[1]]
        converted_input = np.transpose(input_np, axes)

    # Since tensorflow Conv2D op currently only supports only the NHWC tensor format on the CPU
    if test_infer:
        converted_output = converted_model(converted_input)
        output = model(input_np)
        # Assert converted model is computing equally
        assert np.allclose(output, converted_output)
