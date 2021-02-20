import os, json, numbers
import mxdevtool as mx
import mxdevtool.utils as utils
import numpy as np
#import mxdevtool.termstructures as ts
from mxdevtool.termstructures import *
from mxdevtool.xenarix.pathcalc import *
from mxdevtool.data.repositories.settings import get_repo
from mxdevtool import TimeGrid, TimeEqualGrid, TimeArrayGrid
from typing import List


XENFILE_EXT = 'xen'
XENBUILDERFILE_EXT = 'xnb'
HASHCODES_KEY = 'hashcodes'
XENREPO_RESULTS_DIR = 'results'


class NameHelper:

    @staticmethod
    def isCompounding(name: str):
        return 'compounding' == name or 'Compounding' == name[-len('Compounding'):]

    @staticmethod
    def isCalendar(name: str):
        return 'calendar' == name or 'Calendar' == name[-len('Calendar'):]

    @staticmethod
    def isDayCounter(name: str):
        return 'dayCounter' == name or 'DayCounter' == name[-len('DayCounter'):]

    @staticmethod
    def isBusinessDayConvention(name: str):
        return 'businessDayConvention' == name or 'BusinessDayConvention' == name[-len('BusinessDayConvention'):]

    @staticmethod
    def isInterpolationType(name: str):
        return 'interpolationType' == name or 'InterpolationType' == name[-len('InterpolationType'):]

    @staticmethod
    def isExtrapolationType(name: str):
        return 'extrapolationType' == name or 'ExtrapolationType' == name[-len('ExtrapolationType'):]

    @staticmethod
    def isTenor(name: str):
        return 'tenor' == name or 'Tenor' == name[-len('Tenor'):]

    @staticmethod
    def isDate(name: str):
        return 'date' == name or 'Date' == name[-len('Date'):]

    @staticmethod
    def isDates(name: str):
        return 'dates' == name or 'Dates' == name[-len('Dates'):]

    @staticmethod
    def getTypeFrom(name: str):
        res = None

        if NameHelper.isCompounding(name):
            res = 'compounding'
        elif NameHelper.isCalendar(name):
            res = 'calendar'
        elif NameHelper.isDayCounter(name):
            res = 'dayCounter'
        elif NameHelper.isBusinessDayConvention(name):
            res = 'businessDayConvention'
        elif NameHelper.isInterpolationType(name):
            res = 'interpolationType'
        elif NameHelper.isExtrapolationType(name):
            res = 'extrapolationType'
        elif NameHelper.isTenor(name):
            res = 'tenor'
        elif NameHelper.isDate(name):
            res = 'date'
        elif NameHelper.isDates(name):
            res = 'dates'

        return res

    @staticmethod
    def toDictArg(name: str, value):
        res = None

        if NameHelper.isCompounding(name):
            res = mx.compoundingToString(value)
        elif NameHelper.isCalendar(name):
            res = str(value)
        elif NameHelper.isDayCounter(name):
            res = str(value)
        elif NameHelper.isBusinessDayConvention(name):
            res = mx.businessDayConventionToString(value)
        elif NameHelper.isInterpolationType(name):
            res = mx.interpolator1DToString(value)
        elif NameHelper.isExtrapolationType(name):
            res = mx.extrapolator1DToString(value)
        elif NameHelper.isTenor(name):
            res = str(value)
        elif NameHelper.isDate(name):
            res = str(value)
        elif NameHelper.isDates(name):
            res = [str(v) for v in value]
        elif isinstance(value, (numbers.Number, str, list)):
            res = value

        return res

    @staticmethod
    def toClassArg(name: str, value):
        arg = None

        if NameHelper.isDate(name):
            arg = mx.Date(value)
        elif NameHelper.isDates(name):
            arg = [ mx.Date(v) for v in value]
        elif NameHelper.isCompounding(name):
            arg = mx.compoundingParse(value) if isinstance(value, str) else value
        elif NameHelper.isCalendar(name):
            arg = mx.calendarParse(value)
        elif NameHelper.isDayCounter(name):
            arg = mx.dayCounterParse(value)
        elif NameHelper.isBusinessDayConvention(name):
            arg = mx.businessDayConventionParse(value) if isinstance(value, str) else value
        elif NameHelper.isInterpolationType(name):
            arg = mx.interpolator1DParse(value) if isinstance(value, str) else value
        elif NameHelper.isExtrapolationType(name):
            arg = mx.extrapolator1DParse(value) if isinstance(value, str) else value
        elif NameHelper.isTenor(name):
            arg = mx.Period(value)
        elif isinstance(value, (numbers.Number, str, list)):
            arg = value
        else:
            raise Exception('unsupported argument name : {0}'.format(value))

        return arg

        

