import pytest

import numpy as np

import lightgbm

from sktmls.models import MLSModelError
from sktmls.models.contrib import FeeNoEquipSingleEmbModel


class TestFeeNoEquipSingleEmbModels:
    @pytest.fixture(scope="class")
    def param(self):
        return {
            "model": FeeNoEquipSingleEmbModel(
                model=lightgbm.basic.Booster(train_set=lightgbm.Dataset(np.array([[1, 2]]), np.array([1]))),
                model_name="test_model",
                model_version="test_version",
                model_features=[
                    "age",
                    "bas_fee_amt",
                    "filter_five_g",
                    "additional_svc_ansim_option_scrb_type",
                    "embedding_vector",
                ],
                default_feature_values=[30, 100000, "Y", "free", [0.1, 0.2, 0.3, 0.4]],
                default_context_value="context_default",
                emb_feature_indices=[0, 2],
                conversion_formulas={
                    "additional_svc_ansim_option_scrb_type": {"map": {"free": 1, "paid": 2}, "default": 0},
                    "age": {"conditions": [(">", 0), ("<", 100)], "default": 30},
                },
                context_features=["filter_tfamilymoa", "context_data_overuse", "app_use_traffic_music_ratio_median_yn"],
                context_values=["tfamilymoa_value", "overuse_value", "music_ratio_value"],
                product_context_indices={
                    "NA00006404": [1, 2],
                    "NA00006536": [0],
                    "NA00006537": [0, 1],
                    "NA00006539": [0, 1, 2],
                },
            )
        }

    def test_000_no_rec_y(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.0]))
        assert param.get("model").predict([30, 100000, "Y", "free", [0.1, 0.2, 0.3, 0.4], "Y", "Y", "Y"]) == {
            "items": []
        }

    def test_001_no_rec_context(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([10.0]))
        assert param.get("model").predict([10, 100000, "N", "free", [0.1, 0.2, 0.3, 0.4], "Y", "Y", "Y"]) == {
            "items": []
        }
        assert param.get("model").predict([90, 100000, "N", "free", [0.1, 0.2, 0.3, 0.4], "Y", "Y", "Y"]) == {
            "items": []
        }

    def test_002_lte_upsell(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([18.0]))
        assert param.get("model").predict([30, 30000, "N", "free", [0.1, 0.2, 0.3, 0.4], "Y", "Y", "Y"]) == {
            "items": [
                {
                    "id": "NA00006536",
                    "name": "T플랜 안심4G",
                    "type": "fee_no_equip",
                    "props": {"context_id": "tfamilymoa_value"},
                }
            ]
        }

        assert param.get("model").predict([30, 30000, "N", "free", [0.1, 0.2, 0.3, 0.4], "N", "Y", "Y"]) == {
            "items": [
                {
                    "id": "NA00006536",
                    "name": "T플랜 안심4G",
                    "type": "fee_no_equip",
                    "props": {"context_id": "context_default"},
                }
            ]
        }

    def test_003_5g_upsell(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([18.0]))
        assert param.get("model").predict([30, 75000, "Y", "free", [0.1, 0.2, 0.3, 0.4], "Y", "N", "Y"]) == {
            "items": [
                {
                    "id": "NA00006404",
                    "name": "5GX 프라임",
                    "type": "fee_no_equip",
                    "props": {"context_id": "music_ratio_value"},
                }
            ]
        }
        assert param.get("model").predict([30, 75000, "Y", "free", [0.1, 0.2, 0.3, 0.4], "Y", "Y", "N"]) == {
            "items": [
                {
                    "id": "NA00006404",
                    "name": "5GX 프라임",
                    "type": "fee_no_equip",
                    "props": {"context_id": "overuse_value"},
                }
            ]
        }

    def test_004_none(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([18.0]))
        assert param.get("model").predict([30, 75000, None, "free", [0.1, 0.2, 0.3, 0.4], "Y", "N", "N"]) == {
            "items": [
                {
                    "id": "NA00006404",
                    "name": "5GX 프라임",
                    "type": "fee_no_equip",
                    "props": {"context_id": "context_default"},
                }
            ]
        }

    def test_005_invalid_x(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([18.0]))
        with pytest.raises(MLSModelError):
            param.get("model").predict([75000, "Y", "free", [0.1, 0.2, 0.3, 0.4]])
        with pytest.raises(MLSModelError):
            param.get("model").predict([30, 75000, "Y", "free", 0.1])
        with pytest.raises(MLSModelError):
            param.get("model").predict([30, 75000, "Y", "free", [0.1, 0.2, 0.3, 0.4, 0.5]])

    def test_006_conversion(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([18.0]))
        assert param.get("model").predict([20000, 75000, "Y", "paid", [0.1, 0.2, 0.3, 0.4], "Y", "N", "N"]) == {
            "items": [
                {
                    "id": "NA00006404",
                    "name": "5GX 프라임",
                    "type": "fee_no_equip",
                    "props": {"context_id": "context_default"},
                }
            ]
        }
