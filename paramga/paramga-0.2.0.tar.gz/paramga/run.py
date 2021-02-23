import numpy
from .generator import generate_param_state
from .crossover import combine_param_state
from .mutation import mutate_param_state
from multiprocessing import Process, Queue
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Callable, List

# RunOutput = namedtuple('RunOutput', 'best_parameters, iterations, loss_values')


@dataclass
class IterationState:
    parameters: List[dict]
    best_parameters: dict
    loss: float = 9999999
    lowest_loss: float = 9999999
    iterations: int = 0
    loss_values: List = field(default_factory=lambda: [])


def get_outputs(func, input_args):
    return [func(*args) for args in input_args]


def get_outputs_parallel(func, input_args):
    Q = Queue()

    def q_wrap(q, args):
        q.put(func(*args))

    procs = []
    outputs = []
    for args in input_args:
        p = Process(target=q_wrap, args=([Q, args]))
        procs.append(p)
        p.start()
    for p in procs:
        res = Q.get()
        outputs.append(res)
    for p in procs:
        p.join()
    return outputs


# def iteration(iteration_state: IterationState, func: Callable, loss_func, population: int, mutation_conf: List[dict], input_data=None):
#     loss = iteration_state.loss
#     parameters = iteration_state.parameters
#     lowest_loss = iteration_state.lowest_loss
#     best_parameters = iteration_state.best_parameters
#     # Run and get losses
#     outputs = [func(params, input_data) for params in parameters]
#     losses = [loss_func(o, p) for p, o in zip(parameters, outputs)]
#     iteration_state.loss = min(losses)
#     iteration_state.loss_values.append(iteration_state.loss)
#     total_loss = sum(losses)

#     # Sort parameters
#     parameters_index_sorted = list(
#         map(lambda x: x[0], sorted(enumerate(losses), key=lambda si: si[1])))

#     # Set new best parameters if loss is lowest
#     best_parameters = parameters[parameters_index_sorted[0]
#                                  ] if iteration_state.loss < lowest_loss else best_parameters
#     lowest_loss = iteration_state.loss if iteration_state.loss < lowest_loss else lowest_loss
#     # Choose next parameter pairs based on
#     loss_ratios = [((total_loss - loss)/total_loss)/(population-1) for loss in losses]
#     choices_population = [numpy.random.choice(
#         population, 2, p=loss_ratios) for i in range(population)]
#     new_parameters = [combine_param_state(*[parameters[i] for i in choices])
#                       for choices in choices_population]

#     mutated_new_parameters = [mutate_param_state(param, mutation_conf) for param in new_parameters]

#     return IterationState(mutated_new_parameters, best_parameters, loss, lowest_loss, iteration_state.iterations + 1, iteration_state.loss_values + [loss])


# def run(
#         param_base,
#         gaconf,
#         func,
#         loss_func,
#         input_data,
#         population=10,
#         tolerance=0.1,
#         max_iterations=1000,
#         verbose=False,
# ):
#     initial_parameters = [mutate_param_state(param_base, gaconf) for _ in range(population)]
#     iteration_state = IterationState(
#         parameters=initial_parameters,
#         best_parameters=initial_parameters[0],
#     )
#     while iteration_state.loss > tolerance and iteration_state.iterations < max_iterations:
#         # Run and get losses
#         outputs = [func(params, input_data) for params in parameters]
#         losses = [loss_func(o, p) for p, o in zip(parameters, outputs)]
#         iteration_state.loss = min(losses)
#         iteration_state.loss_values.append(iteration_state.loss)
#         total_loss = sum(losses)

#         # Sort parameters
#         parameters_index_sorted = list(
#             map(lambda x: x[0], sorted(enumerate(losses), key=lambda si: si[1])))

