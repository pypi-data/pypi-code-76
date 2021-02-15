import pathlib
import dataclasses
import typing
from . import data_parser

BASE_DIR = pathlib.Path(__file__).resolve().parent

mod_rules = data_parser.ModRules.from_file(BASE_DIR / "data" / "weights.txt")
code_subs = data_parser.CodeSubstitutions.from_file(BASE_DIR / "data" / "subs.txt")

def calc_mod_dblal(weighted_sort_code_parts, weighted_account_number_parts, rule: data_parser.ModRule):
    weighted_sort_code_digits = [int(d) for x in weighted_sort_code_parts for d in str(x)]
    weighted_account_number_digits = [int(d) for x in weighted_account_number_parts for d in str(x)]

    weighted_sum = sum(weighted_sort_code_digits + weighted_account_number_digits)

    if rule.exception == 1:
        weighted_sum += 27

    remainder = weighted_sum % 10
    return remainder

def calc_mod10(weighted_sort_code_parts, weighted_account_number_parts, rule: data_parser.ModRule):
    weighted_sum = sum(weighted_sort_code_parts + weighted_account_number_parts)
    remainder = weighted_sum % 10
    return remainder

def calc_mod11(weighted_sort_code_parts, weighted_account_number_parts, rule: data_parser.ModRule):
    weighted_sum = sum(weighted_sort_code_parts + weighted_account_number_parts)
    remainder = weighted_sum % 11
    return remainder

def calc_mod(sort_code: int, account_number: int, rule: data_parser.ModRule, exception_14=False):
    if rule.exception == 5:
        new_sort_code = code_subs.find_substitution(sort_code)
        if new_sort_code is not None:
            sort_code = new_sort_code

    sort_code_parts = [int(x) for x in list(str(sort_code).rjust(6, "0"))]
    account_number_parts = [int(x) for x in list(str(account_number).rjust(8, "0"))]

    if exception_14:
        if account_number_parts[7] not in (0, 1, 9):
            return False
        else:
            account_number_parts = [
                0,
                account_number_parts[0],
                account_number_parts[1],
                account_number_parts[2],
                account_number_parts[3],
                account_number_parts[4],
                account_number_parts[5],
                account_number_parts[6]
            ]

    weighted_sort_code_parts = [
        sort_code_parts[0] * rule.weights.u,
        sort_code_parts[1] * rule.weights.v,
        sort_code_parts[2] * rule.weights.w,
        sort_code_parts[3] * rule.weights.x,
        sort_code_parts[4] * rule.weights.y,
        sort_code_parts[5] * rule.weights.z,
    ]
    weighted_account_number_parts = [
        account_number_parts[0] * rule.weights.a,
        account_number_parts[1] * rule.weights.b,
        account_number_parts[2] * rule.weights.c,
        account_number_parts[3] * rule.weights.d,
        account_number_parts[4] * rule.weights.e,
        account_number_parts[5] * rule.weights.f,
        account_number_parts[6] * rule.weights.g,
        account_number_parts[7] * rule.weights.h,
    ]

    if rule.exception == 2 and account_number_parts[0] != 0:
        if account_number_parts[6] == 9:
            weighted_sort_code_parts = [0, 0, 0, 0, 0, 0]
            weighted_account_number_parts = [
                0,
                0,
                account_number_parts[2] * 8,
                account_number_parts[3] * 7,
                account_number_parts[4] * 10,
                account_number_parts[5] * 9,
                account_number_parts[6] * 3,
                account_number_parts[7] * 1,
            ]
        else:
            weighted_sort_code_parts = [
                0,
                0,
                sort_code_parts[2],
                sort_code_parts[3] * 2,
                sort_code_parts[4] * 5,
                sort_code_parts[5] * 3,
            ]
            weighted_account_number_parts = [
                account_number_parts[0] * 6,
                account_number_parts[1] * 4,
                account_number_parts[2] * 8,
                account_number_parts[3] * 7,
                account_number_parts[4] * 10,
                account_number_parts[5] * 9,
                account_number_parts[6] * 3,
                account_number_parts[7] * 1,
            ]

    if rule.exception == 10:
        if account_number_parts[0] in (0, 9) and account_number_parts[1] == 9 and account_number_parts[6] == 9:
            weighted_sort_code_parts = [0, 0, 0, 0, 0, 0]
            weighted_account_number_parts[0] = 0
            weighted_account_number_parts[1] = 0
    elif rule.exception == 6:
        if account_number_parts[0] in (4, 5, 6, 7, 8) and account_number_parts[6] == account_number_parts[7]:
            return True
    elif rule.exception == 7:
        if account_number_parts[6] == 9:
            weighted_sort_code_parts = [0, 0, 0, 0, 0, 0]
            weighted_account_number_parts[0] = 0
            weighted_account_number_parts[1] = 0

    if rule.mod_mode == data_parser.ModMode.DblAl:
        if rule.exception == 3:
            if account_number_parts[2] in (6, 9):
                return True
        remainder = calc_mod_dblal(weighted_sort_code_parts, weighted_account_number_parts, rule)
    elif rule.mod_mode == data_parser.ModMode.Mod10:
        remainder = calc_mod10(weighted_sort_code_parts, weighted_account_number_parts, rule)
    elif rule.mod_mode == data_parser.ModMode.Mod11:
        remainder = calc_mod11(weighted_sort_code_parts, weighted_account_number_parts, rule)

    if rule.exception == 4:
        check_digit = int(f"{account_number_parts[6]}{account_number_parts[7]}")
        return remainder == check_digit
    elif rule.exception == 5:
        if rule.mod_mode == data_parser.ModMode.Mod11:
            if remainder == 0 and account_number_parts[6] == 0:
                return True
            elif remainder == 1:
                return False
            else:
                return 11 - remainder == account_number_parts[6]
        else:
            if remainder == 0 and account_number_parts[7] == 0:
                return True
            else:
                return 10 - remainder == account_number_parts[7]
    else:
        return remainder == 0


