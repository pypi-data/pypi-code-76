#! /usr/bin/env python3

from praktikum import analyse
import numpy as np
import ROOT

sigmay = 0.2
xmin =  -10.
xmax =  10.

a_true = 0.5
b_true = 0.1
c_true = -5.0

hPullA = ROOT.TH1F('hPullA','pull distribution for a', 100, -4., 4.)
hPullB = ROOT.TH1F('hPullB','pull distribution for b', 100, -4., 4.)
hPullC = ROOT.TH1F('hPullC','pull distribution for c', 100, -4., 4.)
hCorrAB = ROOT.TH1F('hCorrAB','distribution of #rho_{ab}', 100, -1., 1.)
hCorrAC = ROOT.TH1F('hCorrAC','distribution of #rho_{ac}', 100, -1., 1.)
hCorrBC = ROOT.TH1F('hCorrBC','distribution of #rho_{bc}', 100, -1., 1.)

ROOT.gStyle.SetOptFit(11)

for i in range(1000):

    # wuerfele Daten
    x = np.arange(xmin, xmax)
    ydata = np.random.normal(a_true*x**2 + b_true*x + c_true, sigmay)
    ey = 0.*x + sigmay

    # Aufruf der quadratischen Regression
    a, ea, b, eb, c, ec, chiq, corr = \
        analyse.quadratische_regression(x, ydata, ey)
    print('Ergebnis: a=%f+-%f, b=%f+-%f, c=%f+-%f, chi2=%f, corr=%s' % (a,ea,b,eb,c,ec,chiq,corr))

    if i == 999:
        print(x)
        print(ydata)
        print(a, ea, b, eb, c, ec, chiq, corr)

    pullA = (a-a_true)/ea
    pullB = (b-b_true)/eb
    pullC = (c-c_true)/ec
    hPullA.Fill(pullA)
    hPullB.Fill(pullB)
    hPullC.Fill(pullC)
    hCorrAB.Fill(corr[0])
    hCorrAC.Fill(corr[1])
    hCorrBC.Fill(corr[2])

canv = ROOT.TCanvas('cQuadr','pulls and correlations', 1600, 1200)
canv.Divide(3,2)
canv.cd(1)
hPullA.Draw()
hPullA.Fit('gaus','L')
canv.cd(2)
hPullB.Draw()
hPullB.Fit('gaus','L')
canv.cd(3)
hPullC.Draw()
hPullC.Fit('gaus','L')

canv.cd(4)
hCorrAB.Draw()
canv.cd(5)
hCorrBC.Draw()
canv.cd(6)
hCorrAC.Draw()

canv.Update()

input()
