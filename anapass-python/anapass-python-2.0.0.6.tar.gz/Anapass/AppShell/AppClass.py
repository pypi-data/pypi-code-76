from Anapass.TModule import *

class AppGlobal(object):

    def __init__(this):
        this.__ChipType = TChip.Type.Common
        this.__BoardType = TBoard.Type.Common
        this.__Device = TDevice(TDevice.Type.T5)
        isOk = this.__Device.Connect()
        if isOk != True :
            raise ConnectionRefusedError("Fail to connect to TDevice(%s)"%device.GetName())

    def GetDevice(this) :
        return this.__Device

    def GetChipType(this) :
        return this.__ChipType

    def SetChipType(this, chipType) :
        this.__ChipType = chipType


class ShellCommand :

    class ShellItem :
        def __init__(this, cmd, func, desc) :
            this.__Cmd = cmd
            this.__Func = func
            this.__Desc = desc

        def __repr__(this):
            str = this.__Cmd + "  " + this.__Desc
            return str

        def __str__(this) :
            str = this.__Cmd + "  " + this.__Desc
            return str

        def Run(this, app, cmd, strArg) :
            bRet = False
            str1 =cmd.lower()
            str2 =this.__Cmd.lower()
            if(str1 == str2) :
                bRet = True
                this.__Func(app, strArg)
            return bRet

    def __init__(this): 
        this.__Dictionary=dict()

    def Add(this, cmd, func, desc)  :
        item = ShellCommand.ShellItem(cmd, func, desc)
        this.__Dictionary[cmd] = item

    def PrintHelp(this) :
        for shellItem in this :
            print(shellItem)
   
    def __iter__(this) :
        this.__IterIndex = 0;
        return this

    def __next__(this) :
        if  this.__IterIndex >= len(this.__Dictionary) :
            raise StopIteration
        shellItem = list(this.__Dictionary.values())[this.__IterIndex];
        this.__IterIndex += 1;
        return shellItem





