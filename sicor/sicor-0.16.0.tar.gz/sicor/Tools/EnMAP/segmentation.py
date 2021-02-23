#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains image segmentation tools.

# Copyright (C) 2018  Niklas Bohn (GFZ, <nbohn@gfz-potsdam.de>),
# German Research Centre for Geosciences (GFZ, <https://www.gfz-potsdam.de>)

# This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
# funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
# Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


import numpy as np
from multiprocessing import Pool
import platform
from tqdm import tqdm

from sicor.Tools.EnMAP.multiprocessing import initializer


def SLIC_segmentation(data_rad_all, n_pca, segs):
    """
    Perform superpixel segmentation by searching the image for a handful of geographically and compositionally
    representative locations. Create spatially-contiguous clusters of similar radiances.

    :param data_rad_all: radiance data array with shape (rows, cols, bands)
    :param n_pca:        number of principle components
    :param segs:         number of segments
    :return:             flattened radiance data array, number of segments, array of segment labels for each pixel
    """
    # importing skimage and scipy here avoids ImportError: dlopen: cannot load any more object with static TLS
    from skimage.segmentation import slic
    from scipy.linalg import eigh, norm

    # Change from BIP to a long list of spectra
    rows, bands, cols = data_rad_all.shape[0], data_rad_all.shape[2], data_rad_all.shape[1]
    X = np.asarray(data_rad_all, dtype=np.float32).reshape([rows * cols, bands])

    # Excluding bad locations, calculate top PCA coefficients
    mu = X.mean(axis=0)
    C = np.cov(X, rowvar=False)
    [v, d] = eigh(C)

    # Determine segmentation compactness scaling based on top 5 eigenvalues
    cmpct = norm(np.sqrt(v[-n_pca:]))

    # Project, redimension as an image with 5 channels, and segment
    X_pca = (X - mu) @ d[:, -n_pca:]
    X_pca = X_pca.reshape([rows, cols, n_pca])

    labels = slic(image=X_pca,
                  n_segments=segs,
                  compactness=cmpct,
                  max_iter=10,
                  sigma=0,
                  multichannel=True,
                  enforce_connectivity=True,
                  min_size_factor=0.5,
                  max_size_factor=3)

    lbl = np.unique(labels)
    segs = len(lbl)

    return X, segs, labels


def empirical_line_solution(X, rdn_subset, data_l2a_seg, rows, cols, bands, segs, labels, land_only, processes,
                            disable_progressbars):
    """
    Apply empirical line solution to infer exact result of remaining spectra.

    :param X:                    flattened radiance data array
    :param rdn_subset:           radiance data subset
    :param data_l2a_seg:         segmented surface reflectance
    :param rows:                 number of image rows
    :param cols:                 number of image columns
    :param bands:                number of instrument bands
    :param segs:                 number of segments
    :param labels:               array of segment labels for each pixel
    :param land_only:            if True, SICOR is applied to land surfaces only (this may result in edge effects,
                                 e.g., at coastlines); otherwise, all image pixels (land + water) are processed;
                                 default: False
    :param processes:            number of CPUs for multiprocessing
    :param disable_progressbars: True if progress bars should be disabled; default: False
    :return:                     extrapolated surface reflectance for each pixel
    """
    from scipy.spatial import KDTree  # import here to avoid static TLS ImportError

    # First set up a matrix of locations, one per spectrum in both
    # the reference set and the image cube.  We will simply use
    # row and column indices for simplicity, rather than worrying
    # about geographic or 3D locations
    row_grid, col_grid = np.meshgrid(np.arange(rows), np.arange(cols))
    locations = np.array([col_grid.flatten(), row_grid.flatten()]).T
    locations_subset = np.zeros((segs, 2))

    if land_only:
        lbl = np.unique(labels)[1:]

        for ii, idx in enumerate(lbl):
            locations_subset[ii, :] = locations[labels.flat == idx, :].mean(axis=0)

        missing_labels = []

        for ii in range(np.max(lbl)):
            if ii not in lbl:
                missing_labels.append(ii)

        unique_labels = np.arange(0, np.max(lbl) + 1 - len(missing_labels), 1)
    else:
        for i in range(segs):
            if np.count_nonzero(segs == 1) == 0:
                pass
            else:
                locations_subset[i, :] = locations[labels.flat == i, :].mean(axis=0)

        unique_labels = np.unique(labels)
        missing_labels = []

        for ii in range(np.max(unique_labels)):
            if ii not in unique_labels:
                missing_labels.append(ii)

        unique_labels = np.arange(0, np.max(unique_labels) - len(missing_labels), 1)

    tree = KDTree(locations_subset)

    # compute slopes and intercepts in the same shape like radiance and reflectance
    global _globs
    _globs = dict(tree=tree, locs=locations_subset, k=15, rdn=rdn_subset, data=data_l2a_seg, bands=bands)

    if platform.system() == "Windows" or processes == 1:
        initializer(globals(), _globs)
        results = []
        for ii in tqdm(unique_labels, disable=disable_progressbars):
            (sl, ic) = _compute_coefficients_for_label(ii)
            results.append((sl, ic))
    else:
        with Pool(processes=processes) as pool:
            results = pool.map(_compute_coefficients_for_label, unique_labels)

    slopes, intercepts = np.empty([rows * cols, bands]), np.empty([rows * cols, bands])

    if land_only:
        lbl = np.unique(labels)[1:]
        for u_lbl, coeffs in zip(unique_labels, results):
            slopes[labels.flat == lbl[u_lbl], :], intercepts[labels.flat == lbl[u_lbl], :] = coeffs
    else:
        for lbl, coeffs in zip(unique_labels, results):
            slopes[labels.flat == lbl, :], intercepts[labels.flat == lbl, :] = coeffs

    # finally compute reflectance
    reflectance = X * slopes + intercepts

    return reflectance


_globs = dict()


def _compute_coefficients_for_label(label_idx):
    from scipy.stats import linregress  # import here to avoid static TLS ImportError

    nn = _globs['tree'].query(_globs['locs'][label_idx, :], _globs['k'])[1]
    label_slopes, label_intercepts = zip(*[linregress(x=_globs['rdn'][:, nn, b],
                                                      y=_globs['data'][:, nn, b])[:2]
                                           for b in range(_globs['bands'])])

    return label_slopes, label_intercepts
