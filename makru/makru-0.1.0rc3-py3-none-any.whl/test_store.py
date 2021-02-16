from .store import Store, Table


class TestStore:
    def test_store_can_open_in_memory_sqlite3_database(self):
        store = Store(":memory:")  # :memory: means open a in-memory database
        store.get_table("example")

    def test_store_can_remove_table(self):
        store = Store(":memory:")
        t = store.get_table("example")
        t.set("value1", "yah")
        assert t.get("value1") == "yah"
        store.remove_table("example")
        store.get_table("example")
        assert t.get("value1") == None

    def test_store_can_remove_table_even_when_table_does_not_exists(self):
        store = Store(":memory:")
        store.remove_table("this_table_does_not_exists")


def get_table(table_name):
    store = Store(":memory:")
    return store.get_table(table_name)


class TestTable:
    def test_table_could_set_values(self):
        t = get_table("example")
        t.set("value1", "ok")
        t.set("value2", "ok")

    def test_table_could_get_values(self):
        t = get_table("example")
        t.set("value1", "ok")
        assert t.get("value1") == "ok"

    def test_table_could_return_none_if_non_defined(self):
        t = get_table("example")
        assert t.get("unset_value") == None

    def test_table_remove_the_pair_when_value_sets_none(self):
        t = get_table("example")
        t.set("value1", "ok")
        assert t.get("value1") == "ok"
        t.set("value1", None)
        assert t.get("value1") == None
