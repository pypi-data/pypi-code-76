"""This script does a simple simulation of two gravitational attractors and returns their trajectory,
   then does SBI using that model."""

import numpy as np
import matplotlib.pyplot as plt
from sbi.inference import infer
import sbi.utils as utils
import torch


class GravitySimulator:
    def __init__(self, m1, m2, v0, x0, G=1.90809e5, dt=1e-3, nsteps=20000):
        # only use one position/velocity, treat other body as origin --> do we need to correct for this?
        self.m1, self.m2, self.v0, self.x0, self.G, self.dt, self.nsteps = (
            np.array(m1),
            np.array(m2),
            np.array(v0),
            np.array(x0),
            G,
            dt,
            nsteps,
        )
        self.positions = np.zeros([self.nsteps, 2])
        self.positions[0] = self.x0
        # first step special case
        self.positions[1] = (
            self.x0 + self.v0 * self.dt + 0.5 * self.dt ** 2 * self.A(self.x0)
        )
        self.iter_idx = 2

    def rsquare(self, x):
        # square of distance between a point and origin
        return x[0] ** 2 + x[1] ** 2

    def A(self, x):
        # acceleration = Force/mass
        # F = G * m1 * m2 / r^2
        force = self.G * self.m1 * self.m2 / self.rsquare(x)
        # force is attractive, so multiply by unit vector toward origin
        force *= -1.0 * x / np.sqrt(np.sum(x ** 2))
        # compensate for one point always being at [0,0]
        return force / self.m2 - force / self.m1

    def run(self):
        while self.iter_idx < self.nsteps:
            self.step()
        return self.positions

    def step(self):
        # single step of integration with velocity verlet
        last_last_x = self.positions[self.iter_idx - 2]
        last_x = self.positions[self.iter_idx - 1]
        self.positions[self.iter_idx] = (
            2 * last_x - last_last_x + self.A(last_x) * self.dt ** 2
        )
        self.iter_idx += 1

    def plot_traj(self):
        plt.figure()
        plt.plot(self.positions[:, 0], self.positions[:, 1], lw=0.6)
        plt.savefig("trajectory.png")


m1 = 100.0  # solar masses
m2 = 50.0  # solar masses
G = 1.90809e5  # solar radius / solar mass * (km/s)^2
v0 = np.array([100.0, -70.0])  # km/s
x0 = np.array([50.0, 30.5])  # solar radii


def sim_wrapper(params_list):
    """params_list should be: m1, m2, v0[0], v0[1], x0[0], x0[1] in that order"""
    m1, m2 = float(params_list[0]), float(params_list[1])
    v0 = np.array([params_list[2], params_list[3]], dtype=np.float64)
    x0 = np.array([params_list[4], params_list[5]], dtype=np.float64)
    this_sim = GravitySimulator(m1, m2, v0, x0)
    this_traj = this_sim.run()
    summary_stats = torch.tensor(this_traj[::100])
    return summary_stats


prior_mins = [10.0, 10.0, -100.0, -100.0, 10.0, 10.0]
prior_maxes = [200.0, 200.0, 200.0, 200.0, 100.0, 100.0]

prior = utils.torchutils.BoxUniform(
    low=torch.as_tensor(prior_mins, dtype=torch.float64),
    high=torch.as_tensor(prior_maxes, dtype=torch.float64),
)

posterior = infer(sim_wrapper, prior, method="SNRE", num_simulations=40, num_workers=20)

# samples = posterior.sample((10000,), x=observation_summary_stats)

# fig, axes = utils.pairplot(samples)
