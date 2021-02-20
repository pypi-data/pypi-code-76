import mxdevtool as mx
import mxdevtool.utils as utils

from .pricing import *

# for pricing 
class EuropeanOption(mx.core_EuropeanOption, ScenPricing):
    def __init__(self, option_type: str, strike: float, maturityDate: mx.Date):
        self.option_type = utils.toOptionType(option_type)
        self.strike = strike
        self.maturityDate = utils.toDateCls(maturityDate)

        _option_type = mx.Option.Call if option_type == 'c' else mx.Option.Put
        super().__init__(_option_type, strike, maturityDate)        

    def required_path_args(self):
        return ['s1', 'discount']

    def withPricingParams_GBMConst(self, x0: float, rf: float, div: float, vol: float):
        self.setPricingParams_GBMConst(x0, rf, div, vol)
        return self

    # scen_data_d -> { pathname : ndarray(simulNum, timeGridSize) }
    def npv_path(self, scen_data_d, calc_kwargs):
        npv = 0.0
        
        tg = scen_data_d['_timegrid']

        params = self.required_path_args()

        S1 = params[0]
        DISCOUNT = params[1]

        # 필요한 것은 s1, discount
        path_s = scen_data_d[S1]
        path_discount = scen_data_d[DISCOUNT]

        mat_pos = tg.closestIndex_Date(self.maturityDate)
        
        for path in path_s:
            v = 0.0
            s_T = path[mat_pos]
            npv += max(s_T - self.strike, 0.0) * path_discount[mat_pos]

        return npv / len(path_s)

    def cf_path(self):
        pass


class AmericanOption(mx.core_AmericanOption, ScenPricing):
    def __init__(self, option_type: str, strike: float, maturityDate: mx.Date):
        self.option_type = utils.toOptionType(option_type)
        self.strike = strike
        self.maturityDate = utils.toDateCls(maturityDate)

        super().__init__(self.option_type, strike, maturityDate)

    def required_path_args(self):
        return ['s1', 'discount']

    def withPricingParams_GBMConst(self, x0: float, rf: float, div: float, vol: float):
        self.setPricingParams_GBMConst(x0, rf, div, vol)
        return self


class BermudanOption(mx.core_BermudanOption, ScenPricing):
    def __init__(self, option_type: str, strike: float, exerciseDates: list):
        self.option_type = utils.toOptionType(option_type)
        self.strike = strike
        self.exerciseDates = utils.toDateClsList(exerciseDates)

        super().__init__(self.option_type, strike, exerciseDates)

    def required_path_args(self):
        return ['s1', 'discount']

    def withPricingParams_GBMConst(self, x0: float, rf: float, div: float, vol: float):
        self.setPricingParams_GBMConst(x0, rf, div, vol)
        return self


class BarrierOption(mx.core_BarrierOption, ScenPricing):
    def __init__(self, option_type, barrier_type, 
                 barrier: float, rebate: float, strike: float, maturityDate: mx.Date):
        self.option_type = utils.toOptionType(option_type)
        self.barrier_type = utils.toBarrierType(barrier_type)
        self.barrier = barrier
        self.rebate = rebate
        self.strike = strike
        self.maturityDate = utils.toDateCls(maturityDate)

        super().__init__(self.option_type, self.barrier_type, barrier, rebate, strike, maturityDate)

    def required_path_args(self):
        return ['s1', 'discount']

    def withPricingParams_GBMConst(self, x0: float, rf: float, div: float, vol: float):
        self.setPricingParams_GBMConst(x0, rf, div, vol)
        return self
