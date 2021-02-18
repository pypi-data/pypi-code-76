import argparse
import sys
import json
import re
from collections import namedtuple, defaultdict

import numpy as np
import pulp

from homcloud.version import __version__
from homcloud.spatial_searcher import SpatialSearcher
from homcloud.diagram import PD
from homcloud.visualize_3d import ParaViewSimplexDrawer, ParaViewCubeDrawer
from homcloud.utils import deep_tolist
from homcloud.index_map import MapType
from homcloud.argparse_common import parse_range, parse_bool


_debug_mode = False


def argument_parser():
    p = argparse.ArgumentParser(description="Compute volume optimal cycles")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-d", "--degree", type=int, required=True,
                   help="degree of PH")
    p.add_argument("-x", type=float, help="birth time of the pair")
    p.add_argument("-y", type=float, help="death time of the pair")
    p.add_argument("-X", "--x-range", type=parse_range,
                   help="birth time of the pair")
    p.add_argument("-Y", "--y-range", type=parse_range,
                   help="death time of the pair")
    p.add_argument("-c", "--cutoff-radius", type=float,
                   help="cut-off radius in R^n")
    p.add_argument("-T", "--type", default="volume",
                   help="type of optimal cycle (now only volume is available)")
    p.add_argument("-j", "--json-output", help="output in json format")
    p.add_argument("-v", "--vtk-output", help="output in vtk format")
    p.add_argument("-P", "--invoke-paraview", default=False, action="store_true",
                   help="invoke paraview for visualization")
    p.add_argument("-n", "--retry", type=int, default=0,
                   help="number of retry")
    p.add_argument("-C", "--optimal-cycle-children", default=False,
                   type=parse_bool)
    p.add_argument("--integer-programming", default=False,
                   type=parse_bool,
                   help="use integer programming (on/*off*)")
    p.add_argument("--debug", default=False, type=parse_bool,
                   help="debug mode (on/*off*)")
    p.add_argument("--solver", help="LP solver")
    p.add_argument("--constrain-on-birth-simplex", default=False,
                   action="store_true", help="constrain on the birth simplex")
    p.add_argument("--skip-infeasible", default=False, type=parse_bool,
                   help="skip infeasible (on/*off*)")
    p.add_argument("--draw-vertices", default=False, type=parse_bool,
                   help="draw vertices (on/*off*)")
    p.add_argument("--owned-volume", default=None, type=float,
                   metavar="THRESHOLD", help="Compute owned volumes")
    p.add_argument("--owned-volume-connected", default=False,
                   type=parse_bool, metavar="BOOL",
                   help="Output only the connecte component "
                   "of owned volume (on/*off*)")
    p.add_argument("--tightened-volume", default=None, type=float,
                   metavar="THRESHOLD", help="Compute tightened volumes")
    p.add_argument("--tightened-subvolume", default=None, type=float,
                   metavar="THRESHOLD", help="Compute tightened subvolumes")
    p.add_argument("--no-optimal-volume", metavar="BOOL", default=False,
                   type=parse_bool,
                   help="Optimal volume is not computed (on/*off*)")
    p.add_argument("--show-optimal-volume", metavar="BOOL", default=True,
                   type=parse_bool,
                   help="(default: TRUE)")
    p.add_argument("--threads", default=1, type=int, metavar="NUM_THREADS",
                   help="the number of threads to use by a LP solver, "
                   "this option is used when the solver is pulp-cbc-cmd")
    p.add_argument("-O", "--option", action="append", default=[],
                   help="Options for LP solver")
    p.add_argument("input", help="input file")
    return p


