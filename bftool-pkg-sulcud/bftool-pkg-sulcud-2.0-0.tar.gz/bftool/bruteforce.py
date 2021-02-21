import itertools

from .bftool_types import SpecialGenerator

__all__ = ["bruteforce_wordlist"]


# elements, minlength, maxlength
def _bruteforce_wordlist(rule: dict):
    for length in range(rule["minlength"], rule["maxlength"] + 1):
        for product in itertools.product(rule["elements"], repeat=length):
            if rule.get("string-join"):
                yield "".join(str(element) for element in product)
            else:
                try:
                    _ = product[1]
                    yield product
                except IndexError:
                    yield product[0]


def bruteforce_wordlist(rule: dict):
    return SpecialGenerator(_bruteforce_wordlist, rule)
