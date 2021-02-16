import subprocess

def reset_original_mac():
    interface = input("Which networks' Mac Address do you want to reset?" )
    subprocess.call("macchanger -p {}".format(interface), shell=True)