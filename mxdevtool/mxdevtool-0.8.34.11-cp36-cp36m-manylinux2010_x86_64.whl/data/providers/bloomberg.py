import os, sys, datetime, inspect, collections

import mxdevtool as mx
import mxdevtool.termstructures as ts
import mxdevtool.quotes as qt

from mxdevtool.data.providers import MetaInfoMarketDataProvider
from collections import namedtuple

RequestItem = namedtuple('RequestItem', ['name', 'ticker', 'field'])

BLP_DLL_PATH = '.'
BLP_REQUEST_TIMEOUT = 1000
BLP_RESPONSE_MAX_COUNT = 100

QUOTE_DEFAULT_FLDNAME='PX_LAST'
IRCURVE_DEFAULT_FLDNAME='CURVE_TENOR_RATES'
EQVOL_DEFAULT_FLDNAME='IVOL_SURFACE_MONEYNESS'

RAW_DATA_RATES_NAME = 'rates'
RAW_DATA_PERIODS_NAME = 'periods'
RAW_DATA_VOLS_NAME = 'vols'
RAW_DATA_EXPIRYDATES_NAME = 'expirydates'
RAW_DATA_MONEYNESSES_NAME = 'moneynesses'
RAW_DATA_STRIKES_NAME = 'strikes'
RAW_DATA_DIVIDENDS_NAME = 'divedends'

# with os.add_dll_directory('<path to blpapi dlls>'):
#     import blpapi

import blpapi


class FieldParser:
    def __init__(self):
        self.parser_func_d = dict()

        self.parser_func_d[QUOTE_DEFAULT_FLDNAME] = self.parse_default_qt
        self.parser_func_d[IRCURVE_DEFAULT_FLDNAME] = self.parse_default_yc
        self.parser_func_d[EQVOL_DEFAULT_FLDNAME] = self.parse_default_vts


    def parse_default_qt(self, **kwargs):
        d = dict()
        fieldData = kwargs['fieldData']
        d['v'] = fieldData.getElementAsFloat(QUOTE_DEFAULT_FLDNAME)
        return d

    def parse_default_yc(self, **kwargs):
        d = dict()
        fieldData = kwargs['fieldData']
        refDate = kwargs['refDate']

        items = fieldData.getElement(IRCURVE_DEFAULT_FLDNAME)
        periods = []
        rates = []

        for item in items.values():
            periods.append(item.getElementAsString('Tenor'))
            rates.append(item.getElementAsFloat('Mid Yield') / 100.0)
        
        d['refDate'] = str(refDate)
        d[RAW_DATA_PERIODS_NAME] = periods
        d[RAW_DATA_RATES_NAME] = rates

        return d

    def parse_default_vts(self, **kwargs):
        d = dict()
        fieldData = kwargs['fieldData']
        refDate = kwargs['refDate']
        items = fieldData.getElement(EQVOL_DEFAULT_FLDNAME)

        # periods = []
        expirydates = []
        moneynesses = []
        strikes = []
        vols = []
        divedends = []

        for item in items.values():
            # period = (exdate.year() - refDate.year()) * 12 + (exdate.month() - refDate.month())
            # periods.append(str(period) + 'M')
            moneynesses.append(item.getElementAsFloat('Moneyness'))

            exdate = mx.dateParse_yyyymmdd(item.getElementAsString('Expiry Date'))

            expirydates.append(str(exdate))
            strikes.append(item.getElementAsFloat('Strike'))
            vols.append(item.getElementAsFloat('Implied Volatility') / 100.0)
            divedends.append(item.getElementAsFloat('Dividend') / 100.0)

        d['refDate'] = str(refDate)

        d[RAW_DATA_EXPIRYDATES_NAME] = expirydates
        d[RAW_DATA_MONEYNESSES_NAME] = moneynesses
        d[RAW_DATA_STRIKES_NAME] = strikes
        d[RAW_DATA_VOLS_NAME] = vols
        d[RAW_DATA_DIVIDENDS_NAME] = divedends

        return d


