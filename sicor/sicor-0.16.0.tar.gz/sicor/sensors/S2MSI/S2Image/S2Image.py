"""Read Sentinel-2 Level-1C and Level-2A data into RSImage object."""
import logging
import re
import warnings
from glob import glob
import os
from os import path
from os.path import abspath
from subprocess import call
from tempfile import TemporaryFile
from time import time
from uuid import uuid1
from xml.etree.ElementTree import QName
import xml.etree.ElementTree
import gdal
import glymur
import iso8601
import matplotlib.pyplot as plt
import numpy as np
import osr
import pandas as pd
import pyproj
from PIL import Image
from gdalconst import GA_ReadOnly
from geoarray import GeoArray
from psutil import virtual_memory

from ...RSImage import RSImage
from ..GranuleInfo import GranuleInfo


def get_tck(x, y, z, kk_default=3, logger=None):
    """Estimate spline model parameters."""
    from scipy.interpolate import bisplrep  # import here to avoid static TLS ImportError

    logger = logger or logging.getLogger(__name__)
    # estimate max number of allowed spline order
    mm = len(x)
    kk_max = int(np.floor(np.sqrt(mm / 2.0) - 1))
    kk = np.min([kk_default, kk_max])

    result = bisplrep(x=x, y=y, z=z, kx=kk, ky=kk, full_output=1)
    if result[2] > 0:
        logger.info("Interpolation problem:%s" % result[-1])
        logger.info("Now, try to adjust s")
        result = bisplrep(x=x, y=y, z=z, kx=kk, ky=kk, s=result[1], full_output=1)
        if result[2] > 0:
            raise ValueError("Interpolation problem:%s" % result[-1])
    return result[0]


