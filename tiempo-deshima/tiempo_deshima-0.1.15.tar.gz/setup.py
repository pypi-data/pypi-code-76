# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiempo_deshima',
 'tiempo_deshima.Atmosphere',
 'tiempo_deshima.DESHIMA',
 'tiempo_deshima.DESHIMA.MKID',
 'tiempo_deshima.DESHIMA.desim',
 'tiempo_deshima.DESHIMA.desim.lines',
 'tiempo_deshima.Telescope']

package_data = \
{'': ['*'],
 'tiempo_deshima': ['Data/eta_atm/*', 'Data/splines_Tb_sky/*'],
 'tiempo_deshima.DESHIMA.desim': ['data/*']}

install_requires = \
['astropy>=4.0.1,<5.0.0',
 'galspec>=0.2.5,<0.3.0',
 'joblib>=0.16.0,<0.17.0',
 'matplotlib>=3.3.2,<4.0.0',
 'numpy>=1.19.2,<2.0.0',
 'pandas>=1.1.2,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pydata_sphinx_theme>=0.4.0,<0.5.0',
 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'tiempo-deshima',
    'version': '0.1.15',
    'description': 'time-dependent end-to-end model for post-process optimization',
    'long_description': "[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4279085.svg)](https://doi.org/10.5281/zenodo.4279085)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nTime-dependent end-to-end model for post-process optimization of the DESHIMA spectrometer.\n\n## TL;DR\nTiEMPO allows for simulating the output of the DESHIMA spectrometer. The model features simulation of an input galaxy with atomic spectral lines that is sampled with the ABBA chopnod method. The simulation includes atmospheric distrotion through distortions in the optical thickness of the atmosphere due to precipitable water vapor using outputs of the ARIS model (provided by the user), telescope transmission and finally noise and attenuation due to the MKID filterbank of DESHIMA.\n\n## Output of the model \nThe model outputs the following data: \n1. Vector of the time: all moments in time at which the signal is calculated in s.\n2. Matrix of the power: matrix of all the power values of the signal in W. It has dimensions [5, #filters, #timesamples]. The first dimension equals 5, as 5 pwv values are taken in each timesample. \n3. Matrix of the sky temperature: matrix of the power converted to sky temperature (has the same dimensions as the matrix of the power) in K. \n4. Center frequencies of the filters: The center frequencies of the filters in the filterbank in the MKID chip in Hz. \n\nThe pwv values are taken in the following order: \n\n![pwv values](https://raw.githubusercontent.com/deshima-dev/tiempo_deshima/master/skychopping.png)\n1. Left position\n2. Center position with galaxy\n3. Right position\n4. Center position without galaxy\nThe pwv values in position 2 and position 4 are equal, but otherwise the sky temperatures are computed separately.\n\n## Using the model\n### Example\n```\ntime_vector, center_freq = tiempo_deshima.run_tiempo(input_dictionary = 'deshima_2', prefix_atm_data = 'aris200602.dat-', sourcefolder = '../Data/output_ARIS', save_name_data = 'TiEMPO_simulation')\n```\nInputs include:\n\n### Atmosphere\n**pwv_0** (*float*): The value of the precipitable water vapor that is added to the dpwv from ARIS in mm. \n**windspeed** (*float*): The windspeed of the atmosphere in m/s.\n**prefix_atm_data** (*string*): The beginning of the name with which the atmosphere data is saved. For example, if the files are called *sample-00.dat-000*, *sample-00.dat-001* etc, then Prefix_atm_data must be 'sample-00.dat-'\n**sourcefolder** (*string*): folder in which the atmosphere data is saved (relative to cwd)\n**grid** (*float*): The width of a grid square in the atmosphere map in m\n**max_num_strips** (*integer*): The number of atmosphere strips that are saved as ARIS output.\n**x_length_strip** (*int*): The length of one atmosphere strip in the x direction. This is the number of gridpoints, *not* the distance in meters.  \n**separation** (*float*): Separation between two chop positions in m, assuming that the atmosphere is at 1km height. Default is 1.1326 (this corresponds to 116.8 arcsec).\n**useDESIM** (*bool*): Determines whether the simple atmospheric model is used (0) or the more sophisticated desim simulation (1).\n**inclAtmosphere** (*bool*):Determines whether the simple atmospheric model is used (0) or the more sophisticated desim simulation (1).\n\n### Galaxy\n**luminosity** (*float*): Luminosity of the galaxy, in Log(L_fir [L_sol])\n**redshift** (*float*): The redshift of the galaxy\n**linewidth** (*float*): The linewidth, in km/s\n**num_bins** (*int*): Determines the amount of bins used in the simulation of the galaxy spectrum. \n**galaxy_on** (*bool*): Can be used to turn the galaxy in position 2 off. Default is True (galaxy is present).\n\n### Observation\n**EL** (*float*): The elevation of the telescope, in degrees\n**EL_vec** (*vector of floats*): If this parameter is set, it allows to specify the elevation of the telescope in degrees per timestep, for example in the case of tracking a target. Vector must have a length of 160Hz times obs_time.\n**obs_time** (*float*): The observation time. This parameter has to be smaller than **max_obs_time**, which is calculated using the windspeed and the total length of the strips of atmosphere data, in s.\n\n### Instrument\n**F_min** (*float*): Lowest center frequency of all the MKIDs.\n**spec_res** (*float*): Spectral resolution\n**f_spacing** (*float*): spacing between center frequencies = F/dF (mean).\n**num_filters** (*float*): Number of filters in the filterbank\n**beam_radius** (*float*): Radius of the Gaussian telescope beam in meters.\n\n### Miscellaneous\n**input_dictionary** (*string*): Determines where the input values of keywords F_min thru come from: either standard values for DESHIMA, manual entry from the keywords or from a txt file \n**dictionary_name** (*string*): name of a txt file in which the values of optional keywords are saved.\n**save_name_data** (*string*): The name with which the produced data is saved.\n**savefolder** (*string*): Folder in which the produced data is saved (relative to cwd)\n**save_P** (*bool*): determines whether power in Watts is saved\n**save_T** (*bool*): determines whether sky temperature in Kelvins is saved\n**n_jobs** (*int*): amount of threads in the threadpool\n**n_batches** (*int*): amount of batches in which the output data is divided into in time\n\n## Important instructions\n\n### Atmosphere\n* All atmosphere strips must have the same length in the x direction and a length in the y direction of at least 30 gridpoints. ('length' means number of gridpoints, *not* distance in meters)\n\n### Changing the number of filters or the distribution of the center frequencies of the filters\n* For each filter, an interpolation between the power and the sky temperature is made. This means that these interpolations need to be made and saved again if the center frequencies of the filters are changed, before TiEMPO can be run again. This can be done by using ```new_filterbank()``` with the desired input dictionary, which can be generated using ```get_dictionary()```.\n* Since the chip properties are altered, 'deshima_1' and 'deshima_2' cannot be used as keywords for *input_dictionary* anymore.\n\n#### Example of changing the filters\n```\ndict = tiempo_deshima.get_dictionary(input_dictionary = 'manual', prefix_atm_data = 'aris.dat-', sourcefolder = '../Data/output_ARIS', save_name_data = 'TiEMPO_simulation_new_filters')\ntiempo_deshima.new_filterbank(dict)\ntime_vector, center_freq = tiempo_deshima.run_tiempo(input_dictionary = 'manual', prefix_atm_data = 'aris.dat-', sourcefolder = '../Data/output_ARIS', save_name_data = 'TiEMPO_simulation_new_filters')\n```\n## Installation\n```\npip install tiempo_deshima\n```",
    'author': 'Esmee Huijten',
    'author_email': None,
    'maintainer': 'Stefanie-B',
    'maintainer_email': 's.a.brackenhoff@student.tudelft.nl',
    'url': 'https://github.com/deshima-dev/tiempo_deshima',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
