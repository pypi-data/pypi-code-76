#
#    (C) Quantum Computing Inc., 2020.
#
#    THIS IS UNPUBLISHED PROPRIETARY SOURCE CODE of the Copyright Holder. 
#    The contents of this file may not be disclosed to third parties, copied 
#    or duplicated in any form, in whole or in part, without the prior written
#    permission of the Copyright Holder.
#
from os import getenv

from qatalyst.client import ClientService, get_client_kwargs
from qatalyst.result import Result
from qatalyst.utils import *

__all__ = ['sample_qubo', 'sample_constraint_problem', 'sample_lagrange_optimization']


class QatalystCore(ClientService):

    def __init__(self,
                 username: str = None,
                 password: str = None,
                 access_token: str = None,
                 sampler: str = 'csample',
                 configuration: str = 'default',
                 conf_path: str = None,
                 url: str = 'https://api.qci-prod.com',
                 ignore_qpu_window: bool = False,
                 **kwargs):
        """

        :param username: str
        :param password: str
        :param access_token: str
        :param configuration: str, configuration name, in case the config file contains multiples
        :param conf_path: str, optional path to local configuration file. By default, HttpClient will check in
               these locations: ('~/.qci.conf', '~/.qci/qci.conf').
        :param url: str, Portal-API server. Default = 'https://api.qci-prod.com'
        :param sampler: str, string representation of the ampler to invoke. Default = 'csample'.
        :param ignore_qpu_window: bool, disable user confirmation for situations in which QPUs are only available during limited hours.

        """
        super().__init__(username, password, access_token, sampler, configuration, conf_path, url, **kwargs)

        if not ignore_qpu_window:
                ignore_qpu_window = bool(getenv('QATALYST_IGNORE_QPU_WINDOW'))

        self.ignore_qpu_window = ignore_qpu_window

    def _qpu_execution_user_confirm(self):
        # Inform the user of possibly limited execution window
        if not self.ignore_qpu_window:
            if is_braket_qpu_execution_limited(self.device):
                message = get_braket_qpu_execution_message(self.device)
                self.confirm_qpu_execution(message)
        else:
            print("Ignoring QPU execution window.")
            return True

    def _check_qubo(self, qubo: Union[dict, np.ndarray, sp.spmatrix]) -> None:
        """
        Make sure that the QUBO is properly constructed. Check that it is square and symmetric.

        :param qubo: dict, np.ndarray or sp.spmatrix, User-input QUBO

        Raises AssertionError if QUBO is not square or symmetric

        :return: None
        """
        print(f"Checking validity of objective function... ")
        if isinstance(qubo, dict):
            # raises AssertionError if anything is amiss
            check_qubo_dict(qubo)
        else:
            # raises AssertionError if anything is amiss
            check_qubo(qubo)

    def _check_constraints(self, objective, constraints) -> None:
        """

        :param objective: np.ndarray or sp.spmatrix, User-input objective function
        :param constraints: np.ndarray or sp.spmatrix, User-input constraint matrix

        Raises AssertionError if Objective is not square or symmetric, or

        :return: None
        """
        self._check_qubo(objective)
        print(f"Checking validity of constraints...")
        check_constraints(objective, constraints)

    def set_quantum_params(self, params):
        # replace num_solutions by num_reads for D-Wave
        if 'dwave' in self.sampler:
            if 'num_reads' not in params:
                params['num_reads'] = params.get('num_solutions', self.DEFAULT_NUM_READS)
        elif 'rigetti' in self.sampler or 'ionq' in self.sampler or 'simulator' in self.sampler:
            if 'num_shots' not in params:
                params['num_shots'] = self.DEFAULT_NUM_SHOTS
            if 'circuit_depth' not in params:
                params['circuit_depth'] = self.DEFAULT_CIRCUIT_DEPTH
            if 'optimizer' not in params:
                params['optimizer'] = self.DEFAULT_OPTIMIZER

    def sample_qubo(self,
                    qubo: Union[dict, np.ndarray, sp.spmatrix],
                    **params) -> Result:
        """
        Given a Quadratic Unconstrained Binary Optimization model (QUBO), return samples of optimal or near optimal
        solutions.

        :param qubo: dict, np.ndarray, or sp.spmatrix, n x n QUBO matrix
        :param sampler: str

        :param params:
            Parameters and arguments for the sampler and solver algorithm. Different samplers permit different arguments.

        :return: Result
        """
        # make sure the input is correct before
        self._check_qubo(qubo)

        # Figure out if we are using a qpu and if the size is compatible with the
        # number of variables in the qubo.
        self._check_size(qubo)

        if self.is_quantum() or self.is_hybrid():
            self._qpu_execution_user_confirm()
            self.set_quantum_params(params)

        if isinstance(qubo, dict):
            qubo = convert_dict_to_sparse_qubo(qubo)
        metadata = self.process_metadata('qubo', qubo)
        params = self.process_params(params)
        # convert qubo to npz byte stream
        data_obj = self.process_data(qubo)

        message = {'data_obj': (self.DATA_OBJ_FNAME, data_obj, 'application/octet-stream'),
                   'metadata': (self.METADATA_FNAME, metadata, 'text/plain'),
                   'params': (self.PARAMS_NAME, params, 'text/plain')}

        res = self.sendRequest(message)
        return Result.from_dict_response(res)

    def sample_constraint_problem(self,
                                  objective: Union[np.ndarray, sp.spmatrix],
                                  constraints: Union[np.ndarray, sp.spmatrix],
                                  alpha: float = 1.0,
                                  **params) -> Result:
        """
        Given an objective function and linear constraint matrix, find optimal or near optimal solutions to the
        associated QUBO,

        :math:`Q = B + alpha * C.T * C,`

        where :math:`B` is the :math:`n x n` objective function matrix, and :math:`C` is the linear constraint matrix.
        The dimension of :math:`C` is :math:`m x n+1`, where the constraint vector is appended to the final column of
        :math:`C`.

        :param objective: np.ndarray or sp.spmatrix, n x n cost function matrix
        :param constraints: np.ndarray or sp.spmatrix, m x n or m x n+1 constraint functions matrix, where
            m is the number of constraints and n is the dimension of the solutions space.
        :param alpha: float, Lagrange multiplier to scale constraints when computing QUBO,
            Q = objective + alpha * constraints
            Default = 1.0
        :param params: Parameters for the provided sampler. For allowed arguments see documentation
            on in the sampler module.

        :return: Result
        """
        assert alpha > 0, "Lagrangian multiplier 'alpha' must be positive."
        self._check_size(objective)

        if self.is_quantum():
            self._qpu_execution_user_confirm()
            self.set_quantum_params(params)

        self._check_constraints(objective, constraints)
        params.update({'alpha': alpha})
        metadata = self.process_metadata('constraint_problem', constraints)
        params = self.process_params(params)
        # Process data arrays to byte streams
        data_obj = self.process_data(objective)
        data_con = self.process_data(constraints)
        message = {'data_obj': (self.DATA_OBJ_FNAME, data_obj, 'application/octet-stream'),
                   'data_con': (self.DATA_CON_FNAME, data_con, 'application/octet-stream'),
                   'metadata': (self.METADATA_FNAME, metadata, 'text/plain'),
                   'params': (self.PARAMS_NAME, params, 'text/plain')}
        res = self.sendRequest(message)
        return Result.from_dict_response(res)

    def sample_lagrange_optimization(self,
                                     objective: Union[np.ndarray, sp.spmatrix],
                                     constraints: Union[np.ndarray, sp.spmatrix],
                                     **kwargs) -> Result:
        """
        An iterative solver that uses a modified gradient descent algorithm to find the optimal
        Lagrange multiplier, alpha, for the Qubo equation,

            Q = objective + alpha * constraints

        :param objective: np.ndarray or sp.spmatrix, :math:`n x n` cost function matrix
        :param constraints: np.ndarray or sp.spmatrix, :math:`m x n+1` constraint functions matrix, where
            :math:`m` is the number of constraints and :math:`n` is the dimension of the solutions space.
        :param kwargs: Parameters for the provided sampler and optimization.
            For allowed arguments see documentation on in the sampler module.
            For Lagrange optimization, **max_depth**, int,  corresponds to the number of iterations allowed for the
            optimization loop. Default = 5.

        :return: Result
        """
        self._check_size(objective)

        self._check_constraints(objective, constraints)

        if self.is_quantum():
            self._qpu_execution_user_confirm()

        if kwargs.get('max_depth') is None:
            kwargs['max_depth'] = self.DEFAULT_LAGRANGE_MAX_DEPTH

        # if the user input 'max_depth', max sure it's nonnegative
        assert kwargs['max_depth'] >= 0, "Parameter 'max_depth' must be nonnegative."
        metadata = self.process_metadata('lagrange_opt', constraints)
        params = self.process_params(kwargs)
        # Process data arrays to byte streams
        data_obj = self.process_data(objective)
        data_con = self.process_data(constraints)
        message = {'data_obj': (self.DATA_OBJ_FNAME, data_obj, 'application/octet-stream'),
                   'data_con': (self.DATA_CON_FNAME, data_con, 'application/octet-stream'),
                   'metadata': (self.METADATA_FNAME, metadata, 'text/plain'),
                   'params': (self.PARAMS_NAME, params, 'text/plain')}
        res = self.sendRequest(message)
        return Result.from_dict_response(res)


