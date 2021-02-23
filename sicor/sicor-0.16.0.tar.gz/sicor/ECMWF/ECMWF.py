#!/usr/bin/env python
"""
Downloading and interpolation within ECMWF variables (also grib/netCDF to hdf5 conversion).
"""
import calendar
from datetime import datetime
import numpy as np
import tables

import h5py
import logging
from datetime import timedelta
from os.path import join, dirname, isfile
from os import makedirs, remove
# non-standard imports
from netCDF4 import Dataset
from multiprocessing import Pool


__author__ = "Niklas Bohn, Andre Hollstein"

"""
to install:
pip install ecmwf-api-client
documentation:
https://software.ecmwf.int/wiki/display/WEBAPI/Accessing+ECMWF+data+servers+in+batch
keyfile: needed in $HOME/.ecmwfapirc
"""

"""
pip install pygrib # might not work for you since it did not work for me -> manual install might be needed here
1st: grib_api
download software here: https://www.ecmwf.int/en/elibrary/18135-grib-api

e.g. on Fedora 21:
>yum install openjpeg
>yum install jasper
>yum install openjpeg-devel
>yum install jasper-devel

# bash style:
grib_api-1.13.0.tar.gz -> untar to dir, move into, then:

build_path="/home/andre/working/enmap_cloud_sceening/momo/get_ECMWF_products/pygrib/build"
./configure --prefix $build_path

>make
>make check
>make install

2nd: pygrib

git clone https://github.com/jswhit/pygrib.git
cd pygrib
cp setup.cfg.template setup.cfg

edit setup.cfg, e.g.:
grib_api_dir = /home/andre/working/enmap_cloud_sceening/momo/get_ECMWF_products/pygrib/build/

>python setup.py build
>python setup.py install

"""


