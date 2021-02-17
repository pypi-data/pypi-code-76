__all__ = ['GraphType', 'ModelType', 'InferenceType', 'SamplerType', 'StatisticsType', 'Optimizer']

import ctypes
import time
import numpy
import json
import itertools
import struct
import sys, os
import atexit
import platform
from .functions import *
from pathlib import Path
path = Path(__file__)

__os  = platform.uname().system
__cpu = platform.uname().machine
__lib = 'lib/libpx'
__ext = 'lib/libpx'
__suf = '.so'

default_itype = numpy.uint64
default_vtype = numpy.float64

if os.environ.get('PX_ITYPE') is not None:
	if (os.environ.get('PX_ITYPE') == 'uint8'):
		default_itype = numpy.uint8
	elif (os.environ.get('PX_ITYPE') == 'uint16'):
		default_itype = numpy.uint16
	elif (os.environ.get('PX_ITYPE') == 'uint32'):
		default_itype = numpy.uint32
	elif (os.environ.get('PX_ITYPE') == 'uint64'):
		default_itype = numpy.uint64
	else:
		raise TypeError('PX_ITYPE must be one of {uint8,uint16,uint32,uint64}')
	
if os.environ.get('PX_VTYPE') is not None:
	if (os.environ.get('PX_VTYPE') == 'uint8'):
		default_vtype = numpy.uint8
	elif (os.environ.get('PX_VTYPE') == 'uint16'):
		default_vtype = numpy.uint16
	elif (os.environ.get('PX_VTYPE') == 'uint32'):
		default_vtype = numpy.uint32
	elif (os.environ.get('PX_VTYPE') == 'uint64'):
		default_vtype = numpy.uint64
	elif (os.environ.get('PX_VTYPE') == 'float32'):
		default_vtype = numpy.float32
	elif (os.environ.get('PX_VTYPE') == 'float64'):
		default_vtype = numpy.float64
	else:
		raise TypeError('PX_VTYPE must be one of {uint8,uint16,uint32,uint64,float32,float64}')

DEBUGMODE = False
if os.environ.get('PX_DEBUGMODE') is not None:
	DEBUGMODE = (os.environ['PX_DEBUGMODE'] == 'True')

if __os == 'Windows': # otherwise: assume linux
	__suf = '.dll' # Tested on Win10 1909 but should work on older Windows versions

if __cpu == 'aarch64': # otherwise: assume x86_64 / AMD64
	__lib += '_aarch64' # Tested NVIDIA Jetson TX1, but might work on other aarch64 systems
	__ext += '_aarch64' # Tested NVIDIA Jetson TX1, but might work on other aarch64 systems

if DEBUGMODE: # Warning: Windows debug core is not included in the pypi package!
	__lib += '_dbg'

pxpath = str( path.parent / (__lib + __suf) )

example_data_filename  = str(path.parent / "data/sin44")

if os.environ.get('PX_EXTINF') is not None:
	extpath = Path(os.environ['PX_EXTINF'])
else:
	extpath = path.parent / (__ext + '_ext_culbp' + __suf) # Warning: Windows CUDA driver is not included in the pypi package!

ext_lib = None
# TODO: defer the following decision to infer()
EXTINF = 0
if extpath.exists():
	ext_lib = ctypes.cdll.LoadLibrary(str(extpath))
	ext_lib.external.restype = ctypes.c_uint64
	ext_lib.external.argtypes = [ctypes.c_uint8, ctypes.c_uint8]

class disc_t(ctypes.Structure):
	_fields_ = [("num_intervals", ctypes.c_uint64), ("num_moments", ctypes.c_uint64), ("_intervals", ctypes.POINTER(ctypes.c_double)), ("_moments", ctypes.POINTER(ctypes.c_double)), ("mean", ctypes.c_double), ("sdev", ctypes.c_double)]

	__from_file = False
	__intervals = []
	__moments   = []

	@property
	def intervals(self):
		if not self.__from_file:
			return numpy.ctypeslib.as_array(self._intervals, shape = (self.num_intervals, 2))
		else:
			return self.__intervals

	@property
	def moments(self):
		if not self.__from_file:
			return numpy.ctypeslib.as_array(self._moments, shape = (self.num_moments, 5))
		else:
			return self.__moments

	def __init__(self, I, M, m, s):
		self.__from_file = True
		self.__intervals = I
		self.__moments = M
		self.mean = m
		self.sdev = s

lib = ctypes.cdll.LoadLibrary(pxpath)

lib.create_ctx.restype = ctypes.c_uint64

lib.version.restype = ctypes.c_uint64

lib.ctx_set_code.restype = ctypes.c_bool

lib.discretize.restype = disc_t
lib.discretize.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]

lib.discretize_precomputed.restype = None
lib.discretize_precomputed.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, disc_t]

lib.reset_ctx.restype  = ctypes.c_bool
lib.reset_ctx.argtypes = [ctypes.c_uint64]

lib.run_ctx.restype  = ctypes.c_bool
lib.run_ctx.argtypes = [ctypes.c_uint64]

lib.destroy_ctx.restype  = None
lib.destroy_ctx.argtypes = [ctypes.c_uint64]

lib.ctx_write_reg.restype  = ctypes.c_bool
lib.ctx_write_reg.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_uint64]

lib.ctx_read_reg.restype  = ctypes.c_uint64
lib.ctx_read_reg.argtypes = [ctypes.c_uint64, ctypes.c_char_p]

MISSING_VALUE = 65535

def array_check(a, name, dtype=None):
	if not isinstance(a, numpy.ndarray):
		raise TypeError(name,'must be of type numpy.ndarray')
	if isinstance(a, numpy.ndarray) and not a.flags['C_CONTIGUOUS']:
		raise TypeError(name,'must be a C-style contiguous numpy array')
	if dtype is not None:
		if isinstance(a, numpy.ndarray) and not a.dtype==dtype:
			raise TypeError('ERROR: type of',a,'must be',str(dtype))

		
def switch_type(T):
	if T == numpy.uint8:
		return 0
	if T == numpy.uint16:
		return 1
	if T == numpy.uint32:
		return 2
	if T == numpy.uint64:
		return 3
	if T == numpy.float32:
		return 4
	if T == numpy.float64:
		return 5
	TypeError('ERROR: unsupported type: '+str(T))


class Graph_incomplete(ctypes.Structure):

	__edgelistref = None
	destroyed = False

	@property
	def nodes(self):
		if self.destroyed:
			return 0
		return self._nodes

	@property
	def edges(self):
		if self.destroyed:
			return 0
		return self._edges

	def __len__(self):
		if self.destroyed:
			return 0
		return self.nodes

	def delete(self):
		if not self.destroyed:
			self.destroyed = True
			L = ["GPT "+str(ctypes.addressof(self))+";", "DEL GPT;"]
			recode(L)
			run()

	@property
	def edgelist(self):
		if self.destroyed:
			return numpy.array([])
		res = numpy.ctypeslib.as_array(self.A, shape = (self.edges, 2))
		res.flags.writeable = False
		return res

	def add_node_to_dot(self, dot, i, nodenames=None):
		if nodenames is not None and i < len(nodenames):
			dot.node(str(i), nodenames[i])
		elif nodenames is not None and i >= len(nodenames):
			dot.node(str(i), "H"+str(i-len(nodenames)))
		else:
			dot.node(str(i))

	def draw(self,filename,nodenames=None):
		if self.destroyed:
			return
		import os
		from graphviz import Graph
		dot = Graph(comment="pxpy",engine="neato")
		dot.attr(overlap = 'false')
		dot.attr('node', shape='box')
		for i in range(0,self.nodes):
			self.add_node_to_dot(dot,i,nodenames)

		for e in self.edgelist:
			dot.edge(str(e[0]), str(e[1]), len='1.0')

		dot.render(os.path.splitext(filename)[0],format='pdf')

	def draw_neighbors(self,target,filename,nodenames=None):
		if self.destroyed:
			return
		import os
		from graphviz import Graph
		dot = Graph(comment="pxpy",engine="neato")
		dot.attr(overlap = 'false')
		dot.attr('node', shape='box')

		self.add_node_to_dot(dot,target,nodenames)

		for e in self.edgelist:
			if e[0] == target:
				self.add_node_to_dot(dot,e[1],nodenames)
				dot.edge(str(e[0]), str(e[1]), len='1.0')
			elif e[1] == target:
				self.add_node_to_dot(dot,e[0],nodenames)
				dot.edge(str(e[0]), str(e[1]), len='1.0')

		dot.render(os.path.splitext(filename)[0],format='pdf')

class Graph0(ctypes.Structure):

	_fields_ = [("__unused", ctypes.c_uint64), ("itype", ctypes.c_uint8)]
			
	@property
	def __cidxtype(self):
		if self.itype == 0:
			return ctypes.c_uint8
		elif self.itype == 1:
			return ctypes.c_uint16
		elif self.itype == 2:
			return ctypes.c_uint32
		else:
			return ctypes.c_uint64
			
	def get_fields(self):
		return [("__unused", ctypes.c_uint64), ("itype", ctypes.c_uint8), ("_nodes", self.__cidxtype), ("_edges", self.__cidxtype), ("A", ctypes.POINTER(self.__cidxtype))]
		
	def get_type(self):
		return type("Graph", (Graph_incomplete,), {"_fields_": self.get_fields()})
		
	def cast(self):
		self.__class__ = self.get_type()
		return self

class STGraph_incomplete(ctypes.Structure):

	@property
	def __idxtype(self):
		if self.itype == 0:
			return numpy.uint8
		elif self.itype == 1:
			return numpy.uint16
		elif self.itype == 2:
			return numpy.uint32
		else:
			return numpy.uint64

	__LOCAL_G = None
	destroyed = False

	@property
	def base(self):
		if self.__LOCAL_G is None:
			self.__LOCAL_G = ctypes.cast(self.base0, ctypes.POINTER(Graph0)).contents.cast()
		return self.__LOCAL_G

	def delete(self):
		if not self.destroyed:
			self.base.delete()

	@property
	def nodes(self):
		return self.base.nodes * self.T

	def __len__(self):
		return self.nodes

	@property
	def edges(self):
		return self.base.edges * self.T + (self.T-1) * ( self.base.nodes + 2 * self.base.edges )

	@property
	def edgelist(self):
		if not hasattr(self, 'E'):
			self.E = numpy.zeros((self.edges, 2), dtype = self.__idxtype)

			for v in range(self.base.nodes):
				for t in range(self.T-1):
					e = v * (self.T-1) + t
					self.E[e][0] = t * self.base.nodes + v
					self.E[e][1] = (t + 1) * self.base.nodes + v

			for f in range(self.base.edges):
				a = self.base.edgelist[f][0]
				b = self.base.edgelist[f][1]
				for t in range(self.T-1):
					e = (self.T-1) * self.base.nodes + f * 3 * (self.T-1) + t * 3
					self.E[e + 0][0] = t * self.base.nodes + a
					self.E[e + 0][1] = t * self.base.nodes + b
					self.E[e + 1][0] = t * self.base.nodes + a
					self.E[e + 1][1] = (t + 1) * self.base.nodes + b
					self.E[e + 2][0] = (t + 1) * self.base.nodes + a
					self.E[e + 2][1] = t * self.base.nodes + b

				e = (self.T-1) * self.base.nodes + (self.T-1) * 3 * self.base.edges + f
				self.E[e][0] = (self.T-1) * self.base.nodes + a
				self.E[e][1] = (self.T-1) * self.base.nodes + b

			self.E.flags.writeable = False

		return self.E

	def spatial_vertex(self, v):
		return v % self.base.nodes

	def time(self, v):
		return (v-self.spatial_vertex(v)) / self.base.nodes

	def is_spatial_edge(self, e):
		return self.time(self.edgelist[e][0]) == self.time(self.edgelist[e][1])

