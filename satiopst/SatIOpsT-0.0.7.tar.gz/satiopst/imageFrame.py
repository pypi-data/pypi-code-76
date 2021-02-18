import numpy
import pandas

def imagetoframe(imgarray):
    """
    Convert n-d image array to stucture data for ML algo.

    Parameters
    ----------
    imgarray : image as numpy ndarray.

    Returns
    -------
    satdf : satellite image as stuctured data.
        In the table columns represent bands and rows represent pixels.

    """
    imlist=[] # Blank list to store 1D array
    for i in range(imgarray.shape[0]):
        i2=imgarray[i].flatten() # Convert 2D array to 1D array
        imlist.append(i2) # Append to list
        imga=numpy.asarray(imlist) # Convert to array
        imgat=imga.transpose() # Transpose matrix for daataframe convertion
        satdf=pandas.DataFrame(imgat)
    return satdf

def frametoimage(imgframe,imgmeta):
    """
    To convert stuctured image frame to nd image array.

    Parameters
    ----------
    imgframe : Stuctured image data.
    imgmeta : Metadata of the image.
            Needed for get image width, height and band information.

    Returns
    -------
    rs : A nd numpy image array.

    """
    width=imgmeta["width"]
    height=imgmeta["height"]
    cou=len(imgframe.columns)
    narray=imgframe.to_numpy()
    if cou==1:
        tm=narray.transpose()
        rs=tm.reshape(height,width)
    else:
        tm=narray.transpose()
        iml=[]
        for i in range(tm.shape[0]):
            band=tm[i,:]
            band=band.reshape(height,width)
            iml.append(band)
        rs=numpy.asarray(iml)
    return rs
