import numpy as np
import pandas as pd
import os
import re

import utils

dlm = utils.dlm_default

def load_data(filename=None, folder=None, pattern='', expttype='', delimiter=dlm, filetype=''):
	"""
	Loads data file(s) as a pandas DataFrame

	Function to load data files as a pandas DataFrame. If called with no
	arguments, loads all supported data files in the present folder. Currently
	supports xls, xlsx, csv, and txt filetypes

	Parameters
	__________
	filename : str, path object, or file-like
			   Full filename of a file in the present directory or a path 
			   to an individual file. If filename is specified, all other
			   arguments except delimiter are ignored.
	folder : str, path object, or path-like
			 Directory containing data files. If none, defaults to the present
			 directory.
	pattern : str or regex
			  If specified, only files matching this pattern in the specified
			  folder are loaded. Ignored if filename is specified.
	expttype : str
			   Alternative to specifying pattern; ignored if pattern is
			   specified. All files containing expttype anywhere in the filename
			   will be loaded. Ex: to load all chronopotentiometery files,
			   specify expttype='cp'.
	delimiter : char (default = '\t')
				Delimiting character required for reading text files, and only
				used when reading text files. Defaults to tab delimiting.
	filetype : str
			   Any supported filetype
			   Only files of the specified filetype will be loaded. Can be used
			   in conjunction with pattern or expttype.
	Returns
	_______
	DataFrame or dict
		If a single file is read, it is returned directly as a pandas DataFrame.
		If multiple files are read, a dictionary is returned with the file names
		as keys and dataframes as values.
	"""
	data = None
	if filename:
		name, data = utils.read_file(filename, delimiter)
	else:
		if folder:
			dirpath = os.path.realpath(folder)
		else:
			dirpath = os.getcwd()
		if expttype and not pattern:
			pattern = r'.*' + expttype + r'.*'
		files = utils.get_files(dirpath, pattern, filetype)
		data = dict()
		for f in files:
			path = os.path.join(dirpath, f)
			name, df = utils.read_file(path, delimiter)
			if df is not None:
				data[name] = df
		if len(data) == 1:
			data = list(data.values())[0]
	return data

def cv_raw(filename=None, folder=None, pattern='', delimiter=dlm):
	"""
	Directly loads cyclic voltammetry data

	Efficient way to load multiple CV files at once; equivalent to calling
	load_data and specifying expttype='cv'.  If filename is specified, all other
	arguments except delimiter are ignored. If called with no arguments, loads
	all 'cv' files in the present folder.

	Parameters
	__________
	filename : str, path object, or file-like
			   Full filename of a file in the present directory or a path 
			   to an individual file. If filename is specified, all other
			   arguments except delimiter are ignored.
	folder : str, path object, or path-like
			 Directory containing data files. If none, defaults to the present
			 directory.
	pattern : str or regex
			  If specified, only files matching this pattern in the specified
			  folder are loaded. Ignored if filename is specified.
	delimiter : char (default = '\t')
				Delimiting character required for reading text files, and only
				used when reading text files. Defaults to tab delimiting.
	Returns
	_______
	DataFrame or dict
		If a single file is read, it is returned directly as a pandas DataFrame.
		If multiple files are read, a dictionary is returned with the file names
		as keys and dataframes as values.
	"""
	data = load_data(filename, folder, pattern, 'cv', delimiter)
	return data

def cp_raw(filename=None, folder=None, pattern='', delimiter=dlm):
	"""
	Directly loads chronopotentiometery data

	Efficient way to load multiple CP files at once; equivalent to calling
	load_data and specifying expttype='cp'.  If filename is specified, all other
	arguments except delimiter are ignored. If called with no arguments, loads
	all 'cp' files in the present folder.

	Parameters
	__________
	filename : str, path object, or file-like
			   Full filename of a file in the present directory or a path 
			   to an individual file. If filename is specified, all other
			   arguments except delimiter are ignored.
	folder : str, path object, or path-like
			 Directory containing data files. If none, defaults to the present
			 directory.
	pattern : str or regex
			  If specified, only files matching this pattern in the specified
			  folder are loaded. Ignored if filename is specified.
	delimiter : char (default = '\t')
				Delimiting character required for reading text files, and only
				used when reading text files. Defaults to tab delimiting.
	Returns
	_______
	DataFrame or dict
		If a single file is read, it is returned directly as a pandas DataFrame.
		If multiple files are read, a dictionary is returned with the file names
		as keys and dataframes as values.
	"""
	data = load_data(filename, folder, pattern, 'cp', delimiter)
	return data

