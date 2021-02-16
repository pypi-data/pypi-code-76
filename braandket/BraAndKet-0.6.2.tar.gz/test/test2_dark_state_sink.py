#%%

import numpy as np
import matplotlib.pyplot as plt
import bnk

#%% md

# Structure

#%% md

## Cavity Structure

#%%

class Cavity(bnk.HSpace):
    def __init__(self, n=4, name='cavity'):
        super().__init__(n, name)

        excite = 0
        for i in range(1, n):
            excite_i = self.eigenstate(i) @ self.eigenstate(i - 1).ct
            excite += np.sqrt(i) * excite_i
        relax = excite.ct

        self.excite = excite
        self.relax = relax

cavity1 = Cavity(3,'cavity1')
cavity2 = Cavity(3,'cavity2')
cavity3 = Cavity(3,'cavity3')


plt.subplot(1, 2, 1)
plt.matshow(cavity1.excite.flattened_values, 0)
plt.title("cavity1 excite")

plt.subplot(1, 2, 2)
plt.matshow(cavity1.relax.flattened_values, 0)
plt.title("cavity1 relax")

plt.show()

#%% md

## Sink Structure

#%%

sink = bnk.HSpace(3,'sink')

sink_excite = sink.eigenstate(1) @ sink.eigenstate(0).ct
sink_relax = sink_excite.ct


plt.subplot(1, 2, 1)
plt.matshow(sink_excite.flattened_values, 0)
plt.title("sink excite")

plt.subplot(1, 2, 2)
plt.matshow(sink_relax.flattened_values, 0)
plt.title("sink relax")

plt.show()

#%% md

# Evolution

#%% md

## Hamiltonian

#%%

hb = 1
w = 1
v12 = 0.2
v23 = 0.2

energy = (0
    + cavity1.excite @ cavity1.relax
    + cavity2.excite @ cavity2.relax
    + cavity3.excite @ cavity3.relax
    + sink_excite @ sink_relax
)

interaction12 = ( 0
    + cavity1.relax @ cavity2.excite
    + cavity1.excite @ cavity2.relax
)

interaction23 = ( 0
    + cavity2.relax @ cavity3.excite
    + cavity2.excite @ cavity3.relax
)

hamiltonian = hb * w * energy+ v12 * interaction12 + v23 * interaction23


plt.matshow(hamiltonian.flattened_values)
plt.title("hamiltonian")
plt.show()

#%% md

## Decoherence

#%%

gamma = 0.2

decoherence = sink_excite @ cavity2.relax


plt.matshow(decoherence.flattened_values)
plt.title("decoherence")
plt.show()

#%% md

# Iteration

#%% md

## Initial $\rho$

#%%

psi0 = \
    cavity1.eigenstate(1) @ \
    cavity2.eigenstate(0) @ \
    cavity3.eigenstate(0) @ \
    sink.eigenstate(0)

rho0 = psi0 @ psi0.ct


plt.matshow(rho0.flattened_values)
plt.title("$\\rho_0$")
plt.show()

#%% md

## Configurations

#%%

dt = 0.005
mt = 70

dlt = mt / 200

#%% md

## Iteration

#%%

logs_t = []
logs_probs = []

def log_func(t, rho):
    logs_t.append(t)

    rhos1 = rho.trace(cavity2, cavity3)
    rho23 = rho.trace(sink, cavity1)

    prob_sink = sink.eigenstate(1).ct @ rhos1.trace(cavity1) @ sink.eigenstate(1)
    prob_cavity1 = cavity1.eigenstate(1).ct @ rhos1.trace(sink) @ cavity1.eigenstate(1)
    prob_cavity2 = cavity2.eigenstate(1).ct @ rho23.trace(cavity3) @ cavity2.eigenstate(1)
    prob_cavity3 = cavity3.eigenstate(1).ct @ rho23.trace(cavity2) @ cavity3.eigenstate(1)

    probs = [prob_sink, prob_cavity1, prob_cavity2, prob_cavity3]
    probs = [prob.values for prob in probs]
    probs = np.abs(probs)
    logs_probs.append(probs)

#%%


bnk.lindblad_evolve(
    0.0, rho0, hamiltonian, decoherence, gamma, hb,
    mt, dt, dlt, log_func,
    reduce=False)

#%%

def plot_logs(logs_t, logs_probs):
    logs_probs = np.asarray(logs_probs)

    plt.plot(logs_t, logs_probs[:,0], label='sink')
    plt.plot(logs_t, logs_probs[:,1], label='cavity1')
    plt.plot(logs_t, logs_probs[:,2], label='cavity2')
    plt.plot(logs_t, logs_probs[:,3], label='cavity3')
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("prob")
    plt.show()

plot_logs(logs_t,logs_probs)

#%% md

# Reduction

#%%

reduced_space = bnk.ReducedKetSpace.from_initial(
    [rho0],[hamiltonian, decoherence],'reduced_system')

print([space.name for space in reduced_space.org_eigenstates[0].spaces])
for i, org_eigenstate in enumerate(reduced_space.org_eigenstates):
    code = list(np.transpose(np.where(org_eigenstate.values))[0])
    print(i, code)

#%% md

## Evolution (reduced)

#%%

reduced_rho0 = reduced_space.reduce(rho0)
reduced_hamiltonian = reduced_space.reduce(hamiltonian)
reduced_decoherence = reduced_space.reduce(decoherence)


plt.figure()
plt.matshow(reduced_rho0.flattened_values)
plt.title("reduced $\\rho_0$")

plt.figure()
plt.matshow(reduced_hamiltonian.flattened_values)
plt.title("reduced hamiltonian")

plt.show()

#%% md

## Iteration (reduced)

#%%

logs_t = []
logs_probs = []

def log_func_reduced(t, rho_reduced):
    log_func(t, reduced_space.inflate(rho_reduced))

#%%


bnk.lindblad_evolve(
    0.0, reduced_rho0, reduced_hamiltonian, reduced_decoherence, gamma, hb,
    mt, dt, dlt, log_func_reduced)

#%%

plot_logs(logs_t, logs_probs)

#%%


