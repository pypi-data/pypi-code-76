#!/usr/bin/env python
# coding: utf-8

# ---
# title: Triple Pendulum Example
# type: submodule
# ---

# In[1]:




# Try running with this variable set to true and to false and see the difference in the resulting equations of motion

# In[2]:


global_q = False


# Import all the necessary modules

# In[3]:


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
import numpy
import matplotlib.pyplot as plt
plt.ion()
from math import pi
import scipy.interpolate
import sympy

# The next two lines create a new system object and set that system as the global system within the module so that other variables can use and find it.

# In[4]:


system = System()
pynamics.set_system(__name__,system)


# ## Parameterization
# 
# ### Constants
# 
# Declare constants and seed them with their default value.  This can be changed at integration time but is often a nice shortcut when you don't want the value to change but you want it to be represented symbolically in calculations

# In[5]:


lA = Constant(1,'lA',system)
lB = Constant(1,'lB',system)
lC = Constant(6*25.4/1000,'lC',system)

mA = Constant(1,'mA',system)
mB = Constant(1,'mB',system)
mC = Constant(1,'mC',system)
m1 = Constant(2,'m1',system)

g = Constant(9.81,'g',system)
b = Constant(1e1,'b',system)
k1 = Constant(1e2,'k1',system)
k2 = Constant(1e1,'k2',system)

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

k_constraint = Constant(1e4,'k_constraint',system)
b_constraint = Constant(1e2,'b_constraint',system)

force_var = sympy.Symbol('fv')

# ## Integration Tolerance
# Specify the precision of the integration

# In[6]:


tol = 1e-11


# ### Time 
# Define variables for time that can be used throughout the script.  These get used to create the t array, a list of every time value that is solved for during integration

# In[7]:


tinitial = 0
tfinal = 10
fps = 30
tstep = 1/fps
t = numpy.r_[tinitial:tfinal:tstep]


force = t*0
ii = (t==3).nonzero()[0][0]
jj = (t==5).nonzero()[0][0]
force[ii:jj] = 10
f_force = scipy.interpolate.interp1d(t, force,fill_value='extrapolate')

# ### Differentiable State Variables
# 
# Define your differentiable state variables that you will use to model the state of the system.  In this case $qA$, $qB$, and $qC$ are the rotation angles of a three-link mechanism

# In[8]:


x,x_d,x_dd = Differentiable('x',system)
y,y_d,y_dd = Differentiable('y',system)
qA,qA_d,qA_dd = Differentiable('qA',system)
qB,qB_d,qB_dd = Differentiable('qB',system)
qC,qC_d,qC_dd = Differentiable('qC',system)
x2,x2_d,x2_dd = Differentiable('x2',system)


# ### Initial Values
# Define a set of initial values for the position and velocity of each of your state variables.  It is necessary to define a known.  This code create a dictionary of initial values.

# In[9]:


initialvalues = {}
initialvalues[x]=0
initialvalues[x_d]=0
initialvalues[y]=2.01
initialvalues[y_d]=0
initialvalues[qA]=0*pi/180
initialvalues[qA_d]=0*pi/180
initialvalues[qB]=0*pi/180
initialvalues[qB_d]=0*pi/180
initialvalues[qC]=0*pi/180
initialvalues[qC_d]=0*pi/180
initialvalues[x2]=-1.5
initialvalues[x2_d]=.5


# These two lines of code order the initial values in a list in such a way that the integrator can use it in the same order that it expects the variables to be supplied

# In[10]:


statevariables = system.get_state_variables()
ini = [initialvalues[item] for item in statevariables]


# ## Kinematics
# 
# ### Frames
# Define the reference frames of the system

# In[11]:


N = Frame('N')
A = Frame('A')
B = Frame('B')
C = Frame('C')


# ### Newtonian Frame
# 
# It is important to define the Newtonian reference frame as a reference frame that is not accelerating, otherwise the dynamic equations will not be correct

# In[12]:


system.set_newtonian(N)


# This is the first time that the "global_q" variable is used.  If you choose to rotate each frame with reference to the base frame, there is the potential for a representational simplification.  If you use a relative rotation, this can also be simpler in some cases.  Try running the code either way to see which one is simpler in this case.

# In[13]:


A.rotate_fixed_axis_directed(N,[0,0,1],qA,system)
B.rotate_fixed_axis_directed(A,[0,0,1],qB,system)
C.rotate_fixed_axis_directed(B,[0,0,1],qC,system)

