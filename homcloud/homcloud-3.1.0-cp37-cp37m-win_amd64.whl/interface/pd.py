"""

"""
import subprocess
import warnings
import shutil
import sys
import enum
import operator
import os
from tempfile import NamedTemporaryFile

import numpy as np
from forwardable import forwardable
from cached_property import cached_property

import homcloud.alpha_filtration as alpha_filtration
import homcloud.rips as rips
import homcloud.bitmap
import homcloud.abstract_filtration as abstract_filtration
import homcloud.optvol as optvol
import homcloud.int_reduction as int_reduction
import homcloud.pdgm as pdgm
import homcloud.pdgm_format as pdgm_format
import homcloud.diagram as homdiag
import homcloud.pict.optimal_one_cycle as pict_opt1cyc
import homcloud.optimal_one_cycle as opt1cyc
import homcloud.plot_PD_slice as plot_PD_slice
from homcloud.spatial_searcher import SpatialSearcher

from .distance_transform import distance_transform
from .histogram import HistoSpec, SliceHistogram
from .optimal_volume import OptimalVolume, StableVolume
from .exceptions import VolumeNotFound
from .bitmap_optimal_1_cycle import BitmapOptimal1Cycle
from .boundary_map_optimal_1_cycle import Optimal1Cycle
from .ph0_component import PH0Components


