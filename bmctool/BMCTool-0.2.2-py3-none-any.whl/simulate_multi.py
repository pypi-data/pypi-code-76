"""
simulate_multi.py
    Script to run the BMCTool simulation based on a seq-file and a *.yaml config file.
"""
import numpy as np
from os import path
from pathlib import Path
from bmctool.bmc_tool import BMCTool
from bmctool.utils.eval import plot_z
from bmctool.set_params import load_params


def simulate_multi(config_file: (str, Path) = None, seq_file: (str, Path) = None):
    """
    Function to run the BMCTool simulation based on a seq-file and a *.yaml config file..
    :param config_file: Path of the config file (can be of type str or Path)
    :param seq_file: Path of the seq file (can be of type str or Path)
    """

    if config_file is None:
        config_file = Path(path.dirname(__file__)) / 'library' / 'sim-library' / 'config_wasabiti.yaml'

    if seq_file is None:
        # seq_file = Path(path.dirname(__file__)) / 'library' / 'WASABITI_3T_3p75uT_5ms_48rect_vary_trec_sim.seq'
        seq_file = Path(path.dirname(__file__)) / 'library' / 'seq-library' / 'WASABITI_sim.seq'

    # load config file(s)
    sim_params = load_params(config_file)

    # create BMCTool object and run simulation
    sim = BMCTool(sim_params, seq_file)

    # vary_vals = np.linspace(-0.3, 0.3, 7)  # dB0
    # vary_vals = np.linspace(0.7, 1.3, 7)  # rB1
    # vary_vals = np.linspace(0.05, 7, 3)  # T1
    # vary_vals = np.linspace(0.15, 20, 10)  # R1
    vary_vals = np.array([0.5, 1.0, 1.5, 2, 2.5, 3, 4])
    # vary_vals = np.linspace(0, 0.01, 21)  # f

    # vary_vals = np.array([-0.4, 0.0, 0.4])  # dB0
    # vary_vals = np.array([0.7, 1.0, 1.4])  # rB1
    # vary_vals = np.array([0.8, 1.3, 4.1]) # T1
    # vary_vals = np.array([0, 0.006, 0.01])  # f

    spec_list = []
    for val in vary_vals:
        # sim_params.update_scanner(b0_inhom=val)
        # sim_params.update_scanner(rel_b1=val)
        sim_params.update_water_pool(r1=1/val)
        # sim_params.update_cest_pool(0, f=val)
        sim.params = sim_params
        sim.run()

        # extract and plot z-spectrum
        offsets, mz = sim.get_zspec(return_abs=True)
        spec_list.append(mz[1:])

    return offsets[1:], spec_list, vary_vals


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    offsets, specs, vals = simulate_multi()

    for i, spec in enumerate(specs):
        plt.plot(offsets, spec, marker='o', linestyle='--', label=f'T1 = {vals[i]:.1f} s')
    plt.title(f'T1')
    plt.xlabel('frequency offset [ppm]')
    plt.ylabel('normalized signal')
    plt.legend()
    plt.show()