####################################
# Entry point functions below
#
def sample_qubo(qubo: Union[dict, np.ndarray, sp.spmatrix], **kwargs) -> Result:
    """
    Return samples of (near) optimal solutions for a Quadratic Unconstrained Binary Optimization (QUBO) problem.

    :param qubo: Union[dict, np.ndarray, or sp.spmatrix], :math:`n \\times n` QUBO matrix.
        Matrices must be symmetric. Dictionary input can represent the upper triangular portion of a matrix
        (including the diagonal) or the full matrix.

    :param kwargs: dict, Parameters and arguments for the sampler and solver algorithm plus optional login information for the cloud client:

        * *access_token* str, None.
            Retrieved from .qco.conf file unless provided.
        * *conf_path* str, None.
            Path to .qci.conf file on local system. Defaults to `~/.qci.conf` on Linux/Mac.
        * *configuration* str, default = 'default'.
            Specific configuration to use, in case multiple tokens and configurations are provided in the conf `~/.qci.conf`.
        * *url* str, default = https://api.qci-prod.com.
            Url for Qatalyst web-service
        * *sampler* str, default= 'csample'.
            Available classical and quantum samplers are obtainable through `utils.print_available_samplers`.
            Use 'target_name' to specify `sampler` argument.
            List of available samplers: `braket_rigetti`, `braket_ionq`, `braket_dwave`, `braket_simulator`, `csample`.
                Braket's simulator comes in two flavors: SV1 (state vector simulator) and TN1 (based on tensor networks),
                the former is a general purpose quantum circuit simulator, while TN1 is only suitable for certain
                types of quantum circuits (see Braket documentation for further information).
                `braket_simulator` calls SV1 while `braket_simulator_tn1` calls TN1.
        * *optimizer* str
            We utilize algorithms found in `scipy.minimize` and additional stochastic version of such optimizers. If sampler is of hybrid type, defaults to 'cobyla',
            otherwise defaults to None.
        * *optimizer_params* dict = None.
            A dictionary of options to pass to the optimizer. Default will be set in the backend if argument is None. Example: `options = {'disp': False, 'maxiter': 5}`.
            If sampler is of hybrid type, defaults to {'maxiter': 5}, otherwise defaults to None.
        * *algorithm* str,
            Variational algorithm to run with a hybrid 'sampler' and classical 'optimizer'. Both of QAOA or VQE are implement (see [FGG]_, [PM]_, [MR]_). Select with 'qaoa' or 'vqe'. Defaults to 'qaoa' when sampler is of hybrid type.
        * *num_shots* int
            Number of samples taken per iteration on gate-based QPU samplers.


    :return: :meth:`qatalyst.result.Result`

    :Example:

    QUBO function input using a Numpy array (see [GK]_):

    >>> import numpy as np
    >>> from qatalyst import qcore
    >>> # 'qubo' is a symmetric version of a quadratic unconstrained binary optimization (QUBO) problem
    >>> qubo = np.array([[-6, 10, 0, 0], [10, -8, 2, 8], [0, 2, -3, 4], [0, 8, 4, -5]])
    >>> # sample_qubo requires a symmetric matrix
    >>> res = qcore.sample_qubo(qubo, num_solutions=5)
    >>> print(res)
    >>>  # Job started with JobID: 5ef37a0d08b481fef4af1d1f.
    >>>     # Problem COMPLETE, returning solution.
    >>>     # Result
    >>>     # samples
    >>>     # [[1. 0. 0. 1.]
    >>>     #  [1. 0. 1. 0.]
    >>>     #  ...
    >>>     #  [0. 0. 1. 1.]]
    >>>     # energies
    >>>     # [-11.  -9.  -8.  -7.  -6.  -6.  -5.  -3.   0.   0.]
    >>>     # counts
    >>>     # [1 1 1 1 1 1 1 1 1 1]


    Running the same problem on AWS Braket is straightforward. Suppose we would like to find an optimal solution
    using QAOA on a gate model machine [FGG]_ with a circuit depth of 2. In order to use Rigetti's Aspen-8 device with changes to the default classical
    optimizer parameters, we call `sample_qubo` with the following additional arguments:

    >>> import numpy as np
    >>> from qatalyst import qcore
    >>> qubo = np.array([[-6, 10, 0, 0], [10, -8, 2, 8], [0, 2, -3, 4], [0, 8, 4, -5]])
    >>> res = qcore.sample_qubo(qubo, sampler='braket_rigetti', algorithm='qaoa',
    >>>                         depth=2, optimizer='cobyla', optimizer_params={'maxiter': 5})
    >>> print(res)
    >>>    # Result
    >>>    # samples
    >>>    # [[1 0 0 1]
    >>>    #  [1 0 1 0]
    >>>    #  [0 1 0 0]
    >>>    #  [0 1 1 0]
    >>>    #  [1 0 0 0]
    >>>    #  [1 0 1 1]
    >>>    #  [0 0 0 1]
    >>>    #  [0 0 1 0]
    >>>    #  [0 0 0 0]
    >>>    #  [0 0 1 1]]
    >>>    # energies
    >>>    # [-11.  -9.  -8.  -7.  -6.  -6.  -5.  -3.   0.   0.]
    >>>    # counts
    >>>    # [16 20 17 17 19 25 26 22 22 18]

    Note that the energies and solutions are identical in the classical and QAOA solutions.

    Alternatively, the VQE algorithm [MR]_ uses a similar hybrid approach.

    >>> import numpy as np
    >>> from qatalyst import qcore
    >>> qubo = np.array([[-6, 10, 0, 0], [10, -8, 2, 8], [0, 2, -3, 4], [0, 8, 4, -5]])
    >>> res = qcore.sample_qubo(qubo, sampler='braket_ionq', algorithm='vqe', num_shots=10,
    >>>                         optimizer='cobyla', optimizer_params={'maxiter': 5})
    >>> print(res)
    >>>    # Result
    >>>    # samples
    >>>    # [[1 0 0 1]
    >>>    #  [1 0 1 0]
    >>>    #  [0 1 0 0]
    >>>    #  [0 1 1 0]
    >>>    #  [1 0 0 0]
    >>>    #  [1 0 1 1]
    >>>    #  [0 0 0 1]
    >>>    #  [0 0 1 0]
    >>>    #  [0 0 0 0]
    >>>    #  [0 0 1 1]]
    >>>    # energies
    >>>    # [-11.  -9.  -8.  -7.  -6.  -6.  -5.  -3.   0.   0.]
    >>>    # counts
    >>>    # [16 20 17 17 19 25 26 22 22 18]

    Lastly, we can select one of D-Wave Systems' processors to solve a small 10x10 QUBO:

    >>> import numpy as np
    >>> from qatalyst import qcore
    >>>
    >>> q = np.random.normal(size=(10,10))
    >>> Q = q + q.T         # make a symmetric matrix
    >>> # defaults to Advantage system
    >>> res = qcore.sample_qubo(Q, sampler='braket_dwave', num_reads=10)
    >>> print(res)
    >>>     # Result
    >>>     # samples
    >>>     # [[0. 0. 1. 1. 0. 1. 0. 0. 1. 1.]
    >>>     #  [0. 0. 1. 1. 0. 1. 0. 1. 1. 1.]
    >>>     #  [0. 0. 1. 1. 0. 1. 0. 1. 1. 0.]
    >>>     #  [0. 1. 1. 1. 0. 1. 0. 1. 1. 1.]
    >>>     #  [0. 1. 1. 1. 0. 1. 0. 0. 1. 1.]]
    >>>     # energies
    >>>     # [-18.25006755 -18.22989166 -17.23651149 -14.37725584 -13.82046326]
    >>>     # counts
    >>>     # [2 1 4 1 2]

    """
    client_kwargs, param_kwargs = get_client_kwargs(**kwargs)
    client = QatalystCore(**client_kwargs)
    return client.sample_qubo(qubo, **param_kwargs)


