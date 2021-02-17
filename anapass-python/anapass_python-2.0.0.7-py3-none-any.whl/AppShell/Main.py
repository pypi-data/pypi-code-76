from Anapass.TModule import *
from Anapass.AppShell import AppClass
from Anapass.AppShell import CommandTFlash


def TestFunc1(app, strArg) :
   print("TestFunc1= ", strArg)

def TestFunc2(app, strArg) :
   print("TestFunc2= ", strArg)

app = AppClass.AppGlobal()    
app.SetChipType(TChip.Type.ANA6705)
#app.SetChipType(TChip.Type.ANA6706)

PROMPT="TEDTools>> "

print("----------------------------------------------------")
print("App: Python MyShell")
print("----------------------------------------------------")

shellCmd = AppClass.ShellCommand()
#shellCmd.Add("Test1", TestFunc1, "TestFunc1")
#shellCmd.Add("Test2", TestFunc1, "TestFunc2")
shellCmd.Add("Flash", CommandTFlash.Main, "Flash Memory Read/Write")

for shellItem in shellCmd :
    print(shellItem)

while True : 
    print(PROMPT, end='')
    str = input()
    #print("Input=[" + str + "]")
    strlist = str.split(' ')
    
    if( (strlist[0] == 'exit') and (len(strlist)==1) ) :
        break

    cmd=""
    argIdx = 0
    listArg=list()
    for s in strlist :
        if len(s) != 0 :
            if argIdx == 0 :
                cmd = s.lower()
                argIdx += 1
            else :
                listArg.append(s.lower())
    tupleArg = tuple(listArg)
    if len(cmd) > 0 :
        if cmd == 'help' or cmd == '?' : 
            shellCmd.PrintHelp()
        else :
            isCmdRun = False
            for shellItem in shellCmd :
                if shellItem.Run(app, cmd, tupleArg) == True :
                    isCmdRun = True
                    break

            if isCmdRun == False :
                print("Can't find command")