# arguments parse from arg name
def get_arg_fromValue(name: str, arg_v, mrk: mx.MarketData, models_calcs):
    arg = None

    # class type case
    if not isinstance(arg_v, (numbers.Number, str, dict, list)):
        return arg_v

    if 'Curve' == name[-len('Curve'):]:
        curve_d = mrk.get_yieldCurve_d(arg_v)
        curveType = curve_d[mx.CLASS_TYPE_NAME]

        class_instance = globals()[curveType]
        arg = class_instance.fromDict(curve_d, mrk)

    elif 'volTs' == name or 'VolTs' == name[-len('VolTs'):]:
        volTs_d = mrk.get_volTs_d(arg_v)
        volType = volTs_d[mx.CLASS_TYPE_NAME]

        class_instance = globals()[volType]
        arg = class_instance.fromDict(volTs_d, mrk)

    elif 'Para' == name[-len('Para'):]:
        arg = DeterministicParameter.fromDict(arg_v)

    elif NameHelper.getTypeFrom(name) != None:
        arg = NameHelper.toClassArg(name, arg_v)

    elif name in ['ir_pc', 'pc', 'pc1', 'pc2'] and isinstance(arg_v, str):
        if not arg_v in models_calcs:
            raise Exception('model or calc does not exist - {0}, {1}'.format(arg_v, models_calcs.keys()))
        arg = models_calcs[arg_v]

    elif name == 'pc_list':
        for pc in arg_v:
            if not arg_v in models_calcs:
                raise Exception('model or calc does not exist - {0}'.format(arg_v, models_calcs.keys()))
        arg = [models_calcs[pc] for pc in arg_v]

    elif name == 'name' or 'type' == name[-len('type'):].lower():
        arg = arg_v

    elif isinstance(arg_v, numbers.Number):
        arg = arg_v

    else:
        arg = mrk.get_quote_v(arg_v)
        # quote_d = mrk.get_quote_d(arg_v)
        # arg = quote_d['v']

    if arg is None:
        raise Exception('unsupported argument name : {0}'.format(arg_v))

    return arg


def get_args_fromDict(d: dict, mrk: mx.MarketData, models_calcs, parameters):
    args = []
    for name, v in parameters.items():
        if name == 'self':
            continue
        
        if not name in d and v.default != inspect._empty:
            args.append(v.default)
        else:
            args.append(get_arg_fromValue(name, d[name], mrk, models_calcs))

    return args


# model parse
def parseClassFromDict(d: dict, models_calcs=[], mrk=mx.MarketData()):
    if not isinstance(d, dict):
        raise Exception('dictionary type is required')
    
    classTypeName = d[mx.CLASS_TYPE_NAME]

    if not classTypeName in globals():
        raise Exception('unknown classTypeName - {0}'.format(classTypeName))

    try:
        class_instance = globals()[classTypeName]
        init = getattr(class_instance, "__init__", None)
        
        #args = get_args_fromDict(d, mrk, models_calcs, inspect.getfullargspec(init).args[1:])
        args = get_args_fromDict(d, mrk, models_calcs, inspect.signature(init).parameters)

        return class_instance(*args)
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        raise


