from runeatest import pysparkconnect


def add_testcase(name, issuccess, testdescription="", failurereason=""):
    context = pysparkconnect.get_context()
    return {
        "test": name,
        "issuccess": str(issuccess),
        "description": str(testdescription),
        "classname": (context["extraContext"]["notebook_path"]),
        "result": (get_result(issuccess)),
        "failurereason": str(failurereason),
    }


def get_result(issuccess):
    if issuccess:
        return str("success")
    else:
        return str("failure")
