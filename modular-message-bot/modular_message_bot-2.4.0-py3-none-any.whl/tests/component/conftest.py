import json
import locale
import os
from datetime import datetime
from logging import Logger

import pytest
import yaml
from pytest_mock import MockerFixture
from requests import get as request_get

from modular_message_bot.config.config_collection import ConfigCollection, DictConfigProvider
from modular_message_bot.config.constants import SCHEDULER_TIMEZONE_CFG_KEY


@pytest.fixture(autouse=True)
def setup_locale():
    locale.setlocale(locale.LC_ALL, "en_GB.utf8")
    os.environ["LANG"] = "en_GB.utf8"


class TestingConfigProvider(DictConfigProvider):
    # https://stackoverflow.com/questions/24614851/configure-pytest-discovery-to-ignore-class-name
    __test__ = False

    def __init__(self):
        default_config = {
            SCHEDULER_TIMEZONE_CFG_KEY: "utc",
            "OPEN_WEATHER_KEY": "a1b2c3",
            "SLACK_HOOK_ENDPOINT": "https://slack.example.com",
            "SLACK_HOOK_AUTH": "?a=b&c=d",
            "EASY_HTTP_ENDPOINT": "https://something.example.com/path/here",
            "EASY_HTTP_AUTH_TOKEN": "a1b2c3d4e5",
        }
        priority = 10000
        super().__init__(default_config, "Test Config", priority)

    def add_config_map(self, config_map: dict):
        self.config_map = {**config_map, **self.config_map}

    def add(self, key: str, value: str):
        self.config_map[key] = value

    def set_config_map(self, config_map=None):
        if config_map is None:
            config_map = {}
        self.config_map = config_map


def get_test_data(name: str) -> str:
    resources_folder = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/../component-resources")
    return open(f"{resources_folder}/{name}", "r").read()


def get_test_data_yaml(name: str) -> str:
    return yaml.safe_load(get_test_data(name))


def get_test_data_json(name: str):
    return json.loads(get_test_data(name))


@pytest.fixture(autouse=True)
def mock_get_run_details(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.utils.run_utils.get_run_details")


@pytest.fixture(autouse=True)
def testing_config():
    return TestingConfigProvider()


@pytest.fixture(autouse=True)
def mock_config(mocker: MockerFixture, testing_config: TestingConfigProvider):
    mock = mocker.patch("modular_message_bot.utils.run_utils.build_init_config")
    config = ConfigCollection()
    config.add_provider(testing_config)
    mock.return_value = config
    return mock


# === RUN UTIL ===
@pytest.fixture(autouse=True)
def run_util_get_extension(mocker: MockerFixture):
    mock_get_extension = mocker.patch("modular_message_bot.utils.run_utils.get_extension")
    mock_get_extension.return_value = None
    return mock_get_extension


# === PRES ==================================================================
# --- chance_pre ---
@pytest.fixture(autouse=True)
def mock_pre_chance_random(mocker: MockerFixture):
    mock = mocker.patch("modular_message_bot.handlers.pres.chance_pre.randint")
    mock.return_value = 50
    return mock


@pytest.fixture(autouse=True)
def mock_pre_chance_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.pres.chance_pre.logger")


# === INPUTS ================================================================
# --- datetime_input ---
@pytest.fixture(autouse=True)
def mock_date_time_input_datetime(mocker: MockerFixture):
    mock_dt = mocker.patch("modular_message_bot.handlers.inputs.date_time_input.datetime")
    mock_dt.utcnow.return_value = datetime(2020, 12, 29, 19, 51, 18, 342380)
    return mock_dt


# --- elastic_search_input ---
@pytest.fixture(autouse=True)
def mock_elasticsearch_input_elasticsearch_definition(mocker: MockerFixture):
    mock_es = mocker.patch("modular_message_bot.handlers.inputs.elastic_search_input.Elasticsearch")
    mock_es.return_value.search.return_value = {}
    return mock_es


# --- github_prs_input ---
@pytest.fixture(autouse=True)
def mock_github_prs_input_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.inputs.github_prs_input.logger")


@pytest.fixture(autouse=True)
def mock_github_prs_input_requests_get(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.inputs.github_prs_input.requests_get")


@pytest.fixture(autouse=True)
def mock_github_prs_input_http_basic_auth(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.inputs.github_prs_input.HTTPBasicAuth")


# --- gitlab_merge_requests ---
@pytest.fixture(autouse=True)
def mock_gitlab_merge_requests_input_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.inputs.gitlab_merge_requests_input.logger", spec=Logger)


@pytest.fixture(autouse=True)
def mock_gitlab_merge_requests_input_requests_get(mocker: MockerFixture):
    return mocker.patch(
        "modular_message_bot.handlers.inputs.gitlab_merge_requests_input.requests_get", spec=request_get
    )


# --- random_message ---
@pytest.fixture(autouse=True)
def mock_random_message_input_random_choice(mocker: MockerFixture):
    random_choice = mocker.patch("modular_message_bot.handlers.inputs.random_message_input.random_choice")
    random_choice.side_effect = lambda x: x[0]
    return random_choice


# --- open_weather_city_input ---
@pytest.fixture(autouse=True)
def mock_open_weather_city_input_requests(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.inputs.open_weather_city_input.requests")


# === PROCESSORS ============================================================
# --- regex_match_all_abort_processor ---
@pytest.fixture(autouse=True)
def mock_regex_match_all_abort_processor_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.processors.regex_match_all_abort_processor.logger")


# --- regex_match_all_continue_processor ---
@pytest.fixture(autouse=True)
def mock_regex_match_all_continue_processor_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.processors.regex_match_all_continue_processor.logger")


# --- regex_match_one_abort_processor ---
@pytest.fixture(autouse=True)
def mock_regex_match_one_abort_processor_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.processors.regex_match_one_abort_processor.logger")


# --- regex_match_one_continue_processor ---
@pytest.fixture(autouse=True)
def mock_regex_match_one_continue_processor_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.processors.regex_match_one_continue_processor.logger")


# === OUTPUTS ===============================================================

# --- easy_http_output ---
@pytest.fixture(autouse=True)
def mock_easy_http_output_requests(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.outputs.easy_http_output.requests")


# --- slack_output ---
@pytest.fixture(autouse=True)
def mock_slack_output_requests(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.outputs.slack_output.requests")


# --- stdout_output ---
@pytest.fixture(autouse=True)
def mock_stdout_output_write_to_standard_out(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.outputs.stdout_output.write_to_standard_out")


@pytest.fixture(autouse=True)
def mock_pushover_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.outputs.pushover_output.logger")


@pytest.fixture(autouse=True)
def mock_pushover_request_post(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.outputs.pushover_output.request_post")
