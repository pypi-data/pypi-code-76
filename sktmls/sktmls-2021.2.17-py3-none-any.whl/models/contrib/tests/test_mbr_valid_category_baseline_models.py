import pytest

from sktmls.models import MLSModelError
from sktmls.models.contrib import MbrValidCategoryBaselineModel


class TestMbrValidCategoryBaselineModel:
    def test_000_mbr_valid_baseline_1(self):
        mbm = MbrValidCategoryBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=1,
        )

        results = mbm.predict(["1234567890", ["a1", "a2", "a3", "a4"], None, ["b1", "b2", "3", "4"]])
        assert len(results["items"]) == 1

        item = results["items"][0]
        assert item["id"] == "test_type"
        assert item["type"] == "test_type"
        assert len(item["props"]["test_type"]) == 1
        assert "mbr_activity" in item["props"]["test_type"] or "mbr_beauty" in item["props"]["test_type"]

    def test_001_mbr_valid_baseline_2(self):
        mbm = MbrValidCategoryBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=2,
        )

        results = mbm.predict(["1234567890", ["a1", "a2", "a3", "a4"], None, ["b1", "b2", "3", "4"]])
        assert len(results["items"]) == 1

        item = results["items"][0]
        assert item["id"] == "test_type"
        assert item["type"] == "test_type"
        assert len(item["props"]["test_type"]) == 2
        assert "mbr_activity" in item["props"]["test_type"] and "mbr_beauty" in item["props"]["test_type"]

    def test_002_mbr_valid_baseline_2_many_none(self):
        mbm = MbrValidCategoryBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=2,
        )

        results = mbm.predict(["1234567890", ["a1", "a2", "a3", "a4"], None, None])
        assert len(results["items"]) == 1

        item = results["items"][0]
        assert item["id"] == "test_type"
        assert item["type"] == "test_type"
        assert len(item["props"]["test_type"]) == 1
        assert "mbr_activity" in item["props"]["test_type"]

    def test_003_mbr_valid_baseline_2_all_none(self):
        mbm = MbrValidCategoryBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=1,
        )

        results = mbm.predict(["1234567890", ["a1"], None, None])
        assert len(results["items"]) == 0

    def test_004_mbr_valid_baseline_invalid(self):
        mbm = MbrValidCategoryBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=1,
        )

        with pytest.raises(MLSModelError):
            mbm.predict(["1234567890", ["a1", "a2", "a3", "a4"], None, "good"])
