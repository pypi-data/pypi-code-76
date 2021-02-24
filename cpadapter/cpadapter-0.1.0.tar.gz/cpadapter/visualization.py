import numpy as np
import matplotlib.pyplot as plt
import seaborn
from typing import List

def band_interval_plot(y: np.ndarray, lower: np.ndarray, upper: np.ndarray, conf_percentage: float, sort: bool) -> None:
	r"""Function used to plot the data in `y` and it's confidence interval 

	This function plots `y`, with a line plot, and the interval defined by the
	`lower` and `upper` bounds, with a band plot.

	Parameters
	----------
	y: numpy.ndarray
		Array of observation or predictions we want to plot
	lower: numpy.ndarray
		Array of lower bound predictions for the confidence interval
	upper: numpy.ndarray
		Array of upper bound predictions for the confidence interval
	conf_percetage: float
		The desired confidence level of the predicted confidente interval
	sort: bool
		Boolean variable that indicates if the data, and the respective lower
		and upper bound values should be sorted ascendingly.

	Returns
	-------
	None

	Notes
	-----
	This function must only be used for regression cases
	"""
	if sort:
		idx = np.argsort(y)
		y = y[idx]
		lower = lower[idx]
		upper = upper[idx]
	fig, ax = plt.subplots(figsize=(14, 8))
	ax.plot(y.reshape(-1), label='data')
	conf = str(conf_percentage*100) + '%'
	ax.fill_between([*range(y.shape[0])], lower, upper, label=conf, alpha=0.3)
	ax.legend()

def conditional_band_interval_plot(y, lower, upper, sort):
	r"""Function for plotting the data in `y` and it's confidence interval

	This function plots `y` and it's confidence interval. The confidence
	interval is green when the `y` observation falls inside the predicted
	interval, on the other hand, it's red when it doesn't. The interval is
	defined by the `lower` and `upper` bound.

	Parameters
	----------
	y: numpy.ndarray
		Array of observation or predictions we want to plot
	lower: numpy.ndarray
		Array of lower bound predictions for the confidence interval
	upper: numpy.ndarray
		Array of upper bound predictions for the confidence interval
	conf_percetage: float
		The desired confidence level of the predicted confidente interval
	sort: bool
		Boolean variable that indicates if the data, and the respective lower
		and upper bound values should be sorted ascendingly.

	Returns
	-------
	None

	Notes
	-----
	This function must only be used for regression cases
	"""
	if sort:
		idx = np.argsort(y)
		y = y[idx]
		lower = lower[idx]
		upper = upper[idx]
	fig, ax = plt.subplots(figsize=(14, 8))
	ax.plot(y.reshape(-1), 'o', label='data')
	ax.fill_between([*range(y.shape[0])], lower, upper, label='target inside the interval', 
					alpha=0.3, color='g', where=[l <= y_i and y_i <= u for (l, y_i, u) in zip(lower, y, upper)])
	ax.fill_between([*range(y.shape[0])], lower, upper, label='target outside the interval',
					alpha=0.3, color='r', where=[l >= y_i or y_i >= u for (l, y_i, u) in zip(lower, y, upper)])
	ax.legend()

def line_interval_plot(y, lower, upper, sort):
	r"""Function for plotting `y` and it's confidence interval

	The `y` data is represented by a big blue point. On the other had, 
	the `lower` bound of the interval is represented by a smaller red point
	and the `upper` bound by a smmaler blue point, both bounds are connected
	by a vertical line.

	Parameters
	----------
	y: numpy.ndarray
		Array of observation or predictions we want to plot
	lower: numpy.ndarray
		Array of lower bound predictions for the confidence interval
	upper: numpy.ndarray
		Array of upper bound predictions for the confidence interval
	conf_percetage: float
		The desired confidence level of the predicted confidente interval
	sort: bool
		Boolean variable that indicates if the data, and the respective lower
		and upper bound values should be sorted ascendingly.

	Returns
	-------
	None

	Notes
	-----
	This function must only be used for regression cases
	"""
	if sort:
		idx = np.argsort(y)
		y = y[idx]
		lower = lower[idx]
		upper = upper[idx]
	fig, ax = plt.subplots(figsize=(14, 8))
	ax.plot(y.reshape(-1), 'o',label='data')
	x = np.arange(y.shape[0])
	ax.vlines(x, ymin=lower, ymax=upper)
	ax.plot(lower, 'ro', markersize = 4, label='lower limit')
	ax.plot(upper, 'bo', markersize = 4, label='upper limit')
	ax.legend()