# noinspection PyMissingConstructor,PyShadowingNames
class S2Image(RSImage):
    """Load Sentinel-2 Level-1C or Level-2A product."""
    # noinspection PyDefaultArgument,PyDictCreation
    def __init__(self, granule_path, import_bands="all",
                 namespace_candidate=None, aux_fields=None, default_u=1.0,
                 target_resolution=None, dtype_float=np.float16, dtype_int=np.int16, unit="reflectance",
                 interpolation_order=1, data_mode="dense", driver="OpenJpeg2000",
                 call_cmd=None, logger=None, slice_x=slice(None), slice_y=slice(None),
                 default_solar_irradiance={'B01': 1913.57, 'B02': 1941.63, 'B03': 1822.61, 'B04': 1512.79,
                                           'B05': 1425.56, 'B06': 1288.32, 'B07': 1163.19, 'B08': 1036.39,
                                           'B09': 813.04, 'B10': 367.15, 'B11': 245.59, 'B12': 85.25, 'B8A': 955.19},
                 **kwarg):
        """
        Reads Sentinel-2 MSI data into numpy array. Images for different channels are resampled to a common sampling
        :param granule_path: path to granule folder, folder should contain IMG_DATA folder and S2A_[..].xml file
        :param import_bands: list of bands to import, default: ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08',
                                                                                    'B8A', 'B09', 'B10', 'B11', 'B12',]
        :param namespace_candidate: for XML file, or None, then several default namespaces are tested
        :param target_resolution: spatial resolution in meter, or None for data not interpolated
        :param interpolation_order: integer for interpolation 1,2,3
        :param data_mode: either "dense" or "sparse"
        :param aux_fields: either None or dict of to be loaded aux fields, e.g. {"cwv":[ss],"spr":[ss],"ozo":[ss]}
                           with ss being "mean" or iterable of spatial samplings, e.g. [20.0] or [20.0,60.0]
        :param driver: should be "OpenJpeg2000" -> glymur, "kdu_expand"->shell command, "gdal_[driver] e.g. gdal_JP2ECW
                       gdal_JPEG2000, gdal_JP2OpenJPEG,gdal_JP2KAK


        ..todo:: Real nodata mask

        """
        # import here to avoid static TLS ImportError
        from scipy.interpolate import bisplev
        from scipy.ndimage.interpolation import zoom

        t0_init = time()

        self.full_band_list = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B10', 'B11',
                               'B12']
        self.logger = logger or logging.getLogger(__name__)
        self.metadata = {}
        self.namespace = namespace_candidate
        self.call_cmd = call_cmd

        self.sliceX = slice(None, None, None)
        if isinstance(slice_x, slice):
            self.sliceX = slice_x
        self.sliceY = slice(None, None, None)
        if isinstance(slice_y, slice):
            self.sliceY = slice_y

        self.driver = str(driver)
        if unit in ["reflectance", "dn"]:
            self.unit = unit
        else:
            raise ValueError("Unit not implemented: %s" % str(unit))

        self.dtype_float = dtype_float
        self.dtype_int = dtype_int

        if self.unit == "dn":
            self.dtype_return = self.dtype_int
            self.bad_data_value = -999
        else:
            self.dtype_return = self.dtype_float
            self.bad_data_value = np.nan

        self.target_resolution = target_resolution
        self.S2_MSI_granule_path = path.abspath(granule_path)
        self.tile_name = re.search('_T[0-9]{2,2}[A-Z]{3,3}_', self.S2_MSI_granule_path).group(0).replace("_", "")[1:]

        # find XML files for granule (granule folder) and product (two folders above granule folder)
        self.granule_xml_file_name = self.get_granule_metadata_xml()

        if self.namespace is not None:
            self.metadata.update(S2Image.parse_s2_granule_xml(self.granule_xml_file_name, self.namespace))
        else:
            self.logger.info("No namespace was given, try default ones:")
            for namespace_candidate in ["https://psd-12.sentinel2.eo.esa.int/PSD/S2_PDI_Level-1C_Tile_Metadata.xsd",
                                        "https://psd-12.sentinel2.eo.esa.int/PSD/S2_PDI_Level-2A_Tile_Metadata.xsd",
                                        "https://psd-14.sentinel2.eo.esa.int/PSD/S2_PDI_Level-1C_Tile_Metadata.xsd"]:
                self.logger.info("Namespace:%s" % namespace_candidate)
                try:
                    self.metadata.update(S2Image.parse_s2_granule_xml(self.granule_xml_file_name, namespace_candidate))
                    self.namespace = namespace_candidate
                except Exception:  # go over any exception, raise later if self.namespace is still None
                    pass
            if self.namespace is None:
                raise ValueError("None of the default xml namespaces worked, please supply as parameter.")
            else:
                self.logger.info("Final namespace: %s" % self.namespace)

        try:
            self.product_xml_file_name = glob(path.join(path.dirname(path.dirname(self.S2_MSI_granule_path)),
                                                        "*MTD*.xml"))[0]
            self.metadata.update(S2Image.parse_s2_product_xml(self.product_xml_file_name))
            self.metadata['solar_irradiance'] = {
                self.metadata['bandId2bandName'][bi]: self.metadata['solar_irradiance_bid'][bi] for bi in
                self.metadata['solar_irradiance_bid'].keys()}
        except IndexError:
            self.product_xml_file_name = None
            self.logger.info("Product xml file is not available -> fallback to default values.")
            self.metadata.update({"dn2rfl": 10000,
                                  "solar_irradiance": default_solar_irradiance,
                                  "physical_gains": None,
                                  "U": default_u})
        except AttributeError:
            # apparantly the xml is not L1C
            self.metadata.update({"dn2rfl": 10000})

        self.logger.info("Load S2 MSI data from:%s" % self.S2_MSI_granule_path)
        if os.name == "nt":
            warnings.warn("Reading Sentinel-2 aux data in grib file format is not supported on Windows."
                          "Alternatively, please download aux data from ECMWF in netCDF file format.")
        else:
            self.metadata["aux_data"] = S2Image.read_aux_data(self.S2_MSI_granule_path)

        # select bands
        if import_bands == "all":
            self.band_list = self.metadata["bandNames"]
        else:
            self.band_list = list(import_bands)
        # search for jp2 files which contain the data
        self.band_fns = {self._band_name_l1c(fn): fn for fn in
                         glob(path.join(self.S2_MSI_granule_path, "IMG_DATA", "*_B*.jp2"))}

        suffix = ""
        self.band_fns.update({self._band_name_l2a(fn): fn for fn in glob(path.join(
            self.S2_MSI_granule_path, "IMG_DATA", "R[1,2,6]0m", "*_[1,2,6]0m%s.jp2" % suffix))})
        self.band_list = list(self.band_fns)

        # import masks
        self.msk_fns = glob(path.join(self.S2_MSI_granule_path, "*_MSK_*[1,2,6]0m%s.jp2" % suffix))
        self.msk = {self._spatial_sampling_msk(fn): GeoArray(fn) for fn in self.msk_fns}

        # set final sizes
        if self.target_resolution is None:
            self.final_shape = None
            self.data = {}
        elif self.target_resolution in self.metadata["spatial_samplings"].keys():
            ss = self.metadata["spatial_samplings"]
            self.full_shape = [ss[self.target_resolution][ii] for ii in ("NROWS", "NCOLS")]
            self.final_shape = list(np.empty(self.full_shape)[self.sliceX, self.sliceY].shape)

            self.logger.info("Final shape for each channel: %s" % str(self.final_shape))
            if data_mode == "dense":
                self.data = self.__zeros__(shape=(self.final_shape + [len(self.band_list)]),
                                           dtype=self.dtype_return, logger=self.logger)
            elif data_mode == "sparse":
                self.data = self.__zeros__(shape=list(self.final_shape) + [len(self.metadata["bandNames"])],
                                           dtype=self.dtype_return, logger=self.logger)
            else:
                raise ValueError("data_mode=%s not implemented" % data_mode)
        else:
            raise ValueError("target_resolution should be None or in: %s" %
                             str(list(self.metadata["spatial_samplings"].keys())))

        # simple nodata mask -> should be improved
        try:
            self.nodata = {10.0: self.__read_img(self.band_fns["B02"]) == 0}
        except KeyError:
            self.nodata = {10.0: self.__read_img(self.band_fns["B02_10m"]) == 0}

        self.nodata[20.0] = zoom(self.nodata[10.0], 1 / 2, order=0)
        self.nodata[60.0] = zoom(self.nodata[10.0], 1 / 6, order=0)
        self.yesdata = {tr: np.logical_not(msk) for tr, msk in self.nodata.items()}

        # get projection for all bands
        self.metadata["projection"] = {band: S2Image.get_projection(self.band_fns[band]) for band in self.band_list}

        self.cnv = {}
        _t0 = time()
        for iband, band in enumerate(self.band_list):
            t0 = time()
            image_data_raw = self.__read_img(self.band_fns[band])

            if self.unit == "reflectance":
                # make image conversion on high precision, then convert to final type
                image_data = np.array(np.array(image_data_raw[:, :], dtype=np.float64) / self.metadata["dn2rfl"],
                                      dtype=self.dtype_return)

            elif self.unit == "dn":
                image_data = np.array(image_data_raw[:, :], dtype=self.dtype_return)

            image_data[self.bad_data_mask(image_data)] = self.bad_data_value

            if self.target_resolution is None:
                self.data[band] = np.array(image_data, dtype=self.dtype_float)
                t2 = time()
                self.logger.info("Read band %s in %.2fs." % (band, t2 - t0))
            else:
                zoom_fac = self.metadata["shape_to_resolution"][image_data.shape] / self.target_resolution
                if data_mode == "dense":
                    ii = iband
                elif data_mode == "sparse":
                    ii = self.full_band_list.index(band)
                else:
                    raise ValueError("data_mode=%s not implemented" % data_mode)
                t1 = time()
                # noinspection PyUnresolvedReferences
                self.data[:, :, ii] = zoom(input=np.array(image_data, dtype=np.float32),
                                           zoom=zoom_fac,
                                           order=interpolation_order)[self.sliceX, self.sliceY]
                self.cnv[ii] = band
                self.cnv[band] = ii
                t2 = time()
                self.logger.info("""Read band %s in %.2fs, pure load time:%.2fs, resample time: %.2fs, zoom: %.3f,
final shape: %s, index: %i""" % (band, t2 - t0, t1 - t0, t2 - t1, zoom_fac, str(self.final_shape), ii))
        self.logger.info("Total time for reading and converting bands: %.2fs" % (time() - _t0))

        if self.target_resolution is None:
            self.band_spatial_sampling = {band: self.metadata['shape_to_resolution'][data.shape]
                                          for band, data in self.data.items()}
            self.spatial_sampling_shapes = {self.band_spatial_sampling[band]: data.shape
                                            for band, data in self.data.items()}

        if aux_fields is not None and self.metadata["aux_data"]:
            self.logger.info("Read aux-data from level 1C Product.")
            ti = GranuleInfo(version="lite")[self.tile_name]
            zm = 2 * np.ceil(np.mean(self.metadata["aux_data"]["lons"].shape))

            lats_s2 = zoom(np.array([[ti["tl"]["lat"], ti["tr"]["lat"]], [ti["ll"]["lat"], ti["lr"]["lat"]]]), zoom=zm)
            lons_s2 = zoom(np.array([[ti["tl"]["lon"], ti["tr"]["lon"]], [ti["ll"]["lon"], ti["lr"]["lon"]]]), zoom=zm)

            fields_func = {field: get_tck(x=self.metadata["aux_data"]["lons"].flatten(),
                                          y=self.metadata["aux_data"]["lats"].flatten(),
                                          z=self.metadata["aux_data"][field].flatten()
                                          ) for field in aux_fields.keys()}

            self.fields_func = fields_func
            self.aux_fields = {}
            self.aux_fields["lats_s2"] = lats_s2
            self.aux_fields["lons_s2"] = lons_s2

            for field_name in aux_fields.keys():
                self.logger.info("Interpolate: %s" % field_name)
                bf = np.zeros(lats_s2.shape)
                for ii0 in range(lats_s2.shape[0]):
                    for ii1 in range(lats_s2.shape[1]):
                        # noinspection PyUnresolvedReferences
                        bf[ii0, ii1] = bisplev(x=lons_s2[ii0, ii1],
                                               y=lats_s2[ii0, ii1],
                                               tck=fields_func[field_name])

                if self.final_shape is not None:
                    zoom_fac = (self.full_shape[0] / bf.shape[0],
                                self.full_shape[1] / bf.shape[1])
                    bf_zoom = zoom(bf, zoom_fac, order=3)
                    self.aux_fields[field_name] = np.array(bf_zoom[self.sliceX, self.sliceY], dtype=np.float32)
                else:
                    if aux_fields[field_name] == "mean":
                        self.aux_fields[field_name] = np.mean(bf)
                    else:
                        self.aux_fields[field_name] = {}
                        for spatial_sampling, res in self.metadata["spatial_samplings"].items():
                            if spatial_sampling in aux_fields[field_name]:
                                zoom_fac = (res["NCOLS"] / bf.shape[0], res["NROWS"] / bf.shape[0])
                                bf_zoom = zoom(bf, zoom_fac, order=3)
                                self.aux_fields[field_name][spatial_sampling] = np.array(bf_zoom, dtype=np.float32)
                                self.logger.info("Interpolate: %s, zoom: %s, sampling: %f" %
                                                 (field_name, "(%.1f,%.1f)" % zoom_fac, spatial_sampling))

        if ("lats" not in self.metadata['aux_data']) or ("lats" not in self.metadata['aux_data']):
            # if lons or lats are missing from metadata -> add from tile info
            self.logger.warning("Missing lon/lats from aux data -> get it from granule info.")
            ti = GranuleInfo(version="lite")[self.tile_name]
            lats = np.zeros((2, 2), dtype=float)
            lons = np.zeros((2, 2), dtype=float)
            try:
                for i1, tb in enumerate(["t", "l"]):
                    for i2, lr in enumerate(["l", "r"]):
                        lons[i1, i2] = ti["%s%s" % (tb, lr)]["lon"]
                        lats[i1, i2] = ti["%s%s" % (tb, lr)]["lat"]
                self.metadata['aux_data']["lats"] = zoom(lats, 5)
                self.metadata['aux_data']["lons"] = zoom(lons, 5)
            except KeyError:
                logger.warning("Granule info incomplete:" + str(ti))

        self.logger.info("Total runtime: %.2fs" % (time() - t0_init))

    def get_granule_metadata_xml(self):
        """Try to find metadata xml file for the granule."""
        path_buffer = path.join(self.S2_MSI_granule_path, "MTD_TL.xml")
        if path.exists(path_buffer):
            # new style naming convention
            return path_buffer
        else:
            # test for style naming convention, only one file should match this pattern
            path_buffers = glob(path.join(self.S2_MSI_granule_path, "*_L[12][AC]_TL*.xml"))
            path_buffers = [bf for bf in path_buffers if ".aux.xml" not in bf]  # exclude gdal metadata

            if len(path_buffers) == 1:
                return path_buffers[0]
            else:
                raise FileNotFoundError("No meta data xml file for the granule was found: %s, search path: %s" % (
                    str(path_buffers), str(self.S2_MSI_granule_path)))

    @staticmethod
    def __zeros__(shape, dtype, max_mem_frac=0.3, logger=None):
        logger = logger or logging.getLogger(__name__)

        def in_memory_array(shape, dtype):
            """Use in-memory numpy array."""
            return np.zeros(shape, dtype)

        def out_memory_array(shape, dtype):
            """Fall back to memory mapped file if memory is not sufficient."""
            logger.warning("Not enough memory to keep full image -> fall back to memorymap.")
            dat = np.memmap(filename=TemporaryFile(mode="w+b"), dtype=dtype, shape=tuple(shape))
            dat[:] = 0.0
            return dat

        to_gb = 1.0 / 1024.0 ** 3
        mem = virtual_memory().total * to_gb
        arr = int(np.prod(np.array(shape, dtype=np.int64)) * np.zeros(1, dtype=dtype).nbytes * to_gb)

        if arr < max_mem_frac * mem:
            try:
                return in_memory_array(shape, dtype)
            except MemoryError:
                return out_memory_array(shape, dtype)
        else:
            logger.info(
                "Try to create array of size %.2fGB on a box with %.2fGB memory -> fall back to memorymap." % (
                    arr, mem))
            return out_memory_array(shape, dtype)

    @staticmethod
    def parse_s2_product_xml(fn):
        """
        S2 XML helper function to parse product xml file
        :param fn: file name of xml file
        :return: metadata dictionary
        """
        metadata = {}
        xml_root = xml.etree.ElementTree.parse(fn).getroot()
        metadata["dn2rfl"] = (int(xml_root.find(".//QUANTIFICATION_VALUE").text))
        metadata["solar_irradiance_bid"] = {int(ele.get('bandId')): float(ele.text) for ele in
                                            xml_root.find(".//Solar_Irradiance_List").findall("SOLAR_IRRADIANCE")}
        metadata["physical_gains"] = {int(ele.get('bandId')): float(ele.text) for ele in
                                      xml_root.findall(".//PHYSICAL_GAINS")}
        metadata["U"] = float(xml_root.find(".//U").text)
        return metadata

    @staticmethod
    def read_aux_data(fn):
        """
        Read grib file with aux data, return dictionary
        :param fn: path to granule
        :return: dict with data
        """
        import pygrib

        metadata = {}
        try:
            fn_aux_data = glob(path.join(fn, "AUX_DATA", "S2A_*"))[0]
            aux_data = pygrib.open(fn_aux_data)

            for var_name, index in zip(["cwv", "spr", "ozo"], [1, 2, 3]):
                metadata[var_name] = aux_data.message(index).data()[0]
                metadata["%s_unit" % var_name] = aux_data.message(index)["parameterUnits"]

            metadata["lats"], metadata["lons"] = aux_data.message(1).latlons()
            return metadata
        except Exception:
            return metadata

    @staticmethod
    def parse_s2_granule_xml(fn, namespace):
        """
        parse XML file in granule folder and return metadata
        :param fn: full filename tile xml file
        :param namespace: xml namespace
        :return: dictionary with metadata
        """

        def stack_detectors(inp):
            """Some data is given per detector with NaN values otherwise -> stack those to a common image."""
            warnings.filterwarnings(action='ignore', message=r'Mean of empty slice')
            res = {bandId: np.nanmean(np.dstack(tuple(inp[bandId].values())), axis=2) for bandId, dat in inp.items()}
            warnings.filterwarnings(action='default', message=r'Mean of empty slice')
            return res

        xml_root = xml.etree.ElementTree.parse(fn).getroot()
        metadata = {}

        general_info = S2Image.find_in_xml_root(namespace, xml_root, "General_Info")

        for key in ["TILE_ID", "DATASTRIP_ID", "TILE_ID_2A"]:
            try:
                metadata[key] = general_info.find(key).text
            except AttributeError:
                pass

        metadata["SENSING_TIME"] = iso8601.parse_date(general_info.find("SENSING_TIME").text)

        geo_codings = S2Image.find_in_xml_root(namespace, xml_root, 'Geometric_Info', "Tile_Geocoding")
        metadata["HORIZONTAL_CS_NAME"] = geo_codings.find("HORIZONTAL_CS_NAME").text
        metadata["HORIZONTAL_CS_CODE"] = geo_codings.find("HORIZONTAL_CS_CODE").text
        metadata["bandId2bandName"] = {
            int(ele.get("bandId")): re.search("_B[0-18][0-9A]", ele.text).group().split("_")[-1] for ele in
            xml_root.findall(".//MASK_FILENAME") if ele.get("bandId") is not None}

        metadata["bandName2bandId"] = {bandName: bandId for bandId, bandName in metadata["bandId2bandName"].items()}
        metadata["bandIds"] = sorted(list(metadata["bandId2bandName"].keys()))
        metadata["bandNames"] = sorted(list(metadata["bandName2bandId"].keys()))
        metadata["sun_zenith"] = S2Image.get_values_from_xml(S2Image.find_in_xml_root(namespace, xml_root, *(
            "Geometric_Info", "Tile_Angles", "Sun_Angles_Grid", "Zenith", "Values_List")))
        metadata["sun_azimuth"] = S2Image.get_values_from_xml(S2Image.find_in_xml_root(namespace, xml_root, *(
            "Geometric_Info", "Tile_Angles", "Sun_Angles_Grid", "Azimuth", "Values_List")))
        metadata["sun_mean_zenith"] = float(S2Image.find_in_xml_root(namespace, xml_root, *(
            "Geometric_Info", "Tile_Angles", "Mean_Sun_Angle", "ZENITH_ANGLE")).text)
        metadata["sun_mean_azimuth"] = float(S2Image.find_in_xml_root(namespace, xml_root, *(
            "Geometric_Info", "Tile_Angles", "Mean_Sun_Angle", "AZIMUTH_ANGLE")).text)

        branch = S2Image.find_in_xml_root(namespace, xml_root, *("Geometric_Info", "Tile_Angles"))
        metadata["viewing_zenith_detectors"] = {
            bandId: {bf.get("detectorId"): S2Image.get_values_from_xml(
                S2Image.find_in_xml(bf, *("Zenith", "Values_List"))) for bf in
                branch.findall("Viewing_Incidence_Angles_Grids[@bandId='%i']" % bandId)} for bandId in
            metadata["bandIds"]}

        try:
            metadata["viewing_zenith"] = stack_detectors(metadata["viewing_zenith_detectors"])
        except ValueError:
            metadata["viewing_zenith"] = 0.0

        metadata["viewing_azimuth_detectors"] = {bandId: {bf.get("detectorId"): S2Image.get_values_from_xml(
            S2Image.find_in_xml(bf, *("Azimuth", "Values_List"))) for bf in branch.findall(
                "Viewing_Incidence_Angles_Grids[@bandId='%i']" % bandId)} for bandId in metadata["bandIds"]}

        try:
            metadata["viewing_azimuth"] = stack_detectors(metadata["viewing_azimuth_detectors"])
        except ValueError:
            metadata["viewing_azimuth"] = 0.0

        metadata["spatial_samplings"] = {
            float(size.get("resolution")): {key: int(size.find(key).text) for key in ["NROWS", "NCOLS"]} for size in
            geo_codings.findall("Size")}
        for geo in geo_codings.findall("Geoposition"):
            metadata["spatial_samplings"][float(geo.get("resolution"))].update(
                {key: int(geo.find(key).text) for key in ["ULX", "ULY", "XDIM", "YDIM"]})
        metadata["shape_to_resolution"] = {(values["NCOLS"], values["NROWS"]): spatial_sampling for
                                           spatial_sampling, values in metadata["spatial_samplings"].items()}
        return metadata

    @staticmethod
    def find_in_xml_root(namespace, xml_root, branch, *branches, findall=None):
        """
        S2 xml helper function, search from root
        :param namespace:
        :param xml_root:
        :param branch: first branch, is combined with namespace
        :param branches: repeated find's along these parameters
        :param findall: if given, at final a findall
        :return: found xml object, None if nothing was found
        """
        buf = xml_root.find(str(QName(namespace, branch)))
        for br in branches:
            buf = buf.find(br)
        if findall is not None:
            buf = buf.findall(findall)
        return buf

    @staticmethod
    def find_in_xml(xml, *branch):
        """
        S2 xml helper function
        :param xml: xml object
        :param branch: iterate to branches using find
        :return: xml object, None if nothing was found
        """
        buf = xml
        for br in branch:
            buf = buf.find(br)
        return buf

    @staticmethod
    def get_values_from_xml(leaf, dtype=float):
        """
        S2 xml helper function
        :param leaf: xml object which is searched for VALUES tag which are then composed into a numpy array
        :param dtype: dtype of returned numpy array
        :return: numpy array
        """
        return np.array([ele.text.split(" ") for ele in leaf.findall("VALUES")], dtype=dtype)

    @staticmethod
    def _band_name_l1c(fn):
        """
        S2 helper function, parse band name from jp2 file name
        :param fn: filename
        :return: string with band name
        """
        return fn.split(".jp2")[0].split("_")[-1]

    @staticmethod
    def _spatial_sampling_msk(fn):
        return path.basename(fn).split(".jp2")[0].split("_")[10]

    @staticmethod
    def _band_name_l2a(fn):

        for pr in ["AOT", "WVP", "VIS", "TCI", "SCL"]:
            if pr in fn:
                return "%s_%s" % (pr, fn.split("_")[-1].split(".")[0])

        band_name = re.search('_B[0-9][0-9A]_', path.basename(fn).split(".jp2")[0]).group().replace("_", "")
        spatial_sampling = re.search('_[126]0m[_.]', path.basename(fn).split("jp2")[0]).group().replace("_",
                                                                                                        "").replace(".",
                                                                                                                    "")
        return "%s_%s" % (band_name, spatial_sampling)

    def bad_data_mask(self, image_data):
        """ Return mask of bad data
        :param image_data: numpy array
        :return: 2D boolean array
        """
        self.logger.warning("Masks are computed on value basis, provider masks are not yet implemented")
        nodata = self.nodata[self.metadata['shape_to_resolution'][image_data.shape]]
        assert nodata.shape == image_data.shape

        if self.unit == "reflectance":
            return nodata
        elif self.unit == "dn":
            return nodata
        else:
            raise ValueError("Unit not implemented: %s" % self.unit)

    def __read_img(self, fn):
        self.logger.info("Reading: %s" % fn)
        if self.driver == "OpenJpeg2000":
            img = np.array(glymur.Jp2k(fn)[:, :], dtype=np.int16)
        elif self.driver == "kdu_expand":
            img = self.__read_jp2_kdu_app(fn, call_cmd=self.call_cmd)
        elif re.search("gdal[_]", self.driver) is not None:
            img = S2Image.gdal_read(fn, self.driver.split("_")[-1])
        else:
            raise ValueError("Driver not supported: %s" % self.driver)

        return img

    @staticmethod
    def __rd(fn):
        return fn

    @staticmethod
    def __read_jp2_kdu_app(fn, call_cmd=None):
        fn_tmp = "/dev/shm/%s.tif" % uuid1()
        cmd_kdu = "kdu_expand -i %s -o %s -fprec 16" % (abspath(fn), fn_tmp)
        cmd_rm = "rm %s" % fn_tmp

        if call_cmd is None:
            call(cmd_kdu, shell=True)
        else:
            call_cmd(cmd_kdu)

        dat = np.array(Image.open(fn_tmp), dtype=np.int16)

        if call_cmd is None:
            call(cmd_rm, shell=True)
        else:
            call_cmd(cmd_rm)

        return dat

    @staticmethod
    def gdal_read(fnjp, driver_name):
        """Read image file using gdal."""
        gdal.AllRegister()
        gdal_drivers = [gdal.GetDriver(ii).GetDescription() for ii in range(gdal.GetDriverCount())]
        if driver_name not in gdal_drivers:
            raise ValueError("Selected driver seems to be missing in gdal, available are: %s" % str(gdal_drivers))
        else:
            while gdal.GetDriverCount() > 1:
                for ii in range(gdal.GetDriverCount()):
                    drv = gdal.GetDriver(ii)
                    if drv is not None:
                        if drv.GetDescription() != driver_name:
                            try:
                                drv.Deregister()
                            except AttributeError:
                                pass

        ds = gdal.Open(fnjp, GA_ReadOnly)
        img = ds.GetRasterBand(1).ReadAsArray()
        # noinspection PyUnusedLocal
        ds = None
        return img

    @staticmethod
    def save_rgb_image(rgb_img, fn, dpi=100.0):
        """Save image as RGB to file system."""
        fig = plt.figure(figsize=np.array(rgb_img.shape[:2]) / dpi)
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        ax = plt.subplot()
        ax.imshow(rgb_img, interpolation="none")
        ax.set_axis_off()
        plt.savefig(fn, dpi=dpi)
        fig.clear()
        plt.close(fig)

    @staticmethod
    def transform_utm_to_wgs84(easting, northing, zone, south=False):
        """returns lon, lat, altitude"""
        utm = pyproj.Proj(proj='utm', zone=abs(zone), ellps='WGS84', south=(zone < 0 or south))
        return utm(easting, northing, inverse=True)

    @staticmethod
    def geotransform2mapinfo(gt, prj):
        """Builds an ENVI map info from given GDAL GeoTransform and Projection
        :param gt:  GDAL GeoTransform, e.g. (249885.0, 30.0, 0.0, 4578615.0, 0.0, -30.0)
        :param prj: GDAL Projection - WKT Format
        :returns: ENVI map info, e.g. [ UTM , 1 , 1 , 256785.0 , 4572015.0 , 30.0 , 30.0 , 43 , North , WGS-84 ]
        :rtype: list
        """
        if gt[2] != 0 or gt[4] != 0:  # TODO
            raise NotImplementedError('Currently, rotated datasets are not supported.')
        srs = osr.SpatialReference()
        srs.ImportFromWkt(prj)
        proj4 = [i[1:] for i in srs.ExportToProj4().split()]
        proj4_proj = [v.split('=')[1] for i, v in enumerate(proj4) if '=' in v and v.split('=')[0] == 'proj'][0]
        proj4_ellps = \
            [v.split('=')[1] for i, v in enumerate(proj4) if '=' in v and v.split('=')[0] in ['ellps', 'datum']][0]
        proj = 'Geographic Lat/Lon' if proj4_proj == 'longlat' else 'UTM' if proj4_proj == 'utm' else proj4_proj
        ellps = 'WGS-84' if proj4_ellps == 'WGS84' else proj4_ellps
        ul_x, ul_y, gsd_x, gsd_y = gt[0], gt[3], gt[1], gt[5]

        def utm2wgs84(utm_x, utm_y):
            return S2Image.transform_utm_to_wgs84(utm_x, utm_y, srs.GetUTMZone())

        def is_utm_north_south(lon_lat):
            return 'North' if lon_lat[1] >= 0. else 'South'

        map_info = [proj, 1, 1, ul_x, ul_y, gsd_x, abs(gsd_y), ellps] if proj != 'UTM' else \
            ['UTM', 1, 1, ul_x, ul_y, gsd_x, abs(gsd_y), srs.GetUTMZone(), is_utm_north_south(utm2wgs84(ul_x, ul_y)),
             ellps]
        return map_info

    @staticmethod
    def get_projection(file_name):
        """
        :param file_name string, points to filename
        :return: return {"gt":geotransform,"prj":coordinate projections string} for filename
        :rtype dict
        """
        ds = gdal.Open(file_name)
        gt = ds.GetGeoTransform()
        prj = ds.GetProjection()
        ds = None  # release memory
        # noinspection PyBroadException
        try:
            mapinfo = S2Image.geotransform2mapinfo(gt, prj)
        except Exception:
            mapinfo = None

        return {"gt": gt, "prj": prj, "mapinfo": mapinfo}


