# -*- coding: utf-8 -*-

"""
Written by Daniel M. Aukes
Email: danaukes<at>gmail.com
Please see LICENSE for full license.
"""

import pynamics
from pynamics.tree_node import TreeNode
from pynamics.vector import Vector
from pynamics.rotation import Rotation, RotationalVelocity
from pynamics.name_generator import NameGenerator

import sympy


class Frame(NameGenerator):
    def __init__(self,name = None):
        super(Frame,self).__init__()
        self.connections_R = {}
        self.precomputed_R = {}
        self.connections_w = {}
        self.precomputed_w = {}
        self.reps = {}
        self.R_tree = TreeNode(self)
        self.w_tree = TreeNode(self)

        name = name or self.generate_name()
        self.name = name
        
        self.x = Vector()
        self.y = Vector()
        self.z = Vector()

        self.x_sym = sympy.Symbol(name+'.x')
        self.y_sym = sympy.Symbol(name+'.y')
        self.z_sym = sympy.Symbol(name+'.z')
        self.syms = sympy.Matrix([self.x_sym,self.y_sym,self.z_sym])
        
        self.x.add_component(self,[1,0,0])
        self.y.add_component(self,[0,1,0])
        self.z.add_component(self,[0,0,1])
        
        r = Rotation(self,self,sympy.Matrix.eye(3))
        w = RotationalVelocity(self,self,sympy.Number(0)*self.x)
        self.add_rotation(r)
        self.add_w(w)
        
        pynamics.addself(self,name)
        
    def add_rotation(self,rotation):
        self.connections_R[rotation.other(self)] = rotation
        
    def add_precomputed_rotation(self,rotation):
        self.precomputed_R[rotation.other(self)] = rotation


    def add_w(self,w):
        self.connections_w[w.other(self)] = w

    def add_precomputed_w(self,w):
        self.precomputed_w[w.other(self)] = w
        
    
    @property
    def principal_axes(self):
        return [self.x,self.y,self.z]
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)

    def calc_R(self,other):
        if other in self.connections_R:
            return self.connections_R[other]
        elif other in self.precomputed_R:
            return self.precomputed_R[other]
        else: 
            path = self.R_tree.path_to(other.R_tree)
            path = [item.myclass for item in path]
            from_frames = path[:-1]
            to_frames = path[1:]
            Rs = [from_frame.connections_R[to_frame].to_other(from_frame) for from_frame,to_frame in zip(from_frames,to_frames)]
            # w_s = [from_frame.connections[to_frame].w__from(from_frame) for from_frame,to_frame in zip(from_frames,to_frames)]
            R_final = Rs.pop(0)      
            # w_final = w_s.pop(0)    
            for R,to_frame in zip(Rs,to_frames[1:]):
                R_final = R*R_final
                # w_final += w_
                rotation = Rotation(self,to_frame,R_final)
                # rotation.set_w(w_final)
                self.add_precomputed_rotation(rotation)
                to_frame.add_precomputed_rotation(rotation)
#            rotation = Rotation(self,to_frame,R_final,w_final)
            return rotation

    def calc_w(self,other):
        if other in self.connections_w:
            return self.connections_w[other]
        elif other in self.precomputed_w:
            return self.precomputed_w[other]
        else: 
            path = self.w_tree.path_to(other.w_tree)
            path = [item.myclass for item in path]
            from_frames = path[:-1]
            to_frames = path[1:]
            # Rs = [from_frame.connections[to_frame].to_other(from_frame) for from_frame,to_frame in zip(from_frames,to_frames)]
            w_s = [from_frame.connections_w[to_frame].w__from(from_frame) for from_frame,to_frame in zip(from_frames,to_frames)]
            # R_final = Rs.pop(0)      
            w_final = w_s.pop(0)    
            for w_,to_frame in zip(w_s,to_frames[1:]):
                # R_final = R*R_final
                w_final += w_
                rotational_velocity = RotationalVelocity(self,to_frame,w_final)
                # rotation.set_w(w_final)
                self.add_precomputed_w(rotational_velocity)
                to_frame.add_precomputed_w(rotational_velocity)
#            rotation = Rotation(self,to_frame,R_final,w_final)
            return rotational_velocity

    def getR(self,other):
        return self.calc_R(other).to_other(self)

    def getw_(self,other):
        return self.calc_w(other).w__from(self)

    def set_w(self,other,w):
        rotational_velocity = RotationalVelocity(self, other, w)
        self.add_w(rotational_velocity)
        other.add_w(rotational_velocity)
        self.w_tree.add_branch(other.w_tree)        


    def rotate_fixed_axis(self,fromframe,axis,q,system = None):
        system = system or pynamics.get_system()

        rotation = Rotation.build_fixed_axis(fromframe,self,axis,q,system)
        rotational_velocity = RotationalVelocity.build_fixed_axis(fromframe,self,axis,q,system)
        self.add_rotation(rotation)
        self.add_w(rotational_velocity)
        fromframe.add_rotation(rotation)
        fromframe.add_w(rotational_velocity)
        fromframe.R_tree.add_branch(self.R_tree)        
        fromframe.w_tree.add_branch(self.w_tree)        

    def rotate_fixed_axis_directed(self,fromframe,axis,q,system=None):
        self.rotate_fixed_axis(fromframe,axis,q,system)
        
    def efficient_rep(self,other,functionname):
        key = (other,functionname)
        if key in self.reps:
            return self.reps[key]
        else:
            path = self.R_tree.path_to(other.R_tree)
            dot = {}
            for mysym,myvec in zip(self.syms,[self.x,self.y,self.z]):
                for othersym,othervec in zip(other.syms,[other.x,other.y,other.z]):
                    min_dot_len = 0
                    for frame in path:
                        frame = frame.myclass
                        v1 = myvec.express(frame).components[frame]
                        v2 = othervec.express(frame).components[frame]
                        function = getattr(v1,functionname)
                        dot_rep = function(v2)
                        dot_len = len(str(dot_rep))
                        if min_dot_len==0 or dot_len<min_dot_len:
                            min_dot_len=dot_len
                            min_dot_frame = frame
                        elif dot_len==min_dot_len:
                            if min_dot_frame in frame.decendents:
                                min_dot_frame = frame
                    dot[frozenset((mysym,othersym))] = min_dot_frame
            self.reps[key] = dot
            return dot
                