@dataclasses.dataclass
class ValidationResult:
    result: bool
    known_sort_code: bool
    substitute_sort_code: typing.Optional[int]


def validate(sort_code: int, account_number: int) -> ValidationResult:
    sort_code_rules = mod_rules.find_rule(sort_code)

    if not len(sort_code_rules):
        return ValidationResult(
            result=True,
            known_sort_code=False,
            substitute_sort_code=None
        )

    exception_2_9 = False
    exception_10_11 = False
    exception_12_13 = False
    if len(sort_code_rules) >= 2:
        if sort_code_rules[0].exception == 2 and sort_code_rules[1].exception == 9:
            exception_2_9 = True
        if sort_code_rules[0].exception == 10 and sort_code_rules[1].exception == 11:
            exception_10_11 = True
        if sort_code_rules[0].exception == 12 and sort_code_rules[1].exception == 13:
            exception_12_13 = True

    for rule in sort_code_rules:
        if rule.exception == 9:
            mod_pass = calc_mod(309634, account_number, rule)
            if mod_pass:
                return ValidationResult(
                    result=True,
                    known_sort_code=True,
                    substitute_sort_code=309634,
                )
        else:
            mod_pass = calc_mod(sort_code, account_number, rule)
        if exception_10_11 or exception_12_13 or exception_2_9:
            if mod_pass:
                return ValidationResult(
                    result=True,
                    known_sort_code=True,
                    substitute_sort_code=None
                )
        elif rule.exception == 14:
            if mod_pass:
                return ValidationResult(
                    result=True,
                    known_sort_code=True,
                    substitute_sort_code=None
                )
            else:
                mod_pass = calc_mod(sort_code, account_number, rule, exception_14=True)
                return ValidationResult(
                    result=mod_pass,
                    known_sort_code=True,
                    substitute_sort_code=None
                )
        else:
            if not mod_pass:
                return ValidationResult(
                    result=False,
                    known_sort_code=True,
                    substitute_sort_code=None
                )

    if exception_10_11 or exception_12_13 or exception_2_9:
        return ValidationResult(
            result=False,
            known_sort_code=True,
            substitute_sort_code=None
        )
    else:
        return ValidationResult(
            result=True,
            known_sort_code=True,
            substitute_sort_code=None
        )