import hashlib
import numpy as np
import pxpy as px
from pxpy import *

##############################################################################################################

def test_init():
	assert px.version() == 10066

def test_recode():
	code = []
	ret = px.recode(code)

	assert ret == 0

	px.run()
	code = ['GPS \"THIS IS PX\";', 'DEL GPS;']
	ret = px.recode(code)
	px.run()

	assert ret == 2

def test_register():
	px.write_register("LSN", 4)

	assert px.read_register("LSN") == 4
	
def test_discretization():
	A = np.array([np.arange(10.0)]).reshape(10,1)
	
	eps = 0.00000001
	
	_,U1 = px.discretize(A,32) # bins > distinct values

	assert U1[0].num_intervals == 10
	assert U1[0].num_intervals == U1[0].num_moments

	m = U1[0].mean
	s = U1[0].sdev

	for i in range(0,10):
		assert np.abs(U1[0].moments[i][0] * s + m - i * 1.0) < eps

	_,U2 = px.discretize(A,3)

	m = U2[0].mean
	s = U2[0].sdev

	assert U2[0].num_intervals == 3
	assert U2[0].num_intervals == U2[0].num_moments

	assert np.abs(U2[0].moments[0][0] * s + m - (0+1+2) / 3)   < eps
	assert np.abs(U2[0].moments[1][0] * s + m - (3+4+5) / 3)   < eps
	assert np.abs(U2[0].moments[2][0] * s + m - (6+7+8+9) / 4) < eps

	assert np.abs(U2[0].moments[0][1] * s * s - 1)   < eps
	assert np.abs(U2[0].moments[1][1] * s * s - 1)   < eps
	assert np.abs(U2[0].moments[2][1] * s * s - 5/3) < eps

def test_train_strf():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)

	model = px.train(data=D, iters=100, T=4, lambda_proximal=0.5, lambda_regularization=0.1, graph=GraphType.chain, mode=ModelType.strf_rational, proximal_operator=px.prox_l1, regularization=px.squared_l2_regularization)

	assert hashlib.sha1(model.graph.edgelist.astype(np.uint64)).hexdigest() == "305f3755d5e5e8926ed18f2727a2c97faec8d92d"
	assert abs(model.obj - 6.2687) < 0.0001

	model.graph.delete()
	model.delete()

def test_train_mrf():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)

	model = px.train(data=D, iters=100, graph=GraphType.auto_tree, mode=ModelType.mrf)

	x = np.zeros(shape=(model.graph.nodes, ))
	score = np.dot(model.weights, model.phi(x))

	assert hashlib.sha1(model.graph.edgelist.astype(np.uint64)).hexdigest() == "d3a50e11e1d42a530968179054b2dd4f77b40d46"
	assert abs(model.obj - 3.8664) < 0.0001
	assert abs(score - -41.3515) < 0.0001

	model.graph.delete()
	model.delete()

def test_train_intmrf():
	px.set_seed(1337)

	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	model = px.train(data=D, iters=100, graph=GraphType.auto_tree, k=32, mode=ModelType.integer)

	probs, A = model.infer()

	assert hashlib.sha1(model.graph.edgelist.astype(np.uint64)).hexdigest() == "d3a50e11e1d42a530968179054b2dd4f77b40d46"
	KLval = px.KL(model.statistics, probs[model.woffsets[model.graph.nodes]:]) / model.graph.edges
	assert KLval < 0.02
	assert model.obj == 10

	model.graph.delete()
	model.delete()

def test_train_dbt():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	model = px.train(data=D, iters=1000, graph=GraphType.auto, clique_size=3, mode=ModelType.dbt)

	assert hashlib.sha1(model.graph.edgelist.astype(np.uint64)).hexdigest() == "07a739b4285f2d3b0b3277870087ea7cbf0636a5"
	assert abs(model.obj - 4.1935) < 0.0001
	
	model.graph.delete()
	model.delete()

