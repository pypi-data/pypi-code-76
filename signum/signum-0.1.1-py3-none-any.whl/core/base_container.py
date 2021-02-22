# based on: https://www.numpy.org/devdocs/user/basics.subclassing.html

import matplotlib.pyplot as plt
import numpy as np
import logging
from collections import abc
from typing import Iterable, List, NamedTuple, Any

from signum.tools.plotting_tools import adjust_plot_scale


logger = logging.getLogger(__name__)

SCA = NamedTuple('DataContainerAttribute', [('name', str), ('default_value', Any), ('is_core', bool)])


class SignalContainer(np.ndarray):
    """A subclass of numpy.ndarray, wrapping array data to include metadata envelope (such as sampling frequency)."""

    ATTRIBUTES = [SCA('unit', '', True),
                  SCA('x_unit', '', True),
                  SCA('_base_resolution', 1, True),
                  SCA('x_start', 0, False),
                  SCA('_nonstandard_x_axis', None, False),
                  SCA('description', '', False),
                  SCA('x_description', '', False),
                  SCA('meta', {}, False)]

    def __new__(cls, data, unit: str = None, x_unit: str = None, description: str = None, x_description: str = None,
                x_start: float = None, x_axis=None, resolution: float = None, meta: dict = None):
        """Create a new instance of a DataContainer.

        Parameters
        ----------
        data            :   array_like
            input data to be converted to an array (see numpy.asarray for more details)
        unit            :   str, optional
            data unit
        x_unit          :   str, optional
            unit of the x axis data (e.g. 's', 'Hz')
        description     :   str, optional
            data description
        x_description   :   str, optional
            description of the x axis data (e.g. 'Time')
        x_start         :   float, optional
            starting value for an automatically-generated x axis (calculated from data length and resolution)
        x_axis          :   array_like, optional
            nonstandard x axis data (e.g. if the signal data is not equally spaced); must match the first dimension
            of the data shape
        resolution      :   float, optional
            data spacing (in the x axis units)
        meta            :   dict, optional
            additional, user-provided metadata
        """

        obj = np.asarray(data).view(cls)

        def gv(val, name):
            return val if val is not None else getattr(obj, name)

        # definition of object properties
        obj.unit = gv(unit, 'unit')
        obj.x_unit = gv(x_unit, 'x_unit')
        obj.description = gv(description, 'description')
        obj.x_description = gv(x_description, 'x_description')
        obj.x_start = gv(x_start, 'x_start')
        obj.resolution = gv(resolution, 'resolution')  # using the resolution setter
        obj.meta = gv(meta, 'meta')

        if x_axis is not None:
            obj.x_axis = x_axis  # using the (nonstandard) x axis setter

        return obj

    def __array_finalize__(self, obj):
        """Finalize DataContainer instance creation by assigning the envelope attributes.

        This method is automatically called in every case a new instance of DataContainer is created (unlike __new__ and
        __init_, used only during explicit constructor call; in that case, __array_finalize__ is called first).
        See https://www.numpy.org/devdocs/user/basics.subclassing.html for more details.

        The goal of using this method is to make sure that all the envelope attributes are defined for the newly created
        object."""

        # update the attributes of the newly created object
        self._update_from_obj(obj)

    def _update_from_obj(self, obj=None):
        """Update self to include all the envelope attributes. Copy values from the template object or use defaults.

        The attribute values can come from three sources, depending on the way an instance is created:
        - class defaults (self.defaults from self.ATTRIBUTES)
        - previously defined values (self.__dict__)
        - template object (obj, instance of the same class as self).
        """

        # create container for attributes to be set
        _attributes = {}

        # pre-fill with default values; make sure all attribute names are present
        _attributes.update(self.defaults)

        # preserve current attribute values
        # (if present; when initializing from explicit constructor call, self.__dict__ at this point is empty)
        _attributes.update(self.__dict__)

        # copy attributes from obj (if it is of the same type as self; it might also be None)
        if isinstance(obj, type(self)):
            _attributes.update({k: getattr(obj, k) for k in _attributes.keys()})

        # update the instance attributes with the final set
        self.__dict__.update(_attributes)

    @property
    def defaults(self):
        """Return a dictionary of the default values for the envelope attributes."""

        return {t.name: t.default_value for t in self.ATTRIBUTES}

    @property
    def core_attributes(self) -> List[str]:
        """Return a list of names of the core envelope attributes.

        These are the attributes that need to be taken into account when performing an operation (e.g. addition) on two
        DataContainers (their values must be the same for both inputs - otherwise the operation is not valid).
        """

        return [t.name for t in self.ATTRIBUTES if t.is_core]

    @property
    def envelope_attributes(self):
        """Return a dictionary of current values of the core envelope attributes."""

        return self.get_attributes(self.core_attributes)

    @property
    def envelope_attributes_extended(self):
        """Return a dictionary of current values of the core envelope attributes."""

        return self.get_attributes(self.defaults.keys())

    def get_attributes(self, attr_names: Iterable[str]):
        return {attr: getattr(self, attr, None) for attr in attr_names}

    @envelope_attributes.setter
    def envelope_attributes(self, envelope_dict):
        self.set_attributes(envelope_dict)

    def set_attributes(self, attributes_dict):
        invalid_keys = set(attributes_dict.keys()) - set(self.defaults.keys())
        n = len(invalid_keys)
        if n:
            raise AttributeError(f"{type(self)} has no attribute{'s' if n > 1 else ''}: {invalid_keys}")

        for k, v in attributes_dict.items():
            setattr(self, k, v)

    def copy_attributes(self, other):
        if not isinstance(other, type(self)):
            logger.warning(f"The template object is not an instance of {self.__class__.__name__}")
            return

        self._update_from_obj(other)

    @staticmethod
    def recast_type(func):
        """Perform view casting and copy attributes from the first input to first output of the decorated function."""

        def wrapper(data_in: SignalContainer, *args, **kwargs):
            data_out = func(data_in, *args, **kwargs)

            # if there are multiple outputs - handle only the first one, leave the rest unchanged
            if isinstance(data_out, tuple):
                data_out, *other_outputs = data_out
            else:
                other_outputs = ()

            # view casting
            data_out = data_out.view(type(data_in))

            # propagating attributes
            if isinstance(data_out, SignalContainer):
                data_out.copy_attributes(data_in)

            # fold the outputs tuple back
            return (data_out, *other_outputs) if other_outputs else data_out

        return wrapper

    def __repr__(self):
        return f"{self.description or ''}{': ' if self.description else ''}{self.__class__.__name__} object " \
               f"containing {self.dtype} data array of shape {self.shape}"

    def __array_ufunc__(self, ufunc, method, *args, **kwargs):

        args_envelope = []

        def check_envelope_attributes(obj, side="Inputs"):
            new_envelope = obj.envelope_attributes
            if not len(args_envelope):
                args_envelope.append(new_envelope)
            else:
                if args_envelope[0] != new_envelope:
                    raise TypeError(f"{side} attributes mismatch! ({args_envelope[0]}, {new_envelope})")

        inputs = []
        for arg in args:
            if isinstance(arg, self.__class__):
                check_envelope_attributes(arg)
                inputs.append(arg.view(np.ndarray))  # cast to plain ndarray
            else:
                inputs.append(arg)

        outputs = kwargs.pop('out', None)
        if outputs:
            out_args = []
            for output in outputs:
                if isinstance(output, self.__class__):
                    check_envelope_attributes(output, 'Input/output')
                    out_args.append(output.view(np.ndarray))
                else:
                    out_args.append(output)
            kwargs['out'] = tuple(out_args)
        else:
            outputs = (None,) * ufunc.nout

        results = super(SignalContainer, self).__array_ufunc__(ufunc, method, *inputs, **kwargs)

        if results is NotImplemented:
            return NotImplemented

        if ufunc.nout == 1:
            results = (results,)

        results_converted = []
        for result, output in zip(results, outputs):
            out = result if output is None else output

            # convert back to DataContainer
            rconv = np.asarray(out).view(self.__class__)
            rconv.copy_attributes(self)
            results_converted.append(rconv)

        return results_converted[0] if len(results_converted) == 1 else tuple(results_converted)

    def __getitem__(self, item):
        res = super().__getitem__(item)

        if isinstance(res, type(self)):
            if isinstance(item, tuple):
                item = item[0]

            if not isinstance(item, slice) or self._nonstandard_x_axis is not None:
                res._nonstandard_x_axis = self.x_axis[item]  # nonstandard choice of indices
            else:
                res.x_start = self.x_axis[item][0]
                if item.step is not None:
                    res._base_resolution *= item.step

        return res

    @property
    def resolution(self):
        return self._base_resolution

    @resolution.setter
    def resolution(self, val):
        logger.debug(f"Setting base resolution to {val}")
        self._base_resolution = val

    def _resolution_defaults_setter(self):
        self._base_resolution = 1
        self._nonstandard_x_axis = None

    @property
    def x_axis(self):
        if self._nonstandard_x_axis is not None:
            return self._nonstandard_x_axis

        x0 = self.x_start if self.x_start is not None else 0
        return x0 + np.arange(self.shape[0]) * self.resolution

    @x_axis.setter
    def x_axis(self, val):
        if val is None:
            return

        if not isinstance(val, (abc.Sequence, abc.Iterable)):
            raise TypeError("x axis should be a sequence")

        if not len(val) == self.shape[0]:
            raise ValueError(f"Length of the x axis ({len(val)}) does not match the signal shape ({self.shape})")

        self._nonstandard_x_axis = val

        if val is not None:
            self.x_start = 0

    @property
    def x_label(self):
        return self.x_description + (f' [{self.x_unit}]' if self.x_unit else '')

    @property
    def y_label(self):
        return self.description + (f' [{self.unit}]' if self.unit else '')

    @property
    def magnitude(self):
        mag = np.abs(self)
        mag.description = (self.description or '') + f' (magnitude)'
        return mag

    @property
    def magnitude_db(self):
        mag_db = 20 * np.log10(self.magnitude)
        mag_db.unit = 'dB'
        return mag_db

    @property
    def phase(self):
        return self.get_phase()

    def get_phase(self, rad=False, unwrapped=True):
        """Calculate phase of the signal.

        Parameters
        ----------
        rad         :   bool
            if True, return the phase in radians; otherwise (default) - use degrees
        unwrapped   :   bool
            if True (default), unwrap the phase to avoid 2pi jumps; otherwise, return the phase limited to (-pi, pi)
            or (-180, 180), depending on the desired unit
        """

        ph = np.angle(self)
        if unwrapped:
            ph = np.unwrap(ph)
        if not rad:
            ph = np.rad2deg(ph)

        ph = ph.view(self.__class__)
        ph.copy_attributes(self)
        ph.unit = 'rad' if rad else 'deg'
        ph.description = (ph.description or '') + ' (phase)'
        return ph

    def display(self, complex_plot: str = 'bode', show: bool = True, **kwargs):
        """Create a plot to display the data.

        Parameters
        ----------
        complex_plot    :   str
            if the data is complex, this argument specifies the type of plot to be created. Available options:
            'bode', 'nyquist', 'iq'. For real-valued data, this argument is ignored.
        show            :   bool
            if True, display the plot; setting to False allows later customisation before displaying it
        kwargs
            additional keyword arguments passed to the specific plotting methods (or matplotlib.pyplot.plot)
        """

        if np.iscomplexobj(self):
            if complex_plot == 'bode':
                fig, axes = self._display_complex_bode(**kwargs)
            elif complex_plot == 'nyquist':
                fig, axes = self._display_complex_nyquist(**kwargs)
            elif complex_plot == 'iq':
                fig, axes = self._display_complex_iq(**kwargs)
            else:
                raise ValueError(f"Unknown complex plot type code: {complex_plot}; "
                                 f"should be one of: 'bode', 'nyquist', 'iq'")
        else:
            fig, axes = self._display_real(**kwargs)

        for ax in axes:
            ax.grid(color='lightgray')

        if complex_plot != 'nyquist':
            adjust_plot_scale(axes[-1], x_unit=self.x_unit, x_label=self.x_description)

        fig.suptitle(self.description, fontsize=14)

        if show:
            plt.show()

        return fig, axes

    def _display_complex_bode(self, db_scale: bool = False, **kwargs):
        """Display a complex signal in a form of Bode plot (magnitude and phase).

        Parameters
        ----------
        db_scale    :   bool
            if True, display the magnitude in decibels.
        """

        fig, axes = plt.subplots(2, 1, sharex='all')

        mag = self.magnitude_db if db_scale else self.magnitude
        axes[0].plot(mag.x_axis, mag, **kwargs)
        adjust_plot_scale(axes[0], y_unit=mag.unit if not db_scale else None, y_label="Magnitude")

        phase = self.phase
        axes[1].plot(phase.x_axis, phase, **kwargs)
        axes[1].set_ylabel(f"Phase [{phase.unit}]")

        return fig, axes

    def _display_complex_iq(self, sharey='all', **kwargs):
        """Display a complex signal in two subplots: real and imaginary part separately.

        Parameters
        ----------
        sharey  :   str or bool
            passed to matplotlib.pyplot.subplots; if 'all' (or True), the y axis of both subplots is shared.
        """

        fig, axes = plt.subplots(2, 1, sharex='all', sharey=sharey)

        axes[0].plot(self.x_axis, self.real, **kwargs)
        adjust_plot_scale(axes[0], y_unit=self.unit, y_label="Real part")

        axes[1].plot(self.x_axis, self.imag, **kwargs)
        adjust_plot_scale(axes[1], y_unit=self.unit, y_label="Imaginary part")

        return fig, axes

    def _display_complex_nyquist(self, **kwargs):
        """Display a complex-valued signal in a form of a Nyquist plot (imaginary vs real part)."""

        fig, ax = plt.subplots()
        axes = np.array([ax])

        ax.set_aspect('equal')
        ax.plot(self.real, self.imag, **kwargs)

        ax.axvline(0, color='k', zorder=1)
        ax.axhline(0, color='k', zorder=1)

        adjust_plot_scale(ax, x_unit=self.unit, y_unit=self.unit, x_label="I component", y_label="Q component")

        lim = np.max(np.abs([*ax.get_xlim(), *ax.get_ylim()]))
        ax.set_xlim([-lim, lim])
        ax.set_ylim([-lim, lim])

        return fig, axes

    def _display_real(self, **kwargs):
        """Display a real-valued signal."""

        fig, ax = plt.subplots()
        axes = np.array([ax])

        ax.plot(self.x_axis, self, **kwargs)
        adjust_plot_scale(ax, y_unit=self.unit, y_label=self.description)

        return fig, axes
