import os
import mxdevtool as mx
import mxdevtool.xenarix as xen
import mxdevtool.utils as utils
import json, inspect
import numpy as np

from fnmatch import fnmatch

from mxdevtool.shock.traits import *
from typing import List

SHOCKFILE_EXT = 'shk'
SHOCKTRAITFILE_EXT = 'sht'
SHOCKMODELFILE_EXT = 'shm'

class Shock:
    def __init__(self, name: str):
        self.name = name
        self.shocktrait_d_list = []

    def __getitem__(self, shocktrait_name: str):
        for st_d in self.shocktrait_d_list:
            if st_d['name'] == shocktrait_name:
                return st_d['shocktrait']

        raise KeyError(shocktrait_name)

    @staticmethod
    def fromDict(d: dict):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, Shock.__name__)
        
        shock = Shock(d['name'])
        shocktrait_d_list = d['shocktrait_d_list']

        for st_d in shocktrait_d_list:
            shock.addShockTrait(target=st_d['target'], shocktrait=parseClassFromDict(st_d['shocktrait']))

        return shock

    def toDict(self):
        d = dict()

        d[mx.CLASS_TYPE_NAME] = Shock.__name__
        d['name'] = self.name
        d['shocktrait_d_list'] = self.shocktrait_d_list

        return d

    def hashCode(self):
        return utils.get_hashCode(self)

    def shockTraitList(self):
        return self.shocktrait_d_list

    def clone(self, name=None):
        d = copy.deepcopy(self.toDict())

        if name is None:
            d['name'] += '_clone'
        else:
            d['name'] = name

        return Shock.fromDict(d)

    def addShockTrait(self, target: str, shocktrait: ShockTrait):
        d = dict()
        
        d['target'] = target
        d['shocktrait'] = shocktrait.toDict()

        # for st_d in self.shocktrait_d_list:
        #     if st_d['shocktrait']['name'] == shocktrait.name:
        #         raise Exception('shocktrait name exist - {0}'.format(shocktrait.name))

        self.shocktrait_d_list.append(d)

    def removeShockTrait(self, target=None, shocktrait=None):
        shocktrait_d_newlist = []

        for st_d in self.shocktrait_d_list:
            shocktrait_name = st_d['shocktrait']['name']
            _name = shocktrait_name if shocktrait is None else shocktrait.name
            _target = st_d['target'] if target is None else target

            if st_d['target'] != _target or shocktrait_name != _name:
                shocktrait_d_newlist.append(st_d)
            
        self.shocktrait_d_list = shocktrait_d_newlist

    def removeShockTraitAt(self, i):
        del self.shocktrait_d_list[i]


class ShockScenarioModel:
    def __init__(self, name: str, basescen, **kwrags):
        self.name = name
        self.basescen = basescen
        self.shocked_scen_d = { 'basescen': basescen, **kwrags } # filename, Scenario, ScenarioResults
        self.shocked_scen_res_d = dict() # ScenarioResults
        self.shocked_scen_data_d = dict() # array data if requested

        self.timegrid_d = dict()
        self.initialize()

    def check_shocknames_exist(self, shock_names: list):
        for shk_nm in shock_names:
            if shk_nm not in self.shocked_scen_d:
                raise Exception("shock does not exist - {0} in {1}".format(shk_nm, self.shocked_scen_d))

    def check_pathname_exist(self, path_name: str):
        for shk_nm, v in self.shocked_scen_d.items():
            if not path_name in self.shocked_scen_res_d[shk_nm].nameList:
                raise Exception('path is not exist in scenario - {0}, {1}'.format(shk_nm, path_name))

    def initialize(self):
        # convert to ScenarioResults
        scen_res = None

        for k, v in self.shocked_scen_d.items():
            if isinstance(v, xen.Scenario):
                scen_res = v.generate() # generate first
            elif isinstance(v, xen.ScenarioResults):
                scen_res = v
            elif isinstance(v, str):
                scen_res = xen.ScenarioResults(v)
            else:
                raise Exception('Scenario, ScenarioResults or scenariofile(npz) is required - {0}, {1}'.format(k, v))

            self.shocked_scen_res_d[k] = scen_res
            self.timegrid_d[k] = scen_res.timegrid
    #
    def toDict(self):
        def get_filenam(v):
            if isinstance(v, xen.Scenario):
                return v.filename
            elif isinstance(v, xen.ScenarioResults):
                return v.filename
            elif isinstance(v, str):
                return v
            else:
                raise Exception('Scenario, ScenarioResults or scenariofile(npz) is required - {0}'.format(v))

        d = dict()

        d[mx.CLASS_TYPE_NAME] = ShockScenarioModel.__name__
        d['name'] = self.name
        d['basescen'] = get_filenam(self.basescen)
        
        # filename now
        _shocked_scen_d = dict()
        for k, scen in self.shocked_scen_d.items():
            _shocked_scen_d[k] = get_filenam(scen)

        _shocked_scen_d.pop('basescen')

        d['shocked_scen_d'] = _shocked_scen_d

        return d

    @staticmethod
    def fromDict(d: dict):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ShockScenarioModel.__name__)

        # _shocked_scen_d = dict()

        # for k, filename in d['shocked_scen_d'].items():
        #     _shocked_scen_d[k] = xen.ScenarioResults(filename)

        sm = ShockScenarioModel(d['name'], d['basescen'], **d['shocked_scen_d'])

        return sm

    def hashCode(self):
        return utils.get_hashCode(self)

    # 
    def select_shocked_scen_data_d(self, scenNm_param_tuples: list):
        # load if requested.
        # 
        # shock 별로 scenNm을 추출하고 param으로 mapping함
        # {
        #   'shock1': { 's1': [[1,2,3,4,5], [1,2,3,4,6], ... ], 's2': [1,2,3,4,5] }
        #   'shock2': { 's1': [1,2,3,4,5], 's2': [1,2,3,4,5] }
        # }
        #  
        res = dict()

        for k, v in self.shocked_scen_d.items():
            s_d = dict()
            shk_res = self.shocked_scen_res_d[k]
            shk_data = None

            # load data if not loaded
            # if isinstance(shk_data, xen.ScenarioResults):
            if not k in self.shocked_scen_data_d:
                numpyArr = shk_res.toNumpyArr()
                scen_arr = dict()

                # now all assets... -> requested?
                for info in shk_res.genInfo:
                    idx = int(info[0])
                    pathname = info[1]

                    scen_arr[pathname] = numpyArr[:,idx,:]

                self.shocked_scen_data_d[k] = scen_arr

            for tup in scenNm_param_tuples:
                assetNm = tup[0]
                param = tup[1]

                s_d[param] = self.shocked_scen_data_d[k][assetNm] # (simulNum, timegridNum)

            s_d['_timegrid'] = self.timegrid_d[k]
            res[k] = s_d


        return res



