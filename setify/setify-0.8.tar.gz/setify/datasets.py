import json
import urllib.request
import pandas as pd
from setify import utils


def _get_server():
    return 'https://setify.info:3000'


def hazardous_materials():
    fpath = utils.load_data(
        _get_server() + "/hazardous_materials", 'hazardous_materials.h5')
    return pd.read_hdf(fpath)


def walmart_store_location():
    fpath = utils.load_data(
        _get_server() + "/walmart_store_location", 'walmart_store_location.h5')
    return pd.read_hdf(fpath)


def holiday_songs_spotify():
    fpath = utils.load_data(
        _get_server() + "/holiday_songs_spotify", 'holiday_songs_spotify.h5')
    return pd.read_hdf(fpath)


def titanic():
    fpath = utils.load_data(_get_server() + "/titanic", 'titanic.h5')
    return pd.read_hdf(fpath)


def netflix_titles():
    fpath = utils.load_data(
        _get_server() + "/netflix_titles", 'netflix_titles.h5')
    return pd.read_hdf(fpath)


def wine_quality():
    fpath = utils.load_data(_get_server() + "/wine_quality", 'wine_quality.h5')
    return pd.read_hdf(fpath)


def country_birth_rate():
    fpath = utils.load_data(
        _get_server() + "/country_birth_rate", 'country_birth_rate.h5')
    return pd.read_hdf(fpath)


def country_death_rate():
    fpath = utils.load_data(
        _get_server() + "/country_death_rate", 'country_death_rate.h5')
    return pd.read_hdf(fpath)


def iris():
    fpath = utils.load_data(_get_server() + "/iris", 'iris.h5')
    return pd.read_hdf(fpath)


def country_name_code():
    fpath = utils.load_data(
        _get_server() + "/country_name_code", 'country_name_code.h5')
    return pd.read_hdf(fpath)


def logic_gate_not():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_not", 'logic_gate_not.h5')
    return pd.read_hdf(fpath)


def logic_gate_and():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_and", 'logic_gate_and.h5')
    return pd.read_hdf(fpath)


def logic_gate_nand():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_nand", 'logic_gate_nand.h5')
    return pd.read_hdf(fpath)


def logic_gate_or():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_or", 'logic_gate_or.h5')
    return pd.read_hdf(fpath)


def logic_gate_nor():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_nor", 'logic_gate_nor.h5')
    return pd.read_hdf(fpath)


def logic_gate_xor():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_xor", 'logic_gate_xor.h5')
    return pd.read_hdf(fpath)


def logic_gate_xnor():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_xnor", 'logic_gate_xnor.h5')
    return pd.read_hdf(fpath)


def temperatures_daily_min():
    fpath = utils.load_data(
        _get_server() + "/temperatures_daily_min", 'temperatures_daily_min.h5')
    return pd.read_hdf(fpath)


def shampoo_sales():
    fpath = utils.load_data(
        _get_server() + "/shampoo_sales", 'shampoo_sales.h5')
    return pd.read_hdf(fpath)


def monthly_sunspot():
    fpath = utils.load_data(
        _get_server() + "/monthly_sunspot", 'monthly_sunspot.h5')
    return pd.read_hdf(fpath)


def daily_female_births():
    fpath = utils.load_data(
        _get_server() + "/daily_female_births", 'daily_female_births.h5')
    return pd.read_hdf(fpath)


def occupancy_detection():
    fpath = utils.load_data(
        _get_server() + "/occupancy_detection", 'occupancy_detection.h5')
    return pd.read_hdf(fpath)