class BloombergMarketDataProvider(MetaInfoMarketDataProvider):
    def __init__(self, config: dict):
        MetaInfoMarketDataProvider.__init__(self, config.get('meta'))

        self.config = config
        self.requests = self.config['requests']

        self.parser_func_d = config.get('parser')

        if self.parser_func_d is None:
            self.parser_func_d = FieldParser().parser_func_d

        #self.ticker_name_d = dict()
        self.ticker_corrid_name_tup_list = []
        self.session = None

        self.connect()
        self.initialize()

    def _sendRequest(self, securities, fields, corrId):
        service = self.session.getService('//blp/refdata')
        request = service.createRequest('ReferenceDataRequest')
        for sc in securities:
            request.append("securities", sc)

        for fld in fields:
            request.append("fields", fld)

        self.session.sendRequest(request, correlationId=blpapi.CorrelationId(corrId))

    def initialize(self):
        # make ticker names dictionary for results mapping
        names = []
        for corrid, item_d in self.requests.items():
            for name, d in item_d.items():
                ticker = d['ticker']

                tcn = (name, ticker, corrid)
                # self.ticker_corrid_name_tup_list.append(tcn)
                names.append(name)

        # check name duplication
        name_duplications = [item for item, count in collections.Counter(names).items() if count > 1]
        if len(name_duplications) > 0:
            raise Exception('duplicated name is exist - {0}'.format(name_duplications))

    def connect(self):
        options = blpapi.SessionOptions()
        options.setServerHost('localhost')
        options.setServerPort(8194)

        self.session = blpapi.Session(options)

        self.session.start()
        if not self.session.openService('//blp/refdata'):
            print('error openService')

    def disconnect(self):
        self.session.stop()

    def _parse_response(self, refDate: mx.Date, event, res_d: dict):
        try:
            # 각각의 결과(corrId별)에 ticker 에 여러개의 field가 들어있고,
            # request 정보를 이용해서 자기가 알아서 가져오는 방식
            for msg in event:
                corrId = msg.correlationIds()[0].value()
                for securityData in msg.getElement('securityData').values():
                    if securityData.hasElement('securityError'):
                        continue
                    
                    ticker = securityData.getElementAsString('security')
                    fieldData = securityData.getElement('fieldData')

                    res = dict()
                    for name, item in self.requests[corrId].items():
                        item_ticker = item['ticker']
                        field = item['field']
                        
                        if ticker == item_ticker:
                            parser_func = self.parser_func_d[field]
                            res_d[corrId][name] = parser_func(refDate=refDate, fieldData=fieldData)

        except:
            raise 

    def _request_rt(self):
        res_d = dict()

        try:
            ticker_set = set()
            field_set = set()

            for ctg, item_d in self.requests.items():
                res_d_ctg_d = dict()
                for k, v in item_d.items():
                    ticker_set.add(v['ticker'])
                    field_set.add(v['field'])
                    res_d_ctg_d[k] = None

                self._sendRequest(securities=ticker_set, fields=field_set, corrId=ctg)
                
                res_d[ctg] = res_d_ctg_d


            res_d['timestamp'] = datetime.datetime.now().replace(microsecond=0).isoformat()

            count = 0

            refDate = mx.Date.todaysDate()

            while count < BLP_RESPONSE_MAX_COUNT:
                event = self.session.nextEvent(BLP_REQUEST_TIMEOUT)

                if event.eventType() == event.RESPONSE:
                    self._parse_response(refDate, event, res_d)
                elif event.eventType() == event.TIMEOUT:
                    break
                else:
                    pass
                
                count += 1

        except:
            self.disconnect()
            raise

        return res_d

    def _request_hist(self, refDate: mx.Date):
        pass

    def with_meta(self, data: dict) -> dict:
        # map to class argument name from raw data name
        def rename(target: dict, ori_nm: str, new_nm: str):
            target[new_nm] = target[ori_nm]
            target.pop(ori_nm)

        def remove_others(clsnm: str, target: dict):
            class_instance = globals()['ts'] .__dict__[clsnm]
            init = getattr(class_instance, "__init__", None)
            required_args = inspect.signature(init).parameters

            remove = [k for k in target if k not in required_args]
            remove.remove(mx.CLASS_TYPE_NAME)
            for k in remove: del target[k]

        # insert metainfo to raw data
        for ctg in [mx.MarketData.CTG_QUOTE_NAME, mx.MarketData.CTG_YIELDCURVE_NAME, mx.MarketData.CTG_VOLTS_NAME]:
            d = data[ctg]

            meta_d = self.meta.get(ctg)

            if meta_d is None:
                continue

            for k, v in d.items():
                if k in meta_d:
                    v.update(meta_d[k])
                else:
                    pass

        # processing data using metainfo
        ## yieldCuve
        for yc in data[mx.MarketData.CTG_YIELDCURVE_NAME].values():
            clsnm = yc.get(mx.CLASS_TYPE_NAME)
            if clsnm is None:
                continue
            
            if clsnm == ts.ZeroYieldCurve.__name__:
                rename(yc, RAW_DATA_RATES_NAME, 'zeroRates')
            elif clsnm == ts.BootstapSwapCurveCCP.__name__:
                rename(yc, RAW_DATA_RATES_NAME, 'quotes')
        ## volTs
        for vts in data[mx.MarketData.CTG_VOLTS_NAME].values():
            clsnm = vts.get(mx.CLASS_TYPE_NAME)

            # todo - non equit type does not use IVOL_SURFACE_MONEYNESS ticker must be added
            vts_moneynesses = vts[RAW_DATA_MONEYNESSES_NAME]
            vts_strikes = vts[RAW_DATA_STRIKES_NAME]
            vts_expirydates = vts[RAW_DATA_EXPIRYDATES_NAME]
            vts_vols = vts[RAW_DATA_VOLS_NAME]

            if clsnm == ts.BlackVarianceCurve.__name__:
                selected_moneyness = vts.get('selected_moneyness')
                
                if selected_moneyness is None:
                    selected_moneyness = 1.0

                # moneyness existance check
                if not selected_moneyness in vts_moneynesses:
                    raise Exception('selected moneyness does not exist - {0}, {1}'.format(selected_moneyness, vts[RAW_DATA_MONEYNESSES_NAME]))
                
                dates = []
                volatilities = []

                for m, d, v in zip(vts_moneynesses, vts_expirydates, vts_vols):
                    if m == selected_moneyness:
                        dates.append(d)
                        volatilities.append(v)

                vts['dates'] = dates
                vts['volatilities'] = volatilities
                vts['strike'] = vts_strikes[vts_moneynesses.index(selected_moneyness)]

            elif clsnm == ts.BlackVarianceSurface.__name__:
                selected_moneyness_list = vts.get('selected_moneyness_list')
                
                if selected_moneyness_list is None:
                    selected_moneyness_list = list(set(vts_moneynesses)) # get all moneyness

                # moneyness existance check
                for selected_moneyness in selected_moneyness_list:
                    if not selected_moneyness in vts_moneynesses:
                        raise Exception('selected moneyness does not exist - {0}, {1}'.format(selected_moneyness, vts[RAW_DATA_MONEYNESSES_NAME]))

                # convert to matrix - row: strike, col: expirydate
                rows = len(set(vts_strikes))
                cols = len(set(vts_expirydates))

                blackVols = mx.Matrix(rows, cols, 0.0)
                
                _strikes = sorted(list(set(vts_strikes)))
                _expirydates = sorted(list(set(vts_expirydates)))

                # reduce for moneyness
                for m, s, d, v in zip(vts_moneynesses, vts_strikes, vts_expirydates, vts_vols):
                    r = _strikes.index(s)
                    c = _expirydates.index(d)
                    blackVols[r][c] = v

                vts['dates'] = _expirydates
                vts['strikes'] = _strikes
                vts['blackVols'] = blackVols.toList()

            remove_others(clsnm, vts)

        return data
        

    def get_data(self, **kwargs) -> mx.MarketData:
        ref_date = kwargs.get('refDate')

        if ref_date is None or ref_date == mx.Date.todaysDate():
            res_d = self.with_meta(self._request_rt())
        else:
            res_d = self.with_meta(self._request_hist(ref_date))
        
        return mx.MarketData(res_d)