class s2_snr_model(object):
    """Sentinel-2 SNR model from CNES instrument characterization.
    :param: s2_snr_csv_file: path to valid s2_snr_csv_file, e.g. line: B1,129.0,588,"0,04840000","0,00003130",
    "4,07374605","129,00","525,5132410906","0,1370807224","941,05","1614,99","983,3"
    :param: rfl_to_rad: dict with band names as keys and conversion factor from reflectance to radiance, e.g.:
            rfl_to_rad={'B8a': 0.0, 'B12': 0.0, 'B10': 0.0, 'B03': 0.0, 'B07': 0.0, 'B04': 0.0, 'B11': 0.0,
            'B02': 0.0, 'B08': 0.0, 'B05': 0.0, 'B09': 0.0, 'B01': 0.0, 'B06': 0.0}
    """
    def __init__(self, s2_snr_csv_file, rfl_to_rad, logger=None):
        # get logger
        self.logger = logging.getLogger() if logger is None else logger
        # read data file
        self.s2_snr_csv_file = s2_snr_csv_file
        df = pd.read_csv(self.s2_snr_csv_file, decimal=",")
        to_band_name = (
            lambda x: x.upper() if len(x) == 3 else "B0" + x[1])  # normalize band names: Bx -> B0x and Byx -> Byx
        self.snr_parameters = {to_band_name(ll[0]): np.array([l.replace(",", ".") for l in ll[3:6]], dtype=float)
                               for ll in df.values[2:2 + 13, :]}
        self.rfl_to_rad = rfl_to_rad

    def noise(self, reflectance, band_name):
        """Sentinel-2 radiance to noise model"""
        # get noise model parameters: sqrt(x0^2+x1*x2*radiance)
        x = self.snr_parameters[band_name]
        rfl2rad = self.rfl_to_rad[band_name]
        #      (noise in radiance         ( -> to radiance             )) -> convert back to reflectance
        return np.sqrt(x[0] ** 2.0 + x[1] * (x[2] * reflectance * rfl2rad)) / rfl2rad  # noise reflectance
