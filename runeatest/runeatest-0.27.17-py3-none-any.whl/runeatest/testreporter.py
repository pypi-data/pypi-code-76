def add_testcase(name, issuccess, failurereason=""):
    return {
        "test": name,
        "issuccess": str(issuccess),
        "result": (get_result(issuccess)),
        "failurereason": (get_failurereason(issuccess, failurereason)),
    }


def get_result(issuccess):
    if issuccess:
        return str("success")
    else:
        return str("failure")


def get_failurereason(issuccess, failurereason):
    if issuccess and len(failurereason) > 0:
        raise Exception("Sorry, no failure reason can be added if test is successful")
    else:
        return str(failurereason)
