# TODO
import os.path
import configparser

from .utils import normpath


def read_cfg_file(filename):
    """
        read_cfg_file()

        Read the config file <filename>.

        This function doesn't use a logger or rich text output.
        _______________________________________________________________________

        PARAMETER : (str)filename

        RETURNED VALUE : (bool_success, (list of str)errors, configparser.ConfigParser object)
    """
    if not os.path.exists(filename):
        return (False,
                ["Where is config file '{filename}', namely '{filename2}' ?".format(
                    filename=filename,
                    filename2=normpath(filename))],
                None)

    success = True
    errors = []
    cfgini = configparser.ConfigParser()

    try:
        cfgini.read(filename)
    except configparser.DuplicateOptionError as err:
        success = False
        errors.append("[ERRID007] Ill-formed config file '{filename}' : duplicate key {err}".format(
            filename=filename,
            err=err))

    return success, errors, cfgini


def read_main_cfg_file(filename):
    """
        read_main_cfg_file()

        Read the config file <filename>.

        pimydoc:main config file format
        _______________________________________________________________________

        PARAMETER : (str)filename

        RETURNED VALUE : (bool_success, (list of str)errors, configparser.ConfigParser object)
    """
    success, errors, cfgini = read_cfg_file(filename)

    if success:
        # let's check the presence of some values :
        try:
            if cfgini["logging"].getboolean("authorize logging") is None:
                raise KeyError("[logging][authorize logging]")  # missing key.

        except KeyError as err:
            success = False
            errors.append("[ERRID001] Ill-formed config file '{filename}' : "
                          "missing key '{err}'.".format(
                              filename=filename,
                              err=err))

        except ValueError as err:
            success = False
            errors.append("[ERRID003] Ill-formed config file '{filename}' : "
                          "{err}".format(
                              filename=filename,
                              err=err))

    return success, errors, cfgini

