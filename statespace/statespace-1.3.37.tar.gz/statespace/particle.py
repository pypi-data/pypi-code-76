# monte carlo sampling processor, bootstrap particle filter
import numpy as np
import math
from decisions import Innovs, Dists, DistsEns
import statespacemodels

def resample(xi, Wi):
    tmp = []
    for i in range(xi.size):
        tmp.append([xi[i], Wi[i]])
    tmp = sorted(tmp, key=lambda x: x[0])
    cdf = [[tmp[0][0], tmp[0][1]]]
    for i in range(1, len(tmp)):
        cdf.append([tmp[i][0], tmp[i][1] + cdf[i - 1][1]])
    cdf = np.asarray(cdf)
    uk = np.sort(np.random.uniform(size=xi.size))
    xhati, k = [], 0
    for row in cdf:
        while k < uk.size and uk[k] <= row[1]:
            xhati.append(row[0])
            k += 1
    xhati = np.asarray(xhati)
    assert xhati.size == xi.size
    return xhati

class Particle():
    def __init__(self, mode, innovs=False, dists=False):
        self.innovs = Innovs()
        self.dists = Dists()
        self.ens = DistsEns()
        if mode == 'test':
            for i in range(100):
                m = statespacemodels.Jazwinski1()
                self.pf1(m)
                self.ens.update(distslog=self.dists.log)
            self.ens.plot()
        if mode == 'pf1':
            m = statespacemodels.Jazwinski1()
            self.pf1(m)
            if dists: self.dists.plot()
        if mode == 'pf2':
            m = statespacemodels.Jazwinski2()
            self.pf2(m)
        if innovs: self.innovs.plot()

    def pf1(self, m):
        xhat = 2.05
        x = xhat + math.sqrt(1e-2) * np.random.randn(m.nsamp)
        W = normalize(np.ones(m.nsamp))
        for step in m.steps():
            x = resample(x, W)
            x = m.Apf(x)
            W = normalize(m.Cpf(step[2], x))
            yhat = m.c(xhat, 0)
            xhat = W @ x
            self.innovs.update(t=step[0], xhat=xhat, yhat=yhat, err=step[1] - xhat, inn=step[2] - yhat)
            self.dists.update(t=step[0], tru=m.Apf(step[1]), est=x)

    def pf2(self, m):
        xhat = np.array([2.0, .055, .044])
        x = xhat + np.sqrt(m.Rww) * np.random.randn(m.nsamp, 3)
        W = np.ones((m.nsamp, 3)) / m.nsamp
        for step in m.steps():
            x[:, 0], x[:, 1], x[:, 2] = resample(x[:, 0], W[:, 0]), roughen(x[:, 1]), roughen(x[:, 2])
            x[:, 0] = np.apply_along_axis(m.Apf, 1, x)
            W[:, 0] = normalize(m.Cpf(step[2], x[:, 0]))
            yhat = m.c(xhat, 0)
            xhat = [W[:, 0].T @ x[:, 0], W[:, 1].T @ x[:, 1], W[:, 2].T @ x[:, 2]]
            self.innovs.update(t=step[0], xhat=xhat[0], yhat=yhat, err=step[1][0] - xhat[0], inn=step[2] - yhat)

def roughen(x):
    return x + .1 * np.random.randn(x.size)

def normalize(W):
    return W / sum(W)

if __name__ == "__main__":
    Particle('test')
    # Particle('pf1', dists=1, innovs=0)
    # Particle('pf2', innovs=1)
