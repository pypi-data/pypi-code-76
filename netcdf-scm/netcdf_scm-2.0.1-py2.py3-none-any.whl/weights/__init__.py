"""
Module which calculates the weights to be used when taking SCM-box averages

This typically requires considering both the fraction of each cell which is of the desired type (e.g. land or ocean) and the area of each cell. The combination of these two pieces of information creates the weights for each cell which are used when taking area-weighted means.
"""
import logging
import os
from abc import ABC, abstractmethod
from functools import lru_cache

import numpy as np
from packaging import version

from ..utils import cube_lat_lon_grid_compatible_with_array

try:
    import iris
    from iris.analysis.cartography import wrap_lons
except ModuleNotFoundError:  # pragma: no cover # emergency valve
    from ..errors import raise_no_iris_warning

    raise_no_iris_warning()

try:
    import regionmask
    import xarray as xr

    if version.parse(regionmask.__version__) >= version.parse("0.6"):
        has_regionmask = True
    else:
        has_regionmask = False
except ImportError:
    has_regionmask = False


logger = logging.getLogger(__name__)

_DEFAULT_SFTLF_FILE = "default_land_ocean_weights.nc"
DEFAULT_REGIONS = (
    "World",
    "World|Land",
    "World|Ocean",
    "World|Northern Hemisphere",
    "World|Southern Hemisphere",
    "World|Northern Hemisphere|Land",
    "World|Southern Hemisphere|Land",
    "World|Northern Hemisphere|Ocean",
    "World|Southern Hemisphere|Ocean",
)


class InvalidWeightsError(Exception):
    """
    Raised when a weight cannot be calculated.

    This error usually propogates. For example, if a child weight used in the
    calculation of a parent weight fails then the parent weight should also raise an
    InvalidWeightsError exception (unless it can be satisfactorily handled).
    """


def subtract_weights(weights_to_subtract, subtract_from):
    """
    Subtract weights from some other number

    e.g. useful to convert e.g. from fraction of land to ocean (where
    ocean fractions are 1 - land fractions)

    Parameters
    ----------
    weights_to_subtract: str
        Name of the weights to subtract. These weights are loaded at evaluation time.

    subtract_from : float
        The number from which to subtract the values of ``weights_to_invert`` (once
        loaded)

    Returns
    -------
    :func:`WeightFunc`
        WeightFunc which subtracts the input weights from ``subtract_from``
    """

    def f(weight_calculator, cube, **kwargs):  # pylint:disable=unused-argument
        base = (
            weights_to_subtract(weight_calculator, cube, **kwargs)
            if callable(weights_to_subtract)
            else weight_calculator.get_weights_array_without_area_weighting(
                weights_to_subtract
            )
        )

        return subtract_from - base

    return f


def multiply_weights(weight_a, weight_b):
    """
    Take the product of two weights

    Parameters
    ----------
    weight_a : str or WeightFunc
        If a string is provided, the weights specified by the string are retrieved.
        Otherwise the WeightFunc is evaluated at runtime

    weight_b: str or WeightFunc
        If a string is provided, the weights specified by the string are retrieved.
        Otherwise the WeightFunc is evaluated at runtime

    Returns
    -------
    :func:`WeightFunc`
        WeightFunc which multiplies the input weights
    """

    def f(weight_calculator, cube, **kwargs):
        a = (
            weight_a(weight_calculator, cube, **kwargs)
            if callable(weight_a)
            else weight_calculator.get_weights_array_without_area_weighting(weight_a)
        )
        b = (
            weight_b(weight_calculator, cube, **kwargs)
            if callable(weight_b)
            else weight_calculator.get_weights_array_without_area_weighting(weight_b)
        )
        return a * b

    return f


@lru_cache(maxsize=1)
def get_default_sftlf_cube():
    """Load netCDF-SCM's default (last resort) surface land fraction cube"""
    return iris.load_cube(os.path.join(os.path.dirname(__file__), _DEFAULT_SFTLF_FILE))


def _check_surface_fraction_bounds_and_shape(surface_frac_data, base_cube):
    surface_frac_data_max = surface_frac_data.max()
    if not np.isclose(surface_frac_data_max, 1, atol=0.1):
        logger.debug(
            "%s data max is %s, dividing by %s to convert units to fraction",
            base_cube.surface_fraction_var,
            surface_frac_data_max,
            surface_frac_data_max,
        )
        surface_frac_data = surface_frac_data / surface_frac_data_max

    if not cube_lat_lon_grid_compatible_with_array(base_cube, surface_frac_data):
        raise AssertionError(
            "the {} cube data must be the same shape as the cube's "
            "longitude-latitude grid".format(base_cube.surface_fraction_var)
        )

    return surface_frac_data


