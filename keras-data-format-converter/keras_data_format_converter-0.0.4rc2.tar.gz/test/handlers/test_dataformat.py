import pytest
from tensorflow.keras.layers import Conv2D

from keras_data_format_converter.layers.confighandlers.dataformat import handle_data_format


@pytest.mark.parametrize('data_format', ["channels_last", "channels_first"])
def test_handle_data_format(data_format: str):
    # Arrange
    layer = Conv2D(2, 3)
    layer_config = layer.get_config()

    # Action handle config
    new_config = handle_data_format(data_format, layer_config)

    # Assert
    assert new_config["data_format"] == data_format
