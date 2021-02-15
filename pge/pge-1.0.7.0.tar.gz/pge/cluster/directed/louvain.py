import os
from pathlib import Path


def split(path, local="..\\PGEstimate\\pge\\cluster\\directed\\", save="split"):
    Path(save).mkdir(parents=True, exist_ok=True)

    os.system(local + "convert -i " + path + " -o " + save + "\\test.bin")
    os.system(local+"community test.bin -l -1 -v > " + save + "\\comms.tree")
    #os.system(local+"hierarchy -l 2 " + save + "\\comms.tree > " + save + "\\comms.txt")
