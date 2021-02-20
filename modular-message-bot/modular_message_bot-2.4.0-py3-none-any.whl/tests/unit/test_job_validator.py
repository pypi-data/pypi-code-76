from unittest.mock import MagicMock, Mock, call, patch

from modular_message_bot.handlers.handler_collections import (
    InputHandlerCollection,
    OutputHandlerCollection,
    PreHandlerCollection,
    ProcessorHandlerCollection,
)
from modular_message_bot.job_validator import JobValidator
from modular_message_bot.models.job import Job, JobsCollection


@patch.object(JobValidator, "validate_handlers")
def test_validate(mock_validate_handlers: MagicMock):
    # Given
    mock_validate_handlers.side_effect = ["", "", "", ""]
    mock_jobs_collection = Mock(spec=JobsCollection)
    mock_jobs_collection.get_all.return_value = [Mock(spec=Job), Mock(spec=Job)]
    mock_pre_handlers = Mock(spec=PreHandlerCollection)
    mock_input_handlers = Mock(spec=InputHandlerCollection)
    mock_processor_handlers = Mock(spec=ProcessorHandlerCollection)
    mock_output_handlers = Mock(spec=OutputHandlerCollection)

    # When
    validator = JobValidator(mock_pre_handlers, mock_input_handlers, mock_processor_handlers, mock_output_handlers)
    validation_result = validator.validate(mock_jobs_collection)

    # Then
    assert validation_result == ""
    mock_validate_handlers.assert_has_calls(
        [
            call("pre", mock_jobs_collection.get_all.return_value),
            call("input", mock_jobs_collection.get_all.return_value),
            call("processor", mock_jobs_collection.get_all.return_value),
            call("output", mock_jobs_collection.get_all.return_value),
        ]
    )


@patch.object(JobValidator, "validate_handlers")
def test_validate_invalid_pre(mock_validate_handlers: MagicMock):
    # Given
    mock_validate_handlers.side_effect = ["Pre failed due to something", "", "", ""]
    mock_jobs_collection = Mock(spec=JobsCollection)
    mock_jobs_collection.get_all.return_value = [Mock(spec=Job), Mock(spec=Job)]
    mock_pre_handlers = Mock(spec=PreHandlerCollection)
    mock_input_handlers = Mock(spec=InputHandlerCollection)
    mock_processor_handlers = Mock(spec=ProcessorHandlerCollection)
    mock_output_handlers = Mock(spec=OutputHandlerCollection)

    # When
    validator = JobValidator(mock_pre_handlers, mock_input_handlers, mock_processor_handlers, mock_output_handlers)
    validation_result = validator.validate(mock_jobs_collection)

    # Then
    assert validation_result == "Pre failed due to something"
    mock_validate_handlers.assert_has_calls(
        [
            call("pre", mock_jobs_collection.get_all.return_value),
            call("input", mock_jobs_collection.get_all.return_value),
            call("processor", mock_jobs_collection.get_all.return_value),
            call("output", mock_jobs_collection.get_all.return_value),
        ]
    )


@patch.object(JobValidator, "validate_handlers")
def test_validate_invalid_input(mock_validate_handlers: MagicMock):
    # Given
    mock_validate_handlers.side_effect = ["", "Input failed due to something", "", ""]
    mock_jobs_collection = Mock(spec=JobsCollection)
    mock_jobs_collection.get_all.return_value = [Mock(spec=Job), Mock(spec=Job)]
    mock_pre_handlers = Mock(spec=PreHandlerCollection)
    mock_input_handlers = Mock(spec=InputHandlerCollection)
    mock_processor_handlers = Mock(spec=ProcessorHandlerCollection)
    mock_output_handlers = Mock(spec=OutputHandlerCollection)

    # When
    validator = JobValidator(mock_pre_handlers, mock_input_handlers, mock_processor_handlers, mock_output_handlers)
    validation_result = validator.validate(mock_jobs_collection)

    # Then
    assert validation_result == "Input failed due to something"
    mock_validate_handlers.assert_has_calls(
        [
            call("pre", mock_jobs_collection.get_all.return_value),
            call("input", mock_jobs_collection.get_all.return_value),
            call("processor", mock_jobs_collection.get_all.return_value),
            call("output", mock_jobs_collection.get_all.return_value),
        ]
    )


@patch.object(JobValidator, "validate_handlers")
def test_validate_invalid_process(mock_validate_handlers: MagicMock):
    # Given
    mock_validate_handlers.side_effect = ["", "", "Process failed due to something", ""]
    mock_jobs_collection = Mock(spec=JobsCollection)
    mock_jobs_collection.get_all.return_value = [Mock(spec=Job), Mock(spec=Job)]
    mock_pre_handlers = Mock(spec=PreHandlerCollection)
    mock_input_handlers = Mock(spec=InputHandlerCollection)
    mock_processor_handlers = Mock(spec=ProcessorHandlerCollection)
    mock_output_handlers = Mock(spec=OutputHandlerCollection)

    # When
    validator = JobValidator(mock_pre_handlers, mock_input_handlers, mock_processor_handlers, mock_output_handlers)
    validation_result = validator.validate(mock_jobs_collection)

    # Then
    assert validation_result == "Process failed due to something"
    mock_validate_handlers.assert_has_calls(
        [
            call("pre", mock_jobs_collection.get_all.return_value),
            call("input", mock_jobs_collection.get_all.return_value),
            call("processor", mock_jobs_collection.get_all.return_value),
            call("output", mock_jobs_collection.get_all.return_value),
        ]
    )


