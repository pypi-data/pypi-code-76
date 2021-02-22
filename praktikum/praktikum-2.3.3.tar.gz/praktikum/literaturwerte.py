# -*- coding: utf-8 -*-

"""
Dieses Modul enthält Literaturwerte bzw. Herstellerangaben, die bei der Auswertung im
Grundpraktikum Physik nützlich, aber nicht einfach anders zugänglich sind.
"""

from numpy import exp,sqrt

def saettigungsdampfdruck_wasser(t):
    '''
    Näherungsformel nach Magnus für den Sättigungsdampfdruck über einer Wasseroberfläche

    :param t: Temperatur in °C
    :type t: float

    Quelle: https://de.wikipedia.org/wiki/S%C3%A4ttigungsdampfdruck (abgerufen am 4.7.2019)
    
    :rtype: Sättigungsdampfdruck in mbar (bzw. hPa)
    '''
    # in mbar=hPa
    return 6.112 * exp(17.62*t / (243.12 + t))


def molare_masse_luft(phi, p, t):
    '''
    Berechung der molaren Masse von (feuchter) Luft

    :param phi: relative Luftfeuchtigkeit
    :type phi: float

    :param p: Luftdruck in mbar
    :type p: float

    :param t: Temperatur in °C
    :type t: float

    :rtype: Molare Masse der feuchten Luft in g/mol.
    '''

    if phi < 0. or phi > 1.:
        raise ValueError('Luftfeuchtigkeit muss im Intervall [0,1] liegen!')

    ML = 28.949 # molare Masse von Luft (g/mol)
    MW = 18.  # molare Masse von Wasser (g/mol)

    pS = saettigungsdampfdruck_wasser(t)

    M = phi*(pS/p)*MW + (1.-phi*pS/p)*ML
    return M


def dichte_luft(phi, p, t):
    '''
    Berechung der Dichte von (feuchter) Luft

    :param phi: relative Luftfeuchtigkeit
    :type phi: float

    :param p: Luftdruck in mbar
    :type p: float

    :param t: Temperatur in °C
    :type t: float

    :rtype: Dichte der feuchten Luft in :math:`kg/m^3`.
    '''

    if phi < 0. or phi > 1.:
        raise ValueError('Luftfeuchtigkeit muss im Intervall [0,1] liegen!')

    T = t + 273.15

    RL = 287.058 # J/(kg K)
    RW = 461.523
    pS = saettigungsdampfdruck_wasser(t)
    Rf = RL / (1. - phi*(pS/p) * (1. - RL/RW))

    rho = p / (Rf*T) * 1.e2  # mbar -> SI-standard
    return rho


def brechungsindex_luft(lambd, t=20.0, p=1013.25, e=13.33):
    '''
    Berechnung des Brechungsindex von Luft

    :param lambd: Vakuumwellenlänge der Lichtquelle in :math:`\mu{}m`
    :param t:     Temperatur in °C
    :param p:     Luftdruck in mbar
    :param e:     Wasserdampfpartialdruck (Feuchtigkeit) in mbar

    Quelle: Kohlrausch, Praktische Physik, 23. Auflage, Band 1, S. 461

    Die Formel gilt in guter Näherung im Temperaturbereich von 15 bis 30 °C und im
    Druckbereich von 933 bis 1067 mbar, außerdem für ein CO2-Volumengehalt von 0,03%.
    
    Mit der Formel lassen sich nicht die im Kohlrausch angegebenen beispielhaften Werte
    für einzelne Wellenlängen reproduzieren. Gleichwohl stimmen die Werte für trockene
    Luft mit denen überein, die sich nach dem CRC Handbook (78. Auflage, S. 10-259)
    berechnen lassen (das CRC Handbook gibt keine Formel für feuchte Luft an).

    :rtype: Brechungsindex der Luft
    '''
    
    cA = 8.34213e-5
    cB = 2.40603e-2 # um^-2
    cC = 130. # um^-2
    cD = 1.5997e-4 # um^-2
    cE = 38.9 # um^-2

    sigma2 = 1.0/(lambd**2)
    
    nLNm1 = cA + cB/(cC - sigma2) + cD/(cE - sigma2)

    cAlpha = 3.671e-3 # degC^-1
    cBeta = 4.292e-8 # mbar^-1
    cGamma = 3.43e-8 # um^2 mbar^-1

    t0 = 15.0 # degC
    p0 = 1013.25 # mbar
    
    nLm1 = nLNm1 * (1.0 + cAlpha*t0) / (1.0 + cAlpha*t) * (p/p0) - (cBeta - cGamma*sigma2) * e

    return 1.0 + nLm1

def n_dryair(lambd, t=20.0, p=1013.25):

    # CRC Handbook (78th ed, p. 10-259)
    
    sigma2 = 1.0/(lambd**2)
    nm1 = 1.e-8 * (8342.13 + 2406030./(130-sigma2) + 15997./(38.9-sigma2))

    pPascal = 100.*p
    
    corr = pPascal * (1. + pPascal*(61.3-t)*1.e-10) / (96095.4 * (1.0 + 0.003661*t))
    
    return 1.0 + nm1*corr


