import rasterio

def imgRead(imgpath,mode="r"):
    """
    Import satellite image to python env.

    Parameters
    ----------
    imgpath : Path to satellite image.
    mode : mode of the operation no need to change, optional
        Don't change. The default is "r".

    Returns
    -------
    imgf : Image as nd Numpy array.
    imgmeta : Metadata of the image.

    """
    with rasterio.open(imgpath,mode) as img:
        imgf=img.read()
        imgmeta=img.meta
    return imgf,imgmeta


def imgWrite(imgarray,filepath,imgmeta,mode="w",bands=1):
    """
    Export or write satellite image from python enviroment to disk.

    Parameters
    ----------
    imgarray : Array of the satellite image.
    filepath : output file destination.
        With directory if needed.
    imgmeta : metadata for the image 
        DESCRIPTION.
    mode : mode of the operation no need to change, optional
        Don't change. The default is "w".
    bands : Number of bands in the image, optional
        Change according to the bands. The default is 1.

    Returns
    -------
    Export image to disk.

    """
    if bands==1:
        imgmeta["count"]=bands
        with rasterio.open(filepath,mode,**imgmeta) as imgc:
            imgc.write(imgarray,1)
    else:
        imgmeta["count"]=bands
        with rasterio.open(filepath,mode,**imgmeta) as imgc:
            imgc.write(imgarray)

