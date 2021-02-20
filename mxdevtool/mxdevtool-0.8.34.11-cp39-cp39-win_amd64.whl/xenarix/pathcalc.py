from mxdevtool.mxdevtool import YieldTermStructure
import mxdevtool as mx
import mxdevtool.termstructures as ts
import numpy as np
import inspect, numbers


class DeterministicParameter(mx.core_DeterministicParameter):
    def __init__(self, times, values):
        self._times = times
        self._values = values
        mx.core_DeterministicParameter.__init__(self, times, values)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        if isinstance(d, numbers.Number):
            return DeterministicParameter(['1Y', '100Y'], [d, d])

        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, DeterministicParameter.__name__)

        times = d['times']
        values = d['values']

        return DeterministicParameter(times, values)

    def toDict(self):
        res = dict()
        
        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['times'] = self._times
        res['values'] = self._values

        return res

# models ----------------------------

class GBMConst(mx.core_GBMConstModel):
    def __init__(self, name, x0, rf, div, vol):
        self._x0 = x0
        self._rf = rf
        self._div = div
        self._vol = vol

        mx.core_GBMConstModel.__init__(self, name, x0, rf, div, vol)


class GBM(mx.core_GBMModel):
    def __init__(self, name, x0, rfCurve, divCurve, volTs):

        self._x0 = x0
        self._rfCurve = rfCurve
        self._divCurve = divCurve
        self._volTs = volTs

        mx.core_GBMModel.__init__(self, name, x0, rfCurve, divCurve, volTs)


class Heston(mx.core_HestonModel):
    def __init__(self, name, x0, rfCurve, divCurve, v0, volRevertingSpeed, longTermVol, volOfVol, rho):

        self._x0 = x0
        self._rfCurve = rfCurve
        self._divCurve = divCurve
        self._v0 = v0
        self._volRevertingSpeed = volRevertingSpeed
        self._longTermVol = longTermVol
        self._volOfVol = volOfVol
        self._rho = rho

        mx.core_HestonModel.__init__(self, name, x0, rfCurve, divCurve, v0, volRevertingSpeed, longTermVol, volOfVol, rho)


class CIR1F(mx.core_CIR1FModel):
    def __init__(self, name, r0, alpha, longterm, sigma):
        self._r0 = r0
        self._alpha = alpha
        self._longterm = longterm
        self._sigma = sigma

        mx.core_CIR1FModel.__init__(self, name, r0, alpha, longterm, sigma)


class Vasicek1F(mx.core_Vasicek1FModel):
    def __init__(self, name, r0, alpha, longterm, sigma):

        self._r0 = r0
        self._alpha = alpha
        self._longterm = longterm
        self._sigma = sigma

        mx.core_Vasicek1FModel.__init__(self, name, r0, alpha, longterm, sigma)


class HullWhite1F(mx.core_HullWhite1FModel):
    def __init__(self, name, fittingCurve, alphaPara, sigmaPara):

        self._fittingCurve = fittingCurve
        self._alphaPara = alphaPara
        self._sigmaPara = sigmaPara

        mx.core_HullWhite1FModel.__init__(self, name, fittingCurve, alphaPara, sigmaPara)
    
    # def calibrate(self, volMatrix, expiries, tenors, vols_using=None, familyname='default', tool='swaption'):
    #     mx.core_HullWhite1FModel.calibrate(self, volMatrix, expiries, tenors, vols_using, familyname)


class BK1F(mx.core_BK1FModel):
    def __init__(self, name, fittingCurve, alphaPara, sigmaPara):

        self._fittingCurve = fittingCurve
        self._alphaPara = alphaPara
        self._sigmaPara = sigmaPara

        mx.core_BK1FModel.__init__(self, name, fittingCurve, alphaPara, sigmaPara)


class G2Ext(mx.core_GTwoExtModel):
    def __init__(self, name, fittingCurve, alpha1, sigma1, alpha2, sigma2, corr):
        
        self._fittingCurve = fittingCurve
        self._alpha1 = alpha1
        self._sigma1 = sigma1
        self._alpha2 = alpha2
        self._sigma2 = sigma2
        self._corr = corr

        mx.core_GTwoExtModel.__init__(self, name, fittingCurve, alpha1, sigma1, alpha2, sigma2, corr)


# operators -----------------------------
class PlusOper(mx.core_PlusOperCalc):
    def __init__(self, pc):
        self._pc = pc
        mx.core_PlusOperCalc.__init__(self, pc)


class MinusOper(mx.core_MinusOperCalc):
    def __init__(self, pc):
        self._pc = pc
        mx.core_MinusOperCalc.__init__(self, pc)


class AdditionOper(mx.core_AdditionOperCalc):
    def __init__(self, pc1, pc2):
        self._pc1 = pc1
        self._pc2 = pc2
        mx.core_AdditionOperCalc.__init__(self, pc1, pc2)


class SubtractionOper(mx.core_SubtractionOperCalc):
    def __init__(self, pc1, pc2):
        self._pc1 = pc1
        self._pc2 = pc2
        mx.core_SubtractionOperCalc.__init__(self, pc1, pc2)


class MultiplicationOper(mx.core_MultiplicationOperCalc):
    def __init__(self, pc1, pc2):
        self._pc1 = pc1
        self._pc2 = pc2
        mx.core_MultiplicationOperCalc.__init__(self, pc1, pc2)


class DivisionOper(mx.core_DivisionOperCalc):
    def __init__(self, pc1, pc2):
        self._pc1 = pc1
        self._pc2 = pc2
        mx.core_DivisionOperCalc.__init__(self, pc1, pc2)        


# calcs -----------------------------

