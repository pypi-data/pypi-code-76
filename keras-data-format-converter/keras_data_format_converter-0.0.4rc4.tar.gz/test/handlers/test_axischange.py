import pytest
from tensorflow.python.keras.layers import BatchNormalization

from keras_data_format_converter.layers.confighandlers.axischange import handle_axis_change


@pytest.mark.parametrize("data_format,expected", [("channels_last", -1), ("channels_first", 1)])
def test_axischange(data_format, expected):
    # Arrange
    layer = BatchNormalization()
    layer_config = layer.get_config()

    # Action handle config
    new_config = handle_axis_change(data_format, layer_config)

    # Assert
    assert new_config["axis"] == expected
