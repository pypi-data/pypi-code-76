from sktmls.models.contrib import RandomPickModel, PeriodicRandomPickModel


class TestRandomPickModel:
    def test_000_random_pick_1(self):
        rpm = RandomPickModel(
            model_name="test_model",
            model_version="test_version",
            candidates=[
                {"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}},
                {"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}},
            ],
            num_pick=1,
        )

        assert rpm.predict(None) in [
            {"items": [{"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}}]},
            {"items": [{"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}}]},
        ]

    def test_001_random_pick_2(self):
        rpm = RandomPickModel(
            model_name="test_model",
            model_version="test_version",
            candidates=[
                {"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}},
                {"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}},
            ],
            num_pick=2,
        )

        result = rpm.predict(None)
        assert result == {
            "items": [
                {"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}},
                {"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}},
            ]
        } or result == {
            "items": [
                {"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}},
                {"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}},
            ]
        }


class TestPeriodicRandomPickModel:
    def test_000_periodic_random_pick_2(self):
        rpm = PeriodicRandomPickModel(
            model_name="test_model",
            model_version="test_version",
            candidates=[
                {"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}},
                {"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}},
                {"id": "test_id3", "name": "test_name3", "type": "test_type", "props": {}},
                {"id": "test_id4", "name": "test_name4", "type": "test_type", "props": {}},
                {"id": "test_id5", "name": "test_name5", "type": "test_type", "props": {}},
            ],
            num_pick=2,
            random_cycle="daily",
        )

        result1 = rpm.predict("1234567890")
        result2 = rpm.predict("1234567890")
        assert result1 == result2