class Rsg(mx.core_Rsg):
    def __init__(self, sampleNum, dimension=365, seed=1, skip=0, isMomentMatching=False, randomType='pseudo', subType='mersennetwister', randomTransformType='boxmullernormal'):

        self._randomType = randomType
        self._subType = subType
        self._randomTransformType = randomTransformType

        mx.core_Rsg.__init__(self, sampleNum, dimension, seed, skip, isMomentMatching, randomType, subType, randomTransformType)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, Rsg.__name__)

        return parseClassFromDict(d)

        # sampleNum = d['sampleNum']
        # dimension = d['dimension']
        # seed = d['seed']
        # skip = d['skip']
        # isMomentMatching = d['isMomentMatching']
        # randomType = d['randomType']
        # subType = d['subType']
        # randomTransformType = d['randomTransformType']

        # return Rsg(sampleNum, dimension, seed, skip, isMomentMatching, randomType, subType, randomTransformType)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__

        res['sampleNum'] = self.sampleNum
        res['dimension'] = self.dimension
        res['seed'] = self.seed
        res['skip'] = self.skip
        res['isMomentMatching'] = self.isMomentMatching
        res['randomType'] = self.randomType
        res['subType'] = self.subType
        res['randomTransformType'] = self.randomTransformType

        return res

    randomType = property(lambda self: self._randomType,None,None)
    subType = property(lambda self: self._subType,None,None)
    randomTransformType = property(lambda self: self._randomTransformType,None,None)


class ScenarioBuilder:
    def __init__(self, json_dict: dict = None):
        if json_dict is None:
            self.reset()
        else:
            if 'hashcodes' in json_dict:
                del json_dict['hashcodes']

            self.check_json_dict(json_dict)
            self.__dict__ = json_dict

    @staticmethod
    def fromDict(d: dict):
        return ScenarioBuilder(d)

    def toDict(self):
        import copy
        return copy.deepcopy(self.__dict__)

    def hashCode(self):
        return utils.get_hashCode(self)

    def check_json_dict(self, d: dict):
        keys = ['models', 'calcs', 'timegrid', 'corr', 'rsg', 'filename', 'isMomentMatching']

        for k in keys:
            if not k in d:
                raise Exception("invalid json for scenario building. '{0}' is required\n{1}".format(k, d))

    def build_scenario(self, mrk: mx.MarketData()):
        if mrk is None:
            mrk = mx.MarketData()

        # models
        models_calcs = dict()

        models = []
        for m in self.models:
            model = parseClassFromDict(m, models_calcs, mrk)
            models_calcs[model.name] = model
            models.append(model)
        
        calcs = []
        for c in self.calcs:
            calc = parseClassFromDict(c, models_calcs, mrk)
            models_calcs[calc.name] = calc
            calcs.append(calc)
        
        # corr = mx.Matrix(self.corr)
        corr = mx.IdentityMatrix(len(self.models))

        for r, row in enumerate(self.corr):
            for c, v in enumerate(row):
                corr[r][c] = mrk.get_quote_v(v)

        utils.check_correlation(corr.toList())

        if len(models) != corr.rows() or len(models) != corr.columns():
            raise Exception("correlation matrix's rows({0}) and columns({1}) size must be same to model size({2})".format(corr.rows(), corr.columns(), len(models)))

        timegrid = parseClassFromDict(self._toDict(self.timegrid))
        rsg = Rsg.fromDict(self._toDict(self.rsg), mrk)

        return Scenario(models, calcs, corr, timegrid, rsg, self.filename, self.isMomentMatching)

    def reset(self):
        d = dict()

        d['models'] = []
        d['calcs'] = []
        d['corr'] = mx.IdentityMatrix(1).toList()
        d['timegrid'] = mx.TimeEqualGrid().toDict()
        d['rsg'] = Rsg(sampleNum=1000).toDict()
        d['filename'] = 'temp.npz'
        d['isMomentMatching'] = False

        self.__dict__ = d

    def _makeDictFromArgs(self, clsnm: str, name: str, **kwargs):
        d = dict()

        class_instance = globals()[clsnm]
        utils.check_args_in_dict(class_instance, clsnm, d, True)

        if name is not None:
            d['name'] = name

        d[mx.CLASS_TYPE_NAME] = clsnm
        d = { **d, **self._toDictArgs(kwargs)}

        # default arguments which does not exist in kwargs ( for serialize)

        init = getattr(class_instance, "__init__", None)
        
        for k, v in inspect.signature(init).parameters.items():
            if not k in d and v.default != inspect._empty:
                d[k] = v.default

        return d

    def _toDict(self, v):
        toDict = getattr(v, "toDict", None)

        if isinstance(v, dict):
            return v
        elif toDict is not None:
            return v.toDict()
        else:
            raise Exception('dict or serializable is required - {0}'.format(v))

    def _toDictArgs(self, d: dict):
        res = dict()

        for k, v in d.items():
            toDict = getattr(v, "toDict", None)

            if toDict is None:
                res[k] = NameHelper.toDictArg(k, v)
            else:
                res[k] = v.toDict()

        return res

    def getModel(self, name):
        for m in self.models:
            if m.name == name:
                return m

    def addModel(self, clsnm: str, name: str, **kwargs):
        self.models.append(self._makeDictFromArgs(clsnm, name, **kwargs))    
        self.resetCorrelation()

    def removeModel(self, name: str):
        self.models.remove(self.getModel(name))
        self.resetCorrelation()
    
    def getCalc(self, name):
        for c in self.calcs:
            if c['name'] == name:
                return c

    def addCalc(self, clsnm: str, name: str, **kwargs):
        self.calcs.append(self._makeDictFromArgs(clsnm, name, **kwargs))

    def removeCalc(self, name: str):
        self.calcs.remove(self.getCalc(name))

    def setTimeGrid(self, clsnm: str, **kwargs):
        self.timegrid = self._makeDictFromArgs(clsnm, None, **kwargs)

    def setTimeGridCls(self, tg):
        if isinstance(tg, (mx.TimeGrid, mx.TimeArrayGrid, mx.TimeEqualGrid)):
            self.timegrid = tg.toDict()
        else:
            raise Exception('TimeGrid type is required - {0}'.format(tg))

    def setRsg(self, clsnm: str, **kwargs):
        self.rsg = self._makeDictFromArgs(clsnm, None, **kwargs)

    def setRsgCls(self, rsg):
        if isinstance(rsg, Rsg):
            self.rsg = rsg.toDict()
        else:
            raise Exception('Rsg type is required - {0}'.format(rsg))        
    
    def setCorrelationMatrix(self, m):
        if isinstance(m, mx.Matrix):
            self.corr = m.toList()
        elif isinstance(m, np.matrixlib.matrix):
            self.corr = m.tolist()
        else:
            raise Exception('Matrix type is required - {0}'.format(m))        

    def resetCorrelation(self):
        dim = len(self.models)
        self.corr = np.identity(dim).tolist()
        # (mx.IdentityMatrix(len(self.models)).toList()).tolist()
    

