#!/usr/bin/env python3
# coding: utf-8

"""line integral convolution for numpy arrays

LICENSE
   MIT (https://mit-license.org/)

COPYRIGHT
   © 2020 Steffen Brinkmann <s-b@mailbox.org>
"""

__version__ = '0.4.5'

import argparse
import logging
from multiprocessing import Pool
import os
import sys
from typing import Sequence, Tuple, Union

import imageio  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
from tqdm import tqdm, trange  # type: ignore

_LIC_DEBUG_MODE = False
_LIC_QUIET_MODE = False

logging_format = 'lic | %(asctime)s | %(levelname)-8s | %(message)s'
logging.basicConfig(format=logging_format, level=logging.WARNING)
plt_logger = logging.getLogger('matplotlib')
plt_logger.setLevel(level=logging.WARNING)

logging.debug(f'matplotlib version {np.__version__}')
logging.debug(f'numpy version {np.__version__}')

_eps = 1e-6


def _load_npy_data(file_x: str, file_y: str) -> Tuple[np.ndarray, np.ndarray]:
    logging.info(f'loading data files: {file_x} and {file_y}')
    try:
        data_x = np.load(file_x)
        data_y = np.load(file_y)
    except FileNotFoundError as e:
        logging.error('Could not read one of the input files')
        raise e

    logging.info(f'successfully opened the data files: {file_x} and {file_y}')
    logging.debug(f'shape of data_x: {data_x.shape}')
    logging.debug(f'shape of data_y: {data_y.shape}')

    return data_x, data_y


def _load_seed(seed_file: str) -> np.ndarray:
    logging.info(f'loading seed file: {seed_file}')
    try:
        seed = np.load(seed_file)
    except FileNotFoundError as e:  # pragma: no cover
        logging.error('Could not read the seed file')
        raise e

    logging.info(f'successfully opened the seed file: {seed_file}')
    logging.debug(f'shape of seed: {seed.shape}')

    return seed


def _load_pluto_single_file_data(file_data: str,
                                 var='B',
                                 dim='12') -> Tuple[np.ndarray, np.ndarray]:  # pragma: no cover
    logging.warning('only 2d PLUTO dbl single files are supported at the moment')
    try:
        data = np.fromfile(file_data)
    except FileNotFoundError as e:
        logging.error('could not read one of the input files')
        raise e

    data = data.reshape((7, 400, 160))
    if var == 'B':
        data_x = data[2 + int(dim[1]), :, :]
        data_y = data[2 + int(dim[0]), :, :]
    elif var == 'v':
        data_x = data[int(dim[0]), :, :]
        data_y = data[int(dim[1]), :, :]
    else:
        raise NotImplementedError('in _load_pluto_single_file_data: var has to be one of "v" or "B"')
    return data_x, data_y


def _check_data(data_x: np.ndarray, data_y: np.ndarray) -> bool:
    logging.info('checking the data')
    if len(data_x.shape) != 2:
        logging.error(f'data has to be 2d. data_x is {len(data_x.shape)}d.')
    if len(data_y.shape) != 2:
        logging.error(f'data has to be 2d. data_y is {len(data_y.shape)}d.')
    if len(data_x.shape) != 2 or len(data_y.shape) != 2:
        return False

    if (data_x.shape[0] != data_y.shape[0] or data_x.shape[1] != data_y.shape[1]):
        logging.error(f'data shapes do not match: x {data_x.shape}, y {data_y.shape}.')
        return False
    logging.info('data is valid')

    return True


