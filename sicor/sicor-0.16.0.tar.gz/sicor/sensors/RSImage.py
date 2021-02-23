import logging
import numpy as np
from numbers import Number


class RSImage(object):
    """
    Remote Sensing Image base class.

    :param unit: string "reflectance", in future other units might be supported
    :param target_resolution: None: keep data as is (e.g. separate bands), or give spatial sampling for
                              interpolation to larger cube
    :param bad_data_value: vale to exclude data from processing
    :param dtype_float: dtype for intermediate computations
    :param *kwargs: See below

    :Keyword Arguments:
        * *data*: {B10:ndarray(dtype=float16),[...],B09:ndarray(dtype=float16)}
        * *tile_name*: "32UMA"
        * *nodata* (and or yesdata with same interface){60.0:ndarray(dtype=bool),[...],20.0:ndarray(dtype=bool)}
        * *band_spatial_sampling*: {B10:60.0,[...],B02:10.0,[...],B11:20.0}
        * *mask_clouds*: should be instance of S2MSI.Mask or similar object, some attributes need to be
            present: ['clf_to_col', 'export_confidence_to_jpeg2000', 'export_mask_blend', 'export_mask_rgb',
            'export_to_jpeg200', 'geo_coding', 'mask_array', 'mask_confidence_array', 'mask_legend',
            'mask_legend_inv', 'mask_rgb_array', 'metadata', 'mk_mask_at_spatial_scales']
        * *metadata*:

        .. code-block:: python

            {"U":1.0,# Eun - Earth distance
             "SENSING_TIME":2015-08-12 10:40:21.459000+00:00,
             "viewing_zenith":{B10:ndarray(dtype=float16),[...],B09:ndarray(dtype=float16)},
             "viewing_azimut":{B10:ndarray(dtype=float16),[...],B09:ndarray(dtype=float16)},
             "sun_mean_azimuth":161.57,
             "sun_mean_zenith":36.21,
             "solar_irradiance:{B10:367.15,[...],B09:813.04},
             "aux_data":{},
             "spatial_samplings":{
                    60.0:{
                    XDIM:60,
                    NCOLS:1830,
                    NROWS:1830,
                    YDIM:-60,
                    ULX:399960,
                    ULY:5600040
                    },
                    10.0:{
                    XDIM:10,
                    NCOLS:10980,
                    NROWS:10980,
                    YDIM:-10,
                    ULX:399960,
                    ULY:5600040
                    },
                    20.0:{
                    XDIM:20,
                    NCOLS:5490,
                    NROWS:5490,
                    YDIM:-20,
                    ULX:399960,
                    ULY:5600040
                    }}
    """

    def __init__(self, unit="reflectance", target_resolution=None, bad_data_value=np.NaN, dtype_float=np.float16,
                 mask_clouds=None, **kwargs):

        all_kwargs = arguments()["kwargs"]
        self.dtype_float = dtype_float
        self.bad_data_value = bad_data_value
        self.unit = unit
        self.target_resolution = target_resolution
        self.metadata = {}
        self.data = {}
        self.final_shape = None
        self.logger = logging.getLogger()

        for key, value in all_kwargs.items():
            if key not in ["mask_clouds"]:  # special treatment attributes here
                self.__setattr__(key, value)
        # individually treated attributes here
        if mask_clouds is not None:
            assert self.__is_mask__(mask_clouds)
            self.mask_clouds = mask_clouds

        if "band_list" not in all_kwargs.keys():
            if hasattr(self, "data"):
                self.band_list = list(self.data.keys())
            else:
                self.band_list = None
        if "nodata" not in all_kwargs.keys() and "yesdata" in all_kwargs.keys():
            self.nodata = {ss: np.invert(ar) for ss, ar in self.yesdata.items()}
        if "yesdata" not in all_kwargs.keys() and "nodata" in all_kwargs.keys():
            self.yesdata = {ss: np.invert(ar) for ss, ar in self.nodata.items()}

        self.spatial_sampling_shapes = {ss: (vv["NROWS"], vv["NCOLS"]) for ss, vv in
                                        self.metadata["spatial_samplings"].items()}
        self._validate()

    @staticmethod
    def __is_mask__(msk):
        needed_attributes = [
            'clf_to_col', 'export_confidence_to_jpeg2000', 'export_mask_blend', 'export_mask_rgb', 'export_to_jpeg200',
            'geo_coding', 'mask_array', 'mask_confidence_array', 'mask_legend', 'mask_legend_inv', 'mask_rgb_array',
            'metadata', 'mk_mask_at_spatial_scales'
        ]
        present_attributes = dir(msk)
        for at in needed_attributes:
            if at not in present_attributes:
                return False
        return True

    def _validate(self):
        for method in ['image_to_rgb', 'image_subsample', 'ecmwf_xi']:
            assert method in dir(self)

        assert "metadata" in dir(self)
        for md in ['spatial_samplings', 'SENSING_TIME', "aux_data", "sun_mean_zenith", 'viewing_zenith',
                   'sun_mean_azimuth', 'viewing_azimuth']:
            assert md in self.metadata, "%s missing in metadata" % md

        for at in ["data", "target_resolution", "nodata", "tile_name", "unit", 'bad_data_value',
                   'yesdata', 'band_list', "band_spatial_sampling"]:
            assert at in dir(self), "%s missing in attributes" % at

    def ecmwf_xi(self):
        return {
            "step": self.metadata['SENSING_TIME'].hour + self.metadata['SENSING_TIME'].minute / 60.,
            "lats": self.metadata['aux_data']["lats"],  # -90° - 90°
            "lons": (360 + self.metadata['aux_data']["lons"]) % 360,  # 0° - 380°
            "order": 3
        }

    def image_subsample(self, channels, target_resolution, order=3):
        """

        :param channels: list of strings with channel names
        :param target_resolution: float
        :param order: interpolation order, integer
        :return: data as desired
        """
        from scipy.ndimage import zoom  # import here to avoid static TLS ImportError

        assert self.target_resolution is None

        if target_resolution is None:
            shape = list(self.data[channels[0]].shape)
        else:
            shape = [self.metadata["spatial_samplings"][target_resolution][ii] for ii in ["NCOLS", "NROWS"]]
        shape.append(len(channels))

        dtype_internal = np.float32
        data = np.zeros(shape, dtype=dtype_internal)
        for ich, ch in enumerate(channels):
            zoom_fac = [shape[0] / self.data[ch].shape[0],
                        shape[1] / self.data[ch].shape[1]
                        ]

            bf = np.array(self.data[ch], dtype=dtype_internal)
            bf_nan = np.isnan(bf)
            bf[bf_nan] = 0.0
            data[:, :, ich] = zoom(input=bf, zoom=zoom_fac, order=order)
            bf_nan = zoom(input=np.array(bf_nan, dtype=np.float32), zoom=zoom_fac, order=0)
            data[:, :, ich][bf_nan > 0.0] = np.NaN

        return np.array(data, dtype=self.dtype_float)

    def image_to_rgb(self, rgb_bands=("B11", "B08", "B03"), rgb_gamma=(1.0, 1.0, 1.0), hist_chop_off_fraction=0.01,
                     output_size=None, max_hist_pixel=1000 ** 2, resample_order=3):
        # importing skimage and scipy here avoids ImportError: dlopen: cannot load any more object with static TLS
        from skimage.exposure import rescale_intensity, adjust_gamma
        from scipy.ndimage import zoom

        if output_size is None:
            if self.target_resolution is None:
                raise ValueError("output_size=None is only allowed for target_resolution != None")
            else:
                output_shape = list(self.final_shape)
        else:
            output_shape = [output_size, output_size]

        rgb_type = np.uint8
        rgb = np.zeros(output_shape + [len(rgb_bands), ], dtype=rgb_type)

        if self.unit == "reflectance":
            bins = np.linspace(0.0, 1.0, 50)
        elif self.unit == "dn":
            bins = np.linspace(0, 10000, 50)

        for i_rgb, (band, gamma) in enumerate(zip(rgb_bands, rgb_gamma)):
            if self.target_resolution is None:
                data = self.data[band]
            else:
                i_band = self.band_list.index(band)
                data = self.data[:, :, i_band]

            if self.bad_data_value is np.NAN:
                bf = data[:, :][np.isfinite(data[:, :])]
            else:
                bf = data[:, :][data[:, :] == self.bad_data_value]

            pixel_skip = int(np.floor(bf.shape[0] / max_hist_pixel) + 1)
            bf = bf[::pixel_skip]
            hh, xx = np.histogram(bf, bins=bins)
            bb = 0.5 * (xx[1:] + xx[:-1])
            hist_chop_off = hist_chop_off_fraction * np.sum(hh) / len(bins)
            try:
                lim = (lambda x: (np.min(x), np.max(x)))(bb[hh > hist_chop_off])
            except ValueError:
                # e.g. when bb[hh > hist_chop_off] = [] -> fallback to sensible default
                lim = (0.0, 1.0)
            zoom_factor = np.array(output_shape) / np.array(data[:, :].shape)

            zm = np.nan_to_num(np.array(data[:, :], dtype=np.float32))
            if (zoom_factor != [1.0, 1.0]).all():
                self.logger.info("Resample band for RGB image: %i,%s,zoom:%.2f" % (i_rgb, band, zoom_factor[0]))
                zm = zoom(input=zm, zoom=zoom_factor, order=resample_order)

            bf = rescale_intensity(image=zm, in_range=lim, out_range=(0.0, 255.0))
            rgb[:, :, i_rgb] = np.array(bf, dtype=rgb_type)

            self.logger.info("Rescale band for RGB image: %i,%s,(%.2f,%.2f)->(0,256), zoom:%.2f" %
                             (i_rgb, band, lim[0], lim[1], zoom_factor[0]))

            if gamma != 0.0:
                rgb[:, :, i_rgb] = np.array(
                    adjust_gamma(np.array(rgb[:, :, i_rgb], dtype=np.float32), gamma), dtype=rgb_type)
        return rgb


# noinspection PyDefaultArgument
def arguments(ignore=["logger"]):
    """Returns tuple containing dictionary of calling function's
       named arguments and a list of calling function's unnamed
       positional arguments.
    """
    from inspect import getargvalues, stack
    posname, kwname, kwargs = getargvalues(stack()[1][0])[-3:]
    args = kwargs.pop(posname, [])
    kwargs.update(kwargs.pop(kwname, []))
    return {"args": args, "kwargs": {k: v for k, v in kwargs.items() if k not in ignore}}


class const_snr_model():
    """SNR model with constant snr."""
    def __init__(self, snr: Number):
        """SNR of instrument. """
        self.snr = float(snr)

    def noise(self, reflectance, **kwargs):
        """Error, simply computed from SNR."""
        return reflectance / self.snr
