import pytest
import json
from runeatest import nunitresults
from runeatest import pysparkconnect
from runeatest import utils
from runeatest import testreporter


def test_get_nunit_header(mocker):
    x = '{"tags": {"opId": "ServerBackend-f421e441fa310430","browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","orgId": "1009391617598028","userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","clusterId": "0216-124733-lone970","user": "eter.natus@galar.com","principalIdpObjectId": "71b45910-e7b4-44d8-82f7-bf6fac4630d0","browserHostName": "uksouth.azuredatabricks.net","parentOpId": "RPCClient-bb9b9591c29c01f7","jettyRpcType": "InternalDriverBackendMessages$DriverBackendRequest"},"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    t = ("2020-9-13", "13:20:16")
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    mocker.patch("runeatest.utils.get_date_and_time", return_value=t)
    results = []
    results.append(testreporter.add_testcase("test name", False))
    results.append(testreporter.add_testcase("test name 2", True))
    expected = '<test-results name="/Users/lorem.ipsum@fake.io/runeatest" total="2" date="2020-9-13" time="13:20:16">\n<environment nunit-version="2.6.0.12035" clr-version="2.0.50727.4963" os-version="uksouth.azuredatabricks.net" platform="Win32NT" cwd="C:\\Program Files\\NUnit 2.6\\bin\\" machine-name="0216-124733-lone970" user="eter.natus@galar.com" user-domain="1009391617598028"/>\n<culture-info current-culture="en-US" current-uiculture="en-US"/>'
    actual = nunitresults.get_nunit_header(results, context)
    assert expected == actual


def test_get_nunit_footer():
    expected = "</results>\n</test-suite>\n</test-results>"
    actual = nunitresults.get_nunit_footer()
    assert expected == actual


