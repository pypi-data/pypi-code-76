from .. import Globals
import numpy as np
from ..Tools.Downloading._DownloadData import _DownloadData
from ..Tools.ListDates import ListDates

def DownloadData(prod,Date=[20170101,20200101],Overwrite=False,Verbose=False):
	'''
	Downloads Arase position data.

	prod : 'l3' or 'def'
	
	'''
	url0 = 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/satellite/erg/orb/{:s}/'.format(prod)
	vfmt = ['v']	
	idxfname = Globals.DataPath + 'Pos/Index-{:s}.dat'.format(prod)
	datapath = Globals.DataPath + 'Pos/{:s}/'.format(prod)

	#populate the list of dates to download
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	#a hack because of directory structures
	if prod == 'l3':
		u16 = np.where(dates < 20170101)[0]
		dates16 = dates[u16]
		u17 = np.where(dates >= 20170101)[0]
		dates = dates[u17]
	else:
		dates16 = np.array([])
		
	if dates16.size > 0 :
		url16 = url0 + '{:04d}/tmp/'
		_DownloadData(url16,idxfname,datapath,dates16,vfmt,Overwrite,Verbose)
		StartYear = 2017
	
	url0 += '{:04d}/'
	_DownloadData(url0,idxfname,datapath,dates,vfmt,Overwrite,Verbose)
	
