#!/usr/bin/python
import psutil
import random
import time
try:
    import httplib
except:
    import http.client as httplib
def setrandomhi():
    randhi=["Hello ","Heyo ","Hiiiiiii "]
    return randhi[random.randint(0,2)]
def internetcon():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

def main():
    mainmsg=""+setrandomhi()
    mainmsg+=psutil.Process().username()+"! "

    #Memory

    if psutil.virtual_memory().available * 100 / psutil.virtual_memory().total < 30:
        mainmsg+="I'm kinda feeling overwhelmed... Why not kill some program's that you are not using? "
    elif psutil.virtual_memory().available * 100 / psutil.virtual_memory().total > 30 and psutil.virtual_memory().available * 100 / psutil.virtual_memory().total < 80:
        mainmsg+="I'm feeling awesome today! "
    else:
        mainmsg+="Kinda feeling bored. "

    #Battery

    battery=psutil.sensors_battery()
    if battery.power_plugged:
        mainmsg+=""
    else:
        bpercent=battery.percent
        if bpercent<=30:
            mainmsg+="And, do you see the charger cable lying somewhere near? "
        elif bpercent<=20:
            mainmsg+="I- am- dying... CHARGE MEEEEEE! "
        else:
            mainmsg+=""

    #Network

    if internetcon() :
        mainmsg+=""
    else:
        internetno=["btw are you and the internet having a fight? ","btw psst, connect me to internet. UwU "]
        mainmsg+=internetno[random.randint(0,1)]

    #Uptime

    seconds=int(time.time() - psutil.boot_time())
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    if hour>15:
        mainmsg+="Also do you mind giving me a shutdown or restart? Pleaseuwu? "
    elif hour>24:
        mainmsg+="Give. Me. Some. Break. REEEEE"
    else:
        mainmsg+=""

    #For user

    usrmsg=["How's you tho? And, don't forget to drink water. ","How are you on this fine day? ","Give your eyes some rest!! "]
    mainmsg+=usrmsg[random.randint(0,2)]

    print(mainmsg)
    exit(0)

if __name__=="__main__":
    main()

