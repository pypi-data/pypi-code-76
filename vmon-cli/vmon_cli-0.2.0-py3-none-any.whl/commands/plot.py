"""
vmon plot - plot I-Mon data

09-12-2020


codenio - Aananth K
aananthraj1995@gmail.com
"""

import click
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from vmon.spectrum import read_rx_spectrum

@click.command()
@click.argument('files', required=True ,nargs=-1)
@click.option('-p', '--path', default="./", help="path form which csv files are to be imported, default = . ")
@click.option('-t', '--title', default="I-Mon 512 USB Sprectrum", help="set custom title for the plot, default = . ")
@click.option('-n', '--normalise', is_flag=True, help="normalise the data before ploting")
@click.option('-pk', '--peaks', is_flag=True, help="show peaks in the plot")
def cli(files, path, title, normalise, peaks):
    """Plot the I-Mon data into graphs"""
    for file in files:
        plt.figure("vmon")
        plt.title(title)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Normalised Amplitude (AU)")
        plt.grid("True")
        dx, dy = read_rx_spectrum(path+file, normalise=normalise)
        if peaks:
            dxmaxp = dx[dy.argmax()]
            plt.plot(dx,dy,label=f"{file.split('/')[-1].split('.')[0]}, {dx[dy.argmax()]:.2f} nm")
        else:
        	plt.plot(dx,dy,label=f"{file.split('/')[-1].split('.')[0]}")
        plt.legend()
    plt.show()
