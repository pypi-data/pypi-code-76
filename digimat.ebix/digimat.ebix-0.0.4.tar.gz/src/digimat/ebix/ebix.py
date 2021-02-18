from __future__ import print_function
import os

import pkg_resources

import logging
import logging.handlers

from functools import lru_cache
import xml.etree.ElementTree as ET

# from prettytable import PrettyTable
from io import BytesIO
import gzip
import re

# pip install pytz
from pytz import UTC

# pip install pyyaml
import yaml

from ftplib import FTP

from dateutil.parser import parse as dtparser
import datetime


UNIT_STR = ["V", "C", "Pa", "kPa", "%", "l/h", "bar", "Hz",
    "s", "ms", "min", "kW", "kWh", "J", "kJ", "",
    "m/s", "'", "h", "MWh", "MJ", "GJ", "W", "MW",
    "kJ/h", "MJ/h", "GJ/h", "ml", "l", "m3", "ml/h", "m3/h",
    "Wh", "?", "K", "", "lx", "t/min", "kvar", "kvarh",
    "mbar", "msg/m", "m", "kJ/kg", "g/kg", "ppm", "A", "kVA",
    "kVAh", "ohm"]


# Empty = 0,       // pas de flags
# Alarm = 1,      // A [1] alarme
# AlarmAck = 2,   // K [2] alarme quitancée
# Warning = 4,    // W [4] avertissements
# Error = 8,      // E [8] erreur
# Manual = 0x10,   // M [16] manuel
# Derogation = 0x20,   // D [32] dérogation,
# Event = 0x40,   // V [64] événements
# Device = 0x80,  // X [128] propre au device
# Denied = 0x100, // R [256] accès refusé
# Unknown = 0x200, // U [512] ressurce inconnue
# Timeout = 0x400, // T [1024] time-out

class DIGFlags(object):

    FLAGS = {'A': 1, 'K': 2, 'W': 4, 'E': 8, 'M': 16, 'D': 32, 'V': 64, 'X': 128, 'R': 256, 'U': 512, 'T': 1024}

    def __init__(self, flags=None):
        self._flags={}
        self.set(flags)

    def has(self, flags):
        if flags:
            for f in flags:
                if not self._flags.get(f.upper()):
                    return False
            return True
        return False

    def set(self, flags):
        if flags:
            for f in flags:
                f=f.upper()
                if f in self.FLAGS:
                    self._flags[f]=self.FLAGS[f]

    def flags(self):
        if self._flags:
            flags=''
            for f in self._flags.keys():
                flags+=f
            return flags

    def code(self):
        fcode=0
        if self._flags:
            for f in self._flags.values():
                fcode+=f
        return fcode

    def setError(self):
        self.set('E')


class EBIXCodes(object):
    def __init__(self, data=None):
        self._codes={}
        self.update(data)

    def update(self, data):
        if data:
            self._codes.update(data)

    def isLoaded(self):
        if self._codes:
            return True
        return False

    def load(self):
        pass

    def get(self, code):
        try:
            if not self.isLoaded():
                self.load()
            return self._codes[code]
        except:
            pass

    def label(self, code):
        try:
            return self.get(code)['label']
        except:
            pass

    def __getitem__(self, key):
        return self.label(key)


class EBIXBusinessReasonCodes(EBIXCodes):
    def load(self):
        data={'C10': {'label': 'Check Information'},
            'C11': {'label': 'Kostenzuteilung (Systemdienstleistung)'},
            'C12': {'label': 'Kostenwaelzung'},
            'C13': {'label': 'Order energy'},
            'C14': {'label': 'Reserved'},
            'C15': {'label': 'Reserved'},
            'C16': {'label': 'Start of ancillary service provider'},
            'C17': {'label': 'End of Ancillary service provider'},
            'C18': {'label': 'Change of masterdata party connected to the grid'},
            'C19': {'label': 'Change of masterdata metering point'},
            'C20': {'label': 'Query metering point identifier'},
            'C21': {'label': 'Query switch information'},
            'C22': {'label': 'Query metering point information'},
            'C23': {'label': 'Query validated metered data'},
            'C24': {'label': 'Query aggregated metered data'},
            'C25': {'label': 'Ersatzversorgung'},
            'C37': {'label': 'Metered data Ostral PS'},
            'C87': {'label': 'Ancillary service for CRF'},
            'E03': {'label': 'Change of balance supplier'},
            'E05': {'label': 'Cancellation'},
            'E06': {'label': 'Unrequested change of balance supplier'},
            'E0D': {'label': 'Labelling Energie'},
            'E20': {'label': 'End of supply'},
            'E44': {'label': 'Imbalance settlement'},
            'E88': {'label': 'Billing energy'},
            'E89': {'label': 'Billing grid cost'},
            'E92': {'label': 'Change of Party Connected to the Grid'},
            'E93': {'label': 'End of Party Connected to the Grid'}}
        self.update(data)


