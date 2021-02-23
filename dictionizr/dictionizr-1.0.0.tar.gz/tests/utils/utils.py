
def eq(a, b) -> bool:
    if a is None and b is None:
        return True
    elif a is None or b is None:
        return False

    try:
        a_vars = vars(a) 
        b_vars = vars(b)
        if len(a_vars) != len(b_vars):
            return False

        for a_key, a_value in a_vars.items():
            b_value = b_vars[a_key]
            if not eq(a_value, b_value):
                return False
        return True
    except TypeError:
        if isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                return False
            a = sorted(a)
            b = sorted(b)
            for index, a_value in enumerate(a):
                b_value = b[index]
                if not eq(a_value, b_value):
                    return False
            return True

        return a == b