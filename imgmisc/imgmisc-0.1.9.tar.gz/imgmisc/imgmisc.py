# -*- coding: utf-8 -*-

"""Main module."""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 20:00:11 2018

@author: henrik
"""

import re
import os
import numpy as np
import tifffile as tiff
import scipy.ndimage as ndi
from skimage.measure import regionprops
from PIL import Image, ImageChops
import pyvista as pv
import mahotas as mh

import numpy as np
from scipy import ndimage as ndi
import networkx as nx
#from .misc import crop
from skimage.measure import marching_cubes

def create_mesh(contour, resolution=[1, 1, 1]):
    v, f, _, _ = marching_cubes(
        contour > 0, 0, spacing=list(resolution), step_size=1, allow_degenerate=False)
    mesh = pv.PolyData(v, np.hstack(np.c_[np.full(f.shape[0], 3), f]))
    return mesh

def create_cellular_mesh(seg_img, resolution=[1,1,1], verbose=True):
    cells = []
    n_cells = len(np.unique(seg_img)) - 1
    for c_idx, cell_id in enumerate(np.unique(seg_img)[1:]):
        if verbose:
            print(f'Now meshing cell {c_idx} (label: {cell_id}) out of {n_cells}')
        cell_img, cell_cuts = autocrop(seg_img == cell_id, threshold=0, n=1, return_cuts=True, offset=[[2,2], [2,2], [2,2]])
        cell_volume = np.sum(cell_img > 0) * np.product(resolution)
        
        v, f, _, _ = marching_cubes(cell_img, 0, allow_degenerate=False, 
                                    step_size=1, spacing=resolution)
        v[:, 0] += cell_cuts[0, 0] * resolution[0]
        v[:, 1] += cell_cuts[1, 0] * resolution[1]
        v[:, 2] += cell_cuts[2, 0] * resolution[2]
        
        cell_mesh = pv.PolyData(v, np.ravel(np.c_[[[3]]*len(f), f]))
        cell_mesh['cell_id'] = np.full(fill_value=cell_id, shape=cell_mesh.n_points)
        cell_mesh['volume'] = np.full(fill_value=cell_volume, shape=cell_mesh.n_points)
    
        cells.append(cell_mesh)
    
    multi = pv.MultiBlock(cells)
    poly = pv.PolyData()
    for ii in range(multi.n_blocks):
        poly += multi.get(ii)
    return poly

from skimage.morphology import binary_dilation
def get_l1(seg_img, bg=0, selem=None):
    # TODO: Include option to remove cells bordering the image limits?
    bg_dilated = np.logical_and(binary_dilation(seg_img==bg, selem=selem), seg_img)
    
    labels = np.unique(seg_img)
    labels = labels[labels != bg]
    l1 = np.unique(seg_img[bg_dilated])
    l1 = l1[l1 != bg]
    l1 = np.isin(labels, l1)
    return l1

def get_layers(seg_img, bg=0, depth=None):
    labeled_img = seg_img.copy()
    layers = []

    while True:
        if depth is not None and len(layers) >= depth:
            break
        
        layer = get_l1(labeled_img, bg=bg)
        
        if sum(layer) == 0:
            continue
        layer_labels = np.unique(labeled_img)[1:][layer]
        layers.append(layer_labels)
        labeled_img[np.isin(labeled_img, layer_labels)] = bg
    return layers

# def get_layers(seg_img, bg=0):
#     from img2org.quantify import get_l1
#     labeled_img = seg_img.copy()
#     l1 = get_l1(labeled_img, bg=bg).astype('int')
#     layers = [l1]
#     while(True):
#         layer = get_l1(labeled_img, bg=bg).astype('int')
#         layer_indices = np.where(layer)[0]
        
#         if len(layer_indices) == 0:
#             continue
        
#         layers.append(layer)            
#         labeled_img[np.isin(labeled_img, layer_indices)] = bg
#     return layers            

import czifile as czi 
def xml2dict(xml_str):
    from lxml import objectify as xml_objectify
    """ Convert xml to dict, using lxml v3.4.2 xml processing library """
    def xml_to_dict_recursion(xml_object):
        dict_object = xml_object.__dict__
        if not dict_object:
            return xml_object
        for key, value in dict_object.items():
            dict_object[key] = xml_to_dict_recursion(value)
        return dict_object
    return xml_to_dict_recursion(xml_objectify.fromstring(xml_str))

# acq_meta = xml_to_dict(file.metadata())['Metadata']['Experiment']['ExperimentBlocks']['AcquisitionBlock']['AcquisitionModeSetup']
# print(np.array([float(acq_meta.get(key)) for key in ('ScalingZ', 'ScalingY', 'ScalingX')]) * 1e6)

def get_resolution(fname):
    ext = os.path.splitext(fname)[-1].lower()
    if ext in ['.czi']:
        import czifile as czi 
        f = czi.CziFile(fname)
        try:
            acq_meta = xml2dict(f.metadata())['Metadata']['Experiment']['ExperimentBlocks']['AcquisitionBlock']['AcquisitionModeSetup']
            res = tuple([float(acq_meta.get(key)) for key in ('ScalingZ', 'ScalingY', 'ScalingX')])
        except:
            res = 1., 1., 1.
        return res
    
    f = tiff.TiffFile(fname)
    if f.imagej_metadata is not None:
        try:
            z = f.imagej_metadata['spacing']
        except:
            z = 1.
        x = f.pages[0].tags['XResolution'].value[1] / f.pages[0].tags['XResolution'].value[0]
        y = x
    elif f.lsm_metadata is not None:
        try:
            z = f.lsm_metadata['VoxelSizeZ']
            y = f.lsm_metadata['VoxelSizeY']
            x = f.lsm_metadata['VoxelSizeX']
        except:
            z, y, x = 1, 1, 1
    else:
        z, y, x = 1., 1., 1.
    return z, y, x


def autocrop_2d(im):
    bg = Image.new(im.mode, im.size, (255, 255, 255, 0)) # transparent
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    # Bounding box given as a 4-tuple defining the left, upper, right, and lower 
    # pixel coordinates. If the image is completely empty, this method returns None.
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def sgroup(strings, regex):
    import re
    from itertools import groupby
    keyf = lambda text: (re.findall(regex, text) + [text])[0]
    groups = [list(items) for gr, items in groupby(sorted(strings), key=keyf)]
    # groups = np.array(groups)
    return groups

def cut(img, cuts):
    if img.ndim == 3:
        return img[
            cuts[0, 0] : cuts[0, 1], cuts[1, 0] : cuts[1, 1], cuts[2, 0] : cuts[2, 1]
        ]
    else:
        return img[
            cuts[0, 0] : cuts[0, 1], :, cuts[1, 0] : cuts[1, 1], cuts[2, 0] : cuts[2, 1]
        ]


def merge(lists):
    """
    Merge lists based on overlapping elements.

    Parameters
    ----------
    lists : list of lists
        Lists to be merged.

    Returns
    -------
    sets : list
        Minimal list of independent sets.

    """
    sets = [set(lst) for lst in lists if lst]
    merged = 1
    while merged:
        merged = 0
        results = []
        while sets:
            common, rest = sets[0], sets[1:]
            sets = []
            for x in rest:
                if x.isdisjoint(common):
                    sets.append(x)
                else:
                    merged = 1
                    common |= x
            results.append(common)
        sets = results
    return sets


def flatten(llist):
    """ Flatten a list of lists """
    return [item for sublist in llist for item in sublist]


def remove_empty_slices(arr, keepaxis=0):
    """ Remove empty slices (based on the total intensity) in an ndarray """
    not_empty = np.sum(arr, axis=tuple(np.delete(list(range(arr.ndim)), keepaxis))) > 0
    arr = arr[not_empty]
    return arr


def autocrop(arr, threshold=8e3, channel=-1, n=1, return_cuts=False, offset=None):

    if offset is None:
        offset = np.full((3,2), 0) #[[0, 0], [0, 0], [0, 0]]
    elif isinstance(offset, int):
        offset = np.full((3,2), offset)
    else:
        offset = np.array(offset)

    sumarr = arr
    if arr.ndim > 3:
        if channel == -1:
            sumarr = np.max(arr, axis=1)
        elif isinstance(channel, (list, np.ndarray, tuple)):
            sumarr = np.max(arr.take(channel, axis=1), axis=1)
        else:
            sumarr = sumarr[:, channel]

    cp = np.zeros((sumarr.ndim, 2), dtype=np.int)
    for ii in range(sumarr.ndim):
        axes = np.array([0, 1, 2])[np.array([0, 1, 2]) != ii]

        transposed = np.transpose(sumarr, (ii,) + tuple(axes))
        nabove = np.sum(
            np.reshape(transposed, (transposed.shape[0], -1)) > threshold, axis=1
        )

        first = next((e[0] for e in enumerate(nabove) if e[1] >= n), 0)
        last = len(nabove) - next(
            (e[0] for e in enumerate(nabove[::-1]) if e[1] >= n), 0
        )

        cp[ii] = first, last
    #    ranges = [range(cp[ii, 0], cp[ii, 1]) for ii in range(len(cp))]
    cp[0, 0] = np.max([0, cp[0, 0] - offset[0, 0]])
    cp[0, 1] = np.min([arr.shape[0], cp[0, 1] + offset[0, 1]])
    cp[1, 0] = np.max([0, cp[1, 0] - offset[1, 0]])
    cp[1, 1] = np.min([arr.shape[1], cp[1, 1] + offset[1, 1]])
    cp[2, 0] = np.max([0, cp[2, 0] - offset[2, 0]])
    cp[2, 1] = np.min([arr.shape[2], cp[2, 1] + offset[2, 1]])

    if arr.ndim > 3:
        arr = np.moveaxis(arr, 1, -1)
    for ii, _range in enumerate(cp):
        arr = np.swapaxes(arr, 0, ii)
        arr = arr[_range[0] : _range[1]]
        arr = np.swapaxes(arr, 0, ii)
    if arr.ndim > 3:
        arr = np.moveaxis(arr, -1, 1)

    if return_cuts:
        return arr, cp
    else:
        return arr

def symlink(src, dest):
    """
    Symlink a file if it doesn't exist already.
    """
    if not os.path.exists(dest):
        tid = True if os.path.isdir(dest) else False
        os.symlink(src, dest, target_is_directory=tid)


def mkdir(path):
    """
    Make a directory if it doesn't exist already.

    Parameters
    ----------
    path : str
        Path to directory.

    Returns
    -------
    None.

    """

    if not os.path.exists(path):
        os.makedirs(os.path.abspath(path))

def _scandirs(dir):
    subfolders= [f.path for f in os.scandir(dir) if f.is_dir()]
    for dir in list(subfolders):
        subfolders.extend(_scandirs(dir))
    return subfolders

def listdir(path, include=None, exclude=None, full=True, sorting=None, recursive=False, exclude_directories=True):
    if isinstance(path, (list, np.ndarray)):
        files = flatten([listdir(ff, include, exclude, full, sorting, recursive) for ff in path])
        return np.array(files)
    else:
        if recursive:
            folders = _scandirs(path) + [path]
            files = flatten([listdir(ff, include, exclude, full, sorting, recursive=False) for ff in folders])
        else:
            files = os.listdir(path)
            files = np.array(files)

    if full:
        files = np.array([os.path.join(os.path.abspath(path), x) for x in files])

    # Include
    if isinstance(include, str):
        files = np.array([x for x in files if include in x])
    elif isinstance(include, (list, np.ndarray)):
        matches = np.array([np.array([inc in ii for ii in files]) for inc in include])
        matches = np.any(matches, axis=0)
        files = files[matches]

    # Exclude
    if isinstance(exclude, str):
        files = np.array([x for x in files if exclude not in x])
    elif isinstance(exclude, (list, np.ndarray)):
        matches = np.array([np.array([exc in ii for ii in files]) for exc in exclude])
        matches = np.logical_not(np.any(matches, axis=0))
        files = files[matches]

    if exclude_directories:
        files = [ff for ff in files if not os.path.isdir(ff)]

    if sorting == "natural":
        files = np.array(natural_sort(files))
    elif sorting == "alphabetical":
        files = np.sort(files)
    elif sorting == True:
        files = np.sort(files)
    

    return files


def natural_sort(l):
    """
    Sort a list alphanumerically (natural sorting).

    Parameters
    ----------
    l : list or np.ndarray
        Structure to sort.

    Returns
    -------
    list or np.ndarray
        Sorted list/array.

    """

    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split("([0-9]+)", key)]

    return sorted(l, key=alphanum_key)

def binary_extract_largest(seg_img, background=0, selem=None):
    if selem is None:
        selem = np.ones((3, 3, 3))

    markers = ndi.label(seg_img != background, selem)[0]
    
    if len(np.unique(markers)) <= 2:
        return seg_img
    
    # Assumes that background is 0. Can this cause errors?
    r = regionprops(markers)
    largest = r[np.argmax([rr.area for rr in r])].label
    
    seg_img[markers != largest] = background
    
    return seg_img     


def match_shape(a, t, side="both", val=0):
    """

    Parameters
    ----------
    a : np.ndarray
    t : Dimensions to pad/trim to, must be a list or tuple
    side : One of 'both', 'before', and 'after'
    val : value to pad with
    """
    try:
        if len(t) != a.ndim:
            raise TypeError(
                "t shape must have the same number of dimensions as the input"
            )
    except TypeError:
        raise TypeError("t must be array-like")

    try:
        if isinstance(val, (int, float, complex)):
            b = np.ones(t, a.dtype) * val
        elif val == "max":
            b = np.ones(t, a.dtype) * np.max(a)
        elif val == "mean":
            b = np.ones(t, a.dtype) * np.mean(a)
        elif val == "median":
            b = np.ones(t, a.dtype) * np.median(a)
        elif val == "min":
            b = np.ones(t, a.dtype) * np.min(a)
    except TypeError:
        raise TypeError("Pad value must be numeric or string")
    except ValueError:
        raise ValueError("Pad value must be scalar or valid string")

    aind = [slice(None, None)] * a.ndim
    bind = [slice(None, None)] * a.ndim

    # pad/trim comes after the array in each dimension
    if side == "after":
        for dd in range(a.ndim):
            if a.shape[dd] > t[dd]:
                aind[dd] = slice(None, t[dd])
            elif a.shape[dd] < t[dd]:
                bind[dd] = slice(None, a.shape[dd])
    # pad/trim comes before the array in each dimension
    elif side == "before":
        for dd in range(a.ndim):
            if a.shape[dd] > t[dd]:
                aind[dd] = slice(int(a.shape[dd] - t[dd]), None)
            elif a.shape[dd] < t[dd]:
                bind[dd] = slice(int(t[dd] - a.shape[dd]), None)
    # pad/trim both sides of the array in each dimension
    elif side == "both":
        for dd in range(a.ndim):
            if a.shape[dd] > t[dd]:
                diff = (a.shape[dd] - t[dd]) / 2.0
                aind[dd] = slice(int(np.floor(diff)), int(a.shape[dd] - np.ceil(diff)))
            elif a.shape[dd] < t[dd]:
                diff = (t[dd] - a.shape[dd]) / 2.0
                bind[dd] = slice(int(np.floor(diff)), int(t[dd] - np.ceil(diff)))
    else:
        raise Exception("Invalid choice of pad type: %s" % side)

    b[tuple(bind)] = a[tuple(aind)]

    return b


def intensity_projection_series_all(infiles, outname, fct=np.max, normalize="all"):
    import phenotastic.file_processing as fp
    from pystackreg import StackReg
    from skimage.transform import warp
    import tifffile as tiff

    fdata = [fp.tiffload(x).data for x in infiles]
    shapes = [x.shape for x in fdata]
    max_dim = np.max(shapes)
    nchannels = fdata[0].shape[1]
    ntp = len(fdata)

    sr = StackReg(StackReg.RIGID_BODY)
    stack = np.zeros((nchannels, max_dim * ntp, 3 * max_dim))
    for chan in range(nchannels):
        cstack = np.zeros((3, max_dim * ntp, max_dim))
        for dim in range(3):
            cdstack = np.zeros((ntp, max_dim, max_dim))
            for tp in range(len(fdata)):
                one_proj = np.max(fdata[tp][:, chan], axis=dim)
                one_proj = match_shape(one_proj, (max_dim, max_dim))
                cdstack[tp] = one_proj
            tmats = sr.register_stack(cdstack, moving_average=ntp)
            for ii in range(len(tmats)):
                cdstack[ii] = warp(cdstack[ii], tmats[ii], preserve_range=True)
            cdstack = np.vstack(cdstack)
            cstack[dim] = cdstack

        if normalize == "all":
            cstack /= np.max(cstack)
        elif normalize == "first":
            cstack /= np.max(cstack[0])

        cstack = np.hstack(cstack)
        stack[chan] = cstack

    out = np.hstack(stack)
    out = out.astype(np.float32)
    # TODO: Save as png instead
    tiff.imsave(outname, out)


def to_uint8(data, normalize=True):
    data = data.astype("float")
    if normalize:
        data = (data - np.min(data)) / (np.max(data) - np.min(data)) * np.iinfo(np.uint8).max
    else:
        data = data / np.max(data) * np.iinfo(np.uint8).max
    data = data.astype(np.uint8)
    return data

def to_uint16(data, normalize=True):
    data = data.astype("float")
    if normalize:
        data = (data - np.min(data)) / (np.max(data) - np.min(data)) * np.iinfo(np.uint16).max
    else:
        data = data / np.max(data) * np.iinfo(np.uint16).max
    data = data.astype(np.uint16)
    return data


def matching_rows(array1, array2):
    return np.array(
        np.all((array1[:, None, :] == array2[None, :, :]), axis=-1).nonzero()
    ).T


def rand_cmap(
    nlabels,
    type="bright",
    first_color_black=True,
    last_color_black=False,
    verbose=False,
):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """
    from matplotlib.colors import LinearSegmentedColormap
    import colorsys
    import numpy as np

    if type not in ("bright", "soft"):
        print('Please choose "bright" or "soft" for type')
        return

    if verbose:
        print("Number of labels: " + str(nlabels))

    # Generate color map for bright colors, based on hsv
    if type == "bright":
        randHSVcolors = [
            (
                np.random.uniform(low=0.0, high=1),
                np.random.uniform(low=0.2, high=1),
                np.random.uniform(low=0.9, high=1),
            )
            for i in range(nlabels)
        ]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(
                colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2])
            )

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

        random_colormap = LinearSegmentedColormap.from_list(
            "new_map", randRGBcolors, N=nlabels
        )

    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == "soft":
        low = 0.6
        high = 0.95
        randRGBcolors = [
            (
                np.random.uniform(low=low, high=high),
                np.random.uniform(low=low, high=high),
                np.random.uniform(low=low, high=high),
            )
            for i in range(nlabels)
        ]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list(
            "new_map", randRGBcolors, N=nlabels
        )

    # Display colorbar
    if verbose:
        from matplotlib import colors, colorbar
        from matplotlib import pyplot as plt

        fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))

        bounds = np.linspace(0, nlabels, nlabels + 1)
        norm = colors.BoundaryNorm(bounds, nlabels)

        cb = colorbar.ColorbarBase(
            ax,
            cmap=random_colormap,
            norm=norm,
            spacing="proportional",
            ticks=None,
            boundaries=bounds,
            format="%1i",
            orientation=u"horizontal",
        )

    return random_colormap