def main(args=None):
    if not args:
        args = argument_parser().parse_args()

    def vtk_required():
        return args.vtk_output or args.invoke_paraview

    check_args(args)
    diagram = PD.load_from_indexed_diphafile(args.input, args.degree, True)
    geom_resolver = diagram.geometry_resolver()
    vocfinder = VolumeOptimalCycleFinder.from_args(diagram, geom_resolver, args)
    spatial_searcher = build_spatial_searcher(diagram)
    query_args = build_query_args(args)

    if args.x is not None and args.y is not None:
        query = PointQuery(args.x, args.y, spatial_searcher,
                           vocfinder, diagram.index_map, **query_args)
    elif args.x_range and args.y_range:
        query = RectangleQuery(args.x_range, args.y_range, spatial_searcher,
                               vocfinder, diagram.index_map, **query_args)
    else:
        print("Please specify (x and y) or (x_range and y_range)")
        exit(11)

    try:
        query.invoke()
    except InfeasibleError as err:
        print(err.message, file=sys.stderr)
        exit(err.code)
    except RadiusSmallError as err:
        print(err.message, file=sys.stderr)
        exit(err.code)
    except pulp.solvers.PulpSolverError as err:
        print(pulp.LpStatus[pulp.solvers.PulpSolverError], file=sys.stderr)
        exit(err)

    if query.num_infeasible:
        print("Num infeasible: {}".format(query.num_infeasible),
              file=sys.stderr)

    if vtk_required():
        drawer = prepare_drawer_for_paraview(diagram)
        if args.draw_vertices:
            draw_all_vertices(drawer)
        query.draw(drawer)

        if args.vtk_output:
            drawer.output(args.vtk_output)
        if args.invoke_paraview:
            drawer.invoke()
    if args.json_output:
        with open(args.json_output, "w") as f:
            json.dump(query.to_jsondict(), f)


def build_spatial_searcher(diagram):
    return SpatialSearcher(
        list(zip(diagram.masked_birth_indices, diagram.masked_death_indices)),
        diagram.births, diagram.deaths
    )


def build_query_args(args):
    return {
        "skip_infeasible": args.skip_infeasible,
        "optimal_cycle_children": args.optimal_cycle_children,
        "owned_volume": args.owned_volume,
        "tightened_volume": args.tightened_volume,
        "tightened_subvolume": args.tightened_subvolume,
        "no_optimal_volume": args.no_optimal_volume,
        "owned_volume_connected_component": args.owned_volume_connected,
        "show_optimal_volume": args.show_optimal_volume,
    }


