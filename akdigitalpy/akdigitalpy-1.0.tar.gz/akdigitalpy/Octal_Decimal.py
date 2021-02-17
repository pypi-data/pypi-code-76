def OcttoDec(n):
    if isinstance(n, str) != True:
        n1 = str(n)
        decnum = int(n1,8)
        return decnum
    else:
        decnum1 = int(n, 8)
        return decnum1
