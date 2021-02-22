from sktmls.models.contrib import MbrPopularBenefitModel


class TestMbrPopularBenefitModel:
    def test_000_mbr_valid_1(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "benefit_ranking_weekday_hour_00": ["0", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_01": ["1", "0", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_02": ["2", "1", "0", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_03": ["3", "1", "2", "0", "4", "5", "6"],
                "benefit_ranking_weekday_hour_04": ["4", "1", "2", "3", "0", "5", "6"],
                "benefit_ranking_weekday_hour_05": ["5", "1", "2", "3", "4", "0", "6"],
                "benefit_ranking_weekday_hour_06": ["6", "1", "2", "3", "4", "5", "0"],
                "benefit_ranking_weekday_hour_07": ["7", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_08": ["8", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_09": ["9", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_10": ["10", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_11": ["11", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_12": ["12", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_13": ["13", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_14": ["14", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_15": ["15", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_16": ["16", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_17": ["17", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_18": ["18", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_19": ["19", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_20": ["20", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_21": ["21", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_22": ["22", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_23": ["23", "1", "2", "3", "4", "5", "6"],
            },
        )

        mbm = MbrPopularBenefitModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "sex_cd",
                "age",
                "mbr_card_gr_cd",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            hourly_contexts=[i for i in range(24)],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=1,
        )

        sex_cd = "1"
        age = 32
        mbr_card_gr_cd = "V"
        available_benefit_activity = ["103", "c21", "a3", "b4"]
        available_benefit_asianfood = None
        available_benefit_beauty = ["1", "104", "320"]

        results = mbm.predict(
            [
                "user_id",
                sex_cd,
                age,
                mbr_card_gr_cd,
                available_benefit_activity,
                available_benefit_asianfood,
                available_benefit_beauty,
            ]
        )

        assert len(results["items"]) == 1

        item = results["items"][0]
        assert item["id"] == "1"
        assert item["type"] == "test_type"

    def test_001_mbr_valid_2(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "benefit_ranking_weekday_hour_00": ["0", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_01": ["1", "0", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_02": ["2", "1", "0", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_03": ["3", "1", "2", "0", "4", "5", "6"],
                "benefit_ranking_weekday_hour_04": ["4", "1", "2", "3", "0", "5", "6"],
                "benefit_ranking_weekday_hour_05": ["5", "1", "2", "3", "4", "0", "6"],
                "benefit_ranking_weekday_hour_06": ["6", "1", "2", "3", "4", "5", "0"],
                "benefit_ranking_weekday_hour_07": ["7", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_08": ["8", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_09": ["9", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_10": ["10", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_11": ["11", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_12": ["12", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_13": ["13", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_14": ["14", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_15": ["15", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_16": ["16", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_17": ["17", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_18": ["18", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_19": ["19", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_20": ["20", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_21": ["21", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_22": ["22", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_23": ["23", "1", "2", "3", "4", "5", "6"],
            },
        )

        mbm = MbrPopularBenefitModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "sex_cd",
                "age",
                "mbr_card_gr_cd",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            hourly_contexts=[i for i in range(24)],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=10,
        )

        sex_cd = "1"
        age = 32
        mbr_card_gr_cd = "V"
        available_benefit_activity = ["103", "210", "a3", "4"]
        available_benefit_asianfood = None
        available_benefit_beauty = ["1", "104", "200"]

        results = mbm.predict(
            [
                "user_id",
                sex_cd,
                age,
                mbr_card_gr_cd,
                available_benefit_activity,
                available_benefit_asianfood,
                available_benefit_beauty,
            ]
        )

        assert len(results["items"]) == 2

        item = results["items"][0]
        assert item["type"] == "test_type"

        item = results["items"][1]
        assert item["type"] == "test_type"

    def test_002_mbr_invalid_condition(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "benefit_ranking_weekday_hour_00": ["0", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_01": ["1", "0", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_02": ["2", "1", "0", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_03": ["3", "1", "2", "0", "4", "5", "6"],
                "benefit_ranking_weekday_hour_04": ["4", "1", "2", "3", "0", "5", "6"],
                "benefit_ranking_weekday_hour_05": ["5", "1", "2", "3", "4", "0", "6"],
                "benefit_ranking_weekday_hour_06": ["6", "1", "2", "3", "4", "5", "0"],
                "benefit_ranking_weekday_hour_07": ["7", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_08": ["8", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_09": ["9", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_10": ["10", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_11": ["11", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_12": ["12", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_13": ["13", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_14": ["14", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_15": ["15", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_16": ["16", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_17": ["17", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_18": ["18", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_19": ["19", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_20": ["20", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_21": ["21", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_22": ["22", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_23": ["23", "1", "2", "3", "4", "5", "6"],
            },
        )

        sex_cd = "3"
        age = 32
        mbr_card_gr_cd = "V"

        available_benefit_activity = ["103", "c21", "3", "4"]
        available_benefit_asianfood = None
        available_benefit_beauty = ["a1", "b104", "c20"]

        mbm = MbrPopularBenefitModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "sex_cd",
                "age",
                "mbr_card_gr_cd",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            hourly_contexts=[i for i in range(24)],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=10,
        )

        results = mbm.predict(
            [
                "user_id",
                sex_cd,
                age,
                mbr_card_gr_cd,
                available_benefit_activity,
                available_benefit_asianfood,
                available_benefit_beauty,
            ]
        )

        assert len(results["items"]) == 0

    def test_003_mbr_valid_all_none(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "benefit_ranking_weekday_hour_00": ["0", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_01": ["1", "0", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_02": ["2", "1", "0", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_03": ["3", "1", "2", "0", "4", "5", "6"],
                "benefit_ranking_weekday_hour_04": ["4", "1", "2", "3", "0", "5", "6"],
                "benefit_ranking_weekday_hour_05": ["5", "1", "2", "3", "4", "0", "6"],
                "benefit_ranking_weekday_hour_06": ["6", "1", "2", "3", "4", "5", "0"],
                "benefit_ranking_weekday_hour_07": ["7", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_08": ["8", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_09": ["9", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_10": ["10", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_11": ["11", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_12": ["12", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_13": ["13", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_14": ["14", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_15": ["15", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_16": ["16", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_17": ["17", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_18": ["18", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_19": ["19", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_20": ["20", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_21": ["21", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_22": ["22", "1", "2", "3", "4", "5", "6"],
                "benefit_ranking_weekday_hour_23": ["23", "1", "2", "3", "4", "5", "6"],
            },
        )

        sex_cd = "1"
        age = 32
        mbr_card_gr_cd = "V"
        available_benefit_activity = ["103", "c21", "a3", "b4"]
        available_benefit_asianfood = None
        available_benefit_beauty = ["a1", "b104", "c20"]

        mbm = MbrPopularBenefitModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "sex_cd",
                "age",
                "mbr_card_gr_cd",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            hourly_contexts=[i for i in range(24)],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=1,
        )

        results = mbm.predict(
            [
                "user_id",
                sex_cd,
                age,
                mbr_card_gr_cd,
                available_benefit_activity,
                available_benefit_asianfood,
                available_benefit_beauty,
            ]
        )

        assert len(results["items"]) == 0
