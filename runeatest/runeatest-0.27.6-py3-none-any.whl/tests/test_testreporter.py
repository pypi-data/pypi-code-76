import pytest


def test_add_all_passed_test_cases():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    actual.append(testreporter.add_testcase("test name 2", True))
    expected = [
        {"test": "test name", "issuccess": "True", "result": "success"},
        {"test": "test name 2", "issuccess": "True", "result": "success"},
    ]
    assert expected == actual


def test_add_passed_test_case():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    expected = [{"test": "test name", "issuccess": "True", "result": "success"}]
    assert expected == actual


def test_add_failed_test_case():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", False))
    expected = [{"test": "test name", "issuccess": "False", "result": "failure"}]
    assert expected == actual


def test_add_all_failed_test_cases():
    from runeatest import testreporter

    actual_test_add_all_failed_test_cases = []
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase("test name", False)
    )
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase("test name 2", False)
    )
    expected_test_add_all_failed_test_cases = [
        {"test": "test name", "issuccess": "False", "result": "failure"},
        {"test": "test name 2", "issuccess": "False", "result": "failure"},
    ]
    assert (
        expected_test_add_all_failed_test_cases == actual_test_add_all_failed_test_cases
    )


def test_add_one_passed_one_failed_test_cases():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    actual.append(testreporter.add_testcase("test name 2", False))
    expected = [
        {"test": "test name", "issuccess": "True", "result": "success"},
        {"test": "test name 2", "issuccess": "False", "result": "failure"},
    ]
    actual_string = str(actual)
    assert expected == actual


def test_add_one_passed_one_failed_test_cases_to_string():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    actual.append(testreporter.add_testcase("test name 2", False))
    expected = "[{'test': 'test name', 'issuccess': 'True', 'result': 'success'}, {'test': 'test name 2', 'issuccess': 'False', 'result': 'failure'}]"
    actual_string = str(actual)
    assert expected == actual_string


def test_add_all_failed_test_cases_to_string():
    from runeatest import testreporter

    actual_test_add_all_failed_test_cases = []
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase("test name", False)
    )
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase("test name 2", False)
    )
    expected_test_add_all_failed_test_cases_string = "[{'test': 'test name', 'issuccess': 'False', 'result': 'failure'}, {'test': 'test name 2', 'issuccess': 'False', 'result': 'failure'}]"
    actual_test_add_all_failed_test_cases_string = str(
        actual_test_add_all_failed_test_cases
    )
    assert (
        expected_test_add_all_failed_test_cases_string
        == actual_test_add_all_failed_test_cases_string
    )