def n_schott_f2(lambd):
    '''
    Formel für den Brechungsindex des Schott-Glases F2 (Flintglas)

    Quelle: https://www.schott.com/d/advanced_optics/47d79895-2965-472d-83ed-af9e48ac72c0/1.1/schott-optisches-glas-datenblatt-sammlung-german-17012017.pdf

    :param lambd: Vakuumwellenlänge der Lichtquelle in :math:`\mu{}m`

    :rtype: Brechungsindex bei der gegebenen Wellenlänge.
    '''

    B1 = 1.34533359
    B2 = 0.209073176
    B3 = 0.937357162
    C1 = 0.00997743871
    C2 = 0.0470450767
    C3 = 111.8867640

    l2 = lambd**2

    nsqrm1 = B1*l2/(l2-C1) + B2*l2/(l2-C2) + B3*l2/(l2-C3)
    return sqrt(1.0 + nsqrm1)


def n_schott_nsf10(lambd):
    '''
    Formel für den Brechungsindex des Schott-Glases N-SF10 (Schwerflintglas)

    Quelle: https://www.schott.com/d/advanced_optics/47d79895-2965-472d-83ed-af9e48ac72c0/1.1/schott-optisches-glas-datenblatt-sammlung-german-17012017.pdf

    :param lambd: Vakuumwellenlänge der Lichtquelle in :math:`\mu{}m`

    :rtype: Brechungsindex bei der gegebenen Wellenlänge.
    '''

    B1 = 1.62153902
    B2 = 0.256287842
    B3 = 1.644475520
    C1 = 0.01222414570
    C2 = 0.0595736775
    C3 = 147.4687930

    l2 = lambd**2

    nsqrm1 = B1*l2/(l2-C1) + B2*l2/(l2-C2) + B3*l2/(l2-C3)
    return sqrt(1.0 + nsqrm1)


def schallgeschwindigkeit_luft(T):
    '''
    Näherungsformel für die Schallgeschwindigkeit in Luft

    Quelle: Wikipedia, https://de.wikipedia.org/wiki/Schallgeschwindigkeit

    :param T: Temperatur in Kelvin

    :rtype: Schallgeschwindigkeit in m/s.
    '''

    return sqrt(1.402 * 8.3145 * T / 0.02896)


if __name__ == '__main__':

    import numpy as np
    import matplotlib.pyplot as plt

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['figure.titleweight'] = 'bold'
    plt.rcParams['axes.labelsize'] = 'large'
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.formatter.useoffset'] = 'False'
    
    pnorm = 1013.25
    tnorm = 22.0
    hnorm = 0.5
    enorm = hnorm * saettigungsdampfdruck_wasser(tnorm)
    lambdnorm = 0.632
    nnorm = brechungsindex_luft(lambd=lambdnorm, t=tnorm, p=pnorm, e=enorm)
    nmin = nnorm - 0.000011
    nmax = nnorm + 0.00001
    
    #print('H20 Partialdruck = %.3f mbar' % enorm)
    ylabel = '$n_\mathrm{Luft}$'
    
    fig, ax = plt.subplots(2, 2, figsize=(20,10))
    lambdas = np.arange(400., 800., 5.)
    ax[0][0].plot(lambdas, brechungsindex_luft(lambdas/1000., t=tnorm, p=pnorm, e=enorm), 'b-')
    ax[0][0].set_title(u'Abhängigkeit von der Wellenlänge', fontweight='bold')
    ax[0][0].set_xlabel('$\lambda$ (nm)')
    ax[0][0].set_ylabel(ylabel)
    ax[0][0].set_ylim(nmin, nmax)

    ts = np.arange(19., 25., 0.1)
    ax[0][1].plot(ts, brechungsindex_luft(lambdnorm, t=ts, p=pnorm, e=enorm), 'b-')
    ax[0][1].set_title(u'Temperaturabhängigkeit', fontweight='bold')
    ax[0][1].set_xlabel(u'$t$ (°C)')
    ax[0][1].set_ylabel(ylabel)
    ax[0][1].set_ylim(nmin, nmax)

    ps = np.arange(980., 1040., 1.)
    ax[1][0].plot(ps, brechungsindex_luft(lambdnorm, t=tnorm, p=ps, e=enorm), 'b-')
    ax[1][0].set_title(u'Druckabhängigkeit', fontweight='bold')
    ax[1][0].set_xlabel('$P$ (mbar)')
    ax[1][0].set_ylabel(ylabel)
    ax[1][0].set_ylim(nmin, nmax)

    hs = np.arange(0., 100.1, 2.)
    es = saettigungsdampfdruck_wasser(tnorm) * hs/100.
    ax[1][1].plot(hs, brechungsindex_luft(lambdnorm, t=tnorm, p=pnorm, e=es), 'b-')
    ax[1][1].set_title(u'Abhängigkeit von der Luftfeuchtigkeit', fontweight='bold')
    ax[1][1].set_xlabel('rel. Luftfeuchte (%)')
    ax[1][1].set_ylabel(ylabel)
    ax[1][1].set_xlim(0., 100.)
    ax[1][1].set_ylim(nmin, nmax)
    
    plt.tight_layout()
    plt.show()
