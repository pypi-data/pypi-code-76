# -*- coding: utf-8 -*-
# +
"""
    latticetools.py - Takes care of sampling data on a lattice
    Copyright (C) 2020 Jack Maxwell jack@maxman.cc

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

from functools import reduce
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib.ticker import MultipleLocator, FuncFormatter, ScalarFormatter, LogLocator, Formatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import operator
try:
    from pyfftw.interfaces import numpy_fft as mod_fft
except ImportError:
    from numpy import fft as mod_fft
ifft = mod_fft.ifft
fft = mod_fft.fft
fftfreq, fftshift, ifftshift = mod_fft.fftfreq, mod_fft.fftshift, mod_fft.ifftshift
from itertools import count, product
from skimage.transform import warp as _warp
from collections import deque
from operator import itemgetter

_slt = lambda sl, step: slice(sl.start, sl.stop + 0.5 * step, step)
can_iter = lambda x: hasattr(x, '__iter__')
_coords2slice = lambda cflat: slice(
    cflat[0], 
    cflat[-1] + cflat[:2].ptp() / 2,
    cflat[:2].ptp(),
)
coords2slice = lambda coords: _coords2slice(coords.flatten())
def extf(*dims,upper=False):
    ext1d = lambda dim: [dim[0] - .5 * dim[:2].ptp(),
                         dim[-1] + .5 * dim[:2].ptp()]
    uppercheck = lambda axis, dim: ext1d(dim)[::1 - 2 * (upper and axis)]
    res = reduce(lambda sofar, i_n_dim: sofar + uppercheck(*i_n_dim),
                 enumerate(map(lambda dim: dim.flatten(), dims)), [])
    return res
lastel = lambda sl: (sl.stop - sl.start) // sl.step * sl.step + sl.start
ogrid2extents = lambda ogrid: np.array(list(map(slice2extent, map(coords2slice, ogrid))))
ogrid2mgrid = lambda ogrid: np.stack(tuple(
    ogridi + sum(ogrid) * 0 for ogridi in ogrid))
primefactors = lambda x, sofar = [], nextone = 2: sofar if x == 1 else (
        primefactors(x, sofar, nextone + 1) if x / nextone % 1 else
        primefactors(x / nextone, sofar + [nextone], nextone))
shapeof = lambda x: (len(x), *shapeof(x[0])) if can_iter(x) else ()
sliceflesher = lambda sl: slice(*(
    d if v is None else v
    for d, v in zip(
        (0, None, 1),
        (sl.start, sl.stop, sl.step),
        )))
slice2extent = lambda slice: [sl.start - .5 * sl.step, lastel(sl) + .5 * sl.step]
slices2extents = lambda slices: np.array([
    [
        sl.start - .5 * sl.step, 
        lastel(sl) + .5 * sl.step,
    ]
    for sl in slices
])
slicesanitiser = lambda sl: slice(
        sl.start,
        (
            sl.stop - .5 * sl.step
            if any(np.isclose((sl.stop - sl.start) % sl.step * sl.step, (0,1)))
            else sl.stop
        ),
        sl.step
) 
slicetricker = lambda sl: (
        _slt(sl, (sl.stop - sl.start) / sl.step.imag)
        if type(sl.step) is complex else sl
)
to_iter = lambda x: x if can_iter(x) else (x,)
val2i = lambda space, axis, dft = False: lambda val: (
    val - (space.freq_slices if dft else space.slices)[axis].start) / (
    space.dF if dft else space.dR)[axis]
vals2inds_gen = lambda sp, dft_axes: lambda *vals: (
        val2i(sp, axi, axi in dft_axes)(vali)
        for axi, vali in
        zip(count(), vals))
warp = lambda *args, **kwargs: (
    _warp(np.real(args[0]), *args[1:], **kwargs)
    + 1j * _warp(np.imag(args[0]), *args[1:], **kwargs)
) if args[0].dtype == 'complex' else _warp(args[0]*1.,*args[1:], **kwargs)
def unit_formatter(unit_name, divby):
    lookup = {
            'def' : lambda x:'${:.3g}{}$'.format(x, unit_name),
        -1 : '$-{}$'.format(unit_name),
        0. : '$0$',
        1 : '${}$'.format(unit_name),
    }
    func = lambda x: lookup[x] if x in lookup else lookup['def'](x)
    formatter = FuncFormatter(lambda x,fuck: func(x/divby))
    return formatter

def gridder(
    xmaj = None, 
    xmin = None, 
    ymaj = None, 
    ymin = None, 
    majls = '-', 
    minls = ':', 
    lc = 'grey',
): 
    axes = plt.gca()
    scales = axes.get_xscale(), axes.get_yscale()
    for mi, maj, axis, an, scale in zip(
        (xmin, ymin), 
        (xmaj, ymaj), 
        (axes.xaxis, axes.yaxis), 
        'xy', 
        scales,
    ):
        if maj is not None: 
            if scale == 'linear':
                locator = MultipleLocator(maj)
            else:
                locator = LogLocator(base = maj)
            axis.set_major_locator(locator)
            plt.grid(
                b = maj is not None 
                    or (xmaj == xmin == ymaj == ymin == None),
                which = 'major',
                axis = an, 
                linestyle = majls, 
                c = lc, 
                alpha = .75, 
                linewidth =.7
            )
            axis.set_major_formatter(FuncFormatter(lambda val, loc: f'{val:.3g}'))
        if mi is not None or scale == 'log': 
            if scale == 'linear':
                locator = MultipleLocator(mi)
            else:
                locator = LogLocator(maj, subs = np.arange(0,maj,mi))
            axis.set_minor_locator(locator)
            plt.grid(
                b = mi is not None, 
                which = 'minor',
                axis = an, 
                linestyle = minls if mi is not None else (0, (0,1)), 
                c = lc, 
                alpha = .75, 
                linewidth =.7
            )
            axis.set_minor_formatter(FuncFormatter(lambda val, loc: ''))

def space_warp(source, dest, func_dest2source,
        source_dft_axes = None, dest_dft_axes = None, mode = 'constant'):
    """
    Helps to perform a geometric transform between spatial coordinates.
    Works for 1-1 mappings, so not things like Fourier transforms.
    Creates a warp function like scikit-image's transform.warp, which
    can be called with a field from the source space and returns the
    transformed field in the destination space. Works for real or complex
    fields, and if transforming to/from DFT axes, then maintains
    oversampling due to zero-padding factors.
    
    Parameters:
        source : Space instance to which input fields will belong
        dest : Space instance to which output fields will belong
        func_dest2source : callable, with a destination field coordinate as
            inputs, and returns a tuple of associated source field coordinates
        source_dft_axes : tuple of source axes which will be DFT axes, e.g.
            if transforming from the X-frequency domain and Y-time domain, then
            use (0,) or 0. None is the same as ().
        dest_dft_axes : tuple of destination axes which will be DFT axes
        mode : mode to use when retreiving values outside the range of the
            source; matches numpy.pad options.
    
    Returns:
        warper : callable, which when called with a source field as argmument
            will return the associated destination field.
    """

    dest_dft_axes = to_iter(dest_dft_axes)
    source_dft_axes = to_iter(source_dft_axes)
    func_coords2inds = vals2inds_gen(source, source_dft_axes)

    dest_ogrid = tuple(Fi if i in dest_dft_axes else Ri
                              for i, (Fi, Ri)
                              in enumerate(zip(dest.F, dest.R)))
    source_mgrid = func_dest2source(*ogrid2mgrid(dest_ogrid))
    source_mgrid = (source_mgrid[None]
            if shapeof(source_mgrid) == source.shape
            else source_mgrid)
    source_inds = np.stack(tuple(func_coords2inds(*source_mgrid)))
    warper = lambda source_field: warp(source_field, source_inds, mode = mode)
    return warper

nonedef = lambda inp, default: default if inp is None else inp

def StrSpace(*axis_details):
    '''Space initialiser function, where a string
is given for each dimension in the format:
'Name / units [Frequency name / units]'
where any component is optional, as well as spaces.
Alternatively, tuples of each component string can be given
instead of strings, with None being given for components
which are unspecified.
The frequency name is shown when the DFT functionality of
the space is used. The slices of the space are not
defined here, and should be set by the getitem method
(instance[0:10:0.1] e.g.).
'''
    def string2args(string):
        if '[' in string:
            sep = string.index('[')
            lastpart = string[sep + 1:-1]
            if '/' in lastpart:
                freq_name, freq_unit = (part.strip(' ') for part in lastpart.split('/'))
            else:
                freq_name = lastpart.strip(' ')
                freq_unit = None
            string = string[:sep]
        else:
            freq_name, freq_unit = None, None
        if '/' in string:
            name, unit = (part.strip(' ') for part in string.split('/'))
        else:
            name = string.strip(' ')
            unit = None
        return name, unit, freq_name, freq_unit
    tupleExtend = lambda length, fillval = None: lambda tup: tuple((*tup, *([fillval] * max(0, length - len(tup)))))
    details = [
        string2args(deet) if type(deet) is str else tupleExtend(4)(deet)
        for deet in axis_details
    ]
    return Space(
        slices = [slice(None)] * len(details),
        axis_names = tuple(map(itemgetter(0), details)),
        axis_units = tuple(map(itemgetter(1), details)),
        freq_names = tuple(map(itemgetter(2), details)),
        freq_units = tuple(map(itemgetter(3), details)),
    )
    
class Space:
    def __init__(
        self, 
        slices, 
        axis_names = None, 
        axis_units = None,
        freq_names = None,
        freq_units = None,
        factors = 1, 
        vert_axes = None, 
        cmap = None, 
        dft_norm = 'ortho',
    ):
        '''
        Helper object for dealing with fields defined on
        an N-dimensional spatial coordinate system. Contains
        fields of the coordinates themselves, a template
        field of the appropriate shape, can generate, differentiate,
        and integrate fields, and helps to imshow slices of the fields.

        Parameters:
            slices: (required) one or iterable of slices, describing the spatial 
                    samples in each dimension
            axis_names: iterable of strings of axis names, not including units
            axis_units: iterable of strings of axis units, separated in order
                        to correctly write labels in DFT images
            factors: tuple of odd, positive integers, as default zero-padding
                     factors when doing a DFT
            vert_axes: which axes to prefer to imshow as the vertical axis, with
                       the first as the most preferred
            cmap: default cmap argument to pass to imshow for 2D plots
            dft_norm: the value passed to the 'norm' parameter in dft and idft calls
        '''
        self._field = None
        self.slices = list(to_iter(slices))
        self.vert_axes = vert_axes
        self.axis_names = nonedef(axis_names,[None]*self.ndim)
        self.axis_units = nonedef(axis_units,[None]*self.ndim)
        self.freq_names = nonedef(freq_names, [None]*self.ndim)
        self.freq_units = nonedef(freq_units, [None]*self.ndim)
        self.cmap = cmap
        self.dft_norm = dft_norm
        self.factors = factors
        
    @property
    def dft_extent(self):
        return slices2extents(self.freq_slices)
    @property
    def dF(self):
        def time2df(timeslice, pad_factor):
            n = int(
                (timeslice.stop - timeslice.start) 
                // timeslice.step + 1
            ) * pad_factor
            d = timeslice.step
            df = 1 / (n * d)
            return df
        return tuple(
            time2df(timeslice, pad_factor)
            for timeslice, pad_factor
            in zip(self.slices, self.factors)
        )
    @property
    def dR(self):
        return tuple(s.step for s in self.slices)
    @property
    def extent(self):
        return slices2extents(self.slices)
    @property
    def factors(self):
        return self._factors
    @factors.setter
    def factors(self, factors):
        factors = (
            np.ones(self.ndim) * factors 
            if type(factors) == int 
            else np.array(factors)
        ).astype(int)
        assert np.all(factors > 0), \
               'factors {} must all be positive numbers'.format(
                       str(factors))
        self._factors = factors
    @property
    def field(self):
        return self._field
    @field.setter
    def field(self, field):
        self._compatible_field_slices(field, self.slices)
        self._field = field
    @property
    def freq_period(self):
        return tuple(
            sl.step * shi
            for sl, shi 
            in zip(self.freq_slices, self.freq_shape)
        )
    @property
    def freq_shape(self):
        return tuple(
            int((sl.stop - sl.start) / sl.step) + 1
            for sl 
            in self.freq_slices
        )
    @property
    def freq_slices(self):
        def time2freq(timeslice, pad_factor):
            n = int(
                (timeslice.stop - timeslice.start) 
                // timeslice.step + 1
            ) * pad_factor
            d = timeslice.step
            val = 1 / (n * d)
            f0 = -(n//2) * val
            f1 = ((n-1)//2 + .5) * val
            df = val
            return slice(f0, f1, df)
        return tuple(
            time2freq(timeslice, pad_factor)
            for timeslice, pad_factor
            in zip(self.slices, self.factors)
        )
    @property
    def F(self):
        return np.ogrid[self.freq_slices]
    @property
    def ndim(self):
        return len(self.slices)
    @property
    def offset(self):
        return tuple(map(lambda sl: sl.start, self.freq_slices))
    @property
    def period(self):
        return tuple(
            sl.step * shi
            for sl, shi 
            in zip(self.slices, self.shape)
        )
    @property
    def R(self):
        return np.ogrid[self.slices]
    @property
    def shape(self):
        return tuple(
            int((sl.stop - sl.start) / sl.step) + 1
            for sl 
            in self.slices
        )
    @property
    def size(self):
        return reduce(np.multiply, self.shape)
    @property
    def slices(self):
        slices = self._slices_unadjusted
        res = []
        for sli in slices:
            start, stop, step = sli.start, sli.stop, sli.step
            n = (stop - start) / step
            stop = (
                start + (round(n) - 0.5) * step
                if (((n + 0.5) % 1) - 0.5) ** 2 < 1e-20
                else stop
            )
            res.append(slice(start, stop, step))
        return res
    @property
    def _slices_unadjusted(self):
        res = []
        for i, sli in enumerate(self._slices):
            start, stop, step = sli.start, sli.stop, sli.step
            start = 0 if start is None else start
            step = 1 if step is None else step
            if self.field is None:
                assert stop is not None, (
                    f'Slice index {i} has no step and there is no field.'
                )
            else:
                stop = start + (self.field.shape[i]) * step
            res.append(slice(start, stop, step))
        return res
    @slices.setter
    def slices(self, slices):
        if self.field is not None:
            self._compatible_field_slices(self.field, slices)
        self._slices = slices
    @property
    def vert_axes(self):
        return self._vert_axes
    @vert_axes.setter
    def vert_axes(self, vert_axes):
        vat = [i for i in to_iter(vert_axes) if i is not None]
        for i in range(self.ndim -1, -1, -1, ):
            if i not in vat:
                vat.append(i)
        self._vert_axes = tuple(vat)
    def textcoord(self, axis, text):
        '''Converts a string coordinate such as
10% or 0.1 to the value at the given fraction along
the given axis.'''
        sl = self.slices[axis]
        period = self.period[axis]
        val = (
            float(text[:-1]) / 100 if text.endswith('%') 
            else float(text)
        )
        return sl.start + val * period
    def _compatible_field_slices(self, field, slices):
        if field is None: return
        fnd = field.ndim
        lsl = len(slices)
        assert fnd == lsl, (
            f'Field number of dimensions ({fnd}) does not equal'
            f'number of slices ({lsl})'
        )
        for i, (fshi, sli) in enumerate(zip(field.shape, slices)):
            dof = sum(
                1 for thing in (sli.start, sli.stop, sli.step) 
                if thing is None
            )
            if dof == 0:
                slsh = int((sli.stop - sli.start) / sli.step + 1)
                assert slsh in (fshi, 1), (
                    f'Field shape index {i} ({fshi}) does not equal '
                    f'space slice shape {slsh}'
                )
    def __getitem_tocoords(self, slices):
        '''Takes a set of __getitem__ arguments
and does some magic on complex values. Pads
out the input to match the space ndim.

For each given value, if it's a complex number nj, it
is converted to the n-th coordinate in the current
sampling of the relevant axis, and can be a decimal.

For slices, complex start and stop values are converted
the same way, while a complex step value is regarded
in units of the current stepsize.

If None is passed insead of a number or slice, then
it is substituted with the mid-point of the axis.

Example: Original axis is slice(0, 10, 0.2),
    argument is slice(10j, 40).
    Becomes (2, 40, 0.2)  
Example: slice(40, 55, 100j)
    Becomes slice(40, 55, 15 / 99) .
Example: slice(40, 55, 0.5)
    Stays unchanged.'''
        new_slices = []
        slices = list(slices[:self.ndim]) + (self.ndim - len(slices)) * [slice(None)]
        for i, (sl, sl0) in enumerate(zip(
            slices, self._slices_unadjusted
        )):
            if type(sl) == slice:
                start = nonedef(sl.start, sl0.start)
                stop = nonedef(sl.stop, sl0.stop)
                step = nonedef(sl.step, sl0.step)
                start, stop, step = [
                    self.textcoord(i, s) if type(s) == str else s
                    for s in (start, stop, step)
                ]
                if type(start) is complex:
                    start = start.imag
                    start = start % self.shape[i] if start < 0 else start
                    start = sl0.start + start * sl0.step
                if type(stop) is complex:
                    stop = stop.imag
                    stop = stop % self.shape[i] if stop < 0 else stop
                    stop = sl0.start + stop * sl0.step
                if type(step) is complex:
                    step = step.imag * sl0.step
                sl_new = slice(start, stop, step)
            elif sl is None:
                try:
                    sl_new = sl0.start + self.shape[i] / 2 * sl0.step
                except TypeError:
                    sl_new = None
            elif type(sl) is complex:
                try:
                    sl_new = sl0.start + (sl.imag % self.shape[i]) * sl0.step
                except TypeError:
                    sl_new = None
            else:
                sl_new = sl
            new_slices.append(sl_new)
        return tuple(new_slices)
    def __getitem_indsnear(self, slices):
        '''Converts __getitem__ arguments to slices or values
of integer indices of the current space sampling, mapping to
coordinates which are closest to the argument samples. The input
is passed to __getitem_tocoords before calculation.'''
        
        new_slices = []
        slices = self.__getitem_tocoords(slices)
        for i, (sl, sl0) in enumerate(zip(
            slices, self.slices
        )):
            if type(sl) == slice:
                start = int(round(self.coord2ind(i, sl.start, clip = False)))
                stop = int(np.ceil(self.coord2ind(i, sl.stop, clip = False)))
                step = int(round(sl.step / sl0.step))
                step = step if step else 1
                sl_new = slice(start, stop, step)
            else:
                sl_new = int(round(self.coord2ind(i, sl)))
            new_slices.append(sl_new)
        return tuple(new_slices)
    def __getitem_inds2coords(self, slices, clip = False):
        '''Converts index slices to coordinates of the current
sampling.'''
        return tuple(
            slice(*(
                self.ind2coord(axis, ind, clip = clip)
                for ind in (sl.start, sl.stop - .5)
            ), sl0.step * sl.step)
            if type(sl) == slice
            else self.ind2coord(axis, sl, clip = clip)
            for axis, (sl, sl0) in enumerate(zip(
                slices, self.slices
            ))
        )
    
    def __getitem__(self, slices):
        '''Works in one of two ways. If there is a field
assigned to the space, then the getitem arguments are adjusted
to the nearest current samples and the field is sliced as well.
The space and the field are returned as a tuple. Otherwise,
the arguments are used precisely to give a new space with the given
axes.'''
        slices = to_iter(slices)
        slices = list(slices) + [slice(None)] * max(0, self.ndim - len(slices))
        assert len(slices) == self.ndim, (
            f'Provided more slices ({len(slices)}) than space dimensions ({self.ndim})')
        if self.field is None:
            coordslices = self.__getitem_tocoords(slices)
            field = None
        else:
            indslices = self.__getitem_indsnear(slices)
            coordslices = self.__getitem_inds2coords(indslices)
            lc = len(coordslices)
            fnd = self.field.ndim
            assert lc == fnd, (
                f'Should have as many coordslices ({lc}) as field dimensions ({fnd})'
            )
            field = self.field[tuple(
                slice(None)
                if shi == 1 and type(indslice) == slice
                else indslice
                for indslice, shi
                in zip(indslices, self.field.shape)
            )]
        axes2keep = [
            i for i,sl in enumerate(coordslices)
            if type(sl) == slice
        ]
        sp = Space(**self.properties)
        sp.slices = [coordslices[i] for i in axes2keep]
        sp.axis_names = [sp.axis_names[i] for i in axes2keep]
        sp.axis_units = [sp.axis_units[i] for i in axes2keep]
        sp.freq_names = [sp.freq_names[i] for i in axes2keep]
        sp.freq_units = [sp.freq_units[i] for i in axes2keep]
        sp.field = field
        return sp
        
    def __iter__(self):
        sp = self.copy()
        sp._field = None
        yield sp
        if self.field is not None:
            yield self.field
        
    def __add__(self, other):
        '''Magic for adding together spaces for extending
axes, or assigning a field to a space instance
before performing an operation on the result.'''
        if type(other) == type(self):
            sp = Space(
                (*self.slices, *other.slices,),
                (*self.axis_names, *other.axis_names,),
                (*self.axis_units, *other.axis_units,),
                (*self.freq_names, *other.freq_names,),
                (*self.freq_units, *other.freq_units,),
                (*self.factors, *other.factors,),
                (*self.vert_axes, *(vi + self.ndim for vi in other.vert_axes),),
                self.cmap,
                self.dft_norm,
            )
            if self.field is None:
                sp = sp + self.field[tuple((
                    *(slice(None) for i in range(self.ndim)),
                    *(None for i in range(other.ndim)),
                ))]
            if other.field is None:
                sp = sp + other.field[tuple((
                    *(None for i in range(self.ndim)),
                    *(slice(None) for i in range(other.ndim)),
                ))]
            return sp
        elif type(other) == np.ndarray:
            sp = self.copy()
            sp.field = other
            return sp
    @property
    def properties(self):
        '''Contains the defining properties of the space as a dict,
which could be used to make a new Space instance.'''
        return {
            'slices' : self.slices,
            'axis_names' : self.axis_names, 
            'axis_units' : self.axis_units,
            'freq_names' : self.freq_names,
            'freq_units' : self.freq_units,
            'factors' : self.factors, 
            'vert_axes' : self.vert_axes, 
            'cmap' : self.cmap, 
            'dft_norm' : self.dft_norm,
        }
    def copy(self):
        sp = Space(**self.properties)
        sp._field = self._field
        return sp
    _axnames_converter = lambda self, axes: tuple(
        self.axis_names.index(axis) 
        if type(axis) is str 
        else axis
        for axis in axes
    )
    _axes_fixer = lambda self, axes: (
        range(self.ndim) 
        if axes is None 
        else self._axnames_converter(to_iter(axes))
    )
    def generate_field(self, func=None, dft_axes = None,
            origin = False, split = True):
        '''
        Evaluates a given function on the coordinate space of this instance.

        Parameters:
            func : Function which takes the ogrid of coordinates as an argument
                and returns the value of the field. If not provided, then a
                zero-field is used.
            dft_axes : Which axes the function will expect to be frequency
                coordinates
            origin : Whether to pass time-domain coordinate axes shifted to
                be centred on the origin, helpful for designing convolution
                kernels.
            split : Whether func expects separate arguments for coordinates
                of each axis, e.g. func(X, Y Z) rather than func(R)
        Returns:
            Either the function evaluated on the space, or a zero field.
        '''
        dft_axes = self._axnames_converter(to_iter(dft_axes))
        args = tuple((Fi if axis in dft_axes
                      else (Ri - Ri.mean() if origin else Ri))
                for Fi, Ri, axis in zip(self.F, self.R, count()))
        func = (
            (
                (lambda *R: sum(R) * 0)
                if split
                else (lambda R: sum(R) * 0)
            )
            if func is None else func
        )
        return func(*(args if split else (args,)))

    def pad(self, field = None, axes = None, mode= 'zeros'):
        '''
        Pads the field with zeros s.t. its shape elements extend to
        the given integer factors.

        Parameters:
            field : field to pad; if unspecified then space's field is used
            axes : which axes to pad
            mode : if this is 'reverse' then pads with tiles of back-to-front
                field (for use of convolve method).
        Returns:
            Padded field
        '''
        internal = field is None
        if internal: 
            assert self.field is not None, (
                'If not providing a field then the space must'
                'contain a field (by addition).'
            )
            self, field = self
        fsh = field.shape
        axes = self._axes_fixer(axes)
        axes = [
            i 
            for i, shape 
            in enumerate(field.shape) 
            if shape > 1 and i in axes
        ]
        factors = [f if i in axes else 1 for i, f in enumerate(self.factors)]
        newshape = tuple(map(np.product, zip(fsh, factors)))
        res = np.zeros(newshape, dtype = field.dtype)
        if mode == 'zeros':
            middlebit = tuple(
                slice((nsh - osh) // 2, (nsh + osh) // 2, 1)
                for nsh, osh in zip(newshape, fsh)
            )
            res[middlebit] = field
        elif mode == 'reverse':
            for indices in product(*map(range,factors)):
                res[tuple(
                    slice(index * shi, (index + 1) * shi, 1)
                    for index, shi in zip(indices, fsh)
                )] = field[tuple(
                    slice(None, None, -1 + 2 * ((index + (factors[i] % 2) * (factors[i] // 2 - 1)) % 2))
                    for i, index in enumerate(indices)
                )]
            shifts = tuple(((fi - 1) * shi // 2) % shi
                    for fi, shi in zip(factors, fsh))
            res = reduce(lambda sofar, i_n_shift: np.roll(
                sofar, 
                shift = i_n_shift[1],
                axis = i_n_shift[0],
            ), enumerate(shifts), res)
        else:
            raise NotImplementedError(
                    'mode value \'{}\' not supported'.format(mode))
        return self + res if internal else res

    def unpad(self,field = None, axes = None):
        '''
        Unpads the field, given that it was originally padded
        with the given factors in the given axes.
        '''
        internal = field is None
        if internal: 
            assert self.field is not None, (
                'If not providing a field then the space must'
                'contain a field (by addition).'
            )
            self, field = self
        fsh = field.shape
        axes = self._axes_fixer(axes)
        axes = [
            i 
            for i, shape 
            in enumerate(field.shape) 
            if shape > 1 and i in axes
        ]
        slices = tuple(
            slice(*(
                olshi * (fi + j) // (2 * fi) 
                for j in (-1, 1)
            ))
            if i in axes and olshi > 1 
            else slice(None,)
            for i, (olshi, fi) 
            in enumerate(zip(field.shape, self.factors))
        )
        res = field[slices]
        return self + res if internal else res

    def _offset_tilter(self, axes = None):
        axes = self._axes_fixer(axes)
        axes = to_iter(axes)
        return self.generate_field(
            lambda F: np.exp(
                1j * 2 * np.pi
                * sum(
                    ((offi % peri) + ((shi + 1) // 2) * dRi) * Fi
                    for i, (Fi, offi, peri, shi, dRi)
                    in enumerate(zip(
                        F, 
                        self.offset, 
                        self.period, 
                        self.shape, 
                        self.dR,
                    ))
                    if i in axes
                )
            ),
            split = False,
            dft_axes = range(self.ndim)
        )

    def dft(self, field = None, axes = None, mode = 'zeros',
            offset_adjust = False):
        '''
        Performs a unitary discrete FT on the field in the given dimensions,
        with the appropriate zero-padding factors.

        Parameters:
            field : field to DFT
            axes : which axes to DFT in
            mode : if this is 'reverse' then pads with tiles of back-to-front
                field (for use of convolve method.
            offset_adjust : whether to multiply by a complex tilt in line with
                the fact that the time-domain field may not be centred on
                the origin.
        Returns:
            DFTed field
        '''
        internal = field is None
        if internal: 
            assert self.field is not None, (
                'If not providing a field then the space must'
                'contain a field (by addition).'
            )
            self, field = self
        axes = self._axes_fixer(axes)
        field_pad = self.pad(field, axes, mode)
        myfft = lambda field, axis: fftshift(
            fft(
                fftshift(
                    field,
                    axes = axis,
                ), 
                axis = axis, 
                norm = self.dft_norm,
            ), 
            axes = axis,
        )
        res = reduce(
            myfft,
            axes, 
            field_pad,
        )
        res = res / self._offset_tilter(axes) if offset_adjust else res
        return self + res if internal else res

    def idft(self, field = None, axes = None, offset_adjust = False):
        '''
        Performs a unitary inverse discrete FT on the field in the given
        dimensions, with the desired zero-padding factors.

        Parameters:
            field : field to IDFT
            axes : which axes to IDFT
            offset_adjust : whether to multiply by a complex tilt in line with
                the fact that the time-domain field may not be centred on
                the origin.
        Returns:
            IDFTed field
        '''
        internal = field is None
        if internal: 
            assert self.field is not None, (
                'If not providing a field then the space must'
                'contain a field (by addition).'
            )
            self, field = self
        axes = self._axes_fixer(axes)
        field = (field * self._offset_tilter(axes)
                if offset_adjust else field)
        myifft = lambda field, axis: ifftshift(
            ifft(
                ifftshift(
                    field,
                    axes = axis,
                ), 
                axis = axis, 
                norm = self.dft_norm,
            ), 
            axes = axis,
        )
        idfted = reduce(
            myifft,
            axes, 
            field,
        )
        field_unpad = self.unpad(idfted, axes)
        return self + field_unpad if internal else field_unpad
    
    def convolve(self, field = None, kernel = None, axes = None, mode = 'zeros',):
        '''
        Convolves the field with the kernel. Real/complex-ness is preserved.

        Parameters:
            field : ndarray of subject field
            kernel : ndarray of convolution kernel
            axes : int or tuple thereof, of axes over which to convolve. The
                    kernel must have len 1 dimensions in the remaining axes.
            mode : padding mode to apply to field, out of 'zeros', 'reverse'
        '''
        internal = field is None
        if internal: 
            assert self.field is None, (
                'If not providing a field then the space must'
                'contain a field (by addition).'
            )
            self, field = self
        if type(kernel) == Space:
            _, kernel = kernel
        res_complex = any((f.dtype == np.complex128 for f in (field, kernel)))
        axes = self._axes_fixer(axes)
        dfts = tuple(self.dft(thing, axes, mode = modei, offset_adjust = False)
            for thing, modei
            in zip((field, kernel), (mode, 'zeros',)))
        multiplied = np.multiply(*dfts)
        res = self.idft(multiplied, axes)
        res = res if res_complex else res.real
        mult = reduce(
            np.multiply,
            map(
                lambda i: (self.shape[i] * self.factors[i]) ** .5 * self.dR[i],
                axes
            ),
            1,
        )
        res = res * mult
        return self + res if internal else res

    def differentiate(self, field = None, axis = 0):
        '''
        Performs a Fourier differentiation on the given field along one axis.
        Real/complex-ness is preserved.

        Parameters:
            field : Field to differentiate
            axis : Axis along which to perform differentiation
        Returns:
            d/d(axis) [field]
        '''
        internal = field is None
        if internal: 
            assert self.field is not None, (
                'If not providing a field then the space must'
                'contain a field (by addition).'
            )
            self, field = self
        res_complex = field.dtype == np.complex128
        f_dft = self.dft(field, axes = axis)
        v = self.F[axis]
        diff_dft = 1j * 2 * np.pi * v * f_dft
        diff = self.idft(diff_dft, axes = axis)
        diff = diff if res_complex else diff.real
        return self + diff if internal else diff


    def integrate(self, field = None, axis = 0):
        '''
        Performs a Fourier integration on the given
        field along one axis.
        Parameters:
            field : Field to integrate
            axis : Axis along which to perform integration
        Returns:
            \int d(axis) [field]
        '''
        internal = field is None
        if internal: 
            assert self.field is not None, (
                'If not providing a field then the space must'
                'contain a field (by addition).'
            )
            self, field = self
        res_complex = field.dtype == np.complex128
        f_dft = self.dft(field, axes = axis)
        v = self.F[axis]
        int_dft = 1j * f_dft * v / (v * v + (v == 0))
        int_t = self.idft(int_dft, axes = axis)
        int_t = int_t if res_complex else int_t.real
        return self + int_t if internal else int_t

    def label_gen(self, axes, dft_axes = ()):
        '''
        Generates axis labels for plots.

        Parameters:
            axes : tuple of axes for which to generate
            dft_axes : which axes will be frequency-domain
        Returns:
            label or tuple of labels
        '''
        axes = self._axes_fixer(axes)
        defs = 'XYZACBDEFGH'
        nameunit2label = lambda name, unit: name if unit is None else name + ' / ' +  unit
        namesunits = [
            (
                (
                    nonedef(self.freq_names[axis], '$\\nu_'+ defs[axis] + '$')
                    if axis in dft_axes
                    else nonedef(self.axis_names[axis], defs[axis])
                ), (
                    self.freq_units[axis]
                    if axis in dft_axes
                    else self.axis_units[axis]
                )
            )
            for axis in axes
        ]
        labels = [
            nameunit2label(n,u)
            for n, u in namesunits
        ]
        return labels
    

    def coord2ind(self, axis, coord, dft = False, clip = True):
        '''
        Converts a coordinate to the index at which it appears; may not be
        an integer.

        Parameters:
            axis : which axis
            coord : Coordinate
            dft : Whether it's frequency domain
            clip : Whether to clip at the limits of the field support
        Returns:
            index as a float
        '''
        sl = (self.freq_slices if dft else self.slices)[axis]
        coord_clipped = max(sl.start, min(sl.stop - sl.step, coord)) if clip else coord
        ind = (coord_clipped - sl.start) / sl.step
        return ind
    def ind2coord(self, axis, ind, dft = False, clip = True):
        sl = (self.freq_slices if dft else self.slices)[axis]
        ind = ind % self.shape[axis] if clip else ind
        return sl.start + ind * sl.step

    def coord_near(self, axis, coord, dft = False):
        '''
        Returns the sampled coordinate nearest to a given coordinate.

        Parameters:
            axis : which axis
            coord : Coordinate
            dft : Whether it's frequency domain
        Returns:
            Coordinate nearest to coord that appears in self.R[axis]
        '''
        sl = (self.freq_slices if dft else self.slices)[axis]
        near_ind = round(self.coord2ind(axis, coord, dft))
        val = sl.start + sl.step * near_ind
        return val

    def show(self, field = None, title = None, axes = None, coordinates = None,
            lims = None, show = False, dft_axes = None, vert_axis = None,
            norm = None, titleas = None, origin = 'lower', vmin = None,
            vmax = None, colorbar = True, unit_name = None,
            dft = None, symm_vms = False, **kwargs):
        '''
        Produce an imshow or plot of a cross-section of the field.
        Parameters:
            field : Field to show - if a field has been literally added
                to the space then this parameter can be None, making that field
                be shown.
            title : Title to show
            axes : Axes or axis to show
            coordinates : Coordinates of the remaining dimensions at which
                to slice the field. If None, or one of the values is None,
                or not provided, then central coordinate will be used.
            lims : 1 or 2 length 2 iterables, giving the limits of the  axes
                to show, if not the whole extent.
            show : Whether to call pyplot.show at the end
            dft_axes : Which axes (out of all axes) will be frequency-domain
            dft : Set this to True to simply treat all axes as frequency-domain
            vert_axis : which axis (out of all axes) to imshow as vertical axis
            norm : A value of either 'log' or 'linear' will give either 
                logarithmic or linear colors or yscale. Alternatively
                a matplotlib.colors norm instance can be given to pass to
                pyplot.imshow
            titleas : In the case of a 1D plot, whether to use title as the
                title above the plot ('title'), the y-axis label ('ylabel'),
                or the legend label ('legend')
            origin : For 2D plots, whether the y axis lowest coordinate should
                be 'lower' or 'upper' in the image
            vmin/vmax : imposed limits on either the colorbar (2D) or ylims (1D)
            symm_vms : whether to set symmetrical colour limits; if vmin/vmax
                provided, then the greater value will be used
            colorbar : For 2D plots, whether to make a colorbar
            unit_name : name of the unit to show on ticks, e.g. \pi, 2\pi
                        instead of 1, 2. Don't use $ signs as they will be
                        inserted internally. Or leave blank for just numbers.
            **kwargs : All remaining kwargs are sent to pyplit.imshow
        Returns:
            mappable of the image, or plot line
        '''
        field = self.field if field is None else field
        axes = self._axes_fixer(axes)
        axes = axes[:2]
        dft_axes = nonedef(dft_axes, ())
        dft_axes = dft_axes if dft is None else tuple(range(self.ndim))
        axes, dft_axes = (tuple(axis % self.ndim for axis in ax_list)
                for ax_list in map(to_iter, (axes, dft_axes)))
        slices4image = []
        labels = self.label_gen(axes, dft_axes)
        coordinates = kwargs.get('coords', coordinates)
        coordinates = (coordinates if coordinates is None
                else iter(to_iter(coordinates)))
        for j in range(self.ndim):
            if j in axes:
                slices4image.append(slice(None))
            else:
                c_def = (self.F if j in dft_axes else self.R)[j].mean()
                coord = c_def if coordinates is None else next(coordinates)
                coord = c_def if coord is None else coord
                ind = self.coord2ind(j, coord, j in dft_axes)
                ind *= field.shape[j] / (self.freq_shape if j in dft_axes
                                         else self.shape)[j]
                ind = 0 if field.shape[j] == 1 else ind
                slices4image.append(int(ind))
        normer = bool(len(dft_axes))
        default_norm = (
                'log'
                if bool(len(dft_axes))
                and field.dtype != bool
                else 'linear'
        )
        norm = default_norm if norm is None else norm
        field = field.astype(int) if field.dtype == bool else field
        toshow = np.absolute(field) if norm == 'log' else field.real
        if norm == 'log':
            smallnum = toshow.max() / 2 ** 512 / 2 ** 512
            toshow[toshow <= smallnum] = toshow[toshow > smallnum].min()
        if unit_name is not None:
            
            formatter = unit_formatter(unit_name, 1)
        else:
            formatter = ScalarFormatter(useMathText=True)
        if len(axes) == 2:
            if vert_axis is None:
                try:
                    vert_axis = next(ax for ax in self.vert_axes if ax in axes)
                except StopIteration:
                    vert_axis = axes[-1]
                
            transposing = vert_axis == axes[-1]
            transposer = lambda im: im.T if transposing else im
            extent_padder = lambda ext, fact: (ext - ext.mean()) * fact + ext.mean()
            extent = reduce(
                lambda sofar, axis: sofar + (
                    extent_padder(self.dft_extent[axis],self.factors[axis])
                    if axis in dft_axes 
                    else self.extent[axis]
                ).tolist(),
                axes[::-1+2*transposing],
                []
            )
            if origin == 'upper':
                extent[-2:] = extent[:-3:-1]
            imnorm = colors.LogNorm if norm == 'log' else colors.Normalize
            toshow = transposer(toshow[tuple(slices4image)])
            vm = max(map(abs,filter(lambda x: x is not None, (vmin,vmax))), default = None)
            vmin = toshow.min() if vmin is None else vmin
            vmax = toshow.max() if vmax is None else vmax
            vmd = max(map(abs,(vmin,vmax)))
            vmin, vmax = ((-vmd, vmd) if vm is None else (-vm, vm)) if symm_vms else (vmin, vmax)
            im = plt.imshow(
                    toshow,
                    origin = origin,
                    extent = extent,
                    aspect = kwargs.pop(
                        'aspect',
                        1
                        if self.axis_units[axes[0]] == self.axis_units[axes[1]]
                        and not sum(ax in dft_axes for ax in axes) % 2
                        else 'auto'
                    ),
                    norm = imnorm(vmin = vmin, vmax = vmax),
                    cmap = kwargs.pop('cmap', self.cmap), 
                    **kwargs)
            sl = slice(None, None, -1 + 2 * transposing)
            for i, (flab, flim) in enumerate(zip(
                    (plt.xlabel, plt.ylabel),
                    (plt.xlim, plt.ylim)
            )):
                flab(labels[sl][i])
                if lims is not None:
                    flim(lims[sl][i])
            if colorbar:
                ax = plt.gca()
                f = plt.gcf()
                ext = sum(map(list, (plt.xlim(), plt.ylim(), )), [], )
                asp = ax.get_aspect()
                asp = 1 if asp == 'equal' else asp
                coord_ext = abs(ext[1] - ext[0]), abs(ext[2] - ext[3])
                bb = ax.bbox._bbox
                fracs = (bb.width, bb.height)
                inches = f.get_size_inches()
                if asp == 'auto':
                    aw = f.get_size_inches()[0] * bb.width
                else:
                    bigsize = list(
                        inch * frac
                        for inch, frac
                        in zip(inches, fracs)
                    )
                    needed_aspect = coord_ext[1] * asp / coord_ext[0]
                    big_aspect = bigsize[1] / bigsize[0]
                    if needed_aspect > big_aspect:
                        bigsize[0] = bigsize[1] / needed_aspect
                    aw = bigsize[0]
                fract = .125 / aw
                divider = make_axes_locatable(ax)
                cax = divider.append_axes(
                    "right", 
                    size="{}%".format(100 * fract), 
                    pad=.125
                )
                cb = plt.colorbar(im, cax = cax)
                plt.sca(ax)
                if norm == 'linear':
                    cb.formatter = formatter
                    cb.update_ticks()
            if title:
                plt.gca().set_title(title)
        elif len(axes) == 1:
            titleas = nonedef(titleas, 'legend')
            sl = (self.freq_slices if axes[0] in dft_axes else self.slices
                    )[axes[0]]
            y = toshow[tuple(slices4image)]
            p = (1 / self.dR[axes[0]] if axes[0] in dft_axes
                    else self.period[axes[0]])
            s = toshow.shape[axes[0]]
            x = np.arange(s) * p / s + sl.start
            im = plt.plot(x, y, label = title if titleas == 'legend' else None,
                    **kwargs)
            plt.xlabel(labels[0])
            if lims:
                plt.xlim(lims)
            plt.grid(True)
            if norm == 'log':
                plt.gca().set_yscale('log')
            else:
                plt.gca().yaxis.set_major_formatter(formatter)
            if any(vmi is not None for vmi in (vmin, vmax)):
                plt.ylim(vmin, vmax)
            if titleas == 'title':
                plt.title(title)
            elif titleas == 'legend':
                if title is not None:
                    plt.legend()
            elif titleas == 'ylabel':
                plt.ylabel(title)
            else:
                raise NotImplementedError('titleas value \'{}\' not supported'
                        .format(titleas))
        else:
            raise NotImplementedError('Showing of {} axes ({}) is not supported'
                    .format(len(axes), axes))
        if show:
            plt.show()
        return (im, cb) if len(axes ) == 2 and colorbar else im
