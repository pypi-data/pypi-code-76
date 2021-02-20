from unittest.mock import MagicMock, Mock, patch

import pytest
from pytest_mock import MockerFixture

from modular_message_bot.job_runner import JobRunner


@pytest.fixture(autouse=True)
def mock_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.job_runner.logger")


@patch.object(JobRunner, "get_job_run_vars_collection")
def test_job_run(mock_get_job_run_vars_collection: MagicMock, mock_logger: MagicMock):
    # Given
    mock_job_run_vars_collection = Mock()
    mock_get_job_run_vars_collection.return_value = mock_job_run_vars_collection

    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_pre_handlers = Mock()
    mock_pre_handlers.run.return_value = True
    mock_input_handlers = Mock()
    mock_input_handlers.validate_job_vars.return_value = ""
    mock_processor_handlers = Mock()
    mock_processor_handlers.process.return_value = True
    mock_output_handlers = Mock()

    mock_job = Mock()
    mock_job.get_name.return_value = "0300ebe0-fdbe-4a2c-8097-ce8ba4df200a"
    mock_job.vars.return_value = {"a": "1"}

    # When
    job_runner = JobRunner(
        mock_dynamic_config_interpolator,
        mock_job_string_interpolator,
        mock_pre_handlers,
        mock_input_handlers,
        mock_processor_handlers,
        mock_output_handlers,
    )
    job_runner.run_job(mock_job)

    # Then
    mock_logger.info.assert_called_once_with("Running job '0300ebe0-fdbe-4a2c-8097-ce8ba4df200a'")
    mock_get_job_run_vars_collection.assert_called_once_with(mock_job)
    mock_pre_handlers.run.assert_called_once_with(mock_job, mock_job_run_vars_collection)
    mock_input_handlers.run.assert_called_once_with(mock_job, mock_job_run_vars_collection)
    mock_input_handlers.validate_job_vars.assert_called_once_with(mock_job_run_vars_collection)
    mock_processor_handlers.process.assert_called_once_with(mock_job, mock_job_run_vars_collection)
    mock_output_handlers.output.assert_called_once_with(mock_job, mock_job_run_vars_collection)


@patch.object(JobRunner, "get_job_run_vars_collection")
def test_job_run_pre_failure(mock_get_job_run_vars_collection: MagicMock, mock_logger: MagicMock):
    # Given
    mock_job_run_vars_collection = Mock()
    mock_get_job_run_vars_collection.return_value = mock_job_run_vars_collection

    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_pre_handlers = Mock()
    mock_pre_handlers.run.return_value = False
    mock_input_handlers = Mock()
    mock_input_handlers.validate_job_vars.return_value = ""
    mock_processor_handlers = Mock()
    mock_processor_handlers.process.return_value = True
    mock_output_handlers = Mock()

    mock_job = Mock()
    mock_job.get_name.return_value = "0300ebe0-fdbe-4a2c-8097-ce8ba4df200a"
    mock_job.vars.return_value = {"a": "1"}

    # When
    job_runner = JobRunner(
        mock_dynamic_config_interpolator,
        mock_job_string_interpolator,
        mock_pre_handlers,
        mock_input_handlers,
        mock_processor_handlers,
        mock_output_handlers,
    )
    job_runner.run_job(mock_job)

    # Then
    mock_logger.info.assert_called_once_with("Running job '0300ebe0-fdbe-4a2c-8097-ce8ba4df200a'")
    mock_get_job_run_vars_collection.assert_called_once_with(mock_job)
    mock_pre_handlers.run.assert_called_once_with(mock_job, mock_job_run_vars_collection)
    mock_input_handlers.run.assert_not_called()
    mock_input_handlers.validate_job_vars.assert_not_called()
    mock_processor_handlers.process.assert_not_called()
    mock_output_handlers.output.assert_not_called()


