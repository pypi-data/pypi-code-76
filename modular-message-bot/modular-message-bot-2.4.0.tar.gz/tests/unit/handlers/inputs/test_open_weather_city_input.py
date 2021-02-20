from unittest.mock import MagicMock, Mock, call, patch

import pytest

from modular_message_bot.handlers.inputs.open_weather_city_input import OpenWeatherCityInput, weather_slack_icon
from modular_message_bot.models.job_run import JobRunVar

from tests.unit.conftest import get_test_data_json


def test_weather_slack_icon():
    tests = [
        # Specific values (advanced)
        [701, ":droplet:"],
        [711, ":smoking:"],
        [721, ":cloud:"],
        [731, ":dusty_stick:"],
        [741, ":fog:"],
        [751, ":sandwich:"],
        [761, ":dusty_stick:"],
        [762, ":clubs:"],
        [771, ":wind_blowing_face:"],
        [781, ":tornado_cloud:"],
        [800, ":eye:"],
        # Simple values
        [200, ":thunder_cloud_and_rain:"],
        [201, ":thunder_cloud_and_rain:"],
        [299, ":thunder_cloud_and_rain:"],
        [300, ":sweat_drops:"],
        [301, ":sweat_drops:"],
        [399, ":sweat_drops:"],
        [500, ":rain_cloud:"],
        [501, ":rain_cloud:"],
        [599, ":rain_cloud:"],
        [600, ":snow_cloud:"],
        [601, ":snow_cloud:"],
        [699, ":snow_cloud:"],
        [801, ":cloud:"],
        [899, ":cloud:"],
        # Unknown
        [900, ":question:"],
        [901, ":question:"],
        [1000, ":question:"],
        [1, ":question:"],
    ]
    for test in tests:
        test_input = {"weather": [{"id": test[0]}]}
        assert weather_slack_icon(test_input) == test[1]


def test_get_code():
    assert OpenWeatherCityInput.get_code() == "open_weather_city"


def test_validate_job_config():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    # fmt: off
    mock_job_config.parameters = {
         "query": {
             "q": "edinburgh,uk",
             "appid": "a1b2c3",
         },
         "jq-vars": {
             "weather_edi": ".weather[0].description + \" \" + .weather_by"
         }
    }
    # fmt: on

    # When
    module = OpenWeatherCityInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == ""


def test_validate_job_config_no_jq():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    # fmt: off
    mock_job_config.parameters = {
        "query": {
            "q": "edinburgh,uk",
            "appid": "a1b2c3",
        }
    }
    # fmt: on

    # When
    module = OpenWeatherCityInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == "'jq-vars' is required for 'open_weather_city' input"


def test_validate_job_config_no_query_q():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    # fmt: off
    mock_job_config.parameters = {
        "query": {
            "appid": "abcdefg"
        },
        "jq-vars": {
            "weather_edi": ".weather[0].description + \" \" + .weather_by"
        }
    }
    # fmt: on

    # When
    module = OpenWeatherCityInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == "query.'q' is required for 'open_weather_city' input"


def test_validate_job_config_no_query_appid():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    # fmt: off
    mock_job_config.parameters = {
        "query": {
            "q": "edinburgh,uk"
        },
        "jq-vars": {
            "weather_edi": ".weather[0].description + \" \" + .weather_by"
        }
    }
    # fmt: on

    # When
    module = OpenWeatherCityInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == "query.'appid' is required for 'open_weather_city' input"


def test_validate_interpolated_message():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    tests = [
        {
            "message_key": "test1",
            "message_value": "The weather in Edinburgh is Sun Weather by Openweathermap",
            "expected": "",
        },
        {
            "message_key": "test2",
            "message_value": "The weather in Edinburgh is Rain Weather by Openweathermap (openweathermap.org)",
            "expected": "",
        },
        {
            "message_key": "test3",
            "message_value": "The weather in Edinburgh is Fog",
            "expected": "For message 'test3' no weather by blurb present in the output message!",
        },
    ]

    # Then / When
    for test in tests:
        (msg_key, msg_value, expected) = test.values()
        module = OpenWeatherCityInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
        validate = JobRunVar(code=msg_key, value=msg_value, interpolated_by_input_codes=[])
        assert module.validate_job_run_var(validate) == expected


