from stdnum.gb import sedol
from stdnum import isin, cusip


def is_valid_cusip(idvalue):
    try:
        if len(idvalue) == 8:
            idvalue = idvalue + cusip.calc_check_digit(idvalue)
            is_valid = cusip.is_valid(idvalue)
        else:
            is_valid = cusip.is_valid(idvalue)
    except:
        is_valid = False
    return is_valid


def is_valid_sedol(idvalue):
    try:
        if len(idvalue) == 6:
            idvalue = idvalue + sedol.calc_check_digit(idvalue)
            is_valid = sedol.is_valid(idvalue)
        else:
            is_valid = sedol.is_valid(idvalue)
    except:
        is_valid = False
    return is_valid


def is_valid_isin(idvalue):
    try:
        if len(idvalue) == 11:
            idvalue = idvalue + isin.calc_check_digit(idvalue)
            is_valid = isin.is_valid(idvalue)
        else:
            is_valid = isin.is_valid(idvalue)
    except:
        is_valid = False
    return is_valid


def standardize_cusip(id_value):
    if cusip.is_valid(id_value):
        return id_value
    else:
        return id_value + cusip.calc_check_digit(id_value)


def standardize_sedol(id_value):
    if sedol.is_valid(id_value):
        return id_value
    else:
        return id_value + sedol.calc_check_digit(id_value)


def standardize_isin(id_value):
    if isin.is_valid(id_value):
        return id_value
    else:
        return id_value + isin.calc_check_digit(id_value)
