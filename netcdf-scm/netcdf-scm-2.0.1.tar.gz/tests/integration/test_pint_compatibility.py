import numpy.testing as npt
from openscm_units import unit_registry

from netcdf_scm.io import load_mag_file


def test_stitch_output(stitched_mag_file):
    drs = "CMIP6Output" if "CMIP6" in stitched_mag_file else "MarbleCMIP5"
    res = load_mag_file(stitched_mag_file, drs=drs)

    check_unit = 3 * unit_registry(res.get_unique_meta("unit", no_duplicates=True))

    assert str(check_unit.units) != ""
    npt.assert_equal(check_unit.magnitude, 3)
