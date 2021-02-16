#
#    (C) Quantum Computing Inc., 2020.
#
#    THIS IS UNPUBLISHED PROPRIETARY SOURCE CODE of the Copyright Holder. 
#    The contents of this file may not be disclosed to third parties, copied 
#    or duplicated in any form, in whole or in part, without the prior written
#    permission of the Copyright Holder.
#
import os
import dateutil as du
import re
import requests
from typing import Union, List, AnyStr
from itertools import chain
import networkx as nx
import numpy as np
import scipy.sparse as sp
from scipy.optimize import show_options
import pandas as pd

from .data_processing import Status, StatusCodes, AwsDeviceClient


def map_nodes(qubo: dict) -> dict:
    """
    Maps unique tuples of length k representing nodes in a graph to integers.

    Args:
        qubo: QUBO in dictionary form with tuples as keys

    Returns:
        dict[tuple, int], mapping from key to unique integer
    """
    nodes = sorted(set(chain(*qubo.keys())))
    return {u: i for i, u in enumerate(nodes)}


def construct_qubo_int_keys(qubo: dict):
    """
    Construct a mapping from keys of a QUBO to integer keys. Currently, options are tuple or string source keys.

    Args:
        qubo: dict, QUBO in sparse dict form.

    Returns:
        dict of QUBO with integer nodes/keys, with associated mapping from original nodes to integer nodes
    """
    node_map = map_nodes(qubo)
    Qint = {}
    for (u, v), val in qubo.items():
        Qint[node_map[u], node_map[v]] = val
    return {'qubo': Qint, 'node_map': _invert_mapping(node_map)}


def _invert_mapping(mapping: dict) -> dict:
    return {v:k for k,v in mapping.items()}


def map_solutions(solns, mapping):
    return [map_solution(soln, mapping) for soln in solns]


def map_solution(soln, mapping):
    """
    Invert a dictionary `mapping`.

    Args:
        soln: dict[int, val], logical variable or graph node and sampled value (float). Assumed that
            keys are ints due to limitation of csample.
        mapping: dict[int, (any hashable)], mapping ints to non-integer variable indices.

        The `mapping` must have the same values as the keys in `soln`, so that when `mapping`
        is inverted the lookup is well-defined for 'inverted mapping'.

    Returns:
        dict[mapping[int], val]
    """
    return {mapping[i]: val for i, val in soln.items()}


def check_int_nodes(qubo: dict) -> bool:
    idx = set(chain(*qubo.keys()))
    return all(map(lambda m: isinstance(m, int), idx))


def is_upper_tri(qubo: dict) -> bool:
    idx = sorted(set(qubo.keys()))
    return all(map(lambda m: m[0] <= m[1], idx))


def convert_dict_to_sparse_qubo(qubo: dict) -> sp.spmatrix:
    """
    Convert dictionary to sparse matrix format.

    :param qubo: dict, QUBO

    :return: COO matrix
    """
    upper_tri = False
    # we need to divide the influence of each off-diagnonal term.
    if is_upper_tri(qubo):
        upper_tri = True
        get_val = lambda row, col, v: v if row == col else v / 2.
    else:
        get_val = lambda row, col, v: v

    n = max(set(chain(*qubo.keys())))
    mat = sp.dok_matrix((n + 1, n + 1), dtype=np.float)
    for i, j in qubo.keys():
        if not upper_tri:
            assert qubo[i,j] == qubo[j,i]
        mat[i, j] = mat[j, i] = get_val(i, j, qubo[i, j])
    return mat.tocoo()


def check_qubo_dict(qubo: dict):
    # check keys are in [0, 1, ..., n-1]
    assert check_int_nodes(qubo), "QUBO keys must be integers in [0, 1, ..., n-1]."


def check_qubo(qubo: Union[np.ndarray, sp.spmatrix], size_limit=50000):
    assert (isinstance(qubo, np.ndarray) or isinstance(qubo, sp.spmatrix)), \
        "QUBO must be of type ndarray or sparse matrix."
    assert qubo.ndim == 2, "QUBO or Objective must be a 2-dimensional array."
    # check QUBO problems in array form are symmetric and square
    assert qubo.shape[0] == qubo.shape[1], "Input QUBO or Objective must be square. QUBO.shape = {}".format(qubo.shape)
    # check QUBO size is less than or equal to 10k (Qatalyst 2.0)
    assert qubo.shape[0] <= size_limit, "QUBO must be less than or equal to {} x {}. The input QUBO is QUBO.shape = {}".format(size_limit, size_limit, qubo.shape)
    # these only get called if qubo is square
    if isinstance(qubo, np.ndarray):
        assert check_symmetric_ndarray(qubo), "QUBO or Objective is not symmetric."
    else:
        assert check_symmetric_sparse(qubo), "QUBO or Objective is not symmetric."


