from pathlib import Path

import pytest

from dkist_processing_common._util.globus import submit_globus_transfer


def test_submit_globus_transfer_non_equal_source_and_dest():
    with pytest.raises(ValueError):
        submit_globus_transfer(
            source_files=[Path("1"), Path("2"), Path("3")],
            destination_files=[Path("4"), Path("5")],
            source_endpoint="test",
            destination_endpoint="test",
        )


def test_invalid_source_endpoint():
    with pytest.raises(ValueError):
        submit_globus_transfer(
            source_files=[Path("1"), Path("2"), Path("3")],
            destination_files=[Path("4"), Path("5"), Path("6")],
            source_endpoint="test",
            destination_endpoint="a62e451d-1927-4e74-9a8c-9c42d0bc5217",
        )


def test_invalid_destination_endpoint():
    with pytest.raises(ValueError):
        submit_globus_transfer(
            source_files=[Path("1"), Path("2"), Path("3")],
            destination_files=[Path("4"), Path("5"), Path("6")],
            source_endpoint="a62e451d-1927-4e74-9a8c-9c42d0bc5217",
            destination_endpoint="test",
        )


def test_globus_transfer(mocker):
    mocker.patch("dkist_processing_common._util.globus.get_globus_transfer_client", autospec=True)
    submit_globus_transfer(
        source_files=[Path("1"), Path("2"), Path("3")],
        destination_files=[Path("4"), Path("5"), Path("6")],
        source_endpoint="a62e451d-1927-4e74-9a8c-9c42d0bc5217",
        destination_endpoint="a62e451d-1927-4e74-9a8c-9c42d0bc5217",
    )
