class UnhandledBoolType(Exception):
    pass


def to_bool(v):
    valid_responses = ["yes", "y", "true", "1", "valid"]
    invalid_responses = ["no", "n", "false", "0", "invalid"]
    try:
        v = v.lower()
    except AttributeError:
        v = str(v)

    if v in valid_responses:
        return True
    elif v in invalid_responses:
        return False
    else:
        raise UnhandledBoolType()


def list_to_string(s):
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += str(ele)

        # return string
    return str1


if __name__ == "__main__":
    import thompcoutils.test_utils as test_utils

    test_utils.test(to_bool, ["valid"], expected_value=True)
    test_utils.test(to_bool, ["invalid"], expected_value=False)
    test_utils.test(to_bool, ["Yes"], expected_value=True)
    test_utils.test(to_bool, ["No"], expected_value=False)
    test_utils.test(to_bool, ["y"], expected_value=True)
    test_utils.test(to_bool, ["n"], expected_value=False)
    test_utils.test(to_bool, ["True"], expected_value=True)
    test_utils.test(to_bool, ["FALSE"], expected_value=False)
    test_utils.test(to_bool, [1], expected_value=True)
    test_utils.test(to_bool, [0], expected_value=False)
    test_utils.test(to_bool, ["dd"], expected_value=False, expected_exception=UnhandledBoolType)

    try:
        to_bool(1)
    except UnhandledBoolType:
        raise Exception("Should not fail")
    try:
        to_bool(2)
    except UnhandledBoolType:
        "pased"