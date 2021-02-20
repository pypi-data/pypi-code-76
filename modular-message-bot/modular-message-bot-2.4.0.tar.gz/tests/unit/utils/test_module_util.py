from unittest.mock import MagicMock, patch

from modular_message_bot.handlers.inputs.date_time_input import DateTimeInput
from modular_message_bot.handlers.inputs.github_prs_input import GithubPrsInput
from modular_message_bot.handlers.inputs.open_weather_city_input import OpenWeatherCityInput
from modular_message_bot.handlers.inputs.random_message_input import RandomMessageInput
from modular_message_bot.utils.module_util import (
    get_extension,
    get_handler_files,
    get_handler_module_name,
    get_handlers_module_definitions,
    get_module_definition,
)


@patch("modular_message_bot.utils.module_util.import_module")
def test_get_module_definition(mock_import_module: MagicMock):
    # Given

    # When
    result = get_module_definition("modular_message_bot.example.module", "function_name")

    # Then
    assert result == mock_import_module.return_value.function_name


@patch("modular_message_bot.utils.module_util.import_module")
def test_get_module_definition_missing(mock_import_module: MagicMock):
    # Given
    mock_import_module.side_effect = ModuleNotFoundError("Module function_name not found")

    # When / Then
    result = get_module_definition("modular_message_bot.example.module", "function_name")

    # Then
    assert result is None


@patch("modular_message_bot.utils.module_util.import_module")
def test_get_module_function_missing(mock_import_module: MagicMock):
    # Given
    mock_import_module.return_value = {}

    # When / Then
    result = get_module_definition("modular_message_bot.example.module", "function_name")

    # Then
    assert result is None


@patch("modular_message_bot.utils.module_util.get_module_definition")
def test_get_extension(mock_get_module_definition: MagicMock):
    # Given

    # When / Then
    result = get_extension("run_init_extension")

    # Then
    assert result == mock_get_module_definition.return_value
    mock_get_module_definition.assert_called_once_with("modular_message_bot.extension", "run_init_extension")


@patch("modular_message_bot.utils.module_util.dir_files")
@patch("modular_message_bot.utils.module_util.root_dir")
def test_get_handler_files(mock_root_dir: MagicMock, mock_dir_files: MagicMock):
    # Given
    mock_root_dir.return_value = "/some/root/path/here"
    mock_dir_files.return_value = [
        "__init__.py",
        "abstract_input_handler.py",
        "date_time_input.py",
        "github_prs_input.py",
        "open_weather_city_input.py",
        "random_message_input.py",
    ]

    # When
    results = get_handler_files("inputs")

    # Then
    mock_dir_files.assert_called_once_with("/some/root/path/here/modular_message_bot/handlers/inputs")
    assert results == [
        "/some/root/path/here/modular_message_bot/handlers/inputs/date_time_input.py",
        "/some/root/path/here/modular_message_bot/handlers/inputs/github_prs_input.py",
        "/some/root/path/here/modular_message_bot/handlers/inputs/open_weather_city_input.py",
        "/some/root/path/here/modular_message_bot/handlers/inputs/random_message_input.py",
    ]


@patch("modular_message_bot.utils.module_util.root_dir")
def test_get_handler_module_name(mock_root_dir: MagicMock):
    # Given
    mock_root_dir.return_value = "/some/root/path/here"
    test_file = "/some/root/path/here/modular_message_bot/handlers/inputs/github_prs_input.py"

    # When
    result = get_handler_module_name(test_file)

    # Then
    assert result == ("modular_message_bot.handlers.inputs.github_prs_input", "GithubPrsInput")


@patch("modular_message_bot.utils.module_util.dir_files")
@patch("modular_message_bot.utils.module_util.root_dir")
def test_get_handlers_module_definitions(mock_root_dir: MagicMock, mock_dir_files: MagicMock):
    # Given
    mock_root_dir.return_value = "/some/root/path/here"
    mock_dir_files.return_value = [
        "__init__.py",
        "abstract_input_handler.py",
        "date_time_input.py",
        "github_prs_input.py",
        "open_weather_city_input.py",
        "random_message_input.py",
    ]

    # When
    results = get_handlers_module_definitions("inputs")

    # Then
    mock_dir_files.assert_called_once_with("/some/root/path/here/modular_message_bot/handlers/inputs")
    assert len(results) == 4
    assert results[0] == DateTimeInput
    assert results[1] == GithubPrsInput
    assert results[2] == OpenWeatherCityInput
    assert results[3] == RandomMessageInput