class Query(object):
    def __init__(self, spatial_searcher, vocfinder, index_map,
                 skip_infeasible=False, optimal_cycle_children=False,
                 owned_volume=None, tightened_volume=None,
                 tightened_subvolume=None, no_optimal_volume=False,
                 owned_volume_connected_component=False,
                 show_optimal_volume=True):
        self.spatial_searcher = spatial_searcher
        self.vocfinder = vocfinder
        self.index_map = index_map
        self.results = []
        self.num_infeasible = 0
        self.skip_infeasible = skip_infeasible
        self.optimal_cycle_children = optimal_cycle_children
        self.owned_volume = owned_volume
        self.owned_volume_connected_component = owned_volume_connected_component
        self.tightened_volume = tightened_volume
        self.tightened_subvolume = tightened_subvolume
        self.no_optimal_volume = no_optimal_volume
        self.children_index = 1
        self.show_optimal_volume = show_optimal_volume

    def query_pair(self, birth, death):
        result = Result(self.resolve_time(birth), self.resolve_time(death))
        if not self.no_optimal_volume:
            result.optimal_volume = self.query_optimal_volume(birth, death)

        if self.optimal_cycle_children:
            children_volumes = self.vocfinder.query_children(result.optimal_volume)
            self.numbering_children(children_volumes)
            result.children_volumes = children_volumes

        if self.tightened_volume:
            result.tightened_volume = self.query_tightened_volume(birth, death)

        if self.tightened_subvolume:
            result.tightened_subvolume = self.query_tightened_subvolume(
                result.optimal_volume
            )

        if self.owned_volume:
            result.owned_volume = self.query_owned_volume(
                result.optimal_volume, result.children_volumes
            )

        self.results.append(result)

    def query_optimal_volume(self, birth, death):
        optimal_volume, status = self.vocfinder.query(birth, death)
        if not optimal_volume:
            print(status.message, file=sys.stderr)
            if status.code == pulp.LpStatusInfeasible and self.skip_infeasible:
                self.num_infeasible += 1
                return None
            else:
                raise InfeasibleError(status.message, -(status.code - 1))
        return optimal_volume

    def query_tightened_volume(self, birth, death):
        lower_time = self.resolve_time(birth) + self.tightened_volume
        new_birth = np.searchsorted(self.index_map.levels, lower_time) - 1
        volume = self.query_optimal_volume(new_birth, death)
        return TightenedVolume(volume.volume_cells, birth, death,
                               self.tightened_volume, self.vocfinder.diagram)

    def query_tightened_subvolume(self, optimal_volume):
        tightened_subvolume, status = self.vocfinder.query_tightened_subvolume(
            optimal_volume, self.tightened_subvolume
        )
        if tightened_subvolume:
            return tightened_subvolume
        else:
            print(status.message, file=sys.stderr)
            self.query_failure(status)

    def query_owned_volume(self, optimal_volume, children_volumes):
        if not children_volumes:
            children_volumes = self.vocfinder.query_children(optimal_volume)
        owned_volume_cells = OwnedVolumeSolver(
            optimal_volume, children_volumes, self.owned_volume,
            self.owned_volume_connected_component,
        ).solve()
        return OwnedVolume(owned_volume_cells, optimal_volume.birth,
                           optimal_volume.death, self.owned_volume,
                           optimal_volume.diagram)

    def resolve_time(self, cell):
        return self.index_map.resolve_level(cell)

    def query_failure(self, status):
        exit(-(status.code - 1))

    def numbering_children(self, children_volumes):
        for child_volume in children_volumes:
            child_volume.child_index = self.children_index
            self.children_index += 1

    def draw(self, drawer):
        for (i, volume) in enumerate(self.results):
            volume.draw(drawer, i, self.show_optimal_volume)

    def to_jsondict(self):
        return {
            "format-version": Query.FORMAT_VERSION,
            "query": self.queryinfo_jsondict(),
            "dimension": self.vocfinder.diagram.index_map.dimension,
            "num-volumes": len(self.results),
            "num-infeasible": self.num_infeasible,
            "result": self.result_jsondicts(),
        }

    def common_queryinfo_jsondict(self):
        return {
            "query-target": "volume-optimal-cycle",
            "degree": self.vocfinder.degree,
            "cutoff-radius": self.vocfinder.cutoff_radius,
            "num-retry": self.vocfinder.num_retry,
            "integer-programming": self.vocfinder.integer_programming,
            "constrain-on-birth-simplex": self.vocfinder.constrain_birth,
            "skip-infeasible": self.skip_infeasible,
            "optimal-cycle-children": self.optimal_cycle_children,
            "solver": self.vocfinder.solver_real_name(),
            "owned-volume": self.owned_volume,
            "owned-volume-connected-component":
            self.owned_volume_connected_component,
            "tightened-volume": self.tightened_volume,
            "tightened-subvolume": self.tightened_subvolume,
            "no-optimal-cycle": self.no_optimal_volume,
        }

    FORMAT_VERSION = 1.1

    def result_jsondicts(self):
        return [volume.to_jsondict() for volume in self.results]


class PointQuery(Query):
    def __init__(self, x, y, spatial_searcher, vocfinder, index_map, **kwargs):
        super().__init__(spatial_searcher, vocfinder, index_map, **kwargs)
        self.x = x
        self.y = y

    def invoke(self):
        birth, death = self.spatial_searcher.nearest_pair(self.x, self.y)
        self.query_pair(birth, death)

    def queryinfo_jsondict(self):
        dic = {"query-type": "single", "birth": self.x, "death": self.y}
        dic.update(self.common_queryinfo_jsondict())
        return dic


class RectangleQuery(Query):
    def __init__(self, x_range, y_range, spatial_searcher, vocfinder,
                 index_map, **kw):
        super().__init__(spatial_searcher, vocfinder, index_map, **kw)
        self.x_range = x_range
        self.y_range = y_range

    def invoke(self):
        for (birth, death) in self.pairs_in_rectangle():
            self.query_pair(birth, death)

    def pairs_in_rectangle(self):
        return self.spatial_searcher.in_rectangle(
            self.x_range[0], self.x_range[1], self.y_range[0], self.y_range[1]
        )

    def queryinfo_jsondict(self):
        dic = {
            "query-type": "rectangle",
            "birth-range": self.x_range, "death-range": self.y_range
        }
        dic.update(self.common_queryinfo_jsondict())
        return dic


