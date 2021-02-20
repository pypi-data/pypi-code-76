import mxdevtool as mx
import mxdevtool.xenarix as xen
import mxdevtool.shock as mx_s
import mxdevtool.utils as utils

import statistics

from .outputs import *

# for inherit
class ScenPricing:
    def get_reduce_func(self, func_name):
        if func_name == 'aver':
            return statistics.mean
        else:
            return statistics.mean
            
    def required_path_args(self):
        raise Exception('this method must be inherited')

    def check_calc_args(self, outputs: list, shm: mx_s.ShockScenarioModel, **kwargs):
        # checking required args of this class
        for arg in self.required_path_args():
            if not arg in kwargs:
                raise Exception("argument is required - {0} -> {1}".format(arg, self.required_args))
            else:
                pass

        # checking shock exist in shm for outputs
        for otp in outputs:
            shm.check_shocknames_exist(otp.shock_scen_args)

        # checking args exist in shm
        for k, path_name in kwargs.items():
            shm.check_pathname_exist(path_name)

    # tensorflow ?
    def calculateScen(self, outputs: list, shm: mx_s.ShockScenarioModel, reduce, path_kwargs=dict(), calc_kwargs=dict()):
        self.check_calc_args(outputs, shm, **path_kwargs)
        reduce_fun = self.get_reduce_func(reduce)
        res = []

        # type check
        if not all([isinstance(otp, Output) for otp in outputs]):
            raise Exception('Output class is required - {0}'.format(outputs))

        for otp in outputs:
            params = self.required_path_args()
            scenNm_param_tuples = [(path_kwargs.get(nm), nm) for nm in params]
            shocked_scen_data_d = shm.select_shocked_scen_data_d(scenNm_param_tuples)

            v = otp.func(shocked_scen_data_d, calc_kwargs, self.npv_path)
            res.append(v)

        return res

    def withPricingParams_Model(self, model):

        if isinstance(model, xen.GBMConst):
            self.setPricingParams_GBMConst(model.x0, model.rf, model.div, model.vol)
        elif isinstance(model, xen.GBM):
            self.setPricingParams_GBM(model.x0, model.rfCurve, model.divCurve, model.volTs)
        else:
            raise Exception('unknown model - {0}'.format(model))

        return self

