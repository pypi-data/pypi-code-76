from .alphabetic_number import alpha_to_number

ALPHA_TO_NUMBER_TEST_CASE = {
    'ABC': 731,
    'CBA': 2081,
    'DRL': 3184,
    'AA': 27,
    'AB': 28,
    'A': 1,
    'Z': 26
}


def alpha_to_number_test():
    for case in ALPHA_TO_NUMBER_TEST_CASE.keys():
        print(f'test case {case}')
        try:
            received = alpha_to_number(case)
            expected = ALPHA_TO_NUMBER_TEST_CASE[case]
            assert received == expected
        except AssertionError:
            raise print(f'failed test: {case} | expected: {expected} | received: {received}')


if __name__ == '__main__':
    alpha_to_number_test()