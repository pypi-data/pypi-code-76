import numpy as np
from matplotlib import mlab
import logging

from signum.tools.scale_manager import ScaleManager

from signum.core.base_container import SignalContainer, SCA
from signum.core.freq_domain_signal import FreqDomainSignal


logger = logging.getLogger(__name__)


class TimeDomainSignal(SignalContainer):
    ATTRIBUTES = SignalContainer.ATTRIBUTES + [SCA('_t_sampling', 1, True)]

    def __new__(cls, *args, f_sampling: float = 1, f_sampling_unit='Hz', **kwargs):
        kwargs['x_unit'] = kwargs.pop('x_unit', 's')
        kwargs['x_description'] = kwargs.pop('x_description', 'Time')
        obj = super().__new__(cls, *args, **kwargs)

        # set sampling time
        f_sampling, f_sampling_unit = ScaleManager.rescale_to_basic(f_sampling, f_sampling_unit)
        obj.t_sampling = 1./f_sampling  # using the t sampling setter

        return obj

    def __repr__(self):
        return super().__repr__() + f' sampled at {ScaleManager.display(self.f_sampling, "Hz")}'

    @property
    def resolution(self):
        return self._base_resolution * self._t_sampling

    @resolution.setter
    def resolution(self, val):
        self._resolution_setter_(val)

    def _resolution_setter_(self, val):
        self._t_sampling = val
        self._resolution_defaults_setter()

    @property
    def t_sampling(self):
        return self.resolution

    @t_sampling.setter
    def t_sampling(self, val):
        self._resolution_setter_(val)

    @property
    def f_sampling(self):
        return 1./self.t_sampling

    @f_sampling.setter
    def f_sampling(self, val):
        self._resolution_setter_(1./val)

    @staticmethod
    def check_metadata(arr1, arr2, require_type=False):
        for i, arr in enumerate([arr1, arr2]):
            if not isinstance(arr, TimeDomainSignal):
                m = f'Input array #{i+1} is not an instance of TimeDomainSignal'
                if require_type:
                    raise TypeError(m)
                logger.debug(m)
                return

        if not np.isclose(arr1.f_sampling, arr2.f_sampling):
            raise ValueError(f"Inputs sampling frequencies mismatch: {arr1.f_sampling:.2E} and {arr2.f_sampling:.2E}")

    @staticmethod
    def csd(x, y=None, **kwargs) -> FreqDomainSignal:
        """Cross spectral density"""

        y_in = y if y is not None else x

        # check that the operation is applicable to the inputs
        TimeDomainSignal.check_metadata(x, y_in, require_type=True)

        # calculate the spectrum
        spectrum, frequencies = mlab.csd(y_in, x, **kwargs, Fs=x.f_sampling)

        # cast type to FreqDomainSingal
        if y is None:
            description = f"{x.description}: power spectral density"
            meta = {**x.meta, 'original_description': x.description}
        else:
            description = f"{x.description} & {y.description}: cross spectral density"
            meta = {**x.meta, **y.meta, 'original_descriptions': [x.description, y.description]}

        spectrum = FreqDomainSignal(spectrum, f_resolution=frequencies[1] - frequencies[0], x_start=frequencies[0],
                                    description=description, meta=meta, unit=x.unit)

        return spectrum

    @staticmethod
    def psd(x, **kwargs):
        """Power spectral density"""

        return TimeDomainSignal.csd(x, **kwargs)


if __name__ == '__main__':
    data1 = TimeDomainSignal(np.random.rand(12), f_sampling=40e6)
    data2 = TimeDomainSignal(np.arange(12).reshape(1, -1), f_sampling=1, unit='V')
    data3 = TimeDomainSignal(np.arange(12), f_sampling=40e6)

    data1.display()

    psd = TimeDomainSignal.psd(data1)
    psd.display()

    csd = TimeDomainSignal.csd(data1, data3)
    csd.display()
