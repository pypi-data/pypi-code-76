# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes
Email: danaukes<at>gmail.com
Please see LICENSE for full license.
"""

import pynamics
from pynamics.name_generator import NameGenerator
from pynamics.force import Force

class PseudoParticle(NameGenerator):
    def __init__(self,pCM,mass,name = None,system = None,vCM = None,aCM=None):
        system = system or pynamics.get_system()

        name = name or self.generate_name()
        self.name = name

        self.pCM = pCM
        self.mass = mass
        self.system = system

        self.vCM= vCM or self.pCM.time_derivative(self.system.newtonian,self.system)
        self.aCM= aCM or self.vCM.time_derivative(self.system.newtonian,self.system)
                
        self.gravityvector = None
        self.forcegravity = None        
        
        self.system.particles.append(self)
        pynamics.addself(self,self.name)

        self.effectiveforces = []

    def adddynamics(self):
        effectiveforce = self.mass*self.aCM
        self.KE = .5*self.mass*self.vCM.dot(self.vCM)

        self.effectiveforces = []
        self.effectiveforces.append(Force(effectiveforce,self.vCM))

        return self.effectiveforces
        
    def addforcegravity(self,gravityvector):
        pass

class Particle(PseudoParticle):
    def addforcegravity(self,gravityvector):
        self.gravityvector = gravityvector
        self.forcegravity = self.mass*gravityvector
        self.system.addforce(self.forcegravity,self.vCM)
        
if __name__=='__main__':
    from pynamics.system import System
    from pynamics.frame import Frame
    sys = System()
    N = Frame(name = 'N')
    
    sys.set_newtonian(N)
    Particle(0*N.x,1)