# class Scenario(mx.core_ScenarioGenerator2):
class Scenario:
    def __init__(self, models, calcs, corr, timegrid, rsg, filename, isMomentMatching = False):
        _corr = mx.Matrix(corr)

        # _dimension = (len(timegrid) - 1) * len(models)
        # _rsg = Rsg(rsg.sampleNum, _dimension, rsg.seed, rsg.skip, rsg.isMomentMatching, rsg.randomType, rsg.subType, rsg.randomTransformType)

        self.models = models
        self.calcs = calcs
        self.corr = _corr
        self.timegrid = timegrid
        self.rsg = rsg
        self.filename = filename
        self.isMomentMatching = isMomentMatching

        # set jsonStr for generation


    @staticmethod
    def fromDict(d: dict, mrk: mx.MarketData = None):
        if not isinstance(d, dict):
            raise Exception('dictionary type is required')

        sjb = ScenarioBuilder(d)

        if mrk == None:
            mrk = mx.MarketData()
        
        return sjb.build_scenario(mrk)
        # args = sjb.build_scenario(mrk)
        # return Scenario(*args)

    def toDict(self):
        res = dict()
        
        res['models'] = [ m.toDict() for m in self.models]
        res['calcs'] = [ c.toDict() for c in self.calcs]
        res['corr'] = self.corr.toList()
        res['timegrid'] = self.timegrid.toDict()
        res['rsg'] = self.rsg.toDict()
        res['filename'] = self.filename
        res['isMomentMatching'] = self.isMomentMatching

        return res

    def hashCode(self):
        return utils.get_hashCode(self)
    
    def clone(self, **kwargs):
        try:
            _dimension = (len(self.timegrid) - 1) * len(self.models)
            _rsg = Rsg(self.rsg.sampleNum, _dimension, self.rsg.seed, self.rsg.skip, self.rsg.isMomentMatching, 
                       self.rsg.randomType, self.rsg.subType, self.rsg.randomTransformType)

            models = kwargs['models'] if 'models' in kwargs else self.models
            calcs = kwargs['calcs'] if 'calcs' in kwargs else self.calcs
            corr = kwargs['corr'] if 'corr' in kwargs else self.corr
            timegrid = kwargs['timegrid'] if 'timegrid' in kwargs else self.timegrid
            rsg = kwargs['rsg'] if 'rsg' in kwargs else _rsg
            filename = kwargs['filename'] if 'filename' in kwargs else self.filename
            isMomentMatching = kwargs['isMomentMatching'] if 'isMomentMatching' in kwargs else self.isMomentMatching

            if not filename[-4:] == '.npz':
                filename += '.npz'

            scen = Scenario(models, calcs, corr, timegrid, rsg, filename, isMomentMatching)

            return scen

        except Exception as e:
            if len(e.args) >= 1:
                e.args = (e.args[0] + '\nscenario inputs: {0}'.format((self.models, self.calcs, self.corr, self.timegrid, 
                        self.rsg, self.filename, self.isMomentMatching)),) + e.args[1:]
            raise

    def generate(self, **kwargs):
        scen = self.clone(**kwargs)
        hashCode = utils.get_hashCode(scen) # for logging

        core = mx.core_ScenarioGenerator2(scen.models, scen.calcs, scen.corr, scen.timegrid, scen.rsg, scen.filename, scen.isMomentMatching, hashCode)
        core.generate()
        
        # logging and history
        # from mxdevtool.data.repositories import repo
        # repo.logging_scen(scen)

        return ScenarioResults(scen.filename)
    

