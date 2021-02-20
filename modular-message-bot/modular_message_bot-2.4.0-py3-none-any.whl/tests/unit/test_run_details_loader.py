import base64
from unittest.mock import MagicMock, Mock, call, patch

from modular_message_bot.models.job import JobInput, JobOutput, JobPre, JobProcessor
from modular_message_bot.run_details_loader import (
    get_jobs_collection,
    get_run_details,
    get_run_details_config_provider,
    map_job_config,
)

from tests.unit.conftest import get_test_data, get_test_data_yaml


@patch("modular_message_bot.run_details_loader.root_dir")
@patch("modular_message_bot.run_details_loader.dir_files")
@patch("modular_message_bot.run_details_loader.file_contents")
def test_get_run_details_and_co(mock_file_contents: MagicMock, mock_dir_files: MagicMock, mock_root_dir: MagicMock):
    # Tests:
    #   * get_run_details
    #   * get_run_details_list
    #   * get_run_details_from_dir
    #   * run_details_combine

    # Given
    mock_root_dir.return_value = "/root-dir"
    mock_config = Mock()
    mock_config.get.side_effect = [
        base64.b64encode(get_test_data("job-simple-1.yml").encode("utf8")),  # RUN_DETAILS_B64
        "/some/file/here.yml",  # RUN_DETAILS_FILE
        "/some/dir/here",  # RUN_DETAILS_DIR
    ]
    mock_file_contents.side_effect = [
        get_test_data("job-simple-2.yml"),  # RUN_DETAILS_FILE
        get_test_data("job-simple-3.yml"),  # RUN_DETAILS_DIR 1
        get_test_data("job-simple-4.yml"),  # RUN_DETAILS_DIR 2
        get_test_data("job-simple-5.yml"),  # RUN_DETAILS_DIR 3
    ]
    mock_dir_files.return_value = ["job-simple-3.yml", "job-simple-4.yml", "job-simple-5.yml", "skip-me.txt"]

    # When
    result = get_run_details(mock_config)
    result_config = result.get("config", {})
    result_jobs = result.get("jobs", [])

    # Then
    assert len(result_jobs) == 5
    assert result_config == {"a": 1, "b": 2, "c": 3, "z": 5}
    assert result_jobs[0]["id"] == "d946db37-683e-4402-a124-14f9ec70151c"
    assert result_jobs[1]["id"] == "3da75640-646b-47b8-b37e-96f1ab66a63a"
    assert result_jobs[2]["id"] == "f01de261-7b0a-41c3-ad73-d6aadd4a2627"
    assert result_jobs[3]["id"] == "b8e2b9a2-439d-44d0-a87c-1a88080f73ff"
    assert result_jobs[4]["id"] == "ed0af377-078d-4618-81ac-47e9774b4549"
    mock_config.get.assert_has_calls(
        [call("RUN_DETAILS_B64", ""), call("RUN_DETAILS_FILE", ""), call("RUN_DETAILS_DIR", "/root-dir/config")]
    )
    mock_file_contents.assert_has_calls(
        [
            call("/some/file/here.yml"),
            call("/some/dir/here/job-simple-3.yml"),
            call("/some/dir/here/job-simple-4.yml"),
            call("/some/dir/here/job-simple-5.yml"),
        ]
    )


def test_get_run_details_config_provider():
    # Given
    run_details = {"config": {"a": "b", "c": "d"}}

    # When
    result = get_run_details_config_provider(run_details, 1000)

    # Then
    assert result.get_priority() == 1000
    assert result.get_keys() == ["a", "c"]
    assert result.get_value("a") == "b"
    assert result.get_value("c") == "d"


def test_get_jobs_collection():
    # Given
    mock_config = Mock()
    run_details = get_test_data_yaml("job-simple-3.yml")

    # When
    results = get_jobs_collection(mock_config, run_details)

    # Then
    assert len(results.get_all()) == 1


def test_map_job_config():
    # Given
    mock_config = Mock()
    job_config = get_test_data_yaml("job-map.yml")

    # When
    job_result = map_job_config(job_config, mock_config)

    # Then
    assert job_result.id == "444d3161-2b8f-40a7-aaf1-6d49e8003075"
    assert job_result.schedules == ["0 17 * * *", "0 9 * * MON-FRI"]
    assert job_result.vars == {
        "msg_date": "A test at {date}",
        "msg_weather": "Weather is {weather_edi} {weather_license}",
    }

    # Then - Pre
    assert len(job_result.pres) == 1
    assert isinstance(job_result.pres[0], JobPre)
    assert job_result.pres[0].code == "chance"
    assert job_result.pres[0].parameters == {"percentage": 90}

    # Then - Inputs
    assert len(job_result.inputs) == 2
    assert isinstance(job_result.inputs[0], JobInput)
    assert job_result.inputs[0].code == "datetime"
    assert job_result.inputs[0].parameters == {"var": "date", "format": "Week %W (day %j) - %A %B %x"}
    assert isinstance(job_result.inputs[1], JobInput)
    assert job_result.inputs[1].code == "open_weather_city"
    # fmt: off
    assert job_result.inputs[1].parameters == {
        "query": {
            "q": "edinburgh,uk",
            "appid": "a1b2c3",
        },
        "jq-vars": {
            "weather_edi": ".weather[0].description + \" \" + .weather_by"
        }
    }
    # fmt: on

    # Then - Processors
    assert len(job_result.processors) == 1
    assert isinstance(job_result.processors[0], JobProcessor)
    assert job_result.processors[0].code == "regex"
    # fmt: off
    assert job_result.processors[0].parameters == {
        "is-match-abort": False,
        "match": {
            "msg_date": "^A test at",
            "msg_weather_slack": "weather",
            "msg_weather_stdout": "weather",
        }
    }
    # fmt: on

    # Then - Outputs
    assert len(job_result.outputs) == 2
    assert isinstance(job_result.outputs[0], JobOutput)
    assert job_result.outputs[0].code == "stdout"
    assert job_result.outputs[0].parameters == {"message": "{msg_date}"}
    assert job_result.outputs[1].code == "slack"
    assert job_result.outputs[1].parameters == {"message": "{msg_weather}"}


def test_map_job_config_schedule_string():
    # Given
    mock_config = Mock()
    job_config = {"schedule": "0 17 * * *"}

    # When
    job_result = map_job_config(job_config, mock_config)

    # Then
    assert job_result.id == ""
    assert job_result.schedules == ["0 17 * * *"]
    assert job_result.vars == {}

    assert len(job_result.inputs) == 0

    assert len(job_result.outputs) == 0


def test_map_job_config_schedule_missing():
    # Given
    mock_config = Mock()
    job_config = {}

    # When
    job_result = map_job_config(job_config, mock_config)

    # Then
    assert job_result.id == ""
    assert job_result.schedules == []
    assert job_result.vars == {}

    assert len(job_result.inputs) == 0

    assert len(job_result.outputs) == 0