def get_land_weights(  # pylint:disable=unused-argument
    weight_calculator, cube, sftlf_cube=None, **kwargs
):
    """
    Get the land weights

    The weights are always adjusted to have units of percentage. If the units are
    detected to be fraction rather than percentage, they will be automatically
    adjusted and a warning will be thrown.

    If the default sftlf cube is used, it is regridded onto ``cube``'s grid using a
    linear interpolation. We hope to use an area-weighted regridding in future but at
    the moment its performance is not good enough to be put into production (
    approximately 100x slower than the linear interpolation regridding).

    Parameters
    ----------
    weight_calculator : :obj:`CubeWeightCalculator`
        Cube weight calculator from which to retrieve the weights

    cube : :obj:`ScmCube`
        Cube to create weights for

    sftlf_cube : :obj:`ScmCube`
        Cube containing the surface land-fraction data

    kwargs : Any
        Ignored (required for compatibility with ``CubeWeightCalculator``)

    Returns
    -------
    np.ndarray
        Land weights

    Raises
    ------
    AssertionError
        The land weights are incompatible with the cube's lat-lon grid
    """

    def _return_and_set_cache(vals):
        weight_calculator._weights_no_area_weighting[  # pylint:disable=protected-access
            "World|Land"
        ] = vals
        return vals

    if cube.netcdf_scm_realm == "ocean":
        return _return_and_set_cache(
            np.zeros(get_binary_nh_weights(weight_calculator, cube).shape)
        )

    sftlf_data = None
    try:
        sftlf_cube = cube.get_metadata_cube(cube.surface_fraction_var, cube=sftlf_cube)
        sftlf_data = sftlf_cube.cube.data
    except (OSError, KeyError):  # TODO: fix reading so KeyError not needed
        warn_msg = (
            "Land surface fraction (sftlf) data not available, using default instead"
        )
        logger.warning(warn_msg)
        try:
            def_cube_regridded = (
                get_default_sftlf_cube()
                .copy()
                .regrid(
                    cube.cube,
                    iris.analysis.Linear(),  # AreaWeighted() in future but too slow now
                )
            )
        except ValueError:  # pragma: no cover # only required for AreaWeighted() regridding
            logger.warning("Guessing bounds to regrid default sftlf data")
            cube.lat_dim.guess_bounds()
            cube.lon_dim.guess_bounds()
            def_cube_regridded = (
                get_default_sftlf_cube()
                .copy()
                .regrid(
                    cube.cube,
                    iris.analysis.Linear(),  # AreaWeighted() in future but too slow now
                )
            )

        sftlf_data = def_cube_regridded.data

    sftlf_data = _check_surface_fraction_bounds_and_shape(sftlf_data, cube)

    return _return_and_set_cache(sftlf_data)


def get_ocean_weights(  # pylint:disable=unused-argument
    weight_calculator, cube, sftof_cube=None, **kwargs
):
    """
    Get the ocean weights

    The weights are always adjusted to have units of percentage.

    Parameters
    ----------
    weight_calculator : :obj:`CubeWeightCalculator`
        Cube weight calculator from which to retrieve the weights

    cube : :obj:`ScmCube`
        Cube to create weights for

    sftof_cube : :obj:`ScmCube`
        Cube containing the surface ocean-fraction data

    kwargs : Any
        Ignored (required for compatibility with ``CubeWeightCalculator``)

    Returns
    -------
    np.ndarray
        Ocean weights

    Raises
    ------
    AssertionError
        The ocean weights are incompatible with the cube's lat-lon grid
    """

    def _return_and_set_cache(vals):
        weight_calculator._weights_no_area_weighting[  # pylint:disable=protected-access
            "World|Ocean"
        ] = vals
        return vals

    if cube.netcdf_scm_realm == "land":
        return _return_and_set_cache(
            0 * np.ones(get_binary_nh_weights(weight_calculator, cube).shape)
        )

    if cube.netcdf_scm_realm == "ocean":
        try:
            sftof_cube = cube.get_metadata_cube(
                cube.surface_fraction_var, cube=sftof_cube
            )
            sftof_data = sftof_cube.cube.data
            sftof_data = _check_surface_fraction_bounds_and_shape(sftof_data, cube)

            return _return_and_set_cache(sftof_data)

        except (OSError, KeyError):  # TODO: fix reading so KeyError not needed
            pass

    return _return_and_set_cache(
        1 - weight_calculator.get_weights_array_without_area_weighting("World|Land")
    )


