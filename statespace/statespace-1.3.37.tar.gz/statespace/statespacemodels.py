import math
import numpy as np
import matplotlib.pyplot as plt

class Rccircuit():

    def __init__(self, signal):
        self.u = signal * 1e-6 # amps step-function input
        self.tsteps = 301
        self.dt = .1
        self.x = 2.5 + math.sqrt(1e-6) * np.random.randn()
        self.Rww = 1e-5
        self.Rvv = 4
        self.log = []
        v = math.sqrt(self.Rvv) * np.random.randn()
        self.y = 2 * self.x + v
        self.log.append([0, self.x, self.y])

    def steps(self):
        for tstep in range(1, self.tsteps):
            tsec = tstep * self.dt
            w = math.sqrt(self.Rww) * np.random.randn()
            v = math.sqrt(self.Rvv) * np.random.randn()
            self.x = .97 * self.x + 100 * self.u + w
            self.y = 2 * self.x + v
            self.log.append([tsec, self.x, self.y])
            yield (tsec, self.x, self.y)

    def plot(self):
        log = np.asarray(self.log)
        lw = 1
        plt.figure()
        plt.subplot(2, 1, 1), plt.plot(log[:, 0], log[:, 1], linewidth=lw), plt.ylabel('x')
        plt.subplot(2, 1, 2), plt.plot(log[:, 0], log[:, 2], linewidth=lw), plt.ylabel('y')

class Jazwinski1():
    def __init__(self):
        self.tsteps = 151
        self.dt = .01
        self.x = 2.
        self.Rww = 1e-6
        self.Rvv = 9e-2
        self.log = []
        self.va = np.vectorize(self.a)
        self.vc = np.vectorize(self.c)
        bignsubx = 1
        kappa = 1
        k0 = bignsubx + kappa
        k1 = kappa / float(k0)
        k2 = 1 / float(2 * k0)
        self.nsamp = 250
        self.W = np.array([k1, k2, k2])
        self.k0 = k0
        self.kappa = kappa

    def a(self, x, w=0):
        return (1 - .05 * self.dt) * x + (.04 * self.dt) * x ** 2 + w

    def c(self, x, v=0):
        return x ** 2 + x ** 3 + v

    def A(self, x):
        return 1 - .05 * self.dt + .08 * self.dt * x

    def C(self, x):
        return 2 * x + 3 * x ** 2

    def X(self, xhat, Ptil):
        return [xhat, xhat + math.sqrt(self.k0 * Ptil), xhat - math.sqrt(self.k0 * Ptil)]

    def Xhat(self, X, Rww):
        return [X[0], X[1] + self.kappa * math.sqrt(Rww), X[2] - self.kappa * math.sqrt(Rww)]

    def Apf(self, x):
        return (1 - .05 * self.dt) * x + (.04 * self.dt) * x ** 2 + math.sqrt(self.Rww) * np.random.randn(self.nsamp)

    def Cpf(self, y, x):
        return np.exp(-np.log(2. * np.pi * self.Rvv) / 2. - (y - x ** 2 - x ** 3) ** 2 / (2. * self.Rvv))

    def steps(self):
        for tstep in range(self.tsteps):
            tsec = tstep * self.dt
            w = math.sqrt(self.Rww) * np.random.randn()
            v = math.sqrt(self.Rvv) * np.random.randn()
            self.x = self.a(self.x, w)
            self.y = self.c(self.x, v)
            if tstep == 0: continue
            self.log.append([tsec, self.x, self.y])
            yield (tsec, self.x, self.y)


