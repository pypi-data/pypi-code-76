def OcttoHex(n):
    if isinstance(n, str) != True:
        n1 = str(n)
        decnum = int(n1,8)
        hexnum = hex(decnum)[2:]
        return hexnum.upper()
    else:
        decnum = int(n, 8)
        hexnum = hex(decnum)[2:]
        return hexnum.upper()
