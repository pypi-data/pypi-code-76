import numpy as np
from catboost import CatBoostClassifier

from sktmls.models.contrib import CatBoostPointwiseRankingModel


class TestCatBoostPointwiseRankingModel:
    def test_000_pointwise(self, mocker):
        cpr = CatBoostPointwiseRankingModel(
            model=CatBoostClassifier(custom_loss=["Accuracy"], random_seed=42, logging_level="Silent"),
            model_name="test_model",
            model_version="test_version",
            point_feature="test_point",
            model_features=["feature1", "feature2", "feature3"],
            context_features=["context1", "context2", "context3"],
            products={
                "PROD001": {"name": "상품001", "context_features": ["context1"], "context_default": "context_default"},
                "PROD002": {
                    "name": "상품002",
                    "context_features": ["context2", "context3"],
                    "context_default": "context_default",
                },
                "PROD003": {"name": "상품003", "context_features": ["context3"], "context_default": "context_age1020"},
                "PROD004": {
                    "name": "상품004",
                    "context_features": ["context1", "context2", "context3"],
                    "context_default": "context_default",
                },
            },
            item_type="test_type",
            cutoff=0.5,
        )

        mocker.patch(
            "catboost.CatBoostClassifier.predict_proba", return_value=np.array([[0.9, 0.1], [0.7, 0.3], [0.3, 0.7]])
        )

        assert cpr.predict([["PROD001", "PROD002", "PROD003"], 4, 5, 6, "Y", "Y", "Y"]) == {
            "items": [{"id": "PROD003", "name": "상품003", "type": "test_type", "props": {"context_id": "context3"}}]
        }

    def test_001_pointwise_not_exists_in_products(self, mocker):
        cpr = CatBoostPointwiseRankingModel(
            model=CatBoostClassifier(custom_loss=["Accuracy"], random_seed=42, logging_level="Silent"),
            model_name="test_model",
            model_version="test_version",
            point_feature="test_point",
            model_features=["feature1", "feature2", "feature3"],
            context_features=["context1", "context2", "context3"],
            products={
                "PROD001": {"name": "상품001", "context_features": ["context1"], "context_default": "context_default"},
                "PROD002": {
                    "name": "상품002",
                    "context_features": ["context2", "context3"],
                    "context_default": "context_default",
                },
                "PROD004": {
                    "name": "상품004",
                    "context_features": ["context1", "context2", "context3"],
                    "context_default": "context_default",
                },
            },
            item_type="test_type",
            cutoff=0.5,
        )

        mocker.patch(
            "catboost.CatBoostClassifier.predict_proba", return_value=np.array([[0.9, 0.1], [0.7, 0.3], [0.3, 0.7]])
        )

        assert cpr.predict([["PROD001", "PROD002", "PROD003"], 4, 5, 6, "Y", "Y", "Y"]) == {
            "items": [{"id": "PROD003", "name": "#", "type": "test_type", "props": {"context_id": "context_default"}}]
        }

    def test_002_pointwise_all_n(self, mocker):
        cpr = CatBoostPointwiseRankingModel(
            model=CatBoostClassifier(custom_loss=["Accuracy"], random_seed=42, logging_level="Silent"),
            model_name="test_model",
            model_version="test_version",
            point_feature="test_point",
            model_features=["feature1", "feature2", "feature3"],
            context_features=["context1", "context2", "context3"],
            products={
                "PROD001": {"name": "상품001", "context_features": ["context1"], "context_default": "context_default"},
                "PROD002": {
                    "name": "상품002",
                    "context_features": ["context2", "context3"],
                    "context_default": "context_default",
                },
                "PROD003": {"name": "상품003", "context_features": ["context3"], "context_default": "context_age1020"},
                "PROD004": {
                    "name": "상품004",
                    "context_features": ["context1", "context2", "context3"],
                    "context_default": "context_default",
                },
            },
            item_type="test_type",
            cutoff=0.5,
        )

        mocker.patch(
            "catboost.CatBoostClassifier.predict_proba", return_value=np.array([[0.9, 0.1], [0.7, 0.3], [0.3, 0.7]])
        )

        assert cpr.predict([["PROD001", "PROD002", "PROD003"], 4, 5, 6, "N", "N", "N"]) == {
            "items": [
                {"id": "PROD003", "name": "상품003", "type": "test_type", "props": {"context_id": "context_age1020"}}
            ]
        }

    def test_003_pointwise_all_cut(self, mocker):
        cpr = CatBoostPointwiseRankingModel(
            model=CatBoostClassifier(custom_loss=["Accuracy"], random_seed=42, logging_level="Silent"),
            model_name="test_model",
            model_version="test_version",
            point_feature="test_point",
            model_features=["feature1", "feature2", "feature3"],
            context_features=["context1", "context2", "context3"],
            products={
                "PROD001": {"name": "상품001", "context_features": ["context1"], "context_default": "context_default"},
                "PROD002": {
                    "name": "상품002",
                    "context_features": ["context2", "context3"],
                    "context_default": "context_default",
                },
                "PROD003": {"name": "상품003", "context_features": ["context3"], "context_default": "context_age1020"},
                "PROD004": {
                    "name": "상품004",
                    "context_features": ["context1", "context2", "context3"],
                    "context_default": "context_default",
                },
            },
            item_type="test_type",
            cutoff=0.5,
        )

        mocker.patch(
            "catboost.CatBoostClassifier.predict_proba", return_value=np.array([[0.9, 0.1], [0.7, 0.3], [0.6, 0.4]])
        )

        assert cpr.predict([["PROD001", "PROD002", "PROD003"], 4, 5, 6, "Y", "Y", "Y"]) == {"items": []}

    def test_004_pointwise_all_in(self, mocker):
        cpr = CatBoostPointwiseRankingModel(
            model=CatBoostClassifier(custom_loss=["Accuracy"], random_seed=42, logging_level="Silent"),
            model_name="test_model",
            model_version="test_version",
            point_feature="test_point",
            model_features=["feature1", "feature2", "feature3"],
            context_features=["context1", "context2", "context3"],
            products={
                "PROD001": {"name": "상품001", "context_features": ["context1"], "context_default": "context_default"},
                "PROD002": {
                    "name": "상품002",
                    "context_features": ["context2", "context3"],
                    "context_default": "context_default",
                },
                "PROD003": {"name": "상품003", "context_features": ["context3"], "context_default": "context_age1020"},
                "PROD004": {
                    "name": "상품004",
                    "context_features": ["context1", "context2", "context3"],
                    "context_default": "context_default",
                },
            },
            item_type="test_type",
            cutoff=0.5,
        )

        mocker.patch(
            "catboost.CatBoostClassifier.predict_proba", return_value=np.array([[0.2, 0.8], [0.2, 0.8], [0.3, 0.7]])
        )

        assert cpr.predict([["PROD001", "PROD002", "PROD003"], 4, 5, 6, "Y", "Y", "Y"]) == {
            "items": [
                {"id": "PROD001", "name": "상품001", "type": "test_type", "props": {"context_id": "context1"}},
                {"id": "PROD002", "name": "상품002", "type": "test_type", "props": {"context_id": "context2"}},
                {"id": "PROD003", "name": "상품003", "type": "test_type", "props": {"context_id": "context3"}},
            ]
        }

    def test_005_pointwise_all_in_num_pick(self, mocker):
        cpr = CatBoostPointwiseRankingModel(
            model=CatBoostClassifier(custom_loss=["Accuracy"], random_seed=42, logging_level="Silent"),
            model_name="test_model",
            model_version="test_version",
            point_feature="test_point",
            model_features=["feature1", "feature2", "feature3"],
            context_features=["context1", "context2", "context3"],
            products={
                "PROD001": {"name": "상품001", "context_features": ["context1"], "context_default": "context_default"},
                "PROD002": {
                    "name": "상품002",
                    "context_features": ["context2", "context3"],
                    "context_default": "context_default",
                },
                "PROD003": {"name": "상품003", "context_features": ["context3"], "context_default": "context_age1020"},
                "PROD004": {
                    "name": "상품004",
                    "context_features": ["context1", "context2", "context3"],
                    "context_default": "context_default",
                },
            },
            item_type="test_type",
            cutoff=0.5,
            num_pick=2,
        )

        mocker.patch(
            "catboost.CatBoostClassifier.predict_proba", return_value=np.array([[0.2, 0.8], [0.2, 0.8], [0.3, 0.7]])
        )

        assert cpr.predict([["PROD001", "PROD002", "PROD003"], 4, 5, 6, "Y", "Y", "Y"]) == {
            "items": [
                {"id": "PROD001", "name": "상품001", "type": "test_type", "props": {"context_id": "context1"}},
                {"id": "PROD002", "name": "상품002", "type": "test_type", "props": {"context_id": "context2"}},
            ]
        }
