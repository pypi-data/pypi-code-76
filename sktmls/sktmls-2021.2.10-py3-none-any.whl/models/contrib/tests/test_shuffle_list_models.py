from sktmls.models.contrib import ShuffleListModel, PeriodicShuffleListModel


class TestShuffleListModel:
    def test_000_shuffle_list(self):
        slm = ShuffleListModel("test_model", "test_version", "item001", "item001_name", ["h", "e", "l", "o", "w"])

        results = slm.predict(None)
        assert "items" in results
        items = results["items"][0]

        assert items.get("id") == "item001"
        assert items.get("name") == "item001_name"
        assert "props" in items
        assert type(items.get("props").get("item001")) == list
        assert set(items.get("props").get("item001")) == {"h", "e", "l", "o", "w"}


class TestPeriodicShuffleListModel:
    def test_000_periodic_shuffle_list(self):
        slm = PeriodicShuffleListModel(
            "test_model", "test_version", "item001", "item001_name", ["h", "e", "l", "o", "w"], "daily"
        )

        results = slm.predict("1234567890")
        assert "items" in results
        items = results["items"][0]

        assert items.get("id") == "item001"
        assert items.get("name") == "item001_name"
        assert "props" in items
        assert type(items.get("props").get("item001")) == list
        assert set(items.get("props").get("item001")) == {"h", "e", "l", "o", "w"}

        second_results = slm.predict("1234567890")
        second_items = second_results["items"][0]
        assert items.get("props").get("item001") == second_items.get("props").get("item001")
