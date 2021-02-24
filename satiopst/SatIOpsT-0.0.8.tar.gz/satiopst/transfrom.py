import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

def reprojectR(imgpath,save_disk=False,out_proj=None,out_nodata=None,resample_method=Resampling.nearest):
    """
    Reproject raster from one coordinate system to another.

    Parameters
    ----------
    imgpath : Path to satellite image.
    save_disk : save image to disk, optional
        If true, it save reprojected image in the image directory. The default is False.
    out_proj : EPGS code in the format of 'EPGS:4326', to the coordinate system you want to reproject, optional
        visit https://epsg.io/ to get EPSG code. The default is None.
    out_nodata : nodata value for output image, optional
        It fill the outer values. The default is None.
    resample_method : Resampling method same as rasterio.warp.Resampling, optional
        Resampling.nearest, Resampling.bilinear, Resampling.cubic visit https://rasterio.readthedocs.io/en/latest/api/rasterio.warp.html for more info. The default is Resampling.nearest.

    Returns
    -------
    Image as ndArray
        Nd numpy array .
    Image metadata
        Metadata of the reprojected image.

    """
    if out_proj==None:
        return print("Provide a valid EPSG code in format of 'EPSG:4326'.")
    s=rasterio.open(imgpath)
    t, w, h = calculate_default_transform(s.crs, out_proj, s.width, s.height, *s.bounds)
    nmeta = s.meta.copy()
    nmeta.update({
        'nodata':out_nodata,
        'crs': out_proj,
        'transform': t,
        'width': w,
        'height': h
    })
    path=os.path.split(imgpath)[0]
    name="\\"+os.path.split(imgpath)[1].split(".")[0]+"_reproj"+"."+os.path.split(imgpath)[1].split(".")[1]
    if len(path)==0:
        path=os.getcwd()
    path+=name
    with rasterio.open(path, 'w', **nmeta) as d:
        for i in range(1, s.count + 1):
            reproject(
                source=rasterio.band(s, i),
                destination=rasterio.band(d, i),
                src_transform=s.transform,
                src_crs=s.crs,
                dst_transform=t,
                dst_crs=out_proj,
                dst_nodata=out_nodata,
                resampling=resample_method)

    with rasterio.open(path,"r") as re:
        imgA=re.read()
        meta=re.meta
    if save_disk==False:
        os.remove(path)
    return imgA , meta

