from enum import IntEnum

__all__ = ['GraphType','ModelType','InferenceType','SamplerType','StatisticsType', 'Optimizer']

class StatisticsType(IntEnum):
	overcomplete = 0
	minimal = 1

class GraphType(IntEnum):
	custom = 0
	chain = 1
	grid = 2
	star = 3
	full = 5
	auto_tree = 6
	elemgm = 7
	other = 8
	auto = 12
	auto_random = 13

class InferenceType(IntEnum):
	belief_propagation = 0
	junction_tree = 1
	stochastic_quadrature = 2
	external = 3
	belief_propagation_gpu = 3

class SamplerType(IntEnum):
	gibbs = 0
	perturb_and_map = 1

class Optimizer(IntEnum):
	gradient_descent = 4
	proximal_gradient = 5
	accelerated_proximal_gradient = 6
	ea = 7

class ModelType(IntEnum):
	mrf = 0
	strf_linear = 1
	strf_quadratic = 2
	strf_cubic = 3
	strf_rational = 4
	strf_exponential = 5
	strf_inv_quadratic = 6
	strf_inv_cubic = 7
	strf_inv_rational = 8
	strf_inv_exponential = 9
	integer = 10
	dbt = 11
	ising = 12

#class Model:
#	def __init__(self, _ptr):
#		self.ptr = _ptr
