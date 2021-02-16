# %%

import numpy as np
import matplotlib.pyplot as plt
import bnk

# %% md

# Structure

# %% md

## Atom Structure

# %%

atom = bnk.HSpace(2, name='atom')

atom_excite = atom.eigenstate(1) @ atom.eigenstate(0).ct
atom_relax = atom_excite.ct

# plt.subplot(1, 2, 1)
# plt.matshow(atom_excite.flattened_values, 0)
# plt.title("atom excite")
#
# plt.subplot(1, 2, 2)
# plt.matshow(atom_relax.flattened_values, 0)
# plt.title("atom relax")
#
# plt.show()

# %% md

## Field Structure

# %%

field = bnk.HSpace(4, name='field')

field_excite = bnk.zero
for i in range(1, field.n):
    field_excite_i = field.eigenstate(i) @ field.eigenstate(i - 1).ct
    field_excite += np.sqrt(i) * field_excite_i
field_relax = field_excite.ct

# plt.subplot(1, 2, 1)
# plt.matshow(field_excite.flattened_values, 0)
# plt.title("field excite")
#
# plt.subplot(1, 2, 2)
# plt.matshow(field_relax.flattened_values, 0)
# plt.title("field relax")

plt.show()

# %% md

# Evolution

# %% md

## Hamiltonian

# %%

hb = 1
w = 1
g = 1

interaction = g * bnk.sum(
    atom_relax @ field_excite,
    atom_excite @ field_relax,
    atom_excite @ field_excite,
    atom_relax @ field_relax,
)

energy = hb * w * bnk.sum(
    atom_excite @ atom_relax,
    field_excite @ field_relax,
)

hamiltonian = energy + interaction

# plt.matshow(hamiltonian.flattened_values)
# plt.title("hamiltonian")
# plt.show()

# %% md

# Iteration

# %% md

## Initial $\psi$

# %%

psi0 = atom.eigenstate(0) @ field.eigenstate(1)

print('psi0')
print(psi0.values)

# %% md

## Configurations

# %%

mt = 100


# %% md

## Iteration

# %%


def log_func(t, psi):
    probs = np.abs(np.conj(psi.values) * psi.values)

    logs_t.append(t)
    logs_probs.append(probs)


# %%

logs_t = []
logs_probs = []


def compute(method, dt):
    dlt = 0.5

    logs_t = []
    logs_probs = []

    t = 0.0
    psi = psi0

    t, psi = bnk.schrodinger_evolve(
        t, psi, hamiltonian, hb,
        mt, dt, dlt, log_func,
        method=method, verbose=False)

    logs_probs = np.asarray(logs_probs)
    return logs_probs


pade_probs = compute('pade', None)

for method in ['euler', 'rk4']:
    dlt = 0.5
    for dt in [0.1, 1e-3, 1e-5]:
        probs = compute(method, dt)
        error = np.sum(pade_probs - probs)

        print(f"{method}\tdt={dt}\terror={error}")
