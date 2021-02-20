import os, inspect

from numpy.lib.arraysetops import isin
import mxdevtool as mx
import mxdevtool.config as mx_config
import numpy as np
from datetime import datetime
import tempfile
import json
from hashlib import sha256
from collections import OrderedDict
from typing import List


def npzee_view(arg):
    if isinstance(arg, np.ndarray):
        tempfilename = os.path.join(tempfile.gettempdir(), 'temp_' + datetime.utcnow().strftime('%Y%m%d%H%M%S%f') + '.npz')
        np.savez(tempfilename, data=arg)
        os.startfile(tempfilename)
    elif isinstance(arg, str):
        if os.path.exists(arg):
            os.startfile(arg)
        else:
            raise Exception('file does not exist')
    elif isinstance(arg, mx.core_ScenarioResult):
        if os.path.exists(arg.filename):
            os.startfile(arg.filename)
        else:
            raise Exception('file does not exist')
    else:
        print('unknown')


def yield_curve_view(yieldcurve):
    pass


def get_hashCode(serializable) -> str:
    d = OrderedDict(serializable.toDict())
    try:
        json_str = json.dumps(d)
        return sha256(json_str.encode(mx_config.HASHCODE_ENCODING)).hexdigest()
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        raise e


def toJsonStr(serializable):
    d = serializable.toDict()
    json_str = json.dumps(d)
    return json_str


def toJson(filename, serializable):
    f = open(filename, "w")
    d = serializable.toDict()
    
    try:
        json_str = json.dumps(d)
        f.write(json_str)
        f.close()
        return sha256(json_str.encode(mx_config.HASHCODE_ENCODING)).hexdigest()
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        f.close()
        raise e


def check_hashCode(*serializables, exception=True):
    res = []
    for s in serializables:
        hashCode = s.hashCode()
        recreated_hashCode = s.fromDict(s.toDict()).hashCode()

        tf = hashCode == recreated_hashCode

        if tf == False and exception:
            raise Exception('hashCode is not valid - {0} != {1}'.format(hashCode, recreated_hashCode))
        
        res.append(tf)

    return res


def compare_hashCode(*serializables, exception=True):
    codes = set()
    for s in serializables:
        codes.add(s.hashCode())
    
    tf = len(codes) == 1

    if tf == False and exception:
        raise Exception('hashCode is not same')

    return tf


def check_args_in_dict(class_instance, clsnm: str, input_d: dict, strict_check=False):
    init = getattr(class_instance, "__init__", None)
    # required_args = inspect.getargspec(init).args[1:]
    required_args = inspect.signature(init).parameters

    for k, v in required_args.items():
        if k == 'self':
            continue

        if not k in input_d and v == inspect._empty:
            raise Exception('{0} missing required argument: {1}'.format(clsnm, k))
    
    if not strict_check:
        return

    for k in input_d:
        if k in ['name', 'clsnm']:
            continue

        if not k in required_args:
            raise Exception('{0} useless argument exist: {1}'.format(clsnm, k))


def volatility_range_check(value):
    lower = 1.0
    upper = 0.0

    if value < lower or upper < value:
        raise Exception('volatility must be in [{0}, {1}]'.format(lower, upper))


def interestrate_range_check(value):
    lower = 1.0
    upper = -1.0
    
    if value < lower or upper < value:
        raise Exception('interestrate must be in [{0}, {1}]'.format(lower, upper))


def check_correlation(corr):
    m = np.matrixlib.matrix(corr)

    if not np.allclose(m, m.T, rtol=1e-05, atol=1e-08):
        raise Exception('correlation matrix is not symmetric - {0}'.format(corr))


