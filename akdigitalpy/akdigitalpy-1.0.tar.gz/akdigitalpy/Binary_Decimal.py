def BintoDec(num):
    if isinstance(num,int) == True:
        Strnum = str(num)
        decinum = int(Strnum, 2)
        return  decinum
    else:
        decinum = int(num, 2)
        return decinum