# noinspection PyPep8
class ECMWF_download(object):
    def __init__(self, server, logger=None, max_step=120):
        """
        Class for downloading data from the ECMWF service.
        :param server: instance of ECMWFDataServer
        """
        self.logger = logger or logging.getLogger(__name__)
        self.server = server

        # "hard wired" parameters for retrieving data from era interim
        # get for analysis: http://apps.ecmwf.int/datasets/data/interim-full-daily/
        # get for forecast: http://apps.ecmwf.int/datasets/data/cams-nrealtime/

        ecmwf_fc_steps = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69,
                          72, 75, 78, 81, 84, 87, 90, 93, 96, 99, 102, 105, 108, 111, 114, 117, 120]
        step_fc = "/".join([str(step) for step in ecmwf_fc_steps if step <= max_step])

        self.era_setup = {
            "fc_T2M": {
                "Name": "2 metre temperature",
                "class": "mc",
                "dataset": "cams_nrealtime",
                "expver": "0001",
                "levtype": "sfc",
                "param": "167.128",
                "step": step_fc,
                "stream": "oper",
                "time": "00:00:00",
                "type": "fc",
                "levellist": None
            },
            "fc_O3": {
                "Name": "GEMS Total column ozone",
                "class": "mc",
                "dataset": "cams_nrealtime",
                "expver": "0001",
                "levtype": "sfc",
                "param": "206.210",
                "step": step_fc,
                "stream": "oper",
                "time": "00:00:00",
                "type": "fc",
                "levellist": None
            },
            "fc_SLP": {
                "Name": "Mean sea level pressure",
                "class": "mc",
                "dataset": "cams_nrealtime",
                "expver": "0001",
                "levtype": "sfc",
                "param": "151.128",
                "step": step_fc,
                "stream": "oper",
                "time": "00:00:00",
                "type": "fc",
                "levellist": None
            },
            "an_TCWV": {  # untested
                "Name": "Total column water vapour",
                "class": "ei",
                "dataset": "interim",
                "expver": "1",
                "grid": "0.75/0.75",
                "levtype": "sfc",
                "param": "137.128",
                "step": "0",
                "stream": "oper",
                "time": "00/06/12/18",
                "type": "an",
                "levellist": None
            },
            "fc_TCWV": {  # tested
                "Name": "Total column water vapour",
                "class": "mc",
                "dataset": "macc_nrealtime",
                "expver": "0001",
                "levtype": "sfc",
                "param": "137.128",
                "step": step_fc,
                "stream": "oper",
                "time": "00:00:00",
                "type": "fc",
                "levellist": None
            },
            "fc_GMES_ozone": {  # tested
                "Name": "GEMS Total column ozone",
                "class": "mc",
                "dataset": "macc_nrealtime",
                "expver": "0001",
                "levtype": "sfc",
                "param": "206.210",
                "step": step_fc,
                "stream": "oper",
                "time": "00:00:00",
                "type": "fc",
                "levellist": None
            },
            "an_GMES_ozone": {  # untested
                "Name": "Total column ozone",
                "class": "ei",
                "dataset": "interim",
                "date": "2015-05-01/to/2015-05-31",
                "expver": "1",
                "grid": "0.75/0.75",
                "levtype": "sfc",
                "param": "206.128",
                "step": "0",
                "time": "00/06/12/18",
                "stream": "oper",
                "type": "an",
                "levellist": None
            },
            "fc_total_AOT_550nm": {
                "Name": "Total Aerosol Optical Depth at 550nm",
                "class": "mc",
                "dataset": "macc_nrealtime",
                "expver": "0001",
                "levtype": "sfc",
                "param": "207.210",
                "step": step_fc,
                "stream": "oper",
                "time": "00:00:00",
                "type": "fc",
                "levellist": None,
            },
            "fc_sulphate_AOT_550nm": {
                "Name": "Sulphate Aerosol Optical Depth at 550nm",
                "class": "mc",
                "dataset": "macc_nrealtime",
                "expver": "0001",
                "levtype": "sfc",
                "param": "212.210",
                "step": step_fc,
                "stream": "oper",
                "time": "00:00:00",
                "type": "fc",
                "levellist": None,
            },
            "fc_black_carbon_AOT_550nm": {
                "Name": "Black Carbon Aerosol Optical Depth at 550nm",
                "class": "mc",
                "dataset": "macc_nrealtime",
                "expver": "0001",
                "levtype": "sfc",
                "param": "211.210",
                "step": step_fc,
                "stream": "oper",
                "time": "00:00:00",
                "type": "fc",
                "levellist": None,
            },
            "fc_dust_AOT_550nm": {
                "Name": "Dust Aerosol Optical Depth at 550nm",
                "class": "mc",
                "dataset": "macc_nrealtime",
                "expver": "0001",
                "levtype": "sfc",
                "param": "209.210",
                "step": step_fc,
                "stream": "oper",
                "time": "00:00:00",
                "type": "fc",
                "levellist": None,
            },
            "fc_organic_matter_AOT_550nm": {
                "Name": "Organic Matter Aerosol Optical Depth at 550nm",
                "class": "mc",
                "dataset": "macc_nrealtime",
                "expver": "0001",
                "levtype": "sfc",
                "param": "210.210",
                "step": step_fc,
                "stream": "oper",
                "time": "00:00:00",
                "type": "fc",
                "levellist": None,
            },
            "fc_sea_salt_AOT_550nm": {
                "Name": "Sea Salt Aerosol Optical Depth at 550nm",
                "class": "mc",
                "dataset": "macc_nrealtime",
                "expver": "0001",
                "levtype": "sfc",
                "param": "208.210",
                "step": step_fc,
                "stream": "oper",
                "time": "00:00:00",
                "type": "fc",
                "levellist": None,
            },
            "an_temperature": {
                "Name": "Temperature",
                "step": "0",
                "grid": "0.75/0.75",
                "class": "ei",
                "dataset": "interim",
                "stream": "oper",
                "time": "00/06/12/18",
                "type": "an",
                "param": "130.128",
                "levtype": "ml",
                "levellist": "/".join([str(i) for i in range(1, 60 + 1)])

            },
            "an_specific_humidity": {
                "Name": "Specific humidity",
                "step": "0",
                "grid": "0.75/0.75",
                "class": "ei",
                "dataset": "interim",
                "stream": "oper",
                "time": "00/06/12/18",
                "type": "an",
                "param": "133.128",
                "levtype": "ml",
                "levellist": "/".join([str(i) for i in range(1, 60 + 1)])

            },
            "an_ozone_mass_mixing_ratio": {
                "Name": "Ozone mass mixing ratio",
                "step": "0",
                "grid": "0.75/0.75",
                "class": "ei",
                "dataset": "interim",
                "stream": "oper",
                "time": "00/06/12/18",
                "type": "an",
                "param": "203.128",
                "levtype": "ml",
                "levellist": "/".join([str(i) for i in range(1, 60 + 1)])
            },
            "an_surface_pressure": {
                "Name": "Surface pressure",
                "step": "0",
                "grid": "0.75/0.75",
                "class": "ei",
                "dataset": "interim",
                "stream": "oper",
                "time": "00/06/12/18",
                "type": "an",
                "param": "134.128",
                "levtype": "sfc",
                "levellist": None,
                "unit_conversion": lambda x: x / 100.  # conversion from Pa to hPa
            },
            "an_column_water_vapour": {
                "Name": "Total column water vapour",
                "step": "0",
                "grid": "0.75/0.75",
                "class": "ei",
                "dataset": "interim",
                "stream": "oper",
                "time": "00/06/12/18",
                "type": "an",
                "param": "137.128",
                "levtype": "sfc",
                "levellist": None
            },
            "an_column_ozone": {
                "Name": "Total column ozone",
                "step": "0",
                "grid": "0.75/0.75",
                "class": "ei",
                "dataset": "interim",
                "stream": "oper",
                "time": "00/06/12/18",
                "type": "an",
                "param": "206.128",
                "levtype": "sfc",
                "levellist": None
            }
        }

        self.year = None
        self.month_start = None
        self.month_end = None
        self.day_start = None
        self.day_end = None

        self.jday_start = None
        self.jday_end = None
        self.tind_start = None
        self.tind_end = None

    @staticmethod
    def db_path(variable, dt, db_path):
        """

        :param variable:name as valid for downloading
        :param dt: date object
        :param db_path: root path for db
        :return: path to file
        """
        return join(db_path, variable, str(dt.year), "%02i" % dt.month,
                    "%4i%02i%02i_%s.h5" % (dt.year, dt.month, dt.day, variable))

    def era_month_string(self, year, month=None, month_start=None, month_end=None, day_start=None, day_end=None):
        """
        Create string for ERA request

        :param year: integer, year
        :param month: integer, month or None, then month_start and month_end should be given
        :param month_start: integer or None, if None, month should be given
        :param month_end: integer or None, if None, month should be given
        :param day_start: integer or None, if None, assume 1
        :param day_end: integer or None, if None, end of month is used
        :return: string for era request
        """

        # basic sanity check for date inputs
        if month is not None or month_start == month_end:  # days are in the same month
            month_start = month
            month_end = month
            if month is None:  # set month
                month = month_start
                _, n_days = calendar.monthrange(year, month)
                if day_start is None:
                    day_start = 1
                if day_end is None:
                    day_end = n_days
                else:
                    assert day_start <= day_end
                    assert day_end <= n_days
        else:  # time span is covering different months
            _, n_days = calendar.monthrange(year, month_start)
            assert day_start >= 1
            assert day_start <= n_days

            _, n_days = calendar.monthrange(year, month_end)
            assert day_end >= 1
            assert day_end <= n_days

        # save dates in object
        self.year = year
        self.month_start = month_start
        self.month_end = month_end
        self.day_start = day_start
        self.day_end = day_end

        # compute time span
        self.jday_start = self.time_to_julian_day(year=self.year, month=self.month_start, day=self.day_start)
        self.jday_end = self.time_to_julian_day(year=self.year, month=self.month_end, day=self.day_end)
        self.tind_start = self.time_to_ind(self.jday_start, 0)
        self.tind_end = self.time_to_ind(self.jday_end, 3)

        return "%i-%0.2i-%0.2i/to/%i-%0.2i-%0.2i" % (year, month_start, day_start, year, month_end, day_end)

    def request(self, parameter, output_file_name, year, month=None, month_start=None, month_end=None, day_start=None,
                day_end=None, nc=False):
        """
        Prepare request for ECMWF server
        :param parameter: as given in self.era_setup
        :param output_file_name: string, file name, should be grb
        :param year:
        :param month:
        :param month_start:
        :param month_end:
        :param day_start:
        :param day_end:
        :param nc:
        :return:
        """
        assert parameter in self.era_setup, "parameter should one of:" + str(list(self.era_setup.keys()))

        rq = {key: item for key, item in self.era_setup[parameter].items() if key in
              ["class", "dataset", "date", "expver", "levtype", "param", "step", "stream", "time", "type"]}
        rq["target"] = output_file_name
        rq["date"] = self.era_month_string(year, month, month_start, month_end, day_start, day_end)
        if nc:
            rq["format"] = "netcdf"
            rq["grid"] = "0.705/0.705"
            if rq["type"] == "fc":
                rq["step"] = "0/3/6/9/12/15/18/21"
        return rq

    # set up little helper functions
    @staticmethod
    def time_to_ind(day, tme):
        return (day - 1) * 4 + tme

    @staticmethod
    def ind_to_time(ind):  # starts with zero for 1st Jan
        return ind / 4 + 1, ind % 4

    @staticmethod
    def time_to_julian_day(year, month, day):
        dt = datetime(year, month, day)
        return dt.timetuple().tm_yday

    def retrieve_grib(self, **kwargs):
        req = self.request(**kwargs)
        self.server.retrieve(req)

    def retrieve_netcdf(self, **kwargs):
        req = self.request(nc=True, **kwargs)
        self.server.retrieve(req)

    def retrieve_hdf5(self, complevel=1, remove_ECMWF_file=True, grib=True, **kwargs):
        hdf_file = kwargs["output_file_name"]
        if grib:
            grb_file = hdf_file + ".grb"
            kwargs["output_file_name"] = grb_file
            self.retrieve_grib(**kwargs)
            self.convert_grib_to_hdf5(grb_file=grb_file, hdf_file=hdf_file, complevel=complevel, **kwargs)
            if remove_ECMWF_file:
                self.logger.info("Remove grib file.")
                remove(grb_file)
        else:
            nc_file = hdf_file + ".nc"
            kwargs["output_file_name"] = nc_file
            self.retrieve_netcdf(**kwargs)
            self.convert_netcdf_to_hdf5(nc_file=nc_file, hdf_file=hdf_file, complevel=complevel, **kwargs)
            if remove_ECMWF_file:
                self.logger.info("Remove netCDF file.")
                remove(nc_file)

    def convert_grib_to_hdf5(self, grb_file, hdf_file, complevel=1, **kwargs):

        import pygrib

        parameter = kwargs["parameter"]

        def identity(x):
            return x

        try:
            unit_conversion = self.era_setup["parameter"]["unit_conversion!!!"]
        except KeyError:
            unit_conversion = identity  # no unit conversion

        self.logger.info("Open grb file: %s" % grb_file)
        with pygrib.open(grb_file) as era_data_file:
            lats, lons = era_data_file.message(1).latlons()
            lat, lon = lats[:, 0], lons[0, :]

            if self.era_setup[parameter]["step"] != "0":  # we use forcast data
                tp = "forcast"
                tinds = np.arange(self.tind_start, self.tind_end + 1)  # four times per day for reanalysis
                # number of steps * number of days
                n_time = int((self.era_setup[parameter]["step"].count("/") + 1)) * int((len(tinds) / 4))
                tinds = tinds[::4]  # only t0
                steps = [int(s) for s in self.era_setup[parameter]["step"].split("/")]
            else:  # we use reanalysis data, 4 steps per day
                tp = "reanalysis"
                tinds = np.arange(self.tind_start, self.tind_end + 1)
                steps = None
                n_time = len(tinds)

            n_lat = len(lat)
            n_lon = len(lon)

            n_lev = 60

            at = tables.Float32Atom()
            fl = tables.Filters(complevel=complevel, complib='zlib')

            self.logger.info("Create HDF file: %s" % hdf_file)
            with tables.open_file(hdf_file, "w") as era_h5_file:
                era_h5 = era_h5_file.root

                if self.era_setup[parameter]['levellist'] is None:  # 2D type parameter
                    shape = (n_time, n_lat, n_lon)
                    n_dim_parameter = 2
                elif self.era_setup["temperature"]['levellist'].count("/") + 1 == n_lev:
                    shape = (n_time, n_lev, n_lat, n_lon)
                    n_dim_parameter = 3
                else:
                    raise NotImplementedError("To Do")

                meta_data = [("tinds", tinds), ("lons", lons), ("lats", lats), ("lon", lon), ("lat", lat),
                             ("day_start", self.day_start), ("day_end", self.day_end),
                             ("month_start", self.month_start), ("month_end", self.month_end),
                             ("year", self.year)]
                if steps is not None:
                    meta_data.append(("steps", np.array(steps, dtype=float)))

                for name, obj in meta_data:
                    era_h5_file.create_array(era_h5, name=name, obj=obj)
                data = era_h5_file.create_carray(era_h5, name=parameter, title=self.era_setup[parameter]["Name"],
                                                 atom=at, shape=shape, filters=fl)
                data[:, :, :] = np.NaN

                for ii, grb in enumerate(era_data_file.select(name=self.era_setup[parameter]["Name"], year=self.year)):
                    tind = self.time_to_ind(self.time_to_julian_day(grb["year"], grb["month"], grb["day"]),
                                            {0: 0, 600: 1, 1200: 2, 1800: 3}[grb["time"]])
                    if tp == "reanalysis":
                        if tind != tinds[ii]:
                            raise ValueError("Incorrect times in grb file.")
                        if n_dim_parameter == 2 and tp == "reanalysis":
                            data[ii, :, :] = unit_conversion(grb.data()[0])
                        elif n_dim_parameter == 3:
                            data[ii, grb["level"] - 1, :, :] = unit_conversion(grb.data()[0])
                    elif tp == "forcast":
                        if n_dim_parameter == 2:
                            data[steps.index(grb["step"]), :, :] = grb.data()[0]
                        else:
                            raise ValueError(tp)

            self.logger.info("Done writing data to HDF5 file.")
        self.logger.info("Done reading from grb file.")

    def convert_netcdf_to_hdf5(self, nc_file, hdf_file, complevel=1, **kwargs):

        parameter = kwargs["parameter"]

        def identity(x):
            return x

        try:
            unit_conversion = self.era_setup["parameter"]["unit_conversion!!!"]
        except KeyError:
            unit_conversion = identity  # no unit conversion

        self.logger.info("Open netcdf file: %s" % nc_file)
        with Dataset(nc_file) as era_data_file:
            lat = np.asarray(era_data_file.variables["latitude"])
            lon = np.asarray(era_data_file.variables["longitude"])

            if self.era_setup[parameter]["step"] != "0":  # we use forcast data
                tp = "forcast"
                tinds = np.arange(self.tind_start, self.tind_end + 1)  # four times per day for reanalysis
                # number of steps * number of days
                n_time = int((self.era_setup[parameter]["step"].count("/") + 1)) * int((len(tinds) / 4))
                tinds = tinds[::4]  # only t0
                steps = [int(s) for s in self.era_setup[parameter]["step"].split("/")]
            else:  # we use reanalysis data, 4 steps per day
                tp = "reanalysis"
                tinds = np.arange(self.tind_start, self.tind_end + 1)
                steps = None
                n_time = len(tinds)

            n_lat = len(lat)
            n_lon = len(lon)
            lats = np.zeros((n_lat, n_lon))
            lons = np.zeros((n_lat, n_lon))
            for ii in range(n_lon):
                lats[:, ii] = lat
            for ii in range(n_lat):
                lons[ii, :] = lon

            at = tables.Float32Atom()
            fl = tables.Filters(complevel=complevel, complib='zlib')

            self.logger.info("Create HDF file: %s" % hdf_file)
            with tables.open_file(hdf_file, "w") as era_h5_file:
                era_h5 = era_h5_file.root

                if self.era_setup[parameter]['levellist'] is None:  # 2D type parameter
                    shape = (n_time, n_lat, n_lon)
                    n_dim_parameter = 2
                else:
                    raise NotImplementedError("To Do")

                meta_data = [("tinds", tinds), ("lons", lons), ("lats", lats), ("lon", lon), ("lat", lat),
                             ("day_start", self.day_start), ("day_end", self.day_end),
                             ("month_start", self.month_start), ("month_end", self.month_end),
                             ("year", self.year)]
                if steps is not None:
                    meta_data.append(("steps", np.array(steps, dtype=float)))

                for name, obj in meta_data:
                    era_h5_file.create_array(era_h5, name=name, obj=obj)
                data = era_h5_file.create_carray(era_h5, name=parameter, title=self.era_setup[parameter]["Name"],
                                                 atom=at, shape=shape, filters=fl)
                data[:, :, :] = np.NaN

                for ii in range(era_data_file.variables["time"].shape[0]):
                    if tp == "reanalysis":
                        if n_dim_parameter == 2 and tp == "reanalysis":
                            data[ii, :, :] = unit_conversion(
                                era_data_file.variables[list(era_data_file.variables.keys())[3]][:][ii, :, :])
                        else:
                            raise ValueError(tp)
                    elif tp == "forcast":
                        if n_dim_parameter == 2:
                            data[ii, :, :] = era_data_file.variables[list(
                                era_data_file.variables.keys())[3]][:][ii, :, :]
                        else:
                            raise ValueError(tp)

            self.logger.info("Done writing data to HDF5 file.")
        self.logger.info("Done reading from netCDF file.")


