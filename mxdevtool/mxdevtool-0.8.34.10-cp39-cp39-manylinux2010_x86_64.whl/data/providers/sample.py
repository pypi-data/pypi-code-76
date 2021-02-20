import mxdevtool as mx
import mxdevtool.termstructures as ts
import mxdevtool.quotes as qt


# class SampleMarketData(mx.MarketData):
#     def __init__(self, data=None):
#         mx.MarketData.__init__(self, data)

#     def get_quote_d(self, arg):
#         # extract in [] ?
#         # ex : irskrw[3m] -> irskrw , 3m
#         return 0.02


class SampleMarketDataProvider(mx.MarketDataProvider):

    def __init__(self):
        self.sample_data = None
        self.initialize()

    def initialize(self):
        m = mx.MarketData()

        refDate = mx.Date(2021, 1, 21)

        m.quote['kospi2_ni225_corr'] = { 'v': 0.3 }
        m.quote['kospi2'] = { 'v': 400 }
        m.quote['spx'] = { 'v': 3700 }
        m.quote['ni225'] = { 'v': 28000 }
        m.quote['cd91'] = { 'v': 0.025 }
        m.quote['alpha1'] = { 'v': 0.1 }
        
        zerocurve1 = { 
            'clsnm' : ts.ZeroYieldCurve.__name__,
            'refDate' : str(refDate),
            'periods': ['3m', '20Y'],
            'zeroRates': [0.03, 0.03],
            'interpolationType': 'Linear',
            'extrapolationType': 'FlatForward',
            'calendar': str(mx.SouthKorea()),
            'dayCounter': str(mx.Actual365Fixed()),
            'businessDayConvention': mx.businessDayConventionToString(mx.ModifiedFollowing),
            'compounding': mx.compoundingToString(mx.Compounded)
        }

        m.yieldCurve['zerocurve1'] = zerocurve1

        zerocurve2 = ts.ZeroYieldCurve(refDate, ['3m', '20Y'], [0.03, 0.03])
        m.yieldCurve['zerocurve2'] = zerocurve2.toDict()

        const_volTs1 = { 
            'clsnm' : ts.BlackConstantVol.__name__,
            'refDate' : str(refDate),
            'vol': 0.25,
            'calendar': str(mx.SouthKorea()),
            'dayCounter': str(mx.Actual365Fixed()),
        }

        m.volTs['const_volTs1'] = const_volTs1

        const_volTs2 = ts.BlackConstantVol(refDate, 0.25)
        m.volTs['const_volTs2'] = const_volTs2.toDict()

        self.sample_data = m

    def get_data(self, **kwargs):
        return self.sample_data



class SampleMetaInfoMarketDataProvider(mx.MarketDataProvider):
    def __init__(self, meta=None):
        self.meta = meta
        self.data = None

        self.initialize()

    def initialize(self):
        self.meta = {
            'quote':{
                'usdkrw':   { 'clsnm': qt.FxRateQuote.__name__ },
                'usdkrw_f': { 'clsnm': qt.ForwardFxRateQuote.__name__ }
            },
            'yieldCurve':
            {
                'irskrw':  { 'clsnm': ts.ZeroYieldCurve.__name__, 'calendar': str(mx.SouthKorea()) },
            },
            'volTs':
            {

            }
        }

        self.data = {
            '2021-01-21': {
                'quote':
                {
                    'usdkrw': { 'v': 1100 },
                    'kospi2': { 'volumns': 100000, 'v': 400 }
                },
                'yieldCurve':
                {
                    'irskrw': { 'periods': ['3m', '6m', '9m', '1y'], 'rates': [0.01, 0.011, 0.012, 0.013] }
                },
                'volTs':
                {
                    
                },
                'timestamp': '20210121T03300'


            },
        }

    def with_meta(self, data):
        for ctg in ['quote', 'yieldcurve', 'volTs']:
            d = data[ctg]
            meta_d = self.meta[ctg]

            for k, v in d.items():
                if k in meta_d:
                    v.update(meta_d[k])
                else:
                    pass
        
        return data

    def get_data(self, **kwargs):
        m = mx.MarketData()

        refDate = mx.Date(2021, 1, 21)
        res = self.data[str(refDate)]
        res_with_meta = self.with_meta(res)

        return res_with_meta
        


