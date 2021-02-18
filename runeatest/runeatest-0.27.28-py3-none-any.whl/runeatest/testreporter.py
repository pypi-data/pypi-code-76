def add_testcase(name, issuccess, failurereason=""):
    return {
        "test": name,
        "issuccess": str(issuccess),
        "result": (get_result(issuccess)),
        "failurereason": str(failurereason),
    }


def get_result(issuccess):
    if issuccess:
        return str("success")
    else:
        return str("failure")