@patch.object(JobRunner, "get_job_run_vars_collection")
def test_job_run_input_validation_failed(mock_get_job_run_vars_collection: MagicMock, mock_logger: MagicMock):
    # Given
    mock_job_run_vars_collection = Mock()
    mock_get_job_run_vars_collection.return_value = mock_job_run_vars_collection

    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_pre_handlers = Mock()
    mock_pre_handlers.run.return_value = True
    mock_input_handlers = Mock()
    mock_input_handlers.validate_job_vars.return_value = "Some message is invalid because xyz"
    mock_processor_handlers = Mock()
    mock_processor_handlers.process.return_value = True
    mock_output_handlers = Mock()

    mock_job = Mock()
    mock_job.get_name.return_value = "0300ebe0-fdbe-4a2c-8097-ce8ba4df200a"
    mock_job.vars.return_value = {"a": "1"}

    # When
    job_runner = JobRunner(
        mock_dynamic_config_interpolator,
        mock_job_string_interpolator,
        mock_pre_handlers,
        mock_input_handlers,
        mock_processor_handlers,
        mock_output_handlers,
    )

    # When / Then
    with pytest.raises(Exception, match="Some message is invalid because xyz"):
        job_runner.run_job(mock_job)

    # Then
    mock_logger.info.assert_called_once_with("Running job '0300ebe0-fdbe-4a2c-8097-ce8ba4df200a'")
    mock_get_job_run_vars_collection.assert_called_once_with(mock_job)
    mock_pre_handlers.run.assert_called_once_with(mock_job, mock_job_run_vars_collection)
    mock_input_handlers.run.assert_called_once_with(mock_job, mock_job_run_vars_collection)
    mock_input_handlers.validate_job_vars.assert_called_once_with(mock_job_run_vars_collection)
    mock_processor_handlers.process.assert_not_called()
    mock_output_handlers.output.assert_not_called()


@patch.object(JobRunner, "get_job_run_vars_collection")
def test_job_run_processor_handlers_failed(mock_get_job_run_vars_collection: MagicMock, mock_logger: MagicMock):
    # Given
    mock_job_run_vars_collection = Mock()
    mock_get_job_run_vars_collection.return_value = mock_job_run_vars_collection

    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_pre_handlers = Mock()
    mock_pre_handlers.run.return_value = True
    mock_input_handlers = Mock()
    mock_input_handlers.validate_job_vars.return_value = ""
    mock_processor_handlers = Mock()
    mock_processor_handlers.process.return_value = False
    mock_output_handlers = Mock()

    mock_job = Mock()
    mock_job.get_name.return_value = "0300ebe0-fdbe-4a2c-8097-ce8ba4df200a"
    mock_job.vars.return_value = {"a": "1"}

    # When
    job_runner = JobRunner(
        mock_dynamic_config_interpolator,
        mock_job_string_interpolator,
        mock_pre_handlers,
        mock_input_handlers,
        mock_processor_handlers,
        mock_output_handlers,
    )
    job_runner.run_job(mock_job)

    # Then
    mock_logger.info.assert_called_once_with("Running job '0300ebe0-fdbe-4a2c-8097-ce8ba4df200a'")
    mock_get_job_run_vars_collection.assert_called_once_with(mock_job)
    mock_pre_handlers.run.assert_called_once_with(mock_job, mock_job_run_vars_collection)
    mock_input_handlers.run.assert_called_once_with(mock_job, mock_job_run_vars_collection)
    mock_input_handlers.validate_job_vars.assert_called_once_with(mock_job_run_vars_collection)
    mock_processor_handlers.process.assert_called_once_with(mock_job, mock_job_run_vars_collection)
    mock_output_handlers.output.assert_not_called()


def test_get_job_run_vars_collection():
    # Given
    mock_dynamic_config_interpolator = Mock()
    mock_dynamic_config_interpolator.interpolate.side_effect = ["1a", "2b", "3", "4"]
    mock_job_string_interpolator = Mock()
    mock_pre_handlers = Mock()
    mock_input_handlers = Mock()
    mock_processor_handlers = Mock()
    mock_output_handlers = Mock()

    mock_job = Mock()
    # fmt: off
    mock_job.vars = {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": 42,
        "e": "4"
    }
    # fmt: on

    # When
    job_runner = JobRunner(
        mock_dynamic_config_interpolator,
        mock_job_string_interpolator,
        mock_pre_handlers,
        mock_input_handlers,
        mock_processor_handlers,
        mock_output_handlers,
    )
    result = job_runner.get_job_run_vars_collection(mock_job)
    all_job_vars = result.get_all()

    # Then
    assert len(all_job_vars) == 5

    assert all_job_vars[0].code == "a"
    assert all_job_vars[0].value == "1a"
    assert all_job_vars[0].interpolated_by_input_codes == []

    assert all_job_vars[1].code == "b"
    assert all_job_vars[1].value == "2b"
    assert all_job_vars[1].interpolated_by_input_codes == []

    assert all_job_vars[2].code == "c"
    assert all_job_vars[2].value == "3"
    assert all_job_vars[2].interpolated_by_input_codes == []

    assert all_job_vars[3].code == "d"
    assert all_job_vars[3].value == 42
    assert all_job_vars[3].interpolated_by_input_codes == []

    assert all_job_vars[4].code == "e"
    assert all_job_vars[4].value == "4"
    assert all_job_vars[4].interpolated_by_input_codes == []
