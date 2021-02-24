"""
Parallelisation functions for the command-line operations

With some adaptation, the functions provided in this module could also be used
in other contexts. However, given they are in our 'private' API, we make no
guarantees about their usage.
"""
import logging
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

import tqdm

try:
    import dask
except ModuleNotFoundError:  # pragma: no cover # emergency valve
    from .errors import raise_no_iris_warning

    raise_no_iris_warning()


logger = logging.getLogger(__name__)


def _apply_func(  # pylint:disable=too-many-arguments
    apply_func,
    loop_kwarglist,
    common_arglist=None,
    common_kwarglist=None,
    postprocess_func=None,
    n_workers=2,
    style="processes",
    return_res=False,
):
    common_arglist = [] if common_arglist is None else common_arglist
    common_kwarglist = {} if common_kwarglist is None else common_kwarglist
    tqdm_kwargs = {
        "total": len(loop_kwarglist),
        "unit": "it",
        "unit_scale": True,
        "leave": True,
    }
    if n_workers == 1:
        failures = _apply_func_serially(
            apply_func=apply_func,
            loop_kwarglist=loop_kwarglist,
            tqdm_kwargs=tqdm_kwargs,
            common_arglist=common_arglist,
            common_kwarglist=common_kwarglist,
            postprocess_func=postprocess_func,
            return_res=return_res,
        )
    else:
        failures = _apply_func_parallel(
            apply_func=apply_func,
            loop_kwarglist=loop_kwarglist,
            tqdm_kwargs=tqdm_kwargs,
            common_arglist=common_arglist,
            common_kwarglist=common_kwarglist,
            postprocess_func=postprocess_func,
            n_workers=n_workers,
            style=style,
            return_res=return_res,
        )

    return failures


def _apply_func_serially(  # pylint:disable=too-many-arguments
    apply_func,
    loop_kwarglist,
    tqdm_kwargs,
    common_arglist,
    common_kwarglist,
    postprocess_func,
    return_res=False,
):
    failures = False
    logger.info("Processing serially")
    full_res = []
    for ikwargs in tqdm.tqdm(loop_kwarglist, **tqdm_kwargs):
        try:
            res = apply_func(*common_arglist, **ikwargs, **common_kwarglist)
            if return_res:
                full_res.append(res)
            if postprocess_func is not None:
                postprocess_func(res)
        except Exception as e:  # pylint:disable=broad-except
            logger.exception("Exception found %s", e)
            failures = True

    if return_res:
        return full_res

    return failures


def _apply_func_parallel(  # pylint:disable=too-many-arguments
    apply_func,
    loop_kwarglist,
    tqdm_kwargs,
    common_arglist,
    common_kwarglist,
    postprocess_func,
    n_workers,
    style,
    return_res=False,
):
    failures = False
    logger.info("Processing in parallel with %s workers", n_workers)
    logger.info("Forcing dask to use a single thread when reading")
    with dask.config.set(scheduler="single-threaded"):
        if style == "processes":
            executor_cls = ProcessPoolExecutor
        elif style == "threads":
            executor_cls = ThreadPoolExecutor
        else:
            raise ValueError("Unrecognised executor: {}".format(style))
        with executor_cls(max_workers=n_workers) as executor:
            futures = [
                executor.submit(
                    apply_func, *common_arglist, **ikwargs, **common_kwarglist
                )
                for ikwargs in loop_kwarglist
            ]
            failures = False
            full_res = []
            # Print out the progress as tasks complete
            for future in tqdm.tqdm(as_completed(futures), **tqdm_kwargs):
                try:
                    res = future.result()
                    if postprocess_func is not None:
                        postprocess_func(res)
                    if return_res:
                        full_res.append(res)
                except Exception as e:  # pylint:disable=broad-except
                    logger.exception("Exception found %s", e)
                    failures = True

    if return_res:
        return full_res

    return failures
