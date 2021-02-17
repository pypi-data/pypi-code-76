# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes
Email: danaukes<at>gmail.com
Please see LICENSE for full license.
"""

import pynamics
from pynamics.frame import Frame
from pynamics.variable_types import Differentiable,Constant
from pynamics.system import System
from pynamics.body import Body
from pynamics.dyadic import Dyadic
from pynamics.output import Output,PointsOutput
from pynamics.particle import Particle
import pynamics.integration

import sympy
import numpy
import matplotlib.pyplot as plt
plt.ion()
from math import pi
system = System()
pynamics.set_system(__name__,system)
tol=1e-3

lO = Constant(name='lO',system=system)
lA = Constant(name='lA',system=system)
lB = Constant(name='lB',system=system)
lC = Constant(name='lC',system=system)
lD = Constant(name='lD',system=system)

mO = Constant(name='mO',system=system)
mA = Constant(name='mA',system=system)
mB = Constant(name='mB',system=system)
mC = Constant(name='mC',system=system)
mD = Constant(name='mD',system=system)
#m_motor = Constant(name='m_motor',system=system)

#I_main = Constant(name='I_main',system=system)

g = Constant(name='g',system=system)
b_joint = Constant(name='b_joint',system=system)
k_joint = Constant(name='k_joint',system=system)
b_beam = Constant(name='b_beam',system=system)
k_beam = Constant(name='k_beam',system=system)
stall_torque = Constant(name='stall_torque',system=system)

k_constraint = Constant(name='k_constraint',system=system)
b_constraint = Constant(name='b_constraint',system=system)

tinitial = 0
tfinal = 5
tstep = 1/30
t = numpy.r_[tinitial:tfinal:tstep]

preload1 = Constant(name='preload1',system=system)
preload2 = Constant(name='preload2',system=system)
preload3 = Constant(name='preload3',system=system)
preload4 = Constant(name='preload4',system=system)
preload5 = Constant(name='preload5',system=system)


constants = {}
constants[lO]=.03
constants[lA] = .12
constants[lB] = .12
constants[lC] = .12
constants[lD] = .12
constants[mO] = .0369
constants[mA] = .003
constants[mB] = .003
constants[mC] = .003
constants[mD] = .003
#constants[m_motor] = .1
#constants[I_main] = 1
constants[g] = 9.81
constants[b_joint] = .00025
constants[k_joint] = .0229183
constants[b_beam] = 0
constants[k_beam] = 14.0224
constants[stall_torque] = .00016*5.7/4.3586
constants[k_constraint] = 1e3
constants[b_constraint] = 1e1
constants[preload1] = 0*pi/180
constants[preload2] = 0*pi/180
constants[preload3] = -180*pi/180
constants[preload4] = 0*pi/180
constants[preload5] = 180*pi/180


x,x_d,x_dd = Differentiable(name='x',system=system)
y,y_d,y_dd = Differentiable(name='y',system=system)
qO,qO_d,qO_dd = Differentiable(name='qO',system=system)
qA1,qA1_d,qA1_dd = Differentiable(name='qA1',system=system)
qB1,qB1_d,qB1_dd = Differentiable(name='qB1',system=system)
qC1,qC1_d,qC1_dd = Differentiable(name='qC1',system=system)
qD1,qD1_d,qD1_dd = Differentiable(name='qD1',system=system)
qA2,qA2_d,qA2_dd = Differentiable(name='qA2',system=system)
qB2,qB2_d,qB2_dd = Differentiable(name='qB2',system=system)
qC2,qC2_d,qC2_dd = Differentiable(name='qC2',system=system)
qD2,qD2_d,qD2_dd = Differentiable(name='qD2',system=system)

initialvalues={
        x: 0,
        x_d: 0,
        y: .5,
        y_d: 0,
        qO: 0,
        qO_d: 0,
        qA1: -0.89,
        qA1_d: 0,
        qB1: -2.64,
        qB1_d: 0,
        qC1: -pi+0.89,
        qC1_d: 0,
        qD1: -pi+2.64,
        qD1_d: 0,
        qA2: -0.89,
        qA2_d: 0,
        qB2: -2.64,
        qB2_d: 0,
        qC2: -pi+0.89,
        qC2_d: 0,
        qD2: -pi+2.64,
        qD2_d: 0}

statevariables = system.get_state_variables()
ini = [initialvalues[item] for item in statevariables]

N = Frame('N')
O = Frame('O')
A1 = Frame('A1')
B1 = Frame('B1')
C1 = Frame('C1')
D1 = Frame('D1')
A2 = Frame('A2')
B2 = Frame('B2')
C2 = Frame('C2')
D2 = Frame('D2')

system.set_newtonian(N)
O.rotate_fixed_axis_directed(N,[0,0,1],qO,system)

A1.rotate_fixed_axis_directed(N,[0,0,1],qA1,system)
B1.rotate_fixed_axis_directed(N,[0,0,1],qB1,system)
C1.rotate_fixed_axis_directed(N,[0,0,1],qC1,system)
D1.rotate_fixed_axis_directed(N,[0,0,1],qD1,system)

A2.rotate_fixed_axis_directed(N,[0,0,1],qA2,system)
B2.rotate_fixed_axis_directed(N,[0,0,1],qB2,system)
C2.rotate_fixed_axis_directed(N,[0,0,1],qC2,system)
D2.rotate_fixed_axis_directed(N,[0,0,1],qD2,system)

pOrigin = 0*N.x+0*N.y
pOcm=x*N.x+y*N.y
pOA = pOcm+lO/2*O.x
pOC = pOcm-lO/2*O.x
pA1A2 = pOA+lA/2*A1.x
pAB = pA1A2 + lA/2*A2.x
pB1B2 = pAB + lB/2*B1.x
pBtip = pB1B2 + lB/2*B2.x
vBtip = pBtip.time_derivative(N,system)

pC1C2 = pOC + lC/2*C1.x 
pCD = pC1C2 + lC/2*C2.x
pD1D2 = pCD + lD/2*D1.x 
pDtip = pD1D2 + lD/2*D2.x
vDtip = pDtip.time_derivative(N,system)

def gen_init():
    eqs = []
    eqs.append(pBtip-pDtip)
#    eqs.append(pBtip-pOrigin)
    a=[(item).express(N) for item in eqs]
    b=[item.subs(constants) for item in a]
    c = numpy.array([vec.dot(item) for vec in b for item in list(N.principal_axes)])
    d = (c**2).sum()
    e = system.get_state_variables()
    #e = sorted(list(d.atoms(Differentiable)),key=lambda x:str(x))
    f = sympy.lambdify(e,d)
    g = lambda args:f(*args)
    return g
fun = gen_init()

import scipy.optimize
result = scipy.optimize.minimize(fun,ini)

if result.fun<1e-7:
    points = [pDtip,pD1D2,pCD,pC1C2,pOC,pOA,pA1A2,pAB,pB1B2,pBtip]
    points_output = PointsOutput(points, constant_values=constants)
    state = numpy.array([ini,result.x])
    ini1 = list(result.x)
    y = points_output.calc(state)
    y = y.reshape((-1,len(points),2))
    plt.figure()
    for item in y:
        plt.plot(*(item.T))
#    for item,value in zip(system.get_state_variables(),result.x):
#        initialvalues[item]=value
    
pA1cm=pOA+lA/4*A1.x
pB1cm=pAB+lB/4*B1.x
pC1cm=pOC+lC/4*C1.x
pD1cm=pCD+lD/4*D1.x

pA2cm=pA1A2+lA/4*A2.x
pB2cm=pB1B2+lB/4*B2.x
pC2cm=pC1C2+lC/4*C2.x
pD2cm=pD1D2+lD/4*D2.x

wOA1 = O.getw_(A1)
wA1A2 = A1.getw_(A2)
wA2B1 = A2.getw_(B1)
wB1B2 = B1.getw_(B2)
wOC1 = O.getw_(C1)
wC1C2 = C1.getw_(C2)
wC2D1 = C2.getw_(D1)
wD1D2 = D1.getw_(D2)
wB2D2 = B2.getw_(D2)

#BodyO = Body('BodyO',O,pOcm,mO,Dyadic.build(O,I_main,I_main,I_main),system)
#BodyA = Body('BodyA',A,pAcm,mA,Dyadic.build(A,I_leg,I_leg,I_leg),system)
#BodyB = Body('BodyB',B,pBcm,mB,Dyadic.build(B,I_leg,I_leg,I_leg),system)
#BodyC = Body('BodyC',C,pCcm,mC,Dyadic.build(C,I_leg,I_leg,I_leg),system)
#BodyD = Body('BodyD',D,pDcm,mD,Dyadic.build(D,I_leg,I_leg,I_leg),system)

Particle0 = Particle(pOcm,mO,'ParticleO')

ParticleA1 = Particle(pA1cm,mA/2,'ParticleA1')
ParticleB1 = Particle(pB1cm,mB/2,'ParticleB1')
ParticleC1 = Particle(pC1cm,mC/2,'ParticleC1')
ParticleD1 = Particle(pD1cm,mD/2,'ParticleD1')

ParticleA2 = Particle(pA2cm,mA/2,'ParticleA2')
ParticleB2 = Particle(pB2cm,mB/2,'ParticleB2')
ParticleC2 = Particle(pC2cm,mC/2,'ParticleC2')
ParticleD2 = Particle(pD2cm,mD/2,'ParticleD2')

system.addforce(-b_joint*wOA1,wOA1)
system.addforce(-b_joint*wA2B1,wA2B1)
system.addforce(-b_joint*wOC1,wOC1)
system.addforce(-b_joint*wC2D1,wC2D1)
system.addforce(-b_joint*wB2D2,wB2D2)

#system.addforce(-b_beam*wA1A2,wA1A2)
#system.addforce(-b_beam*wB1B2,wB1B2)
#system.addforce(-b_beam*wC1C2,wC1C2)
#system.addforce(-b_beam*wD1D2,wD1D2)

#
stretch = -pBtip.dot(N.y)
stretch_s = (stretch+abs(stretch))
on = stretch_s/(2*stretch+1e-5)
system.add_spring_force1(k_constraint,-stretch_s*N.y,vBtip)
system.addforce(-b_constraint*vBtip*on,vBtip)

system.add_spring_force1(k_joint,(qA1-qO-preload1)*N.z,wOA1)
system.add_spring_force1(k_joint,(qB1-qA2-preload2)*N.z,wA2B1)
system.add_spring_force1(k_joint,(qC1-qO-preload3)*N.z,wOC1)
system.add_spring_force1(k_joint,(qD1-qC2-preload4)*N.z,wC2D1)
system.add_spring_force1(k_joint,(qD2-qB2-preload5)*N.z,wB2D2)

system.add_spring_force1(k_beam,(qA2-qA1)*N.z,wA1A2)
system.add_spring_force1(k_beam,(qB2-qB1)*N.z,wB1B2)
system.add_spring_force1(k_beam,(qC2-qC1)*N.z,wC1C2)
system.add_spring_force1(k_beam,(qD2-qD1)*N.z,wD1D2)

system.addforcegravity(-g*N.y)

import pynamics.time_series
x = [0,2,2,5,5,6,6,10]
y = [0,0,1,1,-1,-1,0,0]
my_signal, ft2 = pynamics.time_series.build_smoothed_time_signal(x,y,t,'my_signal',window_time_width = .1)

#torque = my_signal*stall_torque
#system.addforce(torque*O.z,wOA1)
#system.addforce(-torque*O.z,wOC1)

#
eq = []
eq.append((pBtip-pDtip).dot(N.x))
eq.append((pBtip-pDtip).dot(N.y))
eq.append((O.y.dot(N.y)))
eq_d= [system.derivative(item) for item in eq]
eq_dd= [system.derivative(item) for item in eq_d]
#
f,ma = system.getdynamics()
func1 = system.state_space_post_invert(f,ma,eq_dd,constants = constants,variable_functions={my_signal:ft2})
states=pynamics.integration.integrate(func1,ini1,t,rtol=tol,atol=tol)

#KE = system.get_KE()
#PE = system.getPEGravity(0*N.x) - system.getPESprings()
#energy = Output([KE-PE], constant_values=constants)
#energy.calc(states)
#energy.plot_time()

#torque_plot = Output([torque])
#torque_plot.calc(states)
#torque_plot.plot_time()


points = [pDtip,pD1D2,pCD,pC1C2,pOC,pOA,pA1A2,pAB,pB1B2,pBtip]
points_output = PointsOutput(points, constant_values=constants)
y = points_output.calc(states)
y = y.reshape((-1,len(points),2))
plt.figure()
for item in y[::30]:
    plt.plot(*(item.T))
        

points_output.animate(fps = 30, movie_name='parallel_five_bar_jumper_foot.mp4',lw=2)
