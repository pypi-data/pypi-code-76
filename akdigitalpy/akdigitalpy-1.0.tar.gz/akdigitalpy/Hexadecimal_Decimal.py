def HextoDec(n):
    if isinstance(n, str) == False:
        strnum = str(n)
        decnum = int(strnum,16)
        return decnum
    else:
        decnum = int(n, 16)
        return decnum