def gen_seed(shape: Tuple[int, int],
             noise='white',
             points_every: Union[Tuple[int, int], int] = None,
             points_size: int = 0,
             points_alternate: bool = True,
             combine: str = 'multiply') -> np.ndarray:
    """Generate a 2d seed for the lic algorithm. The seed array can be generated using a random
    noise of values between 0.0 and 1.0 with different power spectrum and additional "points"
    spread evenly across the array. The distance between the points and their size can be adjusted.

    :param shape: the shape of the resulting seed, should be equal to the data dimensions
    :type shape: Tuple[int, int]
    :param noise: the power spectrum of the generated noise, defaults to 'white',
        future options are going to be 'white', 'pink' and 'blue'
    :type noise: str, optional
    :param points_every: add a regoin of values 1.0 every n points, defaults to None, which means nothing is added.
        If a tuple of two ints is given, the values are applied to the x and y direction seperately.
    :type points_every: tuple of ints or int, optional
    :param points_size: size of the added points, defaults to 0, which means a single pixel
    :type points_size: int, optional
    :param points_alternate: whether to alternate the placement of the points, defaults to True
    :type points_alternate: bool, optional
    :param combine: how to add the points to the random background, defaults to 'multiply', possible values are
        'multiply', 'sum', 'replace'
    :type combine: str, optional

    :raises NotImplementedError: in case of selecting options which have not been implementeds yet

    :return: the generated 2d seed array
    :rtype: numpy.ndarray
    """
    logging.info('generate the seed')
    if noise == 'white':
        np.random.seed(28032005)
        seed = np.random.random(shape)
    else:
        raise NotImplementedError('lic.gen_seed: parameter noise must be one of ["white"]')

    if points_size != 0:
        raise NotImplementedError('lic.gen_seed: point size is limited to 0 (i.e., one pixel) as of now.')

    if points_every is not None:
        # generate point pattern
        points = np.zeros_like(seed)
        if isinstance(points_every, int):
            _points_every = points_every, points_every
        else:
            _points_every = points_every

        if points_alternate is True:
            points[1::_points_every[0] * 2, 1::_points_every[1]] = 1.0
            points[1 + _points_every[0]::_points_every[0] * 2, 1 + int(_points_every[1] / 2)::_points_every[1]] = 1.0
        else:
            points[1::_points_every[0], 1::_points_every[1]] = 1.0

        # combine with seed
        if combine == 'multiply':
            seed *= points
        elif combine == 'sum':
            seed += points
        elif combine == 'replace':
            seed = np.where(points == 1.0, points, seed)
        else:
            raise ValueError(f'lic.gen_seed: {combine} is not a valid value for parameter combine.')  # pragma: no cover

    seed[0, :] = seed[:, 0] = seed[-1, :] = seed[:, -1] = 0.5
    logging.info('generated the seed')
    return seed


def lic(data_x: np.ndarray,
        data_y: np.ndarray,
        seed: np.ndarray = None,
        kernel: Sequence = None,
        length: int = None,
        contrast: bool = False) -> np.ndarray:
    """Generate a line integral convolution representation of the input data.

    :param data_x: a 2d numpy.ndarray with the x component of the vector field
    :type data_x: numpy.ndarray
    :param data_y: a 2d numpy.ndarray with the y component of the vector field
    :type data_y: numpy.ndarray
    :param length: the length of the line of the lic
    :type length: int, optional
    :param kernel: the convolution kernel of the lic
    :type kernel: a sequence (e.g., list or numpy.ndarray), optional
    :param seed: a 2d numpy.ndarray containing the seed of the lic. If no seed array is passed,
        a random seed is generated.
    :type seed: numpy.ndarray, optional
    :param contrast: whether to enhance the contrast of the resulting lic image
    :type contrast: bool, optional

    :return: The generated 2d lic array
    :rtype: numpy.ndarray
    """

    assert length is None or length > 0
    assert len(data_x.shape) == 2
    assert len(data_y.shape) == 2
    assert data_x.shape[0] == data_y.shape[0] and data_x.shape[1] == data_y.shape[1]

    logging.info('starting lic')

    # adjust and/or generate kernel and length
    if kernel is None:
        length = length or 20
        _kernel = np.ones(length)
    else:
        if length is not None:  # pragma: no cover
            logging.warning(f'lic.lic: overwriting parameter length with {len(kernel)}')
        length = len(kernel)
        _kernel = np.array(kernel) / np.mean(kernel)

    # generate seed if necessary or check validity of the provided seed
    if seed is None:
        seed = gen_seed(data_x.shape)
    else:
        assert isinstance(seed, np.ndarray), 'lic.lic: parameter seed must be of type numpy.ndarray.'
        assert len(seed.shape) == 2, 'lic.lic: parameter seed must be 2d.'
        assert seed.shape[0] == data_x.shape[0] and seed.shape[1] == data_x.shape[1],\
            'lic.lic: parameter seed must have the same dimensions as the data.\n'\
            f'seed: {seed.shape} ; data_x: {data_x.shape} ; data_y: {data_y.shape}'

    if _LIC_DEBUG_MODE:
        plt.imshow(seed, cmap=plt.get_cmap('binary'), origin='lower')
        plt.show()

    # generate result
    logging.debug(f'{_kernel[int(length / 2):]} [{len(_kernel[int(length / 2):])}]')
    logging.debug(f'{_kernel[int(length / 2)-1::-1]} [{len(_kernel[int(length / 2)-1::-1])}]')
    result = 0.5 * (_gen_lic(data_x, data_y, seed, _kernel[int(length / 2):])
                    + _gen_lic(-data_x, -data_y, seed, _kernel[int(length / 2) - 1::-1]))

    # normalize and enhance contrast
    result = _normalize(result)
    if contrast is True:
        result = _contrast(result)

    logging.info('lic created')
    return result


