from sktmls.models.contrib import RandomScoreModel, PeriodicRandomScoreModel


class TestRandomScoreModel:
    def test_000_random_score(self):
        rsm = RandomScoreModel(
            model_name="test_model", model_version="test_version", item_id="1", item_name="n", item_type="t"
        )

        results = rsm.predict(None)["items"][0]
        assert results["id"] == "1"
        assert results["name"] == "n"
        assert results["type"] == "t"
        assert 0 <= float(results["props"]["score"]) <= 1


class TestPeriodicRandomScoreModel:
    def test_000_periodic_random_score(self):
        rpm = PeriodicRandomScoreModel(
            model_name="test_model",
            model_version="test_version",
            item_id="1",
            item_name="n",
            item_type="t",
            random_cycle="daily",
        )

        result1 = rpm.predict("1234567890")
        result2 = rpm.predict("1234567890")
        assert result1 == result2
