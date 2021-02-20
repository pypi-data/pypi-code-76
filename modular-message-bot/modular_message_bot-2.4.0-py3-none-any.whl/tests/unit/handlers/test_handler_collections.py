from unittest.mock import MagicMock, Mock, call, patch

import pytest
from pytest_mock import MockerFixture

from modular_message_bot.handlers.handler_collections import (
    InputHandlerCollection,
    OutputHandlerCollection,
    PreHandlerCollection,
    ProcessorHandlerCollection,
)
from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractInputHandler
from modular_message_bot.handlers.outputs.abstract_output_hander import AbstractOutputHandler
from modular_message_bot.handlers.pres.abstract_pre_handler import AbstractPreHandler
from modular_message_bot.handlers.processors.abstract_processor_handler import AbstractProcessorHandler
from modular_message_bot.models.job import JobInput, JobOutput, JobPre, JobProcessor
from modular_message_bot.models.job_run import JobRunVar


@pytest.fixture(autouse=True)
def mock_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.handler_collections.logger")


# Note: Not testing the output handler collection as it is identical to the input handler collection
def test_valid_collection():
    # Given
    number_of_handlers = 5
    handlers = []
    for i in range(0, number_of_handlers):
        handler = Mock()
        handler.get_code.return_value = f"handler_{i}"
        handlers.append(handler)

    # When
    handler_collection = InputHandlerCollection()
    handler_collection.add_handlers(handlers)

    # Then
    assert len(handler_collection.get_all()) == number_of_handlers
    for i in range(0, number_of_handlers):
        assert handler_collection.get_by_code(f"handler_{i}") == handlers[i]


def test_duplicate_handler():
    # Given
    handler_1 = Mock()
    handler_1.get_code.return_value = "some_duplicate_name"
    handler_2 = Mock()
    handler_2.get_code.return_value = "some_duplicate_name"

    # When
    handler_collection = InputHandlerCollection()

    # Then
    with pytest.raises(Exception, match="Error: 'some_duplicate_name' already present"):
        handler_collection.add_handlers([handler_1, handler_2])


def test_get_by_code_missing():
    # Given
    number_of_handlers = 5
    handlers = []
    for i in range(0, number_of_handlers):
        handler = Mock()
        handler.get_code.return_value = f"handler_{i}"
        handlers.append(handler)

    # When
    handler_collection = InputHandlerCollection()
    handler_collection.add_handlers(handlers)

    # Then
    with pytest.raises(
        Exception, match="Error: 'handler_that_does_not_exist' not found, please check your jobs config",
    ):
        handler_collection.get_by_code("handler_that_does_not_exist")


@patch.object(PreHandlerCollection, "get_by_code")
def test_pre_handler_collection_run(mock_get_by_code: MagicMock):
    # Given
    handler_1 = Mock(spec=AbstractPreHandler)
    handler_1.run.return_value = True
    handler_2 = Mock(spec=AbstractPreHandler)
    handler_2.run.return_value = True
    handler_3 = Mock(spec=AbstractPreHandler)
    handler_3.run.return_value = True
    mock_get_by_code.side_effect = [handler_1, handler_2, handler_3]

    mock_job = Mock()
    mock_job.pres = [
        JobPre(code="handler_1", parameters={"a": "b"}),
        JobPre(code="handler_2", parameters={"c": "d"}),
        JobPre(code="handler_3", parameters={"e": "f"}),
    ]
    mock_job_run_vars_collection = Mock()

    # When
    collection = PreHandlerCollection()
    result = collection.run(mock_job, mock_job_run_vars_collection)

    # Then
    assert result
    mock_get_by_code.assert_has_calls([call("handler_1"), call("handler_2"), call("handler_3")])
    handler_1.run.assert_called_once_with({"a": "b"}, mock_job_run_vars_collection)
    handler_2.run.assert_called_once_with({"c": "d"}, mock_job_run_vars_collection)
    handler_3.run.assert_called_once_with({"e": "f"}, mock_job_run_vars_collection)


