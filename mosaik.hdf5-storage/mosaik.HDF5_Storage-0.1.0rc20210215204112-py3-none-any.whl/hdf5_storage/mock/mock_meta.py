from mosaik_hdf5_storage.hdf5_storage.mock.mock_model import MockModel

MOCK_META: dict = {
    'models': {
        MockModel.__name__: {
            'public': True,
            'params': [
            ],
            'attrs': [
            ],
        },
    },
}