class IndexQuery(Query):
    def __init__(self, birth_index, death_index, vocfinder, index_map, **kw):
        super().__init__(None, vocfinder, index_map, **kw)
        self.birth_index = birth_index
        self.death_index = death_index

    def invoke(self):
        self.query_pair(self.birth_index, self.death_index)

    def queryinfo_jsondict(self):
        raise(RuntimeError("jsonize is not suuported"))


class VolumeOptimalCycleFinder(object):
    def __init__(self, diagram, degree,
                 cutoff_radius, solver_name, constrain_birth,
                 num_retry, integer_programming=False, threads=1, options=[]):
        self.diagram = diagram
        self.degree = degree
        self.geom_resolver = diagram.geometry_resolver()
        self.cutoff_radius = cutoff_radius
        self.solver_name = solver_name
        self.constrain_birth = constrain_birth
        self.num_retry = num_retry
        self.integer_programming = integer_programming
        self.signs = prepare_signs(degree, diagram.boundary_map_dict)
        self.threads = threads
        self.options = options

    @staticmethod
    def from_args(diagram, geom_resolver, args):
        return VolumeOptimalCycleFinder(
            diagram, args.degree, args.cutoff_radius,
            args.solver, args.constrain_on_birth_simplex,
            args.retry, args.integer_programming, args.threads, args.option
        )

    def query(self, birth, death, optimal_volume_class=None):
        for n in range(self.num_retry + 1):
            voc_indices, status = self.query_once(birth, death, n)
            if voc_indices:
                return (OptimalVolume(voc_indices, birth, death, self.diagram),
                        status)
        return (None, status)

    def query_once(self, birth, death, n):
        center = (self.geom_resolver.centroid(birth) +
                  self.geom_resolver.centroid(death)) / 2.0
        threshold = self.cutoff_radius * (2**n) if self.cutoff_radius else 0

        def is_active_cell(cell_idx):
            if self.cutoff_radius is None:
                return True
            centroid_cell = self.geom_resolver.centroid(cell_idx)
            return np.linalg.norm(center - centroid_cell) < threshold

        if not is_active_cell(death):
            raise (RadiusSmallError("Death cell not in cutoff sphere", 10))

        return self.solve_volume_optimal_cycle(
            birth, death,
            *self.collect_cells_for_lp(is_active_cell, birth, death)
        )

    def query_children(self, volume):
        children_volumes = []
        for (birth_child, death_child) in volume.children_pairs:
            child_volume, status = self.query(birth_child, death_child)
            if not child_volume:
                print(status.message, file=sys.stderr)
                continue
            children_volumes.append(child_volume)
        return children_volumes

    def add_boundary_on(self, cell, boundary_on_dict):
        for (j, sign) in zip(self.diagram.cell_boundary(cell), self.signs):
            if j in boundary_on_dict:
                boundary_on_dict[j].append((sign, cell))

    def collect_cells_for_lp(self, is_active_cell, birth_index, death_index):
        cell_dim = self.diagram.cell_dim

        boundary_on = dict()
        lpvar_indices = []

        for i in range(birth_index, death_index + 1):
            if cell_dim(i) == self.degree:
                boundary_on[i] = list()
            if cell_dim(i) == self.degree + 1 and is_active_cell(i):
                lpvar_indices.append(i)
                self.add_boundary_on(i, boundary_on)

        return boundary_on, lpvar_indices

    def collect_cells_for_tightened_subvolume(self, optimal_volume, threshold):
        birth_time = optimal_volume.birth_time()
        boundary_on = dict()
        lpvar_indices = []

        def is_optimal_volume_boundary(i):
            return (self.diagram.cell_dim(i) == self.degree and
                    self.resolve_time(i) > birth_time + threshold)

        for i in range(optimal_volume.birth, optimal_volume.death):
            if is_optimal_volume_boundary(i):
                boundary_on[i] = list()
        for cell in optimal_volume.volume_cells:
            lpvar_indices.append(cell)
            self.add_boundary_on(cell, boundary_on)

        return boundary_on, lpvar_indices

    def resolve_time(self, cell):
        return self.diagram.index_map.resolve_level(cell)

    def solve_volume_optimal_cycle(self, birth_index, death_index,
                                   boundary_on, lpvar_indices):
        lpvar_type = "Integer" if self.integer_programming else "Continuous"
        xs = ys = None

        def add_constrains_abs_x_lt_y(prob):
            for i in lpvar_indices:
                prob += xs[i] - ys[i] <= 0.0
                prob += xs[i] + ys[i] >= 0.0

        def add_constrains_on_banned_cells(prob):
            for (idx, constrain) in boundary_on.items():
                if not constrain:
                    continue
                if idx == birth_index:
                    continue
                prob += pulp.lpSum(sign * xs[i] for (sign, i) in constrain) == 0

        def add_constrain_on_death_cell(prob):
            prob += xs[death_index] == 1

        # def add_constrain_on_birth_cell(prob):
        #     prob += lpvar_birth == pulp.lpSum(
        #         sign * xs[i] for (sign, i) in boundary_on[death.index]
        #     )
        #     if constrain_on_birth == 0:
        #         return
        #     elif constrain_on_birth > 0:
        #         prob += lpvar_birth > 0.00001
        #     else:
        #         prob += lpvar_birth < -0.00001

        def volume_optimal_cells():
            if _debug_mode:
                print({i: xs[i].varValue for i in lpvar_indices
                       if ys[i].varValue >= 0.0001})
                print(xs[death_index].varValue)
            return [i for i in lpvar_indices if ys[i].varValue >= 0.00001]

        def error_status(status):
            if status == pulp.LpStatusUndefined:
                status_str = "Infeasible[Undefined]"
                status = pulp.LpStatusInfeasible
            else:
                status_str = pulp.LpStatus[status]

            message = "{} at ({}, {})".format(
                status_str,
                self.diagram.index_map.resolve_level(birth_index),
                self.diagram.index_map.resolve_level(death_index)
            )
            return QueryStatus(message, status)

        prob = pulp.LpProblem("VolumeOptimalCycle", pulp.LpMinimize)
        xs = pulp.LpVariable.dicts("x", (lpvar_indices, ),
                                   -1.0, 1.0, lpvar_type)
        ys = pulp.LpVariable.dicts("y", (lpvar_indices, ),
                                   0.0, 1.0, lpvar_type)
        # lpvar_birth = pulp.LpVariable("birth", -10.0, 10.0, "Continuous")
        prob += pulp.lpSum(ys.values())
        # add_constrain_on_birth_cell(prob)
        add_constrains_abs_x_lt_y(prob)
        add_constrains_on_banned_cells(prob)
        add_constrain_on_death_cell(prob)

        # workaround for cplex and pulp
        try:
            status = prob.solve(self.solver())
        except pulp.solvers.PulpSolverError as err:
            if self.is_infeasible_error(err):
                return (None, error_status(pulp.LpStatusInfeasible))
            else:
                raise err

        if status == pulp.LpStatusOptimal:
            return (volume_optimal_cells(), QueryStatus("OK", 0))
        else:
            return (None, error_status(status))

    def solver_real_name(self):
        return type(self.solver()).__name__

    def solver(self):
        if self.solver_name is None:
            return pulp.LpSolverDefault
        if self.solver_name == "coin":
            return pulp.COIN(options=self.options)
        if self.solver_name == "pulp-cbc-cmd":
            return pulp.PULP_CBC_CMD(threads=self.threads, options=self.options)
        if self.solver_name == "cplex":
            return pulp.CPLEX(options=self.options)
        if self.solver_name == "gurobi":
            return pulp.GUROBI(options=self.options)
        if self.solver_name == "glpk":
            return pulp.GLPK(options=self.options)
        if self.solver_name == "coinmp-dll":
            return pulp.COINMP_DLL(options=self.options)
        if self.solver_name == "cplex-dll":
            return pulp.CPLEX_DLL(options=self.options)
        raise RuntimeError("Unknown solver {}".format(self.solver_name))

    @staticmethod
    def is_infeasible_error(err):
        # For CPLEX workaround
        return re.search("infeasible", err.args[0])

    def query_tightened_subvolume(self, optimal_volume, threshold):
        volume, status = self.solve_volume_optimal_cycle(
            optimal_volume.birth, optimal_volume.death,
            *self.collect_cells_for_tightened_subvolume(optimal_volume, threshold)
        )
        if volume:
            return (TightenedSubvolume(volume,
                                       optimal_volume.birth,
                                       optimal_volume.death,
                                       threshold, self.diagram),
                    status)
        else:
            return (None, status)


