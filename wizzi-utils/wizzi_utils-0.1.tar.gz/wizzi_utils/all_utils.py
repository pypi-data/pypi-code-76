import sys
import os
import datetime
from timeit import default_timer as timer
from typing import Callable
import cProfile
import pstats
import io

LINES = '-' * 80


def get_timer_delta(start_timer: float) -> datetime.timedelta:
    end_timer = get_timer()
    d = datetime.timedelta(seconds=(end_timer - start_timer))
    return d


def get_timer() -> float:
    return timer()


def get_current_date_hour() -> str:
    now = datetime.datetime.now()
    current_time = now.strftime('%d-%m-%Y %H:%M:%S')
    return current_time


def get_mac_address() -> str:
    from uuid import getnode as get_mac
    mac = get_mac()
    mac = ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))
    return mac


def get_cuda_version() -> str:
    if 'CUDA_PATH' in os.environ:
        cuda_v = os.path.basename(os.environ['CUDA_PATH'])
    else:
        cuda_v = 'No CUDA_PATH found'
    return cuda_v


def make_cuda_invisible() -> None:
    """
        disable(the -1) gpu 0
        TODO support hiding multiple gpus
    """
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1, 0'
    return


def start_profiler() -> cProfile.Profile:
    pr = cProfile.Profile()
    pr.enable()
    return pr


def end_profiler(pr: cProfile.Profile, rows: int = 10) -> str:
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(rows)
    return s.getvalue()


def main_wrapper(
        main_function: Callable,
        cuda_off: bool = False,
        torch_v: bool = False,
        tf_v: bool = False,
        cv2_v: bool = False,
        with_profiler: bool = False
) -> None:
    """
    :param main_function: the function to run
    :param cuda_off: make gpu invisible and force run on cpu
    :param torch_v: print torch version
    :param tf_v: print tensorflow version
    :param cv2_v: print opencv version
    :param with_profiler: run profiler
    :return:
    """
    print(LINES)
    start_timer = get_timer()

    # make_cuda_invisible()
    print('main_wrapper:')
    print('* Run started at {}'.format(get_current_date_hour()))
    print('* Python Version {}'.format(sys.version))
    print('* Working dir: {}'.format(os.getcwd()))
    print('* Computer Mac: {}'.format(get_mac_address()))
    cuda_msg = '* CUDA Version: {}'.format(get_cuda_version())
    if cuda_off:
        make_cuda_invisible()
        cuda_msg += ' (Turned off)'
    print(cuda_msg)

    if torch_v:
        try:
            import torch
            print('* PyTorch Version {}'.format(torch.__version__))
        except (ModuleNotFoundError, NameError) as err:
            print('* {}'.format(err))

    if tf_v:
        try:
            import tensorflow as tf
            print('* TensorFlow Version {}'.format(tf.__version__))
        except (ModuleNotFoundError, NameError) as err:
            print('* {}'.format(err))

    if cv2_v:
        try:
            import cv2
            print('open cv version {}'.format(cv2.getVersionString()))
        except (ModuleNotFoundError, NameError) as err:
            print('* {}'.format(err))

    print('Function {} started:'.format(main_function))
    print(LINES)
    pr = start_profiler() if with_profiler else None
    main_function()
    if with_profiler:
        print(end_profiler(pr))
    print(LINES)
    print('Total run time {}'.format(get_timer_delta(start_timer)))
    print(LINES)
    return


def main():
    print('big program')


if __name__ == '__main__':
    main_wrapper(
        main_function=main,
        cuda_off=False,
        torch_v=False,
        tf_v=False,
        cv2_v=False,
        with_profiler=False
    )
