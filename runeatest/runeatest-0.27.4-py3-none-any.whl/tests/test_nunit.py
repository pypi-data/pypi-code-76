import pytest
import json
from runeatest import nunit
from runeatest import pysparkconnect
from runeatest import utils
from runeatest import testreporter


def test_get_nunit_header(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    t = ("2020-9-13", "13:20:16")
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    mocker.patch("runeatest.utils.get_date_and_time", return_value=t)
    results = []
    results.append(testreporter.add_testcase("test name", False))
    results.append(testreporter.add_testcase("test name 2", True))
    expected = '<test-results name="/Users/lorem.ipsum@fake.io/runeatest" total="2" date="2020-9-13" time="13:20:16">\n<environment nunit-version="2.6.0.12035" clr-version="2.0.50727.4963" os-version="Microsoft Windows NT 6.1.7600.0" platform="Win32NT" cwd="C:\\Program Files\\NUnit 2.6\\bin\\" machine-name="dummymachine" user="dummyuser" user-domain="dummy"/>\n<culture-info current-culture="en-US" current-uiculture="en-US"/>'
    actual = nunit.get_nunit_header(results, context)
    assert expected == actual


def test_get_nunit_footer():
    expected = "</results>\n</test-suite>\n</test-results>"
    actual = nunit.get_nunit_footer()
    assert expected == actual


def test_get_test_suite_result_one_passed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", True))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="success" success="True" time="0.000" asserts="0"><results>'
    actual = nunit.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_suite_result_one_failed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", False))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="0"><results>'
    actual = nunit.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_suite_result_one_failed_one_passed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", False))
    results.append(testreporter.add_testcase("test name 2", True))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="0"><results>'
    actual = nunit.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_suite_result_one_passed_one_failed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", False))
    results.append(testreporter.add_testcase("test name 2", True))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="0"><results>'
    actual = nunit.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_suite_result_all_failed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", False))
    results.append(testreporter.add_testcase("test name 2", False))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="0"><results>'
    actual = nunit.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_suite_result_all_passed(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    results = []
    results.append(testreporter.add_testcase("test name", True))
    results.append(testreporter.add_testcase("test name 2", True))
    expected = '<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="success" success="True" time="0.000" asserts="0"><results>'
    actual = nunit.get_test_suite_results(results, context)
    assert expected == actual


def test_get_test_case_results_one_failure():
    results = []
    results.append(testreporter.add_testcase("test name", False))
    expected = '<test-case name="test name" description="" executed="True" result="failure" success="False" time="0.000" asserts="1">\n<failure>\n</failure>\n</test-case>'
    actual = nunit.get_test_case_results(results)
    assert expected == actual[0]


def test_get_test_case_results_one_pass():
    results = []
    results.append(testreporter.add_testcase("test name", True))
    expected = '<test-case name="test name" description="" executed="True" result="success" success="True" time="0.000" asserts="1"/>'
    actual = nunit.get_test_case_results(results)
    assert expected == actual[0]


def test_get_test_case_results_one_pass_one_fail():
    results = []
    results.append(testreporter.add_testcase("test name", True))
    results.append(testreporter.add_testcase("test name 2", False))
    expected0 = '<test-case name="test name" description="" executed="True" result="success" success="True" time="0.000" asserts="1"/>'
    expected1 = '<test-case name="test name 2" description="" executed="True" result="failure" success="False" time="0.000" asserts="1">\n<failure>\n</failure>\n</test-case>'
    actual = nunit.get_test_case_results(results)
    assert expected0 == actual[0]
    assert expected1 == actual[1]


def test_get_test_case_results_all_pass():
    results = []
    results.append(testreporter.add_testcase("test name", True))
    results.append(testreporter.add_testcase("test name 2", True))
    expected0 = '<test-case name="test name" description="" executed="True" result="success" success="True" time="0.000" asserts="1"/>'
    expected1 = '<test-case name="test name 2" description="" executed="True" result="success" success="True" time="0.000" asserts="1"/>'
    actual = nunit.get_test_case_results(results)
    assert expected0 == actual[0]
    assert expected1 == actual[1]


def test_get_test_case_results_all_fail():
    results = []
    results.append(testreporter.add_testcase("test name", False))
    results.append(testreporter.add_testcase("test name 2", False))
    expected0 = '<test-case name="test name" description="" executed="True" result="failure" success="False" time="0.000" asserts="1">\n<failure>\n</failure>\n</test-case>'
    expected1 = '<test-case name="test name 2" description="" executed="True" result="failure" success="False" time="0.000" asserts="1">\n<failure>\n</failure>\n</test-case>'
    actual = nunit.get_test_case_results(results)
    assert expected0 == actual[0]
    assert expected1 == actual[1]


def test_convert_to_nunit_results_format(mocker):
    x = '{"extraContext":{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}}'
    context = json.loads(x)
    mocker.patch("runeatest.pysparkconnect.get_context", return_value=context)
    t = ("2020-9-13", "13:20:16")
    mocker.patch("runeatest.utils.get_date_and_time", return_value=t)
    results = []
    results.append(testreporter.add_testcase("test name", False))
    results.append(testreporter.add_testcase("test name 2", False))
    expected = '<test-results name="/Users/lorem.ipsum@fake.io/runeatest" total="2" date="2020-9-13" time="13:20:16">\n<environment nunit-version="2.6.0.12035" clr-version="2.0.50727.4963" os-version="Microsoft Windows NT 6.1.7600.0" platform="Win32NT" cwd="C:\\Program Files\\NUnit 2.6\\bin\\" machine-name="dummymachine" user="dummyuser" user-domain="dummy"/>\n<culture-info current-culture="en-US" current-uiculture="en-US"/>\n<test-suite type="TestFixture" name="/Users/lorem.ipsum@fake.io/runeatest" executed="True" result="failure" success="False" time="0.000" asserts="0"><results>\n</results>\n</test-suite>\n</test-results>'
    actual = nunit.convert_to_nunit_results_format(results)
    assert expected == actual
