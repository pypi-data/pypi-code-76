import pytest
import json
from runeatest import testreporter


def test_add_all_passed_test_cases(mocker):
    x = '{"tags": {"opId": "ServerBackend-f421e441fa310430","browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","orgId": "1009391617598028","userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","clusterId": "0216-124733-lone970","user": "eter.natus@galar.com","principalIdpObjectId": "71b45910-e7b4-44d8-82f7-bf6fac4630d0","browserHostName": "uksouth.azuredatabricks.net","parentOpId": "RPCClient-bb9b9591c29c01f7","jettyRpcType": "InternalDriverBackendMessages$DriverBackendRequest"},"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)

    actual = []
    actual.append(
        testreporter.add_testcase(
            "test name", True, "this test will check that something will work"
        )
    )
    actual.append(
        testreporter.add_testcase(
            "test name 2", True, "this test also will check that something will work"
        )
    )
    expected = [
        {
            "test": "test name",
            "issuccess": "True",
            "description": "this test will check that something will work",
            "classname": "/Users/lorem.ipsum@fake.io/runeatest",
            "result": "success",
            "failurereason": "",
        },
        {
            "test": "test name 2",
            "issuccess": "True",
            "description": "this test also will check that something will work",
            "classname": "/Users/lorem.ipsum@fake.io/runeatest",
            "result": "success",
            "failurereason": "",
        },
    ]
    assert expected == actual


def test_add_passed_test_case(mocker):
    x = '{"tags": {"opId": "ServerBackend-f421e441fa310430","browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","orgId": "1009391617598028","userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","clusterId": "0216-124733-lone970","user": "eter.natus@galar.com","principalIdpObjectId": "71b45910-e7b4-44d8-82f7-bf6fac4630d0","browserHostName": "uksouth.azuredatabricks.net","parentOpId": "RPCClient-bb9b9591c29c01f7","jettyRpcType": "InternalDriverBackendMessages$DriverBackendRequest"},"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)

    actual = []
    actual.append(
        testreporter.add_testcase(
            "test name", True, "this test will check that something will work"
        )
    )
    expected = [
        {
            "test": "test name",
            "issuccess": "True",
            "description": "this test will check that something will work",
            "classname": "/Users/lorem.ipsum@fake.io/runeatest",
            "result": "success",
            "failurereason": "",
        }
    ]
    assert expected == actual


def test_add_failed_test_case(mocker):
    x = '{"tags": {"opId": "ServerBackend-f421e441fa310430","browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","orgId": "1009391617598028","userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","clusterId": "0216-124733-lone970","user": "eter.natus@galar.com","principalIdpObjectId": "71b45910-e7b4-44d8-82f7-bf6fac4630d0","browserHostName": "uksouth.azuredatabricks.net","parentOpId": "RPCClient-bb9b9591c29c01f7","jettyRpcType": "InternalDriverBackendMessages$DriverBackendRequest"},"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)

    actual = []
    actual.append(
        testreporter.add_testcase(
            "test name",
            False,
            "this test will check that something will work",
            "actual isn't expected",
        )
    )
    expected = [
        {
            "test": "test name",
            "issuccess": "False",
            "description": "this test will check that something will work",
            "classname": "/Users/lorem.ipsum@fake.io/runeatest",
            "result": "failure",
            "failurereason": "actual isn't expected",
        }
    ]
    assert expected == actual


def test_add_all_failed_test_cases(mocker):
    x = '{"tags": {"opId": "ServerBackend-f421e441fa310430","browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","orgId": "1009391617598028","userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","clusterId": "0216-124733-lone970","user": "eter.natus@galar.com","principalIdpObjectId": "71b45910-e7b4-44d8-82f7-bf6fac4630d0","browserHostName": "uksouth.azuredatabricks.net","parentOpId": "RPCClient-bb9b9591c29c01f7","jettyRpcType": "InternalDriverBackendMessages$DriverBackendRequest"},"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)

    actual_test_add_all_failed_test_cases = []
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase(
            "test name",
            False,
            "this test will check that something will work",
            "this test failed",
        )
    )
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase(
            "test name 2",
            False,
            "this test will check that something will work",
            "that test failed",
        )
    )
    expected_test_add_all_failed_test_cases = [
        {
            "test": "test name",
            "issuccess": "False",
            "description": "this test will check that something will work",
            "classname": "/Users/lorem.ipsum@fake.io/runeatest",
            "result": "failure",
            "failurereason": "this test failed",
        },
        {
            "test": "test name 2",
            "issuccess": "False",
            "description": "this test will check that something will work",
            "classname": "/Users/lorem.ipsum@fake.io/runeatest",
            "result": "failure",
            "failurereason": "that test failed",
        },
    ]
    assert (
        expected_test_add_all_failed_test_cases == actual_test_add_all_failed_test_cases
    )


