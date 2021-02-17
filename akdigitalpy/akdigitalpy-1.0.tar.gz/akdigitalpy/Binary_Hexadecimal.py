def BintoHex(num):
    if isinstance(num, str) == False:
        strnum = str(num)
        Binnum = int(strnum, 2)
        hexnum = hex(Binnum)[2:]
        return hexnum.upper()
    else:
        Binnum = int(num, 2)
        hexnum = hex(Binnum)[2:]
        return hexnum.upper()


