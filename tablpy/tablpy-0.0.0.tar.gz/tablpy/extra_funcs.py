import re
import os
import math
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


def delt(s):
    return r"\Delta" + str(s) if '\\' in str(s) else r"\Delta\!" + str(s)


def ax_name(tab, qty):
    s = f"${qty}$"
    if not str(tab.units[qty]) == '1':
        s += f" ( {tab.units[qty]} )"
    return s


def preSymp(str):
    str = str.replace("{", "__0__").replace("}", "__1__")
    pat = (r"\b(?!ln|log|sin|cos|tan|exp|atan|sqrt)\\?"
           r"[a-zA-Z]+[_0-9a-zA-Z({{)(}}),]*\b")
    a = [f"Symbol('{i}')" for i in re.findall(pat, str)]
    return re.sub(pat, r"{}", str).format(*a).replace("__0__", "{")\
                                             .replace("__1__", "}")


def roundUp(num):  # arrondis vers le haut à la bonne décimale
    pow = math.floor(sp.log(num, 10).evalf())  # Position de la décimla
    snum = str(num).replace(".", "")
    x = 0
    while snum[x] == "0":  # Trouve le premier chiffre non-nul
        x += 1
    # Revoie arrodis vers le haut
    if "0" * (len(snum) - x - 1) != snum[x + 1:] and x < len(snum):
        return ((int(snum[x]) + 1) * 10**sp.sympify(pow)).evalf(chop=True)
    else:
        return num  # pas de correction à faire!


# Détermine la formule d'incertitude pour une expression donnée
def formule_incertitude(eq):
    eq = sp.sympify(eq)
    variables = list(eq.free_symbols)  # liste de tout les variables
    # liste de touts les incertitudes asssociées au variables
    uncertain = [sp.Symbol(delt(x)) for x in variables]
    fIncert = sp.sqrt(sum(
        [(sp.diff(eq, variables[i]) * uncertain[i])**2
         for i in range(len(variables))]))
    return sp.simplify(fIncert)


def clearfile(file):
    for i in os.listdir(file):
        if os.path.isdir(file + "/" + i):
            clearfile(file + "/" + i)
            os.rmdir(file + "/" + i)
        else:
            os.remove(file + "/" + i)


def extrem(x):
    """return minimum, maximum of a list"""
    return float(min(x)), float(max(x))


def isUncertain(string):
    marqeurs = ['delta',
                'Delta',
                'Δ',
                'Î”']
    return any([marqeur in str(string) for marqeur in marqeurs])


def getTexIncert(x):
    print(sp.latex(formule_incertitude(x)))


def fastPlot(file):
    array = np.genfromtxt(file, skip_header=True, delimiter="\t")
    print(array)
    plt.plot(array[:, 0], array[:, 1])
