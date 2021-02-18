#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
              "Alexis Thibault", "Tobias Van Baarsel"]
__copyright__ = "Copyright 2020, Inria"
__credits__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
               "Alexis Thibault", "Tobias Van Baarsel"]
__license__ = "GPL 3.0"
__version__ = "0.4.2"
__email__ = "openwind-contact@inria.fr"
__status__ = "Dev"

class ReedModel:
    """Model of reed
    """

    def __init__(self, epsilon, pm, mr, omega02, g, y0, w, sr,
                 theta=0.25, omega_NL=316, alpha_NL=4):

        self.epsilon = epsilon
        self.mr = mr
        self.omega02 = omega02
        self.g = g
        self.y0 = y0
        self.w = w
        self.sr = sr
        self.pm = pm
        self.theta = theta
        self.omega_NL = omega_NL
        self.alpha_NL = alpha_NL

    def __valvetype__(self):
        if self.epsilon == 1:
            return('lip')
        elif self.epsilon == -1:
            return('reed')
        else:
            raise NameError('epsilon must be 1 or -1')

    def __str__(self):
        s = "ReedModel({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
        return s.format(self.valvetype(), self.pm, self.mr, self.omega02,
                        self.omega_NL, self.alpha_NL, self.g, self.y0, self.w,
                        self.sr, self.theta)

    def __repr__(self):
        return self.__str__()
