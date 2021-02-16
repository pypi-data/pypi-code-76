"""
Abstraction of plotting with arbitrary plotting apis (backends)
"""
import typing
import warnings
import abc
import pickle
import rna.pattern.backend
import rna


def plot_method(fun):
    """
    This is a decorator which ensures that you pass an axes instance either
        as first argument
    or
        as keyword arugment axes=<axes instance>
    and/or
        you specify the dimension of the axes object ot be generated dim=<dimension>
    Decorator for ApiBackend plot methods.
    """

    def wrapper(self, *data, **kwargs):
        axes = kwargs.pop("axes", None)
        dim = kwargs.pop("dim", None)

        if data:
            if self.is_axes(data[0]):
                if axes is not None and axes is not data[0]:
                    raise ValueError("Conflicting axes passed as arg and kwarg")
                axes = data[0]
                data = data[1:]

        if axes and dim:
            if dim != self.axes_dim(axes):
                raise ValueError(
                    "Axes dimension and dim argument in conflict:"
                    "{self.dim} vs {dim}".format(**locals())
                )
        if axes is None:
            axes = self.gca(dim=dim)

        return fun(self, axes, *data, **kwargs)

    return wrapper


class ApiBackend(
    rna.pattern.backend.Backend, rna.polymorphism.Plottable, rna.polymorphism.Storable
):
    """
    Base class for a backend implementation for a Api subclass

    The plotting api backend is thought of as unified interface for plot arguments taking care of
        * interdependent arguments (axes/dimension, cmap/vmin/vmax, x_index,...)
        * color formating (format_colors)

    processing kwargs for plotting functions and providing easy
    access to axes, dimension and plotting method as well as indices
    for array choice (x..., y..., z_index)

    Examples:
        >>> import rna
        >>> from rna.plotting.backends.matplotlib import ApiBackendMatplotlib

        Dimension arguemnt (dim)
        >>> api = rna.plotting.Api()
        >>> api.backend = 'matplotlib'  # which is default anyway

        As a functionality of the Backend/Strategy pattern the backend is instantiated at
        access time
        >>> backend = api.backend
        >>> assert not isinstance(backend, str)
        >>> assert isinstance(backend, ApiBackendMatplotlib)

        Default dimension of the axis is 2
        >>> backend.axes_dim(backend.gca())
        2

        You can select the correct axes object with the dimension key
        >>> axes = ApiBackendMatplotlib.gca(dim=3)
        >>> backend.axes_dim(axes)
        3

        Switching the backend keeps the top level behaviour the same
        >>> api = rna.plotting.Api()
        >>> api.backend = 'pyqtgraph'
        >>> api.backend.axes_dim(api.backend.gca(dim=2))
        2

    """

    STRATEGY_MODULE_BASE = "rna.plotting.backends"

    @plot_method
    def plot_array(self, *args, **kwargs):
        warnings.warn("Use plot_tensor instead.", DeprecationWarning)
        return self.plot_tensor(*args, **kwargs)  # pylint: disable=no-member

    # dictionary methods
    @staticmethod
    def set(kwargs, attr, value):
        kwargs.kwargs[attr] = value

    @staticmethod
    def retrieve(kwargs, attr, default=None, keep=True):
        if keep:
            return kwargs.get(attr, default)
        return kwargs.pop(attr, default)

    @staticmethod
    def retrieve_chain(kwargs, *args, **retrieve_kwargs):
        default = retrieve_kwargs.pop("default", None)
        keep = retrieve_kwargs.pop("keep", True)
        if len(args) > 1:
            return ApiBackend.retrieve(
                kwargs,
                args[0],
                ApiBackend.retrieve_chain(
                    kwargs, *args[1:], default=default, keep=keep
                ),
                keep=keep,
            )
        if len(args) != 1:
            raise ValueError("Invalid number of args ({0})".format(len(args)))
        return ApiBackend.retrieve(kwargs, args[0], default, keep=keep)

    @staticmethod
    def get_norm_args(kwargs, vmin_default=0, vmax_default=1, cmap_default=None):
        """
        Examples:
            >>> import rna
            >>> from rna.plotting.backends.matplotlib import ApiBackendMatplotlib

            >>> rna.plotting.set_style()
            >>> ApiBackendMatplotlib.get_norm_args(dict(vmin=2, vmax=42))
            ('viridis', 2, 42)
        """
        if cmap_default is None:
            import matplotlib.pyplot as plt  # pylint: disable = import-outside-toplevel

            cmap_default = plt.rcParams["image.cmap"]
        cmap = kwargs.get("cmap", cmap_default)
        vmin = kwargs.get("vmin", vmin_default)
        vmax = kwargs.get("vmax", vmax_default)
        if vmin is None:
            vmin = vmin_default
        if vmax is None:
            vmax = vmax_default
        return cmap, vmin, vmax

    @staticmethod
    def pop_norm_args(kwargs, **defaults):
        """
        Pop vmin, vmax and cmap from plot_kwargs
        Args:
            **defaults:
                see get_norm_args method
        """
        cmap, vmin, vmax = ApiBackend.get_norm_args(kwargs, **defaults)
        kwargs.pop("cmap", None)
        kwargs.pop("vmin", None)
        kwargs.pop("vmax", None)
        return cmap, vmin, vmax

    @staticmethod
    def pop_xyz_index(kwargs: dict):
        """
        Args:
            kwargs: contains optional integer keys x_index, y_index and z_index
                Thes indices refer to the index of some data object which holds data of x, y and
                z axis respectively
        """
        x_index = kwargs.pop("x_index", 0)
        y_index = kwargs.pop("y_index", 1)
        z_index = kwargs.pop("z_index", None)
        if z_index is None:
            z_index = {1, 2, 3}
            z_index.difference_update()
            z_index = z_index.pop()
        return x_index, y_index, z_index

    @staticmethod
    def format_colors(kwargs, colors, fmt="rgba", length=None, dtype=None):
        """
        format colors according to fmt argument
        Args:
            colors (list/one value of rgba tuples/int/float/str): This argument
                will be interpreted as color
            fmt (str): rgba | hex | norm
            length (int/None): if not None: correct colors lenght
            dtype (np.dtype): output data type

        Returns:
            colors in fmt
        """
        cmap, vmin, vmax = ApiBackend.get_norm_args(
            kwargs, cmap_default=None, vmin_default=None, vmax_default=None
        )
        from rna.plotting.colors import to_colors

        return to_colors(
            colors, fmt, length=length, vmin=vmin, vmax=vmax, cmap=cmap, dtype=dtype
        )

    @staticmethod
    @abc.abstractmethod
    def axes_dim(axes):
        """
        Retrieve the current axes object which resembles the canvas you plot on to

        Args:
            dim: dimension of the axes object
        """

    @staticmethod
    @abc.abstractmethod
    def gca(dim: typing.Optional[int] = None, **kwargs):
        """
        Retrieve the current axes object which resembles the canvas you plot on to

        Args:
            dim: dimension of the axes object
        """

    @staticmethod
    @abc.abstractmethod
    def is_axes(obj: typing.Any) -> bool:
        """
        Check if the given object is an axes instance of this backend
        """

    @abc.abstractmethod
    def show(self):
        """
        Render the current api and promt it to display.
        """


