# +---------------------------------------------------------------------------+
#
#      Program:    setup.py
#
#      Purpose:    setup for remote open control key enabling technology (Rocket)
#
#      Target:     arm64
#
#      Author:     Martin Shishkov
#
#      License:    GPL 3
# +---------------------------------------------------------------------------+

import atexit
import os
import sys
from setuptools import setup
from setuptools.command.install import install
import re
import shutil
import io

daisy = "daisy"

with io.open("README.md", "r") as fh:
    long_description = fh.read()

def logo():
    print()
    print("                                          ")
    print("######                                    ")
    print("#     #  ####   ####  #    # ###### ##### ")
    print("#     # #    # #    # #   #  #        #   ")
    print("######  #    # #      ####   #####    #   ")
    print("#   #   #    # #      #  #   #        #   ")
    print("#    #  #    # #    # #   #  #        #   ")
    print("#     #  ####   ####  #    # ######   #   ")
    print("                                          ")


class CustomInstall(install):
    def run(self):
        def _post_install():

            setupDir = os.getcwd()
            logo()
            os.system("apt-get install firmware-b43-installer")
            os.system("apt install rfkill")
            os.system("apt install git")
            get_hostapd()
            get_config_dnsmasq("dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h")
            os.system("systemctl stop dnsmasq")
            os.system("systemctl stop hostapd")
            configure_hostapd()
            os.system("systemctl stop wpa_supplicant")
            os.system("systemctl disable wpa_supplicant")
            os.system("systemctl mask wpa_supplicant")
            adjust_rocketlauncher(setupDir)
            get_maxmotion_lib(setupDir)
            print("Start the demo with:\n python3 -m rocket -d -c /etc/daisy/config")

        atexit.register(_post_install)
        install.run(self)


