import numpy

# Load dependencies
import ovito

# Load the native code module
from ovito.plugins.StdObjPython import DataTable

# Implementation of the DataTable.interval property.
def _get_DataTable_interval(self):
    """
    A pair of float values specifying the x-axis interval covered by the data points in this table.
    This interval is only used by the table if the data points do not possess explicit x-coordinates (i.e. if the table's :py:attr:`x` property is ``None``).
    In the absence of explicit x-coordinates, the interval specifies the range of equispaced x-coordinates implicitly generated
    by the data table.
    
    Implicit x-coordinates are typically used in data tables representing histograms, which consist of equally-sized bins
    covering a certain value range along the x-axis. The bin size is then given by the interval width divided by the
    number of data points (see :py:attr:`PropertyContainer.count` property). The implicit x-coordinates of data points are placed in the centers of the bins. 
    You can call the table's :py:meth:`xy` method to let it explicitly calculate the x-coordinates from the value interval for every data point. 

    :Default: ``(0.0, 0.0)``
    """
    return (self.interval_start, self.interval_end)
def _set_DataTable_interval(self, interval):
    if len(interval) != 2: raise TypeError("Tuple or list of length 2 expected.")
    self.interval_start = interval[0]
    self.interval_end = interval[1]
DataTable.interval = property(_get_DataTable_interval, _set_DataTable_interval)

# Implementation of the DataTable.xy() method.
def _DataTable_xy(self):
    """
    This convenience method returns a two-dimensional NumPy array containing both the x- and the y-coordinates of the data points in this data table.
    If the data table does not contain explicit :py:attr:`x` coordinates, this method will
    automatically compute the x-coordinates from the :py:attr:`interval`.
    """
    x = self.x
    y = self.y
    if not x:
        half_step_size = 0.5 * (self.interval_end - self.interval_start) / len(y)
        x = numpy.linspace(half_step_size, self.interval_end - half_step_size, num = len(y))
    if x.ndim == 1: x = x[:,numpy.newaxis]
    if y.ndim == 1: y = y[:,numpy.newaxis]
    return numpy.hstack((x, y))
DataTable.xy = _DataTable_xy
