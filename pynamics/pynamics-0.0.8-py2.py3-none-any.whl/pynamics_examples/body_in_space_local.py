# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes
Email: danaukes<at>gmail.com
Please see LICENSE for full license.
"""

import pynamics
pynamics.automatic_differentiate=False
from pynamics.frame import Frame
from pynamics.variable_types import Differentiable,Constant
from pynamics.system import System
from pynamics.body import Body
from pynamics.dyadic import Dyadic
from pynamics.output import Output,PointsOutput
from pynamics.particle import Particle
import pynamics.integration
pynamics.script_mode = True

import sympy
import numpy
import matplotlib.pyplot as plt
plt.ion()
import math
system = System()
pynamics.set_system(__name__,system)

g = Constant(9.81,'g',system)

tinitial = 0
tfinal = 5
tstep = 1/30
t = numpy.r_[tinitial:tfinal:tstep]

qA,qA_d = Differentiable('qA',limit=2)
qB,qB_d = Differentiable('qB',limit=2)
qC,qC_d = Differentiable('qC',limit=2)

wx,wx_d= Differentiable('wx',ii = 1,limit=3)
wy,wy_d= Differentiable('wy',ii = 1,limit=3)
wz,wz_d= Differentiable('wz',ii = 1,limit=3)

mC = Constant(1,'mC')
Ixx = Constant(2,'Ixx')
Iyy = Constant(3,'Iyy')
Izz = Constant(1,'Izz')

initialvalues = {}
initialvalues[qA]=0*math.pi/180
initialvalues[qB]=0*math.pi/180
initialvalues[qC]=0*math.pi/180

initialvalues[wx]=1.
initialvalues[wy]=1.
initialvalues[wz]=0.

N = Frame('N')
A = Frame('A')
B = Frame('B')
C = Frame('C')

system.set_newtonian(N)
A.rotate_fixed_axis_directed(N,[1,0,0],qA,system)
B.rotate_fixed_axis_directed(A,[0,1,0],qB,system)
C.rotate_fixed_axis_directed(B,[0,0,1],qC,system)

pCcm=0*N.x

IC = Dyadic.build(C,Ixx,Iyy,Izz)

w1 = N.getw_(C)
w2 = wx*C.x+wy*C.y+wz*C.z
N.set_w(C,w2)

from pynamics.constraint import Constraint

eq0 = w1-w2
eq = []
eq.append(eq0.dot(B.x))
eq.append(eq0.dot(B.y))
eq.append(eq0.dot(B.z))

c = Constraint(eq)
c.linearize(0)
system.add_constraint(c)

for constraint in system.constraints:
    constraint.solve([wx,wy,wz],[qA_d,qB_d,qC_d])

BodyC = Body('BodyC',C,pCcm,mC,IC)

system.addforcegravity(-g*N.y)

points = [1*C.x,0*C.x,1*C.y,0*C.y,1*C.z]

f,ma = system.getdynamics()

func1 = system.state_space_pre_invert(f,ma)
# func1 = system.state_space_post_invert(f,ma)

ini = [initialvalues[item] for item in system.get_state_variables()]

states=pynamics.integration.integrate_odeint(func1,ini,t,args=({'constants':system.constant_values},))

po = PointsOutput(points,system)
po.calc(states)
po.animate(fps = 30,lw=2)

so = Output([qA,qB,qC])
so.calc(states)
so.plot_time()