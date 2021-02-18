import homcloud.phtrees as phtrees
import homcloud.paraview_interface as pv_interface
from homcloud.spatial_searcher import SpatialSearcher

class PHTrees(object):
    """
    This class represents PH trees computed from an alpha filtration.

    Please see `<https://arxiv.org/abs/1712.05103>`_ if you want to know
    the details of optimal volumes and volume optimal cycles.

    You can compute the PH trees by :meth:`PDList.from_alpha_filtration`
    with ``save_boundary_map=True`` and ``save_phtrees=True`` arguments.

    .. You can compute the PH trees by :meth:`PD.phtrees` from the diagram.

    Example:
        >>> import homcloud.interface as hc
        >>> pointcloud = hc.example_data("tetrahedron")
        >>> pdlist = hc.PDList.from_alpha_filtration(pointcloud, save_phtrees=True)
        >>> # Computes PH trees and save them in "tetrahedron.pht"
        >>> pdlist.dth_diagram(2).phtrees(save_to="tetrahedron.pht")
        >>> # Load the file.
        >>> phtrees = hc.PHTrees("tetrahedron.pht")
        >>> # Query the node whose birth-death pair is nearest to (19, 21).
        >>> node = phtrees.node_nearest_to(19, 21)
        >>> # Show birth time and death time
        >>> node.birth_time()
        19.600000000000005
        >>> node.death_time()
        21.069444444444443
        >>> node.boundary_points()
        [[0.0, 0.0, 0.0], [8.0, 0.0, 0.0], [5.0, 6.0, 0.0], [4.0, 2.0, 6.0]]
        >>> node.boundary()
        [[[0.0, 0.0, 0.0], [5.0, 6.0, 0.0], [4.0, 2.0, 6.0]],
         [[0.0, 0.0, 0.0], [8.0, 0.0, 0.0], [5.0, 6.0, 0.0]],
         [[8.0, 0.0, 0.0], [5.0, 6.0, 0.0], [4.0, 2.0, 6.0]],
         [[0.0, 0.0, 0.0], [8.0, 0.0, 0.0], [4.0, 2.0, 6.0]]]

    """

    def __init__(self, orig, spatial_searcher):
        self.orig = orig
        self.spatial_searcher = spatial_searcher

    @staticmethod
    def from_pdgm(pdgm):
        return PHTrees(
            phtrees.PHTrees.from_pdgm(pdgm, PHTrees.Node),
            SpatialSearcher(pdgm.death_indices, pdgm.births, pdgm.deaths),
        )

    def nodes_of(self, pairs):
        """
        Returns the nodes of trees corresponding to birth-death pairs
        in `pairs`.

        Args:
            pairs (list of Pair): The list of pairs.

        Returns:
            list of :class:`PHTrees.Node`: The nodes.
        """
        return [self._resolver().phtree.nodes[pair.death_index]
                for pair in pairs]

    def pair_node_nearest_to(self, x, y):
        """
        Return the node corresponding the pair which is nearest to
        (`x`, `y`).

        Args:
            x (float): The birth-axis coordinate.
            y (float): The death-axis coordinate.

        Returns:
            PHTrees.Node: The nearest node.

        """
        return self.orig.nodes[self.spatial_searcher.nearest_pair(x, y)]

    def pair_nodes_in_rectangle(self, xmin, xmax, ymin, ymax):
        """
        Returns the list of nodes corresponding to the birth-death
        pairs in the given rectangle.

        Args:
           xmin (float): The minimum of the birth-axis of the rectangle.
           xmax (float): The maximum of the birth-axis of the rectangle.
           ymin (float): The minimum of the death-axis of the rectangle.
           ymax (float): The maximum of the death-axis of the rectangle.

        Returns:
           list of :class:`PHTrees.Node`: The nodes in the rectangle.

        """
        return [
            self.orig.nodes[death_index] for death_index
            in self.spatial_searcher.in_rectangle(xmin, xmax, ymin, ymax)
        ]

    def to_paraview_node_from_nodes(self, nodes, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode`
        object to visulize optimal volumes of the nodes.

        Args:
            nodes (list of :class:`PHTrees.Node`): The list of nodes to be visualized.
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.VTK: Paraview Pipeline node object.

        Notes:
            All nodes should be nodes of `self` PHTrees.
        """
        f = pv_interface.TempFile(".vtk")
        drawer = self.orig.coord_resolver.build_paraview_drawer(len(nodes), {})
        for i, node in enumerate(nodes):
            node.draw_volume(drawer, i)
        drawer.write(f)
        f.close()
        return pv_interface.VTK(f.name, gui_name, f).set_representation("Wireframe")

    to_pvnode_from_nodes = to_paraview_node_from_nodes

    class Volume(object):
        """
        The superclass of :class:`PHTrees.Node` and :class:`PHTrees.StableVolume`.

        Methods:
            birth_time()
                Returns:
                    float: The birth time of the corresponding birth-death pair.

            death_time()
                Returns:
                    float: The death time of the corresponding birth-death pair.

            lifetime()
                Returns:
                    float: The lifetime of the corresponding birth-death pair.

            simplices()
                Returns:
                    list of list of list of float, a.k.a list of simplex:
                        The simplices in the optimal volume.

            boundary()
                Returns:
                    list of list of float, a.k.a. list of points:
                        Points in the volume optimal cycle.

            birth_simplex()
                Returns the birth simplex.

            death_simplex()
                Returns the death simplex.

            ancestors()
                Returns:
                    list of :class:`PHTrees.Node`:
                        The ancestors of the tree node include itself.
        """

        def points(self):
            """
            Returns:
                list of list of float, a.k.a list of points:
                    Points in the optimal volume.
            """
            return self.vertices()

        def volume(self):
            return self.volume_nodes

        def boundary_points(self):
            """
            Returns:
                list of list of float, a.k.a list of points:
                    Points in the volume optimal cycle.
            """
            return self.boundary_vertices()

        def points_symbols(self):
            """
            Returns:
                list of string: All vertices in the optimal volume
                in the form of the symbolic representation.
            """
            return self.vertices("symbols")

        def volume_simplices_symbols(self):
            """
            Returns:
                list of list of string: All simplices in volume optimal cycles
                in the form of the symbolic representation.
            """
            return self.simplices("symbols")

        def boundary_points_symbols(self):
            """
            Returns:
                list of string: All vertices in the volume optimal cycle
                in the form of the symbolic representation.
            """
            return self.boundary_vertices("symbols")

        def boundary_symbols(self):
            """
            Returns:
                list of list of string: All simplices in the volume optimal cycle
                in the form of the symbolic representation.
            """
            return self.boundary("symbols")

        def living(self):
            """
            Returns:
                bool: True if the birth time and death time of the node
                are different.
            """
            return self.birth_time() != self.death_time()

        def to_paraview_node(self, gui_name=None):
            """
            Construct a :class:`homcloud.paraview_interface.PipelineNode`
            object to visulize an optimal volume of the node.

            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

            Returns:
                homcloud.paraview_interface.VTK: Paraview Pipeline node object.
            """
            f = pv_interface.TempFile(".vtk")
            drawer = self.trees.coord_resolver.build_paraview_drawer(1, {})
            self.draw_volume(drawer, 0)
            drawer.write(f)
            f.close()
            return pv_interface.VTK(f.name, gui_name, f).set_representation("Wireframe")

        to_pvnode = to_paraview_node

    class Node(Volume, phtrees.Node):
        """
        The class represents a tree node of :class:`PHTrees`.
        """

        def ancestors(self):
            ret = [self]
            while True:
                parent = self.trees.parent_of(ret[-1])
                if parent is None:
                    break
                ret.append(parent)

            return ret

        def living_descendants(self):
            return [node for node in self.volume_nodes if node.living()]

        def stable_volume(self, epsilon):
            """
            Args:
                epsilon (float): Duration noise strength

            Returns:
                :class:`PHTrees.StableVolume`: The stable volume

            """
            return super().stable_volume(epsilon, PHTrees.StableVolume)

        def __repr__(self):
            return "PHTrees.Node({}, {})".format(self.birth_time(),
                                                 self.death_time())

    class StableVolume(Volume, phtrees.StableVolume):
        """
        The class represents a stable volume in :class:`PHTrees`.
        """
        pass