def save_file(filename, serializables, build_dict_method):
    """ save file ( Scenario, ScenarioBuilder, Shock, ...)

    Args:
        filename (str): full path
        serializables (serializable, list, dict): obj has toDict method

    Raises:
        Exception: [description]
    """    

    json_str = None
    # path = os.path.join(self.location, name + '.' + XENFILE_EXT)
    f = open(filename, "w")
    
    # prefix = 'item{0}'
    method_name = 'toDict'

    if isinstance(serializables, dict):
        if len(serializables) == 0:
            raise Exception('empty dict')

        d = dict()
        for k, s in serializables.items():
            toDict = getattr(s, method_name, None)

            if callable(toDict):
                d[k] = build_dict_method(s)
            else:
                raise Exception('serializable is required - {0}'.format(s))
        json_str = json.dumps(d)
    else:
        f.close()
        raise Exception('serializable is required - {0}'.format(serializables))
    
    if json_str is None:
        f.close()
        raise Exception('nothing to write')
    
    f.write(json_str)
    f.close()
    

def toTypeCls(arg, typ):
    # target class list
    from mxdevtool import Period, Date

    if isinstance(arg, typ):
        return arg
    else:
        return typ(arg)


def toTypeClsList(arg, typ):
    # target class list
    from mxdevtool import Period, Date

    if isinstance(arg, list):
        res = []
        for v in arg:
            if isinstance(v, typ):
                res.append(v)
            else:
                res.append(typ(v))
        return res
    else:
        raise Exception('list is required - {0}'.format(arg))

def toStrList(arg) -> List[str]: return [str(v) for v in arg]

def toPeriodCls(arg) -> mx.Period : return toTypeCls(arg, mx.Period)
def toPeriodClsList(arg) -> List[mx.Period]: return toTypeClsList(arg, mx.Period)

def toDateCls(arg) -> mx.Date: return toTypeCls(arg, mx.Date)
def toDateClsList(arg) -> List[mx.Date]: return toTypeClsList(arg, mx.Date)

def periodToDateList(refDate, periods, calendar=None, businessDayConvention=mx.ModifiedFollowing) -> List[mx.Date]: 
    _periods = toPeriodClsList(periods)
    return [calendar.advance(refDate, p, businessDayConvention) for p in _periods]

def toMatrixCls(arg) -> mx.Matrix:
    if isinstance(arg, mx.Matrix):
        return arg
    elif isinstance(arg, list):
        return mx.Matrix(arg)
    elif isinstance(arg, np.ndarray):
        return mx.Matrix(arg.tolist())
    else:
        raise Exception('unable to convert matrix - {0}'.format(arg))


def toMatrixList(arg) -> list:
    if isinstance(arg, mx.Matrix):
        return arg.toList()
    elif isinstance(arg, list):
        return arg
    elif isinstance(arg, np.ndarray):
        return arg.tolist()
    else:
        raise Exception('unable to convert list(2d) - {0}'.format(arg))


def toOptionType(arg):
    if arg in [mx.Option.Call, mx.Option.Put]:
        return arg
    elif isinstance(arg, str):
        if arg.lower() in ['c', 'call']:
            return mx.Option.Call
        elif arg.lower() in ['p', 'put']:
            return mx.Option.Put
        else:
            raise Exception('unknown arg for option_type - {0}'.format(arg))
    else:
        raise Exception('unknown arg for option_type - {0}'.format(arg))


def toBarrierType(arg):
    if arg in [mx.Barrier.UpIn, mx.Barrier.UpOut, mx.Barrier.DownIn, mx.Barrier.DownOut]:
        return arg
    elif isinstance(arg, str):
        if arg.lower() in ['upin']:
            return mx.Barrier.UpIn
        elif arg.lower() in ['upout']:
            return mx.Barrier.UpOut
        elif arg.lower() in ['downin']:
            return mx.Barrier.DownIn
        elif arg.lower() in ['downout']:
            return mx.Barrier.DownOut                       
        else:
            raise Exception('unknown arg for barrier_type - {0}'.format(arg))
    else:
        raise Exception('unknown arg for barrier_type - {0}'.format(arg))
