import bottleneck as bn
import matplotlib.pyplot as plt
import numpy as np

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ------------------------------------------------------
# Get the min and max value to define the contrast scale
def _get_min_max(array, min=None, max=None, percentile=10, percentile_min=None):

    # Calculate the min value
    if min is None:

        # Calculate the percentile
        if percentile_min is None:
            percentile_min = percentile

        min = np.percentile(array, percentile_min)

    # Calculate the max value
    if max is None:

        percentile = 100 - percentile

        max = np.percentile(array, percentile)

    return min, max

# ------------------------------------------------
# Define the new scale for the contrast correction
def _get_scale(array, min=None, max=None, rescale=True):

    # Get the new min value
    if min is None:
        if rescale:
            min = 0

        else:
            min = np.amin(array)

    # Get the new max value
    if max is None:
        if rescale and issubclass(array.dtype.type, np.integer):
            max = np.iinfo(array.dtype).max

        else:
            max = np.amax(array)

    return min, max

# ------------------------------
# Rescale the value in the array
def _rescale_array(array, old_limits, new_limits):

    # Save the data type
    data_type = array.dtype
    array = array.astype(np.float64)

    # Get the limits
    old_min, old_max = old_limits
    new_min, new_max = new_limits

    # Rescale to 0 - 1
    unit_array = (array - old_min) / (old_max - old_min)
    unit_array[unit_array < 0] == 0
    unit_array[unit_array > 1] == 1

    # Rescale to the new limits
    new_array = unit_array * (new_max - new_min) + new_min

    return new_array.astype(data_type)

# ------------------------------
# Correct for signed bits images
def _correct_signed_bits(array):
    return array - (((np.iinfo(array.dtype).max+1)/2)-1)

# -----------------------------
# Calculate the reference image
def _get_reference_image(array, type='mean'):

    # Compute the mean image
    if type.lower() == 'mean':
        reference_array = bn.nanmean(array, axis=0)

    # Compute the median image
    elif type.lower() == 'median':
        reference_array = bn.nanmedian(array, axis=0)

    # Raise an error
    else:
        raise Exception("Type of average ("+str(type)+") not recognized. Please pick between the given choices (mean/median).")

    return reference_array

# ---------------------------------
# Compute the background correction
def _apply_correction(array, reference, type='division'):

    # Compute the subtraction
    if type.lower() == 'subtraction':
        corrected_array = array - reference

    # Compute the median image
    elif type.lower() == 'division':
        corrected_array = array / reference

    # Raise an error
    else:
        raise Exception("Type of correction ("+str(type)+") not recognized. Please pick between the given choices (subtraction/division).")

    return corrected_array

# ---------------------------------------------------
# Display the PV distribution and the user set limits
def _display_distribution(array, min, max, n_bins=1000, log_scale=None):

    # Display the histogram
    plt.hist(np.ravel(array), bins=n_bins)

    # Add the limit bar
    plt.axvline(x=min, color='blue', alpha=.5)
    plt.axvline(x=max, color='blue', alpha=.5)

    # Edit the display of the graph
    plt.ylabel('#')
    plt.xlabel('Pixel value (AU)')

    # Logarithm scale
    if log_scale is not None:
        if 'y' in log_scale.lower():
            plt.yscale('log')
        if 'x' in log_scale.lower():
            plt.xscale('log')

    plt.show()

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------------------------
# Prepare the contrast correction of the image
def setContrastCorrection(array, min=None, max=None, percentile=10, percentile_min=None, rescale=True):

    # Get the limits for the old values
    min, max = _get_min_max(array, min=min, max=max, percentile=percentile, percentile_min=percentile_min)

    # Get the limits in new values
    new_min, new_max = _get_scale(array, rescale=rescale)

    return (min, max), (new_min, new_max)

# -----------------
# Rescale the array
def doContrastCorrection(array, old_limits, new_limits):
    return _rescale_array(array, old_limits, new_limits)

# ---------------------------------------
# Remove the background of an image stack
def backgroundCorrection(array, signed_bits=False, average='mean', correction='division', rescale=True):

    # Save the type of the array
    data_type = array.dtype

    # Correct for signed bits
    if signed_bits:
        array = _correct_signed_bits(array)

    # Calculate the background reference
    reference_array = _get_reference_image(array, type=average)

    # Correct the background
    corrected_array = _apply_correction(array, reference_array, type=correction)

    # Rescale the array
    if rescale:
        corrected_array = corrected_array * np.iinfo(data_type).max / np.amax(corrected_array)
        corrected_array = corrected_array.astype(data_type)

    return corrected_array

# ---------------------------------
# Show the pixel value distribution
def showPVDistribution(array, n_bins=1000, min=None, max=None, percentile=10, percentile_min=None, log_scale=None):

    # Get the limits for the current values
    min, max = _get_min_max(array, min=min, max=max, percentile=percentile, percentile_min=percentile_min)

    # Display the histogram
    _display_distribution(array, min, max, n_bins=n_bins, log_scale=log_scale)