def get_binary_nh_weights(
    weight_calculator, cube, **kwargs
):  # pylint:disable=unused-argument
    """
    Get binary weights to only include the Northern Hemisphere

    Parameters
    ----------
    weight_calculator : :obj:`CubeWeightCalculator`
        Cube weight calculator from which to retrieve the weights

    cube : :obj:`ScmCube`
        Cube to create weights for

    kwargs : Any
        Ignored (required for compatibility with ``CubeWeightCalculator``)

    Returns
    -------
    :obj:`np.ndarray`
        Binary northern hemisphere weights
    """
    weights_nh_lat = np.array([c >= 0 for c in cube.lat_dim.points]).astype(int)
    weights_all_lon = np.ones(cube.lon_dim.points.shape)

    if len(weights_nh_lat.shape) > 1:
        weights_nh = weights_nh_lat * weights_all_lon
    else:
        weights_nh = np.outer(weights_nh_lat, weights_all_lon)

    return weights_nh


def get_nh_weights(weight_calculator, cube, **kwargs):  # pylint:disable=unused-argument
    """
    Get weights to only include the Northern Hemisphere

    Parameters
    ----------
    weight_calculator : :obj:`CubeWeightCalculator`
        Cube weight calculator from which to retrieve the weights

    cube : :obj:`ScmCube`
        Cube to create weights for

    kwargs : Any
        Ignored (required for compatibility with ``CubeWeightCalculator``)

    Returns
    -------
    :obj:`np.ndarray`
        Northern hemisphere weights
    """
    weights_nh = get_binary_nh_weights(weight_calculator, cube, **kwargs)

    if cube.netcdf_scm_realm == "land":
        weights_nh = (
            weights_nh
            * weight_calculator.get_weights_array_without_area_weighting("World|Land")
        )

    elif cube.netcdf_scm_realm == "ocean":
        weights_nh = (
            weights_nh
            * weight_calculator.get_weights_array_without_area_weighting("World|Ocean")
        )

    weight_calculator._weights_no_area_weighting[  # pylint:disable=protected-access
        "World|Northern Hemisphere"
    ] = weights_nh

    return weights_nh


def get_sh_weights(weight_calculator, cube, **kwargs):  # pylint:disable=unused-argument
    """
    Get weights to only include the Southern Hemisphere

    Parameters
    ----------
    weight_calculator : :obj:`CubeWeightCalculator`
        Cube weight calculator from which to retrieve the weights

    cube : :obj:`ScmCube`
        Cube to create weights for

    kwargs : Any
        Ignored (required for compatibility with ``CubeWeightCalculator``)

    Returns
    -------
    :obj:`np.ndarray`
        Southern hemisphere weights
    """
    weights_sh = 1 - get_binary_nh_weights(weight_calculator, cube, **kwargs)

    if cube.netcdf_scm_realm == "land":
        weights_sh = (
            weights_sh
            * weight_calculator.get_weights_array_without_area_weighting("World|Land")
        )

    elif cube.netcdf_scm_realm == "ocean":
        weights_sh = (
            weights_sh
            * weight_calculator.get_weights_array_without_area_weighting("World|Ocean")
        )

    weight_calculator._weights_no_area_weighting[  # pylint:disable=protected-access
        "World|Southern Hemisphere"
    ] = weights_sh

    return weights_sh