class Identity(mx.core_IdentityWrapperCalc):
    def __init__(self, name, pc):
        self._pc = pc

        mx.core_IdentityWrapperCalc.__init__(self, name, pc)

    def toDict(self):
        return self._pc.toDict()


class YieldCurve(mx.core_YieldCurveValueCalc):
    def __init__(self, name, yieldCurve, output_type='spot', compounding=mx.Compounded):

        self._yieldCurve = yieldCurve
        self._output_type = output_type
        self._compounding = compounding

        mx.core_YieldCurveValueCalc.__init__(self, name, yieldCurve, output_type, compounding)


class FixedRateBond(mx.core_FixedRateCMBondPositionCalc):
    def __init__(self, name, ir_pc, 
                 notional=10000, 
                 fixedRate=0.0, 
                 couponTenor=mx.Period(3, mx.Months), 
                 maturityTenor=mx.Period(3, mx.Years), 
                 discountCurve=None):
        if discountCurve is None:
            raise Exception('discount curve is required')
        
        self._ir_pc = ir_pc
        self._notional = notional
        self._fixedRate = fixedRate
        self._couponTenor = couponTenor
        self._maturityTenor = maturityTenor
        self._discountCurve = discountCurve
        
        mx.core_FixedRateCMBondPositionCalc.__init__(self, name, ir_pc, notional, fixedRate, couponTenor, maturityTenor, discountCurve)



class Returns(mx.core_ReturnWrapperCalc):
    def __init__(self, name, pc, return_type='return'):
        self._pc = pc
        self._return_type = return_type

        mx.core_ReturnWrapperCalc.__init__(self, name, pc, return_type)


class Shift(mx.core_ShiftWrapperCalc):
    def __init__(self, name, pc, shift, fill_value=0.0):
        self._pc = pc
        self._shift = shift
        self._fill_value = fill_value

        mx.core_ShiftWrapperCalc.__init__(self, name, pc, shift, fill_value)


class ConstantValue(mx.core_ConstantValueCalc):
    def __init__(self, name, v):
        self._v = v
        mx.core_ConstantValueCalc.__init__(self, name, v)
        

class ConstantArray(mx.core_ConstantArrayCalc):
    def __init__(self, name, arr):
        self._arr = arr
        mx.core_ConstantArrayCalc.__init__(self, name, arr)
        

class LinearOper(mx.core_LinearOperWrapperCalc):
    def __init__(self, name, pc, multiple=1.0, spread=0.0):
        self._pc = pc
        self._multiple = multiple
        self._spread = spread
        mx.core_LinearOperWrapperCalc.__init__(self, name, pc, multiple, spread)


class UnaryFunction(mx.core_UnaryFunctionWrapperCalc):
    def __init__(self, name, pc, func_type):
        self._pc = pc
        self._func_type = func_type
        mx.core_UnaryFunctionWrapperCalc.__init__(self, name, pc, func_type)


class BinaryFunction(mx.core_BinaryFunctionWrapperCalc):
    def __init__(self, name, pc1, pc2, func_type):
        self._pc1 = pc1
        self._pc2 = pc2
        self._func_type = func_type
        mx.core_BinaryFunctionWrapperCalc.__init__(self, name, pc1, pc2, func_type)


class MultaryFunction(mx.core_MultaryFunctionWrapperCalc):
    def __init__(self, name, pc_list, func_type):
        self._pc_list = pc_list
        self._func_type = func_type
        mx.core_MultaryFunctionWrapperCalc.__init__(self, name, pc_list, func_type)


class Overwrite(mx.core_OverwriteWrapperCalc):
    def __init__(self, name, pc, start_pos, arr):
        self._pc = pc
        self._arr = arr
        mx.core_OverwriteWrapperCalc.__init__(self, name, pc, start_pos, arr)


class Fund(mx.core_FundWrapperCalc):
    def __init__(self, name, weights, pc_list):
        self._weights = weights
        self._pc_list = pc_list        
        mx.core_FundWrapperCalc.__init__(self, name, weights, pc_list)

# model
class SpotRate(mx.core_SpotRateCalc):
    def __init__(self, name, ir_pc, maturityTenor, compounding=mx.Compounded):
        self._ir_pc = ir_pc
        self._maturityTenor = maturityTenor
        self._compounding = compounding
        mx.core_SpotRateCalc.__init__(self, name, ir_pc, maturityTenor, compounding)


class ForwardRate(mx.core_ForwardRateCalc):
    def __init__(self, name, ir_pc, startTenor, maturityTenor, compounding=mx.Compounded):
        self._ir_pc = ir_pc
        self._startTenor = startTenor
        self._maturityTenor = maturityTenor
        self._compounding = compounding
        mx.core_ForwardRateCalc.__init__(self, name, ir_pc, startTenor, maturityTenor, compounding)


class DiscountFactor(mx.core_DiscountFactorCalc):
    def __init__(self, name, ir_pc):
        self._ir_pc = ir_pc
        mx.core_DiscountFactorCalc.__init__(self, name, ir_pc)


class DiscountBond(mx.core_DiscountBondCalc):
    def __init__(self, name, ir_pc, maturityTenor):
        self._ir_pc = ir_pc
        self._maturityTenor = maturityTenor
        mx.core_DiscountBondCalc.__init__(self, name, ir_pc, maturityTenor)


# math functions ---------------------

def min(models, name=None):
    if name is None:
        name = '_'.join([m.name() for m in models]) + 'min'
    return mx.core_MultaryFunctionWrapperCalc(name, models, 'min')


def max(models, name=None):
    if name is None:
        name = '_'.join([m.name() for m in models]) + 'max'
    return mx.core_MultaryFunctionWrapperCalc(name, models, 'max')



