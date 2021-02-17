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
from pynamics.particle import Particle, PseudoParticle
import pynamics.integration

import sympy
import numpy
import matplotlib.pyplot as plt
plt.ion()
from math import pi
system = System()
pynamics.set_system(__name__,system)
tol=1e-9

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

L = Constant(name='L',system=system)
#V = Constant(name='V',system=system)
R = Constant(name='R',system=system)
Im = Constant(name='Im',system=system)
#Il = Constant(name='Il',system=system)
G = Constant(name='G',system=system)
#b = Constant(name='b',system=system)
kv = Constant(name='kv',system=system)
kt = Constant(name='kt',system=system)
Tl = Constant(name='Tl',system=system)
m_motor = Constant(name='m_motor',system=system)
#g = Constant(name='g',system=system)

I_main = Constant(name='I_main',system=system)

g = Constant(name='g',system=system)
b = Constant(name='b',system=system)
k = Constant(name='k',system=system)
stall_torque = Constant(name='stall_torque',system=system)

k_constraint = Constant(name='k_constraint',system=system)
b_constraint = Constant(name='b_constraint',system=system)

tinitial = 0
tfinal = 10
tstep = 1/30
t = numpy.r_[tinitial:tfinal:tstep]

preload1 = Constant(name='preload1',system=system)
preload2 = Constant(name='preload2',system=system)
preload3 = Constant(name='preload3',system=system)
preload4 = Constant(name='preload4',system=system)
preload5 = Constant(name='preload5',system=system)


constants = {}
constants[lO]=.15
constants[lA] = .15
constants[lB] = .2
constants[lC] = .15
constants[lD] = .2
constants[mO] = .1
constants[mA] = .01
constants[mB] = .01
constants[mC] = .01
constants[mD] = .01
constants[I_main] = .1
constants[g] = 9.81
constants[b] = 1e-1
constants[k] = 1e1
constants[stall_torque] = 1e1
constants[k_constraint] = 1e3
constants[b_constraint] = 1e1
constants[preload1] = 0*pi/180
constants[preload2] = 0*pi/180
constants[preload3] = -180*pi/180
constants[preload4] = 0*pi/180
constants[preload5] = 180*pi/180

constants[L] = .5
#constants[V] = 1
constants[R] = 1
constants[G] = 10
constants[Im] = .01
#constants[Il] = .1
#constants[b] = .1
constants[kv] = .01
constants[kt] = .01
constants[Tl] = 0
constants[m_motor] = 1
#constants[g] = 9.81


x,x_d,x_dd = Differentiable(name='x',system=system)
y,y_d,y_dd = Differentiable(name='y',system=system)
qO,qO_d,qO_dd = Differentiable(name='qO',system=system)
qMA,qMA_d,qMA_dd = Differentiable(name='qMA',system=system)
qA,qA_d,qA_dd = Differentiable(name='qA',system=system)
qB,qB_d,qB_dd = Differentiable(name='qB',system=system)
qMC,qMC_d,qMC_dd = Differentiable(name='qMC',system=system)
qC,qC_d,qC_dd = Differentiable(name='qC',system=system)
qD,qD_d,qD_dd = Differentiable(name='qD',system=system)

iA,iA_d= Differentiable('iA',ii=1,system=system)
iC,iC_d= Differentiable('iC',ii=1,system=system)


initialvalues={
        x: 0,
        x_d: 0,
        y: .3,
        y_d: 0,
        qO: 0,
        qO_d: 0,
        qA: -0.89,
        qA_d: 0,
        qB: -2.64,
        qB_d: 0,
        qC: -pi+0.89,
        qC_d: 0,
        qD: -pi+2.64,
        qD_d: 0}

initialvalues[iA]=0
initialvalues[iC]=0
initialvalues[qMA]=0
initialvalues[qMA_d]=0
initialvalues[qMC]=0
initialvalues[qMC_d]=0


statevariables = system.get_state_variables()
ini = [initialvalues[item] for item in statevariables]

N = Frame('N')
O = Frame('O')
MA = Frame('MA')
A = Frame('A')
B = Frame('B')
MC = Frame('MC')
C = Frame('C')
D = Frame('D')


system.set_newtonian(N)
O.rotate_fixed_axis_directed(N,[0,0,1],qO,system)
MA.rotate_fixed_axis_directed(N,[0,0,1],qMA,system)
A.rotate_fixed_axis_directed(N,[0,0,1],qA,system)
B.rotate_fixed_axis_directed(N,[0,0,1],qB,system)
MC.rotate_fixed_axis_directed(N,[0,0,1],qMC,system)
C.rotate_fixed_axis_directed(N,[0,0,1],qC,system)
D.rotate_fixed_axis_directed(N,[0,0,1],qD,system)

pOrigin = 0*N.x+0*N.y
pOcm=x*N.x+y*N.y
pOA = pOcm+lO/2*O.x
pOC = pOcm-lO/2*O.x
pAB = pOA+lA*A.x
pBtip = pAB + lB*B.x
vBtip = pBtip.time_derivative(N,system)

pCD = pOC + lC*C.x
pDtip = pCD + lD*D.x
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
    points = [pDtip,pCD,pOC,pOA,pAB,pBtip]
    points = PointsOutput(points, constant_values=constants)
    state = numpy.array([ini,result.x])
    ini1 = list(result.x)
    y = points.calc(state)
    y = y.reshape((-1,6,2))
    plt.figure()
    for item in y:
        plt.plot(*(item.T))
