from __future__ import annotations
from typing import Optional, Sequence, Union, TYPE_CHECKING

import re
import uuid
from datetime import timedelta

# from geodesic.utils.memcache import cache

if TYPE_CHECKING:
    from geodesic import Item, Dataset

try:
    from osgeo import gdal

    gdal.UseExceptions()
except ImportError:
    gdal = None

try:
    import numpy as np
except ImportError:
    np = None

try:
    from tqdm import tqdm
except ImportError:

    def tqdm(iterable, desc=None):
        return iterable


# from geodesic.typing import


gs_re = re.compile(r"gs://([\w\-]{1,})\/([\/\w\.\-]{1,})", re.UNICODE)
s3_re = re.compile(r"s3://([\w\-]{1,})\/([\/\w\.\-]{1,})", re.UNICODE)

if gdal is not None:
    resample_lut = {
        "nearest": gdal.GRA_NearestNeighbour,
        "bilinear": gdal.GRA_Bilinear,
        "lanczos": gdal.GRA_Lanczos,
        "cubic": gdal.GRA_Cubic,
        "cubic_spline": gdal.GRA_CubicSpline,
    }
else:
    resample_lut = {}


class Raster:
    """Handles raster data, typically MSI

    A class used as the main interface to raster data.

    Args:
        item: A Geodesic python api item object.
        dataset: A Geodesic Python API dataset object. Default: ``None``.
    """

    def __init__(self, item: Item, dataset: Dataset = None) -> None:

        self.item = item
        self.dataset = dataset

    def export_raster(
        self,
        bbox: Optional[Sequence] = None,
        bands: Sequence = ["red", "green", "blue"],
        image_size: Optional[Sequence] = None,
        pixel_size: Optional[Union[float, Sequence[float]]] = None,
        resample: str = "nearest",
        input_srs: str = "EPSG:4326",
        output_srs: str = "EPSG:3857",
    ):

        bands = lookup_bands(bands, self.dataset)
        mosaic = mosaic_bands(bands, self.item)

        width = height = None
        x_res = y_res = None

        if image_size is not None:
            height, width = image_size

        if pixel_size is not None:
            try:
                x_res, y_res = pixel_size
            except Exception:
                x_res = y_res = pixel_size

        if x_res is None:
            x_res = y_res = 30.0

        options = gdal.WarpOptions(
            format="GTiff",
            outputBounds=bbox,
            outputBoundsSRS=input_srs,
            resampleAlg=resample_lut.get(resample, gdal.GRA_NearestNeighbour),
            xRes=x_res,
            yRes=y_res,
            width=width,
            height=height,
            dstSRS=output_srs,
        )

        try:
            d = gdal.Warp("/vsimem/test.tiff", mosaic, options=options)
        except Exception:
            mosaic = None
            d = None
            return

        mosaic = None

        x = d.ReadAsArray()
        d = None

        return x


