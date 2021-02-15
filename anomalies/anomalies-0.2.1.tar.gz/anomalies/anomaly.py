import numpy as np
#!/usr/bin/env python3
'''
Implementation of arXiv:1905.13729:

A set of $N$  $n_\alpha$ integers that satisfy Diophantine 
equations
$$ 
\sum_{\alpha=1}^{N}n_{\alpha}=0\,,\qquad  \sum_{\alpha=1}^{N}n_{\alpha}^3=0\,,
$$
can be parametrized as a function of two sets of integers $l$ and $k$, 
with dimensions $(N-3)/2$ and $(N-1)/2$ for $N$ odd, 
or $N/2-1$ and $N/2-1$ for $N$ even
'''
def _z(l,k,sort=True,reverse=False):
    '''
    Implementation of arXiv:1905.13729
    For l,k two set of same dimensions (or k with an extra dimension)
    return a builded array z, such that
     sum( z )=0
     sum( z**3)=0
    '''
    l=list(l)
    k=list(k)
    #Build vector-like solutions x,y
    if len(l)==len(k) :
        x=np.array( [l[0]]+k+[-l[0]]+[-i for i in k ] )
        y=np.array( [0,0] +l        +[-i for i in l ] )
    else:
        x=np.array( [0]+k+[-i for i in k ] )
        y=np.array( l+[k[0]]+[0]+[-i for i in l ]+[-k[0]])
    xfac=0
    yfac=0
    # Build not trivial solution
    zz=(x*y**2).sum()*x-(x**2*y).sum()*y
    if sort:
        zz=sorted( zz ,key=abs, reverse=reverse ) 
    return np.array(zz)

class cfree(object):
    '''
    Add attributes to the _z function:
    * `gcd`: general common denominator
    * `simplified`: solution with gcd=1 
    '''
    def __call__(self,l,k,sort=True,reverse=False):
        zz=_z(l,k,sort=sort,reverse=reverse)
        self.gcd=np.gcd.reduce(zz)
        self.simplified=(zz/self.gcd).astype(int)
        return zz
    
free=cfree()
if __name__=='__main__':
    l=input('List of integers → l=')
    k=input('List of integers → k=')
    sltn=free(eval(l),eval(k))
    print( free.simplified )

