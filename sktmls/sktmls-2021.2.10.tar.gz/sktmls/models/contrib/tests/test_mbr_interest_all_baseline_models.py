import pytest

from sktmls.models import MLSModelError
from sktmls.models.contrib import MbrInterestAllBaselineModel


class TestMbrInterestAllBaselineModel:
    def test_000_mbr_valid_baseline_1(self):
        mbm = MbrInterestAllBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "prefer_category",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            context_id="context",
            num_pick=1,
        )

        results = mbm.predict(["1234567890", ["mbr_beauty"], ["a1", "a2", "a3", "a4"], None, ["b1", "b2", "3", "4"]])
        assert len(results["items"]) == 1

        item = results["items"][0]
        assert item["id"] in ["b1", "b2", "3", "4"]
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] == "context"
        assert item["props"]["prefer_category_yn"] == "Y"
        assert float(item["props"]["score"]) > 1.0

    def test_001_mbr_valid_baseline_2(self):
        mbm = MbrInterestAllBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "prefer_category",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            context_id="context",
            num_pick=2,
        )

        results = mbm.predict(["1234567890", ["mbr_beauty"], ["a1", "a2", "a3", "a4"], None, ["b1", "b2", "3", "4"]])
        assert len(results["items"]) == 2

        item1 = results["items"][0]
        assert item1["id"] in ["b1", "b2", "3", "4"]
        assert item1["type"] == "test_type"
        assert item1["props"]["context_id"] == "context"
        assert item1["props"]["prefer_category_yn"] == "Y"
        assert float(item1["props"]["score"]) > 1.0

        item2 = results["items"][1]
        assert item2["id"] in ["b1", "b2", "3", "4"]
        assert item2["type"] == "test_type"
        assert item2["props"]["context_id"] == "context"
        assert item2["props"]["prefer_category_yn"] == "Y"
        assert float(item2["props"]["score"]) > 1.0

        assert item1["props"]["score"] > item2["props"]["score"]

    def test_002_mbr_valid_baseline_2_prefer_none(self):
        mbm = MbrInterestAllBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "prefer_category",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            context_id="context",
            item_type="test_type",
            num_pick=2,
        )

        results = mbm.predict(["1234567890", ["mbr_beauty"], ["a1", "a2", "a3", "a4"], None, None])
        assert len(results["items"]) == 2

        item1 = results["items"][0]
        assert item1["id"] in ["a1", "a2", "a3", "a4"]
        assert item1["type"] == "test_type"
        assert item1["props"]["context_id"] == "context"
        assert item1["props"]["prefer_category_yn"] == "N"
        assert float(item1["props"]["score"]) < 1.0

        item2 = results["items"][1]
        assert item2["id"] in ["a1", "a2", "a3", "a4"]
        assert item2["type"] == "test_type"
        assert item2["props"]["context_id"] == "context"
        assert item2["props"]["prefer_category_yn"] == "N"
        assert float(item2["props"]["score"]) < 1.0

        assert item1["props"]["score"] > item2["props"]["score"]

    def test_003_mbr_valid_baseline_2_all_none(self):
        mbm = MbrInterestAllBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "prefer_category",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            context_id="context",
            item_type="test_type",
            num_pick=1,
        )

        results = mbm.predict(["1234567890", ["mbr_beauty"], None, None, None])
        assert len(results["items"]) == 0

    def test_004_mbr_valid_baseline_invalid(self):
        mbm = MbrInterestAllBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "prefer_category",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            context_id="context",
            num_pick=1,
        )

        with pytest.raises(MLSModelError):
            mbm.predict(["1234567890", ["mbr_beauty"], ["a1", "a2", "a3", "a4"], None, "good"])

        with pytest.raises(MLSModelError):
            mbm.predict(["1234567890", "good", ["a1", "a2", "a3", "a4"], None, ["b1", "b2", "3", "4"]])
