from typing import List, Tuple

import numpy as np
import pypoman
import pypoman.polyhedron
import cvxopt

from DPGM import Node
import DPGM as AF
from assignments import Assignment
import assignments as asg
from distribution import Distribution

Constraint = Tuple[np.array, float]


class LinearSolver:

    def __init__(self, af: AF):
        self.af = af
        self.all_nodes: List[Node] = sorted(list(af.get_nodes()))
        self.dimension = 2**len(self.all_nodes)

        self.prob_dist_constraints: List[Constraint] = self.generate_prob_dist_constraints()

    def generate_prob_dist_constraints(self):
        constraints = []
        # each entry in the solution vector needs to be larger than zero
        for i in range(self.dimension):
            row = [0] * self.dimension
            row[i] = -1
            constraints.append((row, 0))
        # overall sum equals one
        constraints.append(([1] * self.dimension, 1))
        constraints.append(([-1] * self.dimension, -1))
        return constraints

    def constraint_matrix(self, constraints: List[Constraint]):
        matrix_A_list = []
        vector_b_list = []
        for (row, value) in self.prob_dist_constraints + constraints:
            matrix_A_list.append(row)
            vector_b_list.append(value)

        A = np.array(matrix_A_list)
        b = np.array(vector_b_list)

        # print("\nSystem of linear inequalities:")
        # print("A: \n" + str(A))
        # print("b:", b)
        # print("Solving: A x <= b")

        return A, b

    def constraint_matrix2(self, constraints: List[Constraint]):
        # build matrix directly without using self.prob_dist_constraints
        A = - np.identity(self.dimension)
        b = np.zeros(self.dimension)

        a1 = np.ones(self.dimension)
        a2 = - a1

        print("num constraints:", len(constraints))
        a_list, b_list = list(zip(*constraints))

        A = np.concatenate((A, [a1, a2], a_list))
        b = np.concatenate((b, [1, -1], b_list))

        return A, b

    def any_solution(self, constraints: List[Constraint], solver="cvxopt"):
        if solver == "cvxopt":
            solver = None
        G, h = self.constraint_matrix(constraints)
        c = cvxopt.matrix([0] * self.dimension, tc="d")
        G = cvxopt.matrix(G, tc="d")
        h = cvxopt.matrix(h, tc="d")
        result = cvxopt.solvers.lp(c, G, h, solver=solver)
        status = result['status']
        if status == "optimal":
            x = result['x']
            # print("sum:", sum(x))
            return self.vector_to_distribution(x)
        else:
            # print("Status:", status)
            return None

    def chebyshev_center(self, constraints: List[Constraint]):
        A, b = self.constraint_matrix(constraints)
        b = cvxopt.matrix(b, tc="d")
        try:
            x = pypoman.polyhedron.compute_chebyshev_center(A, b)
        except Exception as ex:
            if str(ex).startswith("Polytope is empty"):  # thrown by pypoman library
                return None
            else:
                raise ex
        return self.vector_to_distribution(x)

    def corner_distributions(self, constraints: List[Constraint]) -> List[Distribution]:
        A, b = self.constraint_matrix(constraints)

        # print("\nSystem of linear inequalities:")
        # print("A: \n" + str(A))
        # print("b:", b)
        # print("Solving: A x <= b")

        # computes corners of solution space with A * x <= b
        vertices = pypoman.compute_polytope_vertices(A, b)

        # print("Simplified system:")
        # A, b = pypoman.compute_polytope_halfspaces(vertices)
        # print("A: \n" + str(A))
        # print("b:", b)
        #
        # # todo: own function for linear optimization
        # print("MaxAvgAdmDgr distribution:")
        # c = cvxopt.matrix(self.adm_degree(), tc="d")
        # if c:
        #     print("c:", c)
        #     x = pypoman.solve_lp(c, A, b)
        #     print("x:", x)
        #     self.vector_to_distribution(x).print_formatted("F")
        # else:
        #     print("no solution")

        # print("Vertices:", vertices)
        distributions = []
        for vector in vertices:
            distributions.append(self.vector_to_distribution(vector))
        return distributions

    def adm_degree(self):
        # todo: this does not completely follow the write-up as all nodes are considered, and not only those whose
        # marginal prob is positive. then again, this is probably not realizable as linear constraints
        rows = []
        for node in self.all_nodes:
            intersection_list = []
            for attacker in node.get_parents():
                union_set = set()
                for defender in attacker.get_parents():
                    if node != defender:
                        # noinspection PyTypeChecker
                        assignment: Assignment = ((node, True), (defender, True))
                    else:
                        assignment = ((node, True),)
                    defender_assignments = asg.sum_out(assignment, self.all_nodes)
                    union_set.update(defender_assignments)
                intersection_list.append(union_set)
            if intersection_list:
                assignments = list(set.intersection(*intersection_list))
                rows.append(self.assignments_to_row(assignments))
        return (1/len(self.all_nodes)) * sum(rows)

    def assignments_to_row(self, assignments: List[Assignment]):
        """
        [((A,False),(B,False)), ((A,True),(B,False))] -> (1 0 1 0)
        """
        row = np.array([0] * self.dimension)
        for assignment in assignments:
            row[asg.to_id(assignment)] = 1.0
        return row

    def constraints_assignments_less_or_equal_value(
            self, assignments: List[Assignment], value) -> List[Constraint]:
        """
        Generate constraints such that the sum of the given assignments is less or equal to the given value.
        """
        row = self.assignments_to_row(assignments)
        return [(row, value)]

    def constraints_assignments_greater_or_equal_value(
            self, assignments: List[Assignment], value) -> List[Constraint]:
        """
        Generate constraints such that the sum of the given assignments is greater or equal to the given value.
        """
        row = -1 * self.assignments_to_row(assignments)
        return [(row, -value)]

    def constraints_assignments_equal_value(
            self, assignments: List[Assignment], value) -> List[Constraint]:
        """
        Generate constraints such that the sum of the given assignments equals the given value.
        """
        return self.constraints_assignments_less_or_equal_value(assignments, value) + \
            self.constraints_assignments_greater_or_equal_value(assignments, value)

    def constraints_assignments_less_or_equal_assignments(
            self, assignments_a: List[Assignment], assignments_b: List[Assignment]) -> List[Constraint]:
        """
        Generate constraints such that the sum of the first assignments is less or equal to the sum of the second
        assignments.
        """
        row_a = self.assignments_to_row(assignments_a)
        row_b = self.assignments_to_row(assignments_b)
        return [(row_a - row_b, 0)]

    def constraints_assignments_greater_or_equal_assignments(
            self, assignments_a: List[Assignment], assignments_b: List[Assignment]) -> List[Constraint]:
        """
        Generate constraints such that the sum of the first assignments is greater or equal to the sum of the second
        assignments.
        """
        row_a = self.assignments_to_row(assignments_a)
        row_b = self.assignments_to_row(assignments_b)
        return [(row_b - row_a, 0)]

    def constraints_assignments_equal_assignments(
            self, assignments_a: List[Assignment], assignments_b: List[Assignment]) -> List[Constraint]:
        """
        Generate constraints such that the sum of the first assignments equals the sum of the second assignments.
        """
        return self.constraints_assignments_less_or_equal_assignments(assignments_a, assignments_b) + \
            self.constraints_assignments_greater_or_equal_assignments(assignments_a, assignments_b)

    def constraints_node_less_or_equal_value(self, node: Node, value) -> List[Constraint]:
        node_full_assignments = asg.get_node_assignments(node, self.all_nodes)
        return self.constraints_assignments_less_or_equal_value(node_full_assignments, value)

    def constraints_node_greater_or_equal_value(self, node: Node, value) -> List[Constraint]:
        node_full_assignments = asg.get_node_assignments(node, self.all_nodes)
        return self.constraints_assignments_greater_or_equal_value(node_full_assignments, value)

    def constraints_node_equals_value(self, node: Node, value) -> List[Constraint]:
        node_full_assignments = asg.get_node_assignments(node, self.all_nodes)
        return self.constraints_assignments_equal_value(node_full_assignments, value)

    def get_node_value(self, node: Node, distribution_vector):
        """
        Return the marginal probability of the given node under the distribution.
        """
        prob_sum = 0
        for a in asg.get_node_assignments(node, self.all_nodes):
            prob_sum += distribution_vector[asg.to_id(a)]
        return prob_sum

    def print_distribution(self, distribution_vector, only_positive=False):
        for i in range(self.dimension):
            value = distribution_vector[i]
            if only_positive and value == 0:
                continue
            asg.print_assignment_prob(asg.from_id(i, self.all_nodes), value)

    def vector_to_distribution(self, distribution_vector):
        distribution = dict()
        for i in range(self.dimension):
            value = distribution_vector[i]
            distribution[asg.from_id(i, self.all_nodes)] = value
        return Distribution(distribution, self.all_nodes)

    def print_formatted_distribution(self, distribution_vector: np.array, format_string: str = ""):
        """
        Print distribution given by the distribution vector in the formats given by the format string: (M) marginal node
        probabilities, (F) full distribution, (S) support of distribution, (Z) internal format, (T) SMT2 format.
        """
        for char in format_string:
            if char == "M":
                for node in self.all_nodes:
                    print(node.name, "=", self.get_node_value(node, distribution_vector))
            elif char == "F":
                self.print_distribution(distribution_vector)
            elif char == "S":
                print("Support:")
                self.print_distribution(distribution_vector, only_positive=True)
            elif char == "Z":
                print(distribution_vector)
            elif char == "T":
                print("SMT2 format not implemented for linear constraints!")
                print(distribution_vector)
            else:
                print("Unknown distribution format '" + char + "'.")