def get_weights_for_area(lower_lat, left_lon, upper_lat, right_lon):
    """
    Weights a subset of the globe using latitudes and longitudes (in degrees East)

    Iris' standard behaviour is to include any point whose bounds overlap with
    the given ranges e.g. if the range is (0, 130) then a cell whose bounds were
    (-90, 5) would be included even if its point were -42.5.

    This can be altered with the ``ignore_bounds`` keyword argument to
    ``cube.intersection``. In this case only cells whose points lie within the
    range are included so if the range is (0, 130) then a cell whose bounds were
    (-90, 5) would be excluded if its point were -42.5.

    Here we follow the ``ignore_bounds=True`` behaviour (i.e. only include if
    the point lies within the specified range). If we want to only include the
    cell if the entire box is within a point we're going to need to tweak things.
    Given this isn't available in iris, it seems to be an unusual way to do
    intersection so we haven't implemented it.

    Circular coordinates (longitude) can cross the 0E.

    Parameters
    ----------
    lower_lat : int or float
        Lower latitude bound (degrees North)

    left_lon : int or float
        Lower longitude bound (degrees East)

    upper_lat : int or float
        Upper latitude bound (degrees North)

    right_lon : int or float
        Upper longitude bound (degrees East)

    Returns
    -------
    :func:`WeightFunc`
        WeightFunc which weights out everything except the specified area
    """

    def f(weight_calculator, cube, **kwargs):  # pylint:disable=unused-argument
        lon_dim_pts = cube.lon_dim.points
        lat_dim_pts = cube.lat_dim.points

        lat_lon_size = cube.lat_lon_shape

        if len(lat_dim_pts.shape) == 1:
            lat_dim_pts = np.broadcast_to(lat_dim_pts, lat_lon_size[::-1]).T
        if len(lon_dim_pts.shape) == 1:
            lon_dim_pts = np.broadcast_to(lon_dim_pts, lat_lon_size)

        weights_lat = ((lower_lat <= lat_dim_pts) & (lat_dim_pts <= upper_lat)).astype(
            int
        )

        lon_modulus = cube.lon_dim.units.modulus
        lon_min = np.floor(lon_dim_pts.min())
        left_lon_wrapped, right_lon_wrapped = wrap_lons(
            np.array([left_lon, right_lon]), lon_min, lon_modulus
        ).astype(int)
        if left_lon_wrapped <= right_lon_wrapped:
            weights_lon = (left_lon_wrapped <= lon_dim_pts) & (
                lon_dim_pts <= right_lon_wrapped
            )
        else:
            weights_lon = (
                (lon_min <= lon_dim_pts) & (lon_dim_pts <= right_lon_wrapped)
            ) | (
                (left_lon_wrapped <= lon_dim_pts)
                & (lon_dim_pts <= lon_min + lon_modulus)
            )

        weights_lon = weights_lon.astype(int)

        # TODO: make issue in Iris about the fact that ``cube.intersection``'s errors
        # are cryptic
        error_msg = "None of the cube's {} lie within the bounds:\nquery: ({}, {})\ncube points: {}"
        if np.equal(np.sum(weights_lon), 0):
            raise InvalidWeightsError(
                error_msg.format("latitudes", lower_lat, upper_lat, cube.lat_dim.points)
            )

        if np.equal(np.sum(weights_lat), 0):
            raise InvalidWeightsError(
                error_msg.format("longitudes", left_lon, right_lon, cube.lon_dim.points)
            )

        weights = weights_lon * weights_lat
        return weights

    return f


def get_world_weights(
    weight_calculator, cube, **kwargs
):  # pylint:disable=unused-argument
    """
    Get weights for the world

    Parameters
    ----------
    weight_calculator : :obj:`CubeWeightCalculator`
        Cube weight calculator from which to retrieve the weights

    cube : :obj:`ScmCube`
        Cube to create weights for

    kwargs : Any
        Ignored (required for compatibility with ``CubeWeightCalculator``)

    Returns
    -------
    :obj:`np.ndarray`
        Weights which can be used for the world mean calculation
    """
    if cube.netcdf_scm_realm == "land":
        return weight_calculator.get_weights_array_without_area_weighting("World|Land")

    if cube.netcdf_scm_realm == "ocean":
        return weight_calculator.get_weights_array_without_area_weighting("World|Ocean")

    return np.ones(
        weight_calculator.get_weights_array_without_area_weighting(
            "World|Northern Hemisphere"
        ).shape
    )


