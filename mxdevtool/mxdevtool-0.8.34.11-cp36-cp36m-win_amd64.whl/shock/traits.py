from mxdevtool import mxdevtool
import mxdevtool as mx
import numpy as np
import inspect, numbers, copy
import mxdevtool.xenarix as xen
import mxdevtool.utils as utils


def check_args_in_dict(clsnm: str, input_d: dict, strict_check=False):
    class_instance = globals()[clsnm]
    init = getattr(class_instance, "__init__", None)
    required_args = inspect.getargspec(init).args[1:]

    for k in required_args:
        if not k in input_d:
            raise Exception('{0} missing required argument: {1}'.format(clsnm, k))
    
    if not strict_check:
        return

    for k in input_d:
        if not k in required_args:
            raise Exception('{0} useless argument exist: {1}'.format(clsnm, k))


# arguments parse from arg name
def get_args_fromDict(d: dict, parameters):
    args = []
    for name, v in parameters.items():
        if name == 'self':
            continue
        
        if not name in d and v.default != inspect._empty:
            args.append(v.default)
        else:
            args.append(d[name])

        # args.append(get_arg_fromValue(name, d[name]))

    return args


def parseClassFromDict(d: dict):
    if not isinstance(d, dict):
        raise Exception('dictionary type is required')
    
    classTypeName = d[mx.CLASS_TYPE_NAME]

    if not classTypeName in globals():
        raise Exception('unknown classTypeName - {0}'.format(classTypeName))

    try:
        class_instance = globals()[classTypeName]
        init = getattr(class_instance, "__init__", None)
        #args = get_args_fromDict(d, inspect.getargspec(init).args[1:])
        args = get_args_fromDict(d, inspect.signature(init).parameters)

        return class_instance(*args)
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        raise e



class ShockTrait:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def fromDict(d: dict):
        return parseClassFromDict(d)
        #raise Exception('not implemented - {0}'.format(d))

    def toDict(self):
        res = dict()
        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['name'] = self.name

        for key, v in self.__dict__.items():
            #key = k[1:]
            toDict = getattr(v, "toDict", None)

            if callable(toDict):
                res[key] = toDict()
            else:
                res[key] = v

        return res

    def hashCode(self):
        return utils.get_hashCode(self)

    def calculate(self, target_v):
        raise Exception('not implemented - {0}'.format(d))


class CustomShockTrait(ShockTrait):
    def __init__(self, name, func):
        self.name = name
        self.func = func

    @staticmethod
    def fromDict(d: dict):
        raise Exception('this class is not serializable now')

    def toDict(self):
        raise Exception('this class is not serializable now')

    def calculate(self, target_v):
        return self.func(target_v)



## Quote
class QuoteShockTrait(ShockTrait):
    def __init__(self, name, value, operand='add'):
        ShockTrait.__init__(self, name)

        if not operand in self.available_operands():
            raise Exception('unknown operand - {0}'.format(self.operand))

        self.name = name
        self.value = value
        self.operand = operand

    def available_operands(self):
        return ['add', 'mul', 'assign']

    def calculate(self, quote_d):
        if not isinstance(quote_d, dict):
            raise Exception('dictionary is required - {0}'.format(quote_d))

        if self.operand == 'add':
            quote_d['v'] += self.value
        elif self.operand == 'mul':
            quote_d['v'] *= self.value
        elif self.operand == 'assign':
            quote_d['v'] = self.value
        else:
            raise Exception('unknown operand - {0}, available - {1}'.format(self.operand, self.available_operands))


## Curve
class CurveShockTrait(ShockTrait):
    def __init__(self, name):
        ShockTrait.__init__(self, name)


class YieldCurveShockTrait(CurveShockTrait):
    def __init__(self, name):
        ShockTrait.__init__(self, name)


class YieldCurveParallelBpShockTrait(YieldCurveShockTrait):
    def __init__(self, name, bp=1):
        ShockTrait.__init__(self, name)

        if abs(bp) > 10000:
            raise Exception('too larger yieldcurve shock bp - {0}'.format(bp))
        
        self.bp = bp

    def calculate(self, yieldcurve_d: dict):
        if not isinstance(yieldcurve_d, dict):
            raise Exception('dictionary is required - {0}'.format(yieldcurve_d))

        res = copy.deepcopy(yieldcurve_d)
        clsnm = yieldcurve_d[mx.CLASS_TYPE_NAME]
        value = self.bp / 10000.0

        if clsnm == xen.FlatForward.__name__:
            yieldcurve_d['forward'] += value
        elif clsnm == xen.ZeroYieldCurve.__name__:
            yieldcurve_d['zeroRates'] = [r + value for r in yieldcurve_d['zeroRates']]
        elif clsnm == xen.BootstapSwapCurveCCP.__name__:
            yieldcurve_d['quotes'] = [r + value for r in yieldcurve_d['quotes']]
        else:
            raise Exception('unknown class type name - {0}'.format(clsnm))

        return res


