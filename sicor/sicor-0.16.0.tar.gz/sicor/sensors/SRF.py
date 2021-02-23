import numpy as np
from pkg_resources import resource_filename, Requirement, DistributionNotFound
from os.path import dirname, join, isfile
import zipfile
import io
from pyrsr import RelativeSpectralResponse


class __SensorSRF(object):
    def __init__(self, srfs, srfs_wvl):
        """
        Baseclass for instrument sicor srfs.
        :param srfs: dictionary with [band_name]:[numpy array with spectral response function table for srfs_wvl]
        :param srfs_wvl: spectral axis for all srf's in srfs
        """
        self.srfs = srfs
        self.srfs_wvl = srfs_wvl

        self.bands = sorted(self.srfs.keys())
        self.wvl = [int(np.trapz(x=self.srfs_wvl, y=self.srfs_wvl * self.srfs[band])) for band in self.bands]
        self.conv = {}
        self.conv.update({key: value for key, value in zip(self.bands, self.wvl)})
        self.conv.update({value: key for key, value in zip(self.bands, self.wvl)})

    def instrument(self, bands):
        instrument = {
            'rspf': np.vstack([self[band] for band in bands]),
            'wvl_rsp': np.copy(self.srfs_wvl),
            'sol_irr': None
        }
        instrument['wvl_inst'] = np.trapz(x=instrument['wvl_rsp'], y=instrument['rspf'][:, :] * instrument['wvl_rsp'])
        return instrument

    def __call__(self, band):
        return self.srfs[band]

    def __getitem__(self, band):
        return self.srfs[band]


class SensorSRF(__SensorSRF):
    def __init__(self, sensor="S2A"):
        """
        Instrument spectral response functions for all supported sensors.
        :param sensor: String with support instrument identifier, possible is: 'S2A','Landsat-8'
        :returns: Sicor __SensorSRF object
        """

        if sensor in ["S2A", "S2B"]:
            srfs, srfs_wvl = self.sentinel2(sensor=sensor)
        elif "Landsat-" in sensor:
            srfs, srfs_wvl = self.landsat(sensor=sensor)
        else:
            raise ValueError("SRF's for sensor %s is unknown." % sensor)

        super().__init__(srfs=srfs, srfs_wvl=srfs_wvl)
        self.fn_srf = ""

    def landsat(self, sensor):
        """
        Read Landsat srf's from zipfile which includes srf's for multiple instruments
        :param sensor: "Landsat-X", X=8,...,
        :return: srfs, wvl for __SensorSRF.__init__
        """
        from scipy.interpolate import interp1d  # import here to avoid static TLS ImportError

        fn_srf = "landsat/data/SRF_Landsat.zip"
        try:
            fn = resource_filename(Requirement.parse("sicor"), fn_srf)
        except DistributionNotFound:
            fn = join(dirname(__file__), fn_srf)
            if isfile(fn) is False:
                raise FileNotFoundError(fn_srf)
        else:
            if isfile(fn) is False:
                fn = join(dirname(__file__), fn_srf)
                if isfile(fn) is False:
                    raise FileNotFoundError(fn_srf)
        self.fn_srf = fn
        srfs = {}
        wvl = np.arange(400, 2500, 1)
        with zipfile.ZipFile(self.fn_srf) as zipper:
            for fl in [fl for fl in zipper.namelist() if sensor in fl and "band" in fl]:
                with io.BufferedReader(zipper.open(fl, mode='r')) as f:
                    bf = np.loadtxt(f, skiprows=1)
                    srfs[fl.split("band_")[-1]] = interp1d(
                        x=bf[:, 0] * 1000, y=bf[:, 1], fill_value=0.0, bounds_error=False)(wvl)
        if len(srfs) == 0:
            raise ValueError("No data found for %s, update: %s" % (sensor, self.fn_srf))

        return srfs, wvl

    def sentinel2(self, sensor="S2A"):
        """
        Load Sentinel-2A spectral response function.

        :param sensor: name of Sentinel sensor (2A or 2B)
        :return: srfs, wvl for __SensorSRF.__init__
        """

        if sensor == "S2A":
            satellite = "Sentinel-2A"
        else:
            satellite = "Sentinel-2B"

        RSR = RelativeSpectralResponse(satellite=satellite, sensor='MSI')

        wvl = RSR.rsrs_wvl

        band_map = {'1': 'B01',
                    '2': 'B02',
                    '3': 'B03',
                    '4': 'B04',
                    '5': 'B05',
                    '6': 'B06',
                    '7': 'B07',
                    '8': 'B08',
                    '8A': 'B8A',
                    '9': 'B09',
                    '10': 'B10',
                    '11': 'B11',
                    '12': 'B12'}

        srfs = {}

        for key in band_map.keys():
            srfs[band_map[key]] = RSR.rsrs[key]

        return srfs, wvl