def _gen_lic(data_x: np.ndarray,
             data_y: np.ndarray,
             seed: np.ndarray,
             kernel: Sequence) -> np.ndarray:
    """generate the lic"""
    length = len(kernel)
    tqdm_prog = trange(1, length,
                       total=length,
                       desc='generate lics',
                       disable=_LIC_QUIET_MODE)
    shape = seed.shape
    fx = np.full(shape, 0.5)
    fy = np.full(shape, 0.5)
    line_fx = np.zeros((shape[0], shape[1], length), dtype=np.int64)
    line_fy = np.zeros((shape[0], shape[1], length), dtype=np.int64)
    # line_fx[:, :, 0], line_fy[:, :, 0] = np.meshgrid(range(shape[0]), range(shape[1]), indexing='ij')
    for i in range(shape[0]):
        line_fy[i, :, 0] = list(range(shape[1]))
    for j in range(shape[1]):
        line_fx[:, j, 0] = list(range(shape[0]))

    tx = np.full(shape, np.inf)
    ty = np.full(shape, np.inf)

    tqdm_prog.update()
    for i in tqdm_prog:
        tx, ty, fx, fy, line_fx, line_fy = _get_point_in_lic(data_x, data_y, tx, ty, fx, fy, line_fx, line_fy, i, shape)

        # tx = np.where(data_x > _eps, (1 - fx) / data_x, tx)
        # tx = np.where(data_x < -_eps, -fx / data_x, tx)
        # ty = np.where(data_y > _eps, (1 - fy) / data_y, ty)
        # ty = np.where(data_y < -_eps, -fy / data_y, ty)

        # line_fx[:, :, i] = np.where((tx < ty) & (data_x > 0), line_fx[:, :, i - 1] + 1, line_fx[:, :, i])
        # line_fx[:, :, i] = np.where((tx < ty) & (data_x <= 0), line_fx[:, :, i - 1] - 1, line_fx[:, :, i])
        # line_fx[:, :, i] = np.where((tx >= ty), line_fx[:, :, i - 1], line_fx[:, :, i])

        # line_fy[:, :, i] = np.where((tx >= ty) & (data_y > 0), line_fy[:, :, i - 1] + 1, line_fy[:, :, i])
        # line_fy[:, :, i] = np.where((tx >= ty) & (data_y <= 0), line_fy[:, :, i - 1] - 1, line_fy[:, :, i])
        # line_fy[:, :, i] = np.where((tx < ty), line_fy[:, :, i - 1], line_fy[:, :, i])

        # fx = np.where((tx < ty) & (data_x > 0), 0., fx)
        # fx = np.where((tx < ty) & (data_x <= 0), 1., fx)

        # fy = np.where((tx >= ty) & (data_y > 0), 0., fy)
        # fy = np.where((tx >= ty) & (data_y <= 0), 1., fy)

        # # np.clip(line_fx, 0, shape[0] - 1, line_fx)
        # # np.clip(line_fy, 0, shape[1] - 1, line_fy)
        # line_fx = np.where(line_fx < 0, 0, line_fx)
        # line_fx = np.where(line_fx >= shape[0], shape[0] - 1, line_fx)
        # line_fy = np.where(line_fy < 0, 0, line_fy)
        # line_fy = np.where(line_fy >= shape[1], shape[1] - 1, line_fy)

        fy = np.where((tx < ty), fy + data_y[line_fx[:, :, i], line_fy[:, :, i], ] * tx, fy)
        fx = np.where((tx >= ty), fx + data_x[line_fx[:, :, i], line_fy[:, :, i], ] * ty, fx)

    lines_f = seed[line_fx, line_fy] * kernel
    return lines_f.mean(axis=2)