#         # Set new best parameters if loss is lowest
#         best_parameters = parameters[parameters_index_sorted[0]
#                                      ] if iteration_state.loss < lowest_loss else best_parameters
#         lowest_loss = iteration_state.loss if iteration_state.loss < lowest_loss else lowest_loss
#         # Choose next parameter pairs based on
#         loss_ratios = [((total_loss - loss)/total_loss)/(population-1) for loss in losses]
#         choices_population = [numpy.random.choice(
#             population, 2, p=loss_ratios) for i in range(population)]
#         new_parameters = [combine_param_state(*[parameters[i] for i in choices])
#                           for choices in choices_population]

#         mutated_new_parameters = [mutate_param_state(param, gaconf) for param in new_parameters]

#         parameters = mutated_new_parameters
#         iteration_state.iterations += 1

#     return iteration_state


class Logger:
    def __init__(self, log_level):
        self.log_level = log_level

    def log(self, message):
        if self.log_level > 0:
            print(message)


def iteration(iteration_state: IterationState, func: Callable, loss_func, population: int, mutation_conf: List[dict], input_data=None, parallel=False):
    loss = iteration_state.loss
    parameters = iteration_state.parameters
    lowest_loss = iteration_state.lowest_loss
    best_parameters = iteration_state.best_parameters

    # Run and get losses
    input_args = [(params, input_data) for params in parameters]

    run_func = get_outputs_parallel if parallel else get_outputs
    outputs = run_func(func, input_args)

    losses = [loss_func(o, p) for p, o in zip(parameters, outputs)]
    loss = min(losses)
    total_loss = sum(losses)

    # Sort parameters
    parameters_index_sorted = list(
        map(lambda x: x[0], sorted(enumerate(losses), key=lambda si: si[1])))

    # Set new best parameters if loss is lowest
    best_parameters = parameters[parameters_index_sorted[0]
                                 ] if loss < lowest_loss else best_parameters
    lowest_loss = loss if loss < lowest_loss else lowest_loss
    # Choose next parameter pairs based on
    loss_ratios = [((total_loss - loss)/total_loss)/(population-1) for loss in losses]
    choices_population = [numpy.random.choice(
        population, 2, p=loss_ratios) for i in range(population)]
    new_parameters = [combine_param_state(*[parameters[i] for i in choices])
                      for choices in choices_population]

    mutated_new_parameters = [mutate_param_state(param, mutation_conf) for param in new_parameters]

    return IterationState(mutated_new_parameters, best_parameters, loss, lowest_loss, iteration_state.iterations + 1, iteration_state.loss_values + [loss])


def run(param_base, mutation_conf, func, loss_func, input_data, population=8, tolerance=0.1, max_iterations=1000, parallel=False, verbose=False):
    initial_parameters = [mutate_param_state(param_base, mutation_conf) for _ in range(population)]
    logger = Logger(1 if verbose else 0)

    iteration_state = IterationState(
        parameters=initial_parameters,
        best_parameters=initial_parameters[0],
    )

    logger.log("Starting")
    while iteration_state.loss > tolerance and iteration_state.iterations < max_iterations:
        logger.log(
            f"========= Running iteration: {iteration_state.iterations}. Loss is {iteration_state.loss}")
        iteration_state = iteration(
            iteration_state,
            func,
            loss_func,
            population,
            mutation_conf,
            input_data=input_data,
            parallel=parallel,
        )

    return iteration_state


def run_iterator(param_base, mutation_conf, func, loss_func, input_data, population=8, tolerance=0.1, max_iterations=1000, verbose=False, parallel=False):
    initial_parameters = [mutate_param_state(param_base, mutation_conf) for _ in range(population)]

    # initial_parameters = [generate_param_state(param_base, gaconf) for i in range(population)]
    logger = Logger(1 if verbose else 0)
    iteration_state = IterationState(
        parameters=initial_parameters,
        best_parameters=initial_parameters[0],
    )

    logger.log("Starting")
    while iteration_state.loss > tolerance and iteration_state.iterations < max_iterations:
        logger.log(
            f"========= Running iteration: {iteration_state.iterations}. Loss is {iteration_state.loss}")
        iteration_state = iteration(
            iteration_state,
            func,
            loss_func,
            population,
            mutation_conf,
            input_data=input_data,
            parallel=parallel,
        )
        yield iteration_state

    yield iteration_state