def test():
    from ecmwfapi import ECMWFDataServer
    self = ECMWF_download(server=ECMWFDataServer(), max_step=24)
    if False:
        self.retrieve_grib(parameter="surface_pressure", year=2013, month=5, day_start=1, day_end=2,
                           output_file_name="./dummy_1.grib")
        self.retrieve_hdf5(parameter="surface_pressure", year=2013, month_start=5, month_end=6, day_start=30, day_end=2,
                           output_file_name="./dummy_2.h5")
    if True:
        self.retrieve_hdf5(parameter="total_AOT_550nm", year=2016, month=5, day_start=17, day_end=17,
                           output_file_name="./dummy_3.h5")


def daterange(start_date, end_date):
    """
    generator for date objects between start_date and end_date
    :param start_date: date object
    :param end_date: date object
    :return: generator for dates between start_date and end_date
    """
    days_diff = int((end_date - start_date).days)

    if days_diff == 0:
        # in case start_date equals end_date
        yield start_date
    else:
        for n in range(days_diff):
            yield start_date + timedelta(n)


# noinspection PyPep8Naming
class ECMWF_variable(object):
    def __init__(self, variable, path_db, delta_day, var_date, dtype=np.float32, logger=None):
        """
        Initialize a selected ECMWF variable. Raise FileNotFoundError if file is not found in database.

        :param variable:  name string as valid for ECMWF_download
        :param path_db:   root of database for ECMWF data
        :param delta_day: deviation of database date from sensing date
        :param var_date:  date object
        """
        from scipy.interpolate import RegularGridInterpolator  # import here to avoid static TLS ImportError

        self.logger = logging.getLogger() if logger is None else logger
        self.fn = ECMWF_download.db_path(variable, var_date, path_db)

        if not isfile(self.fn):  # raise if file doesn't exist
            raise FileNotFoundError(self.fn)
        if delta_day != 0:
            self.logger.warning("ECMWF data of a different date than the acquisition day are used.")

        with h5py.File(name=self.fn, mode="r") as h5f:
            if 'steps' not in h5f.keys():
                self.steps = np.array([0], dtype=dtype)
            else:
                self.steps = np.array(h5f["steps"][()][:], dtype=dtype)
            self.lat = np.array(h5f["lat"][()][:], dtype=dtype)
            self.lon = np.array(h5f["lon"][()][:], dtype=dtype)
            self.variable = np.array(h5f[variable][()][:, :, :], dtype=dtype)
            self.points = (self.steps, self.lat[::-1], self.lon)
            self.values = self.variable[:, ::-1, :]
            if self.values.shape[0] != len(self.points[0]):
                self.steps = np.arange(0, self.values.shape[0] * 3, 3, dtype=dtype)
                self.points = (self.steps, self.lat[::-1], self.lon)
            for step in range(self.values.shape[0]):
                if np.isnan(self.values[step, :, :]).any():
                    self.values[step, :, :] = self.values[step - 1, :, :]
            self.var = RegularGridInterpolator(points=self.points, values=self.values, method="linear")

    def __call__(self, step, lons, lats, shape=None, order=3, dtype=np.float32, force_bounds=True):
        """

        :param step: time in h
        :param lons: 2D array of lon values: 0° - 359°  (correspond to: -180 - 180)
                 prepare lons[-180:180] before: (360 + lons) % 360
        :param lats: 2D array of lat values: -90° - 90°
        :param shape: None or final shape, zoom is used for resampling
        :param order: interpolation order of shape is not None
        :param force_bounds: True / False, force step between bounds of the actually loaded file
        :return: 2D array of variable
        """
        from scipy.ndimage import zoom  # import here to avoid static TLS ImportError

        if step < self.steps[0] or step > self.steps[-1]:
            self.logger.warning(
                "The chosen step of %f is out of bounds [%f,%f]" % (step, self.steps[0], self.steps[-1]))
            if force_bounds is True:  # make sure step is within bounds
                self.logger.warning("Force step to bounds.")
                step = np.clip(step, self.steps[0], self.steps[-1])
            else:
                raise ValueError("Parameter step is out of bounds.")

        ao = self.var(np.vstack((step * np.ones(np.prod(lons.shape)),
                                 lats.reshape(-1),
                                 lons.reshape(-1))
                                ).transpose()).reshape(lons.shape)
        if shape is None:
            return np.array(ao, dtype=dtype)
        else:
            assert len(shape) == 2
            return np.array(zoom(input=ao, zoom=[x / y for x, y in zip(shape, lats.shape)], order=order), dtype=dtype)