class PDList(object):
    """Collection of 0th,1st,..,and q-th persitence diagrams.

    In HomCloud, diagrams for all degrees coming from a filtration
    are combined into a single file. This class is the interface to
    the file.

    Args:
       file (string or file): The pathname to a diagram file
       type (enum PDList.FileType): Type of diagram file. One of the following:
           idiagram, pdgm, or None (autodetected)
       cache (bool): Ignored (for backward compatibility)
       negate (bool): Ignored (for backward compatibility)
    """

    def __init__(self, file, filetype=None, cache=False, negate=False):
        self.filetype = PDList.estimate_format(filetype, file)

        if self.filetype == PDList.FileType.IDIAGRAM:
            self.path = file
            self.reader = None
        elif isinstance(file, str):
            self.path = file
            self.reader = pdgm_format.PDGMReader.open(file)
        else:
            self.path = getattr(file, "name", None)
            self.reader = pdgm_format.PDGMReader(file, self.path)

    def __repr__(self):
        return "PDList(path=%s)" % self.path

    def close(self):
        self.reader.close()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    @enum.unique
    class FileType(enum.Enum):
        IDIAGRAM = "idipha"
        PDGM = "pdgm"

    @staticmethod
    def estimate_format(format, path):
        assert not ((format == PDList.FileType.IDIAGRAM) and (path is None))

        if format:
            return format
        if path is None:
            return PDList.FileType.PDGM

        _, ext = os.path.splitext(path)
        if ext == ".idiagram":
            return PDList.FileType.IDIAGRAM
        elif ext == ".pdgm":
            return PDList.FileType.PDGM
        else:
            raise(ValueError("Unknown file format: {}".format(path)))

    @staticmethod
    def compute_pd(output_filetype, filtration, save_to, parallels, algorithm,
                   save_suppl_info):
        if output_filetype == PDList.FileType.IDIAGRAM:
            filtration.compute_diagram_and_save(save_to, parallels, algorithm)
            return PDList(save_to, PDList.FileType.IDIAGRAM)
        elif output_filetype == PDList.FileType.PDGM:
            f = PDList.open_pdgm_file(save_to)
            filtration.compute_pdgm(f, algorithm, save_suppl_info)
            f.seek(0)
            return PDList(f, PDList.FileType.PDGM)

    @staticmethod
    def open_pdgm_file(save_to):
        if save_to is None:
            return NamedTemporaryFile()
        else:
            return open(save_to, "w+b")

    @staticmethod
    def from_alpha_filtration(pointcloud,
                              weight=False, no_squared=False,
                              subsets=False, check_acyclicity=False,
                              algorithm=None, parallels=1, vertex_symbols=None,
                              save_to=None, indexed=True, save_suppl_info=True,
                              save_boundary_map=False, periodicity=None,
                              save_phtrees=False, output_filetype=None):
        """Compute PDList by using an alpha filtration from a point cloud.

        Args:
            pointcloud (numpy.ndarray): Point cloud data. Each row
                represents a single point.
            weight (bool): If False, the pointcloud has no weight. If True,
                the last column of the pointcloud ndarray is regarded as
                weights. Please note that the weight paramters of points
                should be the square of their own radii.
            no_squared (bool): By default, all birth/death times are squared.
                If no_squared is True, all computed birth/death times are
                not squared.
            subsets (list[int] or bool or None):
                This parameter is used to compute relative homology.
                This parameter allows you to analyze the interspace structures
                between two or more objects in your pointcloud.

                If `subsets` is None, normal persistent homology is computed.

                If `subsets` is a list of integers whose length is the same
                as the number of points, the points are grouped
                by the integers and the gaps in the points in the same
                group is filled. The integer -1 in this list means
                that the point does not belong to any group.

                If subsets is True, the last column of `pointcloud` is regarded
                as the list of group id.
            check_acyclicity (bool):
                Checks the acyclicity of each grouped points in subsets
                if True. This parameter is used only if `subsets` parameter
                is used.
            algorithm (string or None): The name of the algorithm.
                An appropriate algorithm is
                automatically selected if None is given.

                The following algorithms are available:

                * "phat-twist"
                * "phat-chunk-parallel"
                * "dipha"

                In many cases, the parameter should be `None`.
            vertex_symbols (list[string] or None): The names of vertices.
                The names are used to represent some simplices, such as
                birth/death simplices or optimal volumes.

                If None is given, vertices are automatically named by
                "0", "1", "2", ...
            parallels (int): The number of threads used for the computation.
                This parameter is used only if "dipha" algorithm is used.
            save_to (string): The file path which the computation result is
                saved into. You can load the saved data by
                ``homcloud.interface.PDList(FILE_PATH)``.
                Saving the result is recommended since the computation cost is
                often expensive.
            save_suppl_info (bool): Various supplimentary information is saved to
                the file `save_to`. The default is True. This information is
                required to show birth and death pixels and optimal volumes.
                If you do not use such HomCloud's functionality and you want to
                reduce the size of the file, please set the argument ``False``.
                If False, only birth and death times are stored to the file.
            save_boundary_map (bool):
                The boundary map constructed by the given pointcloud is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles.
            periodicity (tuple[tuple[float, float], tuple[float, float], tuple[float, float]] or None):
                Periodic boundary condition.
            save_phtrees (bool): The PH-trees for (n-1)st PH is saved if True.
                Use meth:`PD.load_phtrees` to load the PH trees.
        Returns:
            The :class:`PDList` object computed from the pointcloud.

        Examples:
            >>> import homcloud.interface as hc
            >>> pointcloud = hc.example_data("tetrahedron")
            >>> hc.PDList.from_alpha_filtration(pointcloud)
            -> Returns a new PDList
        """
        assert indexed
        assert (save_phtrees and save_boundary_map) or (not save_phtrees)

        pointcloud = pointcloud.astype(float)
        num_points = pointcloud.shape[0]
        dim = pointcloud.shape[1] - int(weight is True) - int(subsets is True)

        if isinstance(weight, np.ndarray):
            pointcloud = np.hstack([pointcloud, weight.reshape(num_points, 1)])
            weight = True

        if isinstance(subsets, np.ndarray):
            pointcloud = np.hstack([pointcloud, subsets.reshape(num_points, 1)])
            subsets = True

        alpha_shape = alpha_filtration.AlphaShape.build(
            pointcloud, dim, weight, subsets, periodicity
        )

        if check_acyclicity:
            alpha_shape.check_subsets_acyclicity()
        if subsets:
            alpha_shape.become_partial_shape()

        filtration = alpha_shape.create_filtration(no_squared, vertex_symbols,
                                                   save_boundary_map, save_phtrees)

        output_filetype = PDList.estimate_format(output_filetype, save_to)

        return PDList.compute_pd(output_filetype, filtration, save_to, parallels,
                                 algorithm, save_suppl_info)

    @staticmethod
    def from_bitmap_levelset(array, mode="sublevel", type="bitmap",
                             algorithm=None, parallels=1,
                             periodicity=None, save_to=None, indexed=True,
                             save_suppl_info=True, save_boundary_map=False,
                             output_filetype=None):
        """
        Computes superlevel/sublevel PDList from an n-dimensional bitmap.

        Args:
            array (numpy.ndarray): An n-dimensional array.
            mode (string): The direction of the filtration.
               "superlevel" or "sublevel".
            type (string): An internal filtration type.
               "bitmap" or "cubical".
               You can change the internal file format by this parameter.
               The file size of "bitmap" format is much smaller than
               "cubical" and the computation for "bitmap" is
               faster than "cubical".
            algorithm (string, None): The name of the algorithm.
                An appropriate algorithm is
                automatically selected if None is given.

                The following algorithms are available:

                * "homccubes-0", "homccubes-1", "homccubes-2"
                * "phat-twist"
                * "phat-chunk-parallel"
                * "dipha"

                In many cases, the parameter should be `None`.
            parallels (int): The number of threads used for the computation.
                This parameter is used only if "dipha" algorithm is used.
            periodicity (None, list of bool):
                The list of booleans to specify the periodicity.
                For example, if your array is 2D and you want to make
                the array periodic only in 0-axis, you should give `[True, False]`.
                Any periodic structure is not used if None.
            save_to (string): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.
            indexed (bool): Always must be True.
            save_suppl_info (bool): Various supplimentary information is saved to
                the file `save_to`. The default is True. This information is
                required to show birth and death pixels and optimal_1_cycles.
                If you do not use such HomCloud's functionality and you want to
                reduce the size of the file, please set the argument ``False``.
                If False, only birth and death times are stored to the file.
            save_boundary_map (bool):
                The boundary map constructed by the given pointcloud is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles. This parameter is only available
                if the type is "cubical".

        Returns:
            The :class:`PDList` object computed from the bitmap.

        Examples:
            >>> import numpy as np
            >>> import homcloud.interface as hc
            >>> bitmap = np.array([[1.5, 2.0, 0.5],
            >>>                    [0.8, 4.1, 0.9],
            >>>                    [1.3, 1.8, 1.3]])
            >>> hc.PDList.from_bitmap_levelset(bitmap, "sublevel")
            -> Returns PDList object for sublevel persistence diagrams
            >>> hc.PDList.from_bitmap_levelset(bitmap, "superlevel",
            >>>                             periodicity=[True, True])
            -> Returns PDList object for superlevel PDList on a 2-torus
        """
        assert indexed

        array = array.astype(float, copy=False)
        if mode == "sublevel":
            flip_sign = False
        elif mode == "superlevel":
            array = -array
            flip_sign = True
        else:
            raise(ValueError("unknown mode: {}".format(mode)))

        bitmap = homcloud.bitmap.Bitmap(
            array, flip_sign, periodicity, save_boundary_map
        )
        if type == "cubical":
            filt = bitmap.build_cubical_filtration()
        else:
            filt = bitmap.build_bitmap_filtration()

        output_filetype = PDList.estimate_format(output_filetype, save_to)

        return PDList.compute_pd(output_filetype, filt, save_to, parallels,
                                 algorithm, save_suppl_info)

    @staticmethod
    def from_bitmap_distance_function(binary_pict, signed=False,
                                      metric="manhattan", type="bitmap",
                                      mask=None, algorithm=None,
                                      parallels=1, save_to=None, indexed=True,
                                      save_suppl_info=True, save_boundary_map=False,
                                      output_filetype=None):
        """
        This method is obsolete. Please use the combination of
        :meth:`PDList.from_bitmap_levelset` and
        :meth:`distance_transform` instead.

        Computes erosion/dilation PDList from an n-dimensional bitmap.

        In other words, this method computes the sublevel filtration
        whose level function is the distance function.

        Args:
            binary_pict (numpy.ndarray): An n-dimensional boolean array.
            signed (bool): The signed distance function is used
               instead of the normal distance function if True.
            metric (string): The metric. One of the followings:

               * "manhattan"
               * "chebyshev"
               * "euclidean"

            type (string): An internal filtration type.
               "bitmap" or "cubical".
               You can change the internal file format by this parameter.
               The file size of "bitmap" format is much smaller than
               "cubical". However, if you want to use the following
               functionality, you must use "cubical" format.

               * optimal volume/volume optimal cycle
               * dependency check for a field

            mask (numpy.ndarray or None): The mask bitmap.
            algorithm (string, None): The name of the algorithm.
                An appropriate algorithm is
                automatically selected if None is given.

                The following algorithms are available:

                * "homccubes-0", "homccubes-1", "homccubes-2"
                * "phat-twist"
                * "phat-chunk-parallel"
                * "dipha"

                In many cases, the parameter should be `None`.
            parallels (int): The number of threads used for the computation.
                This parameter is used only if "dipha" algorithm is used.
            save_to (string): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.
            save_boundary_map (bool):
                The boundary map constructed by the given pointcloud is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles.

        Returns:
            The :class:`PDList` object computed from the bitmap.

        """
        warnings.warn(
            "interface.PDList.from_bitmap_distance_function is obsolete."
            "Please use interaface.distance_transform and BitmapPHTreesPair.",
            PendingDeprecationWarning
        )
        return PDList.from_bitmap_levelset(
            distance_transform(binary_pict, signed, metric, None, mask),
            "sublevel", type, algorithm, parallels, None, save_to, indexed,
            save_suppl_info, save_boundary_map, output_filetype
        )

    @staticmethod
    def from_rips_filtration(distance_matrix, maxdim, maxvalue=np.inf,
                             simplicial=False, vertex_symbols=None,
                             algorithm=None, parallels=1, save_boundary_map=False,
                             save_to=None):
        """
        Compute a PDList from a distance matrix by using Vietoris-Rips
        filtrations.

        Args:
            distance_matrix (numpy.ndarary): KxK distance matrix.
            maxdim (int): Maximal homology degree computed.
            maxvalue (float): Maximal distance for constructing a filtration.
                All longer edges do not apper in the constructed filtration.
            simplicial (bool): If True, construct a simplicial complex for 
                :meth:`Pair.optimal_volume` (slow)
            vertex_symbols (list[string] or None): The names of vertices.
                The names are used to represent some simplices, such as
                birth/death simplices or optimal volumes.

                If None is given, vertices are automatically named by
                "0", "1", "2", ...
            algorithm: The name of the algorithm. An appropriate algorithm is
                automatically selected if None is given.

                If simplicial is False, "dipha" and "ripser" are available.
                If simpliclal is True, "dipha", "phat-twist", "phat-chunk-parallel"
                are availbale.

            paralles: The number of threads for computation. This value is
                used only if algorith is "dipha".
            save_boundary_map (bool):
                The boundary map constructed by the given distance matrix is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles. This option is only available
                if `simplicial` is True.
            save_to (string or None): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.

        Returns:
            The :class:`PDList` object computed from the distance matrix.

        """
        dm = rips.DistanceMatrix(distance_matrix, maxdim, maxvalue, vertex_symbols)
        if simplicial:
            filtration = dm.build_simplicial_filtration(save_boundary_map)
        else:
            filtration = dm.build_rips_filtration()

        return PDList.compute_pd(PDList.FileType.PDGM, filtration, save_to,
                                 parallels, algorithm, True)

    @staticmethod
    def from_boundary_information(boundary, levels, symbols=None,
                                  algorithm=None, parallels=1, save_to=None,
                                  save_boundary_map=False):
        """
        Compute a PDList from a boundary map and level information
        for abstract combinatorial complex.

        Args:
            boundary (list of (int, list of int, list of int)):
                list of (dim of cell, list of indices of, list of coefs)
            levels (numpy.ndarray): level of each cell.
            symbols (list of string, None): The names of each cell.
            algorithm (string, nil): The name of the algorithm.
                An appropriate algorithm is automatically selected if None is given.
            save_to (string or None): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.
            save_boundary_map (bool):
                The boundary map constructed by the given pointcloud is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles.

        Returns:
            :class:`PDList`: The PDList computed from the boundary map.
        """
        assert len(boundary) == len(levels)
        assert symbols is None or len(symbols) == len(boundary)
        for k in range(len(levels) - 1):
            assert levels[k] <= levels[k + 1]

        maxdim = 0
        for column in boundary:
            maxdim = max(maxdim, column[0])
        if symbols is None:
            symbols = [str(n) for n in range(len(levels))]

        filtration = abstract_filtration.AbstractFiltration(
            boundary, maxdim, levels, symbols, save_boundary_map
        )

        return PDList.compute_pd(PDList.FileType.PDGM, filtration, save_to,
                                 1, algorithm, True)

    def save(self, dest):
        """Save the PDList into `dest`.

        Args:
            dest (string): The filepath which the diagram data is saved into.
        """
        with open(dest, "wb") as destfile:
            srcfile = self.reader.infile
            srcfile.seek(0)
            shutil.copyfileobj(srcfile, destfile)

    def dth_diagram(self, d, load_indexed_pairs=True):
        """Return `d`-th persistence diagram from PDList.

        Args:
            d (int): the degree of the diagram
            load_indexed_pairs (bool): index information is loaded if True.
                Otherwise, the information is not loaded. This parameter will
                be helpful to reduce the loading time.
        Returns:
            The :class:`PD` object.

        """
        if self.filetype == PDList.FileType.PDGM:
            return PD(self.path, pdgm.PDGM(self.reader, d, load_indexed_pairs))
        elif self.filetype == PDList.FileType.IDIAGRAM:
            return PD(self.path, homdiag.PD.load(self.filetype.value, self.path, d))

    __getitem__ = dth_diagram

    def invoke_gui_plotter(self, d, x_range=None, xbins=None,
                           y_range=None, ybins=None,
                           colorbar={"type": "linear"},
                           title=None, unit_name=None, aspect="equal",
                           optimal_volume=False,
                           optimal_volume_options=None):
        """Invoke the GUI plotter.

        Args:
            d (int): The degree of the PD.
        """
        def format_range(r):
            return "[{}:{}]".format(r[0], r[1])

        options = ["-d", str(d)]
        if x_range:
            options.extend(["-x", format_range(x_range)])
        if xbins:
            options.extend(["-X", str(xbins)])
        if y_range:
            options.extend(["-y", format_range(y_range)])
        if ybins:
            options.extend(["-Y", str(ybins)])
        if colorbar["type"] == "linear":
            pass
        elif colorbar["type"] == "log":
            options.append("-l")
        elif colorbar["type"] == "loglog":
            options.append("--loglog")
        if "max" in colorbar:
            options.extend(["--vmax", str(colorbar["max"])])
        if title is not None:
            options.extend(["--title", str(title)])
        if unit_name is not None:
            options.extend(["--unit-name", str(unit_name)])
        options.extend(["--aspect", aspect])
        if optimal_volume:
            options.extend(["--optimal-volume", "on"])
        subprocess.Popen([sys.executable, "-m", "homcloud.plot_PD_gui"] +
                         options + [self.path])

    def bitmap_phtrees(self, degree):
        """
        Read a :class:`BitmapPHTrees` object computed by
        :meth:`BitmapPHTrees.for_bitmap_levelset`.

        Args:
           degree (int): The PD degree. 0 or (n-1).

        Returns:
           A :class:`BitmapPHTrees` object
        """
        from .bitmap_phtrees import BitmapPHTrees
        treedict = self.reader.load_simple_chunk("bitmap_phtrees", degree)
        return BitmapPHTrees(treedict, self.reader.metadata["sign_flipped"])

    def check_coefficient_problem(self):
        pdgm = self.dth_diagram(0).pd
        checker = int_reduction.build_checker(pdgm.input_dim,
                                              pdgm.boundary_map_chunk)
        return checker.check()


