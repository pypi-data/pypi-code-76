import pytest
import sys
import subprocess
from dttxml.dtt2bunch import dtt2bunch


@pytest.mark.xfail(reason = """
This dttxml has references and the bunch exporter currently cannot handle this.
It uses DiagAccess to combinatorically export everything, and the references are
not available through the DiagAccess interfaces
""")
def test_dtt2hdf_1(fpath_join, tpath_join, plot, pprint):
    """
    """
    # EXAMPLE 1: Dealing with a SweptSine measurement file.

    # These are the xml files we want to get our data from.
    measurement_file = fpath_join('data', '2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
    b = dtt2bunch(measurement_file)
    proc = subprocess.run(['dtt2hdf', measurement_file, tpath_join('output.h5')])

    assert(proc.returncode == 0)


@pytest.mark.xfail(reason = """
This dttxml is internally parsed from 'transfer function B/A in format (Y)'.
Currently the parse_transfer function does not generate the FHz array using the
available data. It probably could, but needs testing against exported data.
""")
def test_dtt2hdf_2(fpath_join, tpath_join, plot, pprint):
    """
    """
    # EXAMPLE 1: Dealing with a SweptSine measurement file.

    # These are the xml files we want to get our data from.
    measurement_file = fpath_join('data', '2019-01-25_H1SUSETMX_L1_iEXC2DARM_HFDynamicsTest_40-110Hz.xml')

    b = dtt2bunch(measurement_file)
    proc = subprocess.run(['dtt2hdf', measurement_file, tpath_join('output.h5')])

    assert(proc.returncode == 0)




#@pytest.mark.xfail(reason = """
#""")
def test_dtt2hdf_3(fpath_join, tpath_join, plot, pprint):
    """
    """
    # EXAMPLE 1: Dealing with a SweptSine measurement file.

    # These are the xml files we want to get our data from.
    measurement_file = fpath_join('data', '2019-03-27_H1DARM_OLGTF_BB.xml')

    b = dtt2bunch(measurement_file)
    pprint("----------------------output dict---------------------------")
    pprint(b)
    pprint("----------------------output done---------------------------")
    proc = subprocess.run(['dtt2hdf', measurement_file, tpath_join('output.h5')])

    assert(proc.returncode == 0)