# TODO: Implement mosaic/time series functionality.
class RasterCollection:
    """
    For operations on a list of rasters (as Items)
    """

    def __init__(self, items: Sequence[Item], dataset=None) -> None:

        self.items = items

        first_item = next(iter(items))
        try:
            # Is a geodesic.features.Item
            dt = first_item.datetime
            if dt is None:
                self.static = True
            else:
                self.static = False
        except Exception:
            raise ValueError(
                "unable to check datetime attribute. Is this a `geodesic.Item`?"
            )

        self.dataset = dataset

    def export_rasters(
        self,
        bbox: Optional[Sequence] = None,
        bands: Sequence = ["red", "green", "blue"],
        image_size: Optional[Sequence] = None,
        pixel_size: Optional[Union[float, Sequence[float]]] = None,
        input_srs: str = "EPSG:4326",
        output_srs: str = "EPSG:3857",
        resample: str = "nearest",
        output_nodata: Union[int, float] = 0,
        output_dtype: Union[np.dtype, str] = np.float32,
        mosaic_threshold: timedelta = None,
        verbose=False,
        progress_func=tqdm,
    ):

        width = height = None
        x_res = y_res = None

        if image_size is not None:
            height, width = image_size

        if pixel_size is not None:
            try:
                x_res, y_res = pixel_size
            except Exception:
                x_res = y_res = pixel_size

        if x_res is None:
            x_res = y_res = 30.0

        bands = lookup_bands(bands, self.dataset)

        band_mosaics = [
            mosaic_bands(bands, item)
            for item in progress_func(self.items, desc="building band mosaics")
        ]
        timestamps = [item.datetime for item in self.items]
        ids = [item.id for item in self.items]
        times_mosaics_ids = list(zip(timestamps, band_mosaics, ids))

        # Mosaic iamges within a threshold of each other
        if not self.static and mosaic_threshold is not None:
            groups = []
            group = []
            last_timestamp = None

            for timestamp, band_mosaic, item_id in sorted(
                times_mosaics_ids, key=lambda x: x[0]
            ):

                if last_timestamp is None:
                    last_timestamp = timestamp
                if timestamp > (last_timestamp + mosaic_threshold):
                    groups.append(group)
                    group = [(band_mosaic, timestamp, item_id)]

                    last_timestamp = timestamp
                    continue

                group.append((band_mosaic, timestamp, item_id))
                last_timestamp = timestamp
            if len(group):
                groups.append(group)
        else:
            if self.static:
                groups = [
                    [
                        (band_mosaic, timestamp, item_id)
                        for timestamp, band_mosaic, item_id in sorted(
                            times_mosaics_ids, key=lambda x: 1
                        )
                    ]
                ]
            else:
                groups = [
                    [(band_mosaic, timestamp, item_id)]
                    for timestamp, band_mosaic, item_id in sorted(
                        times_mosaics_ids, key=lambda x: x[0]
                    )
                ]

        options = gdal.WarpOptions(
            format="GTiff",
            outputBounds=bbox,
            outputBoundsSRS=input_srs,
            resampleAlg=resample_lut.get(resample, gdal.GRA_NearestNeighbour),
            xRes=x_res,
            yRes=y_res,
            width=width,
            height=height,
            srcNodata=0,
            dstSRS=output_srs,
        )

        out_rasters = None

        datetimes = []

        for i, group in enumerate(progress_func(groups, desc="warping")):

            if len(group) == 1:
                mosaic = group[0][0]
            else:
                mosaic = [g[0] for g in group if g is not None]

            if not self.static:
                datetimes.append(group[0][1].isoformat())
            else:
                datetimes.append(None)

            if mosaic:

                warp = str(uuid.uuid4())

                try:
                    d = gdal.Warp(f"/vsimem/{warp}.tif", mosaic, options=options)
                except Exception:
                    d = None
                    mosaic = None
                    continue

                mosaic = None
                x = d.ReadAsArray()
                if x.ndim == 2:
                    x = np.expand_dims(x, 0)

                if out_rasters is None:
                    out_rasters = np.full(
                        (len(groups),) + x.shape, output_nodata, dtype=output_dtype
                    )

                out_rasters[i] = x

                d = None

        return out_rasters, np.array(datetimes)

    def export_rasters_gen(
        self,
        bbox: Optional[Sequence] = None,
        bands: Sequence = ["red", "green", "blue"],
        image_size: Optional[Sequence] = None,
        pixel_size: Optional[Union[float, Sequence[float]]] = None,
        input_srs: str = "EPSG:4326",
        output_srs: str = "EPSG:3857",
        resample: str = "nearest",
        output_nodata: Union[int, float] = 0,
        output_dtype: Union[np.dtype, str] = np.float32,
        mosaic_threshold: timedelta = None,
        verbose=False,
        progress_func=tqdm,
    ):

        width = height = None
        x_res = y_res = None

        if image_size is not None:
            height, width = image_size

        if pixel_size is not None:
            try:
                x_res, y_res = pixel_size
            except Exception:
                x_res = y_res = pixel_size

        if x_res is None:
            x_res = y_res = 30.0

        bands = lookup_bands(bands, self.dataset)

        band_mosaics = [
            mosaic_bands(bands, item)
            for item in progress_func(self.items, desc="building band mosaics")
        ]
        timestamps = [item.datetime for item in self.items]
        ids = [item.id for item in self.items]
        times_mosaics_ids = list(zip(timestamps, band_mosaics, ids))

        # Mosaic iamges within a threshold of each other
        if not self.static and mosaic_threshold is not None:
            groups = []
            group = []
            last_timestamp = None

            for timestamp, band_mosaic, item_id in sorted(
                times_mosaics_ids, key=lambda x: x[0]
            ):

                if last_timestamp is None:
                    last_timestamp = timestamp
                if timestamp > (last_timestamp + mosaic_threshold):
                    groups.append(group)
                    group = [(band_mosaic, timestamp, item_id)]

                    last_timestamp = timestamp
                    continue

                group.append((band_mosaic, timestamp, item_id))
                last_timestamp = timestamp
            if len(group):
                groups.append(group)
        else:
            if self.static:
                groups = [
                    [
                        (band_mosaic, timestamp, item_id)
                        for timestamp, band_mosaic, item_id in sorted(
                            times_mosaics_ids, key=lambda x: 1
                        )
                    ]
                ]
            else:
                groups = [
                    [(band_mosaic, timestamp, item_id)]
                    for timestamp, band_mosaic, item_id in sorted(
                        times_mosaics_ids, key=lambda x: x[0]
                    )
                ]

        options = gdal.WarpOptions(
            format="GTiff",
            outputBounds=bbox,
            outputBoundsSRS=input_srs,
            resampleAlg=resample_lut.get(resample, gdal.GRA_NearestNeighbour),
            xRes=x_res,
            yRes=y_res,
            width=width,
            height=height,
            srcNodata=0,
            dstSRS=output_srs,
        )

        for i, group in enumerate(progress_func(groups, desc="warping")):

            if len(group) == 1:
                mosaic = group[0][0]
            else:
                mosaic = [g[0] for g in group if g is not None]

            if not self.static:
                dt = group[0][1].isoformat()
            else:
                dt = None

            if mosaic:

                warp = str(uuid.uuid4())
                vsimem_path = f"/vsimem/{warp}.tif"

                try:
                    d = gdal.Warp(vsimem_path, mosaic, options=options)
                except Exception:
                    try:
                        gdal.Unlink(vsimem_path)
                    except Exception:
                        pass
                    d = None
                    mosaic = None
                    continue

                mosaic = None

                x = d.ReadAsArray()
                if x.ndim == 2:
                    x = np.expand_dims(x, 0)

                x = x.astype(output_dtype)
                try:
                    gdal.Unlink(vsimem_path)
                except Exception as e:
                    print(f"failed Unlink: {e}")
                d = None
            else:
                x = None

            yield i, len(groups), x, dt


