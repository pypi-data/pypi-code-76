import operator

from forwardable import forwardable

import homcloud.optvol as optvol
import homcloud.paraview_interface as pv_interface


@forwardable()
class Volume(object):
    """
    This class represents a volume.
    This is the superclass of OptimalVolume, StableVolume and
    StableSubvolume.

    Notes:
        * point: list of float
        * cell: simplex or cube, simplex is used if the filtration is
          simplicial (alpha filtration) and cube is used if the filtration
          is cubical.
        * simplex: list of point
        * cube: tuple[point, list of {0, 1}],
        * ssimplex: list of string
    """

    def __init__(self, pair, result):
        self.pair = pair
        self.diagram = pair.diagram
        self.result = result

    def birth_time(self):
        """
        Returns:
            float: The birth time.
        """
        return self.pair.birth_time()

    def death_time(self):
        """
        Returns:
            float: The death time.
        """
        return self.pair.death_time()

    def lifetime(self):
        """
        Returns:
            float: The lifetime of the pair.
        """
        return self.death_time() - self.birth_time()

    def death_position(self):
        """
        Returns:
            simplex: The death simplex.
        """
        return self.pair.death_position

    @property
    def geom_resolver(self):
        return self.diagram.pd.geometry_resolver(False)

    @property
    def symbol_resolver(self):
        return self.diagram.pd.alpha_symbol_resolver()

    def points(self):
        """
        Returns:
            list of point: All vertices in the optimal volume.
        """
        return self.geom_resolver.resolve_vertices(self.result.cell_indices)

    def points_symbols(self):
        """
        Returns:
            list of string: All vertices in the optimal volume
            in the form of the symbolic representation.
        """
        return self.symbol_resolver.resolve_vertices(self.result.cell_indices)

    def boundary_points(self):
        """
        Returns:
            list of point: All vertices in the volume optimal cycle.
        """
        return self.geom_resolver.resolve_vertices(self.boundary_cells())

    def boundary_points_symbols(self):
        """
        Returns:
            list of string: All vertices in the volume optimal cycle
            in the form of the symbolic representation.
        """
        return self.symbol_resolver.resolve_vertices(self.boundary_cells())

    def boundary_cells(self):
        return self.geom_resolver.boundary_cells(self.result.cell_indices)

    def boundary(self):
        """
        Returns:
            list of cells: All cells in the volume optimal cycle.
        """
        return self.geom_resolver.resolve_cells(self.boundary_cells())

    def boundary_symbols(self):
        """
        Returns:
            list of ssimplex: All simplices in the volume optimal cycle
            in the form of the symbolic representation.
        """
        return self.symbol_resolver.resolve_cells(self.boundary_cells())

    def cells(self):
        """
        Returns:
            list of cell: All cells in volume optimal cycles.
        """
        return self.geom_resolver.resolve_cells(self.result.cell_indices)

    def simplices(self):
        """
        Returns:
            list of simplex: All simplices in volume optimal cycles.
        """
        return self.cells()

    def simplices_symbols(self):
        """
        Returns:
            list of ssimplex: All simplices in volume optimal cycles
            in the form of the symbolic representation.
        """
        return self.symbol_resolver.resolve_cells(self.result.cell_indices)

    volume_simplices_symbols = simplices_symbols

    def cubes(self):
        """
        Returns:
            list of cube: All cubes in volume optimal cycles.
        """
        return self.cells()

    def children(self):
        """
        Returns:
           list of :class:`Pair`: All children pairs.
        """
        from .pd import Pair
        death_to_number = self.diagram.pd.death_index_to_pair_number

        def valid(d):
            return d != self.pair.death_index and d in death_to_number

        return [
            Pair(self.diagram, death_to_number[d])
            for d in self.result.cell_indices if valid(d)
        ]

    def to_dict(self):
        """
        Returns:
            dict: The information about the optimal volume.
        """
        raise(NotImplementedError("hc.interface.Pair.to_dict"))

    #: The alias of :meth:`death_position`.
    death_pos = death_position

    def to_paraview_node(self, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode` object
        to visulize an optimal volume.

        You can show the optimal volume by
        :meth:`homcloud.paraview_interface.show`. You can also
        adjust the visual by the methods of
        :class:`homcloud.paraview_interface.PipelineNode`.

        Args:
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.PipelineNode: A PipelineNode object.
        """
        return OptimalVolume.to_paraview_node_for_volumes([self], gui_name)

    to_pvnode = to_paraview_node

    @staticmethod
    def to_paraview_node_for_volumes(volumes, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode` object
        to visulize multiple optimal volumes.

        All optimal volumes should come from the same :class:`PD` object.

        Args:
            volumes (list of :class:`OptimalVolume`): The optimal volumes to be
                visualized.
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.PipelineNode: A PipelineNode object.
        """
        diagram = volumes[0].diagram
        if diagram.filtration_type == "alpha":
            geom_resolver = diagram.pd.alpha_coord_resolver()
            drawer = optvol.drawer_for_alpha(geom_resolver.vertices)
        elif diagram.filtration_type == "cubical":
            geom_resolver = diagram.pd.cubical_geometry_resolver()
            drawer = optvol.drawer_for_cubical(geom_resolver.shape)
        optvol.draw_volumes(drawer, map(operator.attrgetter("result"), volumes),
                            geom_resolver)
        f = pv_interface.TempFile(".vtk")
        drawer.write(f)
        f.close()
        return pv_interface.VTK(f.name, gui_name, f).set_representation("Wireframe")


@forwardable()
class OptimalVolume(Volume):
    """
    This class represents an optimal volume.
    """

    def birth_position(self):
        """
        Returns:
            simplex: The birth simplex.
        """
        return self.pair.birth_position

    #: The alias of :meth:`birth_position`.
    birth_pos = birth_position

    def stable_subvolume(self, threshold, solver=None, solver_options=[]):
        """
        Returns the stable subvolume of the optimal volume.

        Args:
            threshold (float): The noise bandwidth.
        Returns:
            StableSubvolume: The stable subvolume.
        """
        lp_solver = optvol.find_lp_solver(solver, solver_options)
        ssvfinder = optvol.TightenedSubVolumeFinder(
            self.diagram.optvol_optimizer_builder(None, None, lp_solver),
            self.diagram.pd.index_to_level, threshold
        )
        result = ssvfinder.find(self.pair.birth_index, self.pair.death_index,
                                self.result.cell_indices)
        return StableSubvolume(self.pair, result, threshold)

    tightened_subvolume = stable_subvolume


@forwardable()
class EigenVolume(Volume):
    """
    This class represents an "eigenvolume". It is the superclass of
    StableVolume and StableSubvolume.

    Attributes:
        threshold (float): The threshold used for the computation of the
            eigenvolume.
    """
    def __init__(self, pair, result, threshold):
        super().__init__(pair, result)
        self.threshold = threshold


class StableVolume(EigenVolume):
    """
    This class represents a stable volume.

    The instance is given by :meth:`Pair.stable_volume`.
    """
    pass


class StableSubvolume(EigenVolume):
    """
    This class represents a stable subvolume.

    The instance is given by :meth:`OptimalVolume.stable_subvolume`.
    """
    pass