def cv_process(data=None, area=5, current_column=1, filename=None, folder=None, pattern='', delimiter=dlm):
	"""
	Loads and/or processes cyclic voltammetry data

	Can either process pre-loaded data or load and process data files. If called
	with no arguments, loads and processes all 'cv' files in the present folder.
	Peforms the following operations in order:
		(1) Parses column labels to find column containing current data. If
			parsing fails, uses the specified column index (zero-indexing)
		(2) Converts current to current density using the specified area

	Parameters
	__________
	data : DataFrame or dict
		   Either a DataFrame containing CV data or a dict with CV DataFrames as
		   values
	area : int or float (default=5)
		   Geometric active area of the MEA. Scaling factor to convert current
		   to durrent density
	current_column : int (default=1)
					 Index (zero-indexing) of the column with current data.
					 Used only if automatic parsing fails.
	folder : str, path object, or path-like
			 Directory containing data files. If none, defaults to the current
			 directory.
	pattern : str or regex
			  If specified, only files matching this pattern in the specified
			  folder are loaded. Ignored if filename is specified.
	delimiter : char (default = '\t')
				Delimiting character required for reading text files, and only
				used when reading text files. Defaults to tab delimiting.
	Returns
	_______
	DataFrame or dict
		If a single file is read, it is returned directly as a pandas DataFrame.
		If multiple files are read, a dictionary is returned with the file names
		as keys and dataframes as values.
	"""
	if data is None:
		data = cv_raw(filename, folder, pattern, delimiter)
	if not utils.check_dict(data):
		data = {'key': data}
	newdata = dict()
	for k, df in data.items():
		newdf = df.copy()
		newdf.columns = utils.check_labels(newdf)
		if 'i' in newdf.columns:
			newdf['i'] = newdf['i'] / area
		else:
			newdf.iloc[:,current_column] = newdf.curr[:,current_column] / area
		newdata[k] = newdf
	if len(newdata) == 1:
		newdata = list(newdata.values())[0]
	return newdata