class EBIXDocumentTypeCodes(EBIXCodes):
    def load(self):
        data={'312': {'label': 'Acknowledgement of acceptance'},
            '313': {'label': 'Model Error Report'},
            '392': {'label': 'Request for change of role connected to Metering Point'},
            '414': {'label': 'Response to Request for change of role connected to Metering Point'},
            'C01': {'label': 'Notification from Imbalance Settlement Responsible'},
            'C02': {'label': 'Notification from the Metered Data Aggregator'},
            'C03': {'label': 'Query Information'},
            'C04': {'label': 'Masterdata Supply Contract'},
            'C05': {'label': 'INVOICE'},
            'C06': {'label': 'CORRECTION'},
            'C07': {'label': 'ACCEPTANCE'},
            'C08': {'label': 'REJECTION'},
            'E07': {'label': 'Master data metering point'},
            'E21': {'label': 'Master data Party connected to the grid'},
            'E31': {'label': 'Aggregated metered data'},
            'E44': {'label': 'Notification of change of role connected to a metering point'},
            'E66': {'label': 'Validated metered data'},
            'E67': {'label': 'Request for cancellation of a business process'},
            'E68': {'label': 'Confirmation/rejection of cancellation of a business process'}}
        self.update(data)


class EBIXBusinessRoleCodes(EBIXCodes):
    def load(self):
        data={'DDK': {'label': 'BalaAncillary service provider nce responsible party'},
            'DDM': {'label': 'Grid access provider'},
            'DDQ': {'label': 'Balance supplier'},
            'DDX': {'label': 'Imbalance settlement responsible'},
            'DDZ': {'label': 'Metering point administrator'},
            'DEA': {'label': 'Metered data aggregator, local'},
            'DEC': {'label': 'Party connected to the grid'},
            'GD': {'label': 'Producer'},
            'MDR': {'label': 'Metered data responsible'},
            'PQ': {'label': 'Certifying Party'},
            'UD': {'label': 'Consumer'},
            'ASP': {'label': 'Ancillary service provider'},
            'Z04': {'label': 'Metered data aggregator, central'},
            'Z06': {'label': 'Reconciliation responsible'},
            'Z07': {'label': 'Reconciled difference responsible'},
            'Z08': {'label': 'Billing agent'}}
        self.update(data)


class EBIXEicCodes(EBIXCodes):
    def __init__(self, fileName):
        super(EBIXEicCodes, self).__init__()
        self._filePath=self.getFilePath(fileName)

    def getFilePath(self, fileName):
        try:
            fpath=os.path.join(os.path.dirname(__file__), 'data', fileName)
            if os.path.exists(fpath):
                return fpath
        except:
            pass

    def load(self):
        # <EicCode>
        # <Spezifikation__c>E</Spezifikation__c>
        # <EIC_Code__c>12XAEW-ENERGIE-E</EIC_Code__c>
        # <Display_Name__c>AEW</Display_Name__c>
        # <Function__c>Sales & Trading</Function__c>
        # <Name>AEW Energie AG</Name>
        # <PLZ__c>5001</PLZ__c>
        # <Ort__c>Aarau</Ort__c>
        # <Date__c>2006-01-17</Date__c>
        # </EicCode>
        try:
            data={}
            tree=ET.parse(self._filePath)
            root=tree.getroot()
            for item in root.iter('EicCode'):
                try:
                    code=item.find('EIC_Code__c').text
                    label=item.find('Name').text
                    data[code]={'label': label}
                except:
                    pass
            self.update(data)
        except:
            pass