class STGraph0(ctypes.Structure):

	_fields_ = [("__unused", ctypes.c_uint64), ("itype", ctypes.c_uint8)]

	@property
	def __idxtype(self):
		if self.itype == 0:
			return numpy.uint8
		elif self.itype == 1:
			return numpy.uint16
		elif self.itype == 2:
			return numpy.uint32
		else:
			return numpy.uint64
			
	@property
	def __cidxtype(self):
		if self.itype == 0:
			return ctypes.c_uint8
		elif self.itype == 1:
			return ctypes.c_uint16
		elif self.itype == 2:
			return ctypes.c_uint32
		else:
			return ctypes.c_uint64

	def get_fields(self):
		# Notice: base0 has pointer type (64-bit)
		return [("__unused", ctypes.c_uint64), ("itype", ctypes.c_uint8), ("T", self.__cidxtype), ("base0", ctypes.c_uint64), ("Tm1inv", ctypes.c_float)]
		
	def get_type(self):
		return type("STGraph", (STGraph_incomplete,), {"_fields_": self.get_fields()})
		
	def cast(self):
		self.__class__ = self.get_type()
		return self

class Model_incomplete(ctypes.Structure):

	@property
	def __idxtype(self):
		if self.itype == 0:
			return numpy.uint8
		elif self.itype == 1:
			return numpy.uint16
		elif self.itype == 2:
			return numpy.uint32
		else:
			return numpy.uint64
			
	@property
	def __cidxtype(self):
		if self.itype == 0:
			return ctypes.c_uint8
		elif self.itype == 1:
			return ctypes.c_uint16
		elif self.itype == 2:
			return ctypes.c_uint32
		else:
			return ctypes.c_uint64
			
	@property
	def __valtype(self):
		if self.vtype == 0:
			return numpy.uint8
		elif self.vtype == 1:
			return numpy.uint16
		elif self.vtype == 2:
			return numpy.uint32
		elif self.vtype == 3:
			return numpy.uint64
		elif self.vtype == 4:
			return numpy.float32
		else:
			return numpy.float64
			
	@property
	def __cvaltype(self):
		if self.vtype == 0:
			return ctypes.c_uint8
		elif self.vtype == 1:
			return ctypes.c_uint16
		elif self.vtype == 2:
			return ctypes.c_uint32
		elif self.vtype == 3:
			return ctypes.c_uint64
		elif self.vtype == 4:
			return ctypes.c_float
		else:
			return ctypes.c_double

	__LOCAL_G = None
	__OLD_G = None
	
	__A         = None
	__observed  = None
	__marginals = None
	__woff      = None

	__ysum      = 0

	__statsref = None
	__weightsref = None
	__statesref  = None
	__woffref    = None

	structure_score = 0;

	destroyed = False

	def __init__(self, weights, graph, states, stats = StatisticsType.overcomplete, itype=default_itype, vtype=default_vtype):

		if not isinstance(graph, Graph_incomplete):
			raise TypeError('ERROR: graph must be an instance of Graph')
			
		if graph.itype != switch_type(itype):
			raise TypeError('ERROR: itype of graph must match model itype')

		array_check(weights, "weights")

		if isinstance(states, numpy.ndarray):
			array_check(states, "states", self.__idxtype)
			if len(states) < graph.nodes:
				raise TypeError('ERROR: states must contain one statespace size for each variable in the model')
		elif not isinstance(states, int):
			raise TypeError('ERROR: states must be an int or of type numpy.ndarray')

		if not isinstance(stats, StatisticsType):
			raise TypeError('ERROR: model must have either covercomplete or minimal sufficient statistics')

		if stats == StatisticsType.minimal and ((isinstance(states, int) and states != 2) or (isinstance(states, numpy.ndarray) and not (numpy.unique(S)[0]==2 or len(numpy.unique(S))==1) )):
			raise TypeError('ERROR: models with minimal sufficient statistics are only supported with 2 states per variable')

		self.itype = switch_type(itype)
		self.vtype = switch_type(vtype)
			
		self.from_file = False
		self.from_python = True
		self.G = ctypes.addressof(graph)
		self.H = 0
		
		if weights.dtype != vtype:
			raise TypeError('ERROR: weights.dtype must be vtype')
		
		if len(weights) > numpy.iinfo(itype).max:
			raise TypeError('ERROR: itype not large enough to handle number of parameters')

		if isinstance(states, numpy.ndarray):
			if len(states) > numpy.iinfo(itype).max:
				raise TypeError('ERROR: itype not large enough to handle number of variables')
			if numpy.max(states) >= numpy.iinfo(itype).max:
				raise TypeError('ERROR: itype not large enough to handle number of states')
		
			self.Y = ctypes.cast(states.ctypes.data, ctypes.POINTER(self.__cidxtype))
			self.__statesref = states
		else:
			if states >= numpy.iinfo(itype).max:
				raise TypeError('ERROR: itype not large enough to handle number of states')
		
			temp1 = states * numpy.ones(graph.nodes, dtype = self.__idxtype)
			self.Y = ctypes.cast(temp1.ctypes.data, ctypes.POINTER(self.__cidxtype))
			self.__statesref = temp1

		self._Model__Ynames = None
		self._Model__Xnames = None

		d = 0
		for e in range(graph.edges):
			d += self.states[graph.edgelist[e][0]] * self.states[graph.edgelist[e][1]]
		self.dimension = int(d)
		self.fulldimension = self.dimension
		for v in range(graph.nodes):
			self.fulldimension += int(self.states[v])
		self.offsetdimension = graph.nodes + graph.edges

		if stats == StatisticsType.minimal:
			self.reparam = 12
		else:
			self.reparam = 0

		if len(weights) < d:
			weights.resize(int(d), refcheck = False)
		self.w = ctypes.cast(weights.ctypes.data, ctypes.POINTER(self.__cvaltype))

		self.__statsref = numpy.zeros(self.fulldimension).astype(self.__valtype)
		self.empirical_stats = ctypes.cast(self.__statsref.ctypes.data, ctypes.POINTER(self.__cvaltype))
		
		self.woffsets = None
		
		self.gtype = int(GraphType.other)
		self.T = 1
		self.K = 0
		self.num_instances = 0
		self.llist = 0
		self.clist = 0

		self.__A         = None
		self.__observed  = None
		self.__marginals = None

		self.__weightsref = weights # IMPORTANT! INCREASES REFCOUNT!

		self.prepare(True)

	def __len__(self):
		if self.destroyed:
			return 0
		return self.dimension

	def delete(self):
		if not self.destroyed:
			self.__set_ctx_state()
			self.destroyed = True
			L = ["MPT"+str(ctypes.addressof(self))+";", "DEL MPT;"]
			recode(L)
			run()

	def __set_ctx_state(self):
		write_register("MPT", ctypes.addressof(self))
		if not self.graph.destroyed:
			write_register("GPT", ctypes.addressof(self.graph))
		else:
			write_register("GPT", 0)
		write_register("REP", self.reparam)
		write_register("GRA", self.gtype)
		write_register("TREE", 0)

	def prepare(self, initOffsets = False):
		offset = 0
		self.obj = 0

		self.__woff = []

		for v in range(self.graph.nodes):
			self.__woff.append(offset)
			offset = offset + self.states[v]
			self.__ysum += self.states[v]
			
		for e in range(self.graph.edges):
			L = self.states[self.graph.edgelist[e][0]] * self.states[self.graph.edgelist[e][1]]
			self.__woff.append(offset)
			offset = offset + L
			
		self.__woff.append(offset)
		
		if initOffsets:
			self.__woffref = numpy.array(self.__woff, dtype=self.__idxtype)
			self.woffsets = ctypes.cast(self.__woffref.ctypes.data, ctypes.POINTER(self.__cidxtype))

	@property
	def dim(self):
		if self.destroyed:
			return 0
		if self.reparam == 12:
			return self.graph.nodes + self.graph.edges
		else:
			return self.dimension

	@property
	def time_frames(self):
		if self.destroyed:
			return 0
		return self.T

	@property
	def offsets(self):
		if self.destroyed:
			return numpy.array([])
		return numpy.ctypeslib.as_array(self.woffsets, shape = (self.offsetdimension, )).view(self.__idxtype)

	@property
	def weights(self):
		if self.destroyed:
			return numpy.array([])
		return numpy.ctypeslib.as_array(self.w, shape = (self.dim, )).view(self.__valtype)

	def slice_edge(self, e, A):
		if self.destroyed:
			return numpy.array([])
		#if self.reparam == 12:
		#	raise TypeError('ERROR: Edge slicing is only supported for overcomplete models')

		array_check(A,"A")

		if len(A) < self.dimension:
			raise TypeError('ERROR: A must be (at least) ' + str(self.dimension) + ' dimensional')
			
		c = self.__woff[self.graph.nodes]

		return A[int(self.__woff[self.graph.nodes + e]-c):int(self.__woff[self.graph.nodes + e + 1]-c)]

	def slice_edge_state(self, e, x, y, A):
		if self.destroyed:
			return 0

		array_check(A,"A")

		w = self.slice_edge(e, A)

		s = self.graph.edgelist[e][0]
		t = self.graph.edgelist[e][1]

		idx = int(x * self.states[t] + y)

		return w[idx:(idx + 1)]

	@property
	def statistics(self):
		if self.destroyed:
			return numpy.array([])
		if self.empirical_stats is None:
			return None
		res = numpy.ctypeslib.as_array(self.empirical_stats, shape = (self.fulldimension, )).view(self.__valtype) / self.num_instances
		res.flags.writeable = False
		return res[self.offsets[self.graph.nodes]:]
		
	@property
	def counts(self):
		if self.destroyed:
			return numpy.array([])
		if self.empirical_stats is None:
			return None
		res = numpy.ctypeslib.as_array(self.empirical_stats, shape = (self.fulldimension, )).view(self.__valtype)

		return res[self.offsets[self.graph.nodes]:]

	def phi(self, x):
		if self.destroyed:
			return numpy.array([])
		array_check(x,"x")

		if len(x) != self.graph.nodes:
			raise TypeError('ERROR: x must be ' + str(self.graph.nodes) + ' dimensional')

		phi_x = numpy.zeros(shape = (self.dim, ))

		if self.reparam == 12:
			for v in range(self.graph.nodes):
				if x[v] >= self.states[v]:
					TypeError('ERROR: Some values of x exceed the state space')

				phi_x[v] = int(x[v])

			for e in range(self.graph.edges):

				s = self.graph.edgelist[e][0]
				t = self.graph.edgelist[e][1]

				if x[s] >= self.states[s] or x[t] >= self.states[t]:
					TypeError('ERROR: Some values of x exceed the state space')

				phi_x[int(self.graph.nodes + e)] = int(x[s] * x[v])
		else:
			for e in range(self.graph.edges):

				s = self.graph.edgelist[e][0]
				t = self.graph.edgelist[e][1]

				if x[s] >= self.states[s] or x[t] >= self.states[t]:
					TypeError('ERROR: Some values of x exceed the state space')
					
				c = self.__woff[self.graph.nodes]

				idx = int(self.__woff[self.graph.nodes + e]-c + x[s] * self.states[t] + x[t])

				phi_x[idx] = 1

		return phi_x

	def score(self, x):
		if self.destroyed:
			return 0
		return numpy.inner(self.weights, self.phi(x))

	def edge_statespace(self, e):
		if self.destroyed:
			return numpy.array([])
		Xs = self.states[self.graph.edgelist[e][0]]
		Xt = self.states[self.graph.edgelist[e][1]]
		return numpy.array(list(itertools.product(range(Xs), range(Xt))))

	def __select_types(self, L):
		L.append("idx_t "+str(self.itype)+";")
		L.append("val_t "+str(self.vtype)+";")

	def save(self, filename):
		if self.destroyed:
			return
		self.__set_ctx_state()
		write_register("OVW", 1)
		L = []
		self.__select_types(L)
		L.append("MFN \"" + filename + "\";")
		L.append("STORE MPT;")
		recode(L)
		run()

	def __load_observed(self, observed, L):
		if observed is not None:
			array_check(observed,"observed")
			if len(observed.shape) == 1:
				observed = observed.reshape(1, len(observed))
			if len(observed.shape) != 2:
				raise ValueError('ERROR: observed must be 1 or 2 dimensional')

		data_ptr = ctypes.c_uint64(observed.ctypes.data)
		L.append("DEL DPT;")
		L.append("EDP " + str(data_ptr.value) + ";")
		L.append("NXX " + str(len(observed)) + ";")
		L.append("GPX " + str(len(observed) * len(observed[0]) * 2) + ";")
		L.append("LDX DPT;")

	def compute_statstics(self, data):
		if self.destroyed:
			return numpy.array([])

		L = []
		self.__select_types(L)
		self.__set_ctx_state()
		self.__load_observed(data, L)
		
		L.append("STATS;")
		
		recode(L)
		run()
		
		return self.statistics
		
	def predict(self, observed, progress_hook = 0, iterations = None, inference = InferenceType.belief_propagation):
		if self.destroyed:
			return numpy.array([])
		if not isinstance(inference, InferenceType):
			raise TypeError('ERROR: inference must be an instance of InferenceType Enum')

		L = []
		self.__select_types(L)
		self.__set_ctx_state()
		self.__load_observed(observed, L)

		if progress_hook != 0:
			f3 = prg_func(progress_hook)
			write_register("CBP", ctypes.c_uint64.from_buffer(f3).value)
		else:
			write_register("CBP", 0)

		if iterations is None:
			iterations = self.graph.nodes

		write_register("PGX", 0)
		write_register("MIL", iterations)
		write_register("INF", int(inference))

		L.append("PREDICT;")

		recode(L)
		run()

		return observed

	def sample(self, observed = None, num_samples = None, sampler = SamplerType.gibbs, progress_hook = 0, iterations = None, perturbation = 1, burn = 100, inference = InferenceType.belief_propagation):
		if self.destroyed:
			return numpy.array([])
		if not isinstance(sampler, SamplerType):
			raise TypeError('ERROR: sampler must be an instance of SamplerType Enum')

		if not ((observed is None) != (num_samples is None)):
			raise ValueError('ERROR: either observed or num_samples must be set (and not both)')

		L = []
		self.__select_types(L)
		self.__set_ctx_state()

		if observed is None:
			observed = numpy.full(shape = (num_samples, self.graph.nodes), fill_value = MISSING_VALUE, dtype = numpy.uint16)

		self.__load_observed(observed, L)

		if progress_hook != 0:
			f3 = prg_func(progress_hook)
			write_register("CBP", ctypes.c_uint64.from_buffer(f3).value)
		else:
			write_register("CBP", 0)

		if iterations is None:
			iterations = self.graph.nodes

		if sampler == SamplerType.perturb_and_map:
			write_register("PAM", integer_from_float(perturbation))
			write_register("MIL", iterations)
			write_register("INF", int(inference))

		elif sampler == SamplerType.gibbs:
			write_register("PAM", 0)
			write_register("GRE", burn) # unified burn-in and resamplings between two samples

		L.append("SAMPLE;")
		recode(L)
		run()

		return numpy.array(observed)


	def infer(self, observed = None, inference = InferenceType.belief_propagation, iterations = None, k = 3, epsilon = 0.000001):
		if self.destroyed:
			return numpy.array([]), numpy.nan
		if not isinstance(inference, InferenceType):
			raise TypeError('ERROR: inference must be an instance of InferenceType Enum')

		L = []
		self.__select_types(L)
		self.__set_ctx_state()

		if observed is not None:
			self.__load_observed(observed, L)
		else:
			L.append("DEL DPT;")
			L.append("DPT 0;")

		if iterations is None:
			iterations = self.graph.nodes
			
		write_register("EPL", integer_from_float(epsilon))

		write_register("KXX", k)
		write_register("MIL", iterations)
		write_register("INF", int(inference))

		L.append("INFER;")
		recode(L)
		run()

		P = ctypes.cast(int(read_register("PPT")), ctypes.POINTER(ctypes.c_double))

		res = numpy.array(numpy.ctypeslib.as_array(P, shape = (int(self.dimension + self.__ysum), )))
		#res.flags.writeable = False

		self.__observed  = observed
		self.__marginals = res
		self.__A         = float_from_integer(read_register("LNZ"))

		return self.__marginals, self.__A

	@property
	def MAP(self):
		if self.destroyed:
			return numpy.array([])
		x = numpy.full(shape = (1, self.graph.nodes), fill_value = MISSING_VALUE, dtype = numpy.uint16)
		self.predict(x)
		return x

	@property
	def LL(self):
		if self.destroyed:
			return 0
		N = self.num_instances
		if N == 0:
			return 0

		P, A = self.infer()
		return N*(numpy.inner(self.weights, self.statistics) - A)

	@property
	def BIC(self):
		if self.destroyed:
			return 0
		N = self.num_instances
		k = numpy.linalg.norm(self.weights, ord=0)
		P, A = self.infer()
		lnL = N*(numpy.inner(self.weights, self.statistics) - A)
		return numpy.log(N)*k - 2*lnL

	@property
	def AIC(self):
		if self.destroyed:
			return 0
		N = self.num_instances
		k = numpy.linalg.norm(self.weights, ord=0)
		P, A = self.infer()
		lnL = N*(numpy.inner(self.weights, self.statistics) - A)
		return 2*k - 2*lnL

	@property
	def graph(self):
		if (self.__LOCAL_G is None) or (self.__OLD_G != self.G):
			self.__OLD_G = self.G
			temp = None
			if self.gtype == 11:
				temp = ctypes.cast(self.G, ctypes.POINTER(STGraph0)).contents
			else:
				temp = ctypes.cast(self.G, ctypes.POINTER(Graph0)).contents
			self.__LOCAL_G = ctypes.cast(self.G, ctypes.POINTER(temp.get_type())).contents
		return self.__LOCAL_G

	@property
	def base_graph(self):
		if self.destroyed:
			return None
		self.__set_ctx_state()
		L = []
		self.__select_types(L)
		L.append("BASEGRAPH;")
		recode(L)
		run()
		G = ctypes.cast(read_register("RES"), ctypes.POINTER(Graph0)).contents.cast()
		return G

	@property
	def states(self):
		if self.destroyed:
			return numpy.array([])
		res = numpy.ctypeslib.as_array(self.Y, shape = (self.graph.nodes, ))
		return res

	def probv(self, v, x):
		if self.destroyed:
			return 0
		if self.__marginals is None:
			raise RuntimeError('ERROR: you must call infer first')

		return self.__marginals[int(self.__woff[v]+x)]

	def probe(self, e, x, y):
		if self.destroyed:
			return 0
		if self.__marginals is None:
			raise RuntimeError('ERROR: you must call infer first')
			
		#s = self.graph.edgelist[e][0]
		t = self.graph.edgelist[e][1]

		return self.__marginals[int(self.__woff[self.graph.nodes + e] + x * self.states[t] + y)] 

	def prob(self, s, x, y = None):
		if self.destroyed:
			return 0
		if self.__marginals is None:
			raise RuntimeError('ERROR: you must call infer first')

		if y is None:
			return self.probv(s,x)

		return self.probe(s,x,y)