class Jazwinski2():
    def __init__(self):
        self.tsteps = 1501
        self.dt = .01
        self.x = np.array([2., .05, .04])
        self.Rww = 1e-9 * np.array([1, 1, 1])
        self.Rvv = 9e-2
        self.Sw = np.linalg.cholesky(np.diag(self.Rww))
        self.Sv = np.linalg.cholesky(np.diag(self.Rvv * np.array([1])))
        self.log = []
        self.nsamp = 250
        n = 3
        kappa = 1
        alpha = 1
        beta = 2
        lam = alpha ** 2 * (n + kappa) - n
        wi = 1 / float(2 * (n + lam))
        w0m = lam / float(n + lam)
        w0c = lam / float(n + lam) + (1 - alpha ** 2 + beta)
        self.Wm = np.array([w0m, wi, wi, wi, wi, wi, wi])
        self.Wc = np.array([w0c, wi, wi, wi, wi, wi, wi])
        self.nlroot = math.sqrt(n + lam)
        self.Xtil = np.zeros((3, 7))
        self.Ytil = np.zeros((1, 7))
        self.Pxy = np.zeros((3, 1))
        self.G = np.eye(3)
        self.Q = np.diag(self.Rww)

    def a(self, x, w=0):
        return np.array([(1 - x[1] * self.dt) * x[0] + x[2] * self.dt * x[0] ** 2, x[1], x[2]]) + w

    def c(self, x, v=0):
        return x[0] ** 2 + x[0] ** 3 + v

    def A(self, x):
        A = np.eye(3)
        A[0, 0] = 1 - x[1] * self.dt + 2 * x[2] * self.dt * x[0]
        A[0, 1] = -self.dt * x[0]
        A[0, 2] = self.dt * x[0] ** 2
        return A

    def C(self, x):
        return np.array([2 * x[0] + 3 * x[0] ** 2, 0, 0])

    def X(self, x, C):
        X = np.zeros([3, 7])
        X[:, 0] = x
        X[:, 1] = x + self.nlroot * C.T[:, 0]
        X[:, 2] = x + self.nlroot * C.T[:, 1]
        X[:, 3] = x + self.nlroot * C.T[:, 2]
        X[:, 4] = x - self.nlroot * C.T[:, 0]
        X[:, 5] = x - self.nlroot * C.T[:, 1]
        X[:, 6] = x - self.nlroot * C.T[:, 2]
        return X

    def Xhat(self, X):
        Xhat = np.zeros([3, 7])
        Xhat[:, 0] = X[:, 0]
        Xhat[:, 1] = X[:, 1] + self.nlroot * self.Sw.T[:, 0]
        Xhat[:, 2] = X[:, 2] + self.nlroot * self.Sw.T[:, 1]
        Xhat[:, 3] = X[:, 3] + self.nlroot * self.Sw.T[:, 2]
        Xhat[:, 4] = X[:, 4] - self.nlroot * self.Sw.T[:, 0]
        Xhat[:, 5] = X[:, 5] - self.nlroot * self.Sw.T[:, 1]
        Xhat[:, 6] = X[:, 6] - self.nlroot * self.Sw.T[:, 2]
        return Xhat

    def va(self, X):
        for i in range(7): X[:, i] = self.a(X[:, i], 0)
        return X

    def vc(self, Xhat):
        Y = np.zeros(7)
        for i in range(7): Y[i] = self.c(Xhat[:, i], 0)
        return Y

    def Xtil(self, X, W):
        Xtil = np.zeros((3, 7))
        for i in range(7): Xtil[:, i] = X[:, i] - W @ X.T
        return Xtil

    def ksi(self, Y, W):
        ksi = np.zeros((1, 7))
        for i in range(7): ksi[0, i] = Y[i] - W @ Y.T
        return ksi

    def Apf(self, x):
        return (1 - x[1] * self.dt) * x[0] + x[2] * self.dt * x[0] ** 2

    def Cpf(self, y, x):
        return np.exp(-np.log(2. * np.pi * self.Rvv) / 2. - (y - x ** 2 - x ** 3) ** 2 / (2. * self.Rvv))

    def steps(self):
        for tstep in range(self.tsteps):
            tsec = tstep * self.dt
            w = np.multiply(np.random.randn(1, 3), np.sqrt(np.diag(self.Rww)))
            v = math.sqrt(self.Rvv) * np.random.randn()
            self.x = self.a(self.x, w[0])
            self.y = self.c(self.x, v)
            if tstep == 0: continue
            self.log.append([tsec, self.x, self.y])
            yield (tsec, self.x, self.y)

class ModelsEns():
    def __init__(self, title):
        self.title = title
        self.runs = []

    def runningmean(self, x, n):
        ypadded = np.pad(x, (n // 2, n - 1 - n // 2), mode='edge')
        return np.convolve(ypadded, np.ones((n,)) / n, mode='valid')

    def finalize(self):
        self.ensx = []
        self.ensy = []
        for log in self.runs:
            log = np.asarray(log)
            self.ensx.append(log[:, 1])
            self.ensy.append(log[:, 2])
        self.ensx = np.asarray(self.ensx)
        self.ensy = np.asarray(self.ensy)
        self.ensxmean = self.runningmean(np.mean(self.ensx, axis=0), 20)
        self.ensymean = self.runningmean(np.mean(self.ensy, axis=0), 20)
        self.ensxstd = self.runningmean(np.std(self.ensx, axis=0), 20)
        self.ensystd = self.runningmean(np.std(self.ensy, axis=0), 20)
        pass

    def plot(self):
        self.finalize()
        lw = 1
        plt.figure()
        plt.subplot(2, 1, 1)
        for log in self.runs:
            log = np.asarray(log)
            plt.plot(log[:, 0], log[:, 1], linewidth=lw, color='g', alpha=.25)
            plt.plot(log[:, 0], self.ensxmean, linewidth=lw, color='b', alpha=.1)
            plt.plot(log[:, 0], self.ensxmean + 1.96 * self.ensxstd, linewidth=lw, color='b', alpha=.05)
            plt.plot(log[:, 0], self.ensxmean - 1.96 * self.ensxstd, linewidth=lw, color='b', alpha=.05)
            plt.ylabel('x')
            if self.title: plt.title(self.title)
        plt.subplot(2, 1, 2)
        for log in self.runs:
            log = np.asarray(log)
            plt.plot(log[:, 0], log[:, 2], linewidth=lw, color='g', alpha=.25)
            plt.plot(log[:, 0], self.ensymean, linewidth=lw, color='b', alpha=.1)
            plt.plot(log[:, 0], self.ensymean + 1.96 * self.ensystd, linewidth=lw, color='b', alpha=.05)
            plt.plot(log[:, 0], self.ensymean - 1.96 * self.ensystd, linewidth=lw, color='b', alpha=.05)
            plt.ylabel('y')

def rccircuit(runs, signal, title=None):
    ens = ModelsEns(title)
    for runndx in range(runs):
        sim = Rccircuit(signal)
        for step in sim.steps(): continue
        ens.runs.append(sim.log)
    return ens

if __name__ == "__main__":
    enssig = rccircuit(runs=10, signal=300., title='signal')
    ensnoise = rccircuit(runs=10, signal=0., title='noise')
    enssig.plot()
    ensnoise.plot()
    plt.show()
