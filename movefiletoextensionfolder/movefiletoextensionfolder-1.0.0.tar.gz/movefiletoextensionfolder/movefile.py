import os
import pyttsx3


def getExtName(file):
    return file.split(".")[-1]


def isDirOrFileExist(filePath):
    return os.path.exists(filePath)


def makeNewPath(filePath):
    # .jpg >> _copy.jpg
    splitWord = filePath.split(".")
    dotExt = '.' + splitWord[-1]
    renamedDotExt = "_copy" + dotExt
    newWord = filePath.replace(dotExt, renamedDotExt)
    return newWord


def voiceMsg(strVal):
    engine = pyttsx3.init()
    engine.setProperty('rate', 110)
    engine.setProperty('volume', 1)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(strVal)
    engine.runAndWait()


def rename(source, destination, file):
    try:
        os.rename(source, destination)
        print(file, " copied  Successfully")
    except Exception as e:
        print(file, " copied  Failed kindly close the file if Opened")
        print(e)


def isFiledCopiedFun(isFiledCopied):
    if isFiledCopied:
        return True


def moveFile(files, trgFol, pathVar):
    for file in files:
        ext = getExtName(file)
        extDirPath = trgFol + "\\" + ext

        filePath = extDirPath + "\\" + file
        src = pathVar + file

        isDirExist1 = isDirOrFileExist(extDirPath)
        print(filePath)
        if isDirExist1:
            if isDirOrFileExist(filePath):
                print(file, "file is already There")
                newFilePath = makeNewPath(filePath)
                rename(src, newFilePath, file)
            else:
                print(file, "file not Present wait moving......")
                rename(src, filePath, file)

        else:
            print("dir not present wait making for you ......")
            try:
                os.mkdir(extDirPath)
                print("dir created")
                rename(src, filePath, file)
            except Exception as e:
                print(e)
    size = len(files)

    if size > 0:
        strVal = "Hi Bhaskar All File Moved  Successfully"
        voiceMsg(strVal)
    else:
        print("No Files To Move Bhaskar bye bye ")




def movefilefromsourcetodestination(source, target):
    for path, dir, files in os.walk(source):
        moveFile(files, target, path)
        break
