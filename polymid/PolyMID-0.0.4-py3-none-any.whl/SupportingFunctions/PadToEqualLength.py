def PadToEqualLength(array1,array2):
#     Inputs:
#     array1: an array whose length is to be made equal to that of array2 by lengthing the shorter of the two arrays by padding with 0s at the end
#     array2: an array whose length is to be made equal to that of array1 by lengthing the shorter of the two arrays by padding with 0s at the end

    # Import required packages
    import numpy as np

    len1 = len(array1)
    len2 = len(array2)

    n_zeros_needed = abs(len2 - len1)

    if len1 < len2:
        array1 = np.pad(array1,(0,n_zeros_needed),mode='constant')

    if len2 < len1:
        array2 = np.pad(array2,(0,n_zeros_needed),mode='constant')

    return(array1,array2)
