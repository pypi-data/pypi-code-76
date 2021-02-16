from runeatest import pysparkconnect
from runeatest import utils


def get_nunit_header(results, context):
    total = str(len(results))
    now = utils.get_date_and_time()
    print(now)
    now_date = now[0]
    now_time = now[1]
    nunit_header = '<test-results name="##name##" total="##total##" date="##getdate##" time="##gettime##">\n<environment nunit-version="2.6.0.12035" clr-version="2.0.50727.4963" os-version="##browserHostName##" platform="Win32NT" cwd="C:\\Program Files\\NUnit 2.6\\bin\\" machine-name="##dummymachine##" user="##dummyuser##" user-domain="##orgid##"/>\n<culture-info current-culture="en-US" current-uiculture="en-US"/>'
    nunit_header = (
        nunit_header.replace("##name##", context["extraContext"]["notebook_path"])
        .replace("##total##", total)
        .replace("##getdate##", now_date)
        .replace("##gettime##", now_time)
        .replace("##dummymachine##", context["tags"]["clusterId"])
        .replace("##dummyuser##", context["tags"]["user"])
        .replace("##orgid##", context["tags"]["orgId"])
        .replace("##browserHostName##", context["tags"]["browserHostName"])
    )
    return nunit_header


def get_test_suite_results(results, context):
    test_suite_result = "success"
    test_suite_success = "True"
    for result in results:
        if result["result"] == "failure":
            test_suite_result = "failure"
            test_suite_success = "False"
    test_suite = '<test-suite type="TestFixture" name="##name##" executed="True" result="##test_suite_result##" success="##test_suite_success##" time="0.000" asserts="0"><results>'
    test_suite = (
        test_suite.replace("##name##", context["extraContext"]["notebook_path"])
        .replace("##test_suite_result##", test_suite_result)
        .replace("##test_suite_success##", test_suite_success)
    )
    return test_suite


def get_test_case_results(results):
    test_cases = []
    for result in results:
        if result["result"] == "failure":
            test_case_result = '<test-case name="##test##" description="" executed="True" result="##result##" success="##issuccess##" time="0.000" asserts="1">\n<failure><message>##failure##\n</message></failure>\n</test-case>'
        elif result["result"] == "success":
            test_case_result = '<test-case name="##test##" description="" executed="True" result="##result##" success="##issuccess##" time="0.000" asserts="1"/>'
        test_case_result = (
            test_case_result.replace("##test##", result["test"])
            .replace("##result##", result["result"])
            .replace("##issuccess##", result["issuccess"])
            .replace("##failure##", result["failurereason"])
        )
        test_cases.append(test_case_result)
    print(test_cases)
    return test_cases


def get_nunit_footer():
    nunit_footer = "</results>\n</test-suite>\n</test-results>"
    return nunit_footer


def convert_to_nunit_results_format(results):
    context = pysparkconnect.get_context()
    header = get_nunit_header(results, context)
    suite = get_test_suite_results(results, context)
    test_cases = get_test_case_results(results)
    footer = get_nunit_footer()
    str_test_cases = "\n".join(test_cases)
    return header + "\n" + suite + "\n" + str_test_cases + "\n" + footer
