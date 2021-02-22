import pytest

from sktmls.models import MLSModelError
from sktmls.models.contrib import MbrCategoryBaselineModel


class TestMbrCategoryBaselineModel:
    def test_000_mbr_baseline_1(self):
        mbm = MbrCategoryBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=["user_id", "available_benefit_pizza", "used_datediff_pizza"],
            item_type="test_type",
            context_id="test_context",
            num_pick=1,
        )

        results = mbm.predict(["1234567890", ["2234", "2308", "2306", "2286"], 37])
        assert len(results["items"]) == 1

        item = results["items"][0]
        assert item["id"] in ["2234", "2308", "2306", "2286"]
        assert item["name"] == "#"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] == "test_context"
        assert item["props"]["category_use_yn"] == "Y"

    def test_001_mbr_baseline_2(self):
        mbm = MbrCategoryBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=["user_id", "available_benefit_pizza", "used_datediff_pizza"],
            item_type="test_type",
            context_id="test_context",
            num_pick=2,
        )

        results = mbm.predict(["1234567890", ["2234", "2308", "2306", "2286"], 37])
        assert len(results["items"]) == 2

        item = results["items"][0]
        assert item["id"] in ["2234", "2308", "2306", "2286"]
        assert item["name"] == "#"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] == "test_context"
        assert item["props"]["category_use_yn"] == "Y"

        item = results["items"][1]
        assert item["id"] in ["2234", "2308", "2306", "2286"]
        assert item["name"] == "#"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] == "test_context"
        assert item["props"]["category_use_yn"] == "Y"

    def test_002_mbr_baseline_false_use_yn(self):
        mbm = MbrCategoryBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=["user_id", "available_benefit_pizza", "used_datediff_pizza"],
            item_type="test_type",
            context_id="test_context",
            num_pick=1,
        )

        results = mbm.predict(["1234567890", ["2234", "2308", "2306", "2286"], 1000])
        assert len(results["items"]) == 1

        item = results["items"][0]
        assert item["id"] in ["2234", "2308", "2306", "2286"]
        assert item["name"] == "#"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] == "test_context"
        assert item["props"]["category_use_yn"] == "N"

    def test_003_mbr_baseline_none_benefit(self):
        mbm = MbrCategoryBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=["user_id", "available_benefit_pizza", "used_datediff_pizza"],
            item_type="test_type",
            context_id="test_context",
            num_pick=1,
        )

        results = mbm.predict(["1234567890", None, 37])
        assert len(results["items"]) == 0

    def test_004_mbr_baseline_invalid_benefit(self):
        mbm = MbrCategoryBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=["user_id", "available_benefit_pizza", "used_datediff_pizza"],
            item_type="test_type",
            context_id="test_context",
            num_pick=1,
        )

        with pytest.raises(MLSModelError):
            mbm.predict(["1234567890", 100, 37])
