"""Trajectory calculation configuration module."""

from .trajectory import Trajectory

from ..esa import CReMAs
from ..kernels import MetaKernel, Kernels
from ..spice import SPICEPool, et_range


class TrajectoryConfig:
    """Trajectory calculation configuration object.

    Prepare the kernels configuration based on the selected
    spacecraft, target and metakernel setup.
    By default the SPICE kernel pool is purge and
    automatically loaded with the selected kernels.

    Parameters
    ----------
    spacecraft: str, optional
        Name of the spacecraft selected (default: `JUICE`).

    mk: kernels.MetaKernel or str, optional
        Choice of a metakernel or a CReMA. You can provide your own
        or use directly the predefined metakernels for the selected
        spacecraft.

        For example: ``'3.0'`` (default) with the spacecraft ``JUICE``
        will load ``JUICE_CReMA['3.0']`` CReMA metakernel.

    target: str, optional
        Name of the target selected (default: `Ganymede`).

    kernels: str or pathlib.Path or kernels.Kernel, optional
        Additional kernel(s) to add that were not listed on the
        metakernel. Multiple files can be loaded at once.

    kernels_dir: str or pathlib.Path, optional
        Kernels location (absolute path). If ``None`` is provided
        (default), the location will be based kernels environment
        variables configuration (`KERNELS_XXXX` with `XXXX` the
        name spacecraft).

    download_kernels: bool, optional
        Try to download the missing kernels if there
        are missing (default: `False`).

    autoload_kernels: bool, optional
        Autoload the kernel pool (:py:func:`spiceypy.furnsh`)
        with all the kernels (default: `True`).
        If the autoloader is disabled, you need to use the
        :py:func:`load_spice_pool` function to load the pool.

    default_time_step: str, optional
        Default time step if a temporal slice is provided without
        a defined temporal step.

    Raises
    ------
    FileNotFoundError
        If some kernels are missing and :py:attr:`download_kernels`
        is set to ``False``.

    KeyError
        If the target name is unknown.

    """

    kernels = ()

    def __init__(self, spacecraft='JUICE', mk='3.0', target='Ganymede',
                 kernels=None, kernels_dir=None,
                 download_kernels=False, autoload_kernels=True,
                 default_time_step='1 minute'):
        # Properties
        self.spacecraft = spacecraft.upper()
        self.target = target.upper()

        self.download_kernels = download_kernels
        self.autoload_kernels = autoload_kernels
        self.default_time_step = default_time_step

        # Kernel setup
        self.kernels_dir = kernels_dir
        self.mk = mk
        self.add_kernel(kernels)

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}> '
            f'Spacecraft: {self.spacecraft} | '
            f'Metakernel: {self.metakernel} | '
            f'Target: {self.target}'
        )

    def __getitem__(self, value):
        if isinstance(value, slice):
            value = et_range(
                value.start,
                value.stop,
                value.step if value.step is not None else self.default_time_step,
            )

        return Trajectory(
            self.kernels,
            self.spacecraft,
            self.target,
            value,
        )

    @property
    def kernels_dir(self):
        """Set of loaded kernels."""
        return self.__kernels_dir

    @kernels_dir.setter
    def kernels_dir(self, kernels_dir):
        """Kernels folder setter."""
        if kernels_dir is None:
            kernels_dir = self.spacecraft

        self.__kernels_dir = Kernels(kernels_dir)

    @property
    def mk(self):
        """Selected metakernel."""
        return self.__mk

    @mk.setter
    def mk(self, mk):
        """Metakernel setter."""
        if mk is None:
            self.__mk = mk
            return

        if isinstance(mk, MetaKernel):
            self.__mk = mk

        elif self.spacecraft in CReMAs and mk in CReMAs[self.spacecraft]:
            self.__mk = CReMAs[self.spacecraft][mk]

        else:
            self.__mk = MetaKernel(mk)

        # Check if the kernels are present locally
        check = self.mk.check(kernels=self.__kernels_dir,
                              download=self.download_kernels)

        if check['missing']:
            missing = ''.join([f'\n - {k}' for k in check['missing']])
            raise FileNotFoundError(
                'Some kernels are missing, use `download_kernels=True`'
                f' to try to download them: {missing}'
            )

        self.kernels = tuple(self.mk(kernels=self.kernels_dir))

        if self.autoload_kernels:
            self.load_spice_pool()

    @property
    def metakernel(self):
        """Metakernel file name."""
        return self.mk.fname.name if self.mk is not None else None

    def add_kernel(self, kernel):
        """Add custom kernels to the configuration."""
        if kernel is not None:
            if isinstance(kernel, (list, tuple)):
                return [self.add_kernel(k) for k in kernel]

            self.kernels += (str(kernel),)

            if self.autoload_kernels:
                SPICEPool.add(str(kernel))

        return kernel

    def load_spice_pool(self):
        """Load the kernels in the SPICE pool."""
        if SPICEPool != self.kernels:
            SPICEPool.add(self.kernels, purge=True)
