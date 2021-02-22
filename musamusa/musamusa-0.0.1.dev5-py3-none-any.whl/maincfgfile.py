# TODO
import musamusa.global_maincfgini
import musamusa.cfgini

def read(maincfgfile):
    """
        read()

        Read the configuration file and initialize nikw.cfgini.MAINCFGINI

        This function is what executes the --maincfgfile command line option.

        This function doesn't use a logger or rich text output.
        ________________________________________________________________________

        PARAMETER:  (str)maincfgfile : main configg file name

        RETURNED VALUE :
            (bool) success
    """
    (maincfgini_success,
     maincfgerrors,
     musamusa.global_maincfgini.MAINCFGINI) = musamusa.cfgini.read_main_cfg_file(maincfgfile)

    if not maincfgini_success:
        print("[ERRID005]  problem with the main config file '{maincfgfile}'; "
              "errors={maincfgerrors}".format(
                  maincfgfile=maincfgfile,
                  maincfgerrors=maincfgerrors))
        return False

    return True

