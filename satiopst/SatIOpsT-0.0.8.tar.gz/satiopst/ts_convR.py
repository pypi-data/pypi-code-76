import rasterio as rio
import numpy as np
import pandas as pd

def ts_stackR(imglist,replace_nodata=True):
    """
    Stack multi-time image list to stacked numpy array

    Parameters
    ----------
    imglist : list of image files.
        image file paths with directory and name.
    replace_nodata : True/False, optional
        convert nodata value to nan if present in the image metadata. The default is True.

    Returns
    -------
    ilist : stacked numpy array of images.
        where 3rd dim represent different time.
    meta : Updated metadata with new bands.

    """
    ilist=[]
    for i in imglist:
        with rio.open(i,"r") as sr:
            img=sr.read()
            meta=sr.meta
        ilist.append(img)
    ilist=np.vstack(ilist)
    meta['count']=ilist.shape[0]
    if replace_nodata==True:
        if meta['nodata'] != None:
            ilist[ilist==meta['nodata']]=np.nan
    return ilist,meta

def ts_frameR(imgarray,startD=None,endD=None,freq="D"):
    """
    Convert time series image array to time series frame. Where band represent Day, Month or Year.

    Parameters
    ----------
    imgarray : image as numpy ndarray.
    startD : Stating data of the image.
        In format of 'YYYY-MM-DD','YYYY' or 'DD'. The default is None.
    endD : End data of the image.
        In format of 'YYYY-MM-DD','YYYY' or 'DD'. The default is None.
    freq : time frequency.
        same as pandas timedate, Visit https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases. The default is "D".

    Returns
    -------
    iframe : Dataframe where index represent time and column represent pixels.
        DESCRIPTION.

    """
    if startD==None or endD==None:
        print("Please enter avalid Date.")
        return
    iarray=[]
    for i in range(imgarray.shape[0]):
        iarray.append(imgarray[i].flatten())
    iarray=np.asarray(iarray)
    iframe=pd.DataFrame(iarray,index=pd.date_range(startD,endD,freq=freq))
    return iframe

def ts_arrayR(imgframe,width=None,height=None):
    """
    Convert time series image frame to image array

    Parameters
    ----------
    imgframe : Stuctured image data.
        Time series image frame.
    width : Width of the image array.
    height : Height of the image array.

    Returns
    -------
    imgr : Image as numpy array.
        bands represent time.

    """
    if width==None or height==None:
        print("Please enter image width and height")
        return
    iarray=imgframe.to_numpy()
    imgr=[]
    if len(imgframe.columns)==1:
        imgr=iarray[0].reshape(height,width)
    else:
        for i in range(iarray.shape[0]):
            imgr.append(iarray[i].reshape(height,width))
    imgr=np.asarray(imgr)
    return imgr
