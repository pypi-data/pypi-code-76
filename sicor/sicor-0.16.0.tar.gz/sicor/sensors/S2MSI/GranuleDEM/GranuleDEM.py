import json
import logging
import zipfile
from glob import glob
from os import remove, makedirs
from os.path import isdir, join, abspath, basename, dirname
from tempfile import TemporaryDirectory

import h5py
import numpy as np

from ....Tools import fill_nan
from ....Tools import write_raster_gdal
from ....Tools import read_image_gdal


class GranuleDEM(object):
    # noinspection PyDefaultArgument
    def __init__(self, fn, target_resolution=60, logger=None,
                 sampling_to_shape={10.0: (10980, 10980), 20.0: (5490, 5490), 60.0: (1830, 1830)},
                 zoom_order=2, slice_x=slice(None), slice_y=slice(None), **kwargs):
        """ get digital elevation models for S2 MSI Granules from archive

        :param fn: filename of DEM archive (zip file or hdf5 file) or path to dem folder structure
        :type fn: string
        :return: Dict like object which returns DEM for given granules if get_dem, [],or () are called
        """
        self.logger = logger or logging.getLogger(__name__)

        self.fn = fn
        self.ext = "tif"
        self.badvalue = -32768
        self.dtype = np.float32
        self.target_resolution = target_resolution
        self.sampling_to_shape = sampling_to_shape
        self.zoom_order = zoom_order
        assert type(slice_x) == slice
        self.sliceX = slice_x
        assert type(slice_y) == slice
        self.sliceY = slice_y

        if self.fn.split(".")[-1] == "zip":
            self.mode = "zip"
            self.get_dem = self._get_dem_zip
            # noinspection PyBroadException
            try:
                self.zf = zipfile.ZipFile(fn)
                self.tiles = sorted([bf.filename.split(".%s" % self.ext)[0] for bf in self.zf.filelist])
            except Exception:
                self.logger.warning("File:%s missing -> proceed for now." % self.fn)
                self.zf = None
                self.tiles = []

        elif self.fn.split(".")[-1] == "h5":
            self.mode = "h5"
            self.get_dem = None
            self.get_dem = self._get_dem_hdf5
            try:
                with h5py.File(name=self.fn, mode="r") as h5f:
                    self.h5f = h5f
                    self.tiles = sorted(list(self.h5f.keys()))
            except OSError:
                self.logger.warning("File:%s missing -> proceed for now." % self.fn)
                self.h5f = None
                self.tiles = []

        elif isdir(fn) is True:
            self.mode = "dir"
            self.get_dem = self._get_dem_dir
            self.dems = {basename(fn).split(".%s" % self.ext)[0]: abspath(fn) for fn
                         in glob(join(self.fn, "**/*.%s" % self.ext), recursive=True)}
            self.tiles = sorted(list(self.dems.keys()))
        else:
            raise ValueError("fn=%s is neither zip file or directory" % self.fn)

    def _to_arr(self, arr):
        return self._to_slice(self._to_target_resolution(self._to_dtype(arr)))

    def _to_target_resolution(self, arr):
        from scipy.ndimage import zoom  # import here to avoid static TLS ImportError

        zf = self.sampling_to_shape[self.target_resolution] / np.array(arr.shape, dtype=float)
        if zf[0] == 1.0 and zf[1] == 1.0:
            return arr
        else:
            return zoom(input=arr, zoom=zf, order=self.zoom_order)

    def _to_dtype(self, arr):
        if arr.dtype == self.dtype:
            return arr
        else:
            bad = arr == self.badvalue
            arr = np.array(arr, dtype=self.dtype)
            arr[bad] = np.nan
            fill_nan(arr)
            return arr

    def _to_slice(self, arr):
        if self.sliceX == slice(None) and self.sliceY == slice(None):
            return arr
        else:
            return arr[self.sliceX, self.sliceY]

    def _get_dem_hdf5(self, tile):
        try:
            return self._to_arr(self.h5f[tile][()])
        except KeyError:
            raise ValueError("The tile:%s is missing in this archive. Included are: %s" % (tile, str(list(self.tiles))))

    def _get_dem_zip(self, tile):
        with TemporaryDirectory() as tmp_dirname:
            try:
                fn = self.zf.extract(self.zf.getinfo("%s.%s" % (tile, self.ext)), path=tmp_dirname)
            except Exception:
                raise ValueError("The tile:%s if missing in this archive. Included are: %s" % (tile, str(self.tiles)))
            else:
                dat = self._to_arr(read_image_gdal(fn))
                return dat

    def _get_dem_dir(self, tile):
        try:
            return self._to_arr(read_image_gdal(self.dems[tile]))
        except KeyError:
            raise ValueError("The tile:%s is missing in this archive. Included are: %s" % (tile, str(list(self.tiles))))

    # noinspection PyDefaultArgument
    def dem_to_file(self, tile, filename, driver_map={"tif": "gtiff"}, lat_lon=None, extent=None):
        """ Write digital elevation data to file
        :param extent:
        :param lat_lon:
        :param driver_map:
        :param tile: S2 MSI tile name e.g. '32UMU'
        :param filename: filename, string
        :return:None
        """
        from scipy.ndimage import zoom  # import here to avoid static TLS ImportError

        dem = np.array(self.get_dem(tile), dtype=np.uint16)
        makedirs(dirname(filename), exist_ok=True)
        try:
            remove(filename)
        except FileNotFoundError:
            pass
        file_ext = filename.split(".")[-1]
        driver = driver_map[file_ext]
        write_raster_gdal(data=dem, filename=filename, driver=driver)

        if extent is not None:
            extent = (lambda x: x["pos"] if "pos" in x else x)(extent)
            fn = filename.replace("." + file_ext, "_extent.json")
            with open(fn, "w") as fl:
                json.dump({"n": extent["tr"]["lat"],
                           "s": extent["ll"]["lat"],
                           "w": extent["ll"]["lon"],
                           "e": extent["tr"]["lon"]}, fl)

        if lat_lon is not None:
            lat_lon = (lambda x: x["pos"] if "pos" in x else x)(lat_lon)
            fnpat = filename.replace("." + file_ext, "_%s." + file_ext)
            zoom_fac = np.array(dem.shape) / 2.0
            ll = {ii: zoom(np.array(
                [[lat_lon["tl"][ii], lat_lon["tr"][ii]], [lat_lon["ll"][ii], lat_lon["lr"][ii]]], dtype=np.float32),
                zoom_fac) for ii in ["lat", "lon"]}

            for ii in ["lat", "lon"]:
                fn = fnpat % ii
                write_raster_gdal(data=ll[ii], filename=fn)

    def __call__(self, tile, return_zeros_if_missing=False):
        """ Wrapper for get_dem """
        try:
            if tile in self.tiles:
                return self.get_dem(tile)
            else:
                raise ValueError("Tile is missing")
        except ValueError as err:
            if return_zeros_if_missing is True:
                self.logger.warning(
                    "Tile: %s missing -> return zeros since return_zeros_if_missing=True was set." % tile)
                return np.zeros(self.sampling_to_shape[self.target_resolution], dtype=np.float16)
            else:
                raise err
