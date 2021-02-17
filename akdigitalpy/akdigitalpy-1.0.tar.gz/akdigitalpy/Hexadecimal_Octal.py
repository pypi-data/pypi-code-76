def HextoOct(n):
    if isinstance(n,str) == False:
        strnum = str(n)
        hexnum = int(strnum,16)
        octnum = oct(hexnum)[2:]
        return octnum
    else:
        hexnum = int(n, 16)
        octnum = oct(hexnum)[2:]
        return octnum