QueryStatus = namedtuple("QueryStatus", ["message", "code"])


def prepare_signs(degree, boundary_map_dict):
    dim = degree + 1
    if dim == 0:
        return []

    if boundary_map_dict["type"] == "simplicial":
        ret = [1] * (dim + 1)
        for i in range(1, dim + 1, 2):
            ret[i] = -1
        return ret

    if boundary_map_dict["type"] == "cubical":
        ret = [1] * (dim * 2)
        for i in range(1, dim * 2, 4):
            ret[i] = -1
        for i in range(2, dim * 2, 4):
            ret[i] = -1
        return ret

    if boundary_map_dict["type"] == "abstract":
        return []

    raise(RuntimeError("Unknown boundary_map type"))


class Result(object):
    def __init__(self, birth_time, death_time):
        self.birth_time = birth_time
        self.death_time = death_time
        self.optimal_volume = None
        self.children_volumes = None
        self.owned_volume = None
        self.tightened_volume = None
        self.tightened_subvolume = None

    def to_jsondict(self):
        dic = {"birth-time": self.birth_time, "death-time": self.death_time}
        if self.optimal_volume:
            dic.update(self.optimal_volume.to_jsondict())
        if self.children_volumes:
            dic["children"] = [child_volume.to_jsondict()
                               for child_volume in self.children_volumes]
        if self.owned_volume:
            dic["owned-volume"] = self.owned_volume.to_jsondict()
        if self.tightened_volume:
            dic["tightened-volume"] = self.tightened_volume.to_jsondict()
        if self.tightened_subvolume:
            dic["tightened-subvolume"] = self.tightened_subvolume.to_jsondict()

        return dic

    def draw(self, drawer, index, show_optimal_volume):
        if self.optimal_volume and show_optimal_volume:
            self.optimal_volume.draw(drawer, index)
        if self.children_volumes:
            for child_volume in self.children_volumes:
                child_volume.draw(drawer, index)
        if self.owned_volume:
            self.owned_volume.draw(drawer, index)
        if self.tightened_volume:
            self.tightened_volume.draw(drawer, index)
        if self.tightened_subvolume:
            self.tightened_subvolume.draw(drawer, index)


