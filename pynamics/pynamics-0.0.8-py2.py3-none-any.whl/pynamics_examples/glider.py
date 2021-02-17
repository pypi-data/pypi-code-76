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
#from pynamics.particle import Particle
import pynamics.integration
import sympy
#import logging
#pynamics.logger.setLevel(logging.ERROR)
#pynamics.system.logger.setLevel(logging.ERROR)

import numpy
import matplotlib.pyplot as plt
plt.ion()
from math import pi, sin, cos
system = System()
pynamics.set_system(__name__,system)


tinitial = 0
tfinal = 5
tstep = 1/30
t = numpy.r_[tinitial:tfinal:tstep]

ang_ini = 0

v=1

x,x_d,x_dd = Differentiable('x',ini=[0,v*cos(ang_ini*pi/180)])
y,y_d,y_dd = Differentiable('y',ini=[1,v*sin(ang_ini*pi/180)])
z,z_d,z_dd = Differentiable('z',ini=[0,0])

qA,qA_d,qA_dd = Differentiable('qA',ini=[0,0])
qB,qB_d,qB_dd = Differentiable('qB',ini=[0,0])
qC,qC_d,qC_dd = Differentiable('qC',ini=[ang_ini*pi/180,0])


mC = Constant(.05,'mC')
g = Constant(9.81,'g')
I_11=Constant(6e-3,'I_11')
rho = Constant(1.292,'rho')
Sw = Constant(.1,'Sw')
Se = Constant(.025,'Se')
l = Constant(.35,'l')
lw = Constant(-.03,'lw')
le = Constant(.04,'le')
qE = Constant(3*pi/180,'qE')

ini = system.get_ini()

N = Frame('N')
A = Frame('A')
B = Frame('B')
C = Frame('C')
E = Frame('E')

system.set_newtonian(N)
A.rotate_fixed_axis_directed(N,[1,0,0],qA)
B.rotate_fixed_axis_directed(A,[0,1,0],qB)
C.rotate_fixed_axis_directed(B,[0,0,1],qC)
E.rotate_fixed_axis_directed(C,[0,0,1],-qE)

pCcm=x*N.x+y*N.y+z*N.z
#pCcm=x*N.x+y*N.y
pCcp=pCcm-lw*C.x

pC1 = pCcm
pC2 = pCcm-l*C.x
pE = pC2-le*E.x
#wNC = N.getw_(C)

vcm = pCcm.time_derivative()

vcp=pCcp.time_derivative()
vcp2 = vcp.dot(vcp)

ve=pE.time_derivative()
ve2 = ve.dot(ve)

IC = Dyadic.build(C,I_11,I_11,I_11)

Body('BodyC',C,pCcm,mC,IC)


vcx = vcp.dot(C.x)
vcy = vcp.dot(-C.y)
angle_of_attack_C = sympy.atan2(vcy,vcx)


vex = ve.dot(E.x)
vey = ve.dot(-E.y)
angle_of_attack_E = sympy.atan2(vey,vex)

#cl = 2*sin(angle_of_attack)*cos(angle_of_attack)
#cd = 2*sin(angle_of_attack)**2

#fl = .5*rho*vcp2*cl*A
#fd = .5*rho*vcp2*cd*A

f_aero_C = rho*vcp2*sympy.sin(angle_of_attack_C)*Sw*C.y
f_aero_E = rho*ve2*sympy.sin(angle_of_attack_E)*Sw*E.y

system.addforcegravity(-g*N.y)
system.addforce(f_aero_C,vcp)
system.addforce(f_aero_E,ve)

points = [pC1,pC2]

#ang = [wNC.dot(C.x),wNC.dot(C.y),wNC.dot(C.z)]

f,ma = system.getdynamics()
func1 = system.state_space_post_invert(f,ma)
states=pynamics.integration.integrate_odeint(func1,ini,t, args=({'constants':system.constant_values},))

#output = Output(ang,system)
#output.calc(states)
#output.plot_time()

po = PointsOutput(points,system)
y=po.calc(states)
#po.plot_time()
#y = y.reshape((-1,2,2))
plt.figure()
for item in y:
    plt.plot(*(item.T),lw=2,marker='o')
#
po.animate(fps = 30, movie_name='glider.mp4',lw=2,marker='o')
