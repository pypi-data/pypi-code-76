# Copyright 2019-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

import itertools
from collections import OrderedDict
from functools import lru_cache
from typing import Dict, Iterable, List, Tuple, Any, Optional

import numpy as np  # type: ignore
from pytket.circuit import Circuit, OpType, Qubit, Bit, Node, CircBox  # type: ignore
from pytket.passes import DecomposeBoxes, FlattenRegisters  # type: ignore
from pytket.backends import Backend
from pytket.utils.results import BitPermuter, CountsDict, StateTuple

MeasurementMap = Dict[Qubit, Bit]
ResultsMap = Dict[Node, int]


def compress_counts(
    counts: Dict[StateTuple, float], tol: float = 1e-6, round_to_int: bool = False
) -> CountsDict:
    """Filter counts to remove states that have a count value (which can be a floating-
    point number) below a tolerance, and optionally round to an integer.

    :param counts: Input counts
    :type counts: Dict[StateTuple, float]
    :param tol: Value below which counts are pruned. Defaults to 1e-6.
    :type tol: float, optional
    :param round_to_int: Whether to round each count to an integer. Defaults to False.
    :type round_to_int: bool, optional
    :return: Filtered counts
    :rtype: CountsDict
    """
    valprocess = (lambda x: int(round(x))) if round_to_int else (lambda x: x)  # type: ignore
    processed_pairs = (
        (key, valprocess(val)) for key, val in counts.items() if val > tol  # type: ignore
    )
    return {key: val for key, val in processed_pairs if val > 0}


@lru_cache(maxsize=128)
def binary_to_int(bintuple: Tuple[int]) -> int:
    """Convert a binary tuple to corresponding integer, with most significant bit as the
    first element of tuple.

    :param bintuple: Binary tuple
    :type bintuple: Tuple[int]
    :return: Integer
    :rtype: int
    """
    integer = 0
    for index, bitset in enumerate(reversed(bintuple)):
        if bitset:
            integer |= 1 << index
    return integer


@lru_cache(maxsize=128)
def int_to_binary(val: int, dim: int) -> Tuple[int, ...]:
    """Convert an integer to corresponding binary tuple, with most significant bit as
    the first element of tuple.

    :param val: input integer
    :type val: int
    :param dim: Bit width
    :type dim: int
    :return: Binary tuple of width dim
    :rtype: Tuple[int]
    """
    return tuple(map(int, format(val, "0{}b".format(dim))))


def _get_measure_map(circ: Circuit) -> MeasurementMap:
    return {com.args[0]: com.args[1] for com in circ if com.op.type == OpType.Measure}


#########################################
### _compute_dot and helper functions ###
###
### With thanks to
### https://math.stackexchange.com/a/3423910
### and especially
### https://gist.github.com/ahwillia/f65bc70cb30206d4eadec857b98c4065
### on which this code is based.


def _unfold(tens: np.ndarray, mode: int, dims: List[int]) -> np.ndarray:
    """
    Unfolds tensor into matrix.
    Parameters
    ----------
    tens : tensor with shape == dims
    mode : which axis to move to the front
    dims : tensor shape
    Returns
    -------
    matrix : shape (dims[mode], prod(dims[/mode]))
    """
    if mode == 0:
        return tens.reshape(dims[0], -1)
    else:
        return np.moveaxis(tens, mode, 0).reshape(dims[mode], -1)


def _refold(vec: np.ndarray, mode: int, dims: List[int]) -> np.ndarray:
    """
    Refolds vector into tensor.
    Parameters
    ----------
    vec : tensor with len == prod(dims)
    mode : which axis was unfolded along.
    dims : tensor shape
    Returns
    -------
    tens : tensor with shape == dims
    """
    if mode == 0:
        return vec.reshape(dims)
    else:
        # Reshape and then move dims[mode] back to its
        # appropriate spot (undoing the `unfold` operation).
        tens = vec.reshape([dims[mode]] + [d for m, d in enumerate(dims) if m != mode])
        return np.moveaxis(tens, 0, mode)


def _compute_dot(submatrices: Iterable[np.ndarray], vector: np.ndarray) -> np.ndarray:
    # Multiply the Kronecker product of the matrices with the vector.
    dims = [A.shape[0] for A in submatrices]
    vt = vector.reshape(dims)
    for i, A in enumerate(submatrices):
        vt = _refold(A @ _unfold(vt, i, dims), i, dims)
    return vt.ravel()