def check_constraints(objective: Union[np.ndarray, sp.spmatrix], constraints: Union[np.ndarray, sp.spmatrix]):
    # Make sure the data type is correct
    assert (isinstance(constraints, np.ndarray) or isinstance(constraints, sp.spmatrix)), \
        "Constraint matrix must be of type ndarray or sparse matrix."
    # Now make sure both objective and constraint are the instance type. This check should suffice.
    assert isinstance(objective, constraints.__class__)
    assert constraints.shape[constraints.ndim-1] == objective.shape[0] + 1, \
        "Column dimension of constraint matrix must equal objective.shape[1] + 1. " \
        "Input: constraint.shape = {}, objective.shape = {}".format(constraints.shape, objective.shape)


def check_symmetric_ndarray(a, rtol=1e-06, atol=1e-09):
    """
    See:
    https://stackoverflow.com/questions/48798893/error-in-checking-symmetric-sparse-matrix
    """
    return np.allclose(a, a.T, rtol=rtol, atol=atol)


def check_symmetric_sparse(a, tol=1e-10):
    """
    See the most excellent post here:
    https://stackoverflow.com/questions/48798893/error-in-checking-symmetric-sparse-matrix
    """
    return (abs(a - a.T) > tol).nnz == 0


def loadQuboFile(filename) -> dict:
    qubo = {}
    with open(filename, 'r') as handle:
        for line in handle.readlines():
            line = line.strip()
            if len(line) == 0 or line[0] == 'c':
                continue
            if line[0] == 'p':
                _, _, _, n_variables, _, _ = line.split()
                qubo = {(a, a): 0 for a in range(int(n_variables))}
                continue
            # TODO: we should check that 'p' line has been found first
            a, b, bias = line.split()
            qubo[int(a), int(b)] = qubo.get((int(a), int(b)), 0) + float(bias)
    return qubo


def sampler_type_is_qpu(sampler_name, samplers=None):
    if samplers is None:
        samplers = load_available_samplers()
    return sampler_name in set(samplers[samplers['quantum']]['target_name'])


def load_available_samplers():
    fname = 'available_samplers.csv'
    path = os.sep.join([*os.path.expanduser(__file__).split(os.sep)[:-1], fname])
    df = pd.read_csv(path, dtype={'max_size': int})
    return df


def print_available_samplers():
    samplers = load_available_samplers()
    cols = samplers.columns.to_list()
    print(f"{cols[0]:<18}{'  ':^5}" + "|".join([f'{col:^15}' for col in cols[1:]]))
    print()
    for _, row in samplers.iterrows():
        print(f"{row['target_name']:<18}{'->':^5}" + "|".join([f'{col:^15}' for col in row.iloc[1:]]))
    print("\nSelect 'target_name' to run a problem on a particular sampler. Size limitations apply. "
          "See Qatalyst documentation for further details.")


def get_scipy_minimize_methods():
    """
    We want to match elements '===' right after the methods in the string returned
    by show_options.
    """
    REGEX = r'[=]+$'
    opts = show_options('minimize', disp=False)
    opts = [x for x in opts.split('\n') if len(x) > 0]
    return [opts[i-1] for i, m in enumerate(opts) if re.match(REGEX, m)]


