# %%
import multiprocessing

class MultiprocessingWrapper:
    
    def __init__(self, single_func, global_params = [], log_module = 10e5, njobs=None):
        
        self.global_params = global_params
        self.single_func = single_func
        self.log_module = log_module

        if njobs is None:
            self.njobs = multiprocessing.cpu_count()
        else:
            self.njobs = njobs
        
    def mp_func_single(self, item_tuple):
        idx, item = item_tuple
        if idx % self.log_module == 0 or idx +1 == self.data_length:
            print("index " + str(idx) + " out of " + str(self.data_length) + " input data")
            
        return self.single_func(item, *self.global_params)
    
    def mp_func(self, data):
        self.data_length = len(data) * 1.0
        
        result = []
        with multiprocessing.Pool(self.njobs) as p:
            results = p.map(self.mp_func_single, enumerate(data))
        return results
    
    def testfunc(item, power, dummy_2):
        return item ** power
    def test():
        import time
        data =list(range(60))
        
        power = 2
        globalpar_2 = "random"
        global_params = [power, globalpar_2] # the order must be same with the single_func; item, globalpar_1, globalpar_2
        
        mpw = MultiprocessingWrapper(MultiprocessingWrapper.testfunc, global_params, log_module= 18)
        mpw.mp_func(data)
        
# MultiprocessingWrapper.test()
    
from functools import partial
