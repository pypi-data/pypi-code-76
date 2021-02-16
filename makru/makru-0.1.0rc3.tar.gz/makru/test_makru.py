from makru import Makru
from makru.helpers import create_makru


class TestMakru:
    def test_search_config_path_should_keep_options_which_not_for_config_path(self):
        options = ["-Ftest1", ":happy", "-Ftest2", ":happy2"]
        Makru.search_config_path(options)
        assert options == [":happy", ":happy2"]

    def test_search_config_path_can_last_path_as_correct_path_when_muiltple_path_options_passed(
        self,
    ):
        options = ["-Ftest1", ":happy", "-Ftest2", ":happy2"]
        path = Makru.search_config_path(options)
        assert path == "test2"