def request_sample():
    blp_config = dict()

    blp_config['requests'] = {
        'quote': {
            'kospi2': { 'ticker': 'KOSPI2 Index', 'field': QUOTE_DEFAULT_FLDNAME },
            'ibm': { 'ticker': 'IBM US Equity', 'field': QUOTE_DEFAULT_FLDNAME }
        },
        'yieldCurve': {
            'zerocurve1': { 'ticker': 'YCSW0057 Index', 'field': IRCURVE_DEFAULT_FLDNAME }
        },
        'volTs': { 
            'kospi2_vol1': { 'ticker': 'KOSPI2 Index', 'field': EQVOL_DEFAULT_FLDNAME },
            'kospi2_vol2': { 'ticker': 'KOSPI2 Index', 'field': EQVOL_DEFAULT_FLDNAME }
        }
    }

    blp_config['meta'] = {
        'quote': {
            'kospi2':   { 'clsnm': qt.SimpleQuote.__name__ },
            'ibm': { 'clsnm': qt.SimpleQuote.__name__ }
        },
        'yieldCurve': {
            'zerocurve1':  { 'clsnm': ts.ZeroYieldCurve.__name__, 'calendar': str(mx.SouthKorea()) },
        },
        'volTs': {
            'kospi2_vol1': { 'clsnm': ts.BlackVarianceCurve.__name__, 'calendar': str(mx.SouthKorea()), 'selected_moneyness': 1.0 },
            'kospi2_vol2': { 'clsnm': ts.BlackVarianceSurface.__name__, 'calendar': str(mx.SouthKorea()), 'selected_moneyness_list': [1.0] },
        }
    }

    blp_provider = BloombergMarketDataProvider(blp_config)
    mrk_blp = blp_provider.get_data(refDate=mx.Date.todaysDate())

    kospi2_vol1 = mrk_blp.get_volTs('kospi2_vol1') 
    kospi2_vol2 = mrk_blp.get_volTs_black('kospi2_vol2') # for intellisense
