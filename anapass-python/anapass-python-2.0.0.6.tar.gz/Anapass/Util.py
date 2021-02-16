

class WorkAgent :
    def __init__(this):
        this.__IsBreak = False
        this.__IsStart = False
        this.__IsStop = False
        this.__MaxValue = 0
        this.__MinValue = 0
        this.__CurValue = 0

    def Start(this) :
        this.__IsStart = True

    def Stop(this) :
        this.__IsStop = True

    def IsStop(this) :
        return this.__IsStop;

    def SetMaxValue(this, v) :
        this.__MaxValue = v

    def GetMaxValue(this) :
        return this.__MaxValue

    def SetMinValue(this, v) :
        this.__MinValue = v

    def SetCurValue(this, v) :
        this.__CurValue = v

    def GetCurValue(this) :
        return this.__CurValue

    def IncCurValue(this, incV) :
        this.__CurValue += incV


class Print :
    def ListHex(startMemAddr, list) :
        lineByte = 16
        i = 0
        strline = ""
        for v in list :
            strline += "0x%02X "%v
            if (i+1)%lineByte == 0 :
                j = ((int)(i/lineByte)*lineByte) + startMemAddr
                print("0x%08X : "%  j, strline)
                strline=""
            i += 1
        if len(strline) > 0 :
            j = ((int)(i/lineByte)*lineByte) + startMemAddr
            print("0x%08X : "% j , strline)


def ListCopy(list1, startIdx1, list2, startIdx2, copyCount) :
    for i in range(copyCount) :
        list1[startIdx1 + i] = list2[startIdx2 + i]

def ListCopyExam() :
    list1 = [1, 2, 3, 4, 5, 6]
    list2 = [33, 44, 55]
    print("list1= ", list1)
    print("list2= ", list2)
    Util.ListCopy(list1, 2, list2, 0, 3)
    print("list1= ", list1)
    print("list2= ", list2)


class List :
    def ToHexString(list) :
        strList = ""
        for v in list :
            strList += "0x%02X "%v
        return strList            