def lookup_bands(bands: Sequence[str], dataset: Dataset):
    if dataset is not None:
        extensions = dataset.stac.get("extensions", [])
        assets = dataset.stac.get("itemAssets", {})
    else:
        assets = {}
        extensions = []

    has_eo_ext = "eo" in extensions
    has_item_assets_ext = "item-assets" in extensions

    band_keys = []
    for band in bands:
        # Check in the item assets for a commonName for the band
        if has_eo_ext and has_item_assets_ext:
            for ia, a in assets.items():
                eo = a.get("eo", {})
                for b in eo.get("bands", []):
                    if b.get("commonName") == band:
                        band = ia
                        break

        band_keys.append(band)
    return band_keys


def mosaic_bands(bands: Sequence[str], item: Item):

    band_files = []
    for band in bands:
        if band not in item.assets:
            assets = ",".join([k for k in item.assets])
            raise ValueError(
                "band '{0}' does not exist for this item. Available assets are: {1}".format(
                    band, assets
                )
            )

        asset = item.assets[band]

        band_files.append(format_uri(asset.href))

    vrt_uuid = str(uuid.uuid4())

    options = gdal.BuildVRTOptions(separate=True)

    vrt = gdal.BuildVRT(f"/vsimem/{vrt_uuid}.vrt", band_files, options=options)

    return vrt


def format_uri(uri):
    m = gs_re.match(uri)

    if m:
        bucket = m.group(1)
        key = m.group(2)

        return f"/vsigs/{bucket}/{key}"

    m = s3_re.match(uri)

    if m:
        bucket = m.group(1)
        key = m.group(2)

        return f"/vsis3/{bucket}/{key}"

    if (
        uri.startswith("http://")
        or uri.startswith("https://")
        or uri.startswith("ftp://")
    ):
        return "/vsicurl/" + uri

    return uri


class BandCombination:
    """
    Creates a band combination
    """
