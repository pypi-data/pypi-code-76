import pytest

from sktmls.models import MLSModelError
from sktmls.models.contrib import MbrBoostparkBaselineModel


class TestMbrBoostparkBaselineModel:
    def test_000_mbr_baseline_1(self):
        mbm = MbrBoostparkBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=["user_id", "available_boostpark_location"],
            item_type="test_type",
            num_pick=1,
        )

        results = mbm.predict(
            [
                "1234567890",
                {
                    "available_benefit": ["2234", "2308", "2306", "2286"],
                    "boostpark": "테스트",
                    "context": "로케이션",
                    "location_score": 0.5714,
                },
            ]
        )
        assert len(results["items"]) == 1

        item = results["items"][0]
        assert item["id"] in ["2234", "2308", "2306", "2286"]
        assert item["name"] == "#"
        assert item["type"] == "test_type"
        assert item["props"]["boostpark"] == "테스트"
        assert item["props"]["location_context"] == "로케이션"

    def test_001_mbr_baseline_2(self):
        mbm = MbrBoostparkBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=["user_id", "available_boostpark_location"],
            item_type="test_type",
            num_pick=2,
        )

        results = mbm.predict(
            [
                "1234567890",
                {
                    "available_benefit": ["2234", "2308", "2306", "2286"],
                    "boostpark": "테스트",
                    "context": "로케이션",
                    "location_score": 0.5714,
                },
            ]
        )
        assert len(results["items"]) == 2

        item1 = results["items"][0]
        assert item1["id"] in ["2234", "2308", "2306", "2286"]
        assert item1["name"] == "#"
        assert item1["type"] == "test_type"
        assert item1["props"]["boostpark"] == "테스트"
        assert item1["props"]["location_context"] == "로케이션"

        item2 = results["items"][1]
        assert item2["id"] in ["2234", "2308", "2306", "2286"]
        assert item2["name"] == "#"
        assert item2["type"] == "test_type"
        assert item2["props"]["boostpark"] == "테스트"
        assert item2["props"]["location_context"] == "로케이션"

        assert item1["props"]["score"] >= item2["props"]["score"]

    def test_002_mbr_baseline_invalid(self):
        mbm = MbrBoostparkBaselineModel(
            model_name="test_model",
            model_version="test_version",
            features=["user_id", "available_boostpark_location"],
            item_type="test_type",
            num_pick=1,
        )

        with pytest.raises(MLSModelError):
            mbm.predict(
                [
                    "1234567890",
                    {
                        "boostpark": "테스트",
                        "context": "로케이션",
                        "location_score": 0.5714,
                    },
                ]
            )

        with pytest.raises(MLSModelError):
            mbm.predict(
                [
                    "1234567890",
                    {
                        "available_benefit": [],
                        "boostpark": "테스트",
                        "context": "로케이션",
                        "location_score": 0.5714,
                    },
                ]
            )

        with pytest.raises(MLSModelError):
            mbm.predict(
                [
                    "1234567890",
                    {
                        "available_benefit": ["2234", "2308", "2306", "2286"],
                        "context": "로케이션",
                        "location_score": 0.5714,
                    },
                ]
            )

        with pytest.raises(MLSModelError):
            mbm.predict(
                [
                    "1234567890",
                    {
                        "available_benefit": ["2234", "2308", "2306", "2286"],
                        "boostpark": "테스트",
                        "location_score": 0.5714,
                    },
                ]
            )
