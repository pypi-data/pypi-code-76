"""Main module."""
def array2Raster(newRasterfn, rasterOrigin, pixelWidth, pixelHeight, array, epsg=3826):
    """"Convert a numpy array to a georeferenced raster
    newRasterfn: File name for output raster
    rasterOrigin: GDAL transformation matrix for the original raster
    pixelWidth: Width of the pixels
    pixelHeight: Height of the pixels
    epsg: The spatial reference for output raster. Default is 3826.
    array: Numpy array that contains the raster cells.
    """
    cols = array.shape[1]
    rows = array.shape[0]
    originX = rasterOrigin[0]
    originY = rasterOrigin[1]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn,cols,rows,1,gdal.GDT_Float32)
    outRaster.SetGeoTransform((originX,pixelWidth,0,originY,0,pixelHeight))
    outBand = outRaster.GetRasterBand(1)
    outBand.WriteArray(array)

    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(epsg)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    
    outBand.FlushCache()