from .imageFrame import imagetoframe
import rasterio
from rasterio.mask import mask
import geopandas
import pandas
import rasterio

def extractbypolygon(imgpath,shppath,class_col=None):
    """
    Extract values from satellite image acoording to the given shapefile containing class information for classification.

    Parameters
    ----------
    imgpath : Path to satellite image.
    shppath : Path to ESRI shapefile.
    mode : mode of the operation no need to change, optional
        Don't change. The default is "r".
    class_col : Name of the column containing class values for classification.
        Need for arrange the table of output. The default is None.

    Returns
    -------
    tdataf : A table containing pixel values and corosponding class value.
        Need for train ML algo.

    """
    if class_col==None:
        print("Please enter the column name containing class information")
    else:
        img=rasterio.open(imgpath)
        meta=img.meta
        if not nod:
            nod = 0
        if 
        shp=geopandas.read_file(shppath)
        clsid=list(shp[class_col].unique())
        tdataf=pandas.DataFrame()
        for i in clsid:
            shpm=shp[shp[class_col]==i]
            maski,t=mask(img,shpm["geometry"])
            df=imagetoframe(maski)
            df = df[(df.T != int(nod)).any()]
            df[class_col]=int(i)
            tdataf=tdataf.append(df)
            tdataf=tdataf.reset_index(drop=True)
        return tdataf
