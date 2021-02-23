# coding: utf-8

import numpy as np

from sample.toolbox.integral.integral import Int

class Integral (Int):

    #public:

        def __init__ (self, func, lft, rgt):
            step = rgt - lft
            val_lft = func (lft)
            val_rgt = func (rgt)
            super ().__init__ (func, step, [lft, rgt], 0.5 * step * (val_lft + val_rgt))

    #private:

        def refine (self):            
            size = len (self.curr.pts)
            def get_val (idx):
                idx0 = idx
                idx1 = idx+1
                lft = self.curr.pts [idx0]
                rgt = self.curr.pts [idx1]
                mid = 0.5 * (lft + rgt)
                self.curr.pts.insert (idx1, mid)
                idx += 1
                return mid
            val = np.array ([get_val (idx) for idx in range (size-1)])
            return np.sum (self.func (val))
        
        
        
        
            
            
