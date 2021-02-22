from sktmls.models.contrib import MbrCustomBenefitRandomModel


class TestMbrSimilarBenefitModel:
    def test_000_mbr_valid_1a(self):
        mcbrm = MbrCustomBenefitRandomModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            contexts={"37": ["97", "27", "32", "99", "26", "133", "84", "37", "15", "38", "85", "48", "47", "12"]},
            item_type="test_type",
            random_cycle="hourly",
            num_pick=10,
        )

        results = mcbrm.predict(
            [
                "1234567890",
                ["103", "21", "a3", "a4"],
                None,
                ["48", "104", "20", "4"],
            ]
        )

        assert len(results["items"]) == 1

        item = results["items"][0]
        assert item["id"] == "48"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] == "37"

    def test_001_mbr_valid_none(self):
        mcbrm = MbrCustomBenefitRandomModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            contexts={"10": [], "20": ["10", "11"]},
            item_type="test_type",
            num_pick=10,
        )

        results = mcbrm.predict(
            [
                "1234567890",
                ["103", "21", "a3", "a4"],
                None,
                ["48", "104", "20", "4"],
            ]
        )

        assert len(results["items"]) == 0
