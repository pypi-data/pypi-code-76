import pytest


def test_add_all_passed_test_cases():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    actual.append(testreporter.add_testcase("test name 2", True))
    expected = [
        {
            "test": "test name",
            "issuccess": "True",
            "result": "success",
            "failurereason": "",
        },
        {
            "test": "test name 2",
            "issuccess": "True",
            "result": "success",
            "failurereason": "",
        },
    ]
    assert expected == actual


def test_add_passed_test_case():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    expected = [
        {
            "test": "test name",
            "issuccess": "True",
            "result": "success",
            "failurereason": "",
        }
    ]
    assert expected == actual


def test_add_failed_test_case():
    from runeatest import testreporter

    actual = []
    actual.append(
        testreporter.add_testcase("test name", False, "actual isn't expected")
    )
    expected = [
        {
            "test": "test name",
            "issuccess": "False",
            "result": "failure",
            "failurereason": "actual isn't expected",
        }
    ]
    assert expected == actual


def test_add_all_failed_test_cases():
    from runeatest import testreporter

    actual_test_add_all_failed_test_cases = []
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase("test name", False, "this test failed")
    )
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase("test name 2", False, "that test failed")
    )
    expected_test_add_all_failed_test_cases = [
        {
            "test": "test name",
            "issuccess": "False",
            "result": "failure",
            "failurereason": "this test failed",
        },
        {
            "test": "test name 2",
            "issuccess": "False",
            "result": "failure",
            "failurereason": "that test failed",
        },
    ]
    assert (
        expected_test_add_all_failed_test_cases == actual_test_add_all_failed_test_cases
    )


def test_add_one_passed_one_failed_test_cases():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    actual.append(
        testreporter.add_testcase("test name 2", False, "my test failed here")
    )
    expected = [
        {
            "test": "test name",
            "issuccess": "True",
            "result": "success",
            "failurereason": "",
        },
        {
            "test": "test name 2",
            "issuccess": "False",
            "result": "failure",
            "failurereason": "my test failed here",
        },
    ]
    actual_string = str(actual)
    assert expected == actual


def test_add_one_passed_one_failed_test_cases_to_string():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    actual.append(testreporter.add_testcase("test name 2", False, "a failed test"))
    expected = "[{'test': 'test name', 'issuccess': 'True', 'result': 'success', 'failurereason': ''}, {'test': 'test name 2', 'issuccess': 'False', 'result': 'failure', 'failurereason': 'a failed test'}]"
    actual_string = str(actual)
    assert expected == actual_string


def test_add_all_failed_test_cases_to_string():
    from runeatest import testreporter

    actual_test_add_all_failed_test_cases = []
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase("test name", False, "test name 1 has failed")
    )
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase("test name 2", False, "test name 2 has failed")
    )
    expected_test_add_all_failed_test_cases_string = "[{'test': 'test name', 'issuccess': 'False', 'result': 'failure', 'failurereason': 'test name 1 has failed'}, {'test': 'test name 2', 'issuccess': 'False', 'result': 'failure', 'failurereason': 'test name 2 has failed'}]"
    actual_test_add_all_failed_test_cases_string = str(
        actual_test_add_all_failed_test_cases
    )
    assert (
        expected_test_add_all_failed_test_cases_string
        == actual_test_add_all_failed_test_cases_string
    )


def test_add_all_passed_test_cases_failure_included():
    from runeatest import testreporter

    actual = []
    actual.append(
        testreporter.add_testcase(
            "test name", True, "my test may have failed because of something"
        )
    )
    actual.append(
        testreporter.add_testcase(
            "test name 2", True, "my test may have failed because of something else"
        )
    )
    expected = [
        {
            "test": "test name",
            "issuccess": "True",
            "result": "success",
            "failurereason": "my test may have failed because of something",
        },
        {
            "test": "test name 2",
            "issuccess": "True",
            "result": "success",
            "failurereason": "my test may have failed because of something else",
        },
    ]
    assert expected == actual