# ### Vectors
# Define the vectors that describe the kinematics of a series of connected lengths
# 
# * pNA - This is a vector with position at the origin.
# * pAB - This vector is length $l_A$ away from the origin along the A.x unit vector
# * pBC - This vector is length $l_B$ away from the pAB along the B.x unit vector 
# * pCtip - This vector is length $l_C$ away from the pBC along the C.x unit vector 

# In[14]:


pNA=x*N.x+y*N.y
pAB=pNA-lA*A.y
pBC=pAB-lB*B.y
pC1 = pBC - lC/2*C.x
pC2 = pBC + lC/2*C.x

pm1 = x2*N.x+2*N.y

vNA = pNA.time_derivative()
vC1 = pC1.time_derivative()
vC2 = pC2.time_derivative()
vm1 = pm1.time_derivative()

# ## Centers of Mass
# 
# It is important to define the centers of mass of each link.  In this case, the center of mass of link A, B, and C is halfway along the length of each

# In[15]:


pAcm=pNA-lA/2*A.y
pBcm=pAB-lB/2*B.y
pCcm=pBC


# ## Calculating Velocity
# 
# The angular velocity between frames, and the time derivatives of vectors are extremely useful in calculating the equations of motion and for determining many of the forces that need to be applied to your system (damping, drag, etc).  Thus, it is useful, once kinematics have been defined, to take or find the derivatives of some of those vectors for calculating  linear or angular velocity vectors
# 
# ### Angular Velocity
# The following three lines of code computes and returns the angular velocity between frames N and A (${}^N\omega^A$), A and B (${}^A\omega^B$), and B and C (${}^B\omega^C$).  In other cases, if the derivative expression is complex or long,  you can supply pynamics with a given angular velocity between frames to speed up computation time.

# In[16]:


wNA = N.getw_(A)
wAB = A.getw_(B)
wBC = B.getw_(C)


# ### Vector derivatives
# The time derivatives of vectors may also be 

# vCtip = pCtip.time_derivative(N,system)

# ### Define Inertias and Bodies
# The next several lines compute the inertia dyadics of each body and define a rigid body on each frame.  In the case of frame C, we represent the mass as a particle located at point pCcm.  

# In[17]:


IA = Dyadic.build(A,Ixx_A,Iyy_A,Izz_A)
IB = Dyadic.build(B,Ixx_B,Iyy_B,Izz_B)
IC = Dyadic.build(B,Ixx_C,Iyy_C,Izz_C)

BodyA = Body('BodyA',A,pAcm,mA,IA,system)
BodyB = Body('BodyB',B,pBcm,mB,IB,system)
BodyC = Body('BodyC',C,pCcm,mC,IC,system)
ParticleM = Particle(pm1,m1,'ParticleM',system)


# ## Forces and Torques
# Forces and torques are added to the system with the generic ```addforce``` method.  The first parameter supplied is a vector describing the force applied at a point or the torque applied along a given rotational axis.  The second parameter is the  vector describing the linear speed (for an applied force) or the angular velocity(for an applied torque)

# In[18]:

stretch1 = -pC1.dot(N.y)
stretch1_s = (stretch1+abs(stretch1))
on = stretch1_s/(2*stretch1+1e-10)
system.add_spring_force1(k_constraint,-stretch1_s*N.y,vC1)
system.addforce(-b_constraint*vC1*on,vC1)

toeforce = k_constraint*-stretch1_s

stretch2 = -pC2.dot(N.y)
stretch2_s = (stretch2+abs(stretch2))
on = stretch2_s/(2*stretch2+1e-10)
system.add_spring_force1(k_constraint,-stretch2_s*N.y,vC2)
system.addforce(-b_constraint*vC2*on,vC2)

system.addforce(-b*wNA,wNA)
system.addforce(-b*wAB,wAB)
system.addforce(-b*wBC,wBC)

# system.addforce(force_var*N.x,vNA)


stretch3_v = (pm1 - pNA)
stretch3_uv = 1/(stretch3_v.length() + 1e-10)* stretch3_v

stretch3 = 1-(pm1 - pNA).length()
stretch3_s = (stretch3+abs(stretch3))
on = stretch3_s/(2*stretch3+1e-10)
system.add_spring_force2(k_constraint,-stretch3_uv*stretch3_s,vm1,-vNA)
# system.addforce(-b_constraint*vC2*on,vC2)


