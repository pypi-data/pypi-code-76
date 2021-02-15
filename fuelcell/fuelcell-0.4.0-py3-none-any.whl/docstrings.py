load_data
	"""
	Loads data file(s) as a pandas DataFrame

	Function to load data files as a pandas DataFrame. If called with no
	arguments, loads all supported data files in the present folder. Currently
	supports xls, xlsx, csv, and txt filetypes

	Parameters
	___________
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
	________
	DataFrame or dict
		If a single file is read, it is returned directly as a pandas DataFrame.
		If multiple files are read, a dictionary is returned with the file names
		as keys and dataframes as values.
	"""

cv_raw
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
cp_raw
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

cv_process
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

cp_process
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

find_steps
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

split_filter
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

avg_last_pts
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

plot_cv
	"""
	Plots cyclic voltammetry files

	Function to plot data from one or more CV tests

	Parameters
	__________
	data : DataFrame or dict
		   Either a DataFrame containing CV data or a dict with CV DataFrames as
		   values
	labels : list
			 Currently unsupported. List of labels to be used in place of dict
			 keys
	line : bool
		   Unused; only present to maintain continuity of function signatures
	scatter : bool
			  Unused; only present to maintain continuity of function signatures
	current_column : int (default=1)
					 Index of the column with current data. Used if automatic
					 column label parsing fails
	potential_column : int (default=0)
					   Index of the column with potential data. Used if
					   automatic column label parsing fails
	xunits : str (default='V')
			 units to use in the x-axis label
	yunits : str (default=r'$mA/cm^2$')
			 units to use in the y-axis label
	export_name : str or path-like
				  Filename used to save the figure. If export_name is specified,
				  figure will be saved in the current directory (or specified
				  directory if pathlike)
	export_type : str (default='png')
				  Image type to save figure as. Only used if export_name is
				  specified and export_name does not include a filetype
	figsize : list or tuple (default=(5,5))
			  Figure dimensions (inches) if figure is to be exported. Only used
			  if export_name is specified
	dpi : int (default=600)
		  Resolution (dots per inch) of exported figure. Only used if
		  export_name is specified

	Returns
	_______
	Figure
		Object containing all plot elements
	Axes
		Object cotaining the plotted data
	"""

polcurve
	"""
	Plots polarization curves

	Function to plot polarization curves

	Parameters
	__________
	data : DataFrame or dict
		   Either a DataFrame a dict with CV DataFrames as values
	labels : list
			 Currently unsupported. List of labels to be used in place of dict
			 keys
	line : bool (default=True)
		   Specifies if a line connecting the points will be drawn
	scatter : bool (default=True)
			  Specifies if a marker will be drawn at each data point
	current_column : int (default=1)
					 Index of the column with current data. Used if automatic
					 column label parsing fails
	potential_column : int (default=0)
					   Index of the column with potential data. Used if
					   automatic column label parsing fails
	xunits : str (default='V')
			 units to use in the x-axis label
	yunits : str (default=r'$mA/cm^2$')
			 units to use in the y-axis label
	export_name : str or path-like
				  Filename used to save the figure. If export_name is specified,
				  figure will be saved in the current directory (or specified
				  directory if pathlike)
	export_type : str (default='png')
				  Image type to save figure as. Only used if export_name is
				  specified and export_name does not include a filetype
	figsize : list or tuple (default=(5,5))
			  Figure dimensions (inches) if figure is to be exported. Only used
			  if export_name is specified
	dpi : int (default=600)
		  Resolution (dots per inch) of exported figure. Only used if
		  export_name is specified

	Returns
	_______
	Figure
		Object containing all plot elements
	Axes
		Object cotaining the plotted data
	"""

plot_cp_raw
	"""
	Plots raw chronopotentiometery data

	Function to plot cp data as it would appear in EC lab.

	Parameters
	__________
	data : DataFrame or dict
		   Either a DataFrame a dict with CV DataFrames as values. Using a dict
		   is supported to preserve continuity accross all visualization 
		   functions, but it is strongly reccomended to pass in a single
		   DataFrame for visual clarity
	labels : list
			 Currently unsupported. List of labels to be used in place of dict
			 keys
	line : bool (default=True)
		    Unused; only present to maintain continuity of function signatures
	scatter : bool (default=True)
			   Unused; only present to maintain continuity of function
			   signatures
	current_column : int (default=2)
					 Index of the column with current data. Used if automatic
					 column label parsing fails
	potential_column : int (default=1)
					   Index of the column with potential data. Used if
					   automatic column label parsing fails
	time_column : int (default=0)
				  Index of the column with time data. Used if automatic column
				  label parsing fails
	xunits : str (default='V')
			 units to use in the x-axis label
	yunits : tuple or list (default=('mA', 'V'))
			 units to use in the y-axis labels.
			 Passed in the order('current units', 'potential units')
	export_name : str or path-like
				  Filename used to save the figure. If export_name is specified,
				  figure will be saved in the current directory (or specified
				  directory if pathlike)
	export_type : str (default='png')
				  Image type to save figure as. Only used if export_name is
				  specified and export_name does not include a filetype
	figsize : list or tuple (default=(5,5))
			  Figure dimensions (inches) if figure is to be exported. Only used
			  if export_name is specified
	dpi : int (default=600)
		  Resolution (dots per inch) of exported figure. Only used if
		  export_name is specified

	Returns
	_______
	Figure
		Object containing all plot elements
	tuple
		tuple of two Axes objects: one each for the potential vs. time and 
		current vs. time plots
	"""

plot_general
	"""
	General plotting function

	Function to plot any data you like

	Parameters
	__________
	data : DataFrame or dict
		   Either a DataFrame a dict with CV DataFrames as values
	labels : list
			 Currently unsupported. List of labels to be used in place of dict
			 keys
	line : bool (default=True)
		   Specifies if a line connecting the points will be drawn
	scatter : bool (default=True)
			  Specifies if a marker will be drawn at each data point
	xcolumn : int (default=1)
			  Index of the column containing x values
	ycolumn : int (default=1)
			  Index of the column containing y values
	xlabel : str (default='x')
			 x-axis label
	ylabel : str (default='y')
			 y-axis label
	export_name : str or path-like
				  Filename used to save the figure. If export_name is specified,
				  figure will be saved in the current directory (or specified
				  directory if pathlike)
	export_type : str (default='png')
				  Image type to save figure as. Only used if export_name is
				  specified and export_name does not include a filetype
	figsize : list or tuple (default=(5,5))
			  Figure dimensions (inches) if figure is to be exported. Only used
			  if export_name is specified
	dpi : int (default=600)
		  Resolution (dots per inch) of exported figure. Only used if
		  export_name is specified

	Returns
	_______
	Figure
		Object containing all plot elements
	Axes
		Object cotaining the plotted data
	"""