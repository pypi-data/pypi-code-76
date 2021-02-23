# coding: utf-8

import math as mth
import random as rd
import numpy as np

from functools import reduce

from sample.toolbox.mathbox import find_index
from sample.toolbox.random_number_generator import RandomNumberGenerator

E = mth.exp (1)
DEFAULT_RANDOM_NUMBER_GENERATOR = RandomNumberGenerator ()

class RandomVariable:

    #public:

        def __init__ (self, value):
            self.value = value

        @property
        def current (self):
            return self.value

        def __del__ (self):
            pass

        def __call__ (self):
            raise NotImplementedError

class Uniform (RandomVariable):

    #public:

        def __init__ (self, a=0, b=1):
            super ().__init__ (None)
            self.left = a
            self.length = b - a
        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            self.value = self.left + self.length * (gen ())
            return self.value

class Exponential (RandomVariable) :

    #public:

        def __init__ (self, lamb):
            super ().__init__ (None)
            self.inv_lamb = 1 / lamb
            self.U = Uniform ()

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            self.value = - self.inv_lamb * mth.log (self.U ())
            return self.value

class Cauchy (RandomVariable) :

    #public:

        def __init__ (self, c):
            super ().__init__ (None)
            half_pi = mth.pi * 0.5
            self.U = Uniform (-half_pi, half_pi)
            self.c = c

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            self.value = self.c *  mth.tan (self.U (gen))
            return self.value

class Pareto (RandomVariable):

    #public:

        def __init__ (self, theta):
            super ().__init__ (None)
            self.inv_theta = - 1 / theta
            self.U = Uniform ()
            
        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            self.value = self.U (gen) ** self.inv_theta
            return self.value

class Choice (RandomVariable):

    #public:

        def __init__ (self, weights):
            super ().__init__ (None)
            self.U = Uniform ()
            self.cumulative_weights = [0]
            for p in weights : self.cumulative_weights.append (self.cumulative_weights [-1] + p)

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            return find_index (self.cumulative_weights, self.U (gen)) [0]

class Bernouilli (RandomVariable):

    #public:

        def __init__ (self, p):
            super ().__init__ (None)
            self.U = Uniform ()
            self.p = p

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            if self.U (gen) < self.p: self.value = 1
            else: self.value = 0
            return self.value

class Binomial (RandomVariable):

    #public:

        def __init__ (self, n, p):
            super ().__init__ (None)
            self.U = Uniform ()
            self.p = p
            self.list = range (n)

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            for _i in self.list:
                if self.U (gen) < self.p: self.value += 1
            return self.value

class Geometric (RandomVariable):

    #public:

        def __init__ (self, p):
            super ().__init__ (None)
            self.X = Bernouilli (p)

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            while not self.X (gen): self.value += 1
            return self.value

class StarGeometric (RandomVariable):

    #public:

        def __init__ (self, p):
            super ().__init__ (None)
            self.X = Geometric (p)

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            self.value = self.X (gen) + 1 
            return self.value 

class NegativeBinomial (RandomVariable):

    #public:

        def __init__ (self, p, n):
            super ().__init__ (None) 
            self.X = Bernouilli (p) 
            self.n = n 

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            cpt = 0 
            while cpt < self.n:
                if self.X (gen): cpt += 1 
                self.value += 1 
            return self.value 

class BallUniform (RandomVariable):

    #public:

        def __init__ (self, d, r):
            super ().__init__ (None) 
            self.U = Uniform (-r, r) 
            self.sq_r = r ** 2 
            self.list = range (d)

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            while np.linalg.norm (self.value) > self.sq_r:
                self.value = [self.U (gen) for i in self.list] 
            return self.value 

class IntGamma (RandomVariable):

    #public:

        def __init__ (self, n):
            super ().__init__ (None) 
            self.U = Uniform () 
            self.n = n 
            self.list = range (n)

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            self.value = - mth.log (reduce (lambda x, y: x * y, [self.U (gen) for _ in self.list], 1))
            return self.value 

class FloatGamma (RandomVariable):

    #public:

        def __init__ (self, a):
            super ().__init__ (None) 
            pre_c = (a + E) / E 
            threshold = 1. / pre_c 
            inv_a = 1. / a 
            self.c = pre_c * inv_a 
            inv_c = 1. / self.c 
            self.f_g = lambda x: inv_c * mth.exp (-x) if x < 1. else inv_c * x ** (a - 1) 
            self.inv_fdr = lambda u: (pre_c * u) ** inv_a if u < threshold else - mth.log (inv_c * (1 - u)) 
            self.U = Uniform () 
            self.V = Uniform () 

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            while self.f_g (self.inv_fdr (self.V (gen))) < self.c * self.U (gen): pass 
            self.value = self.inv_fdr (self.V.current) 
            return self.value 