def sample_constraint_problem(objective: Union[np.ndarray, sp.spmatrix],
                              constraints: Union[np.ndarray, sp.spmatrix],
                              alpha: float = 1.0,
                              **kwargs) -> Result:
    """
    Return samples of a constraint problem with an objective function and linear equality constraints.

    The objective function is defined by a :math:`n \\times n` matrix; the constraint matrix is :math:`m \\times n+1`,
    which is with a constraint vector in the final column.

    Example:

    >>> objective = np.array([[-6, 10, 0, 0], [10, -8, 2, 8], [0, 2, -3, 4], [0, 8, 4, -5]])
    >>> constraints = np.array([[1, 1, 1, 1, -1], [0, 1, 1, 1, -1]])

      where *objective* is an :math:`n \\times n` cost function and *constraints* is an :math:`m \\times (n+1)` matrix composed of a
      system of linear constraints. One can think of constraints as an *augmented* system of linear constraints. In the
      example above this would be

    >>> A = constraints[:, :-1]

        and the final column

    >>> b = np.array([1, 1.])

        giving  *constraints* = [A | -b].

    If the variables are labeled by the column indices, then the rows of the augmented constraint matrix state that

            :math:`x_0 + x_1 + x_2 + x_3 - 1 == 0`

            :math:`x_1 + x_2 + x_3 - 1 == 0`

    To compute the QUBO we combine the objective and constraints.

    :param objective: np.ndarray or sp.spmatrix, :math:`n \\times n` symmetric cost function matrix.
    :param constraints: np.ndarray or sp.spmatrix, :math:`m \\times n+1` constraint matrix, where
       :math:`m` is the number of constraints and :math:`n` is the dimension of the solution space.
    :param alpha: float, optional. Lagrange multiplier to scale constraints when computing QUBO,
       *Q = objective + alpha * constraints*. Default = 1.0.

    :param kwargs: dict, Parameters and arguments for the sampler and solver algorithm.

        * *sampler* -- str, the sampler to call.
            Default = *csample*. Also available for 'braket_dwave_*' and 'braket_simulator'.
        * See `qcore.sample_qubo` for additional kwargs.

    :return: :meth:`qatalyst.result.Result`

    :Example:

    >>> import numpy as np
    >>> from qatalyst import qcore
    >>> objective = np.array([[-6, 10, 0, 0], [10, -8, 2, 8], [0, 2, -3, 4], [0, 8, 4, -5]])
    >>> constraints = np.array([[1, 1, 1, 1, -1], [0, 1, 1, 1, -1]])
    >>> alpha = 2
    >>> res = qcore.sample_constraint_problem(objective, constraints, alpha=alpha, num_solutions=5)

    In addition to the classical sampler, various quantum backends are also available. For instance,
    setting :code:`sampler='braket_dwave'`, will construct a QUBO from the objective and
    constraint matrices and sample the problem on D-Wave System's 2000Q processor to obtain the result in :code:`res`.

    >>> import numpy as np
    >>> from qatalyst import qcore
    >>> objective = np.array([[-6, 10, 0, 0], [10, -8, 2, 8], [0, 2, -3, 4], [0, 8, 4, -5]])
    >>> constraints = np.array([[1, 1, 1, 1, -1], [0, 1, 1, 1, -1]])
    >>> alpha = 2
    >>> res = qcore.sample_constraint_problem(objective, constraints,
    >>>                                       alpha=alpha, num_solutions=5,
    >>>                                       sampler='braket_dwave')

    Alternatively, a variational algorithm can be used to to sample the resultant QUBO, as detailed in the code snippet
    that follows:

    >>> import numpy as np
    >>> from qatalyst import qcore
    >>> objective = np.array([[-6, 10, 0, 0], [10, -8, 2, 8], [0, 2, -3, 4], [0, 8, 4, -5]])
    >>> constraints = np.array([[1, 1, 1, 1, -1], [0, 1, 1, 1, -1]])
    >>> alpha = 2
    >>> res = qcore.sample_constraint_problem(objective, constraints,
    >>>                                       alpha=alpha, num_solutions=5,
    >>>                                       sampler='braket_rigetti', algorithm='qaoa',
    >>>                                       optimizer='cobyla', num_shots=10,
    >>>                                       optimizer_params={'maxiter': 5})

    See :ref:`Quantum Algorithms and Devices` for more details on QPU options and available parameters.

    """
    client_kwargs, param_kwargs = get_client_kwargs(**kwargs)
    client = QatalystCore(**client_kwargs)
    return client.sample_constraint_problem(objective, constraints, alpha, **param_kwargs)


