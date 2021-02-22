import time
import pickle
import gzip
import os
import uuid
from .functions import Parallelize

VARIABLES = {
    'driving': [
        'name', 'kind', 'profile', 't', 'totalrows', 'hours', 'f', 'refdate',
        'states', 'timeseries'
    ],
    'consumption': [
        'name', 'input', 'kind', 'profile', 't', 'totalrows', 'hours', 'f',
        'refdate', 'states', 'vehicle', 'timeseries'
    ],  # 'Trips', 'timeseries'
    'availability': [
        'name', 'input', 'kind', 'profile', 'timeseries', 'chargingdata',
        'battery_capacity', 'charging_eff', 'discharging_eff', 'soc_init',
        'soc_min', 't', 'totalrows', 'refdate', 'success', 'notation'
    ],
    'charging': ['name', 'kind', 'input', 'option', 'timeseries', 'success']
}


class DataBase(object):
    """
    DataBase object useful to manage many
    self.__init__(folder)
        folder: path as string of folder where profiles are hosted.
    optional:
        self.loadfiles(loaddir)
            in this case, some profiles can be hosted in a directory other than the "folder".
            So that diectory must be indicated (loaddir). In this way profiles from many directories can be loaded.
        self.update()
            loads files from database "folder"
    important attribute:
        self.db : It is a dictionary that contains all profiles. The dictionary keys are the name of the profile
            Every profile in this dict has nested dictionary. The keys depend on the type of profile.
            Common keys:
                self.db["name of the profile"]["kind"] that can be ["driving", "availability", "charging"]
                self.db["name of the profile"]["input"] that is a string only for ["availability", "charging"] profiles
    """
    def __init__(self, folder):
        super(DataBase, self).__init__()

        self.name = ''
        self.folder = folder
        self.oldpath = []
        self.db = {}

    def loadfiles(self, loaddir=''):
        if loaddir:
            self.repo = loaddir
        else:
            self.repo = self.folder
        os.makedirs(self.repo, exist_ok=True)
        self.currentpath = [
            f for f in os.listdir(self.repo)
            if os.path.isfile(os.path.join(self.repo, f))
        ]
        self.path_list = list(set(self.currentpath) - set(self.oldpath))
        if self.path_list:
            self.oldpath = self.currentpath

        for f in self.path_list:
            self.fpath = os.path.join(self.repo, f)
            if f.split('.')[-1] == 'pickle':
                self.pickle_off = gzip.open(self.fpath, "rb")
                self.obj = pickle.load(self.pickle_off)
                self.pickle_off.close()
                self.db[self.obj['name']] = self.obj
                del self.pickle_off

    def loadfilesBatch(self,
                       loaddir='',
                       batch=10,
                       nr_workers=4,
                       kind='',
                       add_variables=[]):
        variables = list(set(VARIABLES[kind] + add_variables))
        if loaddir:
            self.repo = loaddir
        else:
            self.repo = self.folder
        os.makedirs(self.repo, exist_ok=True)
        self.currentpath = [
            f for f in os.listdir(self.repo)
            if os.path.isfile(os.path.join(self.repo, f))
        ]
        # create batch
        i = 0
        nr_files = len(self.currentpath)
        paths_batch = []
        flag = False
        for _ in range(nr_files):
            batch_ = []
            for _ in range(batch):
                if i < nr_files:
                    batch_.append(self.currentpath[i])
                else:
                    flag = True
                    break
                i += 1
            if len(batch_) > 0:
                paths_batch.append(batch_)
            if flag:
                break
        for lt in paths_batch:
            dc = {
                k: {
                    'f': os.path.join(self.repo, v)
                }
                for k, v in enumerate(lt) if v.split('.')[-1] == 'pickle'
            }
            odc = Parallelize(self.loadpkl, dc, nr_workers,
                              **dict(variables=variables, kind=kind))
            print(len(odc))
            for j in odc:
                if odc[j][1]:
                    self.db[odc[j][0]['name']] = odc[j][0]

    @staticmethod
    def loadpkl(f, variables, kind):
        pickle_off = gzip.open(f, "rb")
        obj = pickle.load(pickle_off)
        pickle_off.close()
        if obj['kind'] == kind:
            new_obj = {}
            for nm in variables:
                if nm in obj:
                    new_obj[nm] = obj[nm]
            return new_obj, True
        else:
            return {}, False

    def update(self):
        self.loadfiles()

    def getdb(self):
        self.update()
        return self.db

    def remove(self, name):
        self.acum = []
        self.db.pop(name, None)
        if os.path.isfile(os.path.join(self.folder, name + '.pickle')):
            os.remove(os.path.join(self.folder, name + '.pickle'))
            self.acum.append(name + '.pickle')
        self.update()
        print('Files deleted:', len(self.acum))
        print(self.acum)
        del self.acum


class DataManager:
    ''' docstring DataManager '''
    def __init__(self):
        super(DataManager, self).__init__()

    def savedb(self, object, dbdir='db_files'):
        object.update()
        if not object.name:
            nnn = 'db_' + time.strftime("%Y%m%d_%H%M%S") + '_' + uuid.uuid4(
            ).hex[:5]  # + time.strftime("%Y%m%d_%H%M%S")
            object.name = nnn[:]
        os.makedirs(dbdir, exist_ok=True)
        with gzip.open(os.path.join(dbdir, object.name + '.pickle'),
                       'wb') as datei:
            pickle.dump(object, datei)
        print(datei)
        print('=== Database saved ===')

    def loaddb(self, dbfilepath, profilesdir):
        with gzip.open(dbfilepath, 'rb') as datei:
            obj = pickle.load(datei)
        obj.folder = profilesdir
        obj.update()
        return obj