#		a0 = numpy.bincount(numpy.where(self.graph.edgelist==[v,w])[0])
#		a1 = numpy.bincount(numpy.where(self.graph.edgelist==[w,v])[0])
#
#		b0 = numpy.max(a0)
#		b1 = numpy.max(a1)
#
#		if b0 != 2 and b1 != 2:
#			return self.prob(v,x) * self.prob(w,y)
#
#		v0 = v
#		v1 = w
#		x0 = x
#		x1 = y
#
#		if b0 == 2:
#			e = numpy.argmax(a0)
#		else:
#			e = numpy.argmax(a1)
#			v0 = w
#			v1 = v
#			x0 = y
#			x1 = x
#
#		return self.__marginals[int(self.__woff[self.graph.nodes + e] + x0 * self.states[x1] + x1)]

	def export_onnx(self,fname,probmodel=False):
		from onnx import helper, TensorProto
		import onnxmltools

# INT8 to INT32 seem to by unsupported by onnx
#		if self.__idxtype == numpy.uint8:
#			ITYPE = TensorProto.INT8
#		elif self.__idxtype == numpy.uint16:
#			ITYPE = TensorProto.INT16
#		elif self.__idxtype == numpy.uint32:
#			ITYPE = TensorProto.INT32
		if self.__idxtype == numpy.uint64:
			ITYPE = TensorProto.INT64
		else:
			raise TypeError('Index type '+str(self.__idxtype)+' not supported for ONNX export.')

		if self.__valtype == numpy.float32:
			DTYPE = TensorProto.FLOAT
		elif self.__valtype == numpy.float64:
			DTYPE = TensorProto.DOUBLE
		else:
			raise TypeError('Value type '+str(self.__idxtype)+' not supported for ONNX export.')

		################################################################################
		# INIT
		################################################################################

		Ne  = {}
		NeE = {}
		for v in range(self.graph.nodes):
			Ne[v]  = []
			NeE[v] = []

		ONNX_OP_LIST = []

		MAPv   = []
		PROBv  = []

		################################################################################
		# MODEL WEIGHTS, ONE ONNX-NODE FOR EACH EDGE WEIGHT VECTOR
		################################################################################

		for e in range(self.graph.edges):

			s = self.graph.edgelist[e][0]
			t = self.graph.edgelist[e][1]
			
		 	# populate neighborhoods
			if not t in Ne[s]:
				Ne[s].append(t)
				NeE[s].append(e)
			if not s in Ne[t]:
				Ne[t].append(s)
				NeE[t].append(e)
			
			Ys = int(self.states[s])
			Yt = int(self.states[t])
			
			WEIGHTSid = 'WEIGHTS_'+str(e)
			WEIGHTS = helper.make_tensor_value_info(WEIGHTSid, DTYPE, shape=(Ys,Yt))	
			WEIGHTSval = self.slice_edge(e,self.weights).reshape(Ys,Yt)
			WEIGHTSn = helper.make_node(
				'Constant',
				inputs=[],
				outputs=[WEIGHTSid],
			 	value=helper.make_tensor(
					name=WEIGHTSid+'_content',
					data_type=DTYPE,
					dims=WEIGHTSval.shape,
					vals=WEIGHTSval.flatten(),
				),
			)
			ONNX_OP_LIST.append(WEIGHTSn)
			
			EXPWEIGHTSid = 'EXPWEIGHTS_'+str(s)+'_'+str(t)
			EXPWEIGHTS = helper.make_tensor_value_info(EXPWEIGHTSid, DTYPE, shape=(Ys,Yt))
			EXPWEIGHTSn = helper.make_node(
				'Exp',
				inputs=[WEIGHTSid],
				outputs=[EXPWEIGHTSid],
			)
			ONNX_OP_LIST.append(EXPWEIGHTSn)
			
			tEXPWEIGHTSid = 'EXPWEIGHTS_'+str(t)+'_'+str(s)
			tEXPWEIGHTS = helper.make_tensor_value_info(tEXPWEIGHTSid, DTYPE, shape=(Yt,Ys))
			tEXPWEIGHTSn = helper.make_node(
				'Transpose',
				inputs=[EXPWEIGHTSid],
				outputs=[tEXPWEIGHTSid],
			)
			ONNX_OP_LIST.append(tEXPWEIGHTSn)

		CONSTANT_ONEid = 'CONSTANT_ONE'
		CONSTANT_ONE  = helper.make_tensor_value_info(CONSTANT_ONEid, ITYPE, shape=(1,))
		CONSTANT_ONEv = numpy.array([1],dtype=self.__idxtype)
		CONSTANT_ONEn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[CONSTANT_ONEid],
		 	value=helper.make_tensor(
				name=CONSTANT_ONEid+'_content',
				data_type=ITYPE,
				dims=CONSTANT_ONEv.shape,
				vals=CONSTANT_ONEv.flatten(),
			),
		)
		ONNX_OP_LIST.append(CONSTANT_ONEn)

		ONECOLD_VALUESid = 'ONECOLD_VALUES'
		ONECOLD_VALUES = helper.make_tensor_value_info(ONECOLD_VALUESid, ITYPE, shape=(2,))
		ONECOLD_VALUESvals = numpy.array([1,0],dtype=self.__idxtype)
		ONECOLD_VALUESn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[ONECOLD_VALUESid],
		 	value=helper.make_tensor(
				name=ONECOLD_VALUESid+'_content',
				data_type=ITYPE,
				dims=ONECOLD_VALUESvals.shape,
				vals=ONECOLD_VALUESvals.flatten(),
			),
		)
		ONNX_OP_LIST.append(ONECOLD_VALUESn)

		ONEHOT_VALUESid = 'ONEHOT_VALUES'
		ONEHOT_VALUES = helper.make_tensor_value_info(ONEHOT_VALUESid, ITYPE, shape=(2,))
		ONEHOT_VALUESvals = numpy.array([0,1],dtype=self.__idxtype)
		ONEHOT_VALUESn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[ONEHOT_VALUESid],
		 	value=helper.make_tensor(
				name=ONEHOT_VALUESid+'_content',
				data_type=ITYPE,
				dims=ONEHOT_VALUESvals.shape,
				vals=ONEHOT_VALUESvals.flatten(),
			),
		)
		ONNX_OP_LIST.append(ONEHOT_VALUESn)
			
		for v in range(self.graph.nodes):
			nn = len(Ne[v])

			NNid = 'NN_'+str(v)
			NN = helper.make_tensor_value_info(NNid, ITYPE, shape=(1,1))
			NNval = numpy.array([nn],dtype=self.__idxtype)
			NNn = helper.make_node(
				'Constant',
				inputs=[],
				outputs=[NNid],
			 	value=helper.make_tensor(
					name=NNid+'_content',
					data_type=ITYPE,
					dims=NNval.shape,
					vals=NNval.flatten(),
				),
			)
			ONNX_OP_LIST.append(NNn)
			
			NUMid = 'NUM_'+str(v)
			NUM = helper.make_tensor_value_info(NUMid, ITYPE, shape=(1,1))
			NUMval = numpy.array([v],dtype=self.__idxtype)
			NUMn = helper.make_node(
				'Constant',
				inputs=[],
				outputs=[NUMid],
			 	value=helper.make_tensor(
					name=NUMid+'_content',
					data_type=ITYPE,
					dims=NUMval.shape,
					vals=NUMval.flatten(),
				),
			)
			ONNX_OP_LIST.append(NUMn)

			for iw in range(nn):
				w = Ne[v][iw]
				IDXid = 'IDX_'+str(v)+'_'+str(w)
				IDX = helper.make_tensor_value_info(IDXid, ITYPE, shape=(1,))
				IDXval = numpy.array([iw],dtype=self.__idxtype)
				IDXn = helper.make_node(
					'Constant',
					inputs=[],
					outputs=[IDXid],
				 	value=helper.make_tensor(
						name=IDXid+'_content',
						data_type=ITYPE,
						dims=IDXval.shape,
						vals=IDXval.flatten(),
					),
				)
				ONNX_OP_LIST.append(IDXn)

				FMASKED_NEIGHBORSid = 'FMASKED_NEIGHBORS_'+str(v)+'_'+str(w)
				FMASKED_NEIGHBORS = helper.make_tensor_value_info(FMASKED_NEIGHBORSid, ITYPE, shape=(nn,1))
				FMASKED_NEIGHBORSn = helper.make_node(
					'OneHot',
					inputs=[IDXid, NNid, ONECOLD_VALUESid],
					outputs=[FMASKED_NEIGHBORSid],
					axis=0,
				)
				ONNX_OP_LIST.append(FMASKED_NEIGHBORSn)
				
				MASKED_NEIGHBORSid = 'MASKED_NEIGHBORS_'+str(v)+'_'+str(w)
				MASKED_NEIGHBORS = helper.make_tensor_value_info(FMASKED_NEIGHBORSid, DTYPE, shape=(nn,1))
				MASKED_NEIGHBORSn = helper.make_node(
					'Cast',
					inputs=[FMASKED_NEIGHBORSid],
					outputs=[MASKED_NEIGHBORSid],
					to=DTYPE,
				)
				ONNX_OP_LIST.append(MASKED_NEIGHBORSn)

		NUMid = 'NUM_'+str(self.graph.nodes)
		NUM = helper.make_tensor_value_info(NUMid, ITYPE, shape=(1,1))
		NUMval = numpy.array([self.graph.nodes],dtype=self.__idxtype)
		NUMn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[NUMid],
		 	value=helper.make_tensor(
				name=NUMid+'_content',
				data_type=ITYPE,
				dims=NUMval.shape,
				vals=NUMval.flatten(),
			),
		)
		ONNX_OP_LIST.append(NUMn)
		################################################################################
		# INPUT (OBSERVED) VALUES
		################################################################################

		OBSERVED = helper.make_tensor_value_info('observed_data', ITYPE, shape=(self.graph.nodes,))

		################################################################################
		# INITIAL OUTGOING LOG-MESSAGES v -> w, STATE SPACES, AND OBS-VECTORS
		################################################################################

