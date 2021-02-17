def HextoBin(n):
    if isinstance(n,str) == False:
        strnum = str(n)
        hexnum = int(strnum,16)
        binnum = bin(hexnum)
        return binnum
    else:
        hexnum = int(n, 16)
        binnum = bin(hexnum)
        return binnum


