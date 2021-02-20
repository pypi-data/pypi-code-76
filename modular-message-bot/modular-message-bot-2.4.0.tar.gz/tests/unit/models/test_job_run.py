from unittest.mock import Mock

from modular_message_bot.factory import build_job_string_interpolator
from modular_message_bot.models.job_run import JobRunVar, JobRunVarCollection


def test_add_interpolated_by_input_codes():
    # Given

    # When
    job_run_var = JobRunVar(code="test", value="hello", interpolated_by_input_codes=[])
    job_run_var.add_interpolated_by_input_codes("alpha")
    job_run_var.add_interpolated_by_input_codes("beta")
    job_run_var.add_interpolated_by_input_codes("alpha")

    # Then
    assert len(job_run_var.interpolated_by_input_codes) == 2
    assert job_run_var.interpolated_by_input_codes == ["alpha", "beta"]


def test_job_run_var_collection_get_all():
    # Given
    mock_job_var_interpolator = Mock()
    job_run_vars = [
        JobRunVar(code="a", value="1", interpolated_by_input_codes=[]),
        JobRunVar(code="b", value="2", interpolated_by_input_codes=[]),
        JobRunVar(code="c", value="3", interpolated_by_input_codes=[]),
        JobRunVar(code="d", value="4", interpolated_by_input_codes=[]),
    ]

    # When
    job_run_var_collection = JobRunVarCollection(mock_job_var_interpolator, job_run_vars)
    result = job_run_var_collection.get_all()

    # Then
    assert result == job_run_vars


def test_job_run_var_collection_get_by_code():
    # Given
    mock_job_var_interpolator = Mock()
    job_run_vars = [
        JobRunVar(code="a", value="1", interpolated_by_input_codes=[]),
        JobRunVar(code="b", value="2", interpolated_by_input_codes=[]),
        JobRunVar(code="c", value="3", interpolated_by_input_codes=[]),
        JobRunVar(code="d", value="4", interpolated_by_input_codes=[]),
    ]

    # When
    job_run_var_collection = JobRunVarCollection(mock_job_var_interpolator, job_run_vars)
    result_b = job_run_var_collection.get_by_code("b")
    result_c = job_run_var_collection.get_by_code("c")

    # Then
    assert result_b == job_run_vars[1]
    assert result_c == job_run_vars[2]


def test_job_run_var_collection_interpolate():
    # Given
    mock_job_var_interpolator = build_job_string_interpolator()
    job_run_vars = [
        JobRunVar(code="a", value="hi {name}", interpolated_by_input_codes=[]),
        JobRunVar(code="b", value="an {name} was here", interpolated_by_input_codes=[]),
        JobRunVar(code="c", value="some string", interpolated_by_input_codes=[]),
        JobRunVar(code="d", value="another string with name:{name}", interpolated_by_input_codes=["existing_handler"]),
        JobRunVar(code="e", value=42, interpolated_by_input_codes=[]),
        JobRunVar(
            code="f", value="a {name} with {other} vars {here}", interpolated_by_input_codes=["a_handler", "b_handler"]
        ),
    ]

    # When
    job_run_var_collection = JobRunVarCollection(mock_job_var_interpolator, job_run_vars)
    job_run_var_collection.interpolate("name", "example", "some_handler")
    results = job_run_var_collection.get_all()

    # Then
    assert len(results) == 6

    assert results[0].code == "a"
    assert results[0].value == "hi example"
    assert results[0].interpolated_by_input_codes == ["some_handler"]

    assert results[1].code == "b"
    assert results[1].value == "an example was here"
    assert results[1].interpolated_by_input_codes == ["some_handler"]

    assert results[2].code == "c"
    assert results[2].value == "some string"
    assert results[2].interpolated_by_input_codes == []

    assert results[3].code == "d"
    assert results[3].value == "another string with name:example"
    assert results[3].interpolated_by_input_codes == ["existing_handler", "some_handler"]

    assert results[4].code == "e"
    assert results[4].value == 42
    assert results[4].interpolated_by_input_codes == []

    assert results[5].code == "f"
    assert results[5].value == "a example with {other} vars {here}"
    assert results[5].interpolated_by_input_codes == ["a_handler", "b_handler", "some_handler"]


def test_job_run_var_collection_interpolate_into_parameters():
    # Given
    mock_job_var_interpolator = build_job_string_interpolator()
    job_run_vars = [
        JobRunVar(code="a", value="Alfa", interpolated_by_input_codes=[]),
        JobRunVar(code="b", value="Bravo", interpolated_by_input_codes=[]),
        JobRunVar(code="c", value="Charlie", interpolated_by_input_codes=[]),
    ]
    parameters = {
        "param_1": "hi {a}",
        "param_2": "a {a} and {b}",
        "param_3": "a is {a} b is {b} c is {c}",
        "param_4": "a string without vars here",
        "param_5": 42,
    }

    # When
    job_run_var_collection = JobRunVarCollection(mock_job_var_interpolator, job_run_vars)
    job_run_var_collection.interpolate("name", "example", "some_handler")
    results = job_run_var_collection.interpolate_into_parameters(parameters)

    # Then
    assert results["param_1"] == "hi Alfa"
    assert results["param_2"] == "a Alfa and Bravo"
    assert results["param_3"] == "a is Alfa b is Bravo c is Charlie"
    assert results["param_4"] == "a string without vars here"
    assert results["param_5"] == 42
