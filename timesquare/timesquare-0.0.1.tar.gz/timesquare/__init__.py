import math

def solve(a, b, c):
    # +
    aa = (b * b) - (4 * a * c)
    if aa < 0:
        aa = aa * -1
    bb = math.sqrt(aa)
    cc = (b * -1) + bb
    try:
        dd = cc / (2 * a)
    except:
        raise Exception("a Variable can not be 0!")
    global x1
    x1 = dd
    # -
    aa = (b * b) - (4 * a * c)
    if aa < 0:
        aa = aa * -1
    bb = math.sqrt(aa)
    cc = (b * -1) - bb
    try:
        dd = cc / (2 * a)
    except:
        raise Exception("a Variable can not be 0!")
    global x2
    x2 = dd
    return x1, x2