#: Obsolete, for backward compatibility
PDs = PDList


@forwardable()
class PD(object):
    """
    The class for a single persistence diagram.

    You can get the object of this class by :meth:`PDList.dth_diagram` or
    :meth:`PDList.__getitem__`.

    Attributes:
        path (str): File path
        degree (int): Degree of the PD
        births (numpy.ndarray[num_of_pairs]): Birth times
        deaths (numpy.ndarray[num_of_pairs]): Death times
        birth_positions: Birth positions for birth-death pairs
        death_positions: Death positions for birth-death pairs
        essential_births (numpy.ndarray[num_of_ess_pairs]):
            Birth times of essenatial birth-death pairs (birth-death pairs with
            infinite death time)
        essential_birth_positions:
            Birth positions for essenatial birth-death pairs
    """

    def __init__(self, path, pd):
        self.path = path
        self.pd = pd

    def __repr__(self):
        return "PD(path=%s, d=%d)" % (self.path, self.pd.degree)

    def birth_death_times(self):
        """
        Returns the  birth times and death times.

        Returns:
            tuple[numpy.ndarray, numpy.ndarray]:
                The pair of birth times and death times
        """
        return self.pd.births, self.pd.deaths

    def_delegators("pd",
                   "degree,births,deaths,birth_positions,death_positions,"
                   "essential_births,essential_birth_positions,sign_flipped,"
                   "filtration_type")

    def histogram(self, x_range=None, x_bins=128, y_range=None, y_bins=None,):
        """
        Returns the histogram of the PD.

        This is the shortcut method of :meth:`HistoSpec.pd_histogram`

        Args:
           x_range (tuple[float, float] or None): The lower and upper range
               of the bins on x-axis. If None is given, the range
               is determined from the minimum and maximum of
               the birth times and death times of all pairs.
           y_range (int): The number of bins on x-axis.
           y_range (tuple[float, float] or None): The lower and upper range
               of the bins on y-axis. Same as `x_range` if None is given.
           y_bins (int or None): The number of bins on y-axis.
               Same as `x_bins` if None is given.

        Returns:
            The :class:`Histogram` object.
        """
        return HistoSpec(x_range, x_bins, y_range, y_bins, self.pd).pd_histogram(self.pd)

    def load_phtrees(self):
        """
        Load a PH trees from the diagram.

        This method is available only for the (n-1)th diagram of an alpha filtration
        of n-dimensional pointcloud.

        You should compute the PH trees by :meth:`PDList.from_alpha_filtration`
        with ``save_phtrees=True`` before using this method.

        Returns:
            The :class:`PHTrees` object of the (n-1)th PH.
        """
        from .phtrees import PHTrees
        assert self.degree == self.pd.input_dim - 1
        return PHTrees.from_pdgm(self.pd)

    def pair(self, nth):
        """Returns `nth` birth-death pairs.

        Args:
            nth (int): Index of the pair.

        Returns:
            :class:`Pair`: The nth pair.
        """
        return Pair(self, nth)

    def pairs(self):
        """Returns all pairs of the PD.

        Returns:
            list of :class:`Pair`: All birth-death pairs.
        """
        return [self.pair(n) for n in range(self.pd.num_pairs)]

    def nearest_pair_to(self, x, y):
        """Returns a pair closest to `(x, y)`.

        Args:
            x (float): X (birth) coordinate.
            y (float): Y (death) coordinate.

        Returns:
            :class:`Pair`: The cleosest pair.
        """
        return self.spatial_searcher.nearest_pair(x, y)

    @cached_property
    def spatial_searcher(self):
        return SpatialSearcher(self.pairs(), self.births, self.deaths)

    def pairs_in_rectangle(self, xmin, xmax, ymin, ymax):
        """Returns all pairs in the rectangle.

        Returns all birth-death pairs whose birth time is in
        the interval `[xmin, xmax]` and
        whose death time is in `[ymin, ymax]`.

        Args:
           xmin (float): The lower range of birth time.
           xmax (float): The upper range of birth time.
           ymin (float): The lower range of death time.
           ymax (float): The upper range of death time.

        Returns:
           list of :class:`Pair`: All birth-death pairs in the rectangle.
        """
        return self.spatial_searcher.in_rectangle(xmin, xmax, ymin, ymax)

    @staticmethod
    def empty():
        """Returns a persistence diagram which has no birth-death pairs.

        Returns:
            PD: A PD object with no birth-death pair.
        """
        return PD(None, pdgm.empty_pd())

    def slice_histogram(self, x1, y1, x2, y2, width, bins=100):
        """Returns 1D histogram of birth-death pairs in a thin strip.

        This method computes a 1D hitogram of birth-death pairs
        in the thin strip whose center line is
        `(x1, y1) - (x2, y2)` and whose width is `width`.

        Args:
            x1 (float): The x(birth)-coordinate of the starting point.
            y1 (float): The y(death)-coordinate of the starting point.
            x2 (float): The x(birth)-coordinate of the ending point.
            y2 (float): The y(death)-coordinate of the ending point.
            width (float): Width of the strip.
            bins (int): The number of bins.

        Returns:
            :class:`SliceHistogram`: The histogram.
        """
        transl, mat = plot_PD_slice.transform_to_x_axis(
            np.array([x1, y1]), np.array([x2, y2])
        )
        xy = np.dot(mat, np.array([self.births, self.deaths]) - transl.reshape(2, 1))
        mask = (xy[0, :] >= 0) & (xy[0, :] <= 1) & (np.abs(xy[1, :]) < width / 2)
        values, edges = np.histogram(xy[0, mask], bins, (0, 1))
        return SliceHistogram(values, edges, x1, y1, x2, y2)

    def optvol_optimizer_builder(self, cutoff_radius, num_retry, lp_solver):
        if cutoff_radius is None:
            return optvol.OptimizerBuilder(
                self.degree, self.pd.boundary_map_chunk, lp_solver
            )
        else:
            if self.filtration_type == "alpha":
                return optvol.OptimizerBuilder.from_alpha_pdgm(
                    self.pd, cutoff_radius, num_retry, lp_solver
                )
            elif self.filtration_type == "cubical":
                return optvol.OptimizerBuilder.from_cubical_pdgm(
                    self.pd, cutoff_radius, num_retry, lp_solver
                )
            else:
                raise(ValueError("cutoff is not available for {}".format(
                    self.filtration_type
                )))