def _get_point_in_lic(data_x, data_y, tx, ty, fx, fy, line_fx, line_fy, i, shape):
    tx = np.where(data_x > _eps, (1 - fx) / data_x, tx)
    tx = np.where(data_x < -_eps, -fx / data_x, tx)
    ty = np.where(data_y > _eps, (1 - fy) / data_y, ty)
    ty = np.where(data_y < -_eps, -fy / data_y, ty)

    line_fx[:, :, i] = np.where((tx < ty) & (data_x > 0), line_fx[:, :, i - 1] + 1, line_fx[:, :, i])
    line_fx[:, :, i] = np.where((tx < ty) & (data_x <= 0), line_fx[:, :, i - 1] - 1, line_fx[:, :, i])
    line_fx[:, :, i] = np.where((tx >= ty), line_fx[:, :, i - 1], line_fx[:, :, i])

    line_fy[:, :, i] = np.where((tx >= ty) & (data_y > 0), line_fy[:, :, i - 1] + 1, line_fy[:, :, i])
    line_fy[:, :, i] = np.where((tx >= ty) & (data_y <= 0), line_fy[:, :, i - 1] - 1, line_fy[:, :, i])
    line_fy[:, :, i] = np.where((tx < ty), line_fy[:, :, i - 1], line_fy[:, :, i])

    fx = np.where((tx < ty) & (data_x > 0), 0., fx)
    fx = np.where((tx < ty) & (data_x <= 0), 1., fx)

    fy = np.where((tx >= ty) & (data_y > 0), 0., fy)
    fy = np.where((tx >= ty) & (data_y <= 0), 1., fy)

    # np.clip(line_fx, 0, shape[0] - 1, line_fx)
    # np.clip(line_fy, 0, shape[1] - 1, line_fy)
    line_fx = np.where(line_fx < 0, 0, line_fx)
    line_fx = np.where(line_fx >= shape[0], shape[0] - 1, line_fx)
    line_fy = np.where(line_fy < 0, 0, line_fy)
    line_fy = np.where(line_fy >= shape[1], shape[1] - 1, line_fy)

    return tx, ty, fx, fy, line_fx, line_fy


def _contrast(v: Union[np.ndarray, float]) -> Union[np.ndarray, float]:  # pragma: no cover
    return .5 * (1. - np.cos(np.pi * v))


def _normalize(arr: np.ndarray) -> np.ndarray:
    """scale the input array to the interval [0, 1]

    >>> _normalize(np.array([2, 3, 4]))
    array([0. , 0.5, 1. ])
    """
    return (arr - arr.min()) / (arr - arr.min()).max()


def _set_logging_level(quiet: bool, verbose: bool, debug: bool) -> None:  # pragma: no cover
    if debug is True:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info('debug mode engaged')
    if verbose is True:
        logging.getLogger().setLevel(logging.INFO)
    if quiet is True:
        logging.getLogger().setLevel(logging.ERROR)


def _scale(x: np.ndarray, factor: float):
    if factor > 1.0:
        raise NotImplementedError('lic._scale: upscaling not implemented yet')

    skip = int(1 / factor)
    return x[::skip, ::skip]


def _gen_sane_output_filename(output_file, data_x_file, data_y_file, line_length, animate):
    """generate sane output file name"""
    if output_file is None:
        sane_x = data_x_file.name.split('/')[-1].replace('.', '_')
        if data_y_file is not None:
            sane_y = data_y_file.name.split('/')[-1].replace('.', '_')
        else:  # pragma: no cover
            sane_y = ''
        output_filename = f'out_{sane_x}_{sane_y}_{line_length}'
    else:  # pragma: no cover
        output_filename = output_file

    if animate == 1 and not output_filename.endswith('.png'):
        output_filename += '.png'
    if animate != 1 and not output_filename.endswith('.gif'):
        output_filename += '.gif'

    return output_filename


