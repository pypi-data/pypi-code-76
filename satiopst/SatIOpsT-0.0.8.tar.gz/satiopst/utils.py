import rasterio
from rasterio.mask import mask
import geopandas
import numpy

def icrop(imgpath,shppath):
    """
    Crop satellite image using ESRI shapefile

    Parameters
    ----------
    imgpath : Path to satellite image.
    shppath : Path to ESRI shapefile.

    Returns
    -------
    mask1 : Satellite image as numpy ndarray
        Same extent of raw image.
    meta : Metadata of image.
        Needed at the time of save image.

    """
    shp=geopandas.read_file(shppath)
    img=rasterio.open(imgpath,"r")
    meta=img.meta
    mask1,a=mask(img, shp.envelope)
    return mask1,meta

def imask(imgpath,shppath,nodata=0):
    """
    Mask image according ESRI shapefile area.

    Parameters
    ----------
    imgpath : Path to satellite image.
    shppath : Path to ESRI shapefile.
    nodata : no data value, optional
        Value used for fill the outer shapefile area. The default is 0.

    Returns
    -------
    mask1 : Satellite image as numpy ndarray
        Same extent of raw image.
    meta : Metadata of image.
        Needed at the time of save image.

    """
    shp=geopandas.read_file(shppath)
    img=rasterio.open(imgpath,"r")
    meta=img.meta
    if nodata!=0:
        mask1,a=mask(img, shp["geometry"])
        mask1[mask1==0]=nodata
    else:
        mask1,a=mask(img, shp["geometry"])
    return mask1,meta

def layerStack(imglist):
    """
    Stack bands of satellite image.

    Parameters
    ----------
    imglist : list of image files.
        image file paths with directory and name.

    Returns
    -------
    ilist : Satellite image as mumpy ndarray
        Stacked in same order of input list.
    immeta : Updated metadata of the image with same file format.
        Needed at the time of save image.

    """
    ilist=[]
    for i in imglist:
        with rasterio.open(i,"r") as im:
            im2=im.read(1)
            immeta=im.meta
        ilist.append(im2)
    ilist=numpy.asarray(ilist)
    immeta["count"]=ilist.shape[0]
    return ilist,immeta

def ndi(band_1,band_2,nodata=0,replace=True):
    """
    Normalized Difference Index. e.g. NDVI.

    Parameters
    ----------
    band_1 : First band of the index
        e.g. NIR band for NDVI.
    band_2 : Second band of the index
        e.g. RED band for NDVI.
    nodata : nodata value if any present in the input image, optional
        The default is 0.
    replace : Change the nodata value to nan, optional
        If True change the nodata value to np.nan. The default is True.

    Returns
    -------
    index : Normalized Difference Index.

    """
    band_1[band_1==nodata]=numpy.nan
    band_2[band_2==nodata]=numpy.nan
    index=(band_1-band_2)/(band_1+band_2)
    if replace == False:
        index=numpy.nan_to_num(index,nan=nodata)
    return index