class Volume(object):
    def __init__(self, volume_cells, birth_index, death_index, diagram):
        self.volume_cells = volume_cells
        self.birth = birth_index
        self.death = death_index
        self.geom_resolver = diagram.geometry_resolver()
        self.diagram = diagram
        self.index_map = diagram.index_map
        self.child_index = 0
        self.children_pairs = list(self.compute_children_pairs())

    def draw(self, drawer, index):
        if self.child_index == 0:
            volume_color = drawer.various_colors[0]
            boundary_color = drawer.various_colors[1]
        else:
            volume_color = drawer.various_colors[2]
            boundary_color = drawer.various_colors[3]

        self.draw_volume_cells(drawer, volume_color, index)
        self.draw_boundary(drawer, boundary_color, index)
        self.draw_death_cell(drawer, index)

    def draw_volume_cells(self, drawer, color, index):
        self.geom_resolver.draw_cells(
            drawer, self.volume_cells, color,
            children_index=self.child_index,
            issimplex=1, index=index, lifetime=self.lifetime(),
            **self.threshold_values()
        )

    def draw_boundary(self, drawer, color, index):
        self.geom_resolver.draw_cells(
            drawer, self.geom_resolver.boundary(self.volume_cells),
            color, children_index=self.child_index,
            isboundary=1, index=index, lifetime=self.lifetime(),
            **self.threshold_values()
        )

    def draw_death_cell(self, drawer, index):
        self.geom_resolver.draw_cell(
            drawer, self.death, drawer.death_color(),
            children_index=self.child_index,
            isdeath=1, index=index, lifetime=self.lifetime(),
            **self.threshold_values()
        )

    def compute_children_pairs(self):
        for cell in self.volume_cells:
            if self.death == cell:
                continue
            birth_of_cell = self.find_birth_of(cell)
            if birth_of_cell is None:
                continue
            birth_time_of_cell = self.resolve_time(birth_of_cell)
            death_time_of_cell = self.resolve_time(cell)
            if birth_time_of_cell == death_time_of_cell:
                continue
            yield((birth_of_cell, cell))

    def find_birth_of(self, volume_cell):
        where = np.argwhere(self.diagram.death_indices == volume_cell)
        if where.size == 0:
            return None
        else:
            return self.diagram.birth_indices[where[0, 0]]

    def to_jsondict(self):
        if self.diagram.index_map.type() == MapType.alpha:
            return self.to_jsondict_for_alpha()
        if self.diagram.index_map.type() == MapType.cubical:
            return self.to_jsondict_for_cubical()

    def to_jsondict_for_alpha(self):
        return {
            "birth-time": self.birth_time(),
            "death-time": self.death_time(),
            "birth-position": self.birth_position(),
            "death-position": self.death_position(),
            "points": self.points(),
            "simplices": self.volume_simplices(),
            "boundary": self.boundary(),
            "boundary-points": self.boundary_points(),
            "points-symbols": self.points_symbols(),
            "simplices-symbols": self.volume_simplices_symbols(),
            "boundary-symbols": self.boundary_symbols(),
            "boundary-points-symbols": self.boundary_points_symbols(),
            "children": self.children(),
        }

    def to_jsondict_for_cubical(self):
        return {
            "birth-time": self.birth_time(),
            "death-time": self.death_time(),
            "points": self.points(),
            "cubes": self.volume_cubes(),
            "boundary": self.boundary(),
            "boundary-points": self.boundary_points(),
            "children": self.children(),
        }

    def birth_time(self):
        return self.resolve_time(self.birth)

    def death_time(self):
        return self.resolve_time(self.death)

    def resolve_time(self, idx):
        return self.index_map.resolve_level(idx)

    def lifetime(self):
        return self.death_time() - self.birth_time()

    def points(self):
        return deep_tolist(
            self.geom_resolver.unique_vertices_coords(self.volume_cells)
        )

    def points_symbols(self):
        return self.geom_resolver.unique_vertices_symbols(self.volume_cells)

    def volume_simplices(self):
        return deep_tolist(
            self.geom_resolver.cells_coords(self.volume_cells)
        )

    def volume_simplices_symbols(self):
        return self.geom_resolver.cells_symbols(self.volume_cells)

    def volume_cubes(self):
        return self.geom_resolver.cells_coords(self.volume_cells)

    def boundary(self):
        return deep_tolist(
            self.geom_resolver.boundary_coords(self.volume_cells)
        )

    def boundary_symbols(self):
        return self.geom_resolver.boundary_symbols(self.volume_cells)

    def boundary_points(self):
        return deep_tolist(
            self.geom_resolver.boundary_vertices_coords(self.volume_cells)
        )

    def boundary_points_symbols(self):
        return self.geom_resolver.boundary_vertices_symbols(self.volume_cells)

    def children(self):
        return [
            {
                "birth-time": self.resolve_time(birth),
                "death-time": self.resolve_time(death)
            } for (birth, death) in self.children_pairs
        ]

    def birth_position(self):
        return deep_tolist(self.geom_resolver.cell_coords(self.birth))

    def death_position(self):
        return deep_tolist(self.geom_resolver.cell_coords(self.death))