def validate_inputs(image, mask, resolution):
    """Ensure that all inputs to segmentation have matching shapes and types.
    Modified from the Scikit-Image watershed code.

    Parameters
    ----------
    image : array
        The input image.
    mask : array, or None
        A boolean mask, True where we want to segment.
    resolution : array, or None
        Resolution per dimension of the input image.

    Returns
    -------
    image, mask, resolution: arrays
        The validated and formatted arrays. Image and resolution will have dtype
        float64, and mask int8. If ``None`` was given for the mask, it is a volume
        of all 1s.

    Raises
    ------
    ValueError
        If the shapes of the given arrays don't match.
    """

    if mask is not None and mask.shape != image.shape:
        raise ValueError("`mask` must have same shape as `image`")
    if mask is None:
        # Use a complete `True` mask if none is provided
        mask = np.ones(image.shape, bool)

    if not isinstance(image, np.ndarray):
        image = np.array(image)
    if not isinstance(mask, np.ndarray):
        mask = np.array(mask)
    if resolution is None:
        resolution = np.ones((image.ndim), np.float64)
    elif not isinstance(resolution, np.ndarray):
        resolution = np.array(resolution)
    if len(resolution) != image.ndim:
        raise ValueError(
            "`resolution` must have a value per dimension of `image`")

    return (image,
            mask,
            resolution)


