import numpy
from .generator import generate_param_state
from .crossover import combine_param_state
from .mutation import mutate_param_state


def run(param_base, gaconf, func, optfunc, input_data, population=10, tolerance=0.1, max_iterations=1000):
    initial_parameters = [param_base for _ in range(population)]
    # initial_parameters = [generate_param_state(param_base, gaconf) for i in range(population)]

    parameters = initial_parameters
    best_parameters = parameters[0]
    loss = 9999999
    lowest_loss = 999999
    iterations = 0
    loss_values = []

    while loss > tolerance and iterations < max_iterations:
        # Run and get losses
        outputs = [func(params, input_data) for params in parameters]
        losses = [optfunc(o, p) for p, o in zip(parameters, outputs)]
        loss = min(losses)
        loss_values.append(loss)
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

        mutated_new_parameters = [mutate_param_state(param, gaconf) for param in new_parameters]

        parameters = mutated_new_parameters
        iterations += 1

    return best_parameters, iterations, loss_values
