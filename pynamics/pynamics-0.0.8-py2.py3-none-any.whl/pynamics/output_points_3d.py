# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 16:30:38 2020

@author: danaukes
"""
import numpy
import pynamics
from pynamics.output_points import PointsOutput
from pynamics.output_generic import Output

class PointsOutput3D(PointsOutput):
    def __init__(self,y_exp, system=None, constant_values = None,state_variables = None,dot = None):
        system = system or pynamics.get_system()
        dot = dot or [system.newtonian.x,system.newtonian.y, system.newtonian.z]
        y_exp = [item for item2 in y_exp for item in [item2.dot(dotitem) for dotitem in dot]]
        Output.__init__(self,y_exp, system, constant_values,state_variables)

    def calc(self,x):
        Output.calc(self,x)
        self.y.resize(self.y.shape[0],int(self.y.shape[1]/3),3)
        return self.y

    def animate(self,fps = 30,stepsize=1, movie_name = None,*args,azim = 0, elev = 0,**kwargs):
        
        # import numpy as np
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import animation, rc

        y = self.y

        f = plt.figure()
        ax = f.add_subplot(1,1,1,autoscale_on=False,projection='3d')
        ax.view_init(azim=azim,elev=elev)
#        ax.axis('equal')
        limits   = [y[:,:,0].min(),y[:,:,0].max(),y[:,:,1].min(),y[:,:,1].max()]
        ax.axis(limits)


#        y = self.y[::stepsize]
        
        line, = ax.plot([], [], [],*args,**kwargs)
        
        def init():
            # line.set_data([], [],[])
            line.set_xdata(numpy.array([]))
            line.set_ydata(numpy.array([]))
            line.set_3d_properties(numpy.array([]))
            # line.set_zdata([])
            return (line,)
        
        def run(item):
            xdata = item.T[0]
            ydata = item.T[1]
            zdata = item.T[2]
            line.set_xdata(xdata)
            line.set_ydata(ydata)
            line.set_3d_properties(zdata)
            # line.set_zdata(zdata)
#            ax.axis('equal')
#            ax.axis(limits)
            return (line,)

        self.anim = animation.FuncAnimation(f, run, init_func=init,frames=y[::stepsize], interval=1/fps*1000, blit=True,repeat = True,repeat_delay=3000)        
        if movie_name is not None:
            self.anim.save(movie_name, fps=fps,writer='ffmpeg')
        return ax

    def plot_time(self,stepsize=1):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        f=plt.figure()
        ax = f.add_subplot(1,1,1,autoscale_on=False,projection='3d')
        try:
            self.y
        except AttributeError:
            self.calc()


        for item in self.y[::stepsize]:
            ax.plot3D(xs=item[:,0].T,ys=item[:,1].T,zs=item[:,2].T)
        return ax
        # ax.axis('equal')