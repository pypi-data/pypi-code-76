# -*- coding: utf-8 -*-

import pynamics
from pynamics.frame import Frame
from pynamics.variable_types import Differentiable,Constant
from pynamics.system import System
from pynamics.body import Body
from pynamics.dyadic import Dyadic
from pynamics.output import Output,PointsOutput
from pynamics.particle import Particle
import pynamics.integration
import numpy
import matplotlib.pyplot as plt
plt.ion()
from math import pi
import logging
import pynamics.integration
import pynamics.system
import numpy.random
import scipy.interpolate
import cma


system = System()
pynamics.set_system(__name__,system)


lA = Constant(1,'lA',system)
lB = Constant(1,'lB',system)
lC = Constant(1,'lC',system)

mA = Constant(1,'mA',system)
mB = Constant(1,'mB',system)
mC = Constant(1,'mC',system)

g = Constant(9.81,'g',system)
b = Constant(1e1,'b',system)
k = Constant(1e1,'k',system)

preload1 = Constant(0*pi/180,'preload1',system)
preload2 = Constant(0*pi/180,'preload2',system)
preload3 = Constant(0*pi/180,'preload3',system)

Ixx_A = Constant(1,'Ixx_A',system)
Iyy_A = Constant(1,'Iyy_A',system)
Izz_A = Constant(1,'Izz_A',system)
Ixx_B = Constant(1,'Ixx_B',system)
Iyy_B = Constant(1,'Iyy_B',system)
Izz_B = Constant(1,'Izz_B',system)
Ixx_C = Constant(1,'Ixx_C',system)
Iyy_C = Constant(1,'Iyy_C',system)
Izz_C = Constant(1,'Izz_C',system)



tol = 1e-12



tinitial = 0
tfinal = 10
fps = 30
tstep = 1/fps
t = numpy.r_[tinitial:tfinal:tstep]


qA,qA_d,qA_dd = Differentiable('qA',system)
qB,qB_d,qB_dd = Differentiable('qB',system)
qC,qC_d,qC_dd = Differentiable('qC',system)




initialvalues = {}
initialvalues[qA]=-45*pi/180
initialvalues[qA_d]=0*pi/180
initialvalues[qB]=0*pi/180
initialvalues[qB_d]=0*pi/180
initialvalues[qC]=0*pi/180
initialvalues[qC_d]=0*pi/180



statevariables = system.get_state_variables()
ini = [initialvalues[item] for item in statevariables]


N = Frame('N')
A = Frame('A')
B = Frame('B')
C = Frame('C')




system.set_newtonian(N)



A.rotate_fixed_axis_directed(N,[0,0,1],qA,system)
B.rotate_fixed_axis_directed(A,[0,0,1],qB,system)
C.rotate_fixed_axis_directed(B,[0,0,1],qC,system)


pNA=0*N.x
pAB=pNA+lA*A.x
pBC = pAB + lB*B.x
pCtip = pBC + lC*C.x



pAcm=pNA+lA/2*A.x
pBcm=pAB+lB/2*B.x
pCcm=pBC+lC/2*C.x

wNA = N.getw_(A)
wAB = A.getw_(B)
wBC = B.getw_(C)


IA = Dyadic.build(A,Ixx_A,Iyy_A,Izz_A)
IB = Dyadic.build(B,Ixx_B,Iyy_B,Izz_B)
IC = Dyadic.build(C,Ixx_C,Iyy_C,Izz_C)

BodyA = Body('BodyA',A,pAcm,mA,IA,system)
BodyB = Body('BodyB',B,pBcm,mB,IB,system)
BodyC = Body('BodyC',C,pCcm,mC,IC,system)

system.addforce(-b*wNA,wNA)
system.addforce(-b*wAB,wAB)
system.addforce(-b*wBC,wBC)


system.add_spring_force1(k,(qA-preload1)*N.z,wNA) 
system.add_spring_force1(k,(qB-preload2)*A.z,wAB)
system.add_spring_force1(k,(qC-preload3)*B.z,wBC)


system.addforcegravity(-g*N.y)



eq = []
# eq.append(pCtip.dot(N.y))
eq_d=[(system.derivative(item)) for item in eq]
eq_dd=[(system.derivative(item)) for item in eq_d]


f,ma = system.getdynamics()

unknown_constants = [b,k]

known_constants = list(set(system.constant_values.keys())-set(unknown_constants))
known_constants = dict([(key,system.constant_values[key]) for key in known_constants])

func1,lambda1 = system.state_space_post_invert(f,ma,eq_dd,return_lambda = True,constants = known_constants)

def run_sim(args):
    constants = dict([(key,value) for key,value in zip(unknown_constants,args)])
    states=pynamics.integration.integrate(func1,ini,t,rtol=tol,atol=tol,hmin=tol, args=({'constants':constants},))
    return states

input_data_all = run_sim([1.1e2,9e2])
input_positions = input_data_all[:,:3]
# input_positions = input_positions.copy()


# pynamics.integration.logger.setLevel(logging.ERROR)
pynamics.system.logger.setLevel(logging.ERROR)

points = [pNA,pAB,pBC,pCtip]
points_output = PointsOutput(points,system)
y = points_output.calc(input_data_all)
points_output.plot_time()

r = numpy.random.randn(*(y.shape))*.01
y_rand  = y + r
fy = scipy.interpolate.interp1d(t,y_rand.transpose((1,2,0)))
fyt = fy(t)

# points_output.animate(fps = fps,movie_name = 'render.mp4',lw=2,marker='o',color=(1,0,0,1),linestyle='-')

def calc_error(args):
    states_guess = run_sim(args)
    y_guess = points_output.calc(states_guess).transpose((1,2,0))
    error = fyt - y_guess
    error **=2
    error = error.sum()
    return error
    

k_guess = [1e2,1e3]

es = cma.CMAEvolutionStrategy(k_guess, 0.5)
es.logger.disp_header()
while not es.stop():
      X = es.ask()
      es.tell(X, [calc_error(x) for x in X])
      es.logger.add()
      es.logger.disp([-1])


es.best.x
calc_error(es.best.x)
calc_error([1e2,1e3])


input_data_all2 = run_sim(es.best.x)
points_output2 = PointsOutput(points,system)
y2 = points_output2.calc(input_data_all2)
points_output2.plot_time()
# points_output2.animate(fps = fps,movie_name = 'render.mp4',lw=2,marker='o',color=(1,0,0,1),linestyle='-')



# lambda2 = numpy.array([lambda1(item1,item2,system.constant_values) for item1,item2 in zip(t,states)])
# plt.figure()
# plt.plot(t, lambda2)