def get_ar6_region_weights(region):
    """
    Get a function to calculate the weights for a given AR6 region

    AR6 regions defined in Iturbide et al., 2020
    https://essd.copernicus.org/preprints/essd-2019-258/

    Parameters
    ----------
    region : str
        AR6 region to extract
    Returns
    -------
    :func:`WeightFunc`
        WeightFunc which weights out everything except the specified area
    """

    def _calculate_region_weights(weight_calculator, cube, **kwargs):
        if cube.netcdf_scm_realm == "land":
            weights = weight_calculator.get_weights_array_without_area_weighting(
                "World|Land"
            )
        elif cube.netcdf_scm_realm == "ocean":
            weights = weight_calculator.get_weights_array_without_area_weighting(
                "World|Ocean"
            )
        else:
            weights = weight_calculator.get_weights_array_without_area_weighting(
                "World"
            )

        region_mask = regionmask.defined_regions.ar6.all[[region]]

        tdat_xr = xr.DataArray.from_iris(cube.cube)
        mask = region_mask.mask_3D(tdat_xr)

        weights_xr = xr.DataArray(
            weights,
            coords=[
                cube.cube.coord("latitude").points,
                cube.cube.coord("longitude").points,
            ],
            dims=["lat", "lon"],
        )
        weights = weights_xr.where(mask[0]).values
        weights[np.isnan(weights)] = 0
        return weights

    return _calculate_region_weights


"""dict: in-built functions to calculate weights for different regions without area weighting"""
WEIGHTS_FUNCTIONS_WITHOUT_AREA_WEIGHTING = {
    "World": get_world_weights,
    "World|Northern Hemisphere": get_nh_weights,
    "World|Southern Hemisphere": get_sh_weights,
    "World|Land": get_land_weights,
    "World|Ocean": get_ocean_weights,
    "World|Northern Hemisphere|Land": multiply_weights(
        get_binary_nh_weights, "World|Land"
    ),
    "World|Southern Hemisphere|Land": multiply_weights(
        subtract_weights(get_binary_nh_weights, 1), "World|Land"
    ),
    "World|Northern Hemisphere|Ocean": multiply_weights(
        get_binary_nh_weights, "World|Ocean"
    ),
    "World|Southern Hemisphere|Ocean": multiply_weights(
        subtract_weights(get_binary_nh_weights, 1), "World|Ocean"
    ),
    "World|North Atlantic Ocean": multiply_weights(
        get_weights_for_area(0, -80, 65, 0), "World|Ocean"
    ),
    # 5N-5S, 170W-120W (i.e. 190E to 240E) see
    # https://climatedataguide.ucar.edu/climate-data/nino-sst-indices-nino-12-3-34-4-oni-and-tni
    "World|El Nino N3.4": multiply_weights(
        get_weights_for_area(-5, 190, 5, 240), "World|Ocean"
    ),
}

if has_regionmask:
    for ar6_region_abbrev in regionmask.defined_regions.ar6.all.abbrevs:
        region_name = "World|AR6|{}".format(ar6_region_abbrev)
        WEIGHTS_FUNCTIONS_WITHOUT_AREA_WEIGHTING[region_name] = get_ar6_region_weights(
            ar6_region_abbrev
        )


