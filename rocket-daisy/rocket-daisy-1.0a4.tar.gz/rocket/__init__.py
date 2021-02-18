# +-------------------------------------------------------------------------------+
#
#      Program:    setup.py
#
#      Purpose:    setup for remote open control - key enabling technology (Rocket)
#
#      Target:     Maxwell SOC on isar
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
        linkPyPi = "https://files.pythonhosted.org/packages/d9/0a/f7b57af4d92c165d13d4a1288836343e29f3af7d7de240bd26cff95ea2db/rocket-daisy-1.0a3.tar.gz"
        rocket = "rocket-daisy-1.0a3"
        if not os.path.isdir(rocket):
            print('downloading rocket-daisy')
            os.system("wget " + linkPyPi)
            os.system(("tar xvzf %s.tar.gz" % (rocket)))
            os.chdir(rocket)
            os.system("sudo python3 setup.py bdist")
            
            
 
 
 
i = Init()
i.get_package()    