#		DBG_SLICES = []

		for v in range(self.graph.nodes):
			Yv = int(self.states[v])
			for w in Ne[v]:
				INITIALMSGid = 'LOGMSG_'+str(w)+'_'+str(v)+'_0'
				INITIALMSG = helper.make_tensor_value_info(INITIALMSGid, DTYPE, shape=(Yv,1))
				INITIALMSGval = numpy.zeros(Yv).reshape(Yv,1).astype(self.__valtype)
				INITIALMSGn = helper.make_node(
					'Constant',
					inputs=[],
					outputs=[INITIALMSGid], # all messages from w to v in iter 0
				 	value=helper.make_tensor(
						name=INITIALMSGid+'_content',
						data_type=DTYPE,
						dims=INITIALMSGval.shape,
						vals=INITIALMSGval.flatten(),
					),
				)
				ONNX_OP_LIST.append(INITIALMSGn)

			XVid = 'XV'+str(v)
			XV  = helper.make_tensor_value_info(XVid, ITYPE, shape=(1,))
			XVv = numpy.array([Yv],dtype=self.__idxtype)
			XVn = helper.make_node(
				'Constant',
				inputs=[],
				outputs=[XVid],
			 	value=helper.make_tensor(
					name=XVid+'_content',
					data_type=ITYPE,
					dims=XVv.shape,
					vals=XVv.flatten(),
				),
			)
			ONNX_OP_LIST.append(XVn)

			VERTEX_SLICEid = 'OBSERVED_VALUE_'+str(v)
			VERTEX_SLICE = helper.make_tensor_value_info(VERTEX_SLICEid, ITYPE, shape=(Yv,1))
			VERTEX_SLICEn = helper.make_node(
				'Slice',
				inputs=['observed_data','NUM_'+str(v),'NUM_'+str(v+1)],
				outputs=[VERTEX_SLICEid],
			)
			ONNX_OP_LIST.append(VERTEX_SLICEn)
			
			FIS_NOT_OBSERVEDid = 'FIS_NOT_OBSERVED_'+str(v)
			FIS_NOT_OBSERVED = helper.make_tensor_value_info(FIS_NOT_OBSERVEDid, ITYPE, shape=(1,1))
			FIS_NOT_OBSERVEDn = helper.make_node(
				'GreaterOrEqual',
				inputs=[VERTEX_SLICEid,XVid],
				outputs=[FIS_NOT_OBSERVEDid],
			)
			ONNX_OP_LIST.append(FIS_NOT_OBSERVEDn)
			
			IS_NOT_OBSERVEDid = 'IS_NOT_OBSERVED_'+str(v)
			IS_NOT_OBSERVED = helper.make_tensor_value_info(IS_NOT_OBSERVEDid, DTYPE, shape=(1,1))
			IS_NOT_OBSERVEDn = helper.make_node(
				'Cast',
				inputs=[FIS_NOT_OBSERVEDid],
				outputs=[IS_NOT_OBSERVEDid],
				to=DTYPE,
			)
			ONNX_OP_LIST.append(IS_NOT_OBSERVEDn)
			
			FOBSVECid = 'FOBSERVATION_VECTOR_'+str(v)
			FOBSVEC = helper.make_tensor_value_info(FOBSVECid, ITYPE, shape=(Yv,1))
			FOBSVECn = helper.make_node(
				'OneHot',
				inputs=[VERTEX_SLICEid, XVid, ONEHOT_VALUESid],
				outputs=[FOBSVECid],
				axis=0,
			)
			ONNX_OP_LIST.append(FOBSVECn)
			
			tFOBSVECid = 'tFOBSERVATION_VECTOR_'+str(v)
			tFOBSVEC = helper.make_tensor_value_info(tFOBSVECid, ITYPE, shape=(1,Yv))
			tFOBSVECn = helper.make_node(
				'Transpose',
				inputs=[FOBSVECid],
				outputs=[tFOBSVECid],
			)
			ONNX_OP_LIST.append(tFOBSVECn)

			OBSVECid = 'OBSERVATION_VECTOR_'+str(v)
			OBSVEC = helper.make_tensor_value_info(OBSVECid, DTYPE, shape=(1,Yv))
			OBSVECn = helper.make_node(
				'Cast',
				inputs=[tFOBSVECid],
				outputs=[OBSVECid],
				to=DTYPE,
			)
			ONNX_OP_LIST.append(OBSVECn)

		################################################################################
		# Unroll LBP
		################################################################################

		ITERS=self.graph.edges

		for I in range(ITERS):
			for v in range(self.graph.nodes):
				Yv = int(self.states[v])
				nn = len(Ne[v])

				# concatenate incoming log-message vector into on large matrix
				IN = ['LOGMSG_'+str(w)+'_'+str(v)+'_'+str(I) for w in Ne[v]]
				
				INCOMINGSid = 'incoming_'+str(v)+'_'+str(I)
				INCOMINGS = helper.make_tensor_value_info(INCOMINGSid, DTYPE, shape=(Yv,nn))
				INCOMINGSn = helper.make_node(
					'Concat',
					inputs=IN,
					outputs=[INCOMINGSid],
					axis=1,
				)
				ONNX_OP_LIST.append(INCOMINGSn)
				
				# messages from v to w
				for iw in range(nn):
					w = Ne[v][iw]
					e = NeE[v][iw]
					Yw = int(self.states[w])

					MSGSUMid = 'MSGSUM_'+str(v)+'_'+str(w)+'_'+str(I) # sum of incoming log-messages not from w
					MSGSUM = helper.make_tensor_value_info(MSGSUMid, DTYPE, shape=(Yv,1))
					MSGSUMn = helper.make_node(
						'Gemm',
						inputs=[INCOMINGSid,'MASKED_NEIGHBORS_'+str(v)+'_'+str(w)],
						outputs=[MSGSUMid],
					)
					ONNX_OP_LIST.append(MSGSUMn)
					
					EXPMSGSUMid = 'EXPMSGSUM_'+str(v)+'_'+str(w)+'_'+str(I)
					EXPMSGSUM = helper.make_tensor_value_info(EXPMSGSUMid, DTYPE, shape=(Yv,1))
					EXPMSGSUMn = helper.make_node(
						'Exp',
						inputs=[MSGSUMid],
						outputs=[EXPMSGSUMid],
					)
					ONNX_OP_LIST.append(EXPMSGSUMn)

					tEXPMSGSUMid = 'tEXPMSGSUM_'+str(v)+'_'+str(w)+'_'+str(I)
					tEXPMSGSUM = helper.make_tensor_value_info(tEXPMSGSUMid, DTYPE, shape=(1,Yv))
					tEXPMSGSUMn = helper.make_node(
						'Transpose',
						inputs=[EXPMSGSUMid],
						outputs=[tEXPMSGSUMid],
					)
					ONNX_OP_LIST.append(tEXPMSGSUMn)
					
					###################################
					# Incorporate Observations
					###################################
					
					StEXPMSGSUMid = 'StEXPMSGSUM_'+str(v)+'_'+str(w)+'_'+str(I)
					StEXPMSGSUM = helper.make_tensor_value_info(StEXPMSGSUMid, DTYPE, shape=(1,Yv))
					StEXPMSGSUMn = helper.make_node(
						'Mul',
						inputs=[tEXPMSGSUMid,'IS_NOT_OBSERVED_'+str(v)],
						outputs=[StEXPMSGSUMid],
					)
					ONNX_OP_LIST.append(StEXPMSGSUMn)

					INOBSVECid = 'INOBS_'+str(v)+'_'+str(w)+'_'+str(I)
					INOBSVEC = helper.make_tensor_value_info(INOBSVECid, DTYPE, shape=(1,Yv))
					INOBSVECn = helper.make_node(
						'Add',
						inputs=[StEXPMSGSUMid,'OBSERVATION_VECTOR_'+str(v)],
						outputs=[INOBSVECid],
					)
					ONNX_OP_LIST.append(INOBSVECn)
					
					###################################
					
					MULMSGid = 'MULMSG_'+str(v)+'_'+str(w)+'_'+str(I)
					MULMSG = helper.make_tensor_value_info(MULMSGid, DTYPE, shape=(Yw,Yv))
					MULMSGn = helper.make_node(
						'Mul',
						inputs=['EXPWEIGHTS_'+str(w)+'_'+str(v),INOBSVECid],
						outputs=[MULMSGid],
					)
					ONNX_OP_LIST.append(MULMSGn)
					
					if probmodel:

						OUTMSGid = 'MSG_'+str(v)+'_'+str(w)+'_'+str(I)
						OUTMSG = helper.make_tensor_value_info(OUTMSGid, DTYPE, shape=(Yw,1))
						OUTMSGn = helper.make_node(
							'ReduceSum',
							inputs=[MULMSGid,CONSTANT_ONEid],
							outputs=[OUTMSGid],
						)
						ONNX_OP_LIST.append(OUTMSGn)
						
					else:
						# The current runtime does not support ReduceMax with DTYPE
						
						OUTMSG1id = 'MSG1_'+str(v)+'_'+str(w)+'_'+str(I)
						OUTMSG1 = helper.make_tensor_value_info(OUTMSG1id, DTYPE, shape=(Yw,Yv))
						OUTMSG1n = helper.make_node(
							'Cast',
							inputs=[MULMSGid],
							outputs=[OUTMSG1id],
							to=TensorProto.FLOAT,
						)
						ONNX_OP_LIST.append(OUTMSG1n)
						
						OUTMSG1bid = 'MSG1b_'+str(v)+'_'+str(w)+'_'+str(I)
						OUTMSG1b = helper.make_tensor_value_info(OUTMSG1bid, DTYPE, shape=(Yw,1))
						OUTMSG1bn = helper.make_node(
							'ReduceMax',
							inputs=[OUTMSG1id],
							outputs=[OUTMSG1bid],
							axes=[1],
						)
						ONNX_OP_LIST.append(OUTMSG1bn)

						OUTMSGid = 'MSG_'+str(v)+'_'+str(w)+'_'+str(I)
						OUTMSG = helper.make_tensor_value_info(OUTMSGid, DTYPE, shape=(Yw,1))
						OUTMSGn = helper.make_node(
							'Cast',
							inputs=[OUTMSG1bid],
							outputs=[OUTMSGid],
							to=DTYPE,
						)
						ONNX_OP_LIST.append(OUTMSGn)
					
					ZOUTMSGid = 'ZMSG_'+str(v)+'_'+str(w)+'_'+str(I)
					ZOUTMSG = helper.make_tensor_value_info(ZOUTMSGid, DTYPE, shape=(1,))
					ZOUTMSGn = helper.make_node(
						'ReduceSum',
						inputs=[OUTMSGid],
						outputs=[ZOUTMSGid],
						keepdims=0,
					)
					ONNX_OP_LIST.append(ZOUTMSGn)

					NORMOUTMSGid = 'NORMMSG_'+str(v)+'_'+str(w)+'_'+str(I)
					NORMOUTMSG = helper.make_tensor_value_info(NORMOUTMSGid, DTYPE, shape=(Yw,1))
					NORMOUTMSGn = helper.make_node(
						'Div',
						inputs=[OUTMSGid,ZOUTMSGid],
						outputs=[NORMOUTMSGid],
					)
					ONNX_OP_LIST.append(NORMOUTMSGn)
					
					FINALOUTMSGid = 'LOGMSG_'+str(v)+'_'+str(w)+'_'+str(I+1)
					FINALOUTMSG = helper.make_tensor_value_info(FINALOUTMSGid, DTYPE, shape=(Yw,1))
					FINALOUTMSGn = helper.make_node(
						'Log',
						inputs=[NORMOUTMSGid],
						outputs=[FINALOUTMSGid],
					)
					ONNX_OP_LIST.append(FINALOUTMSGn)

		################################################################################
		# VERTEX MARGINALS
		################################################################################

		for v in range(self.graph.nodes):
			Yv = int(self.states[v])
			nn = len(Ne[v])

			# concatenate incoming log-message vector into on large matrix
			IN = ['LOGMSG_'+str(w)+'_'+str(v)+'_'+str(ITERS) for w in Ne[v]]
			
			INCOMINGSid = 'incoming_'+str(v)+'_'+str(ITERS)
			INCOMINGS = helper.make_tensor_value_info(INCOMINGSid, DTYPE, shape=(Yv,nn))
			INCOMINGSn = helper.make_node(
				'Concat',
				inputs=IN,
				outputs=[INCOMINGSid],
				axis=1,
			)
			ONNX_OP_LIST.append(INCOMINGSn)
			
			INSUMid = 'sum_incoming_'+str(v)
			INSUM = helper.make_tensor_value_info(INSUMid, DTYPE, shape=(Yv,))
			INSUMn = helper.make_node(
				'ReduceSum',
				inputs=[INCOMINGSid, CONSTANT_ONEid],
				outputs=[INSUMid],
				keepdims=0,
			)
			ONNX_OP_LIST.append(INSUMn)
			
			ExpINSUMid = 'exp_sum_incoming_'+str(v)
			ExpINSUM = helper.make_tensor_value_info(ExpINSUMid, DTYPE, shape=(Yv,))
			ExpINSUMn = helper.make_node(
				'Exp',
				inputs=[INSUMid],
				outputs=[ExpINSUMid],
			)
			ONNX_OP_LIST.append(ExpINSUMn)
			
			###################################
			# Incorporate Observations
			###################################
					
			SINSUMid = 'switched_exp_sum_incoming_'+str(v)
			SINSUM = helper.make_tensor_value_info(SINSUMid, DTYPE, shape=(Yv,))
			SINSUMn = helper.make_node(
				'Mul',
				inputs=[ExpINSUMid,'IS_NOT_OBSERVED_'+str(v)],
				outputs=[SINSUMid],
			)
			ONNX_OP_LIST.append(SINSUMn)

			MSINSUMid = 'masked_switched_exp_sum_incoming_'+str(v)
			MSINSUM = helper.make_tensor_value_info(INOBSVECid, DTYPE, shape=(Yv,))
			MSINSUMn = helper.make_node(
				'Add',
				inputs=[SINSUMid,'OBSERVATION_VECTOR_'+str(v)],
				outputs=[MSINSUMid],
			)
			ONNX_OP_LIST.append(MSINSUMn)
					
			###################################
			
			ZExpINSUMid = 'Zexp_sum_incoming_'+str(v)
			ZExpINSUM = helper.make_tensor_value_info(ZExpINSUMid, DTYPE, shape=(1,))
			ZExpINSUMn = helper.make_node(
				'ReduceSum',
				inputs=[MSINSUMid],
				outputs=[ZExpINSUMid],
				keepdims=0,
			)
			ONNX_OP_LIST.append(ZExpINSUMn)
			
			MARGINALSid = 'marginals_'+str(v)
			MARGINALS = helper.make_tensor_value_info(MARGINALSid, DTYPE, shape=(Yv,))
			MARGINALSn = helper.make_node(
				'Div',
				inputs=[MSINSUMid,ZExpINSUMid],
				outputs=[MARGINALSid],
			)
			ONNX_OP_LIST.append(MARGINALSn)
			
			rsMARGINALSid = 'rs_marginals_'+str(v)
			rsMARGINALS = helper.make_tensor_value_info(rsMARGINALSid, DTYPE, shape=(Yv,))
			rsMARGINALSn = helper.make_node(
				'Reshape',
				inputs=[MARGINALSid,'XV'+str(v)],
				outputs=[rsMARGINALSid],
			)
			ONNX_OP_LIST.append(rsMARGINALSn)
			
			PROBv.append(rsMARGINALSid)
