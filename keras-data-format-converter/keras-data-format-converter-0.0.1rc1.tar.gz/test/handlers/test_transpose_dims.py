from tensorflow.python.keras.layers import Permute

from keras_data_format_converter.layers.confighandlers.dims import handle_transpose_dims


def test_transpose_dims_channels_first_transposable_identity_permutation():
    """running handle_transpose_dims withs dims of Permute layer as identity permutation, expected no change"""
    # Arrange
    data_format = "channels_first"
    dims = [1, 2, 3, 4]
    permute_layer = Permute(dims)
    layer_config = permute_layer.get_config()

    # Action
    new_config = handle_transpose_dims(data_format, layer_config)

    # Assert
    assert new_config["dims"] == layer_config["dims"]


def test_transpose_dims_channels_first_transposable():
    # Arrange
    data_format = "channels_first"
    dims = [2, 1, 4, 3]
    permute_layer = Permute(dims)
    layer_config = permute_layer.get_config()

    # Action
    new_config = handle_transpose_dims(data_format, layer_config)

    # Assert
    assert new_config["dims"] == [4, 3, 2, 1]


def test_transpose_dims_channels_last_transposable_identity_permutation():
    """running handle_transpose_dims withs dims of Permute layer as identity permutation, expected no change"""
    # Arrange
    data_format = "channels_last"
    dims = [1, 2, 3, 4]
    permute_layer = Permute(dims)
    layer_config = permute_layer.get_config()

    # Action
    new_config = handle_transpose_dims(data_format, layer_config)

    # Assert
    assert new_config["dims"] == layer_config["dims"]


def test_transpose_dims_channels_last_transposable():
    # Arrange
    data_format = "channels_last"
    dims = [4, 3, 2, 1]
    permute_layer = Permute(dims)
    layer_config = permute_layer.get_config()

    # Action
    new_config = handle_transpose_dims(data_format, layer_config)

    # Assert
    assert new_config["dims"] == [2, 1, 4, 3]
