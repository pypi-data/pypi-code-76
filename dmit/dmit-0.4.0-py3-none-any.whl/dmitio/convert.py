#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 \nUtility to convert files from one format to another.
This is very much work in progress and thus not everything
should be expected to work perfect. 

Currently handled formats are:
- GRIB to NetCDF

It is important to set the ECCODES_DEFINITION_PATH correctly before running this.
Especially if you are using some local definitions. For example:
export ECCODES_DEFINITION_PATH=/home/$USER/local_grib_definitions/definitions/:/home/$USER/miniconda3/envs/$ENV/share/eccodes/definitions/
"""
import os
import sys
sys.path.append("../")
import traceback
import docopt
import netCDF4 as nc
import xarray as xr

import dmitio
import ostools
import grib
import netcdf

version = '0.0.1'

__doc__ += """
Usage:
  {filename} [grib_to_nc] [options]
  {filename} (-h | --help)
  {filename} --version

Commands:
  grib_to_nc                    Convert grib-file(s) to NetCDF.

Options:
  --namelist <str>              Specify namelist if not using default
  --indir <str>                 Specify input directory with files to convert. Directory should ONLY hold files to convert.
  -o, --output <str>            Specify output file [default: foo]      
  -h, --help                    Show this screen.
  -V, --version                 Show version

""".format(filename=os.path.basename(__file__), version=version)


if __name__=="__main__":

    if len(sys.argv) < 2:
        print('Input missing: try with -h or --help')
        sys.exit(1)

    args = docopt.docopt(__doc__, version=str(version))

    print('Start converter')
    
    if not args['--namelist']:
        basedir="{}".format(os.path.abspath(__file__+'/..'))
        nml = "{}/{}".format(basedir,"convert.json")
    else:
        nml = args['--namelist']

    try:
        namelist = dmitio.read_json(nml)
    except FileNotFoundError:
        print('Namelist not found')
        sys.exit(1)

    if args['grib_to_nc']:

        outputfile = args['--output']

        gribfiles = ostools.find_files(args['--indir'],
                                       recursive=False,
                                       onlyfiles=True,
                                       fullpath=True,
                                       inorder=True)

        gribread = grib.grib_reader(namelist)
        data = gribread.get_data(gribfiles, namelist)
        print('- Got data from grib files\nProceed to writing')

        ncwrite = netcdf.netcdf_write(namelist)
        ncwrite.write_data(data, outputfile)
        