def __download__(param):
    from ecmwfapi.api import APIException
    # noinspection PyGlobalUndefined
    global download  # provided by initializer in multiprocessing mode
    try:
        download.retrieve_hdf5(**param)
        param["status"] = "OK"
    except APIException as err:
        param["status"] = "error"
        param["error"] = repr(err)
    return param


# noinspection PyShadowingNames
def download_variables(ecmwf_variables, db_path, date_from, date_to, db_path_function=None, processes=0, force=False,
                       max_step=120, grib=True):
    """ download ECMWF products to file system

    :param processes:
    :param ecmwf_variables: iterable of variable names, e.g. [total_AOT_550nm]
    :param db_path: root path of db
    :param db_path_function: (variable,dt,db_path) -> output_file_name, if not given, ECMWF_download.db_path is used
    :param date_from: date object, start date
    :param date_to: date object, end date
    :param force: bool, whether to filter for already available files or not
    :param max_step: largest ECMWF forecast step to download in hours
    :param grib: if True, download grib file, else netcdf (mandatory for windows systems)
    :return: list of downloaded products
    """

    def initializer():
        from ecmwfapi import ECMWFDataServer
        global download
        # make ECMWF instance for data download
        download = ECMWF_download(server=ECMWFDataServer(), max_step=max_step)

    if db_path_function is None:
        db_path_function = ECMWF_download.db_path

    # build full list of needed days
    params = [{"grib": grib, "output_file_name": db_path_function(variable, dt, db_path), "parameter": variable,
               "year": dt.year, "month": dt.month, "day_start": dt.day, "day_end": dt.day}
              for dt in daterange(date_from, date_to) for variable in ecmwf_variables]
    # filter for missing days
    if force is False:
        params = [param for param in params if not isfile(param["output_file_name"])]
    # create directory tree in advance to keep life simple
    for pp in (set([dirname(pp["output_file_name"]) for pp in params])):
        makedirs(pp, exist_ok=True)

    if processes == 0:
        initializer()
        params = [__download__(param) for param in params]
    else:
        with Pool(processes=processes, initializer=initializer) as pool:
            pool.map(__download__, params)

    return params