@patch("modular_message_bot.handlers.inputs.open_weather_city_input.logger")
@patch("modular_message_bot.handlers.inputs.open_weather_city_input.requests")
def test_get_values(mock_request: MagicMock, mock_logger: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_request_get = MagicMock()
    mock_request_get.status_code = 200
    mock_request_get.json.return_value = get_test_data_json("response-open-weather-city.json")
    mock_request.get.return_value = mock_request_get
    mock_job_run_vars_collection = Mock()
    # fmt: off
    parameters = {
        "query": {
            "q": "edinburgh,uk",
            "appid": "abcdefg"
        },
        "jq-vars": {
            "weather_simple": '.weather[0].description + " " + .weather_by',
            "weather_complex": '.slack_icon + " " + .weather[0].description + " " + .weather_by_with_link'
        }
    }
    # fmt: on

    # When
    module = OpenWeatherCityInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_input(parameters, mock_job_run_vars_collection)

    # Then
    mock_job_run_vars_collection.interpolate.assert_has_calls(
        [
            call("weather_simple", "broken clouds Weather by Openweathermap", "open_weather_city"),
            call(
                "weather_complex",
                ":cloud: broken clouds Weather by Openweathermap (openweathermap.org)",
                "open_weather_city",
            ),
        ]
    )
    mock_request.get.assert_called_once_with(
        "https://api.openweathermap.org/data/2.5/weather", params={"q": "edinburgh,uk", "appid": "abcdefg"},
    )


@patch("modular_message_bot.handlers.inputs.open_weather_city_input.logger")
@patch("modular_message_bot.handlers.inputs.open_weather_city_input.requests")
def test_get_values_failure(mock_request: MagicMock, mock_logger: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_request_get = MagicMock()
    mock_request_get.status_code = 500
    mock_request_get.content = "Something something error"
    mock_request.get.return_value = mock_request_get
    mock_job_run_vars_collection = Mock()
    # fmt: off
    parameters = {
        "query": {
            "q": "edinburgh,uk",
            "appid": "abcdefg"
        },
        "jq-vars": {
            "weather_simple": '.weather[0].description + " " + .weather_by',
            "weather_complex": '.slack_icon + " " + .weather[0].description + " " + .weather_by_with_link'
        }
    }
    # fmt: on

    # When / Then
    module = OpenWeatherCityInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    with pytest.raises(Exception, match="Open weather failed '500'\n'Something something error'"):
        module.run_input(parameters, mock_job_run_vars_collection)

    # Then
    mock_request.get.assert_called_once_with(
        "https://api.openweathermap.org/data/2.5/weather", params={"q": "edinburgh,uk", "appid": "abcdefg"},
    )
    mock_job_run_vars_collection.interpolate.assert_not_called()


@patch("modular_message_bot.handlers.inputs.open_weather_city_input.logger")
@patch("modular_message_bot.handlers.inputs.open_weather_city_input.requests")
def test_get_values_no_query(mock_request: MagicMock, mock_logger: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_request_get = MagicMock()
    mock_request_get.status_code = 200
    mock_request_get.json.return_value = get_test_data_json("response-open-weather-city.json")
    mock_request.get.return_value = mock_request_get
    mock_job_run_vars_collection = Mock()
    # fmt: off
    parameters = {
        "jq-vars": {
            "weather_simple": '.weather_by',
            "weather_complex": '.weather_by_with_link'
        }
    }
    # fmt: on

    # When
    module = OpenWeatherCityInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_input(parameters, mock_job_run_vars_collection)

    # Then
    mock_job_run_vars_collection.interpolate.assert_has_calls(
        [
            call("weather_simple", "Weather by Openweathermap", "open_weather_city"),
            call("weather_complex", "Weather by Openweathermap (openweathermap.org)", "open_weather_city"),
        ]
    )
    mock_request.get.assert_not_called()
