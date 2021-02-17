# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes
Email: danaukes<at>gmail.com
Please see LICENSE for full license.
"""
import sympy
sympy.init_printing(pretty_print=False)

import pynamics
from pynamics.frame import Frame
from pynamics.variable_types import Differentiable,Constant,Variable
from pynamics.system import System
from pynamics.body import Body
from pynamics.dyadic import Dyadic
from pynamics.output import Output,PointsOutput
from pynamics.particle import Particle
import pynamics.integration
import pynamics.tanh

import sympy
import numpy
import matplotlib.pyplot as plt
plt.ion()
from math import pi
system = System()
pynamics.set_system(__name__,system)

error = 1e-4
error_tol = 1e-10

from math import sin,cos

#alpha = 1e6
#beta = 1e5

#preload1 = Constant('preload1',0*pi/180,system)
#l1 = Constant(1,'l1',system)
m1 = Constant(1e-1,'m1',system)
m2 = Constant(1e-3,'m2',system)
k = Constant(1.5e2,'k',system)
l0 = Constant(1,'l0',system)
b = Constant(1e0,'b',system)
g = Constant(9.81,'g',system)
k_constraint = Constant(1e4,'k_constraint',system)
b_constraint = Constant(1e5,'b_constraint',system)

tinitial = 0
tfinal = 2
tstep = 1/30
t = numpy.r_[tinitial:tfinal:tstep]

x1,x1_d,x1_dd = Differentiable('x1',system)
y1,y1_d,y1_dd = Differentiable('y1',system)
#x2,x2_d,x2_dd = Differentiable('x2',system)
#y2,y2_d,y2_dd = Differentiable('y2',system)

q1,q1_d,q1_dd = Differentiable('q1',system)
l1,l1_d,l1_dd = Differentiable('l1',system)

vini = 5
aini = -60*pi/180

initialvalues = {}
initialvalues[x1]=0
initialvalues[x1_d]=vini*cos(aini)
initialvalues[y1]=1.2
initialvalues[y1_d]=vini*sin(aini)

initialvalues[q1]=10*pi/180
initialvalues[q1_d]=0

initialvalues[l1]=0
initialvalues[l1_d]=0

#initialvalues[x2]=0
#initialvalues[x2_d]=1
#initialvalues[y2]=1
#initialvalues[y2_d]=0

statevariables = system.get_state_variables()
ini = [initialvalues[item] for item in statevariables]

N = Frame('N')
system.set_newtonian(N)
A = Frame('A')

A.rotate_fixed_axis_directed(N,[0,0,1],q1)


pNA=0*N.x
pm1 = x1*N.x + y1*N.y
pm2 = pm1+(l1-l0)*A.y

#BodyA = Body('BodyA',A,pm1,m1,IA,system)
Particle1 = Particle(pm1,m1,'Particle1',system)
Particle2 = Particle(pm2,m2,'Particle2',system)

vpm1 = pm1.time_derivative(N,system)
vpm2 = pm2.time_derivative(N,system)

#l_ = pm1-pm2
#l = (l_.dot(l_))**.5
#l_d =system.derivative(l)
#stretch = l1
#ul_ = l_*((l+error_tol)**-1)
#vl = l_.time_derivative(N,system)

#system.add_spring_force1(k,stretch*ul_,vpm)
system.addforce(k*l1*A.y,vpm1)
system.addforce(-k*l1*A.y,vpm2)

system.addforce(b*l1_d*A.y,vpm1)
system.addforce(-b*l1_d*A.y,vpm2)

#system.addforce(k*l*ul_,vpm2)
#system.addforce(-b*vl,vl)
#system.addforce(-b*vl,vl)
#system.addforce(-b*vl,vl)



system.addforcegravity(-g*N.y)

#system.addforcegravity(-g*N.y)
#system.addforcegravity(-g*N.y)

y2 = pm2.dot(N.y)

f_floor2 = pynamics.tanh.gen_spring_force(-y2, 1e6, 0, 0, 1,0,0,plot=False)
system.addforce(k_constraint*f_floor2*N.y,vpm2)
system.addforce(-b_constraint*f_floor2*vpm2,vpm2)

f_floor1 = pynamics.tanh.gen_spring_force(-y1, 1e6, 0, 0, 1,0,0,plot=False)
system.addforce(k_constraint*f_floor1*N.y,vpm1)
system.addforce(-b_constraint*f_floor1*vpm1,vpm1)
#system.addforce(k_constraint*f_floor*N.y,vpm2)


#stretch = -pm2.dot(N.y)
#stretch_s = (stretch+abs(stretch))
#on = stretch_s/(2*stretch+1e-10)
#system.add_spring_force1(k_constraint,-stretch_s*N.y,vpm2)


#eq1 = [pm2.dot(N.y)-0]
#eq1_d=[system.derivative(item) for item in eq1]
#eq1_dd=[system.derivative(system.derivative(item)) for item in eq1]

eq = []
#a = [0-pm2.dot(N.y)]
#b = [(item+abs(item)) for item in a]

f,ma = system.getdynamics()
func = system.state_space_post_invert(f,ma)
#func = system.state_space_post_invert2(f,ma,eq1_dd,eq1_d,eq1,eq_active = b)
states=pynamics.integration.integrate_odeint(func,ini,t,rtol = error, atol = error, args=({'constants':system.constant_values},))
#states = states[0]

points = [pm1,pm2]
po = PointsOutput(points, system, constant_values=system.constant_values)
y=po.calc(states)

plt.figure()
for item in y:
    plt.plot(*(item.T),lw=2,marker='o')
plt.axis('equal')
#
po.animate(fps = 30, movie_name='bouncy-mod.mp4',lw=2,marker='o')