class Gamma (RandomVariable):

    #public:

        def __init__ (self, a):
            super ().__init__ (None) 
            int_a =  mth.floor (a) 
            frac_a = a - int_a 
            if int_a != 0: self.g_int = IntGamma (int_a) 
            if frac_a != 0.: self.g_float = FloatGamma (frac_a) 

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            try: self.value = self.g_int (gen) + self.g_float (gen) 
            except AttributeError:
                try: self.value = self.g_int (gen)
                except AttributeError: self.value = self.g_float (gen) 
            return self.value 

class Beta (RandomVariable):

    #public:

        def __init__ (self, a, b):
            super ().__init__ (None)
            a = a - 1
            b = b - 1
            super ().__init__ (0.)
            self.U = Uniform ()
            c = a ** (a) * b ** (b) / (a + b) ** (a + b)
            self.V = Uniform (0, c)
            self.f = lambda x: x ** (a) * (1. - x) ** (b)

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            while (self.V (gen) > self.f (self.U (gen))): pass
            self.value = self.U.current
            return self.value

class Poisson (RandomVariable):

    #public:

        def __init__ (self, t):
            super ().__init__ (None)
            self.U = Uniform ()
            self.e_t = mth.exp (-t)

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            u = 1
            cpt = -1
            while (u > self.e_t): 
                u *= self.U (gen)
                cpt += 1
            self.value = cpt
            return self.value

class StandardNormalBoxMuller (RandomVariable):

    #public:

        def __init__ (self):
            super ().__init__ (None)
            self.sq_R = Exponential (0.5)
            self.U = Uniform (0, 2 * mth.pi)
            self.flag = True
            self.R = 1

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            if (self.flag):
                self.sq_R (gen)
                self.U (gen)
                self.R = mth.sqrt (self.sq_R.current)
                self.value = self.R * mth.cos (self.U.current)
            else:
                self.value = self.R * mth.sin (self.U.current)
            self.flag = not self.flag
            return self.value

class StandardNormalMarsaglia (RandomVariable):

    #public:

        def __init__ (self):
            super ().__init__ (None)
            self.flag = True
            self.U = Uniform (-1, 1)
            self.V = Uniform (-1, 1)
            self.scale = 0

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            if (self.flag):
                sq_R = 2.
                while (sq_R > 1.):
                    u = self.U (gen)
                    v = self.V (gen)
                    sq_R = u * u + v * v
                self.scale = mth.sqrt (-2. * mth.log (sq_R) / sq_R)
                self.value = self.scale * self.U.current
            else:
                self.value = self.scale * self.V.current
            self.flag = not self.flag
            return self.value

class Normal (RandomVariable):

    #public:

        def __init__ (self, mean, standard_deviation, method='Marsaglia'):
            super ().__init__ (None)
            self.mean = mean
            self.standard_deviation = standard_deviation
            self.Z = StandardNormalMarsaglia () if method == 'Marsaglia' else StandardNormalBoxMuller ()

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            self.value = self.mean + self.standard_deviation * self.Z (gen) 
            return self.value

class StandardMultiNormal (RandomVariable):

    #public:

        def __init__ (self, dimension, method='Marsaglia'):
            super ().__init__ (None)
            self.Z = StandardNormalMarsaglia () if method == 'Marsaglia' else StandardNormalBoxMuller ()
            self.list = range (dimension)

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            self.value = np.array ([self.Z (gen) for _ in self.list])
            return self.value

class MultiNormal (RandomVariable):

    #public:
        
        def __init__ (self, dimension, mean, var, method='Marsaglia'):
            super ().__init__ (None)
            self.Z = StandardMultiNormal (dimension, method)
            self.mean = mean
            self.sqrt_var = np.linalg.cholesky (var)

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            self.value = self.mean + self.sqrt_var @ self.Z (gen)
            return self.value

class Choices (RandomVariable):

    #public:

        def __init__ (self, k, set):
            super ().__init__ (None)
            self.set = set
            n = len (set)
            self.indexes = range (n, n-k, -1)
            self.U = Uniform ()

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            proxy_set = self.set.copy ()
            self.value = [proxy_set.pop (int (index * self.U (gen))) for index in self.indexes]
            return self.value

class Folds (RandomVariable):

    #public:

        def __init__ (self, n_folds, set):
            super ().__init__ (None)
            self.set = set
            self.n_folds = n_folds
            self.n_fold = int (len (set) / n_folds)
            self.U = Uniform ()

        def __call__ (self, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            proxy_set = self.set.copy ()
            self.value = []
            for _ in range (self.n_folds):
                n = len (proxy_set)
                indexes = range (n, n-self.n_fold, -1)
                self.value.append ([proxy_set.pop (int (index * self.U (gen))) for index in indexes])
            self.value.append (proxy_set)
            return self.value