def test_infer():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	model = px.train(data=D, iters=100, inference=InferenceType.junction_tree, lambda_proximal=10, graph=GraphType.grid, mode=ModelType.mrf, proximal_operator=px.prox_l1)

	probs, A_jt = model.infer(inference=InferenceType.belief_propagation)
	probs_jt = probs
	probs, A_lbp = model.infer(inference=InferenceType.belief_propagation)
	probs_lbp = probs
	probs, A_sqm = model.infer(inference=InferenceType.stochastic_quadrature, iterations=10000)
	probs_sqm = probs

	print(probs_jt)
	print(probs_lbp)
	print(probs_sqm)

	assert px.KL(probs_jt, probs_lbp)/model.graph.edges < 0.1
	assert px.KL(probs_jt, probs_sqm)/model.graph.edges < 0.1

	model.graph.delete()
	model.delete()

	#print("Average KL of estimated edge marginals:")
	#print("KL[jt || lbp] = "+str(px.KL(probs_jt, probs_lbp)/model.graph.edges))
	#print("KL[jt || sqm] = "+str(px.KL(probs_jt, probs_sqm)/model.graph.edges))
	#print("Log-partition function values:")
	#print("A_jt="+str(A_jt) + ", A_lbp=" + str(A_lbp) + ", A_sqm=" + str(A_sqm))

def test_save_load_model():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	
	model0 = px.train(data=D, iters=100, inference=InferenceType.junction_tree, lambda_proximal=10, graph=GraphType.grid, mode=ModelType.mrf, proximal_operator=px.prox_l1)
	
	model0.save('/tmp/pxpy.testmodel')
	
	model = px.load_model('/tmp/pxpy.testmodel')

	assert model.graph.nodes == 16
	assert model.graph.edges == 24
	assert model.dim == 96 # minimal dim

	assert len(model) == 96 # overcomplete dim
	assert len(model.graph) == model.graph.nodes

	model.graph.delete()
	model.delete()

def test_optimization_hooks():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)

	model = px.train(data=D, iters=100, graph=GraphType.chain, mode=ModelType.mrf)
	l1_ml = np.linalg.norm(model.weights, ord=1)
	l2_ml = np.linalg.norm(model.weights, ord=2)

	model.graph.delete()
	model.delete()

	model = px.train(data=D, iters=100, graph=GraphType.chain, mode=ModelType.mrf, regularization=px.squared_l2_regularization, lambda_regularization=0.1)
	l1_sl2reg = np.linalg.norm(model.weights, ord=1)
	l2_sl2reg = np.linalg.norm(model.weights, ord=2)

	model.graph.delete()
	model.delete()

	model = px.train(data=D, iters=100, graph=GraphType.chain, mode=ModelType.mrf, proximal_operator=px.prox_l1, lambda_proximal=10)
	l1_l1reg = np.linalg.norm(model.weights, ord=1)
	l2_l1reg = np.linalg.norm(model.weights, ord=2)

	model.graph.delete()
	model.delete()

	assert l1_ml > l1_sl2reg and l1_sl2reg > l1_l1reg
	assert l2_ml > l2_sl2reg and l2_sl2reg > l2_l1reg

def test_predict():
	model = px.load_model('/tmp/pxpy.testmodel')

	x = -np.ones(shape=(1, model.graph.nodes), dtype=np.uint16)
	model.predict(x)

	assert hashlib.sha1(x).hexdigest() == "5ab8ef859e6782c2ecfffd4e4d15f5f9e1ed9018"

	model.graph.delete()
	model.delete()