#			DBG_SLICES.append(MARGINALSid)
			
			AMAXMARGINALSid = 'argmax_marginals_'+str(v)
			AMAXMARGINALS = helper.make_tensor_value_info(AMAXMARGINALSid, ITYPE, shape=(1,))
			AMAXMARGINALSn = helper.make_node(
				'ArgMax',
				inputs=[MARGINALSid],
				outputs=[AMAXMARGINALSid],
				axis=1,
				keepdims=0,
				select_last_index=1,
			)
			ONNX_OP_LIST.append(AMAXMARGINALSn)
			
			MAPv.append(AMAXMARGINALSid)

		################################################################################
		# OUTPUT
		################################################################################

		if probmodel:
			PROBid = 'PROB'
			s = numpy.sum(self.states,dtype=self.__idxtype)
			OUTPUT = helper.make_tensor_value_info(PROBid, DTYPE, shape=(int(s),))
			PROBn = helper.make_node(
				'Concat',
				inputs=PROBv,
				outputs=[PROBid],
				axis=0,
			)
			ONNX_OP_LIST.append(PROBn)

		else:
			MAPid = 'MAP'
			OUTPUT = helper.make_tensor_value_info(MAPid, ITYPE, shape=(self.graph.nodes,))
			MAPn = helper.make_node(
				'Concat',
				inputs=MAPv,
				outputs=[MAPid],
				axis=0,
			)
			ONNX_OP_LIST.append(MAPn)
			