def classes_in_interval(preds):
	classes = []
	for i in range(preds.shape[0]):
		classes.append(np.where(preds[i, :]))
	return classes

def plot_class_interval(y: np.ndarray, preds: np.ndarray) -> None:
	r"""Function thas shows the classes in `y` and the classes in it's confidence interval.

	The class for every observation in `y` is represented by a white dot,
	while the classes in the interval `preds` can be seen as a red *.
	When the "y" class and one of the classes in the interval overlap, the
	white dot turns red.

	Parameters
	----------
	y: numpy.ndarray
		Array of predicted or real classes of length num_samples
	preds: numpy.ndarray
		The confidence interval, represented by a numpy array of boolean
		values with size (num_samples, num_classes), where num_classes is the total
		number of classes for the data.

	Returns
	-------
	None

	Notes
	-----
	This function must be used in classification cases
	"""
	x = np.arange(len(y))
	pred_classes = classes_in_interval(preds)
	fig, ax = plt.subplots(figsize=(14, 8))
	ax.scatter(x, y, edgecolors='black', color='w')
	for xe, ye in zip(x, pred_classes):
		ye = np.asarray(ye).reshape(-1, 1)
		ax.scatter([xe] * len(ye), ye, alpha=0.5, color='r', marker='*')
	ax.legend(['class', 'classes in predicted interval'])


def class_histogram(y: np.ndarray, preds: np.ndarray) -> None:
	r"""Function used to plot the histogram of classes in `y` and the classes in it's confidence interval

	There are two histograms in the plot shown by this fuction, the red one corresponds to the
	class histogram of the input `y`. The blue one is the total class histogram of the predicted
	confidence interval `preds`.

	Parameters
	----------
	y: numpy.ndarray
		Array containing the predicted or real classes in num_samples
	preds: numpy.ndarray
		The confidence interval, represented by a numpy array of boolean
		values with size (num_samples, num_classes), where num_classes is the total
		number of classes for the data.

	Returns
	-------
	None

	Notes
	-----
	This function must be used in classification cases
	"""
	pred_classes = np.array(classes_in_interval(preds))
	interval =  np.concatenate(np.concatenate(pred_classes, axis=0), axis=0)
	fig, ax = plt.subplots(figsize=(14, 8))
	ax.hist(interval, alpha=0.3)
	ax.hist(y, alpha=0.4)
	ax.legend(['classes in intervals', 'classes'])

def confusion_matrix(y: np.ndarray, pred: np.ndarray, classes: List[str]) -> None:
	r"""Function for displaying the cofusion matrix

	This function shows a confusion matrix for the real classes in `y`
	and the classes in the predicted interval `preds`. In this case the numbers
	inside the matrix represent the fraction of times a certain class (x axis) is present
	in the confidence interval, when the real class was the one on the y axis.

	Parameters
	----------
	y: numpy.ndarray
		Array of predicted or real classes
	preds: numpy.ndarray
		The confidence interval, represented by a numpy array of boolean
		values with size (num_samples, num_classes), where num_classes is the total
		number of classes for the data.
	classes: List[str]
		List of the classes' names.

	Returns
	-------
	None

	Notes
	-----
	This function must be used in classification cases
	"""
	data = []
	for i in range(len(classes)):
		idx = np.where(y == i)[0]
		class_count = pred[idx].sum(axis=0)
		class_count_norm = class_count/len(idx)
		data.append(class_count_norm.tolist())
	seaborn.set(color_codes=True)
	plt.figure(1, figsize=(18,  18))
	plt.title("Confusion Matrix")
	seaborn.set(font_scale=1)
	ax = seaborn.heatmap(data, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Scale'})
	ax.set_xticklabels(classes)
	ax.set_yticklabels(classes)
	ax.set(ylabel="True Label", xlabel="Predicted Label in Interval")
	plt.show()
	plt.close()
