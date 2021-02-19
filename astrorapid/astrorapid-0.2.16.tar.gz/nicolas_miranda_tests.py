import pandas as pd
from copy import copy
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

from astrorapid.custom_classifier import create_custom_classifier
from astrorapid.ANTARES_object.constants import TRIGGER_PHOTFLAG, GOOD_PHOTFLAG
from astrorapid.process_light_curves import InputLightCurve


BANDS = {'p48r': "r", 'p48g': "g"}
BANDS_VEC = np.vectorize(lambda x: BANDS[x])


def to_classnumber(lc):
    if lc.meta['classification'] == 'SN Ia':
        return 1
    else:
        return 2


def to_astrorapid(this_lc):
    if len(this_lc) < 2:
        return None

    this_lc = copy(this_lc)

    mask = np.logical_or.reduce((this_lc['band'] == 'p48r', this_lc['band'] == 'p48g'))
    this_lc = this_lc[mask]
    mask = this_lc['flux'] != 0.0
    this_lc = this_lc[mask]

    if len(this_lc) == 0:
        return None

    this_lc['band'] = BANDS_VEC(this_lc['band'])

    this_lc['photflag'] = [TRIGGER_PHOTFLAG] + (len(this_lc) - 1) * [GOOD_PHOTFLAG]

    class_number = to_classnumber(this_lc)

    return InputLightCurve(
        this_lc['mjd'],
        this_lc['flux'],
        this_lc['fluxerr'],
        this_lc['band'],
        this_lc['photflag'],
        this_lc.meta['ra'],
        this_lc.meta['dec'],
        this_lc.meta['ztfname'],
        redshift=this_lc.meta['z'],
        mwebv=this_lc.meta['mwebv'],
        training_set_parameters={'class_number': class_number, 'peakmjd': this_lc[np.argmax(this_lc['flux'])]['mjd']}
    )


def get_data(class_num, data_dir, save_dir, passbands, known_redshift, nprocesses, redo):
    lc_data_path = "rcf_marshallc_sncosmo_2018.pkl"
    lc_data = pd.read_pickle(lc_data_path)

    lightcurves = {str(to_classnumber(val)) + '_' + str(key): to_astrorapid(val) for key, val in lc_data.items()}
    valid_lightcurves = {key: val.preprocess_light_curve() for key, val in lightcurves.items() if val is not None}

    return valid_lightcurves


create_custom_classifier(get_data, 'data', plot=True, class_nums=(1,2), reread_data=False, retrain_network=False, nprocesses=1)

