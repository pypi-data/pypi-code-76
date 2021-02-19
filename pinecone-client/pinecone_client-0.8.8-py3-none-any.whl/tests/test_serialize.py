from pinecone import Service
from pinecone.functions.model.transformer.noop import NoOpTransformer
from pinecone.functions.index.vector.numpy import NumpyIndex


def test_serialize_empty_json():
    app = Service('serialize-me')
    json_str = app.to_json()
    loaded_app = Service.from_json(json_str)
    assert loaded_app.to_json() == json_str


def test_serialize_json():
    app = Service('serialize-me')
    app.append_to_all_paths(NoOpTransformer())
    app.append_to_all_paths(NumpyIndex())
    json_str = app.to_json()
    print(json_str)
    loaded_app = Service.from_json(json_str)
    assert loaded_app.to_json() == json_str