class CubeWeightCalculator(ABC):
    """
    Computes weights for a given cube in a somewhat efficient manner.

    Previously calculated weights are cached so each set of weights is only calculated
    once. This implementation trades off some additional memory overhead for the
    ability to generate arbitary weights.

    **Adding new weights**

    Additional weights can be added to ``netcdf_scm.weights.weights``. The values in
    ``weights`` should be WeightFunc's. A WeightFunc is a function which takes a
    ScmCube, CubeWeightCalculator and any additional keyword arguments. The function
    should return a numpy array with the same dimensionality as the ScmCube.

    These WeightFunc's can be composed together to create more complex functionality
    using e.g. ``multiply_weights``.
    """

    def __init__(self, cube, **kwargs):
        """
        Initialise

        Parameters
        ----------
        cube : :obj:`ScmCube`
            cube to generate weights for

        kwargs : dict
            Any optional arguments to be passed to the WeightFunc's during evaluation.
            Possible parameters include:

                sftlf_cube : ScmCube
        """
        self.cube = cube
        self._weights_no_area_weighting = {}
        self._weights = {}
        self._area_weights = None
        self.kwargs = kwargs

    def get_weights_array_without_area_weighting(self, weights_name):
        """
        Get a single normalised weights array without any consideration of area weighting

        The weights are normalised to be in the range [0, 1]

        Parameters
        ----------
        weights_name : str
            Region to get weights for

        Returns
        -------
        np.ndarray
            Weights, normalised to be in the range [0, 1]

        Raises
        ------
        InvalidWeightsError
            If the requested weights cannot be found or evaluated

        ValueError
            The retrieved weights are not normalised to the range [0, 1]
        """
        try:
            return self._weights_no_area_weighting[weights_name]
        except KeyError:
            try:
                if weights_name.startswith("World|AR6|") and not has_regionmask:
                    raise InvalidWeightsError(
                        "regionmask>=0.6 is not installed. Run `pip install regionmask>=0.6`"
                    )

                weights_func = WEIGHTS_FUNCTIONS_WITHOUT_AREA_WEIGHTING[weights_name]
                weights = weights_func(self, self.cube, **self.kwargs)

                # check weights are sensible with some allowance for rounding errors
                if np.logical_or(
                    weights < -(10 ** 8), weights > 1 + 10 ** 8
                ).any():  # pragma: no cover
                    raise InvalidWeightsError(
                        "{} weights not normalised to range [0, 1]".format(weights_name)
                    )

                self._weights_no_area_weighting[weights_name] = weights

            except KeyError:
                raise InvalidWeightsError("Unknown weights: {}".format(weights_name))

        return weights

    def get_weights_array(self, weights_name):
        """
        Get a single weights array

        If the weights have previously been calculated the precalculated result is
        returned from the cache. Otherwise the appropriate WeightFunc is called with
        any kwargs specified in the constructor.

        Parameters
        ----------
        weights_name : str
            Region to get weights for

        Returns
        -------
        ndarray[bool]
            Weights for the region specified by ``weights_name``

        Raises
        ------
        InvalidWeightsError
            If the cube has no data which matches the input weights or is
            invalid in any other way
        """
        try:
            return self._weights[weights_name]
        except KeyError:
            weights_without_area = self.get_weights_array_without_area_weighting(
                weights_name
            )
            area_weights = self._get_area_weights()
            weights = self._combine_area_weights_and_weights_without_area(
                area_weights=area_weights, weights_without_area=weights_without_area,
            )

        if np.equal(np.sum(weights), 0):
            raise InvalidWeightsError(
                "All weights are zero for region: `{}`".format(weights_name)
            )

        self._weights[weights_name] = weights
        return weights

    @abstractmethod
    def _combine_area_weights_and_weights_without_area(
        self, area_weights, weights_without_area
    ):
        raise NotImplementedError

    def _get_area_weights(self):
        if self._area_weights is None:
            self._area_weights = self.cube.get_area_weights()

        return self._area_weights

    def get_weights(self, weights_names):
        """
        Get a number of weights

        Parameters
        ----------
        weights_names: list of str
            List of weights to attempt to load/calculate.

        Returns
        -------
        dict of str: :obj:`np.ndarray`
            Dictionary where keys are weights names and values are :obj:`np.ndarray` of
            bool. The result only contains valid weights. Any invalid weights are dropped.

        Notes
        -----
        This method handles all exceptions and will only
        return weights which can actually be calculated. If no weights could
        be calculated, an empty dictionary will be returned.
        """
        weights = {}
        for name in weights_names:
            try:
                weights_for_name = self.get_weights_array(name)
                weights[name] = weights_for_name
            except InvalidWeightsError as e:
                logger.warning("Failed to create '%s' weights: %s", name, str(e))

        return weights


class AreaSurfaceFractionWeightCalculator(CubeWeightCalculator):
    r"""
    Calculates weights which are both area and surface fraction weighted

    .. math::

        w(lat, lon) = a(lat, lon) \\times s(lat, lon)

    where :math:`w(lat, lon)` is the weight of the cell at given latitude and
    longitude, :math:`a` is area of the cell and :math:`s` is the surface
    fraction of the cell (e.g. fraction of ocean area for ocean based regions).
    """

    def _combine_area_weights_and_weights_without_area(
        self, area_weights, weights_without_area
    ):
        return area_weights * weights_without_area


class AreaWeightCalculator(CubeWeightCalculator):
    r"""
    Calculates weights which are area weighted but surface fraction aware.

    This means that any cells which have a surface fraction of zero will
    receive zero weight, otherwise cells are purely area weighted.

    .. math::

        w(lat, lon) = \\begin{cases}
            a(lat, lon), & s(lat, lon) > 0 \\\\
            0, & s(lat, lon) = 0
        \\end{cases}

    where :math:`w(lat, lon)` is the weight of the cell at given latitude and
    longitude, :math:`a` is area of the cell and :math:`s` is the surface
    fraction of the cell (e.g. fraction of ocean area for ocean based regions).
    """

    def _combine_area_weights_and_weights_without_area(
        self, area_weights, weights_without_area
    ):
        weights_without_area_binary = np.array(
            ~np.equal(weights_without_area, 0)
        ).astype(int)

        return area_weights * weights_without_area_binary