#		DBGid = 'DBG'
#		DBG = helper.make_tensor_value_info(DBGid, DTYPE, shape=(8,3))
#		DBGn = helper.make_node(
#			'Concat',
#			inputs=DBG_SLICES,
#			outputs=[DBGid],
#			axis=0,
#		)
#		ONNX_OP_LIST.append(DBGn)

		graph_def = helper.make_graph(
			ONNX_OP_LIST,
			'unrolled_pxpy_model',
			[OBSERVED],
			[OUTPUT]
		)

		info = {
			"n": self.graph.nodes,
			"N": self.num_instances,
			"LL": self.LL,
			"Y": self.states.tolist()
		}

		onnxmodel = helper.make_model(graph_def, producer_name='pxpy', producer_version=str(version()), model_version=1, doc_string=json.dumps(info))
		onnxmltools.utils.save_model(onnxmodel, fname)

	def export_onnx_marginal_inference(self,filename):
		self.export_onnx(filename,True)
		
	def export_onnx_MAP_inference(self,filename):
		self.export_onnx(filename,False)


class Model0(ctypes.Structure):

	_fields_ = [("itype", ctypes.c_uint8), ("vtype", ctypes.c_uint8)]
			
	@property
	def __cvaltype(self):
		if self.vtype == 0:
			return ctypes.c_uint8
		elif self.vtype == 1:
			return ctypes.c_uint16
		elif self.vtype == 2:
			return ctypes.c_uint32
		elif self.vtype == 3:
			return ctypes.c_uint64
		elif self.vtype == 4:
			return ctypes.c_float
		else:
			return ctypes.c_double
			
	@property
	def __cidxtype(self):
		if self.itype == 0:
			return ctypes.c_uint8
		elif self.itype == 1:
			return ctypes.c_uint16
		elif self.itype == 2:
			return ctypes.c_uint32
		else:
			return ctypes.c_uint64

	def get_fields(self):
		# Notice: G and H have "ponter length" (size_t) which is assumed to be 64-bit
		return [("itype", ctypes.c_uint8), ("vtype", ctypes.c_uint8), ("from_file", ctypes.c_bool), ("from_python", ctypes.c_bool), ("G", ctypes.c_uint64), ("H", ctypes.c_uint64), ("w", ctypes.POINTER(self.__cvaltype)), ("empirical_stats", ctypes.POINTER(self.__cvaltype)), ("Y", ctypes.POINTER(self.__cidxtype)), ("woffsets", ctypes.POINTER(self.__cidxtype)), ("__Ynames", ctypes.POINTER(self.__cidxtype)), ("__Xnames", ctypes.POINTER(self.__cidxtype)), ("dimension", self.__cidxtype), ("offsetdimension", self.__cidxtype), ("fulldimension", self.__cidxtype), ("gtype", self.__cidxtype), ("T", self.__cidxtype), ("reparam", self.__cidxtype), ("K", self.__cidxtype), ("num_instances", self.__cidxtype), ("llist", self.__cidxtype), ("clist", self.__cidxtype)]
		
	def get_type(self):
		return type("Model", (Model_incomplete,), {"_fields_": self.get_fields()})

	def cast(self):
		self.__class__ = self.get_type()
		return self

class progress_t_base(ctypes.Structure):

	@property
	def __idxtype(self):
		if self.itype == 0:
			return numpy.uint8
		elif self.itype == 1:
			return numpy.uint16
		elif self.itype == 2:
			return numpy.uint32
		else:
			return numpy.uint64
			
	@property
	def __valtype(self):
		if self.vtype == 0:
			return numpy.uint8
		elif self.vtype == 1:
			return numpy.uint16
		elif self.vtype == 2:
			return numpy.uint32
		elif self.vtype == 3:
			return numpy.uint64
		elif self.vtype == 4:
			return numpy.float32
		else:
			return numpy.float64
			
	@property
	def obj(self):
		if self.is_int != 0:
			return self._obj / 255.0
		else:
			return self._obj

	@property
	def best_obj(self):
		if self.is_int != 0:
			return self._best_obj / 255.0
		else:
			return self._best_obj

	@property
	def model(self):
		mod = self._model.contents
		mod.prepare()
		mod.obj = self.obj
		return mod

	@property
	def weights(self):
		return numpy.ctypeslib.as_array(self._w, shape = (self.dim, )).view(self.__valtype)

	@property
	def weights_extrapolation(self):
		return numpy.ctypeslib.as_array(self._e, shape = (self.dim, )).view(self.__valtype)
		
	@property
	def best_weights(self):
		return numpy.ctypeslib.as_array(self._best_w, shape = (self.dim, )).view(self.__valtype)

	@property
	def gradient(self):
		return numpy.ctypeslib.as_array(self._g, shape = (self.dim, )).view(self.__valtype)


