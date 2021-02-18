import scipy.ndimage as scind
def mfilter(imgarray,size=3, stat="mean"):
    """
    Mean, Median and Mode filter

    Parameters
    ----------
    imgarray : Image as ndArray.
        Satellite image as n-Dim numpy array.
    size : Filter size.
        All are square filter just add int value of one size like 3.
    stat : TYPE, optional
        "mean", "median", "mode". The default is "mean".

    Returns
    -------
    Filtered image according to the statiatics and kernel.

    """
    if stat=="mean":
        fimg=scind.uniform_filter(imgarray,size=size)
    elif stat=="median":
        fimg=scind.median_filter(imgarray,size=size)
    elif stat=="mode":
        fimg=scind.maximum_filter(imgarray,size=size)
    else:
        print("Please provide a valid statistical method: mean, median or mode")
    return fimg

def edgedetection(imgarray,mode="sobel",size=3):
    """
    Edge detection functions

    Parameters
    ----------
    imgarray : Image as ndArray.
        Satellite image as n-Dim numpy array..
    mode : type of filter , optional
        "sobel", "sobelH", "sobelV", "laplace", "prewitt", "prewittH","prewittV". The default is "sobel".
    size : Size of kernel for laplace, optional
        kernel size only for laplace edge detection. The default is 3.

    Returns
    -------
    Edge detection on satellite image.

    """
    if mode=="sobel":
        sobel_v=scind.filters.sobel(imgarray,axis=-1)
        sobel_h=scind.filters.sobel(imgarray,axis=1)
        out=(sobel_v+sobel_h)/2
    elif mode=="sobelH":
        out=scind.filters.sobel(imgarray,axis=1)
    elif mode=="sobelV":
        out=scind.filters.sobel(imgarray,axis=-1)
    elif mode=="laplace":
        out=scind.morphological_laplace(imgarray,size=size)
    elif mode=="prewitt":
        prewitt_v=scind.filters.prewitt(imgarray,axis=-1)
        prewitt_h=scind.filters.prewitt(imgarray,axis=1)
        out=(prewitt_v+prewitt_h)/2
    elif mode=="prewittH":
        out=scind.filters.prewitt(imgarray,axis=1)
    elif mode=="prewittV":
        out=scind.filters.prewitt(imgarray,axis=-1)
    else:
        print("Please provide a valid statistical method: mean, median or mode")
    return out
    