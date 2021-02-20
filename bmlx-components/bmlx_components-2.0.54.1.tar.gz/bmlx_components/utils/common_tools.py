BYTES_MAP = {
    "TB": 40,
    "GB": 30,
    "MB": 20,
    "KB": 10,
    "B" :  1,
}
def digit_to_bytescount(digit: int):
    assert digit >= 0
    for i in BYTES_MAP:
        v = digit >> BYTES_MAP[i]
        if v:
            res = float(digit) / (1 << BYTES_MAP[i])
            return ("%.1f(%s)" % (res, i))
    return "0(B)"