def test_add_one_passed_one_failed_test_cases(mocker):
    x = '{"tags": {"opId": "ServerBackend-f421e441fa310430","browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","orgId": "1009391617598028","userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","clusterId": "0216-124733-lone970","user": "eter.natus@galar.com","principalIdpObjectId": "71b45910-e7b4-44d8-82f7-bf6fac4630d0","browserHostName": "uksouth.azuredatabricks.net","parentOpId": "RPCClient-bb9b9591c29c01f7","jettyRpcType": "InternalDriverBackendMessages$DriverBackendRequest"},"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)

    actual = []
    actual.append(
        testreporter.add_testcase(
            "test name", True, "this test will check that something will work"
        )
    )
    actual.append(
        testreporter.add_testcase(
            "test name 2",
            False,
            "this test will check that something will work",
            "my test failed here",
        )
    )
    expected = [
        {
            "test": "test name",
            "issuccess": "True",
            "description": "this test will check that something will work",
            "classname": "/Users/lorem.ipsum@fake.io/runeatest",
            "result": "success",
            "failurereason": "",
        },
        {
            "test": "test name 2",
            "issuccess": "False",
            "description": "this test will check that something will work",
            "classname": "/Users/lorem.ipsum@fake.io/runeatest",
            "result": "failure",
            "failurereason": "my test failed here",
        },
    ]
    actual_string = str(actual)
    assert expected == actual


def test_add_one_passed_one_failed_test_cases_to_string(mocker):
    x = '{"tags": {"opId": "ServerBackend-f421e441fa310430","browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","orgId": "1009391617598028","userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","clusterId": "0216-124733-lone970","user": "eter.natus@galar.com","principalIdpObjectId": "71b45910-e7b4-44d8-82f7-bf6fac4630d0","browserHostName": "uksouth.azuredatabricks.net","parentOpId": "RPCClient-bb9b9591c29c01f7","jettyRpcType": "InternalDriverBackendMessages$DriverBackendRequest"},"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)

    actual = []
    actual.append(
        testreporter.add_testcase(
            "test name", True, "this test will check that something will work"
        )
    )
    actual.append(
        testreporter.add_testcase(
            "test name 2",
            False,
            "this test will check that something will work",
            "a failed test",
        )
    )
    expected = "[{'test': 'test name', 'issuccess': 'True', 'description': 'this test will check that something will work', 'classname': '/Users/lorem.ipsum@fake.io/runeatest', 'result': 'success', 'failurereason': ''}, {'test': 'test name 2', 'issuccess': 'False', 'description': 'this test will check that something will work', 'classname': '/Users/lorem.ipsum@fake.io/runeatest', 'result': 'failure', 'failurereason': 'a failed test'}]"
    actual_string = str(actual)
    assert expected == actual_string


def test_add_all_failed_test_cases_to_string(mocker):
    x = '{"tags": {"opId": "ServerBackend-f421e441fa310430","browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","orgId": "1009391617598028","userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","clusterId": "0216-124733-lone970","user": "eter.natus@galar.com","principalIdpObjectId": "71b45910-e7b4-44d8-82f7-bf6fac4630d0","browserHostName": "uksouth.azuredatabricks.net","parentOpId": "RPCClient-bb9b9591c29c01f7","jettyRpcType": "InternalDriverBackendMessages$DriverBackendRequest"},"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)

    actual_test_add_all_failed_test_cases = []
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase(
            "test name",
            False,
            "this test will check that something will work",
            "test name 1 has failed",
        )
    )
    actual_test_add_all_failed_test_cases.append(
        testreporter.add_testcase(
            "test name 2",
            False,
            "this test will check that something will work",
            "test name 2 has failed",
        )
    )
    expected_test_add_all_failed_test_cases_string = "[{'test': 'test name', 'issuccess': 'False', 'description': 'this test will check that something will work', 'classname': '/Users/lorem.ipsum@fake.io/runeatest', 'result': 'failure', 'failurereason': 'test name 1 has failed'}, {'test': 'test name 2', 'issuccess': 'False', 'description': 'this test will check that something will work', 'classname': '/Users/lorem.ipsum@fake.io/runeatest', 'result': 'failure', 'failurereason': 'test name 2 has failed'}]"
    actual_test_add_all_failed_test_cases_string = str(
        actual_test_add_all_failed_test_cases
    )
    assert (
        expected_test_add_all_failed_test_cases_string
        == actual_test_add_all_failed_test_cases_string
    )


def test_add_all_passed_test_cases_failure_included(mocker):
    x = '{"tags": {"opId": "ServerBackend-f421e441fa310430","browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","orgId": "1009391617598028","userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","clusterId": "0216-124733-lone970","user": "eter.natus@galar.com","principalIdpObjectId": "71b45910-e7b4-44d8-82f7-bf6fac4630d0","browserHostName": "uksouth.azuredatabricks.net","parentOpId": "RPCClient-bb9b9591c29c01f7","jettyRpcType": "InternalDriverBackendMessages$DriverBackendRequest"},"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)

    actual = []
    actual.append(
        testreporter.add_testcase(
            "test name",
            True,
            "this test will check that something will work",
            "my test may have failed because of something",
        )
    )
    actual.append(
        testreporter.add_testcase(
            "test name 2",
            True,
            "this test will check that something will work",
            "my test may have failed because of something else",
        )
    )
    expected = [
        {
            "test": "test name",
            "issuccess": "True",
            "description": "this test will check that something will work",
            "classname": "/Users/lorem.ipsum@fake.io/runeatest",
            "result": "success",
            "failurereason": "my test may have failed because of something",
        },
        {
            "test": "test name 2",
            "issuccess": "True",
            "description": "this test will check that something will work",
            "classname": "/Users/lorem.ipsum@fake.io/runeatest",
            "result": "success",
            "failurereason": "my test may have failed because of something else",
        },
    ]
    assert expected == actual
