# +-------------------------------------------------------------------------------+
#
#      Program:    setup.py
#
#      Purpose:    setup for remote open control - key enabling technology (Rocket)
#
#      Target:     armv61/ARM64
#
#      Author:     Martin Shishkov
#
#      License:    GPL 3
# +-------------------------------------------------------------------------------+
import os

class Init:
    def __init__(self):
        print('Installing rocket-daisy')
        
    def get_package(self):
        linkPyPi = "https://files.pythonhosted.org/packages/0d/77/9eb70ecb2cf7511edfaef6565562ac1799b99572a29817954419fe58c41f/rocket-daisy-1.0a7.tar.gz"
        rocket = "rocket-daisy-1.0a7"
        if not os.path.isdir(rocket):
            print('downloading rocket-daisy')
            os.system("wget " + linkPyPi)
            os.system(("tar xvzf %s.tar.gz" % (rocket)))
            os.chdir(rocket)
            os.system("sudo python3 setup.py bdist")
            
            
 
 
 
i = Init()
i.get_package()    
