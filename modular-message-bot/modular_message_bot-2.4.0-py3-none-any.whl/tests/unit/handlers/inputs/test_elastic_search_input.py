from unittest.mock import MagicMock, Mock, call

import pytest
from pytest_mock import MockerFixture

from modular_message_bot.handlers.inputs.elastic_search_input import ElasticSearchInput

from tests.unit.conftest import get_test_data, get_test_data_json


@pytest.fixture(autouse=True)
def mock_elasticsearch_definition(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.inputs.elastic_search_input.Elasticsearch")


def test_get_code():
    assert ElasticSearchInput.get_code() == "elasticsearch"


def test_validate_job_config():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    # fmt: off
    mock_job_config.parameters = {
        "connection": {
            "hosts": [{"host": "some_host.example.com", "port": 9200}],
            "http_auth": ["elastic", "changeme"]
        },
        "search": {
            "index": "docker-logs-*",
            # q = Query in the Lucene query string syntax
            "q": "docker.message: error AND NOT docker.container_id: 81f0bb3014f1"
        },
        "jq-vars": {
            "number": ". | .hits.hits | length",
            "details": ". | .hits.hits | map([._source.docker.message] | join(\" - \")) | join(\"\n\")"
        }
    }
    # fmt: on

    # When
    module = ElasticSearchInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == ""


def test_validate_job_config_missing_search():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    # fmt: off
    mock_job_config.parameters = {
        "jq-vars": {
            "number": ". | .hits.hits | length",
        }
    }
    # fmt: on

    # When
    module = ElasticSearchInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert (
        result == "'search' is required for 'elasticsearch' input. See https://elasticsearch-py.readthedocs.io"
        "/en/7.10.0/api.html?highlight=search#elasticsearch.Elasticsearch.search"
    )


def test_run_input(mock_elasticsearch_definition: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_run_vars_collection = Mock()
    # fmt: off
    parameters = {
        "connection": {
            "hosts": [{"host": "some_host.example.com", "port": 9200}],
            "http_auth": ["elastic", "changeme"]
        },
        "search": {
            "index": "docker-logs-*",
            # q = Query in the Lucene query string syntax
            "q": "docker.message: error AND NOT docker.container_id: 81f0bb3014f1"
        },
        "jq-vars": {
            "number": ". | .hits.hits | length",
            "details": ". | .hits.hits | map([._source.\"@timestamp\", ._source.docker.message] | join(\" - \"))"
                       " | join(\"\n\")"
        }
    }
    # fmt: on
    mock_elasticsearch_definition.return_value.search.return_value = get_test_data_json("response-elasticsearch.json")

    # When
    module = ElasticSearchInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_input(parameters, mock_job_run_vars_collection)

    # Then
    expected_details = get_test_data("test_elasticsearch_input---test_run_input---expected-details.txt")
    mock_job_run_vars_collection.interpolate.assert_has_calls(
        [call("number", "10", "elasticsearch"), call("details", expected_details, "elasticsearch")]
    )