##########################################


def _invert_correct(
    submatrices: Iterable[np.ndarray], input_vector: np.ndarray
) -> np.ndarray:
    try:
        subinverts = [np.linalg.inv(submatrix) for submatrix in submatrices]
    except np.linalg.LinAlgError:
        raise ValueError(
            "Unable to invert calibration matrix: please re-run "
            "calibration experiments or use an alternative correction method."
        )

    v = _compute_dot(subinverts, input_vector)
    # The entries of v will always sum to 1, but they may not all be in the range [0,1].
    # In order to make them genuine probabilities (and thus generate meaningful counts),
    # we adjust them by setting all negative values to 0 and scaling the remainder.
    v[v < 0] = 0
    v /= sum(v)
    return v


def _bayesian_iteration(
    submatrices: Iterable[np.ndarray],
    measurements: np.ndarray,
    t: np.ndarray,
    epsilon: float,
) -> np.ndarray:
    # Transform t according to the Bayesian iteration
    # The parameter epsilon is a stabilization parameter which defines an affine
    # transformation to apply to the submatrices to eliminate zero probabilities. This
    # transformation preserves the property that all columns sum to 1
    if epsilon == 0:
        # avoid copying if we don't need to
        As = submatrices
    else:
        As = [
            epsilon / submatrix.shape[0] + (1 - epsilon) * submatrix
            for submatrix in submatrices
        ]
    z = _compute_dot(As, t)
    if np.isclose(z, 0).any():
        raise ZeroDivisionError
    return t * _compute_dot([A.transpose() for A in As], measurements / z)


def _bayesian_iterative_correct(
    submatrices: Iterable[np.ndarray],
    measurements: np.ndarray,
    tol: float = 1e-5,
    max_it: Optional[int] = None,
) -> np.ndarray:
    # based on method found in https://arxiv.org/abs/1910.00129

    vector_size = measurements.size
    # uniform initial
    true_states = np.full(vector_size, 1 / vector_size)
    prev_true = true_states.copy()
    converged = False
    count = 0
    epsilon: float = 0  # stabilization parameter, adjusted dynamically
    while not converged:
        if max_it:
            if count >= max_it:
                break
            count += 1
        try:
            true_states = _bayesian_iteration(
                submatrices, measurements, true_states, epsilon
            )
            converged = np.allclose(true_states, prev_true, atol=tol)
            prev_true = true_states.copy()
        except ZeroDivisionError:
            # Shift the stabilization parameter up a bit (always < 0.5).
            epsilon = 0.99 * epsilon + 0.01 * 0.5

    return true_states


