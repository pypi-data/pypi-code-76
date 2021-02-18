# Copyright 2020 Cognicept Systems
# Author: Swarooph Seshadri (swarooph@cognicept.systems)
# --> common utilities for the cognicept shell goes here.

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def generate_progress_bar(iteration, total, decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
        Parameters:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    output = "|" + bar + "| " + percent + "%"
    return output