#    for item,value in zip(system.get_state_variables(),result.x):
#        initialvalues[item]=value
    
pAcm=pOA+lA/2*A.x
pBcm=pAB+lB/2*B.x
pCcm=pOC+lC/2*C.x
pDcm=pCD+lD/2*D.x

wOMA = O.getw_(MA)
wOA = O.getw_(A)
wAB = A.getw_(B)
wOMC = O.getw_(MC)
wOC = O.getw_(C)
wCD = C.getw_(D)
wBD = B.getw_(D)



wNMA = N.getw_(MA)
aNMA = wNMA.time_derivative()
wNMC = N.getw_(MC)
aNMC = wNMC.time_derivative()

I_motorA = Dyadic.build(MA,Im,Im,Im)
I_motorC = Dyadic.build(MC,Im,Im,Im)


BodyO = Body('BodyO',O,pOcm,mO,Dyadic.build(O,I_main,I_main,I_main),system)
#BodyA = Body('BodyA',A,pAcm,mA,Dyadic.build(A,I_leg,I_leg,I_leg),system)
#BodyB = Body('BodyB',B,pBcm,mB,Dyadic.build(B,I_leg,I_leg,I_leg),system)
#BodyC = Body('BodyC',C,pCcm,mC,Dyadic.build(C,I_leg,I_leg,I_leg),system)
#BodyD = Body('BodyD',D,pDcm,mD,Dyadic.build(D,I_leg,I_leg,I_leg),system)

MotorA = Body('MotorA',MA,pOA,m_motor,I_motorA,system)
MotorA = Body('MotorC',MC,pOC,m_motor,I_motorC,system)

InductorA = PseudoParticle(0*MA.x,L,name='InductorA',vCM = iA*MA.x,aCM = iA_d*MA.x)
InductorC = PseudoParticle(0*MC.x,L,name='InductorC',vCM = iC*MC.x,aCM = iC_d*MC.x)

ParticleA = Particle(pAcm,mA,'ParticleA')
ParticleB = Particle(pBcm,mB,'ParticleB')
ParticleC = Particle(pCcm,mC,'ParticleC')
ParticleD = Particle(pDcm,mD,'ParticleD')

system.addforce(-b*wOA,wOA)
system.addforce(-b*wAB,wAB)
system.addforce(-b*wOC,wOC)
system.addforce(-b*wCD,wCD)
system.addforce(-b*wBD,wBD)
#


stretch = -pBtip.dot(N.y)
stretch_s = (stretch+abs(stretch))
on = stretch_s/(2*stretch+1e-10)
system.add_spring_force1(k_constraint,-stretch_s*N.y,vBtip)
system.addforce(-b_constraint*vBtip*on,vBtip)

system.add_spring_force1(k,(qA-qO-preload1)*N.z,wOA)
system.add_spring_force1(k,(qB-qA-preload2)*N.z,wAB)
system.add_spring_force1(k,(qC-qO-preload3)*N.z,wOC)
system.add_spring_force1(k,(qD-qC-preload4)*N.z,wCD)
system.add_spring_force1(k,(qD-qB-preload5)*N.z,wBD)

system.addforcegravity(-g*N.y)

import pynamics.time_series
x = [0,2,2,5,5,6,6,10]
y = [0,0,1,1,-1,-1,0,0]
my_signal, ft2 = pynamics.time_series.build_smoothed_time_signal(x,y,t,'my_signal',window_time_width = .1)

V = my_signal*stall_torque

TA = kt*iA
system.addforce(TA*N.z,wNMA)
system.addforce((V-iA*R - kv*qMA_d)*MA.x,iA*MA.x)

TC = kt*iC
system.addforce(-TC*N.z,wNMC)
system.addforce((V-iC*R - kv*qMC_d)*MC.x,iC*MC.x)

#system.addforce(torque*O.z,wOA)
#system.addforce(-torque*O.z,wOC)

#
eq = []
eq.append((pBtip-pDtip).dot(N.x))
eq.append((pBtip-pDtip).dot(N.y))
eq.append((O.y.dot(N.y)))
eq_d= [system.derivative(item) for item in eq]
eq_d.append(wOMA.dot(N.z) - G*wOA.dot(N.z))
eq_d.append(wOMC.dot(N.z) - G*wOC.dot(N.z))
#eq_d = [N.getw_(A).dot(N.z) - G*N.getw_(B).dot(N.z)]

eq_dd= [system.derivative(item) for item in eq_d]
#
f,ma = system.getdynamics()
func1 = system.state_space_post_invert(f,ma,eq_dd,constants = constants, variable_functions={my_signal:ft2})
states=pynamics.integration.integrate(func1,ini1,t,rtol=tol,atol=tol)

KE = system.get_KE()
PE = system.getPEGravity(0*N.x) - system.getPESprings()
energy = Output([KE-PE], constant_values=constants)
energy.calc(states)
energy.plot_time()

#torque_plot = Output([torque])
#torque_plot.calc(states)
#torque_plot.plot_time()

points = [pDtip,pCD,pOC,pOA,pAB,pBtip]
points = PointsOutput(points, constant_values=constants)
y = points.calc(states)
y = y.reshape((-1,6,2))
plt.figure()
for item in y[::30]:
    plt.plot(*(item.T))

points.animate(fps = 30, movie_name='parallel_five_bar_jumper_motor.mp4',lw=2)
