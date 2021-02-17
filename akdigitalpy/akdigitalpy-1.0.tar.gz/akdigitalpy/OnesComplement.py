def OnesComplementOf(n):
    if isinstance(n, str) == True:
        binintnum = int(n)
        binmun = int("{0:08b}".format(binintnum))
        strnum = str(binmun)
        size = len(strnum)
        for i in range(0,size):
            if strnum[i] == '1':
                strnum = list(strnum)
                strnum[i] = '0'
                strnum = ''.join(strnum)
            else:
                strnum = list(strnum)
                strnum[i] = '1'
                strnum = ''.join(strnum)
        return strnum
    else:
        binmun = int("{0:08b}".format(n))
        strnum = str(binmun)
        size = len(strnum)
        for i in range(0, size):
            if strnum[i] == '1':
                strnum = list(strnum)
                strnum[i] = '0'
                strnum = ''.join(strnum)
            else:
                strnum = list(strnum)
                strnum[i] = '1'
                strnum = ''.join(strnum)
        return strnum

