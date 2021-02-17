def DectoOct(n):
    if isinstance(n, int) == True:
        octnum = oct(n)[2:]
        return octnum
    else:
        intnum = int(n)
        octnum = oct(intnum)[2:]
        return octnum





