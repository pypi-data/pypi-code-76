def OcttoBin(n):
    if isinstance(n, str) == True:
        num = int(n,8)
        binnum = bin(num)[2:]
        return binnum
    else:
        strnum = str(n)
        num = int(strnum, 8)
        binnum = bin(num)[2:]
        return binnum




