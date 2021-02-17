def TwosComplementOf(n):
        if isinstance(n,str)  == True:
                binintnum = int(n)
                binmun = int("{0:08b}".format(binintnum))
                strnum = str(binmun)
                size =  len(strnum)
                idx = size -1
                while idx >= 0:
                        if strnum[idx] == '1':
                                break
                        idx = idx - 1
                if idx == -1:
                        return '1'+strnum
                position = idx-1

                while position >= 0:
                        if strnum[position] == '1':
                                strnum = list(strnum)
                                strnum[position] ='0'
                                strnum = ''.join(strnum)
                        else:
                                strnum = list(strnum)
                                strnum[position] = '1'
                                strnum = ''.join(strnum)
                        position = position-1
                return strnum
        else:
                binmun = int("{0:08b}".format(n))
                strnum = str(binmun)
                size = len(strnum)
                idx = size - 1
                while idx >= 0:
                        if strnum[idx] == '1':
                                break
                        idx = idx - 1
                if idx == -1:
                        return '1' + strnum
                position = idx - 1

                while position >= 0:
                        if strnum[position] == '1':
                                strnum = list(strnum)
                                strnum[position] = '0'
                                strnum = ''.join(strnum)
                        else:
                                strnum = list(strnum)
                                strnum[position] = '1'
                                strnum = ''.join(strnum)
                        position = position - 1
                return strnum