## shock manager
class ShockFileManager(mx.ManagerBase):
    def __init__(self, config):
        mx.ManagerBase.__init__(self, config)

        self.location = config['location']

        if not os.path.exists(self.location):
            raise Exception('directory does not exist - {0}'.format(self.location))
    
    def _build_dict(self, serializable):
        return serializable.toDict()

    def _save(self, name, ext, *args):
        json_str = None
        path = os.path.join(self.location, name + '.' + ext)

        d = dict()
        for arg in args:
            d[arg.name] = arg

        utils.save_file(path, d, self._build_dict)

    def _load(self, name, ext):
        path = os.path.join(self.location, name + '.' + ext)

        f = open(path, "r")
        json_str = f.read()
        shock_d = json.loads(json_str)

        res = dict()
        
        for k, v in shock_d.items():
            if ext == SHOCKTRAITFILE_EXT:
                res[k] = parseClassFromDict(v)
            elif ext == SHOCKFILE_EXT:
                res[k] = Shock.fromDict(v)
            elif ext == SHOCKMODELFILE_EXT:
                res[k] = ShockScenarioModel.fromDict(v)
            else:
                raise Exception('unknown shock file - {0}'.format(path))

        return res

    def save_sht(self, name, *args):
        self._save(name, SHOCKTRAITFILE_EXT, *args)

    def load_sht(self, name):
        return self._load(name, SHOCKTRAITFILE_EXT)

    def save_shk(self, name, *args):
        self._save(name, SHOCKFILE_EXT, *args)

    def load_shk(self, name):
        return self._load(name, SHOCKFILE_EXT)

    def save_shm(self, name, *args):
        self._save(name, SHOCKMODELFILE_EXT, *args)

    def load_shm(self, name):
        return self._load(name, SHOCKMODELFILE_EXT)


def build_shockedMrk(shock: Shock, mrk: mx.MarketData):
    mrk_clone = mrk.clone()
    
    target = None

    try:
        for st_d in shock.shocktrait_d_list:
            target = st_d['target']
            shocktrait = parseClassFromDict(st_d['shocktrait'])

            d = {}
            d_clone = {}

            if isinstance(shocktrait, QuoteShockTrait):
                d = mrk.quote
                d_clone = mrk_clone.quote
            elif isinstance(shocktrait, YieldCurveShockTrait):
                d = mrk.yieldCurve
                d_clone = mrk_clone.yieldCurve
            elif isinstance(shocktrait, VolTsShockTrait):
                d = mrk.volTs
                d_clone = mrk_clone.volTs

            for k, v in d.items():
                if fnmatch(k, target):
                    shocktrait.calculate(d_clone[k]) 

    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' - {0}, {1}'.format(shock.name, target),) + e.args[1:]
        raise

    return mrk_clone


def build_shockedScen(shock_list: list, sb: xen.ScenarioBuilder, mrk: mx.MarketData):
    res = []

    for shock in shock_list:
        shocked_mrk = build_shockedMrk(shock, mrk)
        shocked_scen = sb.build_scenario(shocked_mrk)
        res.append(shocked_scen)

    return res
        
