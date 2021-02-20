import mxdevtool as mx
import mxdevtool.utils as utils


class BlackConstantVol(mx.core_BlackConstantVol):
    def __init__(self, refDate, vol, calendar=None, dayCounter=mx.Actual365Fixed()):
        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()
        
        self._refDate = refDate
        self._vol = vol
        self._calendar = _calendar # prevent None 
        self._dayCounter = dayCounter

        mx.core_BlackConstantVol.__init__(self, _refDate, vol, _calendar, dayCounter)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackConstantVol.__name__)

        refDate = mx.Date(d['refDate'])
        vol = d['vol']
        calendar = mx.calendarParse(d['calendar'])
        dayCounter = mx.dayCounterParse(d['dayCounter'])

        return BlackConstantVol(refDate, vol, calendar, dayCounter)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['vol'] = self._vol
        res['calendar'] = str(self._calendar)
        res['dayCounter'] = str(self._dayCounter)

        return res


# dates direct inputs
class BlackVarianceCurve(mx.core_BlackVarianceCurve):
    def __init__(self, refDate, dates, volatilities, strike=None, 
                interpolationType=mx.Interpolator1D.Linear, 
                dayCounter=mx.Actual365Fixed()):

        self._refDate = utils.toTypeCls(refDate, mx.Date)
        self._dates = utils.toTypeClsList(dates, mx.Date)
        self._volatilities = volatilities
        self._interpolationType = interpolationType
        self._dayCounter = dayCounter
        self._strike = strike

        mx.core_BlackVarianceCurve.__init__(self, self._refDate, self._dates, volatilities, interpolationType, dayCounter)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackVarianceCurve.__name__)

        refDate = mx.Date(d['refDate'])
        dates = utils.toTypeClsList(d['dates'], mx.Date)
        volatilities = d['volatilities']
        strike = d['strike']
        interpolationType = mx.interpolator1DParse(d['interpolationType'])
        dayCounter = mx.dayCounterParse(d['dayCounter'])

        return BlackVarianceCurve(refDate, dates, volatilities, strike, interpolationType, dayCounter)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['dates'] = utils.toStrList(self._dates)
        res['volatilities'] = self._volatilities
        res['strike'] = str(self._strike)
        res['interpolationType'] = mx.interpolator1DToString(self._interpolationType)
        res['dayCounter'] = str(self._dayCounter)

        return res


class BlackVarianceCurve2(BlackVarianceCurve):
    def __init__(self, refDate, periods, volatilities, strike=None,
                   interpolationType=mx.Interpolator1D.Linear, 
                   calendar=None,
                   dayCounter=mx.Actual365Fixed(), 
                   businessDayConvention=mx.ModifiedFollowing):
        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()

        #dates = [ _calendar.advance(refDate, p, businessDayConvention) for p in utils.toPeriodClsList(periods)]
        dates = utils.periodToDateList(refDate, periods, _calendar, businessDayConvention)

        self._calendar = _calendar
        self._businessDayConvention = businessDayConvention
        self._periods = utils.toStrList(periods)

        BlackVarianceCurve.__init__(self, refDate, dates, volatilities, strike, interpolationType, dayCounter)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackVarianceCurve2.__name__)

        refDate = mx.Date(d['refDate'])
        periods = d['periods']
        volatilities = d['volatilities']
        strike = d['strike']
        interpolationType = mx.interpolator1DParse(d['interpolationType'])
        calendar = mx.calendarParse(d['calendar'])
        dayCounter = mx.dayCounterParse(d['dayCounter'])
        businessDayConvention = mx.businessDayConventionParse(d['businessDayConvention'])

        return BlackVarianceCurve2(refDate, periods, volatilities, strike, interpolationType, 
                                calendar, dayCounter, businessDayConvention)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['periods'] = self._periods
        res['calendar'] = str(self._calendar)
        res['businessDayConvention'] = mx.businessDayConventionToString(self._businessDayConvention)

        super_d = super().toDict()
        super_d.pop('dates')

        res = { **res, **super_d }

        return res



# dates direct inputs
class BlackVarianceSurface(mx.core_BlackVarianceSurface):
    def __init__(self, refDate, dates, strikes, blackVols,
                   dayCounter=mx.Actual365Fixed()):
        self._refDate = utils.toDateCls(refDate)
        self._dates = utils.toDateClsList(dates)
        self._strikes = strikes
        self._blackVols = utils.toMatrixList(blackVols)
        self._dayCounter = dayCounter
        
        mx.core_BlackVarianceSurface.__init__(self, self._refDate, self._dates, strikes, self._blackVols, dayCounter)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackVarianceSurface.__name__)

        refDate = mx.Date(d['refDate'])
        dates = utils.toDateClsList(d['dates'])
        strikes = d['strikes']
        blackVols = d['blackVols']
        dayCounter = mx.dayCounterParse(d['dayCounter'])

        return BlackVarianceSurface(refDate, dates, strikes, blackVols, dayCounter)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        
        res['refDate'] = str(self._refDate)
        res['dates'] = utils.toStrList(self._dates)
        res['strikes'] = self._strikes
        res['blackVols'] = self._blackVols
        res['dayCounter'] = str(self._dayCounter)

        return res


class BlackVarianceSurface2(BlackVarianceSurface):
    def __init__(self, refDate, periods, strikes, blackVols,
                   calendar=None,
                   dayCounter=mx.Actual365Fixed(),
                   businessDayConvention=mx.ModifiedFollowing):
        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()

        dates = [ _calendar.advance(refDate, p, businessDayConvention) for p in periods ]
        
        self._calendar = _calendar
        self._businessDayConvention = businessDayConvention
        self._periods = utils.toStrList(periods)

        BlackVarianceSurface.__init__(self, refDate, dates, strikes, blackVols, dayCounter)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackVarianceSurface2.__name__)

        refDate = mx.Date(d['refDate'])
        periods = d['periods']
        strikes = d['strikes']
        blackVols = d['blackVols']
        calendar = mx.calendarParse(d['calendar'])
        dayCounter = mx.dayCounterParse(d['dayCounter'])
        businessDayConvention = mx.businessDayConventionParse(d['businessDayConvention'])

        return BlackVarianceSurface2(refDate, periods, strikes, blackVols, 
                                     calendar, dayCounter, businessDayConvention)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['periods'] = self._periods
        res['calendar'] = str(self._calendar)
        res['businessDayConvention'] = mx.businessDayConventionToString(self._businessDayConvention)
        
        super_d = super().toDict()
        super_d.pop('dates')

        res = { **res, **super_d }

        return res

