# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes
Email: danaukes<at>gmail.com
Please see LICENSE for full license.
"""

import pynamics
from pynamics.name_generator import NameGenerator
import pynamics.inertia
from pynamics.force import Force

class Body(NameGenerator):
    def __init__(self,name,frame,pCM,mass,inertia_CM,system = None,about_point = None,about_point_d = None,about_point_dd = None,vCM = None,aCM=None,wNBody = None, alNBody = None,inertia_about_point = None):
        system = system or pynamics.get_system()

        name = name or self.generate_name()
        self.name = name

        self.frame = frame
        self.system = system
        self.pCM = pCM
        self.mass = mass
        self.inertia_CM= inertia_CM
        self.vCM= vCM or self.pCM.time_derivative(self.system.newtonian,self.system)
        self.aCM= aCM or self.vCM.time_derivative(self.system.newtonian,self.system)


        if about_point is None:
            self.about_point = pCM
            self.about_point_d = self.vCM
            self.about_point_dd =self.aCM
        else:
            self.about_point = about_point
            self.about_point_d = about_point_d or self.about_point.time_derivative(self.system.newtonian,self.system)
            self.about_point_dd = about_point_dd or self.about_point_d.time_derivative(self.system.newtonian,self.system)
        
        self.inertia_about_point = inertia_about_point or pynamics.inertia.shift_from_cm(self.inertia_CM,self.pCM,self.about_point,self.mass,self.frame)

        self.gravityvector = None
        self.forcegravity = None        
        
        self.wNBody = wNBody or self.system.newtonian.getw_(self.frame)
        self.alNBody = alNBody or self.wNBody.time_derivative(self.system.newtonian,self.system)
        
#        self.linearmomentum = self.mass*self.vCM
#        self.angularmomentum = self.inertia.dot(self.wNBody)
        
        self.system.bodies.append(self)
        pynamics.addself(self,name)
        
        self.effectiveforces = []

    def adddynamics(self):
        I = self.inertia_about_point
        
        effectiveforce = self.mass*self.aCM
        momentofeffectiveforce= I.dot(self.alNBody)+self.wNBody.cross(I.dot(self.wNBody))+self.mass*(self.pCM-self.about_point).cross(self.about_point_dd)
        self.KE = .5*self.mass*self.vCM.dot(self.vCM) + .5*self.wNBody.dot(self.inertia_CM.dot(self.wNBody))

        self.effectiveforces = []
        self.effectiveforces.append(Force(effectiveforce,self.about_point_d))
        self.effectiveforces.append(Force(momentofeffectiveforce,self.wNBody))
#        self.system.addmomentum(self.linearmomentum,self.vCM)
#        self.system.addmomentum(self.angularmomentum,self.wNBody)
#        self.system.addKE(self.KE)
        return self.effectiveforces

    def addforcegravity(self,gravityvector):
        self.gravityvector = gravityvector
        self.forcegravity = self.mass*self.gravityvector
        self.system.addforce(self.forcegravity,self.vCM)
        
    def __repr__(self):
        return self.name+'(body)'
#        return self.name+' <frame {0:#x}>'.format(self.__hash__())
    def __str__(self):
        return self.name+'(body)'
#        return self.name+' <frame {0:#x}>'.format(self.__hash__())