class Api(
    rna.pattern.backend.Frontend, rna.polymorphism.Plottable, rna.polymorphism.Storable
):
    """
    Base class of a generic api.

    Examples:
        >>> import numpy as np
        >>> from rna.plotting import Api
        >>> api = Api()
        >>> api.backend  # doctest +ELLIPSIS
        <rna.plotting.backends.matplotlib.ApiBackendMatplotlib object at ...>

        To use plot, implement _plot
        >>> class Demo(Api):
        ...     def _plot(self, **kwargs):
        ...         self.set_style()
        ...         labels = kwargs.pop("labels", ["x (m)", "y (m)", "z (m)"])
        ...         ax = self.gca()
        ...         artist = self.plot_tensor(ax, self.data, **kwargs)
        ...         self.set_labels(ax, *labels)
        ...         return artist
        >>> demo = Demo()

        >>> artists = demo.plot(np.array([[1,1], [2,2]]), color='r')
        >>> _ = demo.set_legend(artists)

        # saving with a data format stores the data and allows recovery
        >>> path = "./tmp.pkl"
        >>> demo.save(path)
        >>> demo_restored = demo.load(path)

        >>> artists = demo_restored.plot()

        # rendering the api
        >>> demo_restored.show()

        # saving with a api format stores the Api
        >>> path_demo = "./tmp.png"
        >>> demo.save(path_demo)

        The backend can be easily exchanged:
        >>> demo.backend="plotly"
    """

    STRATEGY_TYPE = ApiBackend
    STRATEGY_DEFAULT = "matplotlib"

    def __init__(self):
        # Make sure you pass nothing to backend
        super().__init__()
        self.data = None

    def plot(self, data=None, **kwargs):
        """
        Args:
            data: data object. If you loaded this Api from data file, this is not required
                data is set to self.data which is then available in _plot
            **kwargs: passed to _plot
        """
        if data is None and self.data is None:
            raise ValueError("No data given (first argument)")
        elif data is not None:
            self.data = data
        return self._plot(**kwargs)

    def _plot(self, **kwargs):
        raise NotImplementedError(
            "{self} requires implementation of _plot(**kwargs)".format(**locals())
        )

    def save(self, *args, **kwargs):
        """
        Data is saved from Api class directly.
        Plots are specific to the backend so _save_<ext> must be implemented there. Also they have
        no load method.
        Data has priority if same format is present in Api and backend. Use Api.backend.save
        if you want to save backend also/only in this format.
        """
        try:
            # data saving
            if self.data is None:
                raise ValueError(
                    "{self}.data is None! You forgot to set the data attribute in plotting."
                )
            super().save(*args, **kwargs)  # pylint: disable=no-member
        except NotImplementedError:
            # figure saving
            self.backend.save(*args, **kwargs)

    def _save_pkl(self, path, **kwargs):
        kwargs.setdefault("protocol", pickle.HIGHEST_PROTOCOL)
        with open(path, "wb") as handle:
            pickle.dump(self.data, handle, **kwargs)

    @classmethod
    def _load_pkl(cls, path, **kwargs):
        with open(path, "rb") as handle:
            data = pickle.load(handle, **kwargs)
        obj = cls()
        obj.data = data
        return obj

    def __getattr__(self, name: str) -> typing.Any:
        """
        Forward to generic Api methods

        Note:
            Possibly only on 3.7 +
            Maybe look closer to
            https://stackoverflow.com/questions/2447353/getattr-on-a-module
        """
        if name in rna.plotting.EXPOSED_BACKEND_METHODS:
            backend = (
                self.backend
            )  # CAREFUL: could break the clever logic of the strategy pattern
            try:
                return getattr(backend, name)
            except AttributeError as err:
                raise NotImplementedError(
                    "Backend {backend} requires implementation of {name}".format(
                        **locals()
                    )
                ) from err
        else:
            raise AttributeError


class Figure(Api):
    """
    The Figure backend should be derived from
    """

    pass