def cp_process(data=None, area=5, current_column=1, potential_column=2, threshold=5, min_step_length=50, pts_to_average=300, pyramid=True, filename=None, folder=None, pattern='', delimiter=dlm):
	"""
	Loads and/or processes chronopotentiometery data

	Can either process pre-loaded data or load and process data files. If called
	with no arguments, loads and processes all 'cp' files in the present folder.
	Peforms the following operations in order:
		(1) Parses column labels to find columns containing current and
			potential data. If parsing fails, uses the specified column index
			(zero-indexing)
		(2) Finds the points at which current steps up or down using specified
			threshold value
		(3) Splits current and potential data at these split points. Filters out
			holds with fewer than the specified number of points to account for
			outliers and random current spikes. Note: splitting is based on
			current values, so this will not filter out unusual potential spikes
			(ie no data loss)
		(4) Averages current and potenial over the last several (specified)
			points of each hold to obtain steady state values
		(5)	If current is ramped up and down, averages the steady-state values
			between the corresponding ramp-up and ramp-down holds. Note: assumes
			same current holds used for ramp-up and ramp-down
		(6) Converts current to current density using the specified area
	
	Parameters
	__________
	data : DataFrame or dict
		   Either DataFrame containing CV data or dict with CV DataFrames as
		   values
	area : int or float (default=5)
		   Geometric active area of the MEA. Scaling factor to convert current
		   to durrent density
	current_column : int (default=1)
					 Index of the column with current data. Used if automatic
					 column label parsing fails
	potential_column : int (default=2)
					   Index of the column with potential data. Used if
					   automatic column label parsing fails
	threshold : int or float (default=5)
				Threshold for splitting data based on current holds
	min_step_length : int (default=50)
					  Minimum length of each current hold. Steps with fewer than
					  min_step_length points are removed. Set min_step_length=0
					  to include all steps
	pts_to_avg : int (default=300)
				 Steady state values are calculated by averaging the last
				 pts_to_avg points of each step. Default is 300 points (last
				 30 seconds of each current hold at the instrument's default
				 collection rate of 10 Hz)
	pyramid : bool (default=True)
			  Specifies if current is ramped symmemtrically in both directions.
			  set pyramid=False if only ramping up or down
	folder : str, path object, or path-like
			 Directory containing data files. If none, defaults to the current
			 directory.
	pattern : str or regex
			  If specified, only files matching this pattern in the specified
			  folder are loaded. Ignored if filename is specified.
	delimiter : char (default = '\t')
				Delimiting character required for reading text files, and only
				used when reading text files. Defaults to tab delimiting.
	Returns
	_______
	DataFrame or dict
		If a single file is read, it is returned directly as a pandas DataFrame.
		If multiple files are read, a dictionary is returned with the file names
		as keys and dataframes as values.
	"""
	if data is None:
		data = cp_raw(filename, folder, pattern, delimiter)
	if not utils.check_dict(data):
		data = {'key': data}
	newdata = dict()
	for k, df in data.items():
		newdf = df.copy()
		newdf.columns = utils.check_labels(newdf)
		# time = np.array(newdf['t'])
		if 'i' in newdf.columns and 'v' in newdf.columns:
			current = np.array(newdf['i'])
			potential = np.array(newdf['v'])
		else:
			current = np.array(newdf.iloc[:, current_column])
			potential = np.array(newdf[:, current_column])
		split_pts = findsteps(current, threshold=threshold)
		current_steps = split_and_filter(current, split_pts, min_length=min_step_length)
		potential_steps = split_and_filter(potential, split_pts, min_length=min_step_length)
		# time_steps = split_and_filter(potential, split_pts, min_length=100)
		current_avg = np.array([avg_last_pts(s, numpts=pts_to_average) for s in current_steps])
		potential_avg = np.array([avg_last_pts(s, numpts=pts_to_average) for s in potential_steps])
		if pyramid:
			current_avg = avg_outside_in(current_avg)
			potential_avg = avg_outside_in(potential_avg)
		current_avg = current_avg / 5
		cp_processed = pd.DataFrame({'i':current_avg, 'v':potential_avg})
		newdata[k] = cp_processed
	if len(newdata) == 1:
		newdata = list(newdata.values())[0]
	return newdata

def findsteps(arr, threshold=5):
	"""
	Auxilliary function to find the points at which current/voltage is stepped
	up or down

	Finds 'jumps' in an array. Determines the indices at which the absolute
	difference between consecutive array values is greater than the specified
	threshold

	Parameters
	__________
	arr : list or numpy array
		  Array used to determine the 'step' points
	threshold : int or float (default=5)
				Minimum consectutive difference which constitutes a 'step'.
	Returns
	_______
	numpy array
		Indices at which the array 'steps' up or down
	"""
	if type(arr) == list:
		arr = np.array(arr)
	diffs = np.abs(np.diff(arr))
	splits = np.where(diffs > threshold)[0] + 1
	return splits

def split_and_filter(arr, split_pts, min_length=0):
	"""
	Auxilliary function to split continuous current or voltage data into
	individual holds

	Splits an array at the specified indices and discards resulting arrays which
	do not meet the required length.

	Parameters
	__________
	arr : list or numpy array
		  Array to split.
	split_pts : int or array-like
				Indices at which to split arr.
	min_length : int
				 Minimum length of arrays which result after splitting arr. 
				 Arrays shorter than min_length will be discarded.
	Returns
	_______
	numpy array
		Array containing one array for each 'hold'
	"""
	if type(arr) == list:
		arr = np.array(arr)
	steps = np.split(arr, split_pts)
	steps_tokeep = np.array([s for s in steps if len(s) > min_length])
	return steps_tokeep

def avg_last_pts(arr, numpts=300):
	"""
	Auxilliary function to average the last several values of an array

	Computes the average of an array across the last specified number of points.

	Parameters
	__________
	arr : list or numpy array
		  Array of values used to compute the average
	numpts : int
			 Average calculated over the last numpts values of the array
	Returns
	_______
	float
		Average of the last several array values
	"""
	if type(arr) == list:
		arr = np.array(arr)
	avg = np.mean(arr[-numpts:])
	return avg

def avg_outside_in(arr):
	l = len(arr)
	avg = np.array([(arr[i]+arr[l-1-i])/2 for i in np.arange(l//2 + l%2)])
	return avg