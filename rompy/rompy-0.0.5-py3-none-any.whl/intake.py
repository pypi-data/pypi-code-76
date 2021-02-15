#-----------------------------------------------------------------------------
# Copyright (c) 2020 - 2021, CSIRO 
#
# All rights reserved.
#
# The full license is in the LICENSE file, distributed with this software.
#-----------------------------------------------------------------------------

from intake_xarray.base import DataSourceMixin
from pandas import to_timedelta

import logging

logger = logging.getLogger('rompy.intake')

class NetCDFFCStackSource(DataSourceMixin):
    """An extension of intake-xarray in an opinionated fashion to open a stack of forecast model results stored as netcdf using xarray.

    Expands urlpath with the product of values passed in parameter ``fmt_fields`` to establish a finite set of urls to stack. Uses fsspec so that the file system can be on a local or http. Useful for subsetting catalogs of netcdf files. Defers to XArray for file opening and backend driver selection.

    Parameters
    ----------
    urlpath : str
        Templated path to scan for source file(s). May include format
        pattern strings.
        Some examples:
            - ``{{ CATALOG_DIR }}/data/{year}/air_{month}.nc``
            - ``https://some.thredds.server/thredds/catalog/model/{year}/{month}/catalog.html``
    fn_fmt : str, optional
        Templated file name to check for existence in the broadcast urlpath
        Example:
            - ``air_{month}.nc``
    fmt_fields: dict
        Dictionary of keys corresponding to urlpath format entries. The product of 
        all values is broadcast across urlpath to establish a finite set of locations 
        to look for source files.
    url_replace:
        Dictionary of string substitutions to be made on found urls.
        Example:
            - {'catalog':'dodsC'}
    ds_filters:
        Dictionary of common dataset manipulations that are applied in order 
        during dataset preprocessing. Configurable from catalog entry yaml. 
        Filters currently available are ['sort','subset','crop','timenorm','rename']
        Examples:
            - {'rename':{'dir':'mean_dir'},
               'sort':['direction'],
               'timenorm':'1H',
               'crop':{'lon':slice(-32.2,-33.2),
                       'lat':slice(114.,115.)}
               }
        Additional documentation to follow - see source code for xarray 
        implementation details.
    startdt, enddt: datetime, optional
        Start and end dates to crop final stacked dataset to. 
    hindcast: bool, optional
        Rather than return a stack of forecasts, return a dataset with a 
        unique time dimension selecting the minimum lead time for each time point. 
        Useful for establishing a pseudo-reanalysis dataset from a stack of forecasts.
    chunks : int or dict, optional
        Chunks is used to load the new dataset into dask
        arrays. ``chunks={}`` loads the dataset with dask using a single
        chunk for all arrays.
    xarray_kwargs: dict
        Additional xarray kwargs for xr.open_dataset().
    storage_options: dict
        If using a remote fs (whether caching locally or not), these are
        the kwargs to pass to that FS.
    """
    name = 'netcdf_fcstack'

    def __init__(self, urlpath, fn_fmt='', fmt_fields=None, url_replace=None, ds_filters=None,
                 startdt = None, enddt = None, hindcast = False,
                 chunks=None, xarray_kwargs=None, metadata=None,
                 storage_options=None, **kwargs):
        
        self.fn_fmt = fn_fmt
        self.url_replace = url_replace or {}
        self.fmt_fields = fmt_fields or {}
        self.ds_filters = ds_filters or {}
        self.startdt = startdt
        self.enddt = enddt
        self.hindcast = hindcast
        self.chunks = chunks or {}
        self.xarray_kwargs = xarray_kwargs or {}
        self._ds = None
        self.deterministic_pattern = True
        self.urlpath = urlpath

        super(NetCDFFCStackSource, self).__init__(metadata=metadata, **kwargs)

    # Replicating intakes PatternMixin
    @property
    def deterministic_pattern(self):
        if hasattr(self, '_deterministic_pattern'):
            return self._deterministic_pattern
        raise KeyError('Plugin needs to set `deterministic_pattern`'
                       ' before setting urlpath')

    @deterministic_pattern.setter
    def deterministic_pattern(self, deterministic_pattern):
        self._deterministic_pattern = deterministic_pattern

    @property
    def urlpath(self):
        return self._urlpath

    @urlpath.setter
    def urlpath(self, urlpath):
        from .utils import walk_server

        if hasattr(self, '_original_urlpath'):
            self._urlpath = urlpath
            return

        self._original_urlpath = urlpath

        if self.deterministic_pattern:
            logger.info(f'Scanning urlpath={urlpath}\n fn_fmt={self.fn_fmt}')
            self._urlpath = walk_server(urlpath, self.fn_fmt, self.fmt_fields, self.url_replace)
            logger.info(f'Found {len(self.urlpath)}')
        else:
            self._urlpath = urlpath

        if isinstance(self.deterministic_pattern, bool):
            if isinstance(urlpath, str) and self._urlpath == urlpath:
                self.deterministic_pattern = False
    
    def _open_dataset(self):
        import xarray as xr
        from dask import delayed, compute
        import dask.config as dc
        from .filters import _open_preprocess

        # Ensure a time normalisation filter is applied to each dataset
        from .filters import timenorm_filter
        if ('timenorm' not in self.ds_filters.keys()) and (timenorm_filter not in self.ds_filters.keys()):
            self.ds_filters[timenorm_filter]='1h'

        if isinstance(self.urlpath,list):
            if len(self.urlpath) == 0:
                raise ValueError(f'No urls matched for query: {self}')
            elif len(self.urlpath) == 1:
                # ds = xr.open_dataset(self.urlpath[0],chunks=self.chunks,**self.xarray_kwargs)
                ds = _open_preprocess(self.urlpath[0],self.chunks,self.ds_filters,self.xarray_kwargs)
                ds = ds.expand_dims('init')
            elif len(self.urlpath) > 1:
                # NOTE: open_mfdataset gives non-deterministic results when using 
                # distributed scheduler
                # ds = xr.open_mfdataset(self.urlpath, 
                #                        concat_dim='init', 
                #                        combine='nested', 
                #                        preprocess=_preprocess_fn,
                #                        parallel=True,
                #                        **self.xarray_kwargs)
                __open_preprocess=delayed(_open_preprocess)
                futures = [__open_preprocess(url,self.chunks,self.ds_filters,self.xarray_kwargs) for url in self.urlpath]
                dsets = compute(*futures,traverse=False)
                ds = xr.concat(dsets, dim='init', 
                                      coords=['time'], 
                                      compat="override", 
                                      combine_attrs="override")
        else:
            raise ValueError('Internal error. Expected urlpath path pattern string to have been expanded to a list')

        if self.hindcast:
            ds = ds.stack(forecast_time=['init','lead'])
            max_init_time = ds['init'].groupby('time').max()
            min_lead_time = ds['lead'].groupby('time').min()
            ds = ds.sel(forecast_time=list(zip(max_init_time.values, min_lead_time.values)))
            ds = ds.reset_index('forecast_time').rename({'forecast_time':'time'})
            
        # Finally return the composed dataset, cropped back to cover the requested time period
        if self.startdt is not None:
            ds = ds.sel(time=slice(self.startdt,self.enddt))

        self._ds = ds


