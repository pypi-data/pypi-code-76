"""
Miscellaneous definitions used in netCDF-SCM
"""

_SCM_TIMESERIES_META_COLUMNS = [
    "variable",
    "variable_standard_name",
    "region",
    "scenario",
    "climate_model",
    "member_id",
    "mip_era",
    "activity_id",
]
"""Metadata columns to include when creating SCM timeseries"""

_LAND_FRACTION_REGIONS = [
    "World",
    "World|Land",
    "World|Ocean",
    "World|Northern Hemisphere",
    "World|Northern Hemisphere|Land",
    "World|Northern Hemisphere|Ocean",
    "World|Southern Hemisphere",
    "World|Southern Hemisphere|Land",
    "World|Southern Hemisphere|Ocean",
]
"""
list: Regions required to perform land fraction calculations

We require all the ocean regions too as it only makes sense to return land fraction if
we're actually looking at data which contains a split.
"""

NAME_COMPONENTS_SEPARATOR = "_"
"""
str: Character assumed to separate different components within a filename

For example, if we come across a filename like 'tas_r1i1p1f1_UoM-Fancy' then
we assume that 'tas', 'r1i1p1f1' and 'UoM-Fancy' all refer to different bits
of metadata which are encoded within the filename.
"""

OUTPUT_PREFIX = "netcdf-scm"
"""
str: Prefix attached to outputs from netCDF-SCM by default
"""