class progress_t0(ctypes.Structure):

	_fields_ = [("itype", ctypes.c_uint8), ("vtype", ctypes.c_uint8)]
			
	@property
	def __cvaltype(self):
		if self.vtype == 0:
			return ctypes.c_uint8
		elif self.vtype == 1:
			return ctypes.c_uint16
		elif self.vtype == 2:
			return ctypes.c_uint32
		elif self.vtype == 3:
			return ctypes.c_uint64
		elif self.vtype == 4:
			return ctypes.c_float
		else:
			return ctypes.c_double
			
	@property
	def __cidxtype(self):
		if self.itype == 0:
			return ctypes.c_uint8
		elif self.itype == 1:
			return ctypes.c_uint16
		elif self.itype == 2:
			return ctypes.c_uint32
		else:
			return ctypes.c_uint64

	def get_fields(self):
		return [("itype", ctypes.c_uint8), ("vtype", ctypes.c_uint8), ("_obj", self.__cvaltype), ("norm", self.__cvaltype), ("stepsize", self.__cvaltype), ("min_stepsize", self.__cvaltype), ("lambda_proximal", self.__cvaltype), ("lambda_regularization", self.__cvaltype), ("iteration", self.__cidxtype), ("max_iterations", self.__cidxtype), ("dim", self.__cidxtype), ("_w", ctypes.POINTER(self.__cvaltype)), ("_g", ctypes.POINTER(self.__cvaltype)), ("_e", ctypes.POINTER(self.__cvaltype)), ("is_int", ctypes.c_bool), ("_best_obj", self.__cvaltype), ("best_norm", self.__cvaltype), ("_best_w", ctypes.POINTER(self.__cvaltype)), ("value_bytes", self.__cidxtype), ("_model", ctypes.POINTER(Model0))]
		
	def get_type(self):
		return type("progress_t", (progress_t_base,), {"_fields_": self.get_fields()})
		
	def cast(self):
		self.__class__ = self.get_type()
		return self


#	def status(self):
#		P,A				= self.infer()
#		mu_hat			= P[:self.dimension]
#		mu_tilde		= self.statistics
#		weig_nrm_2		= numpy.linalg.norm(self.weights)
#		grad_nrm_inf	= numpy.max(numpy.abs(a-b))
#
#		res = numpy.array([-self.LL / self.num_instances, grad_nrm_inf, weig_nrm_2])
#		
#		return res

if platform == "win32":
	opt_func = ctypes.WINFUNCTYPE(None, ctypes.POINTER(progress_t0))
	prg_func = ctypes.WINFUNCTYPE(None, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p)
else:
	opt_func = ctypes.CFUNCTYPE(None, ctypes.POINTER(progress_t0))
	prg_func = ctypes.CFUNCTYPE(None, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p)


ctx = ctypes.c_uint64(lib.create_ctx())

def write_register(name, val):
	l = len(name)
	buff = ctypes.create_string_buffer(l + 1)
	buff.value = name.encode('utf-8')
	ptr = (ctypes.c_char_p)(ctypes.addressof(buff))
	return lib.ctx_write_reg(ctx, ptr, val)

write_register("SEED", int(round(time.time() * 1000)))
write_register("EXT0", EXTINF)

def squared_l2_regularization(state_p):
	state = state_p.contents.cast()
	numpy.copyto(state.gradient, state.gradient + 2.0 * state.lambda_regularization * state.weights)
	state.norm = numpy.linalg.norm(state.gradient, ord=numpy.inf)

	if state.iteration == 0:
		state.min_stepsize = 1.0/(1.0/state.min_stepsize + 2.0 * state.lambda_regularization) # TODO: Add this fact to the book!

def prox_l1(state_p):
	state = state_p.contents.cast()
	l = state.lambda_proximal * state.stepsize

	x = state.weights_extrapolation - state.stepsize * state.gradient

	numpy.copyto(state.weights, 0, where=numpy.absolute(x)<l)
	numpy.copyto(state.weights, x-l, where=x>l)
	numpy.copyto(state.weights, x+l, where=-x>l)

def version():
	return lib.version()

def discretize(data, num_states = None, targets = None, discretization = None, progress_hook = None):
	array_check(data,"data")

	if numpy.issubdtype(data.dtype, numpy.integer):
		print("WARN: Discretization might fail on non-floating-point types!")

	if num_states is None and discretization is None:
		raise ValueError('ERROR: either a desired number of states or a precomputed discretization must be provided')

	columns = len(data[0])

	R = numpy.zeros(shape = (len(data), columns), dtype = numpy.uint16)
	M = []

	if targets is None:
		targets = range(columns)

	for t in range(columns):
		col_data = numpy.ascontiguousarray(data[:, t])
		distinct = len(numpy.unique(col_data))

		if t in targets:# and distinct > num_states:
			result = numpy.zeros(shape = (len(data), ), dtype = numpy.uint16)

			# interpret NaN-values as missing values and filter them out before discretization
			mask = (numpy.isnan(col_data))
			temp = numpy.delete(col_data,mask)

			if progress_hook is not None:
				progress_hook(t+1,columns,"DSCRT")

			if len(temp) == 0:
				disc_info = None
			elif discretization is None and num_states is not None:
				disc_info = lib.discretize(ctypes.c_uint64(result.ctypes.data), ctypes.c_uint64(temp.ctypes.data), ctypes.c_uint64(len(temp)), ctypes.c_uint64(num_states))
			else:
				disc_info = discretization[t]
				lib.discretize_precomputed(ctypes.c_uint64(result.ctypes.data), ctypes.c_uint64(temp.ctypes.data), ctypes.c_uint64(len(temp)), disc_info)

			# restore missing values
			j = 0
			col_data = numpy.array([], dtype = numpy.uint16)
			for i in range(0,len(mask)):
				if mask[i]:
					col_data = numpy.append(col_data, MISSING_VALUE)
				else:
					col_data = numpy.append(col_data, result[j])
					j = j+1

			if len(col_data) != len(mask):
				raise TypeError('ERROR: this cannot happen!')

			M.append(disc_info)
			R[:, t] = col_data
		else:
			M.append(None)
			R[:, t] = col_data

	if progress_hook is not None and columns not in targets:
		progress_hook(columns,columns,"DSCRT")

	return R, M

def undiscretize_single(row, col, data, moms, ints, mean, sdev, lower_tail_factor = 0.0, upper_tail_factor = 0.0, deterministic = False):
	if data[row,col] == MISSING_VALUE:
		return numpy.nan
	elif moms is not None:
		state = data[row,col]

		m = moms[state][0]
		s = numpy.sqrt(moms[state][1])

		l = ints[state][0]
		u = ints[state][1]

		Y = len(ints)
		if state == Y-1: # upper bound is infty
			u += (u-m) * upper_tail_factor

		if state == 0: # lower bound is -infty
			l -= (m-l) * lower_tail_factor

		if deterministic:
			val = m
		else:
			val = numpy.random.default_rng().normal(m,s)

		while val < l or val > u: # truncated normal
			val = numpy.random.default_rng().normal(m,s)

		return val * sdev + mean

def undiscretize_single_helper(args):
	return undiscretize_single(*args)

def undiscretize(data, M, progress_hook = None, lower_tail_factor = 0.0, upper_tail_factor = 0.0, deterministic = False):
	array_check(data,"data")

	#R = numpy.zeros(shape = (len(data), len(data[0])))

	#i = 0
	r,c = data.shape
	N = r*c

	import multiprocessing as mp

	p = mp.Pool(mp.cpu_count())

#	result = p.map(undiscretize_single_helper, ((row, col, data, M[col].moments, M[col].intervals, M[col].mean, M[col].sdev, lower_tail_factor, upper_tail_factor,deterministic) for row in range(r) for col in range(c)))
	result = p.map(undiscretize_single_helper, ((row, col, data, M[col].moments if M[col] is not None else None, M[col].intervals if M[col] is not None else None, M[col].mean if M[col] is not None else 0, M[col].sdev if M[col] is not None else 0, lower_tail_factor, upper_tail_factor,deterministic) for row in range(r) for col in range(c)))

	return numpy.array(result).reshape(r,c)

	#with numpy.nditer(data, flags = ['multi_index']) as it:
	#	while not it.finished:
	#		if progress_hook is not None:
	#			progress_hook(i+1,N,"UDISC")
	#			i=i+1
	#		row = it.multi_index[0]
	#		col = it.multi_index[1]
	#		it.iternext()
	#
	#if progress_hook is not None:
	#	progress_hook(N,N,"UDISC")
	#return R

@atexit.register
def destroy():
	if ctx is None:
		assert False
	lib.destroy_ctx(ctx)

def read_register(name):
	l = len(name)
	buff = ctypes.create_string_buffer(l + 1)
	buff.value = name.encode('utf-8')
	ptr = (ctypes.c_char_p)(ctypes.addressof(buff))
	return lib.ctx_read_reg(ctx, ptr)

def recode(code):
	n = len(code)
	l = 0
	for stmt in code:
		if len(stmt) > l:
			l = len(stmt)
	buffs = [ctypes.create_string_buffer(l + 1) for i in range(len(code))]
	for index, stmt in enumerate(code):
		buffs[index].value = code[index].encode('utf-8')
	ptrs = (ctypes.c_char_p * n)( * map(ctypes.addressof, buffs))
	lib.ctx_set_code(ctx, ptrs, n)
	return n
	
def run(code=None):
	if ctx is None:
		assert False
	if code is not None:
		recode(code)
	lib.run_ctx(ctx)

def set_seed(s):
	write_register("SEED", s)

def float_from_integer(val):
	return struct.unpack('d', struct.pack('N', val))[0]		

def integer_from_float(val):
	return struct.unpack('N', struct.pack('d', val))[0]

def KL(p, q):
	array_check(p,"p")
	array_check(q,"q")

	#if len(p) != len(q):
	#	raise TypeError('ERROR: p and q must have same length')

	res = 0
	for i in range(min(len(p),len(q))):
		res = res + p[i] * (numpy.log(p[i]) - numpy.log(q[i]))

	return res
	
def save_discretization(fn, U):
	temp = dict()
	for i in range(0,len(U)):
		temp['ints'+str(i)] = U[i].intervals
		temp['moms'+str(i)] = U[i].moments
		temp['mean'+str(i)] = U[i].mean
		temp['sdev'+str(i)] = U[i].sdev
	numpy.savez_compressed(fn,**temp)

def load_discretization(fn):
	U = []
	temp = numpy.load(fn, allow_pickle = True)
	n = int(len(temp)/4)
	for i in range(0,n):
		I = temp['ints'+str(i)]
		M = temp['moms'+str(i)]
		m = temp['mean'+str(i)]
		s = temp['sdev'+str(i)]
		U.append(disc_t(I,M,m,s))
	return U

# TODO: howto load integer model?
def load_model(filename):
	L = []
	
	infile = open(filename,"rb")
	itype = int.from_bytes(infile.read(1),byteorder='little')
	vtype = int.from_bytes(infile.read(1),byteorder='little')
	infile.close()
	
	L.append("idx_t "+str(itype)+";")
	L.append("val_t "+str(vtype)+";")
			
	L.append("MFN \"" + filename + "\";")
	L.append("LDX MPT;")
	L.append("DEL MFN;")
#	L.append("DEL LPT;")
#	L.append("DEL IGN;")
	recode(L)
	run()
	mod = ctypes.cast(read_register("MPT"), ctypes.POINTER(Model0)).contents.cast()
	mod.prepare()
	return mod

