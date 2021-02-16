def add_testcase(name, issuccess):
    return {
        "test": name,
        "issuccess": str(issuccess),
        "result": (get_result(issuccess)),
    }


def get_result(issuccess):
    if issuccess:
        return str("success")
    else:
        return str("failure")
