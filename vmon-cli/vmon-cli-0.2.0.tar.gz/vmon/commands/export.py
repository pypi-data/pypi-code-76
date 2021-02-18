"""
vmon export - export I-Mon data into CSV

09-12-2020


codenio - Aananth K
aananthraj1995@gmail.com
"""

import click
from datetime import datetime

import numpy as np
from scipy import interpolate
import pandas as pd
import matplotlib.pyplot as plt

from vmon.spectrum import read_rx_spectrum

@click.command()
@click.argument('files', nargs=-1)
@click.option('-p', '--path', default="./", help="path form which csv files are to be imported, default = . ")
@click.option('-n', '--normalise', is_flag=True, help="normalise the data before ploting")
@click.option('-i', '--inspect', is_flag=True, help="inspect the plot before exporting")
def cli(files, path, normalise, inspect):
    """Export Processed I-Mon data read from <file>.csv into <file>_vmon.csv files"""
    for file in files:

        dx, dy = read_rx_spectrum(path+file, normalise=normalise)

        if inspect:
            plt.figure("vmon")
            plt.xlabel("Wavelength (nm)")
            plt.ylabel("Amplitude (AU)")
            plt.grid("True")
            plt.plot(dx,dy,label=f"{file.split('/')[-1].split('.')[0]}")
            plt.legend()

        df = pd.DataFrame(data={'Wavelength (nm)':dx, 'Amplitude (AU)': dy})
        df.to_csv(f"{path + '/'.join(file.split('/')[:-1])+'/' + file.split('/')[-1].split('.')[0]}_vmon.csv",index=False,index_label=False)

    if inspect:
        plt.show()




