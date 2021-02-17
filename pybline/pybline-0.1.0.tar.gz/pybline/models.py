import pathlib
import sys

import numpy as np
import scipy.signal

import pyrotd

from scipy import constants
from scipy.integrate import cumtrapz
from scipy.signal import tukey

from . import GRAV


def _read_group(fp):
    pair = [{}, {}]
    for p in pair:
        p['input'] = next(fp).strip()

    for p in pair:
        for ext in ['acc', 'rsp', 'unm']:
            p[f'output_{ext}'] = next(fp).strip()

    return pair


class InputFile:
    def __init__(self):
        pass

    @classmethod
    def read(cls, fpath):
        self = cls()
        self.fpath = pathlib.Path(fpath)

        with self.fpath.open() as fp:
            for _ in range(16):
                next(fp)

            self.target_fname = next(fp).strip()

            count = int(next(fp).split()[0])
            self.groups = [_read_group(fp) for _ in range(count)]

        fpath_target = self.fpath.with_name(self.target_fname)
        if fpath_target.exists():
            self.target = TargetSpectrum.read(fpath_target)

        return self

    def read_group(self, names, keys, prefer_blc=True):
        group = []
        for k in keys:
            exts = ['-pb.acc'] if prefer_blc else []
            exts.append('.acc')

            for ext in exts:
                fpath = self.fpath.with_name(names[k].replace('.acc', ext))
                print(fpath)
                if fpath.exists():
                    ts = TimeSeries.read(fpath)
                    break
            else:
                raise FileNotFoundError(fpath)
            group.append(ts)
        return group


class TargetSpectrum:
    def __init__(self, damping=None, freqs=None, spec_accels=None):
        self.header = ''
        self.damping = damping
        self.freq_lim = None
        self.freqs = np.asarray(freqs)
        self.spec_accels = np.asarray(spec_accels)

    @property
    def periods(self):
        return 1. / self.freqs

    @classmethod
    def read(cls, fpath):
        fpath = pathlib.Path(fpath)
        self = cls()

        with fpath.open() as fp:
            self.header = next(fp).strip()
            count = int(next(fp).split()[0])
            self.damping = float(next(fp))
            values = np.array(
                [next(fp).split() for _ in range(count)]).astype(float)
            self.freqs = np.array(values[:, 0])
            self.spec_accels = np.array(values[:, 3])

            self.freq_lim = (values[0, 1], values[0, 2])

        return self

    def write(self, file=sys.stdout):
        print(self.header, file=file)
        print(f'{len(self.freqs)}', '1', file=file)
        print(f'{self.damping:0.3f}', file=file)

        for f, sa in zip(self.freqs, self.spec_accels):
            print(
                f'{f:8.4f}',
                f'{self.freq_lim[0]:7.3f}',
                f'{self.freq_lim[1]:7.3f}',
                f'{sa:10.4e}',
                file=file)

    def interp(self, freqs):
        ln_spec_accels = np.log(self.spec_accels)
        if self.freqs[1] > self.freqs[0]:
            order = 1
            ln_pga = ln_spec_accels[-1]
        else:
            order = -1
            ln_pga = ln_spec_accels[0]

        return np.exp(np.interp(
            np.log(freqs),
            np.log(self.freqs[::order]),
            ln_spec_accels[::order],
            left=np.nan,
            right=ln_pga
        ))


class TimeSeries:
    def __init__(self, time_step=None, accels=None):
        self.header = ''
        self.time_step = time_step
        self.accels = accels

    def __len__(self):
        return len(self.accels)

    @property
    def pga(self):
        return np.abs(self.accels).max()

    @property
    def times(self):
        return self.time_step * np.arange(len(self))

    def calc_spec_accels(self, osc_freqs, osc_damping):
        ars = pyrotd.calc_spec_accels(
            self.time_step, self.accels, osc_freqs, osc_damping)
        return ars

    def calc_fourier_spectrum(self, magnitude_only=True):
        freqs = np.fft.rfftfreq(self.times.size, d=self.time_step)
        # Normalize by the timestep
        ampls = GRAV * self.time_step * np.fft.rfft(self.accels)
        if magnitude_only:
            ampls = np.abs(ampls)
        return freqs, ampls

    def integrate(self):
        # Convert to cm/s
        vels = GRAV * cumtrapz(self.accels, dx=self.time_step, initial=0)
        disps = cumtrapz(vels, dx=self.time_step, initial=0)

        return vels, disps

    def arias_intensity(self, norm=False):
        ia = cumtrapz(
            (constants.g * self.accels) ** 2, dx=self.time_step, initial=0)
        ia *= np.pi / (2 * constants.g)

        if norm:
            ia /= ia[-1]

        return ia

    def copy(self):
        other = TimeSeries()
        other.header = self.header
        other.time_step = self.time_step
        other.accels = np.array(self.accels)
        return other

    @classmethod
    def read(cls, fpath):
        self = cls()
        fpath = pathlib.Path(fpath)

        if fpath.suffix.lower() == '.acc':
            self._read_acc(fpath)
        elif fpath.suffix.lower() == '.at2':
            self._read_at2(fpath)

        return self

    def _read_acc(self, fpath):
        with fpath.open() as fp:
            self.header = next(fp).strip()
            parts = next(fp).split()
            # count = int(parts[0])
            self.time_step = float(parts[1])
            self.accels = np.array([float(p) for l in fp for p in l.split()])

    def _read_at2(self, fpath):
        with fpath.open() as fp:
            next(fp)
            self.header = next(fp).strip()
            next(fp)
            line = next(fp)
            # count = int(line[5:12])
            self.time_step = float(line[17:25])
            self.accels = np.array(
                [float(p) for l in fp for p in l.split()])

    def write(self, file=sys.stdout, ncols=4):
        print(self.header, file=file)
        print(len(self.accels), f'{self.time_step:0.4f}', file=file)

        for i, a in enumerate(self.accels):
            print(f'{a:14.5e}', file=file,
                  end='\n' if (i + 1) % ncols == 0 else '')

    def trim(self, time_start, time_end, taper=0.05, high_pass=0.005):
        accels = self.accels.copy()

        # Trim time series if needed
        if not np.isclose(time_start, time_end):
            start = int(time_start / self.time_step)
            if time_end > 0 and time_start < time_end:
                end = int(time_end / self.time_step)
            else:
                end = None
            accels = accels[start: end]

        # High pass filter in the frequency domain
        if high_pass > 0:
            # Need to normalize frequency by the Nyquist frequency
            w_nyq = 1 / (2 * self.time_step)
            w_n = high_pass / w_nyq
            b, a = scipy.signal.butter(4, w_n, 'highpass')
            accels = scipy.signal.lfilter(b, a, accels)

        # Apply cosine taper
        if taper > 0:
            accels *= tukey(accels.size, taper / 100)

        ts = self.copy()
        ts.accels = accels
        return ts


