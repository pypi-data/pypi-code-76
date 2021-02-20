from unittest.mock import MagicMock, Mock, patch

from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractSimpleInputHandler
from modular_message_bot.models.job_run import JobRunVarCollection


class ExampleInputHandler(AbstractSimpleInputHandler):
    # https://stackoverflow.com/questions/24614851/configure-pytest-discovery-to-ignore-class-name
    __test__ = False

    @classmethod
    def get_code(cls) -> str:
        return "test_simple_output_handler"

    def run_input(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        pass


@patch.object(ExampleInputHandler, "run_input")
def test_run(mock_run_input: MagicMock):
    # Given
    parameters = {"a": "b"}
    params_interpolated = {"c": "d"}
    params_with_strings = {"e": "f"}
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_dynamic_config_interpolator.interpolate_dict.return_value = params_interpolated
    mock_job_string_interpolator = Mock()
    mock_job_run_vars_collection = Mock()
    mock_job_run_vars_collection.interpolate_into_parameters.return_value = params_with_strings

    # When
    example_input = ExampleInputHandler(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    example_input.run(parameters, mock_job_run_vars_collection)

    # Then
    mock_run_input.assert_called_with(params_with_strings, mock_job_run_vars_collection)
    mock_dynamic_config_interpolator.interpolate_dict.assert_called_with(parameters)
    mock_job_run_vars_collection.interpolate_into_parameters.assert_called_with(params_interpolated)
