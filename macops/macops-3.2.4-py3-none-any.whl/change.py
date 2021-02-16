import subprocess
from macops.generate import generate_mac
def change_mac():
    generated_mac = generate_mac()
    interface = input("Which networks' Mac Address do you want to change?" )
    subprocess.call("ifconfig {} down".format(interface), shell=True)
    subprocess.call("ifconfig {} hw ether {}".format(interface, generated_mac), shell=True)
    subprocess.call("ifconfig {} up".format(interface), shell=True)