def sample_lagrange_optimization(objective: Union[np.ndarray, sp.spmatrix],
                                 constraints: Union[np.ndarray, sp.spmatrix],
                                 **kwargs) -> Result:
    """
    Return samples of an optimal solution to a constraint optimization problem with an objective function
    and a system of linear constraints.

    Consider the problem defined by an objective function represented by an :math:`n \\times n` matrix, and an :math:`m \\times n+1`
    constraint matrix. See :meth:`sample_constraint_problem` for details on the *objective* and *constraints* matrices.
    The Lagrange multiplier is designed to balance the scales of the objective function and the system of constraints.

    Ideally, the Lagrangian, :math:`\\alpha`, reflects the importance of the constraints, and can be a vector.
    Lagrange Optimization is an iterative approach for choosing the ideal :math:`\\alpha` such that the constraints are satisfied, allowing the
    sampler to focus on minimizing the energy of the objective function.

    :Example:

    >>> objective = np.array([[-6, 10, 0, 0], [10, -8, 2, 8], [0, 2, -3, 4], [0, 8, 4, -5]])
    >>> constraints = np.array([[1, 0, 1, 1, -1], [1, 1, 0, 1, -1]])

    To compute the QUBO we combine the objective and constraints.

    Lagrange Optimization runs the chosen sampler up to `max_depth` times to determine the :math:`\\alpha` that
    minimizes *Q* while simultaneously satisfying constraints, eg., :math:`Av_0 == 0`, where :math:`v_0` is the
    minimum energy sample returned by the sampler.

    Lagrange optimization is more involved, and returns an additional non-empty `properties` attribute with the
    Result object. In `properties['alpha']`, the :math:`m`-dimensional vectors record the updates to `alpha`,
    which are performed on a
    per-constraint basis, where :math:`m` is the dimension of the row space of the constraint matrix, :math:`A`.
    The  `properties['constraint_evals']` values record the result of :math:`Av_0` for each iteration.

    :param objective: np.ndarray or sp.spmatrix,
        :math:`n \\times n` symmetric cost function matrix.
    :param constraints: np.ndarray or sp.spmatrix,
        :math:`m \\times n+1` constraint matrix, where :math:`m` is the number of constraints and :math:`n` is the dimension of the solution space.

    :param kwargs: dict, Parameters and arguments for the sampler and solver algorithm.

        * *max_depth* -- int
            maximum number of times to update *alpha* in a search for a value that will satisfy
            constraints as well as minimize energy. Note: Indexing for depth (iterations) is 0-based. The `sample_lagrange_optimization`
            function performs at minimum a single (0th) pass. This is consistent with the concept of depth, in that
            a surface-level analysis is `depth=0`, and further exploration, `depth > 1`, implies digging deeper. Furthermore,
            this implies that for `depth=k`, the number of vectors in the `alpha` field of `Result.properties` will
            be `k+1`.
        * *sampler* -- str
            The sampler to call. Default = 'csample'. Also available for 'braket_dwave_advantage', 'braket_dwave_2000Q', and 'braket_simulator'.
        * See `qcore.sample_qubo` for additional kwargs.


    :return: :meth:`qatalyst.result.Result`

    :Examples:

    >>> import numpy as np
    >>> from qatalyst import qcore
    >>> objective = np.array([[ 3.4 ,  1.1 , -1.7 , -1.6 ], [ 1.1 ,  4.5 ,  2.25,  2.25],  [-1.7 ,  2.25,  2.1 ,  0.5 ],  [-1.6 ,  2.25,  0.5 , -2.4 ]])
    >>> constraints = np.array([[1, 0, 1, 1, -1], [1, 1, 0, 1, -1]])
    >>> res = qcore.sample_lagrange_optimization(objective, constraints, max_depth=20,
    >>>                                          num_solutions=5)


    Given objectives and constraints, :math:\\alpha can be optimized on a QPU as well. This is of interest for
    D-Wave's processors, where finding an effective Lagrangian can take time by hand. Here we run the constraint problem
    on the Advantage system, limiting the number of iteration used to find an optimal alpha to `max_depth=5`.

    >>> import numpy as np
    >>> from qatalyst import qcore
    >>> objective = np.array([[-6, 10, 0, 0], [10, -8, 2, 8], [0, 2, -3, 4], [0, 8, 4, -5]])
    >>> constraints = np.array([[1, 1, 1, 1, -1], [0, 1, 1, 1, -1]])
    >>> res = qcore.sample_lagrange_optimization(objective, constraints, max_depth=5,
    >>>                                          sampler='braket_dwave_advantage',
    >>>                                          num_reads=1000)

    It is also possible to optimize the Lagrangian parameter used to construct a QUBO for a variational algorithm
    such as VQE or QAOA. For instance,

    >>> import numpy as np
    >>> from qatalyst import qcore
    >>> objective = np.array([[-6, 10, 0, 0], [10, -8, 2, 8], [0, 2, -3, 4], [0, 8, 4, -5]])
    >>> constraints = np.array([[1, 1, 1, 1, -1], [0, 1, 1, 1, -1]])
    >>> res = qcore.sample_lagrange_optimization(objective, constraints, max_depth=5,
    >>>                                          sampler='braket_rigetti', algorithm='qaoa',
    >>>                                          num_shots=10, optimizer='cobyla',
    >>>                                          optimizer_params={'maxiter': 5})
    """
    client_kwargs, param_kwargs = get_client_kwargs(**kwargs)
    client = QatalystCore(**client_kwargs)
    return client.sample_lagrange_optimization(objective, constraints, **param_kwargs)
