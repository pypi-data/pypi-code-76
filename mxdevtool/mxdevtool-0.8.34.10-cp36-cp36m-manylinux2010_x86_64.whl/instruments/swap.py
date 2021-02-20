import mxdevtool as mx


class SwapFamilyHelper:
    def __init__(self, family_name):
        self.family_name = family_name
        self.iborIndex = mx.IborIndexExt('krwcd', '3M')
        self.calendar = mx.SouthKorea()
        self.convention = mx.ModifiedFollowing


class VanillaSwap(mx.core_VanillaSwapExt):
    def __init__(self, side, notional, settlementDate, maturityTenor, 
                 fixedRate, iborIndex, spread, family_name, engine):

        self.side = side 
        self.notional = notional
        self.settlementDate = settlementDate
        self.maturityTenor = maturityTenor
        self.fixedRate = fixedRate
        self.iborIndex = iborIndex
        self.spread = spread
        self.family_name = family_name
        self.engine = engine

        mx.core_VanillaSwapExt.__init__(self, side, notional, settlementDate, maturityTenor, fixedRate, iborIndex, spread, family_name, engine)

    # def withPricingParams_Curve(self, yieldCurve):
    #     self.setPricingParams_Curve(yieldCurve)
    #     return self


class Swaption(mx.core_Swaption):
    def __init__(self, swap, exerciseDate, engine):
        mx.core_Swaption.__init__(self, swap, exerciseDate)
        self.setPricingEngine(engine)
        self.swap = swap
        self.exerciseDate = exerciseDate


def makeSwap(side=mx.VanillaSwap.Receiver, notional=10000, 
             maturityTenor=mx.Period(3, mx.Years),
             fixedRate=0.01, spread=0.0, settlementDate=None,
             yieldCurve=None, family_name='krwirs'):

    if not isinstance(yieldCurve, mx.YieldTermStructure):
        raise Exception('yieldCurve is required')

    fh = SwapFamilyHelper(family_name)

    calendar = fh.calendar
    bdc = fh.convention
    iborIndex = fh.iborIndex

    if settlementDate is None:
        date = mx.Date.todaysDate()
        settlementDate = calendar.advance(date, '1d', bdc)
    
    engine = mx.core_VanillaSwapExtPartialGreekEngine(yieldCurve,[])
    swap = VanillaSwap(side, notional, settlementDate, maturityTenor, fixedRate, iborIndex, spread, family_name, engine)

    # print('swap npv : ', swap.NPV())

    return swap


def makeSwaption(side=mx.VanillaSwap.Receiver, notional=10000, expiryTenor=mx.Period(1, mx.Years), 
                 maturityTenor=mx.Period(3, mx.Years), strike=None, settlementDate=None, yieldCurve=None, vol=0.3, family_name='irskrw_krccp'):
    
    fh = SwapFamilyHelper(family_name)
    calendar = fh.calendar
    bdc = fh.convention

    if settlementDate is None:
        date = mx.Date.todaysDate()
        expiryDate = calendar.advance(date, expiryTenor, bdc)
    else:
        expiryDate = calendar.advance(settlementDate, expiryTenor, bdc)
    
    if strike is None:
        temp_swap = makeSwap(side, notional, maturityTenor, 0.0, 0.0, expiryDate, yieldCurve, family_name)
        fixedRate = temp_swap.fairRate()

    swap = makeSwap(side, notional, maturityTenor, fixedRate, 0.0, expiryDate, yieldCurve, family_name)
    engine = mx.core_BlackSwaptionEngine(yieldCurve, vol)

    return Swaption(swap, expiryDate, engine)


if __name__ == "__main__":
    pass
    