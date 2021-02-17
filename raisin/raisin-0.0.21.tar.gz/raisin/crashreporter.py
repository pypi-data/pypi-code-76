#!/usr/bin/env python3

"""
En cas de plantage de raisin,
Les erreurs sont recuperes et envoyees
par couriel. Ainsi, les developeurs peuvent corriger
des erreurs de raisin.
"""


import os
import re
import sys
import time


def crash_report(exc_type, value, traceback):
    """
    Il faut uiliser cet objet de la facon suivante:
    sys.excepthook = crash_report
    """
    def get_filenames(traceback):
        """
        Recherche recursivement les fichiers concernes par l'incident.
        """
        if traceback:
            return list(set(
                [os.path.abspath(traceback.tb_frame.f_code.co_filename)] + 
                get_filenames(traceback.tb_next)))
        return []

    def get_raisin_filenames():
        """
        Genere tous les fichiers qui constituent le module raisin.
        """
        for father, dirs, files in os.walk(os.path.dirname(raisin.__file__)):
            for file in files:
                yield os.path.join(father, file)

    def is_time():
        """
        Retourne True si cette fonction a ete appellee
        il y a plus d'une heure. Retourne False si un 
        rapport de plantage a deja ete envoye recement.
        """
        racine = os.path.join(os.path.expanduser("~"), ".raisin")
        if not os.path.exists(racine): # Si raisin n'est pas installe
            sys.stderr.write("This crash report is not sent to the "
                "debauging service because 'raisin' is not installed.\n"
                "To install raisin, type: '%s -m raisin install'\n" % sys.executable)
            return False
        filename = os.path.join(racine, "last_crash.txt")
        t = 0
        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    t = time.mktime(time.strptime(f.read(), "%Y-%m-%dT%H:%M:%S\n"))
                except ValueError:
                    t = 0

        if time.time() - t > 3600:
            with open(filename, "w") as f:
                f.write(time.strftime("%Y-%m-%dT%H:%M:%S\n")) # Representation iso 8601 de la date et de l'heure.
            return True
        return False

    import raisin
    import raisin.tools
    import raisin.communication.mail as mail
    import raisin.errors as errors

    sys.stderr.write("Uh... I planted! I am dead!\n")

    if is_time() and not issubclass(exc_type, (KeyboardInterrupt, EOFError, errors.DecryptError)):
        filenames = get_filenames(traceback)            # recuperation de tous les fichiers qui contribuent au plantage
        if set(filenames) & set(get_raisin_filenames()):# si raisin est concerne par ce plantage
            ancien_stderr = sys.stderr
            with open(os.path.join(raisin.tools.temprep, "erreur.txt"), "w") as f:
                sys.stderr = f
                sys.__excepthook__(exc_type, value, traceback)
            sys.stderr = ancien_stderr
            with open(os.path.join(raisin.tools.temprep, "erreur.txt"), "r") as f:
                traceback_txt = f.read()
            sys.stderr.write(traceback_txt)
            os.remove(os.path.join(raisin.tools.temprep, "erreur.txt"))

            with raisin.tools.Printer("Envoi du rapport de plantage..."):
                message = "type : %s\nvalue: %s\n\n%s\n\n%s" % (
                    exc_type.__name__,
                    "       \n".join(map(str, value.args)),
                    raisin.tools.identity, traceback_txt)
                adresse = re.search(r"[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]{2,}\.[a-z]{2,4}", raisin.__author__).group() # recuperation de l'adresse du createur
                mail.send(adresse, "raisin: crash report", message, attachment=get_filenames(traceback))
        else:
            sys.__excepthook__(exc_type, value, traceback)
    else:
        sys.__excepthook__(exc_type, value, traceback)
