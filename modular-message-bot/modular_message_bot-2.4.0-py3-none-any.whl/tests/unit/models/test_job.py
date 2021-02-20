from unittest.mock import Mock

import pytest

from modular_message_bot.models.job import Job, JobsCollection


def test_get_name():
    # Given
    mock_config = Mock()
    job_id = "175d3ef9-3e62-4684-8328-844764f6f062"
    schedules = ["0 9 * * MON-FRI", "0 17 * * *"]
    schedules_timezone = "UTC"
    vars_dict = {"msg": "Test message"}
    pres = [Mock(), Mock()]
    inputs = [Mock(), Mock()]
    processors = [Mock(), Mock()]
    outputs = [Mock(), Mock()]

    # When
    job = Job(
        config=mock_config,
        id=job_id,
        schedules=schedules,
        schedules_timezone=schedules_timezone,
        vars=vars_dict,
        pres=pres,
        inputs=inputs,
        processors=processors,
        outputs=outputs,
    )

    # Then
    assert job.get_name() == "175d3ef9-3e62-4684-8328-844764f6f062"


def test_get_name_unknown():
    # Given
    mock_config = Mock()
    job_id = ""
    schedules = ["0 9 * * MON-FRI", "0 17 * * *"]
    schedules_timezone = "UTC"
    vars_dict = {"msg": "Test message"}
    pres = [Mock(), Mock()]
    inputs = [Mock(), Mock()]
    processors = [Mock(), Mock()]
    outputs = [Mock(), Mock()]

    # When
    job = Job(
        config=mock_config,
        id=job_id,
        schedules=schedules,
        schedules_timezone=schedules_timezone,
        vars=vars_dict,
        pres=pres,
        inputs=inputs,
        processors=processors,
        outputs=outputs,
    )

    # Then
    assert job.get_name() == "Unknown"


def test_get_schedules_timezone():
    # Given
    mock_config = Mock()
    job_id = "175d3ef9-3e62-4684-8328-844764f6f062"
    schedules = ["0 9 * * MON-FRI", "0 17 * * *"]
    schedules_timezone = "UTC"
    vars_dict = {"msg": "Test message"}
    pres = [Mock(), Mock()]
    inputs = [Mock(), Mock()]
    processors = [Mock(), Mock()]
    outputs = [Mock(), Mock()]

    # When
    job = Job(
        config=mock_config,
        id=job_id,
        schedules=schedules,
        schedules_timezone=schedules_timezone,
        vars=vars_dict,
        pres=pres,
        inputs=inputs,
        processors=processors,
        outputs=outputs,
    )

    # Then
    assert job.get_schedules_timezone() == schedules_timezone


def test_get_schedules_timezone_config():
    # Given
    mock_config = Mock()
    mock_config.get.return_value = "GMT"
    job_id = "175d3ef9-3e62-4684-8328-844764f6f062"
    schedules = ["0 9 * * MON-FRI", "0 17 * * *"]
    schedules_timezone = ""
    vars_dict = {"msg": "Test message"}
    pres = [Mock(), Mock()]
    inputs = [Mock(), Mock()]
    processors = [Mock(), Mock()]
    outputs = [Mock(), Mock()]

    # When
    job = Job(
        config=mock_config,
        id=job_id,
        schedules=schedules,
        schedules_timezone=schedules_timezone,
        vars=vars_dict,
        pres=pres,
        inputs=inputs,
        processors=processors,
        outputs=outputs,
    )

    # Then
    assert job.get_schedules_timezone() == "GMT"
    mock_config.get.assert_called_with("SCHEDULER_TIMEZONE")


def test_valid_collection():
    # Given
    number_of_jobs = 5
    jobs = []
    for i in range(0, number_of_jobs):
        handler = Mock()
        handler.id = f"job_{i}"  # Normally a uuid
        jobs.append(handler)

    # When
    jobs_collection = JobsCollection()
    for job in jobs:
        jobs_collection.add_job(job)

    # Then
    assert len(jobs_collection.get_all()) == number_of_jobs
    for i in range(0, number_of_jobs):
        assert jobs_collection.get_by_id(f"job_{i}") == jobs[i]


def test_add_duplicate_jobs():
    # Given
    mock_job_1 = Mock()
    mock_job_1.id = "some_duplicate_name"
    mock_job_2 = Mock()
    mock_job_2.id = "some_duplicate_name"

    # When
    jobs_collection = JobsCollection()
    jobs_collection.add_job(mock_job_1)

    # Then
    with pytest.raises(
        Exception, match="Job id 'some_duplicate_name' already exists, check your config for duplicate job ids",
    ):
        jobs_collection.add_job(mock_job_2)


def test_missing_job():
    # Given
    mock_job_1 = Mock()
    mock_job_1.id = "job_1"
    mock_job_2 = Mock()
    mock_job_2.id = "job_2"

    # When
    jobs_collection = JobsCollection()
    jobs_collection.add_job(mock_job_1)
    jobs_collection.add_job(mock_job_2)

    # Then
    with pytest.raises(Exception, match="Job id of 'job_id_not_in_collection' is not found"):
        jobs_collection.get_by_id("job_id_not_in_collection")