class OptimalVolume(Volume):
    def threshold_values(self):
        return {"isoptimalvolume": 1}

    def draw(self, drawer, index):
        super().draw(drawer, index)
        self.draw_birth_cell(drawer, index)

    def draw_birth_cell(self, drawer, index):
        self.geom_resolver.draw_cell(
            drawer, self.birth, drawer.birth_color(),
            children_index=self.child_index,
            isbirth=1, index=index, lifetime=self.lifetime(),
            **self.threshold_values()
        )


class EigenVolume(Volume):
    def __init__(self, volume_cells, birth, death, threshold, diagram):
        super().__init__(volume_cells, birth, death, diagram)
        self.threshold = threshold

    def to_jsondict(self):
        dic = super().to_jsondict()
        dic["threshold"] = self.threshold
        dic["type"] = self.eigenvolume_type()
        return dic


class TightenedVolume(EigenVolume):
    def eigenvolume_type(self):
        return "tightened-volume"

    def threshold_values(self):
        return {"istightenedvolume": 1}


class TightenedSubvolume(EigenVolume):
    def eigenvolume_type(self):
        return "tightened-subvolume"

    def threshold_values(self):
        return {"istightenedsubvolume": 1}


class OwnedVolume(EigenVolume):
    def eigenvolume_type(self):
        return "owned-volume"

    def threshold_values(self):
        return {"isownedvolume": 1}


