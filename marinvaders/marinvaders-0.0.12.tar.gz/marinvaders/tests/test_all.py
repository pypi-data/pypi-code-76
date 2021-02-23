import sys

import pandas as pd

sys.path.append('..')

import marinvaders.marinelife as ml  # noqa: E402
import marinvaders.readers as readers  # noqa: E402


def test_ecoregions():
    """
    test existance and fields of ecoregion
    """
    marine_ecoregions = ml.marine_ecoregions()
    assert len(marine_ecoregions) > 0
    assert ['ECO_CODE', 'ECO_CODE_X', 'ECOREGION',
            'PROVINCE', 'REALM',
            'geometry'] == list(marine_ecoregions.columns)


def test_species_class():
    """
    test instance of Species object for random species which we assume
    is always present at obis
    """
    ds = ml.Species(145634)
    assert ds.aphia_id == 145634
    assert len(ds.obis) > 0
    assert isinstance(ds.obis, pd.DataFrame)


def test_marine_life_class():
    """
    test instance of MarineLife object for specific eco code
    """
    marinelife = ml.MarineLife(20194)
    assert marinelife.eco_code == 20194


def test_readers():
    """
    test data readers for different stored datasets
    """
    ecomrgidlink = readers.eco_mrgid_link()
    assert isinstance(ecomrgidlink, pd.DataFrame)
    assert len(ecomrgidlink) > 0

    taxonomy = readers.read_taxonomy()
    assert isinstance(taxonomy, pd.DataFrame)
    assert 'species' in taxonomy.columns
    assert len(taxonomy) > 0

    gisd = readers.read_gisd()
    assert isinstance(gisd, pd.DataFrame)
    assert len(gisd) > 0

    natcon = readers.read_natcon()
    assert isinstance(natcon, pd.DataFrame)
    assert len(natcon) > 0

    gisd_worms_link = readers.read_gisd_worms_link()
    assert isinstance(gisd_worms_link, pd.DataFrame)
    assert len(gisd_worms_link) > 0
