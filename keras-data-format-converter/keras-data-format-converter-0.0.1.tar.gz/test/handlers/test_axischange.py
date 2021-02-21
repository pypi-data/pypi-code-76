import pytest
from tensorflow.python.keras.layers import BatchNormalization

from keras_data_format_converter.layers.confighandlers.axischange import handle_axis_change


@pytest.mark.parametrize("transposable,data_format,expected", [(True, "channels_last", -1), (True, "channels_first", 1),
                                                               (False, "channels_last", -1),
                                                               (False, "channels_first", -1)])
def test_axischange(transposable, data_format, expected):
    # Arrange
    layer = BatchNormalization()
    layer_config = layer.get_config()

    # Action handle config
    new_config = handle_axis_change(data_format, transposable, layer_config)

    # Assert
    assert new_config["axis"] == expected