class EBIXLogger(object):
    def __init__(self, title="EBIX"):
        self._title=title

    def create(self):
        return logging.getLogger(self._title)

    def tcp(self, level=logging.DEBUG, host='localhost'):
        logger=self.create()
        logger.setLevel(level)
        handler = logging.handlers.SocketHandler(host, logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        logger.addHandler(handler)
        return logger

    def null(self):
        logger=self.create()
        logger.setLevel(logging.ERROR)
        handler=logging.NullHandler()
        logger.addHandler(handler)
        return logger


BUSINESS_REASONS=EBIXBusinessReasonCodes()
BUSINESS_ROLES=EBIXBusinessRoleCodes()
DOCUMENT_TYPE=EBIXDocumentTypeCodes()
EIC_X=EBIXEicCodes('io-ch-eic-list-x-codes.xml')
EIC_Y=EBIXEicCodes('io-ch-eic-list-y-codes.xml')
EIC_W=EBIXEicCodes('io-ch-eic-list-w-codes.xml')


class EBIXDecoder(object):
    def __init__(self, fname, data, logger):
        self._logger=logger
        self._fname=fname
        self._namespace=None
        self._meta={}
        self.setMeta('config', {})
        try:
            root=ET.fromstring(data)
            if self.load(root):
                return
        except:
            # self.logger.exception('init')
            pass
        raise ValueError('ebix file content error!')

    @property
    def logger(self):
        return self._logger

    @property
    def fname(self):
        return self._fname

    def itemName(self, name):
        if self._namespace:
            return '%s%s' % (self._namespace, name)
        return name

    def child(self, xml, name):
        node=xml.find(self.itemName(name))
        if node is None:
            # self.logger.warning('xml child %s not found!' % name)
            raise ValueError('non existent xml child %s' % name)
        return node

    def children(self, xml, name):
        nodes=xml.findall(self.itemName(name))
        if nodes is None:
            # self.logger.warning('xml child %s not found!' % name)
            raise ValueError('non existent xml children %s' % name)
        return nodes

    def setMeta(self, key, value):
        self._meta[key]=value

    def setMetaDate(self, key, value):
        self.setMeta(key, dtparser(value))

    def getMeta(self, key):
        try:
            return self._meta[key]
        except:
            pass

    @property
    def meta(self):
        return self._meta

    def __getitem__(self, key):
        return self.getMeta(key)

    def __setitem__(self, key, value):
        self.setMeta(key, value)

    @property
    def mid(self):
        return self['meterId']

    @property
    def unit(self):
        return self['meterUnit']

    @property
    def measures(self):
        return self._measures

    def count(self):
        return len(self._measures)

    def __len__(self):
        return self.count()

    def isEmpty(self):
        try:
            if self.count()>0:
                return False
        except:
            pass
        return True

    @lru_cache()
    def getUnitFromStr(self, unit):
        try:
            unit=unit.lower()
            for n in range(len(UNIT_STR)):
                if unit==UNIT_STR[n].lower():
                    return n
        except:
            pass
        try:
            return UNIT_STR[int(unit)]
        except:
            pass

    def validateData(self, root):
        try:
            if root:
                self['fname']=self._fname
                self._header=self.child(root, 'ValidatedMeteredData_HeaderInformation')

                nodeInstanceDocument=self.child(self._header, 'InstanceDocument')
                nodeDocumentType=self.child(nodeInstanceDocument, 'DocumentType')
                self['documentType']=self.child(nodeDocumentType, 'ebIXCode').text
                self['documentTypeStr']=DOCUMENT_TYPE[self['documentType']]

                nodeBusinessScopeProcess=self.child(self._header, 'BusinessScopeProcess')
                nodeBusinessReasonType=self.child(nodeBusinessScopeProcess, 'BusinessReasonType')
                self['businessReasonType']=self.child(nodeBusinessReasonType, 'ebIXCode').text
                self['businessReasonTypeStr']=BUSINESS_REASONS[self['businessReasonType']]

                self._metering=self.child(root, 'MeteringData')

                node=self.child(self._metering, 'Interval')
                self['start']=dtparser(self.child(node, 'StartDateTime').text)
                self['end']=dtparser(self.child(node, 'EndDateTime').text)

                node=self.child(self._metering, 'Resolution')
                value=float(self.child(node, 'Resolution').text)
                unit=self.child(node, 'Unit').text.lower()

                # AMP ampere
                # ANN Year
                # B8 Joule per cubic metre
                # D90 Cubic meter (net)
                # DAY Day
                # E46 Kilowatt hour per cubic metre
                # G52 Cubic metre per day
                # HUR Hour
                # K3 kVArh (kVA reactive-hour)
                # KWH Kilowatt hour
                # KWN Kilowatt hour per normalized cubic metre
                # KWS Kilowatt hour per standard cubic metre
                # KWT Kilowatt
                # MAW Megawatt
                # MIN Minute
                # MON Month
                # MQH Cubic Meter per Hour
                # MTQ Cubic Meter
                # MWH Megawatt hour
                # NM3 Normalised cubic metre
                # Q37 Standard cubic metre per day
                # Q38 Standard cubic metre per hour
                # Q39 Normalized cubic metre per day
                # Q40 Normalized cubic metre per hour
                # Q41 Joule per normalized cubic metre
                # Q42 Joule per standard cubic

                if unit=='min':
                    value*=60
                elif unit=='HUR':
                    value*=3600
                elif unit=='DAY':
                    value*=3600*24
                else:
                    self.logger.error('Unsupported resolution unit %s' % unit)
                    return False
                self['resolution']=value
                self['countRequired']=(self['end']-self['start']).total_seconds()/self['resolution']

                node=self.child(self._metering, 'ConsumptionMeteringPoint')
                self['meterId']=self.child(node, 'VSENationalID').text
                factor=1.0

                node=self.child(self._metering, 'Product')
                unit=self.child(node, 'MeasureUnit').text.lower()
                self['meterUnit']=unit

                if unit=='kwh':
                    pass
                elif unit=='k3':
                    unit='kvarh'
                elif unit=='kwt':
                    unit='kw'
                elif unit=='amp':
                    unit='a'
                elif unit=='mtq':
                    unit='m3'
                elif unit=='mwh':
                    unit=='kwh'
                    factor=1000.0

                self['meterFactor']=factor

                self['meterDigimatUnit']=self.getUnitFromStr(unit)
                self['meterDigimatUnitStr']=unit
                if not self['meterDigimatUnit']:
                    self.logger.error('Unable to convert unit %s to a valid Digimat unit!' % unit)
                    return False

                node=self.child(self._metering, 'Product')
                observations=self.children(self._metering, 'Observation')

                self['count']=len(observations)
                if self['count']!=self['countRequired']:
                    self.logger.error('found %d measures, should have %d!' % (self['count'], self['countRequired']))
                    return False

                t0=self['start']
                t1=self['end']
                dt=datetime.timedelta(seconds=self['resolution'])

                measuresFlagsFound=[]
                measures=[]
                for observation in observations:
                    position=int(self.child(self.child(observation, 'Position'), 'Sequence').text)
                    t=t0+dt*(position-1)
                    if t<t0 or t>t1:
                        self.logger.error('observation %d time not included in ebix timerange (%s<=%s<=%s)!' % (position, t0, t, t1))
                        return False
                    value=float(self.child(observation, 'Volume').text)*factor

                    flags=DIGFlags()
                    try:
                        condition=int(self.child(observation, 'Condition').text)
                        if condition not in measuresFlagsFound:
                            measuresFlagsFound.append(condition)

                        if condition in [21]:
                            flags.setError()

                        # condition 56 = Estimated (this should be a definitive value)
                    except:
                        pass

                    measure=[t, value, flags.code()]
                    # print(measure)
                    measures.append(measure)

                self._measures=measures
                self['measuresFlagsFound']=measuresFlagsFound
                self.logger.debug(str(self.meta))
                return True
        except:
            self.logger.exception('validateData()')
        return False

    def load(self, root):
        try:
            self._namespace=re.match(r'{.*}', root.tag).group(0)
            if self.validateData(root):
                return True
        except:
            pass
        raise ValueError('Invalid xml file format')

    def stampForTz(self, dt, tz=UTC):
        return dt.astimezone(tz=tz).strftime('%Y%m%d%H%M%S')

    def stampUTC(self, dt):
        return self.stampForTz(dt, tz=UTC)

    def measureToString(self, key, measure):
        data=[
            self.stampUTC(measure[0]),
            key,
            str(measure[1]),  # value
            str(measure[2]),  # flags
            str(self['meterDigimatUnitStr'])]
        # print(measure, data)
        return ';'.join(data)

    def compressData(self, data):
        """gzip the given data to a BytesIO (must be closed by caller)"""
        if data:
            gzdata = BytesIO()
            try:
                with gzip.GzipFile(mode='wb', fileobj=gzdata) as gzip_obj:
                    gzip_obj.write(data.getvalue())
                gzdata.seek(0)
                return gzdata
            except:
                self.logger.exception('%s:compress()')
                gzdata.close()

    def getCompressedDCFRecordsData(self, key):
        """encode measures to a gzdata buffer (must be closed by caller)"""
        if self._measures:
            data=BytesIO()
            try:
                for measure in self.measures:
                    data.write(self.measureToString(key, measure).encode())
                    data.write('\n'.encode())
                data.seek(0)
                try:
                    gzdata=self.compressData(data)
                    return gzdata
                except:
                    gzdata.close()
            finally:
                data.close()


class EBIX(object):
    def __init__(self, host, user, password, rootPath, logger=None):
        if logger is None:
            logger=EBIXLogger().tcp()
        self._logger=logger
        self._host=host
        self._user=user
        self._password=password
        self._rootPath=rootPath
        self._ftp=None
        self._meters={}

    def getVersion(self):
        try:
            distribution=pkg_resources.get_distribution('digimat.ebix')
            return distribution.parsed_version
        except:
            pass

    @property
    def version(self):
        return self.getVersion()

    @property
    def logger(self):
        return self._logger

    def mkdir(self, name):
        try:
            self.connect().mkd(name)
        except:
            pass

    def registerMeter(self, meterId, config):
        self.logger.info('Declaring meter %s %s' % (meterId, config))
        self._meters[meterId]=config

    def getMatchingMeterKeyFromConfig(self, ebix):
        try:
            config=self._meters[ebix['meterId'].upper()]
        except:
            return

        try:
            ebix.setMeta('config', config)

            # a meter could send more than one measure
            # at this moment, the meterid + meterunit (digimatunit) is used to match a digimat key
            unit=config['unit'].lower()
            if not unit or unit!=ebix['meterDigimatUnitStr'].lower():
                return

            try:
                require=config['require']
                for key, value in require.items():
                    if ebix[key].lower()!=value.lower():
                        return
            except:
                pass

            return config['key']
        except:
            pass

    def loadConfig(self):
        files=self.retrieveConfigFiles()
        if files:
            for f in files:
                data=self.retrieveData(f).decode()
                config=yaml.load(data, Loader=yaml.FullLoader)
                for meter in config['meters']:
                    meterId=list(meter)[0].upper()
                    meterConfig=meter[meterId]
                    self.registerMeter(meterId, meterConfig)

    def connect(self):
        try:
            if not self._ftp:
                self.logger.debug('connect FTP(%s/%s)' % (self._host, self._user))
                self._ftp=FTP(self._host, self._user, self._password, timeout=5.0)
                self._ftp.set_pasv(True)
                if self._rootPath:
                    self.logger.debug('change remote directory to %s' % self._rootPath)
                    self._ftp.cwd(self._rootPath)
                self.mkdir('config')
                self.mkdir('archive')
                self.mkdir('unknown')
                self.mkdir('rejected')
                self.mkdir('bad')
                self.loadConfig()
        except:
            self.logger.exception('x')
            self.close()
        return self._ftp

    def close(self):
        try:
            self._ftp.quit()
            self.logger.debug('disconnect FTP(%s)' % (self._host))
        except:
            pass
        self._ftp=None

    def retryBad(self):
        ftp=self.connect()
        try:
            flist=ftp.nlst()
            for f in flist:
                (fname, fext)=os.path.splitext(f)
                if fext=='.bad':
                    self.logger.debug('renaming .bad file %s' % fname)
                    ftp.rename(f, fname)
        except:
            pass

    def retrieveFiles(self, path=None):
        ftp=self.connect()
        try:
            flist=ftp.nlst(path)
            if flist:
                # in EBIX file order my be important as newer values can overwrite older ones
                # so, sort files by name (the name contains the date)
                flist=sorted(flist)
                return flist
        except:
            pass

    def retrieveFilesWithExtension(self, extension, path=None):
        files=self.retrieveFiles(path)
        if files:
            extension='.%s' % extension.lower()
            flist=[]
            for f in files:
                try:
                    fext=os.path.splitext(f)[1].lower()
                    if fext==extension:
                        flist.append(f)
                except:
                    pass
            return flist

    def retrieveEbixFiles(self):
        return self.retrieveFilesWithExtension('xml', 'inbox')

    def retrieveConfigFiles(self):
        return self.retrieveFilesWithExtension('yaml', 'config')

    def retrieveData(self, fname):
        ftp=self.connect()
        try:
            self.logger.debug('FTP downloading file %s...' % fname)
            buf=BytesIO()
            ftp.retrbinary('RETR %s' % fname, buf.write)
            buf.seek(0)
            data=buf.getvalue()
            buf.close()
            return data
        except:
            self.logger.exception('ftpRetrieve(%s) error!' % fname)
            self.close()

    def moveToBad(self, ebix):
        try:
            fname=os.path.basename(ebix['fname'])
            ftp=self.connect()
            self.logger.warning('Moving ftp file %s to bad repository' % fname)
            ftp.rename('inbox/%s' % fname, 'bad/%s' % fname)
        except:
            pass

    def moveToUnknown(self, ebix):
        try:
            fname=os.path.basename(ebix['fname'])
            ftp=self.connect()
            self.logger.warning('Moving ftp file %s to unknown repository' % fname)
            ftp.rename('inbox/%s' % fname, 'unknown/%s' % fname)
        except:
            self.logger.exception('move')
            pass

    def moveToRejected(self, ebix):
        try:
            fname=os.path.basename(ebix['fname'])
            ftp=self.connect()
            self.logger.warning('Moving ftp file %s to rejected repository' % fname)
            ftp.rename('inbox/%s' % fname, 'rejected/%s' % fname)
        except:
            self.logger.exception('move')
            pass

    def moveToArchive(self, ebix):
        try:
            fname=os.path.basename(ebix['fname'])
            ftp=self.connect()
            self.logger.info('Archiving ftp file %s' % fname)
            ftp.rename('inbox/%s' % fname, 'archive/%s' % fname)
        except:
            self.logger.exception('move')
            pass

    # def remove(self, ebix):
        # try:
            # fname=ebix['fname']
            # ftp=self.connect()
            # self.logger.info('Removing ftp file %s' % fname)
            # return ftp.delete(fname)
        # except:
            # self.logger.exception('move')
            # pass

    def processEbix(self, ebixi, key):
        raise NotImplementedError

    def load(self, maxcount=0):
        files=self.retrieveEbixFiles()
        if maxcount>0:
            files=files[0:maxcount]

        if files:
            if not self._meters:
                self.logger.error('No meters declared in config files!')
                return

            for fname in files:
                data=self.retrieveData(fname)
                if data:
                    try:
                        ebix=EBIXDecoder(fname, data, logger=self.logger)
                        try:
                            key=self.getMatchingMeterKeyFromConfig(ebix)
                            if key:
                                if self.processEbix(ebix, key):
                                    self.moveToArchive(ebix)
                            else:
                                if ebix['config']:
                                    # This meter was found in the config list
                                    self.moveToRejected(ebix)
                                else:
                                    self.moveToUnknown(ebix)
                        except:
                            self.logger.exception('processEbix()')
                            self.moveToBad(fname)
                    except:
                        self.moveToBad(fname)

        self.close()


if __name__ == "__main__":
    pass