class ScenarioResults(mx.core_ScenarioResult):
    def __init__(self, filename):
        mx.core_ScenarioResult.__init__(self, filename)
        self.shape = (self.simulNum, self.assetNum, self.timegridNum)
        self.names_idx_d = dict()
        
        for info in self.genInfo:
            self.names_idx_d[info[1]] = int(info[0])

    def toNumpyArr(self) -> np.ndarray:
        npz = np.load(self.filename)
        arr = npz['data']
        arr.reshape(self.shape)

        return arr

    def nameList(self):
        return [k for k in self.names_idx_d.keys()]

    def getScenCount(self, name):
        if not name in self.names_idx_d:
            raise Exception("scenario path does not exist - {0} in {1}".format(name, self.names_idx_d))
        return self.names_idx_d[name]

    def __getitem__(self, key):
        if not isinstance(key, (int, str)):
            raise Exception('ScenCount or PathName is required - {0}'.format(key))

        if isinstance(key, str):
            return self._multiPath(self.getScenCount(key))
        else:
            return self._multiPath(key)

    def tPosSlice(self, t_pos, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPos(t_pos)
        else:
            return self._multiPathTPos(scenCount, t_pos)

    def timeSlice(self, time, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPosInterpolateTime(time)
        else:
            return self._multiPathTPosInterpolateTime(scenCount, time)

    def dateSlice(self, date, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPosInterpolateDate(date)
        else:
            return self._multiPathTPosInterpolateDate(scenCount, date)

    # def getScenario(self):
    #     json_str = get_repo().get_log_scen(self.hashCode) # now files
    #     d = json.loads(json_str)
    #     sb = ScenarioBuilder(d)

        return sb.build_scenario(mrk=None)

    def show(self):
        import mxdevtool.utils as mx_u
        mx_u.npzee_view(self)

    nameList = property(nameList,None,None)


class XenarixFileManager(mx.ManagerBase):
    def __init__(self, config: dict):
        mx.ManagerBase.__init__(self, config)

        self.location = config['location']
        self.results_dir = os.path.join(self.location, XENREPO_RESULTS_DIR)

        if not os.path.exists(self.location):
            os.makedirs(self.location)

        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)


    def _build_dict(self, scen: Scenario):
        scen_d = scen.toDict()
        hashcodes_d = dict()
        
        hashcodes_d['base'] = scen.hashCode()

        scen_d[HASHCODES_KEY] = hashcodes_d

        return scen_d

    def _save(self, name: str, ext: str, **kwargs):
        json_str = None
        path = os.path.join(self.location, name + '.' + ext)
        
        utils.save_file(path, kwargs, self._build_dict)

    def _load(self, name: str, ext: str):
        path = os.path.join(self.location, name + '.' + ext)
        f = open(path, "r")
        json_str = f.read()
        scen_d = json.loads(json_str)

        res = dict()
        
        for k, v in scen_d.items():
            if ext == XENFILE_EXT:
                sb = ScenarioBuilder(v)
                res[k] = sb.build_scenario(mrk=None)
            elif ext == XENBUILDERFILE_EXT:
                res[k] = ScenarioBuilder(v)
            else:
                raise Exception('unknown type file - {0}' - ext)

        return res

    def save_xen(self, name: str, **kwargs):
        for k, v in kwargs.items():
            if not isinstance(v, Scenario):
                raise Exception('Scenario type is required - {0}, {1}'.format(k, v))

        self._save(name, XENFILE_EXT, **kwargs)

    def load_xen(self, name: str):
        return self._load(name, XENFILE_EXT)

    def save_xnb(self, name: str, **kwargs):
        for k, v in kwargs.items():
            if not isinstance(v, ScenarioBuilder):
                raise Exception('ScenarioBuilder type is required - {0}, {1}'.format(k, v))

        self._save(name, XENBUILDERFILE_EXT, **kwargs)

    def load_xnb(self, name: str):
        return self._load(name, XENBUILDERFILE_EXT)

    def _get_file_list(self, *args):
        file_names = [os.path.splitext(fn)[0] for fn in os.listdir(self.location)
            if any(fn.endswith(ext) for ext in args)]
        
        return file_names

    def scenList(self):
        return self._get_file_list(XENFILE_EXT)

    def scenBuilderList(self):
        return self._get_file_list(XENBUILDERFILE_EXT)

    def generate_xen(self, name: str):
        res_dir = os.path.join(self.results_dir, name)

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        scen_d = self.load_xen(name)
        results = []

        for k, scen in scen_d.items():
            filename = os.path.join(self.results_dir, name, k + '.npz')
            results.append(scen.generate(filename=filename))
            
        return results


    def generate_xnb(self, name: str, mrk: mx.MarketData):
        res_dir = os.path.join(self.results_dir, name)

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        sb_d = self.load_xnb(name)
        results = []
        
        for k, sb in sb_d.items():
            filename = os.path.join(self.results_dir, name, k + '.npz')
            scen = sb.build_scenario(mrk)
            results.append(scen.generate(filename=filename))

        return results

    def _load_results(self, name: str, ext: str):
        scen_d = self._load(name, ext)

        results = []
        for k in scen_d.keys():
            filename = os.path.join(self.results_dir, name, k + '.npz')
            results.append(ScenarioResults(filename=filename))
            
        return results   

    def load_results_xen(self, name: str):
        return self._load_results(name, XENFILE_EXT)
    
    def load_results_xnb(self, name: str):
        return self._load_results(name, XENBUILDERFILE_EXT)


def generate1d(model, calcs, timegrid, rsg, filename: str, isMomentMatching = False):
    _calcs = calcs

    if calcs is None:
        _calcs = []

    corr = mx.IdentityMatrix(1)

    scen = Scenario([model], _calcs, corr, timegrid, rsg, filename, isMomentMatching)
    scen.generate()

    # get_repo().logging_scen(scen)

    return ScenarioResults(filename)


def generate(models, calcs, corr, timegrid, rsg, filename: str, isMomentMatching = False):
    if calcs is None:
        calcs = []

    scen = Scenario(models, calcs, corr, timegrid, rsg, filename, isMomentMatching)
    scen.generate()

    # get_repo().logging_scen(scen)

    return ScenarioResults(filename)

