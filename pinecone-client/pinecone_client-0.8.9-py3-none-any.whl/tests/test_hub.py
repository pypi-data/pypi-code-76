import argparse

from pinecone.functions import model
from pinecone.functions.model.scorer.hub import HubScorer
from pinecone.functions.model.transformer.hub import HubTransformer
from pinecone.functions.model.scorer.dot import DotScorer
from pinecone.utils import get_version

import numpy as np
import pytest

SAMPLE_DATA = [np.array([2, 3, 4])]*2, [[np.array([2,3,4])]*5]*2


@pytest.mark.asyncio
async def test_predict():
    model = HubScorer(f'dotscorer:{get_version()}')

    with model:  # spins up model container locally
        predictions = list(await model.score(*SAMPLE_DATA))

    assert len(predictions) == 2
    assert len(list(predictions[0])) == 5


def test_native():
    model = DotScorer()
    assert len(list(model.score(*SAMPLE_DATA))) == 2

    request = HubScorer.build_request(*SAMPLE_DATA)
    assert len(request.query.matches) == 2
    assert request.query.matches[0].data.shape[0] == 5


@pytest.mark.asyncio
async def test_transform():
    model = HubTransformer(f'nooptransformer:{get_version()}')
    with model:
        transformations = list(await model.transform_vectors(np.array(SAMPLE_DATA[0])))
    assert len(transformations) == 2
    assert len(list(transformations[0])) == 3


def test_hubfunction_image():
    name = "test-abc-image"
    hf = model.HubFunction(image=name)
    assert name == hf.image

    parser = argparse.ArgumentParser()
    model.HubFunction.add_args(parser)
    hf2 = model.HubFunction.from_args(parser.parse_args(hf.to_args()))
    assert name == hf2.image


def test_hubfunction_replicas():
    name = "test-abc-image"
    replicas = 2
    hf = model.HubFunction(image=name, replicas=replicas)
    assert hf.replicas == replicas
    parser = argparse.ArgumentParser()
    model.HubFunction.add_args(parser)
    hf2 = model.HubFunction.from_args(parser.parse_args(hf.to_args()))
    assert replicas == hf2.replicas


@pytest.mark.asyncio
async def test_transformer_replicas():
    replicas = 2
    model = HubTransformer(f'nooptransformer:{get_version()}', replicas=2)
    assert model.replicas == replicas
    parser = argparse.ArgumentParser()
    HubTransformer.add_args(parser)
    model2 = HubTransformer.from_args(parser.parse_args(model.to_args()))
    assert replicas == model2.replicas