def _parse_arguments(argv=None):
    # parse the command line options
    parser = argparse.ArgumentParser(description='Line integral convolution (lic) algorithm. '
                                     'Please have a look at the documentation (https://lic.readthedocs.io/en/latest/) '
                                     'for further information on how tho use this software.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('data_x_file', type=argparse.FileType('rb'),
                        help='an npy file containing a 2d numpy.ndarray with the x component '
                        'of the vector field')
    parser.add_argument('data_y_file', type=argparse.FileType('rb'),
                        help='an npy file containing a 2d numpy.ndarray with the y component '
                        'of the vector field')
    parser.add_argument('-s', '--seed-file', type=argparse.FileType('rb'),
                        help='an npy file containing a 2d numpy.ndarray with the seed image')
    parser.add_argument('-l', '--line-length', type=int, default=20, metavar='LENGTH',
                        help='the length of the line of the lic')
    parser.add_argument('-o', '--output-file', type=str, metavar='FILE',
                        help='the name of the output file, If it is not set, a name will be generated from '
                        'the names of the input data files.')
    parser.add_argument('-c', '--enhance-contrast', action='store_true',
                        help='enhance the contrast of the resulting lic image')
    parser.add_argument('-f', '--factor', type=float, default=1.0, metavar='FACTOR',
                        help='scale the lic image by a factor')
    parser.add_argument('-a', '--animate', type=int, default=1, metavar='LENGTH',
                        help='if an animated image is wanted, set this to an integer value larger than 1')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='switch off text output except for error messages. This will overwrite -v.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='more verbose text output')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='switch on debug mode. This will show intermediate results and plots, as well as '
                        'log a lot of debugging information.')
    parser.add_argument('-ps', '--pluto-single-file', action='store_true',
                        help=argparse.SUPPRESS)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}',
                        help='show the version of this software')
    return parser.parse_args(argv)


def run(argv: list = None):
    """the command line tool. Please use the ``--help`` option to get help."""

    global _LIC_QUIET_MODE
    global _LIC_DEBUG_MODE

    # parse the command line options
    args = _parse_arguments(argv)

    # print the logo and version
    if args.quiet is False:  # pragma: no cover
        print(f'⎣⫯ℂ {__version__}')

    # set quiet mode
    _LIC_QUIET_MODE = args.quiet

    # set debug mode
    _LIC_DEBUG_MODE = args.debug

    # set verbosity level
    _set_logging_level(args.quiet, args.verbose, args.debug)

    logging.debug(args)

    if args.pluto_single_file is True:  # pragma: no cover
        x, y = _load_pluto_single_file_data(args.data_x_file.name, 'B', '12')
    else:
        x, y = _load_npy_data(args.data_x_file.name, args.data_y_file.name)

    x = _scale(x, args.factor)
    y = _scale(y, args.factor)

    if _check_data(x, y) is False:  # pragma: no cover
        sys.exit(1)

    if args.seed_file is None:
        seed_data = gen_seed(x.shape,
                             noise='white',
                             points_every=1,
                             points_size=0,
                             points_alternate=True,
                             combine='multiply')
    else:
        seed_data = _load_seed(args.seed_file.name)
        seed_data = _scale(seed_data, args.factor)

    # generate sane output file name
    output_filename = _gen_sane_output_filename(args.output_file,
                                                args.data_x_file,
                                                args.data_y_file,
                                                args.line_length,
                                                args.animate)

    if args.animate == 1:
        logging.info(f'Starting calculation for image of size: {x.shape}, i.e., {x.shape[0] * x.shape[1]} cells')
        lic_result = lic(x, y, length=args.line_length, contrast=args.enhance_contrast, seed=seed_data)
        if _LIC_DEBUG_MODE:
            plt.hist(lic_result.flatten(), 100)
            plt.show()
        # save plot to file
        logging.info(f'saving lic plot to {output_filename}')
        plt.imsave(output_filename, lic_result, cmap=plt.get_cmap('binary'), origin='lower')

        if _LIC_DEBUG_MODE:
            plt.imshow(lic_result, cmap=plt.get_cmap('binary'), origin='lower')
            plt.show()
    else:
        n_proc = max(len(os.sched_getaffinity(0)) // 2, 1)
        logging.info(f'Starting calculation on {n_proc} processes')
        with Pool(processes=n_proc) as pool:
            kernel_base = list(range(args.line_length))
            kernels = [kernel_base[i:] + kernel_base[:i] for i in range(args.animate)]
            lic_results = pool.starmap(lic, zip([x] * len(kernels),
                                                [y] * len(kernels),
                                                [seed_data] * len(kernels),
                                                kernels,
                                                [None] * len(kernels),
                                                [args.enhance_contrast] * len(kernels)
                                                ))

        images = []
        for i, res in tqdm(enumerate(lic_results),
                           desc='generate gif',
                           disable=_LIC_QUIET_MODE,
                           total=(len(lic_results))):
            filename = f'lic_out_{i}.png'
            plt.imsave(filename, res, cmap=plt.get_cmap('binary'), origin='lower')
            images.append(imageio.imread(filename))

        # save animation to file
        logging.info(f'saving lic animation to {output_filename}')
        imageio.mimsave(output_filename, images)

    logging.info('all done.')


if __name__ == '__main__':
    run()
