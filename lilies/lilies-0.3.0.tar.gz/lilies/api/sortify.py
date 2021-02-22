from ..base_utils import wilt


def sortify(iter, case_insensitive=True):
    if case_insensitive:

        def sortkey(s):
            return wilt(s).lower()

    else:
        sortkey = wilt
    return sorted(list(iter), key=sortkey)