setup(name='rocket-daisy',
      version='1.0a5',
      description='Remote open control key enabling technology (Rocket)',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/gulliversoft/motion',
      author='gulliversoft',
      author_email='df6@gulliversoft.com',
      license='GPL3',
      packages=['rocket','rocketlauncher',"rocket.maxmotion","rocket.daisy",
      "rocket.daisy.utils",
      "rocket.daisy.clients",
      "rocket.daisy.protocols",
      "rocket.daisy.server",
      "rocket.daisy.decorators",
      "rocket.daisy.devices",
      "rocket.daisy.devices.digital",
      "rocket.daisy.devices.analog",
      "rocket.daisy.devices.sensor",
      "rocket.daisy.devices.shield"],
      zip_safe=False,
      classifiers=["Intended Audience :: Education",
               'Development Status :: 3 - Alpha',
               'Programming Language :: Python :: 3',
               "Operating System :: POSIX :: Linux",
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware'],
      cmdclass={'install': CustomInstall})
      #install_requires[''])


def get_config_dnsmasq(dhcprange):
    """
    Try to install dnsmasq (dhcp server) on host machine if not present
    in second step adjusts the address range

    :return: None
    :rtype: None
    """
    filename = "/usr/sbin/dnsmasq"

    if not os.path.isfile(filename):
        print("dhcp server (dnsmasq) not found, installing now...")
        os.system("apt-get install dnsmasq")

    if not os.path.isfile(filename):
        sys.exit(("\nUnable to install the \'dnsmasq\' package!\n" +
                  "This process requires a persistent internet connection!\n" +
                  "Run apt-get update for changes to take effect.\n" +
                  "Rerun the script to install dnsmasq.\n" +
                  "Closing"))

    filename = "/usr/sbin/dnsmasq.conf"
    if(search(filename, "interface=wlp1s0b1") > 0):
        return
    else:
        body = "interface=wlp1s0b1\n%s\n" % (dhcprange)
        text_file = open(filename, "w")
        text_file.write(body)
        text_file.close()


def get_hostapd():
    """
    Try to install hostapd on host system if not present

    :return: None
    :rtype: None
    """
    filename = "/usr/sbin/hostapd"

    if not os.path.isfile(filename):
        print(filename + " not found, installing now...")
        os.system("apt-get install hostapd")

    if not os.path.isfile(filename):
        sys.exit(("\nUnable to install the \'hostapd\' package!\n" + 
        "This process requires a persistent internet connection!\n" +
        "Run apt-get update for changes to take effect.\n" +
        "Rerun the script to install hostapd.\n" +
        "Closing"))


def search(str, filename):
    if not os.path.isfile(filename):
        return -1
    n = 0
    with open(filename, 'r') as f:
        for line in f:
            if re.search(str, line):
                return n
            n += 1
    return -1


def configure_hostapd():
  filename = "/etc/hostapd/hostapd.conf"
  ssid = input('Access point SSID: ')
  psk = input('Password: ')
  body = ("interface=wlp1s0b1\n" +
        "ssid=%s\n" +
        "hw_mode=g\n" +
        "channel=7\n" +
        "wmm_enabled=0\n" +
        "macaddr_acl=0\n" +
        "auth_algs=1\n" +
        "ignore_broadcast_ssid=0\n" +
        "wpa=2\n" +
        "wpa_passphrase=%s\n" +
        "wpa_key_mgmt=WPA-PSK\n" +
        "wpa_pairwise=TKIP\n" +
        "rsn_pairwise=CCMP\n" +
        "ctrl_interface=/var/run/hostapd\n" +
        "ctrl_interface_group=0\n") % (ssid, psk)
  text_file = open(filename, "w")
  text_file.write(body)
  text_file.close()

def adjust_http_docroot(setupDir, scriptname):
    """
    set up the default doc-root into Rocket doc-root

    :return: None
    :rtype: The folder of installation
    """

    filename = "/etc/daisy/config"

    if os.path.isfile(filename):
       change = input("There is previous Daisy WebServer configuration, do you need to change? y/n:")
       if change == 'y':
          print("You decided to change or create the web configuration")
       elif change == 'n':
          print("You decided to keep the web configuration unchanged")
          return
       else:
          print("Wrong input, the web configuration keeps unchanged") 
          return

    docroot = ("%s/rocket/html") % (setupDir)
    myscript = ("%s/rocket/python/%s") % (setupDir, scriptname)
    body = ("[GPIO]\n" +
        "[~GPIO]\n" +
        "[SCRIPTS]\n" +
        "myscript = %s\n" +
        "[HTTP]\n" +
        "enabled = true\n" +
        "port = 8000\n" +
        "doc-root = %s\n" +
        "passwd-file = /etc/daisy/passwd\n" +
        "prompt = \"Daisy\"\n" +
        "welcome-file = Index.html\n" +
        "[COAP]\n" +
        "enabled = true\n" +
        "port = 5683\n" +
        "multicast = true\n" +
        "[DEVICES]\n" +
        "[REST]\n" +
        "[ROUTES]\n") % (myscript, docroot)
    text_file = open(filename, "w")
    text_file.write(body)
    text_file.close()

    print("Rocket frontend activated. Use http://192.168.4.1:8000")

def adjust_rocketlauncher(setupDir):
    """
    activates the RIB (if the binary is available) to be started at boot time

    :return: positive or 0 by success
    :rtype: The folder of installation
    """

    os.chdir(setupDir)
    os.chdir("rocketlauncher")
    filename = "/etc/systemd/system/rocket.service"

    src_file = open("rocket.service", "r")
    body = src_file.read()
    src_file.close()


    if not os.path.isfile("RIB_App"):
       input("Missing the RIB_App executable. You need to provide the binary in the " + setupDir + "/rocketlauncher" + " Press Enter to go further with the setup")
       
    product = int(input("The current release shapes one setup for 2 digital products behind\n1. Digger RC Car\n2. Pan-tilt RC camera.\nTake the choice between 1 and 2:\n"))
    if product == 1: 
        print("Installing Digger RC Car")
        body = body % ("rocketlauncher.sh", setupDir + "/rocketlauncher")
        os.remove("Digger_Consumer_App")
        shutil.copyfile("./RC_car_application/Digger_Consumer_App", "Digger_Consumer_App")
        os.remove("RIB_App")
        shutil.copyfile("./RC_car_application/RIB_App", "RIB_App")
        os.remove(setupDir + "/rocket/modules/_DataExchangeBuffer.so")
        shutil.copyfile("./RC_car_application/_DataExchangeBuffer", setupDir + "/rocket/modules/_DataExchangeBuffer.so")
        install_daisy(setupDir)
        adjust_http_docroot(setupDir, "RC_car.py")
    elif product == 2:
        print("Installing Pan-tilt RC Camera")
        body = body % ("wlanUP.sh", setupDir + "/rocketlauncher")
        os.remove("Digger_Consumer_App")
        shutil.copyfile("./Pan_tilt_RC_camera_application/Digger_Consumer_App", "Digger_Consumer_App")
        os.remove("RIB_App")
        shutil.copyfile("./Pan_tilt_RC_camera_application/RIB_App", "RIB_App")
        os.remove(setupDir + "/rocket/modules/_DataExchangeBuffer.so")
        shutil.copyfile("./RC_car_application/_DataExchangeBuffer", setupDir + "/rocket/modules/_DataExchangeBuffer.so")
        install_daisy(setupDir)
        adjust_http_docroot(setupDir, "maxmotion.py")
    else:
        print("Wrong Choice, terminating the program.")
        return 1
    
    text_file = open(filename, "w")
    text_file.write(body)
    text_file.close()
    os.system("systemctl enable rocket.service")
    
    print("Installation done. Enjoy Daisy. launches at start ...")
    return 0

def get_maxmotion_lib(setupDir):
    """
    installs all motion required shared libraries and creates link to the prebuild demo binary
    ensures the demonstration motion getting started apart of the rocket service
    takes the git repo for the maxmotion project (does not build the project)

    :return: positive or 0 by success
    :rtype: The folder of installation
    """

    os.chdir(setupDir)
    os.chdir("rocket/maxmotion/demo")
    os.system("chmod 0777 motion")
    os.system("chmod 0777 libMotionExchangeBuffer.so")
    #creates symbolic link in the launcher folder to the motion executable in the demo folder
    launcherfolder = setupDir + "/rocketlauncher"
    motion_demo_folder = setupDir + "/rocket/maxmotion/demo/"
    os.system("ln -s %s %s" % (motion_demo_folder + "motion", launcherfolder))
    os.system("ln -s %s %s" % (motion_demo_folder + "libMotionExchangeBuffer.so", launcherfolder))
    #creates symbolic link in the launcher folder to the motion configuration in the demo folder
    os.system("ln -s %s %s" % (motion_demo_folder + "motion.conf", launcherfolder))
    #installs related debian packages
    os.system("dpkg -i libmicrohttpd12_0.9.51-1_arm64.deb")
    os.system("dpkg -i libavformat58_4.1.6-1_deb10u1_arm64.deb")
    os.system("apt --fix-broken install")
    os.system("dpkg -i libswscale5_4.1.6-1_deb10u1_arm64.deb")
    os.system("dpkg -i libavdevice58_4.1.6-1_deb10u1_arm64.deb")
    os.system("apt --fix-broken install") 

    repo = "motion"
    os.chdir(setupDir)
    os.chdir("rocket/maxmotion")
    if os.path.isdir(repo):
       print("Nothing to clone. %s already here." % (repo))
    else:
       os.system("git clone https://github.com/gulliversoft/%s" % (repo))

    print("Installation done. Enjoy the demonstration project %s." % (repo))
    return 0

def install_daisy(setupDir):
    """
    instal python modules around of daisy
    :return: positive or 0 by success
    :rtype: The folder of installation
    """

    os.chdir(setupDir)
    os.chdir("rocket/daisy")
    os.system("bash ./daisy_setup.sh")

    os.chdir(setupDir)
    os.chdir("rocketlauncher")
    #creates symbolic link of the broadcom fw blacklst into modprobe.d
    os.system("ln -s %s /etc/modprobe.d" % (setupDir + "/rocketlauncher/blacklist.conf"))
    os.system("chmod 0777 Digger_Consumer_App")
    os.system("chmod 0777 RIB_App")
    os.system("chmod 0777 Digger_Motion_Consumer_App")
    print("Installation done. Enjoy Daisy ...")
    return 0