def validate_connectivity(image_dim, connectivity, offset):
    """Convert any valid connectivity to a structuring element and offset.

    Parameters
    ----------
    image_dim : int
        The number of dimensions of the input image.
    connectivity : int, array, or None
        The neighbourhood connectivity. An integer is interpreted as in
        ``scipy.ndimage.generate_binary_structure``, as the maximum number
        of orthogonal steps to reach a neighbor. An array is directly
        interpreted as a structuring element and its shape is validated against
        the input image shape. ``None`` is interpreted as a connectivity of 1.
    offset : tuple of int, or None
        The coordinates of the center of the structuring element.

    Returns
    -------
    c_connectivity : array of bool
        The structuring element corresponding to the input `connectivity`.
    offset : array of int
        The offset corresponding to the center of the structuring element.

    Raises
    ------
    ValueError:
        If the image dimension and the connectivity or offset dimensions don't
        match.
    """
    if connectivity is None:
        connectivity = 1

    if np.isscalar(connectivity):
        c_connectivity = ndi.generate_binary_structure(image_dim, connectivity)
    else:
        c_connectivity = np.array(connectivity, bool)
        if c_connectivity.ndim != image_dim:
            raise ValueError("Connectivity dimension must be same as image")

    if offset is None:
        if any([x % 2 == 0 for x in c_connectivity.shape]):
            raise ValueError("Connectivity array must have an unambiguous "
                             "center")

        offset = np.array(c_connectivity.shape) // 2

    return c_connectivity, offset