class OwnedVolumeSolver(object):
    def __init__(self, optimal_volume, children, lifetime_threshold, connected):
        self.optimal_volume = optimal_volume
        self.children = children
        self.threshold = lifetime_threshold
        self.diagram = optimal_volume.diagram
        self.connected = connected

    def solve(self):
        cells = set(self.optimal_volume.volume_cells)
        for child in self.children:
            if self.is_removed_volume(child):
                cells.difference_update(child.volume_cells)

        if not self.connected:
            return list(cells)

        death_index = self.optimal_volume.death
        if death_index not in cells:
            return []
        graph = self.build_graph(cells)
        return list(self.connected_component_in(graph, death_index))

    def is_removed_volume(self, child_volume):
        return (
            child_volume.birth_time() - self.optimal_volume.birth_time() <
            self.threshold
        )

    def build_graph(self, cells):
        transposed_map = self.build_transposed_map(cells)
        graph = defaultdict(list)
        for cell in cells:
            for boundary in self.diagram.cell_boundary(cell):
                for other_cell in transposed_map[boundary]:
                    if cell == other_cell:
                        continue
                    if other_cell not in cells:
                        continue
                    graph[cell].append(other_cell)
        return graph

    def build_transposed_map(self, cells):
        transposed_map = defaultdict(list)
        for cell in cells:
            for boundary in self.diagram.cell_boundary(cell):
                transposed_map[boundary].append(cell)
        return transposed_map

    def connected_component_in(self, graph, start):
        visited = set()
        stack = [start]
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            stack.extend(graph[current])
        return visited


def prepare_drawer_for_paraview(diagram):
    columns_spec = {
        "isboundary": 0, "issimplex": 0, "isbirth": 0, "isdeath": 0,
        "isvertex": 0, "isoptimalvolume": 0,
        "istightenedvolume": 0, "istightenedsubvolume": 0, "isownedvolume": 0,
        "children_index": None, "index": None, "lifetime": None,
    }

    if diagram.index_map.type() == MapType.alpha:
        return ParaViewSimplexDrawer(4, diagram.index_map.points, columns_spec)
    elif diagram.index_map.type() == MapType.cubical:
        return ParaViewCubeDrawer(4, diagram.index_map.shape, columns_spec)
    else:
        raise(RuntimeError("Index map type: {} is not available".format(
            diagram.index_map.type
        )))


def draw_all_vertices(drawer):
    drawer.draw_all_vertices(
        drawer.death_color(), children_index=0, index=-1, lifetime=-1,
        isvertex=1,
    )


def check_args(args):
    assert args.degree >= 0
    if args.constrain_on_birth_simplex:
        print("constrain-on-birth-simplex is now not supported",
              file=sys.stderr)


class OptimalVolumeError(Exception):
    """Base class for expretions in homcloud.optimal_volume"""

    def __init__(self, message, code):
        self.message = message
        self.code = code


class InfeasibleError(OptimalVolumeError):
    """Exception raised for errors for LpstatusInfeasible."""

    def __init__(self, message, code):
        super().__init__(message, code)


class RadiusSmallError(OptimalVolumeError):
    """Exception raised for errors in the cutoff-radius."""

    def __init__(self, message, code):
        super().__init__(message, code)


if __name__ == "__main__":
    main()