class BaselineCorrection:
    def __init__(self):
        self.padding = 10
        self.degree = 5
        self.select_start = 0
        self.select_end = 0
        self.taper = 5
        self.force_zero_disp = True

        self.time_series = None
        self.disps_corr = None

    def __call__(self, ts):
        # Pad to improve fitting of the polynomial
        npadding = int(self.padding / 100 * len(ts))
        accels = np.r_[ts.accels, np.zeros((npadding))]
        times = ts.time_step * np.arange(len(accels))

        times_mat = times[:, np.newaxis] ** np.arange(self.degree + 1)

        # Fit the polynomial on the displacement
        vels = cumtrapz(accels, dx=ts.time_step, initial=0)
        disps = cumtrapz(vels, dx=ts.time_step, initial=0)

        if not np.isclose(self.select_start, self.select_end):
            # Use the final time if none is provided
            if self.select_start > 0 and self.select_end == 0:
                select_end = times[-1]
            else:
                select_end = self.select_end

            mask = (self.select_start <= times) & (times <= select_end)
        else:
            mask = np.ones_like(times, dtype=bool)

        # Here first two times are skipped because the coefficients are forced
        # to be zero
        coeffs_disp, res, rank, s = np.linalg.lstsq(
            times_mat[mask, 2:], disps[mask], rcond=None)

        # Compute coefficients for acceleration and velocity
        # The first two coefficients are missing from the fit
        coeffs_vel = [(i + 2) * c
                      for i, c in enumerate(coeffs_disp)]
        coeffs_acc = [(i + 1) * (i + 2) * c
                      for i, c in enumerate(coeffs_disp)]

        # Remove the padded zeros
        end = len(ts)
        times_mat = times_mat[0: end, :]
        times = times[0: end]
        accels = accels[0: end]
        vels = vels[0: end]
        disps = disps[0: end]
        mask = mask[0: end]

        # Correction based on the acceleration
        if np.all(mask):
            correction = times_mat[:, :-2] @ coeffs_acc
        else:
            # The modifed portion
            modif = times_mat[mask, :-2] @ coeffs_acc
            modif *= tukey(modif.size, self.taper / 100)

            correction = np.zeros(end)
            correction[mask] = modif

        if not np.all(mask):
            correction[~mask] = 0

        self.disps_fit = GRAV * (times_mat[:, 2:] @ coeffs_disp)
        self.disps_fit[~mask] = np.nan

        if self.force_zero_disp:
            # Compute tapers for the acceleration, velocity and displacement
            # This will force the velocity and displacement to zero at the end
            # of the traces.
            ntaper = int(self.taper / 100 * len(ts))
            i = np.arange(ntaper) / (ntaper - 1)
            ttaper = ts.time_step * ntaper

            def tscorr(values, coeffs, resp):
                if resp == 'acc':
                    # Acceleration
                    _taper = 0.5 * (np.cos(np.pi * i) + 1)
                    _start, _stop = 0, -2
                elif resp == 'vel':
                    # Velocity
                    _taper = -0.5 * (np.pi / ttaper) * np.sin(np.pi * i)
                    _start, _stop = 1, -1
                else:
                    # Displacement
                    _taper = -0.5 * (np.pi / ttaper) ** 2 * np.cos(np.pi * i)
                    _start, _stop = 2, None

                return (values[-ntaper:] -
                        times_mat[-ntaper:, _start: _stop] @ coeffs) * _taper

            correction[-ntaper:] = accels[-ntaper:] - (
                tscorr(accels, coeffs_acc, 'acc') +
                2 * tscorr(vels, coeffs_vel, 'vel') +
                tscorr(disps, coeffs_disp, 'disp')
            )

        accels -= correction

        self.time_series = ts.copy()
        self.time_series.accels = accels

        return self.time_series

    @property
    def times(self):
        return self.time_series.times

