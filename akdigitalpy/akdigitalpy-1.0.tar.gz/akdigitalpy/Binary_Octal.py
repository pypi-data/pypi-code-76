def BintoOct(num):
    if isinstance(num,str) == False:
        strnum = str(num)
        Binnum = int(strnum,2)
        octnum = oct(Binnum)[2:]
        return octnum
    else:
        Binnum = int(num, 2)
        octnum = oct(Binnum)[2:]
        return octnum



