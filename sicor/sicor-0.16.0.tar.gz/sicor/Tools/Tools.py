import os
from os.path import dirname, isfile, splitext, join
import numpy as np
import gdal
from gdalconst import GA_ReadOnly
import logging
import inspect
import sys
from pkg_resources import resource_filename, Requirement, DistributionNotFound


def get_data_file(module_name, file_basename):
    """Find path to data files either locally or within installed module.
    :param module_name: name od the module to look for data
    :param file_basename: basename of the file to locate
    :raises FileNotFoundError if file can not be found
    """
    try:
        fn = resource_filename(Requirement.parse(module_name), os.path.join("data", file_basename))
        if isfile(fn) is False:
            raise FileNotFoundError(fn, os.listdir(os.path.dirname(fn)))

    except (FileNotFoundError, DistributionNotFound):
        fn = join(dirname(inspect.getfile(sys._getframe(1))), "data", file_basename)
        if isfile(fn) is False:
            raise FileNotFoundError((module_name, file_basename, fn))

    if isfile(fn) is False:
        raise FileNotFoundError(fn, file_basename)
    else:
        return fn


def fl(inp, dec):
    """ Floor inp by number of decimals as given by dec

    :param inp: input, float
    :param dec: integer, number of decimals
    :return: floored value
    """
    return np.floor(inp * 10 ** dec) / 10 ** dec


def cl(inp, dec):
    """ Ceil inp by number of decimals as given by dec

    :param inp: input, float
    :param dec: integer, number of decimals
    :return: ceiled value
    """
    return np.ceil(inp * 10 ** dec) / 10 ** dec


def _fmt_funktion_id(data, nodata_value=None):
    """Format function for write_raster_gdal
    :param data:
    :param nodata_value: All non-finite in data will be replaced by nodada_value.
    :return: data like array, with non finite values replaced with nodata_value
    """
    if nodata_value is None:
        return data
    else:
        bf = np.copy(data)
        bf[not np.isfinite(bf)] = nodata_value
        return bf


def read_image_gdal(filename):
    """ read image file using gdal, driver is determined by gdal

    :param filename:
    :return: numpy array with image data
    """

    if isfile(filename):
        gdal.AllRegister()
        ds = gdal.Open(filename, GA_ReadOnly)
    else:
        raise FileNotFoundError(filename)
    if ds is not None:
        return np.array(ds.GetRasterBand(1).ReadAsArray())
    else:
        raise ValueError("GDAL was unable to open file:%s" % filename)


def write_raster_gdal(data, filename, gdal_type=gdal.GDT_UInt16, driver=None, output_ss=None, order=1, metadata=None,
                      projection=None, geotransform=None, logger=None, options=None, nodata_value=None,
                      fmt_funktion=_fmt_funktion_id):
    """
    Write numpy array to an image file using gdal.

    :param nodata_value:
    :param data: numpy array
    :param filename: destination filename
    :param gdal_type: GDAL type, e.g. gdal.GDT_Int16
    :param driver: either None or string with internal gdal name for file writing, if None, a default driver is selected
    :param projection: e.g. 'PROJCS["WGS 84 / UTM zone 31N",[...],UNIT["metre",1,AUTHORITY["EPSG","9001"]],
           AUTHORITY["EPSG","32631"]]'
    :param geotransform: e.g. (600000.0, 60.0, 0.0, 4900020.0, 0.0, -60.0)
    :param options: list or tuple with option stings for gdal.create, e.g. jp2,losless:
           ["QUALITY=100", "REVERSIBLE=YES"] or jp2 lossy:["QUALITY=10","REVERSIBLE=NO"]
    :param logger: either None or logging instance, if None, a generic logger is created
    :param output_ss: changed spatial sampling, if given gt is updated in resampling is performed (used order)
    :param order: order of resampling is output_ss is different from geotransform
    :param metadata: dictionary with metadata, writen for raster band
    :param fmt_funktion: function to apply on data, e.g. lambda x: x as identity
    :return: None
    """
    from scipy.ndimage import zoom  # import here to avoid static TLS ImportError

    # get logger
    logger = logger or logging.getLogger(__name__)

    logger.info("Write: %s" % filename)

    if driver is None:  # select driver from default
        driver = {".jp2": "JP2OpenJPEG", ".tif": "GTiff"}[splitext(filename)[1]]
    logger.info("GDAL driver: %s" % driver)

    if output_ss is not None:
        assert geotransform is not None
        zoom_fac = float(geotransform[1]) / output_ss
        if zoom_fac != 1.0:
            logger.info("Zoom factor: %f" % zoom_fac)
            geotransform_new = list(geotransform)
            geotransform_new[1] = geotransform[1] / zoom_fac
            geotransform_new[5] = geotransform[5] / zoom_fac

            logger.info("Original geotransform: %s" % str(geotransform))
            geotransform = tuple(geotransform_new)
            logger.info("New geotransform: %s" % str(geotransform))

            logger.info("Original data shape: %s" % str(data.shape))
            dtype = data.dtype
            data = np.array(zoom(np.array(data, dtype=float), zoom_fac, order=order), dtype=dtype)
            logger.info("New data shape: %s" % str(data.shape))

    gdal.AllRegister()
    # random acces driver ?
    ra_driver = True if driver not in ["JP2OpenJPEG", "JP2KAK"] else False
    logger.info("Random_Access Driver: %s" % str(ra_driver))
    # common opts for both cases
    opts = (data.shape[0], data.shape[1], 1, gdal_type)
    if ra_driver:
        dset = gdal.GetDriverByName(driver).Create(filename, *opts, options=options)
    else:
        dset = gdal.GetDriverByName("MEM").Create("", *opts)  # use empty string for in memory dataset

    bnd = dset.GetRasterBand(1)
    bnd.WriteArray(fmt_funktion(data, nodata_value=nodata_value))
    if metadata is not None:
        logger.info("Set metadata: %s" % str(metadata))
        bnd.SetMetadata({str(key): str(value) for key, value in metadata.items()})

    if nodata_value is not None:
        bnd.SetNoDataValue(nodata_value)

    bnd.FlushCache()

    if projection is not None:
        dset.SetProjection(projection)

    if geotransform is not None:
        dset.SetGeoTransform(geotransform)

    if ra_driver is False:
        """
        if driver doesn't support random writes, need to create data first (here in memory)
        and use CreateCopy from that data set
        """
        ds_cp = gdal.GetDriverByName(driver).CreateCopy(filename, dset, options=options)
        ds_cp.FlushCache()
        ds_cp = None
        del ds_cp

    dset = None
    del dset
    return None
