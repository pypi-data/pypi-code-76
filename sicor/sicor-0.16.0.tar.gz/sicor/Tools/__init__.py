import platform

from .Tools import write_raster_gdal
from .Tools import read_image_gdal
from .Tools import fl
from .Tools import cl
from .Tools import get_data_file

from .inpaint import inpaint
from .inpaint import fill_nan
from .inpaint import itt2d
from .inpaint import nanmean_filter

from .sharedndarray import initializer, SharedNdarray
from .SolarIrradiance import SolarIrradiance
from .rsf_functions import box_rspf, gauss_rspf
from .tqdm_joblist import tqdm_joblist
from .get_memory_use import get_memory_use

from .majority_mask_filter import majority_mask_filter
from .linear_error_moddeling import linear_error_modeling

if platform.system() == "Linux":
    from .ram import RAM


__author__ = "Niklas Bohn, Andre Hollstein"
__all__ = ["write_raster_gdal", "fl", "cl", "inpaint", "fill_nan", "itt2d", "nanmean_filter", "RAM",
           "initializer", "SharedNdarray", "SolarIrradiance", "box_rspf", "gauss_rspf",
           "tqdm_joblist", "get_memory_use", "majority_mask_filter", "linear_error_modeling",
           "get_data_file", "read_image_gdal"]
