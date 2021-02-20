import sys
import os
from glob import glob
from os.path import dirname

rootDir = dirname(__file__)

sys.path.append(rootDir)
os.environ["PATH"] = os.environ["PATH"] + os.pathsep + os.path.join(rootDir, "dlls")

#dataFileList = glob(os.path.join(rootDir, "datas", "*.*"))
os.environ["DNN_DATA_FOLDER"] = os.path.join(rootDir, "models")
os.environ["IMG_DATA_FOLDER"] = os.path.join(rootDir, "imgs")
#os.environ["PATH"] = os.environ["PATH"] + os.pathsep + os.path.join(rootDir, "datas")