class SpamCorrecter:
    """A class for generating "state preparation and measurement" (SPAM) calibration
    experiments for ``pytket`` backends, and correcting counts generated from them.

    Supports saving calibrated state to a dictionary format, and restoring from the
    dictionary.

    """

    def __init__(
        self, qubit_subsets: List[List[Node]], backend: Optional[Backend] = None
    ):
        """Construct a new `SpamCorrecter`.

        :param qubit_subsets: A list of lists of correlated Nodes of a `Device`.
            Qubits within the same list are assumed to only have SPAM errors correlated
            with each other. Thus to allow SPAM errors between all qubits you should
            provide a single list.
        :type qubit_subsets: List[List[Node]]
        :param backend: Backend on which the experiments are intended to be run
            (optional). If provided, the qubits in `qubit_subsets` must be nodes in the
            backend's associated `Device`. If not provided, it is assumed that the
            experiment will be run on a `Device` with the nodes in `qubit_subsets`, and
            furthermore that the intended device natively supports X gates.
        :raises ValueError: There are repeats in the `qubit_subsets` specification.
        """
        self.all_qbs = [qb for subset in qubit_subsets for qb in subset]

        if len(self.all_qbs) != len(set(self.all_qbs)):
            raise ValueError("Qubit subsets are not mutually disjoint.")

        xcirc = Circuit(1).X(0)
        if backend is not None:
            if backend.device is None:
                raise ValueError("No device associated with backend.")
            nodes = backend.device.nodes
            if not all(node in nodes for node in self.all_qbs):
                raise ValueError("Nodes do not all belong to device.")
            backend.compile_circuit(xcirc)
            FlattenRegisters().apply(xcirc)
        self.xbox = CircBox(xcirc)

        self.subsets_matrix_map = OrderedDict.fromkeys(
            sorted(map(tuple, qubit_subsets), key=len, reverse=True)
        )
        self._subset_dimensions = [len(subset) for subset in self.subsets_matrix_map]
        # create base circuit with
        self._base_circuit = Circuit()
        self.c_reg = []
        for index, qb in enumerate(self.all_qbs):
            self._base_circuit.add_qubit(qb)
            c_bit = Bit(index)
            self.c_reg.append(c_bit)
            self._base_circuit.add_bit(c_bit)

        self._prepared_states: List[Any] = []
        self.normalised_mats: List[Any] = []

    def calibration_circuits(self) -> List[Circuit]:
        """Generate calibration circuits according to the specified correlations.

        :return: A list of calibration circuits to be run on the machine. The circuits
            should be processed without compilation. Results from these circuits must be
            given back to this class (via the `calculate_matrices` method) in the same
            order.
        :rtype: List[Circuit]
        """
        major_state_dimensions = self._subset_dimensions[0]
        n_circuits = 1 << major_state_dimensions
        circuits = []
        self._prepared_states = []
        for major_state_index in range(n_circuits):
            circ = self._base_circuit.copy()
            # get bit string corresponding to basis state of biggest subset of qubits
            major_state = int_to_binary(major_state_index, major_state_dimensions)
            new_state_dicts = {}
            for dim, qubits in zip(self._subset_dimensions, self.subsets_matrix_map):
                new_state_dicts[qubits] = major_state[:dim]
                for flipped_qb in itertools.compress(qubits, major_state[:dim]):
                    circ.add_circbox(self.xbox, [flipped_qb])
            DecomposeBoxes().apply(circ)
            circ.add_barrier(self.all_qbs)
            for qb, cb in zip(self.all_qbs, self.c_reg):
                circ.Measure(qb, cb)
            circuits.append(circ)

            self._prepared_states.append(new_state_dicts)

        return circuits

    def calculate_matrices(self, counts_list: List[CountsDict]) -> None:
        """Calculate the calibration matrices from the results of running calibration
        circuits.

        :param counts_list: List of result counts. Must be in the same order as the
            corresponding circuits generated by `calibration_circuits`.
        :type counts_list: List[CountsDict]
        :raises RuntimeError: Calibration circuits have not been generated yet.
        """
        if not self._prepared_states:
            raise RuntimeError(
                "Ensure calibration states/circuits have been calculated first."
            )
        # Using sparse matrices and vectors could speed things up in principle, but
        # this seems difficult to achieve in practice because it slows down either the
        # index rebasing (if using csr_matrix) or the matrix-vector multiplication (if
        # using lil_matrix). Could be worth investigating further.
        for qbs, dim in zip(self.subsets_matrix_map, self._subset_dimensions):
            self.subsets_matrix_map[qbs] = np.zeros((1 << dim,) * 2, dtype=float)

        for counts_dict, state_dict in zip(counts_list, self._prepared_states):
            for measured_state, count in counts_dict.items():
                for qb_sub in self.subsets_matrix_map:
                    measured_subset_state = measured_state[: len(qb_sub)]
                    measured_state = measured_state[len(qb_sub) :]

                    prepared_state_index = binary_to_int(state_dict[qb_sub])
                    measured_state_index = binary_to_int(measured_subset_state)
                    self.subsets_matrix_map[qb_sub][
                        measured_state_index, prepared_state_index
                    ] += count

        self.normalised_mats = [
            mat / np.sum(mat, axis=0) for mat in self.subsets_matrix_map.values()
        ]

    def correct_counts(
        self,
        counts: CountsDict,
        res_map: ResultsMap,
        method: str = "bayesian",
        options: Optional[Dict] = None,
    ) -> CountsDict:
        """Correct results counts from calibrated backend according to calibration data,
        using the specified method.

        :param counts: Input counts
        :type counts: CountsDict
        :param res_map: Dictionary mapping each calibrated `Node` of the backend to the
            position in the `counts` state tuple corresponding to the result from that
            qubit.
        :type res_map: ResultsMap
        :param method: Method to use for calculating the corrected counts.
            Options are:

            * "bayesian" (default): Use an iterative Bayesian technique to converge to
              the corrected counts.
            * "invert": Invert the calibration matrix exactly, remove any negative terms
              from the result and rescale.

            The "bayesian" method may be faster than inversion when there are large
            qubit sets in the partition; it is also less sensitive to statistical
            fluctuations in the data. For small qubit sets and a large number of shots
            in the calibration experiments, the "invert" method may give more accurate
            results.
        :type method: str, optional
        :param options: Options for the method. Possible options are:

            * "tol": Convergence tolerance (for "bayesian" method).
            * "maxiter": Number of iterations before terminating if convergence is not
              reached (for "bayesian" method).
        :type options: Dict, optional
        :raises RuntimeError: Calibration matrix has not been calculated, or results
            map does not provide a result position for all calibrated qubits.
        :raises ValueError: Invalid method string.
        :return: Corrected counts, possibly with floating-point count values.
        :rtype: CountsDict
        """
        if self.normalised_mats is None:
            raise RuntimeError("Calibration matrix is not yet defined")
        if len(res_map) != len(next(iter(counts))):
            raise RuntimeError(
                "Results map does not map all calibrated qubits. Make sure all qubits "
                "in calibration pattern have a valid measurement index in the map. "
                "This may be caused by not all qubits having a measure operation in "
                "the compiled circuit."
            )
        valid_methods = ("invert", "bayesian")
        permuter = BitPermuter(tuple(res_map[qb] for qb in self.all_qbs))
        big_dimension = len(self.all_qbs)
        vector_size = 1 << big_dimension
        in_vec = np.zeros(vector_size, dtype=float)
        for state, count in counts.items():
            in_vec[permuter.permute(binary_to_int(state), inverse=True)] = count

        Ncounts = np.sum(in_vec)
        in_vec_norm = in_vec / Ncounts
        if method == "invert":
            outvec = _invert_correct(self.normalised_mats, in_vec_norm)

        elif method == "bayesian":
            if options is None:
                options = {}
            tol_val = options.get("tol", 1 / Ncounts)
            maxit = options.get("maxiter", None)
            outvec = _bayesian_iterative_correct(
                self.normalised_mats, in_vec_norm, tol=tol_val, max_it=maxit
            )

        else:
            raise ValueError("Method must be one of: ", *valid_methods)

        outvec *= Ncounts
        return {
            int_to_binary(permuter.permute(index), big_dimension): Bcount
            for index, Bcount in enumerate(outvec)
        }

    def to_dict(self) -> Dict:
        """Get calibration information as a dictionary.

        :return: Dictionary output
        :rtype: Dict
        """
        prep_states = [
            [
                (tuple((uid.reg_name, uid.index) for uid in subs), state)
                for subs, state in d.items()
            ]
            for d in self._prepared_states
        ]
        subsets_matrices = [
            (tuple((uid.reg_name, uid.index) for uid in s), m.tolist())  # type: ignore
            for s, m in self.subsets_matrix_map.items()
        ]
        self_dict = {
            "subset_matrix_map": subsets_matrices,
            "_prepared_states": prep_states,
        }
        return self_dict

    @classmethod
    def from_dict(class_obj, d: Dict) -> "SpamCorrecter":
        """Build a `SpamCorrecter` instance from a dictionary in the format returned by
        `to_dict`.

        :return: Dictionary of calibration information.
        :rtype: SpamCorrecter
        """
        subsets, mats = zip(
            *(
                (tuple(Node(*pair) for pair in subset_tuple), np.array(matlist))
                for subset_tuple, matlist in d["subset_matrix_map"]
            )
        )
        new_inst = class_obj(list(subsets))
        for s, m in zip(subsets, mats):
            new_inst.subsets_matrix_map[s] = m
        new_inst._prepared_states = [
            {
                tuple(Qubit(*pair) for pair in qb_tuple): tuple(state)
                for qb_tuple, state in subst_list
            }
            for subst_list in d["_prepared_states"]
        ]
        new_inst.normalised_mats = [
            mat / np.sum(mat, axis=0) for mat in new_inst.subsets_matrix_map.values()
        ]

        return new_inst