# ### Spring Forces
# 
# Spring forces are a special case because the energy stored in springs is conservative and should be considered when calculating the system's potential energy.  To do this, use the ```add_spring_force``` command.  In this method, the first value is the linear spring constant.  The second value is the "stretch" vector, indicating the amount of deflection from the neutral point of the spring.  The final parameter is, as above, the linear or angluar velocity vector (depending on whether your spring is a linear or torsional spring)
# 
# In this case, the torques applied to each joint are dependent upon whether qA, qB, and qC are absolute or relative rotations, as defined above.

# In[19]:


# system.add_spring_force1(k1,(qA-preload1)*N.z,wNA) 
system.add_spring_force1(k2,(qB-preload2)*A.z,wAB)
system.add_spring_force1(k1,(qC-preload3)*B.z,wBC)


# ### Gravity
# Again, like springs, the force of gravity is conservative and should be applied to all bodies.  To globally apply the force of gravity to all particles and bodies, you can use the special ```addforcegravity``` method, by supplying the acceleration due to gravity as a vector.  This will get applied to all bodies defined in your system.

# In[20]:


system.addforcegravity(-g*N.y)


# ## Constraints
# Constraints may be defined that prevent the motion of certain elements.  Try uncommenting the commented out line to see what happens.

# In[21]:


eq = []
# eq.append(pCtip.dot(N.y))
eq_d=[(system.derivative(item)) for item in eq]
eq_dd=[(system.derivative(item)) for item in eq_d]


# ## F=ma
# This is where the symbolic expressions for F and ma are calculated.  This must be done after all parts of the system have been defined.  The ```getdynamics``` function uses Kane's method to derive the equations of motion.

# In[22]:


f,ma = system.getdynamics()


# In[23]:


f


# In[24]:


ma


# ## Solve for Acceleration
# 
# The next line of code solves the system of equations F=ma plus any constraint equations that have been added above.  It returns one or two variables.  func1 is the function that computes the velocity and acceleration given a certain state, and lambda1(optional) supplies the function that computes the constraint forces as a function of the resulting states
# 
# There are a few ways of solveing for a.  The below function inverts the mass matrix numerically every time step.  This can be slower because the matrix solution has to be solved for, but is sometimes more tractable than solving the highly nonlinear symbolic expressions that can be generated from the previous step.  The other options would be to use ```state_space_pre_invert```, which pre-inverts the equations symbolically before generating a numerical function, or ```state_space_post_invert2```, which adds Baumgarte's method for intermittent constraints.

# In[25]:


func1,lambda1 = system.state_space_post_invert(f,ma,eq_dd,return_lambda = True,variable_functions={force_var:f_force})


# ## Integrate
# 
# The next line of code integrates the function calculated

# In[26]:


states=pynamics.integration.integrate_odeint(func1,ini,t,rtol=tol,atol=tol,hmin=tol, args=({'constants':system.constant_values},))


# ## Outputs
# 
# 
# The next section simply calculates and plots a variety of data from the previous simulation
# ### States

# In[27]:


plt.figure()
artists = plt.plot(t,states[:,:5])
plt.legend(artists,['x','y','qA','qB','qC'])


# ### Energy

# In[28]:


# KE = system.get_KE()
# PE = system.getPEGravity(pNA) - system.getPESprings()
# energy_output = Output([KE-PE],system)
# energy_output.calc(states)
# energy_output.plot_time()


# ### Motion

# In[29]:


points = [pm1,pNA,pAB,pBC,pC1,pC2]
points_output = PointsOutput(points,system)
y = points_output.calc(states)
points_output.plot_time(5)


# #### Motion Animation
# in normal Python the next lines of code produce an animation using matplotlib

# In[30]:


points_output.animate(fps = fps,movie_name = 'render.mp4',lw=2,marker='o',color=(1,0,0,1),linestyle='-')
#a()


# To plot the animation in jupyter you need a couple extra lines of code...

# In[31]:


# from matplotlib import animation, rc
# from IPython.display import HTML
# HTML(points_output.anim.to_html5_video())


# ### Constraint Forces

# This line of code computes the constraint forces once the system's states have been solved for.

# In[32]:


# lambda2 = numpy.array([lambda1(item1,item2,system.constant_values) for item1,item2 in zip(t,states)])
# plt.figure()
# plt.plot(t, lambda2)


# In[ ]:




