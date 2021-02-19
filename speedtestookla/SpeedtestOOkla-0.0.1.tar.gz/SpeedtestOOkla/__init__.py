import re
from sys import path
path.append(r"c:\Users\LTL4545\anaconda3\lib\site-packages")
path.append(r"C:\Program Files (x86)\TEMS\TEMS Investigation 21\Application\Lib\site-packages")

pip_install_argument = "install"
from uiautomator import device as d
from uiautomator import Device
import subprocess, platform
import time


packages_to_import = ["uiautomator", "subprocess", "time", "socket", "os", "platform"]

###############################################################################################
# In[2]: All Data
###############################################################################################
waittime = 3
iterate_limit = 2
start_time = 0
adbpath = "adb"
pakage = "org.zwanoo.android.speedtest.MainActivity"
DEVICE = 0



def devcss():
    devcs = subprocess.check_output(
        "{} devices".format(adbpath),
        stderr=subprocess.STDOUT,
        shell=True)
    tmpdev = devcs.decode('utf-8').strip()
    tmp = re.sub('[^A-Za-z0-9]+', '#', tmpdev)
    dev_serial = tmp.split("#")[4]
    return dev_serial


serial = devcss()
# print(serial)
dev = Device(serial)


def start_app(d):
    try:
        d.press.home()
        subprocess.check_output(
            "{} shell  monkey -p org.zwanoo.android.speedtest -c android.intent.category.LAUNCHER 1; exit 0".format(
                adbpath),
            stderr=subprocess.STDOUT,
            shell=True)
        print("OOKLA Speed test  ::", " app open successful")
        while True:
            if d(className="android.view.View", resourceId="org.zwanoo.android.speedtest:id/closeIcon").exists:
                d(className="android.view.View", resourceId="org.zwanoo.android.speedtest:id/closeIcon").click()
                time.sleep(2)
            if d(text="Connections").exists:
                d(text="Connections")
                break
            else:
                continue
        time.sleep(waittime)
    except Exception as e:
        try:
            print("error", e)
        except:
            pass


def start_tetsting_speed():
    print("Waiting for begin test", "Debug")
    while True:
        if d(className="android.view.View", resourceId="org.zwanoo.android.speedtest:id/go_button").exists:
            d(className="android.view.View", resourceId="org.zwanoo.android.speedtest:id/go_button").click()
            time.sleep(3)
            break
        else:
            continue



def download_result():
    while True:
        if d(className="android.view.View", resourceId="org.zwanoo.android.speedtest:id/shareIcon").exists:
            time.sleep(3)
            d(className="android.widget.FrameLayout", resourceId="org.zwanoo.android.speedtest:id/tab_results").click()
            time.sleep(3)
            d(className="android.view.ViewGroup", resourceId="org.zwanoo.android.speedtest:id/table_cell").click()
            time.sleep(3)
            download = d(className="android.widget.TextView", instance=3).info.get("text")
            time.sleep(3)
            downloadstring = d(className="android.widget.TextView", instance=4).info.get("text")
            time.sleep(3)
            print("|OKLA_DNLD|","#" + download + "#@" + downloadstring+"@")
            time.sleep(3)
            upload = d(className="android.widget.TextView", instance=7).info.get("text")
            time.sleep(3)
            uploadstring = d(className="android.widget.TextView", instance=8).info.get("text")
            time.sleep(3)
            print("|OKLA_UPLD|","#" + upload + "#@" + uploadstring+"@")
            time.sleep(3)
            ping = d(className="android.widget.TextView", instance=11).info.get("text")
            time.sleep(3)
            time.sleep(3)
            pingstring = d(className="android.widget.TextView", instance=12).info.get("text")
            time.sleep(3)
            print("|OKLA_TIME|","#" + ping + "#@" + pingstring+"@")
            time.sleep(3)
            jitter = d(className="android.widget.TextView", instance=14).info.get("text")
            time.sleep(3)
            jitterstring = d(className="android.widget.TextView", instance=15).info.get("text")
            time.sleep(3)
            print("|OKLA_JITR|","#" + jitter + "#@" + jitterstring+"@")
            time.sleep(3)
            d(className="android.view.View", resourceId="org.zwanoo.android.speedtest:id/backIcon").click()
            time.sleep(3)
            d(className="android.widget.FrameLayout", resourceId="org.zwanoo.android.speedtest:id/tab_internet").click()
            time.sleep(3)
            d(className="android.view.View", resourceId="org.zwanoo.android.speedtest:id/closeIcon").click()
            time.sleep(3)
            return download, downloadstring, upload, uploadstring, ping, pingstring, jitter, jitterstring
        else:
            continue



def main1():
    counter = 1
    success_counter = 0
    fail_counter = 0
    while counter <= iterate_limit:
        try:
            start_app(dev)
            start_tetsting_speed()
            download_result()


            success_counter = success_counter + 1
            try:
                print("OOKLA REPORT ::", "Iteration No: {} success".format(counter))
            except:
                pass
            counter = counter + 1
        except:
            fail_counter = fail_counter + 1
            try:
                print("OOKLA REPORT ::", "Iteration No: {} failed".format(counter))
            except:
                pass
            counter = counter + 1
    success = (success_counter / iterate_limit) * 100
    fail = (fail_counter / iterate_limit) * 100
    try:
        print("OOKLA REPORT ::", "No. of attempted Iterations are: {}".format(iterate_limit))
    except:
        pass
    try:
        print("OOKLA REPORT ::", "No. of successful Iterations are: {}".format(success_counter))
    except:
        pass
    try:
        print("Ookla Report ::", "success Rate is: {}%".format(success))
    except:
        pass
    try:
        print("OOKLA REPORT ::", "Fail Rate is: {}%".format(fail))
    except:
        pass


if __name__ == "__main__":
    main1()