@patch.object(JobValidator, "validate_handlers")
def test_validate_invalid_output(mock_validate_handlers: MagicMock):
    # Given
    mock_validate_handlers.side_effect = ["", "", "", "Output failed due to something"]
    mock_jobs_collection = Mock(spec=JobsCollection)
    mock_jobs_collection.get_all.return_value = [Mock(spec=Job), Mock(spec=Job)]
    mock_pre_handlers = Mock(spec=PreHandlerCollection)
    mock_input_handlers = Mock(spec=InputHandlerCollection)
    mock_processor_handlers = Mock(spec=ProcessorHandlerCollection)
    mock_output_handlers = Mock(spec=OutputHandlerCollection)

    # When
    validator = JobValidator(mock_pre_handlers, mock_input_handlers, mock_processor_handlers, mock_output_handlers)
    validation_result = validator.validate(mock_jobs_collection)

    # Then
    assert validation_result == "Output failed due to something"
    mock_validate_handlers.assert_has_calls(
        [
            call("pre", mock_jobs_collection.get_all.return_value),
            call("input", mock_jobs_collection.get_all.return_value),
            call("processor", mock_jobs_collection.get_all.return_value),
            call("output", mock_jobs_collection.get_all.return_value),
        ]
    )


def test_validate_input_handlers():
    # Given
    attr = "input"
    pre_handlers_collection = PreHandlerCollection()
    input_handlers_collection = InputHandlerCollection()
    processor_handlers_collection = ProcessorHandlerCollection()
    output_handlers_collection = OutputHandlerCollection()

    def make_mock_job(letters: list):
        mock_job = Mock()
        mock_job_configs = {}
        for a_letter in letters:
            mock_job_config = MagicMock()
            mock_job_config.code = f"input_handler_{a_letter}"
            mock_job_configs[a_letter] = mock_job_config
        mock_job.inputs = mock_job_configs.values()
        return mock_job_configs, mock_job

    mock_job1_configs, mock_job1 = make_mock_job(["a", "b"])
    mock_job2_configs, mock_job2 = make_mock_job(["a", "c", "d"])
    jobs = [mock_job1, mock_job2]

    mock_handlers = {}
    for letter in ["a", "b", "c", "d", "e"]:
        mock_handler = Mock()
        mock_handler.get_code.return_value = f"input_handler_{letter}"
        mock_handler.validate_job_config.return_value = ""
        mock_handlers[letter] = mock_handler
        input_handlers_collection.add_handler(mock_handler)

    # When
    validator = JobValidator(
        pre_handlers_collection, input_handlers_collection, processor_handlers_collection, output_handlers_collection
    )
    validation_result = validator.validate_handlers(attr, jobs)

    # Then
    assert validation_result == ""
    mock_handlers["a"].validate_job_config.assert_has_calls(
        [call(mock_job1_configs["a"]), call(mock_job2_configs["a"])]
    )
    mock_handlers["b"].validate_job_config.assert_has_calls([call(mock_job1_configs["b"])])
    mock_handlers["c"].validate_job_config.assert_has_calls([call(mock_job2_configs["c"])])
    mock_handlers["d"].validate_job_config.assert_has_calls([call(mock_job2_configs["d"])])
    mock_handlers["e"].validate_job_config.assert_not_called()


def test_validate_input_handlers_invalid_job_config():
    # Given
    attr = "input"
    pre_handlers_collection = PreHandlerCollection()
    input_handlers_collection = InputHandlerCollection()
    processor_handlers_collection = ProcessorHandlerCollection()
    output_handlers_collection = OutputHandlerCollection()

    def make_mock_job(letters: list):
        mock_job = Mock()
        mock_job_configs = {}
        for a_letter in letters:
            mock_job_config = MagicMock()
            mock_job_config.code = f"input_handler_{a_letter}"
            mock_job_configs[a_letter] = mock_job_config
        mock_job.inputs = mock_job_configs.values()
        return mock_job_configs, mock_job

    mock_job1_configs, mock_job1 = make_mock_job(["a", "b"])
    mock_job2_configs, mock_job2 = make_mock_job(["a", "c", "d"])
    jobs = [mock_job1, mock_job2]

    mock_handlers = {}
    for letter in ["a", "b", "c", "d", "e"]:
        mock_handler = Mock()
        mock_handler.get_code.return_value = f"input_handler_{letter}"
        mock_handler.validate_job_config.return_value = ""
        mock_handlers[letter] = mock_handler
        input_handlers_collection.add_handler(mock_handler)
    mock_handlers["d"].validate_job_config.return_value = "Something in the job config is invalid"

    # When
    validator = JobValidator(
        pre_handlers_collection, input_handlers_collection, processor_handlers_collection, output_handlers_collection
    )
    validation_result = validator.validate_handlers(attr, jobs)

    # Then
    assert validation_result == "Something in the job config is invalid"
