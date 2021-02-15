import pytest

import numpy as np

import lightgbm

from sktmls.models.contrib import LightGBMRandomContextModel


class TestLightGBMRandomContextModels:
    @pytest.fixture(scope="class")
    def param(self):
        return {
            "model": LightGBMRandomContextModel(
                model=lightgbm.basic.Booster(train_set=lightgbm.Dataset(np.array([[1, 2]]), np.array([1]))),
                model_name="test_model",
                model_version="test_version",
                model_features=["feature1", "feature2", "feature3", "feature4"],
                default_feature_values=["3", 1, "A", 100],
                context_features=["feature5", "feature2"],
                context_values=["context_1", "context_2"],
                default_context_value="default_context",
                cutoff=0.3,
                item_id="id",
                item_name="name",
                item_type="type",
            )
        }

    def test_000_lightgbm_random_context_return(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.2]))
        assert param.get("model").predict([0, 0, 0, 0, "Y", "Y"]) == {"items": []}

    def test_001_lightgbm_random_context_return(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.8]))
        assert param.get("model").predict([999, 999, 999, 999, "N", "N"]) == {
            "items": [
                {
                    "id": "id",
                    "name": "name",
                    "type": "type",
                    "props": {"score": 0.8, "context_id": "default_context"},
                }
            ]
        }

    def test_002_lightgbm_random_context_return(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.8]))

        results = param.get("model").predict([999, 999, 999, 999, "Y", "N"])

        assert "items" in results
        items = results["items"][0]

        assert "props" in items
        props = items.pop("props")

        assert items == {
            "id": "id",
            "name": "name",
            "type": "type",
        }

        assert props.get("score") == 0.8
        assert props.get("context_id") in ["context_1", "context_2"]

    def test_003_lightgbm_random_context_return(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.8]))

        results = param.get("model").predict([999, 999, 999, 999, "N", "Y"])

        assert "items" in results
        items = results["items"][0]

        assert "props" in items
        props = items.pop("props")

        assert items == {
            "id": "id",
            "name": "name",
            "type": "type",
        }

        assert props.get("score") == 0.8
        assert props.get("context_id") in ["context_1", "context_2"]

    def test_004_lightgbm_random_context_return(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.8]))

        results = param.get("model").predict([999, 999, 999, 999, "Y", "N"])

        assert "items" in results
        items = results["items"][0]

        assert "props" in items
        props = items.pop("props")

        assert items == {
            "id": "id",
            "name": "name",
            "type": "type",
        }

        assert props.get("score") == 0.8
        assert props.get("context_id") in ["context_1", "context_2"]