def compute_neighbours(image, structure, offset):
    """Compute neighbourhood as an array of linear offsets into the image.

    These are sorted according to Euclidean distance from the center (given
    by `offset`), ensuring that immediate neighbours are visited first.
    """
    structure[tuple(offset)] = 0  # ignore the center; it's not a neighbor
    locations = np.transpose(np.nonzero(structure))
    sqdistances = np.sum((locations - offset)**2, axis=1)
    neighbourhood = (np.ravel_multi_index(locations.T, image.shape) -
                     np.ravel_multi_index(offset, image.shape))
    sorted_neighbourhood = neighbourhood[np.argsort(sqdistances)]
    return sorted_neighbourhood


def get_footprint(dimensions, connectivity, offset=None):
    """ Get footprint. """
    return validate_connectivity(dimensions, connectivity, offset)[0]

def find_neighbors(image, background=0, connectivity=1):
    image, mask, resolution = validate_inputs(image, mask=None, resolution=None)
    connectivity, offset = validate_connectivity(image.ndim, connectivity,
                                                  offset=None)
    mask = mh.borders(image, connectivity)

    # get the distances to the neighbours
    neighbours = connectivity.copy()
    neighbours[tuple(offset)] = False
    neighbours = np.array(np.where(neighbours)).T
    neighbours = np.multiply(neighbours, resolution)
    neighbours = np.subtract(neighbours, offset)

    # pad the image, and mask so that we can use the mask to keep from running
    # off the edges
    pad_width = [(p, p) for p in offset]
    image = np.pad(image, pad_width, mode='constant')
    mask = np.pad(mask, pad_width, mode='constant')

    # get flattened versions of everything
    flat_neighbourhood = compute_neighbours(image, connectivity, offset)
    image_raveled = image.ravel()
    indices = np.where(mask.ravel())[0]
    
    point_neighbours = np.array(list(map(lambda x: x + flat_neighbourhood, indices)))
    neighs = {ii:[] for ii in np.unique(image_raveled[indices])}  # {image_raveled[indices[ii]] : [] for ii in len(range(indices))}
    for ii, ptn in enumerate(point_neighbours):
        neighs[image_raveled[indices[ii]]].append(image_raveled[ptn])
    neighs = {ii:np.unique(neighs[ii]) for ii in neighs.keys()}
    neighs = {ii:neighs[ii][np.logical_and(neighs[ii] != background, neighs[ii] != ii)]  for ii in neighs.keys()}
    del neighs[background]

    return neighs