class Pair(object):
    """
    A class representing a birth-death pair.

    Attributes:
        diagram (:class:`PD`): The diagram which the birth-death pair
            belongs to.
    """

    def __init__(self, diagram, nth):
        self.diagram = diagram
        self.nth = nth

    def __iter__(self):
        return (self.birth_time(), self.death_time()).__iter__()

    def birth_time(self):
        """Returns the birth time of the pair.

        Returns:
            float: The birth time
        """
        return self.diagram.births[self.nth]

    def death_time(self):
        """Returns the death time of the pair.

        Returns:
            float: The death time
        """
        return self.diagram.deaths[self.nth]

    #: float: The birth time
    birth = property(birth_time)
    #: float: The death time
    death = property(death_time)

    @property
    def birth_position(self):
        """Birth position for birth-death pairs"""
        return self.diagram.birth_positions[self.nth]

    birth_pos = property(operator.attrgetter("birth_position"))
    """ Alias of :attr:`birth_position` """

    @property
    def death_position(self):
        """Death position for birth-death pairs"""
        return self.diagram.death_positions[self.nth]

    death_pos = property(operator.attrgetter("death_position"))
    """ Alias of :attr:`death_position` """

    @property
    def birth_index(self):
        return self.diagram.pd.birth_indices[self.nth]

    @property
    def death_index(self):
        return self.diagram.pd.death_indices[self.nth]

    @property
    def birth_position_symbols(self):
        return self.diagram.pd.alpha_symbol_resolver().resolve_cell(self.birth_index)

    @property
    def death_position_symbols(self):
        return self.diagram.pd.alpha_symbol_resolver().resolve_cell(self.death_index)

    def optimal_volume(self, cutoff_radius=None, solver=None, solver_options=[],
                       constrain_birth=False, num_retry=4,
                       integer_programming=False, ):
        """Return the optimal volume of the pair.

        Args:
            cutoff_radius (float or None):
                The cutoff radius. Simplices which are further from
                the center of birth and death simplices than
                `cutoff_radius` are ignored for the computation of
                an optimal volume. You can reduce the computation time
                if you set the `cutoff_radius` properly.
                Too small `cutoff_radius` causes the failure of the computation.
                If this argument is None, all simplices are not ignored.
            solver (string or None): The name of the LP solver.
                The default solver (coinor Clp) is selected if None is given.
            constrain_birth (bool): Now this value is not used.
            num_retry (int): The number of retry.
                The cutoff_radius is doubled at every retrial.
            integer_programming (bool): Integer constrains are used if True.
                Integer constrains make the computation slower, but
                possibly you get a better result.

        Returns:
            :class:`OptimalVolume`: The optimal volume.

        Raises:
            VolumeNotFound: Raised if the volume is not fould.
        """
        lp_solver = optvol.find_lp_solver(solver, solver_options)
        ovfinder = optvol.OptimalVolumeFinder(
            self.diagram.optvol_optimizer_builder(cutoff_radius, num_retry,
                                                  lp_solver)
        )

        result = ovfinder.find(self.birth_index, self.death_index)
        self.check_optimal_volume_error(result)
        return OptimalVolume(self, result)

    def check_optimal_volume_error(self, result):
        if isinstance(result, optvol.Failure):
            result.pair = tuple(self)
            raise(VolumeNotFound(result.status, result.message))

    def stable_volume(self, threshold, cutoff_radius=None, solver=None,
                      solver_options=[], constrain_birth=False, num_retry=4,
                      integer_programming=False):
        """Returns the stable volume of the pair.

        Args:
            threshold (float): The noise bandwidth.
            cutoff_radius (float or None):
                The cutoff radius. Simplices which are further from
                the center of birth and death simplices than
                `cutoff_radius` are ignored for the computation of
                an optimal volume. You can reduce the computation time
                if you set the `cutoff_radius` properly.
                Too small `cutoff_radius` causes the failure of the computation.
                If this argument is None, all simplices are not ignored.
            solver (string or None): The name of the LP solver.
                The default solver (coinor Clp) is selected if None is given.
            solver_options (list of string): Options for LP sovlers.
                The options are forwarded to Pulp program.
            constrain_birth (bool): Ignored
            num_retry (int): The number of retry.
                The cutoff_radius is doubled at every retrial.
            integer_programming (bool): Ignored.
        Returns:
            :class:`StableVolume`: The stable volume.
        """
        lp_solver = optvol.find_lp_solver(solver, solver_options)
        finder = optvol.TightenedVolumeFinder(
            self.diagram.optvol_optimizer_builder(cutoff_radius, num_retry, lp_solver),
            self.diagram.pd.index_to_level, threshold
        )
        result = finder.find(self.birth_index, self.death_index)
        self.check_optimal_volume_error(result)
        return StableVolume(self, result, threshold)

    tightened_volume = stable_volume

    def optimal_1_cycle(self):
        """Returns the optimal (not volume-optimal) 1-cycle
        corresponding to the birth-death pair.

        This method is available only for a bitmap filtration.

        Returns:
            :class:`BitmapOptimal1Cycle`: The optimal 1-cycle.

        Raises:
            AssertionError: Raised if the filtration is not a bitmap filtration
                or the degree of the pair is not 1.
        """
        assert self.degree == 1
        if self.diagram.filtration_type == "bitmap":
            return self.bitmap_optimal_1_cycle()
        else:
            return self.boundary_map_optimal_1_cycle()
        
    def bitmap_optimal_1_cycle(self):
        finder = pict_opt1cyc.Finder(self.diagram.pd)
        return BitmapOptimal1Cycle(finder.query_pair(self.birth_index, self.death_index))

    def boundary_map_optimal_1_cycle(self):
        return Optimal1Cycle(self, opt1cyc.search_on_chunk_bytes(
            self.diagram.pd.boundary_map_bytes, self.birth_index
        ))

    def __eq__(self, other):
        return (isinstance(other, Pair) and
                self.diagram == other.diagram and
                self.nth == other.nth)

    def __repr__(self):
        return "Pair({}, {})".format(self.birth_time(), self.death_time())

    def lifetime(self):
        """The lifetime of the pair.

        Returns:
            float: The lifetime (death - birth) of the pair.
        """
        return self.death_time() - self.birth_time()

    def __hash__(self):
        return(id(self.diagram) + (int(self.nth) << 20))

    @property
    def degree(self):
        """The degree of the pair.
        """
        return self.diagram.degree

    def ph0_components(self, epsilon=0.0):
        assert self.diagram.filtration_type in ["alpha"]
        return PH0Components(self, epsilon)