@patch.object(PreHandlerCollection, "get_by_code")
def test_pre_handler_collection_run_failure(mock_get_by_code: MagicMock, mock_logger: MagicMock):
    # Given
    handler_1 = Mock(spec=AbstractPreHandler)
    handler_1.run.return_value = True
    handler_2 = Mock(spec=AbstractPreHandler)
    handler_2.run.return_value = False
    handler_3 = Mock(spec=AbstractPreHandler)
    handler_3.run.return_value = True
    mock_get_by_code.side_effect = [handler_1, handler_2, handler_3]

    mock_job = Mock()
    mock_job.pres = [
        JobPre(code="handler_1", parameters={"a": "b"}),
        JobPre(code="handler_2", parameters={"c": "d"}),
        JobPre(code="handler_3", parameters={"e": "f"}),
    ]
    mock_job_run_vars_collection = Mock()

    # When
    collection = PreHandlerCollection()
    result = collection.run(mock_job, mock_job_run_vars_collection)

    # Then
    assert not result
    mock_get_by_code.assert_has_calls([call("handler_1"), call("handler_2")])
    handler_1.run.assert_called_once_with({"a": "b"}, mock_job_run_vars_collection)
    handler_2.run.assert_called_once_with({"c": "d"}, mock_job_run_vars_collection)
    handler_3.run.assert_not_called()
    mock_logger.info.assert_called_once_with("Job pre 'handler_2' aborted the job")


@patch.object(InputHandlerCollection, "get_by_code")
def test_input_handler_collection_run(mock_get_by_code: MagicMock):
    # Given
    handler_1 = Mock(spec=AbstractInputHandler)
    handler_2 = Mock(spec=AbstractInputHandler)
    handler_3 = Mock(spec=AbstractInputHandler)
    mock_get_by_code.side_effect = [handler_1, handler_2, handler_3]

    mock_job = Mock()
    mock_job.inputs = [
        JobInput(code="handler_1", parameters={"a": "b"}),
        JobInput(code="handler_2", parameters={"c": "d"}),
        JobInput(code="handler_3", parameters={"e": "f"}),
    ]

    mock_job_run_vars_collection = Mock()

    # When
    collection = InputHandlerCollection()
    collection.run(mock_job, mock_job_run_vars_collection)

    # Then
    mock_get_by_code.assert_has_calls([call("handler_1"), call("handler_2"), call("handler_3")])
    handler_1.run.assert_called_once_with({"a": "b"}, mock_job_run_vars_collection)
    handler_2.run.assert_called_once_with({"c": "d"}, mock_job_run_vars_collection)
    handler_3.run.assert_called_once_with({"e": "f"}, mock_job_run_vars_collection)


@patch.object(InputHandlerCollection, "get_by_code")
def test_input_handler_collection_validate_job_vars(mock_get_by_code: MagicMock):
    # Given
    handler_1 = Mock(spec=AbstractInputHandler)
    handler_1.validate_job_run_var.return_value = ""
    handler_2 = Mock(spec=AbstractInputHandler)
    handler_2.validate_job_run_var.return_value = ""
    handler_3 = Mock(spec=AbstractInputHandler)
    handler_3.validate_job_run_var.return_value = ""
    mock_get_by_code.side_effect = [handler_1, handler_2, handler_3]

    job_run_var_1 = JobRunVar(code="a", value="b", interpolated_by_input_codes=[])
    job_run_var_2 = JobRunVar(code="c", value="d", interpolated_by_input_codes=["z"])
    job_run_var_3 = JobRunVar(code="e", value="f", interpolated_by_input_codes=["x", "y"])

    mock_job_run_vars_collection = Mock()
    mock_job_run_vars_collection.get_all.return_value = [job_run_var_1, job_run_var_2, job_run_var_3]

    # When
    collection = InputHandlerCollection()
    result = collection.validate_job_vars(mock_job_run_vars_collection)

    # Then
    assert result == ""
    handler_1.validate_job_run_var.assert_has_calls([call(job_run_var_2)])
    handler_2.validate_job_run_var.assert_has_calls([call(job_run_var_3)])
    handler_3.validate_job_run_var.assert_has_calls([call(job_run_var_3)])


@patch.object(InputHandlerCollection, "get_by_code")
def test_input_handler_collection_validate_job_vars_invalid(mock_get_by_code: MagicMock):
    # Given
    handler_1 = Mock(spec=AbstractInputHandler)
    handler_1.validate_job_run_var.return_value = ""
    handler_2 = Mock(spec=AbstractInputHandler)
    handler_2.validate_job_run_var.return_value = "Ops, this is invalid"
    handler_3 = Mock(spec=AbstractInputHandler)
    mock_get_by_code.side_effect = [handler_1, handler_2, handler_3]

    job_run_var_1 = JobRunVar(code="a", value="b", interpolated_by_input_codes=[])
    job_run_var_2 = JobRunVar(code="c", value="d", interpolated_by_input_codes=["z"])
    job_run_var_3 = JobRunVar(code="e", value="f", interpolated_by_input_codes=["x"])

    mock_job_run_vars_collection = Mock()
    mock_job_run_vars_collection.get_all.return_value = [job_run_var_1, job_run_var_2, job_run_var_3]

    # When
    collection = InputHandlerCollection()
    result = collection.validate_job_vars(mock_job_run_vars_collection)

    # Then
    assert result == "Ops, this is invalid"
    handler_1.validate_job_run_var.assert_has_calls([call(job_run_var_2)])
    handler_2.validate_job_run_var.assert_has_calls([call(job_run_var_3)])
    handler_3.validate_job_run_var.assert_not_called()


