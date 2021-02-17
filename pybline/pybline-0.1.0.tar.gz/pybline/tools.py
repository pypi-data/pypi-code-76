# -*- coding: utf-8 -*-

import pathlib

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.gridspec as gridspec

from scipy.integrate import cumtrapz

from . import GRAV


def plot_timeseries_spectra(matched, seed=None, target=None):
    osc_freqs = np.logspace(-1, 2, num=301)
    osc_damping = 0.05

    m_vels, m_disps = matched.integrate()

    if seed:
        seed.accels *= matched.pga / seed.pga
        s_vels, s_disps = seed.integrate()

    fig = plt.figure(figsize=(6, 8), constrained_layout=False)
    gs = gridspec.GridSpec(2, 1, height_ratios=(3, 2))

    gs_top = gridspec.GridSpecFromSubplotSpec(4, 1, gs[0, 0], hspace=0.05)
    gs_bot = gridspec.GridSpecFromSubplotSpec(1, 2, gs[1, 0], wspace=0.30)

    ax1 = plt.subplot(gs_top[0, 0])
    ax1.axhline(0, color='black', lw=0.5)
    if seed:
        ax1.plot(seed.times, seed.accels, label='Seed', lw=0.8)
    ax1.plot(matched.times, matched.accels, label='Matched')
    ax1.set(ylabel='Acc. (g)', xticklabels=[])

    ax2 = plt.subplot(gs_top[1, 0])
    ax2.axhline(0, color='black', lw=0.5)
    if seed:
        ax2.plot(seed.times, s_vels, lw=0.8)
    ax2.plot(matched.times, m_vels)
    ax2.set(ylabel='Vel. (cm/s)', xticklabels=[])

    ax3 = plt.subplot(gs_top[2, 0])
    ax3.axhline(0, color='black', lw=0.5)
    if seed:
        ax3.plot(seed.times, s_disps, lw=0.8)
    ax3.plot(matched.times, m_disps)
    ax3.set(ylabel='Disp. (cm)', xticklabels=[])

    ax4 = plt.subplot(gs_top[3, 0])
    if seed:
        ax4.plot(seed.times, seed.arias_intensity(norm=True), lw=0.8)
    ax4.plot(matched.times, matched.arias_intensity(norm=True))

    ax4.set(ylabel='Norm. $I_a$', xlabel='Time (sec)')

    ax5 = plt.subplot(gs_bot[0, 0])
    if seed:
        ax5.plot(*seed.calc_fourier_spectrum(True), lw=0.8)
    ax5.plot(*matched.calc_fourier_spectrum(True), lw=0.8)

    ax5.set(
        xlabel='Frequency (Hz)', xscale='log',
        ylabel='Fourier Ampl. (cm/s)', yscale='log', ylim=(1e-3, 1e3),
    )

    ax6 = plt.subplot(gs_bot[0, 1])
    m_ars = matched.calc_spec_accels(osc_freqs, osc_damping)
    ax6.plot(target.periods, target.spec_accels, label='Target', color='C2')
    if seed:
        s_ars = seed.calc_spec_accels(osc_freqs, osc_damping)
        ax6.plot(1 / s_ars.osc_freq,  s_ars.spec_accel, label='Seed', color='C0', lw=0.8)
    ax6.plot(1 / m_ars.osc_freq,  m_ars.spec_accel, label='Matched', color='C1')

    ax6.set(
        xlabel='Period (s)', xscale='log',
        ylabel='5%-Damped, Spec. Accel. (g)', yscale='linear'
    )
    ax6.legend(fontsize='small')

    return fig, [ax1, ax2, ax3, ax4, ax5, ax6]


def plot_timeseries(fpath, time_step, accels):
    fpath = pathlib.Path(fpath)
    fpath.parent.mkdir(parents=True, exist_ok=True)

    times = time_step * np.arange(len(accels))
    vels = cumtrapz(accels, x=times, initial=0)
    disps = cumtrapz(accels, x=times, initial=0)

    fig, axes = plt.subplots(nrows=3, sharex=True)

    for ax, values, ylabel in zip(axes,
                                  [accels, vels, disps],
                                  ['Accel. (g)', 'Vel. (cm/s)', 'Disp. (cm)']):
        ax.plot(times, values, color='C0')
        ax.set_ylabel(ylabel)

    axes[-1].set_xlabel('Time (sec)')

    fig.tight_layout()
    fig.savefig(str(fpath), dpi=200)
    plt.close(fig)


def plot_spectra(fpath, periods, psas_target, psas_matched):
    fpath = pathlib.Path(fpath)
    fpath.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots()

    ax.plot(periods, psas_target, label='Target')
    ax.plot(periods, psas_matched, label='Matched')

    ax.set(
        xlabel='Period (sec)', xscale='log',
        ylabel='5%-Damped, Spec. Accel. (g)', yscale='log',
    )
    ax.legend()

    fig.tight_layout()
    fig.savefig(str(fpath), dpi=200)
    plt.close(fig)

