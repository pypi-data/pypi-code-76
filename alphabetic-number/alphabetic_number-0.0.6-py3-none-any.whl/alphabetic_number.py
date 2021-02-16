from string import ascii_uppercase


def number_to_alpha(num: int) -> str:
    if num // 26 == 0:
        return ascii_uppercase[num - 1]
    return number_to_alpha(num // 26) + ascii_uppercase[num % 26 - 1]


def alpha_to_number(alpha_num: str, digit_pointer: int = 0) -> int:
    def processor(alpha_num):
        if len(alpha_num) == 1:
            return ascii_uppercase.index(alpha_num[digit_pointer]) + 1
        return (ascii_uppercase.index(alpha_num[digit_pointer]) + 1) * 26 ** (len(alpha_num) - 1) + processor(alpha_num[1:])

    return processor(alpha_num.upper())
