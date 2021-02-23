import pytest
from tensorflow.keras.layers import Reshape

from keras_data_format_converter.layers.confighandlers.targetshape import handle_transpose_target_shape

# params for testing:
h = 2
w = 6
c = 10

h1 = 4
w1 = 3
c1 = 5
c2 = 5


@pytest.mark.parametrize("data_format,layer_target_shape,expected_target_shape",
                         [
                             ("channels_last", [c, h, w], [h, w, c]),
                             ("channels_first", [h, w, c], [c, h, w]),
                             ("channels_last", [c1, c2, h1, w1], [c2, h1, w1, c1])
                         ])
def test_targetshape(data_format, layer_target_shape, expected_target_shape):
    # Arrange
    layer = Reshape(target_shape=layer_target_shape)
    layer_config = layer.get_config()

    # Action handle config
    new_config = handle_transpose_target_shape(data_format, layer_config)

    # Assert
    assert list(new_config["target_shape"]) == expected_target_shape
