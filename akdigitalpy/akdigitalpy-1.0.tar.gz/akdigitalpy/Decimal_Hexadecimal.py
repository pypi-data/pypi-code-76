def DectoHex(n):
    if isinstance(n,int) == True:
        hexnum = hex(n)[2:]
        return hexnum.upper()
    else:
        intnum = int(n)
        hexnum = hex(intnum)[2:]
        return hexnum.upper()