def test_sampler():
	D = np.array([[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[2,2,2,2,2,2,2,2]],dtype=np.uint16)
	model = px.train(D,graph=px.GraphType.chain,iters=2048)

	px.set_seed(1337)

	N = 1000

	S0 = model.sample(sampler=SamplerType.perturb_and_map, num_samples=N, perturbation=1)
	s0 = np.zeros(len(model.statistics))
	for i in range(N):
		s0 += model.phi(S0[i])
	s0 /= N
	err0 = np.linalg.norm(model.statistics-s0)

	S1 = model.sample(sampler=SamplerType.gibbs, num_samples=N, burn=1000)
	s1 = np.zeros(len(model.statistics))
	for i in range(N):
		s1 += model.phi(S1[i])
	s1 /= N
	err1 = np.linalg.norm(model.statistics-s1)
	
	assert err0 < 0.1
	assert err1 < 0.1

	model.graph.delete()
	model.delete()

def test_custom_graph():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)

	E = np.array([0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 10, 0, 11, 0, 12, 0, 13, 0, 14, 0, 15], dtype=px.default_itype).reshape(15, 2)
	G = px.create_graph(E)

	model = px.train(data=D, iters=100, graph=G, mode=ModelType.mrf)

	assert hashlib.sha1(model.graph.edgelist).hexdigest() == hashlib.sha1(E).hexdigest()

	model.delete()
	G.delete()

def test_custom_model():
	A = np.array([0, 1], dtype=px.default_itype).reshape(1, 2)
	G = px.create_graph(A)
	#G = px.create_graph(GraphType.chain, nodes=2)

	a1 = np.array([0.5, 0.6, 0.6, -0.3],dtype=px.default_vtype)
	a2 = np.array([0.1, 0.1, -1.0],dtype=px.default_vtype)

	m1 = px.create_model(a1, G, states = 2, stats = StatisticsType.overcomplete) # overcomplete is the default
	m2 = px.create_model(a2, G, states = 2, stats = StatisticsType.minimal)

	P1, A1 = m1.infer()
	P2, A2 = m2.infer()

	assert px.KL(P1, P2) < 0.000001

	m1.delete()
	m2.delete()
	G.delete()

def test_observations():
	D = np.array([[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[2,2,2,2,2,2,2,2]],dtype=np.uint16)
	model = px.train(D,graph=px.GraphType.chain,iters=100)

	assert np.linalg.norm(model.predict(np.array([[0,-1,-1,-1,-1,-1,-1,-1]],dtype=np.uint16)) - np.zeros(8).astype(np.uint16)) == 0
	assert np.linalg.norm(model.predict(np.array([[-1,-1,-1,-1,1,-1,-1,-1]],dtype=np.uint16)) - np.ones(8).astype(np.uint16)) == 0
	assert np.linalg.norm(model.predict(np.array([[2,-1,-1,-1,-1,-1,-1,2]],dtype=np.uint16)) - 2*np.ones(8).astype(np.uint16)) == 0	

def test_vertex_marginals():
	model = px.load_model('/tmp/pxpy.testmodel')

	model.infer()

	assert abs(model.prob(3,0) - 0.50818) < 0.00001
	assert abs(model.prob(3,1) - 0.49181) < 0.00001

	model.graph.delete()
	model.delete()

def test_edge_marginals():
	model = px.load_model('/tmp/pxpy.testmodel')

	P, _ = model.infer()

	offset = model.fulldimension - model.dimension # = sum_v Y[v]

	e = 2
	Q = model.slice_edge(e,P[offset:])

	s = model.graph.edgelist[e][0]
	t = model.graph.edgelist[e][1]

	assert Q[1] == model.prob(e,0,1)
	assert abs(model.prob(3,0,1) - 0.224441) < 0.00001

	model.graph.delete()
	model.delete()

def test_resume_training():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	m1 = px.train(data=D, iters=10, initial_stepsize=0.00001, graph=GraphType.chain, mode=ModelType.mrf, zero_init=True, optimizer=Optimizer.gradient_descent)
	m2 = px.train(data=D, iters=10, initial_stepsize=0.00001, optimizer=Optimizer.gradient_descent, input_model=m1, mode=ModelType.mrf)
	m3 = px.train(data=D, iters=20, initial_stepsize=0.00001, graph=GraphType.chain, mode=ModelType.mrf, optimizer=Optimizer.gradient_descent, zero_init=True)

	assert hashlib.sha1(m1.weights).hexdigest() == hashlib.sha1(m3.weights).hexdigest()