## VolTs
class VolTsShockTrait(ShockTrait):
    def __init__(self, name):
        ShockTrait.__init__(self, name)


class VolTsParallelShockTrait(VolTsShockTrait):
    def __init__(self, name, value):
        VolTsShockTrait.__init__(self, name)
        
        if abs(value) > 1:
            raise Exception('too larger volTs shock - {0}'.format(bp))

        self.value = value

    def calculate(self, target_v):
        if isinstance(target_v, dict):
            raise Exception('dictionary is required - {0}'.format(target_v))

        res = copy.deepcopy(target_v)
        clsnm = target_v[mx.CLASS_TYPE_NAME]

        if clsnm == xen.BlackConstantVol.__name__:
            res['vol'] = target_v['vol'] + self.value
        elif clsnm == xen.BlackVarianceCurve.__name__:
            res['volatilities'] = [r + self.value for r in target_v['volatilities']]
        elif clsnm == xen.BlackVarianceSurface.__name__:
            blackVols_arr2d = np.array(target_v['blackVols']) + self.value
            target_v['blackVols'] = blackVols_arr2d.tolist()
        else:
            raise Exception('unknown class type name - {0}'.format(clsnm))

        return res


## Composite
class CompositeShockTrait(ShockTrait):
    def __init__(self, name, shocktrait_list):
        ShockTrait.__init__(self, name)
        
        # if not hasattr(self, 'inherit'):
        if self.__class__.__name__ ==  'CompositeShockTrait':
            raise Exception('inherit class must be used, this constructor is protected')

        self.shocktrait_list = []

        self.initialize(name, shocktrait_list)

    def initialize(self, name, st_list):
        if len(name) == 0:
            raise Exception('empty name')

        if len(st_list) == 0:
            raise Exception('empty shocktrait_list')
        
        for st in st_list:
            if isinstance(st, dict):
                self.shocktrait_list.append(parseClassFromDict(st))
            elif isinstance(st, ShockTrait):
                self.shocktrait_list.append(st)
            else:
                raise Exception('shocktrait type is required')
    
    def shocktrait_list_check_type(self, typ):
        # same type check
        if not all(isinstance(st, typ) for st in self.shocktrait_list):
            raise Exception('all shockstrait_list must be {0} class - {1}'.format(typ.__name__, self.shocktrait_list))

    @staticmethod
    def fromDict(d: dict):
        clsnm = d[mx.CLASS_TYPE_NAME]

        shocktrait_list = [ parseClassFromDict(st_d) for st_d in d['shocktrait_list']]

        class_instance = globals()[clsnm]
        init = getattr(class_instance, "__init__", None)
        return class_instance(d['name'], shocktrait_list)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['name'] = self.name
        res['shocktrait_list'] = [ st.toDict() for st in self.shocktrait_list ]

        return res

    def calculate(self, target_d):
        for st in self.shocktrait_list:
            st.calcaulte(target_d)


class CompositeQuoteShockTrait(CompositeShockTrait):
    def __init__(self, name, shocktrait_list):
        CompositeShockTrait.__init__(self, name, shocktrait_list)

        self.shocktrait_list_check_type(QuoteShockTrait)


class CompositeYieldCurveShockTrait(CompositeShockTrait):
    def __init__(self, name, shocktrait_list):
        CompositeShockTrait.__init__(self, name, shocktrait_list)

        self.shocktrait_list_check_type(YieldCurveShockTrait)


class CompositeVolTsShockTrait(CompositeShockTrait):
    def __init__(self, name, shocktrait_list):
        CompositeShockTrait.__init__(self, name, shocktrait_list)
    
        self.shocktrait_list_check_type(VolTsShockTrait)


# class YieldCurveParallelBpIntervalShockTrait(CurveShockTrait):
#     def __init__(self, name, tenors, values):
#         ShockTrait.__init__(self, name)

#         self.tenors = tenors
#         self.values = values


# class YieldCurveZeroSpreadBpShockTrait(CurveShockTrait):
#     def __init__(self, name, value):
#         ShockTrait.__init__(self, name)
#         self.value = value