def test_get_test_suite_result_one_passed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", True))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="success" success="True" time="0.000" asserts="0"><results>'
    actual = nunitresults.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_suite_result_one_failed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", False))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="0"><results>'
    actual = nunitresults.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_suite_result_one_failed_one_passed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", False))
    results.append(testreporter.add_testcase("test name 2", True))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="0"><results>'
    actual = nunitresults.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_suite_result_one_passed_one_failed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", False))
    results.append(testreporter.add_testcase("test name 2", True))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="0"><results>'
    actual = nunitresults.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_suite_result_all_failed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", False))
    results.append(testreporter.add_testcase("test name 2", False))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="0"><results>'
    actual = nunitresults.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_suite_result_all_passed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", True))
    results.append(testreporter.add_testcase("test name 2", True))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="success" success="True" time="0.000" asserts="0"><results>'
    actual = nunitresults.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_suite_result_all_passed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(
        testreporter.add_testcase(
            "test name",
            True,
            "test may also have failed but because it did not this is not included in output",
        )
    )
    results.append(
        testreporter.add_testcase(
            "test name 2",
            True,
            "test may have failed but because it did not this is not included in output",
        )
    )
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="success" success="True" time="0.000" asserts="0"><results>'
    actual = nunitresults.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_case_results_one_failure(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(
        testreporter.add_testcase(
            "test name", False, "this description describes the test", "oh dear"
        )
    )
    expected = '<test-case name="test name" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="1">\n<failure><message>oh dear\n</message></failure>\n</test-case>'
    actual = nunitresults.get_test_case_results(results)
    assert expected == actual[0]


def test_get_test_case_results_one_pass(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(
        testreporter.add_testcase(
            "test name", True, "this description describes the test"
        )
    )
    expected = '<test-case name="test name" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="success" success="True" time="0.000" asserts="1"/>'
    actual = nunitresults.get_test_case_results(results)
    assert expected == actual[0]


def test_get_test_case_results_one_pass_one_fail(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(
        testreporter.add_testcase(
            "test name", True, "this description describes the test"
        )
    )
    results.append(
        testreporter.add_testcase(
            "test name 2", False, "this description describes the test", "oops"
        )
    )
    expected0 = '<test-case name="test name" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="success" success="True" time="0.000" asserts="1"/>'
    expected1 = '<test-case name="test name 2" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="1">\n<failure><message>oops\n</message></failure>\n</test-case>'
    actual = nunitresults.get_test_case_results(results)
    assert expected0 == actual[0]
    assert expected1 == actual[1]


def test_get_test_case_results_all_pass(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(
        testreporter.add_testcase(
            "test name", True, "this description describes the test"
        )
    )
    results.append(
        testreporter.add_testcase(
            "test name 2", True, "this description describes the test"
        )
    )
    expected0 = '<test-case name="test name" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="success" success="True" time="0.000" asserts="1"/>'
    expected1 = '<test-case name="test name 2" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="success" success="True" time="0.000" asserts="1"/>'
    actual = nunitresults.get_test_case_results(results)
    assert expected0 == actual[0]
    assert expected1 == actual[1]


def test_get_test_case_results_all_fail(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(
        testreporter.add_testcase(
            "test name", False, "this description describes the test", "why"
        )
    )
    results.append(
        testreporter.add_testcase(
            "test name 2", False, "this description describes the test", "why oh why"
        )
    )
    expected0 = '<test-case name="test name" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="1">\n<failure><message>why\n</message></failure>\n</test-case>'
    expected1 = '<test-case name="test name 2" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="1">\n<failure><message>why oh why\n</message></failure>\n</test-case>'
    actual = nunitresults.get_test_case_results(results)
    assert expected0 == actual[0]
    assert expected1 == actual[1]


def test_convert_to_nunit_results_format(mocker):
    x = '{"tags": {"opId": "ServerBackend-f421e441fa310430","browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","orgId": "1009391617598028","userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36","clusterId": "0216-124733-lone970","user": "eter.natus@galar.com","principalIdpObjectId": "71b45910-e7b4-44d8-82f7-bf6fac4630d0","browserHostName": "uksouth.azuredatabricks.net","parentOpId": "RPCClient-bb9b9591c29c01f7","jettyRpcType": "InternalDriverBackendMessages$DriverBackendRequest"},"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    t = ("2020-9-13", "13:20:16")
    mocker.patch("runeatest.utils.get_date_and_time", return_value=t)
    results = []
    results.append(
        testreporter.add_testcase(
            "test name",
            False,
            "this description describes the test",
            "this test has failed",
        )
    )
    results.append(
        testreporter.add_testcase(
            "test name 2",
            False,
            "this description describes the test",
            "this test has also failed",
        )
    )
    expected = '<test-results name="/Users/lorem.ipsum@fake.io/runeatest" total="2" date="2020-9-13" time="13:20:16">\n<environment nunit-version="2.6.0.12035" clr-version="2.0.50727.4963" os-version="uksouth.azuredatabricks.net" platform="Win32NT" cwd="C:\\Program Files\\NUnit 2.6\\bin\\" machine-name="0216-124733-lone970" user="eter.natus@galar.com" user-domain="1009391617598028"/>\n<culture-info current-culture="en-US" current-uiculture="en-US"/>\n<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="0"><results>\n<test-case name="test name" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="1">\n<failure><message>this test has failed\n</message></failure>\n</test-case>\n<test-case name="test name 2" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="1">\n<failure><message>this test has also failed\n</message></failure>\n</test-case>\n</results>\n</test-suite>\n</test-results>'
    actual = nunitresults.convert_to_nunit_results_format(results)
    assert expected == actual


def test_get_test_case_results_all_pass_different_notebookpaths(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(
        testreporter.add_testcase(
            "test name", True, "this description describes the test"
        )
    )
    y = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/eternatus"}}'
    context = json.loads(y)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)

    results.append(
        testreporter.add_testcase(
            "test name 2", True, "this description describes the test"
        )
    )
    expected0 = '<test-case name="test name" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="success" success="True" time="0.000" asserts="1"/>'
    expected1 = '<test-case name="test name 2" description="this description describes the test" classname="/Users/lorem.ipsum@fake.io/eternatus" executed="True" result="success" success="True" time="0.000" asserts="1"/>'
    actual = nunitresults.get_test_case_results(results)
    assert expected0 == actual[0]
    assert expected1 == actual[1]