def create_model(weights, graph, states, stats = StatisticsType.overcomplete, vtype=default_vtype, itype=default_itype):
	m0 = Model0()

	m0.itype = switch_type(itype)
	m0.vtype = switch_type(vtype)

	Model = m0.get_type()
	
	return Model(weights, graph, states, stats, itype, vtype)

def create_graph(G, nodes=None, target=None, itype=default_itype):
	if isinstance(G, numpy.ndarray) and len(G[0]) != 2:
		array_check(G,"G",dtype=itype)
	elif isinstance(G, GraphType) and nodes is None:
		raise TypeError('ERROR: Please specify the number of nodes')

	if isinstance(G, GraphType) and  G==3 and target is None:
		raise ValueError('ERROR: Star graph requires a target node')
		
	write_register("DPT", 0)
	write_register("MPT", 0)
	write_register("GPT", 0)
	lib.reset_ctx(ctx)
	write_register("EXT0", EXTINF) # TODO: lib.reset_ctx should not delete value of EXTI

	if target is not None:
		write_register("CEN", int(target))

	L = []

	L.append("idx_t "+str(switch_type(itype))+";")

	if isinstance(G, GraphType):
		if nodes > numpy.iinfo(itype).max:
			raise TypeError('ERROR: itype not large enough to handle number of variables')
		L.append("GVX " + str(nodes) + ";")
		L.append("GRA " + str(int(G)) + ";")
	else:
		M = numpy.amax(G)
		V = numpy.unique(G)
		n = len(V)
		m = len(G)
		if n > numpy.iinfo(itype).max:
			raise TypeError('ERROR: itype not large enough to handle number of variables')
		if m > numpy.iinfo(itype).max:
			raise TypeError('ERROR: itype not large enough to handle number of edges')
		s = numpy.sum(V)

		if (n != M + 1) or (s != (M * (M + 1))/2):
			raise ValueError('ERROR: GraphType is invalid')

		data_ptr = ctypes.c_uint64(G.ctypes.data)

		L.append("EAP " + str(data_ptr.value) + ";")
		L.append("GVX " + str(n) + ";")
		L.append("GEX " + str(m) + ";")
		L.append("GRA " + str(int(GraphType.custom)) + ";")

	L.append("LDX GPT;")
	recode(L)
	run()

	G = ctypes.cast(read_register("GPT"), ctypes.POINTER(Graph0)).contents.cast()
	G._Graph__edgelistref = G # IMPORTANT! INCREASES REFCOUNT!

	return G

def train(data=None, graph=None, mode = ModelType.mrf, inference = InferenceType.belief_propagation, iters = 100, infer_iters=None, seed = 0, k = 3, input_model = None, initial_stepsize = 0.1, opt_progress_hook = 0, progress_hook = 0, regularization = 0, proximal_operator = 0, T = 1, threshold = 0.0, lambda_proximal = 0, lambda_regularization = 0, shared_states = False, optimizer = Optimizer.accelerated_proximal_gradient, zero_init=False, clique_size = 3, states = None, vtype=default_vtype, itype=default_itype, infer_epsilon=0.000001):
	"""Return a new matrix of given shape and type, without initializing entries.

	Parameters
	----------
	shape : int or tuple of int
		Shape of the empty matrix.
	dtype : data-type, optional
		Desired output data-type.
	order : {'C', 'F'}, optional
		Whether to store multi-dimensional data in row-major
		(C-style) or column-major (Fortran-style) order in
		memory.

	See Also
	--------
	empty_like, zeros

	Notes
	-----
	`empty`, unlike `zeros`, does not set the matrix values to zero, 
	and may therefore be marginally faster. On the other hand, it requires
	the user to manually set all the values in the array, and should be
	used with caution.

	Examples
	--------
	>>> import numpy.matlib
	>>> numpy.matlib.empty((2, 2))	# filled with random data
	matrix([[  6.76425276e-320,   9.79033856e-307], # random
			[  7.39337286e-309,   3.22135945e-309]])
	>>> numpy.matlib.empty((2, 2), dtype = int)
	matrix([[ 6600475, 		0], # random
			[ 6586976, 22740995]])

	"""

	if input_model is None and graph is None:
		raise TypeError('ERROR: either input_model or graph must be defined')

	if graph is not None and (not (isinstance(graph, GraphType) or isinstance(graph, Graph_incomplete))):
		raise TypeError('ERROR: graph must be an instance of GraphType enum or Graph class')

	if input_model is not None and not isinstance(input_model, Model_incomplete):
		raise TypeError('ERROR: input_model must be an instance of Model class')

	if not isinstance(mode, ModelType):
		raise TypeError('ERROR: mode must be an instance of ModelType enum')

	if not isinstance(inference, InferenceType):
		raise TypeError('ERROR: inference must be an instance of InferenceType enum')

	write_register("MPT", 0)
	write_register("GPT", 0)
	
	lib.reset_ctx(ctx)
	if ext_lib is not None:
		EXTINF = ext_lib.external(switch_type(itype),switch_type(vtype))
		write_register("EXT0", EXTINF)

	if opt_progress_hook != 0:
		f1 = opt_func(opt_progress_hook)
		write_register("CBO", ctypes.c_uint64.from_buffer(f1).value)
	else:
		write_register("CBO", 0)

	if regularization != 0:
		f2 = opt_func(regularization)
		write_register("CBU", ctypes.c_uint64.from_buffer(f2).value)
	else:
		write_register("CBU", 0)

	if progress_hook != 0:
		f3 = prg_func(progress_hook)
		write_register("CBP", ctypes.c_uint64.from_buffer(f3).value)
	else:
		write_register("CBP", 0)

	if proximal_operator != 0:
		f4 = opt_func(proximal_operator)
		write_register("CPR", ctypes.c_uint64.from_buffer(f4).value)
	else:
		write_register("CPR", 0)

	L = []
	L.append("DEL MPT;");
	
	if states is not None:
		if len(states) > numpy.iinfo(itype).max:
			raise TypeError('ERROR: itype not large enough to handle number of variables')
		if numpy.max(states) >= numpy.iinfo(itype).max:
			raise TypeError('ERROR: itype not large enough to handle number of states')
		states_ptr = ctypes.c_uint64(states.ctypes.data)
		L.append("YYY " + str(states_ptr.value) + ";")

	if isinstance(graph, Graph_incomplete):
		if graph.itype != switch_type(itype):
			raise TypeError('ERROR: itype of graph must match model itype')

	L.append("idx_t "+str(switch_type(itype))+";")
	L.append("val_t "+str(switch_type(vtype))+";")
	
	if numpy.issubdtype(vtype, numpy.integer):
		mode = ModelType.integer

	if mode == ModelType.integer:
		L.append("val_t "+str(switch_type(itype))+";")
		L.append("ALG IGD;")
	else:
		write_register("STP", integer_from_float(initial_stepsize))
		L.append("ALG "+str(int(optimizer))+";")

	if seed != 0:
		write_register("SEED", seed)
	write_register("MIS", ord('?'))
	write_register("SEP", ord(','))
	write_register("OVW", 1)
	write_register("HED", 0)
	write_register("LSN", 2)

	write_register("INF", int(inference))
	write_register("MIO", iters)
	write_register("EPO", 0)
	write_register("LAM", integer_from_float(lambda_proximal))
	write_register("ELAM", integer_from_float(lambda_regularization))
	write_register("EPL", integer_from_float(infer_epsilon))

	if mode >= ModelType.strf_linear and mode <= ModelType.strf_inv_exponential:
		write_register("TXX", T)
		write_register("YYC", 1)
	else:
		write_register("TXX", 1)
		write_register("YYC", 0)
		write_register("REP", 0)

	if shared_states:
		write_register("YYC", 1)

	if data is not None:
		array_check(data,"data",dtype=numpy.uint16)

		data_ptr = ctypes.c_uint64(data.ctypes.data)

		l = len(data[0])

		L.append("EDP " + str(data_ptr.value) + ";")
		L.append("NXX " + str(len(data)) + ";")
		L.append("GPX " + str(len(data) * l * 2) + ";")
		L.append("LDX DPT;")
		
		if infer_iters is None:
			L.append("MIL " + str(l) +";") # len(data[0]) is number of columns
		else:
			L.append("MIL " + str(infer_iters) +";") # len(data[0]) is number of columns

	if input_model is None:
		if isinstance(graph, Graph_incomplete):
			L.append("GRA " + str(int(GraphType.custom)) + ";")
			L.append("GPT " + str(ctypes.addressof(graph)) + ";")
		else:
			L.append("GRA " + str(int(graph)) + ";")
			L.append("TREE 0;")
			L.append("KXX "+str(clique_size)+";")
			L.append("LDX GPT;")

			if infer_iters is None:
				L.append("MOV MIL GVX;") # len(data[0]) is number of columns
			else:
				L.append("MIL " + str(infer_iters) +";") # len(data[0]) is number of columns

		write_register("PEL", integer_from_float(threshold))

		L.append("MODEL;")
		L.append("MOV GP1 RES;")

		if mode == ModelType.dbt:
			L.append("DEL MPT;")
			L.append("GRA DBT;")
			L.append("BOLTZMANNTREE;")
			L.append("INITLATENT;")
			L.append("MODEL;")

		elif mode >= ModelType.strf_linear and mode <= ModelType.strf_inv_exponential and T>1:
			L.append("DEL MPT;")
			L.append("GRA OTHER;")
			L.append("STGRAPH;")
			L.append("TREE 0;")
			L.append("REP " + str(int(mode)) + ";")
			L.append("MODEL;")

		if not zero_init and mode != ModelType.integer: # and regularization == 0 and proximal_operator == 0:
			L.append("CLOSEDFORM;")

	else:
		L.append("MPT " + str(ctypes.addressof(input_model)) + ";")
		L.append("GPT " + str(ctypes.addressof(input_model.graph)) + ";")
		L.append("REP " + str(input_model.reparam) + ";")
		L.append("GRA " + str(input_model.gtype) + ";")

		if infer_iters is None:
			L.append("MOV MIL GVX;") # len(data[0]) is number of columns
		else:
			L.append("MIL " + str(infer_iters) +";") # len(data[0]) is number of columns

		L.append("TREE 0;")
		
	L.append("KXX "+str(k)+";")
	L.append("ESTIMATE;")

	recode(L)
	run()
	#import pdb; pdb.set_trace()
	mod = ctypes.cast(read_register("MPT"), ctypes.POINTER(Model0)).contents.cast()
	mod.prepare()

	res = read_register("RES")
	if mode != ModelType.integer:
		res = float_from_integer(res)

	mod.obj = res
	
	sts = read_register("GP1")
	if mode != ModelType.integer:
		sts = float_from_integer(sts)

	mod.structure_score = sts

	return mod
