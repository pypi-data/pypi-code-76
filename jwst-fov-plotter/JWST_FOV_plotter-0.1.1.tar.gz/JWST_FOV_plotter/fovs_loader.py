import pandas as pd
from astropy.io import fits
import numpy as np


def load_fits_or_csv(file_name):
    """
    Function to easily load a .csv or .fits table and end up with the same
    pandas Dataframe format independently of the original file extension.

    Arguments:
    file_name -- name to the .fits or .csv file to be loaded as a pandas
                 DataFrame
    Return:
    dat -- pandas DataFrame with the content of the .csv or .fits input file.
    """

    if file_name[-4:] == '.csv':
        dat = pd.read_csv(file_name)
    elif file_name[-5:] == '.fits':
        dat = fits.open(file_name)
        dat = pd.DataFrame(np.array(dat[1].data).byteswap().newbyteorder())
    else:
        print('Not .csv of .fits input file.')

    return dat


def fovs_loader(fovs):
    """
    Loads the .csv or .fits file containing the geometry of the FOVs in V2V3
    coordinates.

    Arguments:
    fovs -- name of a .csv or .fits file containing the geometry of all the
            FOVs in the V2V3 reference system, including at least the following
            columns:
            [Instrument', 'Aperture', 'V2_Ref', 'V3_Ref', 'V3_IdlYAngle',
            'V2_1', 'V2_2', 'V2_3', 'V2_4', 'V3_1', 'V3_2', 'V3_3', 'V3_4]
.           If None, the SIAF table from
        https://jwst-docs.stsci.edu/jwst-observatory-hardware/jwst-field-of-view
            is used. Default: None.

    Returns:
    fovs_dataframe -- pandas DataFrame containing the geometry of the FOVs in
                      V2V3 coordinates.
    """

    if fovs is None:
        fovs_dataframe = pd.read_csv('SIAF_V2V3_FOVs.csv')
    else:
        fovs_dataframe = load_fits_or_csv(fovs)

    return fovs_dataframe