@patch.object(ProcessorHandlerCollection, "get_by_code")
def test_processor_handler_collection_process(mock_get_by_code: MagicMock, mock_logger: MagicMock):
    # Given
    handler_1 = Mock(spec=AbstractProcessorHandler)
    handler_1.process.return_value = True
    handler_2 = Mock(spec=AbstractProcessorHandler)
    handler_2.process.return_value = True
    handler_3 = Mock(spec=AbstractProcessorHandler)
    handler_3.process.return_value = True
    mock_get_by_code.side_effect = [handler_1, handler_2, handler_3]

    mock_job = Mock()
    mock_job.processors = [
        JobProcessor(code="handler_1", parameters={"a": "b"}),
        JobProcessor(code="handler_2", parameters={"c": "d"}),
        JobProcessor(code="handler_3", parameters={"e": "f"}),
    ]

    mock_job_run_vars_collection = Mock()

    # When
    collection = ProcessorHandlerCollection()
    is_continue_result = collection.process(mock_job, mock_job_run_vars_collection)

    # Then
    assert is_continue_result
    handler_1.process.assert_called_once_with({"a": "b"}, mock_job_run_vars_collection)
    handler_2.process.assert_called_once_with({"c": "d"}, mock_job_run_vars_collection)
    handler_3.process.assert_called_once_with({"e": "f"}, mock_job_run_vars_collection)


@patch.object(ProcessorHandlerCollection, "get_by_code")
def test_processor_handler_collection_process_failure(mock_get_by_code: MagicMock, mock_logger: MagicMock):
    # Given
    handler_1 = Mock(spec=AbstractProcessorHandler)
    handler_1.process.return_value = True
    handler_2 = Mock(spec=AbstractProcessorHandler)
    handler_2.process.return_value = False
    handler_3 = Mock(spec=AbstractProcessorHandler)
    mock_get_by_code.side_effect = [handler_1, handler_2, handler_3]

    mock_job = Mock()
    mock_job.processors = [
        JobProcessor(code="handler_1", parameters={"a": "b"}),
        JobProcessor(code="handler_2", parameters={"c": "d"}),
        JobProcessor(code="handler_3", parameters={"e": "f"}),
    ]

    mock_job_run_vars_collection = Mock()

    # When
    collection = ProcessorHandlerCollection()
    is_continue_result = collection.process(mock_job, mock_job_run_vars_collection)

    # Then
    assert not is_continue_result
    handler_1.process.assert_called_once_with({"a": "b"}, mock_job_run_vars_collection)
    handler_2.process.assert_called_once_with({"c": "d"}, mock_job_run_vars_collection)
    handler_3.process.assert_not_called()
    mock_logger.info("Job processor 'handler_2' aborted")


@patch.object(OutputHandlerCollection, "get_by_code")
def test_output_handler_collection_output(mock_get_by_code: MagicMock):
    # Given
    handler_1 = Mock(spec=AbstractOutputHandler)
    handler_2 = Mock(spec=AbstractOutputHandler)
    handler_3 = Mock(spec=AbstractOutputHandler)
    mock_get_by_code.side_effect = [handler_1, handler_2, handler_3]

    mock_job = Mock()
    mock_job.outputs = [
        JobOutput(code="handler_1", parameters={"a": "b"}),
        JobOutput(code="handler_2", parameters={"c": "d"}),
        JobOutput(code="handler_3", parameters={"e": "f"}),
    ]

    mock_job_run_vars_collection = Mock()

    # When
    collection = OutputHandlerCollection()
    collection.output(mock_job, mock_job_run_vars_collection)

    # Then
    handler_1.run.assert_called_once_with({"a": "b"}, mock_job_run_vars_collection)
    handler_2.run.assert_called_once_with({"c": "d"}, mock_job_run_vars_collection)
    handler_3.run.assert_called_once_with({"e": "f"}, mock_job_run_vars_collection)