def check_dwave_size(qubo: Union[nx.Graph, np.ndarray, sp.spmatrix],
                     device: AwsDeviceClient) -> bool:
    """
    qubo: Union[nx.Graph, np.ndarray, sp.spmatrix]

    :return: bool
    """
    DWAVE_MAX_CLIQUES = {'DW_2000Q_': 64, 'Advantage_system1': 120}
    for k in DWAVE_MAX_CLIQUES:
        if k in device.name:
            max_fully_connected = DWAVE_MAX_CLIQUES[k]
            break

    if isinstance(qubo, nx.Graph):
        arr = nx.to_numpy_array(qubo)
    else:
        arr = qubo.copy()
    if isinstance(arr, sp.spmatrix):
        arr = arr.toarray()
    d_idx = np.diag_indices_from(arr)
    arr[d_idx] = 0
    size = arr.shape[0]

    #######
    # after replacing diag with 0, all nonzeros should be off the diagonal
    #
    nnz_offdiag = np.count_nonzero(arr)
    max_offdiag_nnz = arr.shape[0]**2 - arr.shape[0]
    if nnz_offdiag - max_offdiag_nnz == 0 and size > max_fully_connected:
        raise ValueError(f"The D-Wave Systems QPU can only run fully connected problems "
                         f"with less then or equal to {max_fully_connected} logical qubits. Problem size is "
                         f"{size} qubits.")
    return True


def mincheck(t, v) -> bool:
    """
    Make sure val > threshold
    """
    return v > t


def algocheck(options: List[AnyStr], algo: str) -> bool:
    return algo.lower() in options


def optimizer_check(optimizers: List[AnyStr], opt: str) -> bool:
    return opt.lower() in optimizers


def optimizer_options_check(param: Union[str, bool, int, float], opts: dict):
    OPTIONS = {'maxiter': param}
    for opt, val in opts.items():
        if opt in OPTIONS:
            thresh = OPTIONS[opt]
            return mincheck(thresh, val)


def parse_status(resp: requests.Response) -> Status:
    """
    Args:
        resp: requests Response

    Return:

    """
    codes = StatusCodes
    res = resp.json()
    status = res['Status']
    message = res.get('Message')
    ts = res.get('TimeStamp')
    ts = du.parser.parse(ts).astimezone()

    if isinstance(message, str) and ('error' in message.lower() or 'exception' in message.lower()):
        return Status(status=codes.error, timestamp=ts, message=message)
    elif status == 'COMPLETE':
        return Status(status=codes.complete, timestamp=ts)
    elif 'ERROR' in status or 'EXCEPTION' in status:
        return Status(status=codes.error, timestamp=ts, message=message)
    else:
        # Strip internal service name from message
        if message is None and '`QUOIR`-' in status:
            processor = status.lstrip('QUOIR-')
            # means we just made it to the consumer and we might be looking for an embedding or something
            if 'producer' in status:
                user_message = f'Sent problem to {processor} preprocessing. Waiting for response...'
            else:
                user_message = f'Sent problem to {processor} processor/QPU. Waiting for response...'
        else:
            user_message = message
        return Status(status=codes.processing, message=user_message, timestamp=ts)


def param_check(params: dict, quantum: bool = False):
    """
    We check the basic parameters here, outside of sampler, which has been checked and set elsewhere.
    """
    checks = {'num_solutions': (mincheck, 0)}

    if quantum:
        checks.update({'num_shots': (mincheck, 0),
                       'num_reads': (mincheck, 0),
                       'depth': (mincheck, 1),
                       'algorithm': (algocheck, ['vqe', 'qaoa']),
                       'optimizer': (optimizer_check, get_scipy_minimize_methods()),
                       'optimizer_options': (optimizer_options_check, 0)}) # only set up for 'maxiter' > 0 check

    # loop through params
    for pname, val in params.items():
        # get the function from above for a given parameter, else None
        func_param = checks.get(pname)
        if func_param is None:
            continue
        else:
            f, param = func_param
        # is the provided value within the range required
        if not f(param, val):
            if isinstance(param, int):
                raise ValueError(f"Parameter '{pname}'={val}, must be greater than {param}.")
            elif isinstance(param, dict):
                raise ValueError(f"Parameter '{pname}'={val}, must be greater than {param}.")
            else:
                raise ValueError(f"Parameter '{pname}={val}', must be one of {param}")
    else:
        return True


def is_braket_qpu_execution_limited(device: AwsDeviceClient):
    """
    Args:

    """
    hours_up = device.execution_window['hours_up_per_day']
    days_up = device.execution_window['days']
    if days_up == 'Everyday' and hours_up == 24:
        return False
    else:
        return True


def get_braket_qpu_execution_message(device: AwsDeviceClient):
    return f"{device.execution_window['message']} Executing outside of this time window could incur significant " \
           f"delays.\nContinue? Proceed (y) or abort (n)?\n* To disable this warning set kwarg ignore_qpu_window=True or set QATALYST_IGNORE_QPU_WINDOW=1 in your environment. *\n"
