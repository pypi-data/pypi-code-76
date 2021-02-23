from __future__ import print_function

import datetime
import logging
import os
import re
import sys

import pprint as pp
import urllib
import magic
import easyprocess
import pathos
import pydicom
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import natsort
import json
import jsbeautifier
import uuid
import zipfile
from dirhash import dirhash


class XnatUploadToolDicom:
    def __init__(self, **kwargs):
        # Designed to be called from script using argparse, otherwise dict must be passed in as kwargs with
        # all following variables set
        try:
            self.args = kwargs

            self.starttime = None
            self.httpsess = None
            self.lastrenew = None
            self.logger = None
            self.prearcdate = False

            self.host = kwargs['host'].rstrip('/')
            self.localval = dict()
            self.upload_time = int()
            self.build_time = int()
            self.archive_time = int()
            self.verbose = kwargs['verbose']
            self.logfile = kwargs['logfile']
            self.filemap = list()

            self.fullmap = dict()

            self.dircount = 0
            self.filecount = 0
            self.dfilecount = 0
            self.uploadcount = 0
            self.newsessions = 0
            self.newscans = 0
            self.newuploads = 0

            self.fullmap = dict()
            self.checked_values = {'projects': {}}
            self.sessionmap = {'projects': {}, 'nondicom': list()}
            self.mapcounts = {'projects': 0, 'subjects': 0, 'sessions': 0, 'scans': 0}

            # Pull u/p from env if not set in args
            if kwargs['username'] is None or kwargs['password'] is None:
                (self.username, self.password) = os.environ['XNATCREDS'].split(':', 2)
            else:
                self.username = kwargs['username']
                self.password = kwargs['password']

            self.timeout = kwargs['timeout']
            self.sessiontimeout = datetime.timedelta(minutes=kwargs['sessiontimeout'])

            if 'jobs' in kwargs and kwargs['jobs'] is not None:
                self.threads = kwargs['jobs']
            else:
                self.threads = 1
            self.project = self.strip_invalid(kwargs['project'])
            self.subject = kwargs['subject']
            self.projectlabel = kwargs['projectlabel']
            self.splitlabel = kwargs['splitlabel']
            self.deletesessions = kwargs['deletesessions']
            self.target = kwargs['target']
            self.splitsample = kwargs['splitsample']

            self.uploadnondicom = kwargs['uploadnondicom']
            self.nondicomlevel = 'project'

            self.gradual = kwargs['gradual']

            self.dumpmap = kwargs['dumpmap']
            self.tmpdir = kwargs['tmpdir']

            self.note = kwargs['note']

            if kwargs['progress'] is not None:
                self.reportcount = int(kwargs['progress'])
            else:
                self.reportcount = None
            self.benchmark = kwargs['benchmark']

            # Set up logging
            self.setup_logger()

            if not os.path.exists(self.target):
                self.logger.error("Target directory %s does not exist, exiting." % self.target)
                exit(1)

            tagmatch = re.compile("^\(([0-9a-fA-F]+),([0-9a-fA-F]+)\)$")

            if kwargs['pulltag'] is not None:
                if tagmatch.match(kwargs['pulltag']) is not None:
                    self.pulltag = [hex(int(tagmatch.search(kwargs['pulltag'].upper()).group(1), 16)),
                                    hex(int(tagmatch.search(kwargs['pulltag'].upper()).group(2), 16))]
                    mytag = self.pull_single_dicom_tag()
                    if mytag is not None:
                        print("%s" % mytag)
                    else:
                        self.logger.error("Pull tag requested for %s, unable to find" %
                                          kwargs['pulltag'])
                        exit(1)
                    exit(0)
                else:
                    self.logger.error("Pull tag requested for %s, invalid format, needs (0000,0000)" %
                                      kwargs['pulltag'])
                    exit(1)

            if kwargs['splitlabel'] is not None and tagmatch.match(kwargs['splitlabel']) is not None:
                self.splitlabel = [hex(int(tagmatch.search(kwargs['splitlabel'].upper()).group(1), 16)),
                                   hex(int(tagmatch.search(kwargs['splitlabel'].upper()).group(2), 16))]

            if kwargs['projectlabel'] is not None:
                if tagmatch.match(kwargs['projectlabel']) is not None:
                    self.projectlabel = [hex(int(tagmatch.search(kwargs['projectlabel'].upper()).group(1), 16)),
                                         hex(int(tagmatch.search(kwargs['projectlabel'].upper()).group(2), 16))]
                else:
                    self.nondicomlevel = 'project'

            if tagmatch.match(kwargs['subjectlabel']) is None:
                self.logger.error('Subject tag %s is not in valid format.' % kwargs['subjectlabel'])
                exit(1)
            else:
                if tagmatch.match(kwargs['subjectlabel']) is not None:
                    self.subjectlabel = [hex(int(tagmatch.search(kwargs['subjectlabel'].upper()).group(1), 16)),
                                         hex(int(tagmatch.search(kwargs['subjectlabel'].upper()).group(2), 16))]
                else:
                    self.nondicomlevel = 'subject'

            if tagmatch.match(kwargs['sessionlabel']) is None:
                self.logger.error('Session tag %s is not in valid format.' % self.sessionlabel)
                exit(1)
            else:
                if tagmatch.match(kwargs['subjectlabel']) is not None:
                    self.sessionlabel = [hex(int(tagmatch.search(kwargs['sessionlabel'].upper()).group(1), 16)),
                                         hex(int(tagmatch.search(kwargs['sessionlabel'].upper()).group(2), 16))]
                else:
                    self.nondicomlevel = 'session'

            if tagmatch.match(kwargs['sessiondate']) is None:
                self.logger.error('Session date %s is not in valid format.' % self.sessionlabel)
                exit(1)
            else:
                self.sessiondate = [hex(int(tagmatch.search(kwargs['sessiondate'].upper()).group(1), 16)),
                                    hex(int(tagmatch.search(kwargs['sessiondate'].upper()).group(2), 16))]

            if tagmatch.match(kwargs['scandate']) is None:
                self.logger.error('Session date %s is not in valid format.' % self.sessionlabel)
                exit(1)
            else:
                self.scandate = [hex(int(tagmatch.search(kwargs['scandate'].upper()).group(1), 16)),
                                 hex(int(tagmatch.search(kwargs['scandate'].upper()).group(2), 16))]

            self.scanuid = ['0x20', '0xe']
            self.sessionuid = ['0x20', '0xd']
            self.scanlabel = ['0x20', '0x11']
            self.modality = ['0x8', '0x60']
            self.seriesdesc = ['0x8', '0x103e']
            self.studydesc = ['0x8', '0x1030']

            # Initialize Sessions
            self.renew_httpsession()
        except KeyError as e:
            logging.error('Unable to initialize uploader, missing argument: %s' % str(e))
            exit(1)

    def setup_logger(self):
        # Set up logging
        hdlr = None
        if self.logfile is not None:
            if os.path.exists(os.path.dirname(os.path.realpath(self.logfile))):
                hdlr = logging.FileHandler(self.logfile)
            else:
                logging.error('Log path %s does not exists' % str(self.logfile))
                exit(1)
        else:
            hdlr = logging.StreamHandler(sys.stdout)

        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        if self.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        if self.splitsample:
            self.logger.setLevel(logging.NOTSET)
        return True

    def setup_upload(self):
        self.logger.info('Preparing for dicom upload of %s to %s as %s' % (self.target, self.host, self.username))
        if self.dumpmap:
            self.logger.info('Mapdump requested to %s, no files will be uploaded' % self.dumpmap)
        return True

    def start_upload(self):
        self.setup_upload()
        self.analyze_dir(self.target)

        if self.dumpmap:
            self.sessionmap_dump()
            exit(0)

        self.logger.info('Beginning dicom upload of %d scans' % self.mapcounts['scans'])

        # Facilitate single threaded/parallel upload
        uploadcount = 0
        upsize = 0
        ndfiles = 0
        totaluptime = 0
        utype = None

        uploadedfilecount = 0
        starttime = datetime.datetime.now()
        prevmarker = 0

        # Walk sessionmap and batch upload each scan as a single push
        for tpro in self.sessionmap['projects']:
            for tsub in self.sessionmap['projects'][tpro]['subjects']:
                for tses in self.sessionmap['projects'][tpro]['subjects'][tsub]['sessions']:
                    for sid, sobj in self.sessionmap['projects'][tpro]['subjects'][tsub]['sessions'][tses]['scans'].\
                            items():
                        if self.gradual:
                            # Use gradual importer
                            utype = 'gradual'
                            (myuploadcount, mysumsize, myuptime) = self.grad_upload_scan(tpro, tsub, tses, sid, sobj)
                        else:
                            # Use batch uploader
                            utype = 'batch'
                            (myuploadcount, mysumsize, myuptime) = self.batch_upload_scan(tpro, tsub, tses, sid, sobj)
                        uploadcount += 1

                        if mysumsize is not None:
                            upsize += int(mysumsize)

                        if myuploadcount is not None:
                            uploadedfilecount += myuploadcount

                        if self.reportcount is not None and uploadedfilecount-prevmarker > self.reportcount:
                            self.logger.info(
                                '%s upload progress: %d scans (%s files [%s] @ %sps)' %
                                (utype.capitalize(), uploadcount, uploadedfilecount, self.bytes_format(upsize),
                                 self.bytes_format((upsize/(datetime.datetime.now() - starttime).total_seconds()))))
                            prevmarker = uploadedfilecount

        totaluptime = ((datetime.datetime.now() - starttime).total_seconds())

        # Tell server to pull headers from uploaded sessions
        self.server_pull_headers()

        dcmruntime = (datetime.datetime.now() - starttime).total_seconds()
        if upsize == 0 or totaluptime == 0:
            ebw = 0
        else:
            ebw = upsize / totaluptime
        self.logger.info('Dicom %s Upload complete. %d files uploaded over %ss (%s @ %s/s)' % (
            utype, uploadedfilecount, round(dcmruntime), self.bytes_format(upsize),  self.bytes_format(ebw)))

        # Push non dicom
        if self.uploadnondicom:
            ndstarttime = datetime.datetime.now()
            self.logger.info('Beginning nondicom upload to %s level resource %s' % (self.nondicomlevel,
                                                                                    self.uploadnondicom))

            (ndfiles, ndsize, myuptime) = self.batch_upload_nondicom()
            totaluptime += myuptime
            ndruntime = (datetime.datetime.now() - ndstarttime).total_seconds()

            if ndsize == 0 or myuptime == 0:
                ebw = 0
            else:
                ebw = ndsize / myuptime
            self.logger.info('Nondicom upload complete. %d files uploaded over %s (%s @ %sps)' % (
                ndfiles, ndruntime, self.bytes_format(ndsize), self.bytes_format(ebw)))

        runtime = (datetime.datetime.now() - starttime).total_seconds()

        if self.benchmark:
            # Output metrics
            dir_md5 = dirhash(self.target, "sha1")
            print('Date,Host,SHA1,Type,Dicom Files, Other Files, Projects, Subjects, Sessions, Scans, '
                  'Total Uploaded Files, Uploaded Size(KB), Runtime(s), Rate(KBps), Comments')
            print('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %
                  (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.host, dir_md5, utype,
                   uploadedfilecount, ndfiles, self.mapcounts['projects'], self.mapcounts['subjects'],
                   self.mapcounts['sessions'], self.mapcounts['scans'], (uploadedfilecount + ndfiles),
                   round(upsize/1024), round(runtime), round(ebw/1024), self.note))
        return True

    def analyze_dir(self, directory):
        # Analyze directory tree to find map of uploadable files
        anasize = 0
        self.logger.debug('Analyzing from basepath %s' % self.target)
        if os.path.exists(directory):
            for d, r, f in os.walk(directory):
                # Cycle through directories
                for subdir in r:
                    if subdir.startswith(".") is not True:
                        self.dircount += 1
                        if self.reportcount and self.dircount % 100 == 0:
                            self.logger.info('Directories scan progress: %d' % self.dircount)

                for subfile in f:
                    self.logger.debug('Analyzing %s' % os.path.relpath(os.path.join(d, subfile), self.target))
                    self.filecount += 1
                    anasize += os.path.getsize(os.path.join(d, subfile))
                    if self.reportcount is not None and self.filecount % self.reportcount == 0:
                        self.logger.info('Files scan progress: %d (%s)' % (self.filecount, self.bytes_format(anasize)))

                    if subfile.startswith('.'):
                        self.logger.debug('Hidden file %s skipped' % subfile)
                    else:
                        mysubdir = os.path.basename(os.path.normpath(d))
                        mypath = os.path.join(d, subfile)
                        mime_type = magic.from_file(mypath, mime=True)
                        if mime_type == 'application/dicom':
                            # Pull tags, if none skip file, logging in function
                            di = self.pull_dicom_tags(mypath)
                            if di is None:
                                continue

                            self.dfilecount += 1
                            self.create_sessionmap(di)
                        else:
                            ndf = os.path.join(d, subfile)
                            self.logger.debug("File %s non-dicom or archive: %s" %
                                              (os.path.relpath(ndf[0]), str(mime_type)))

                            self.sessionmap['nondicom'].append({'path': ndf})

                            if os.path.isfile(subfile):
                                print(mysubdir)

        else:
            self.logger.error('Directory %s does not exist' % (os.path.abspath(directory)))
            exit(1)

        self.logger.info('Found Total: Files: %d Directories: %d, Dicom Files: %d, Size: %s' %
                         (self.filecount, self.dircount, self.dfilecount, self.bytes_format(float(anasize))))
        self.logger.info('Map contains: Project: %d Subjects: %d Sessions: %d Scans: %d' %
                         (self.mapcounts['projects'],
                          self.mapcounts['subjects'],
                          self.mapcounts['sessions'],
                          self.mapcounts['scans']))

        return True

    def create_sessionmap(self, di):
        # Cycle through files to create session map, looking for mismatched label/ids for sessions and scans
        # Sessionmap will later be used for grouping files for batch uploading

        # Project processing
        if di['project'] not in self.sessionmap['projects']:

            self.sessionmap['projects'][di['project']] = {'subjects': dict()}
            self.mapcounts['projects'] += 1

        # Subject processing
        if di['subjectlabel'] not in self.sessionmap['projects'][di['project']]['subjects']:
            # Add subject to map
            self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']] = {'label': di['subjectlabel'],
                                                                                          'sessions': dict()}
            self.mapcounts['subjects'] += 1

        # Session processing
        if di['sessionlabel'] not in \
                self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]['sessions']:
            # Create new label mapping
            self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]['sessions'][di['sessionlabel']]\
                = {'label': di['sessionlabel'],
                   'uid': di['sessionuid'],
                   'scans': dict()}
            self.mapcounts['sessions'] += 1
        else:
            # Label exists in map
            # Check that label and id match
            if di['sessionuid'] != self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]\
                    ['sessions'][di['sessionlabel']]['uid']:
                # Uid mismatch
                result = []
                found = False

                # Look for matching uids in session map
                for key in self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]['sessions']:
                    # If label has same starting, add to list to append on
                    if key.startswith(di['sessionlabel']):
                        result.append(key)
                    # Matching uid, use that label
                    if di['sessionuid'] == self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]\
                            ['sessions'][key]['uid']:
                        di['sessionlabel'] = key
                        found = True

                # If nothing is found that matches, increment on most recent label
                if not found:
                    di['sessionlabel'] = self.generate_dup_label(natsort.natsorted(result)[-1])

                # Create new mapping with new data
                self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]['sessions']\
                    [di['sessionlabel']] = {'label': di['sessionlabel'],
                                            'uid': di['sessionuid'],
                                            'scans': dict()}
                self.mapcounts['sessions'] += 1
            else:
                # If it does match then existing session mapping is fine, move onto scan mapping
                pass

        # Scan processing
        if di['scanlabel'] not in self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]\
                ['sessions'][di['sessionlabel']]['scans']:
            # Create new scan mapping
            self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]['sessions'][di['sessionlabel']]\
                ['scans'][di['scanlabel']] = {'label': di['scanlabel'],
                                              'uid': di['scanuid'],
                                              'files': list()}
            self.mapcounts['scans'] += 1
        else:
            # Label exists in map
            # Check that label and id match
            if di['scanuid'] != self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]\
                    ['sessions'][di['sessionlabel']]['scans'][di['scanlabel']]['uid']:
                # Uid mismatch
                result = []
                found = False

                # Look for matching uids in scan map
                for key in self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]['sessions']\
                        [di['sessionlabel']]['scans']:
                    # If label has same starting, add to list to append on
                    if key.startswith(di['scanlabel']):
                        result.append(key)
                    # Matching uid, use that label
                    if di['scanuid'] == self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]\
                            ['sessions'][di['sessionlabel']]['scans'][key]['uid']:
                        di['scanlabel'] = key
                        found = True

                # If nothing is found that matches, increment on most recent label
                if not found:
                    di['scanlabel'] = self.generate_dup_label(natsort.natsorted(result)[-1])

                # Create new mapping with new data
                self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]['sessions']\
                    [di['sessionlabel']]['scans'][di['scanlabel']] = {'label': di['scanlabel'],
                                                                      'uid': di['scanuid'],
                                                                      'files': list()}
                self.mapcounts['scans'] += 1
            else:
                # If it does match then existing scan mapping is fine
                pass

        # Add scan to map for upload
        self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]['sessions'][di['sessionlabel']]\
            ['scans'][di['scanlabel']]['files'].append(di)

        return True

    def batch_upload_scan(self, project, subject, session, scan, scanlist):
        # Upload generic data files individually
        sumsize = 0
        for thisscan in scanlist['files']:
            sumsize += os.path.getsize(thisscan['path'])

        if sumsize == 0:
            self.logger.error('[%s/%s/%s/%s] : no files in %s suitable for transfer. Skipping' %
                              (project, subject, session, scan, self.target))
            return 0, 0, 0

        self.logger.debug('[%s/%s/%s/%s] : Batch uploading %d files @ %s' %
                          (project, subject, session, scan, len(scanlist), self.bytes_format(sumsize)))

        # Double check dependencies are in place
        if not self.check_upload_dependencies(scanlist['files'][0]):
            return 0, 0, 0

        # Set benchmark stats

        upstat = {'success': 0, 'total': 0}

        self.logger.debug("Creating zip of [%s/%s/%s/%s] (%d files)" % (project, subject, session, scan,
                                                                        len(scanlist['files'])))

        mytmp = self.create_tmpzip(scanlist['files'])
        mysize = os.path.getsize(mytmp)
        filecount = len(scanlist['files'])

        self.logger.debug("Zip %s created @ %s" % (mytmp, self.bytes_format(os.path.getsize(mytmp))))

        bwstarttime = datetime.datetime.now()
        # Check if http session needs to be renewed prior to proceeding
        self.renew_httpsession()
        myurl = (self.host + "/data/projects/%s/subjects/%s/experiments/%s/scans/%s/resources/DICOM/files/%s"
                 "?format=json&event_reason=upload&update-stats=false&extract=true" %
                 (project, subject, session, scan, os.path.basename(mytmp)))

        mydata = {'zipupload': (os.path.basename(mytmp), open(mytmp, 'rb'), 'multipart/form-data')}

        try:
            response = self.httpsess.post(url=myurl, files=mydata, timeout=(30, self.timeout))
        except requests.exceptions.ReadTimeout or requests.exceptions.ConnectionError as e:
            self.logger.error("[%s/%s/%s/%s] Failed to batch upload %s due to connection error %s" %
                              (project, subject, session, scan, os.path.relpath(mytmp, self.target), str(e)))
            os.remove(mytmp)
            return 0, 0, 0

        upstat['total'] += len(scanlist)
        transtime = (datetime.datetime.now() - bwstarttime).total_seconds()

        if response.status_code == 200:
            upstat['success'] += len(scanlist['files'])
            dups = 0
            try:
                mytxt = json.loads(response.text)
                if 'duplicates' in mytxt:
                    dups = len(mytxt['duplicates'])
            except Exception:
                pass

            self.logger.debug('[%s/%s/%s/%s] Transferred %d/%d files /w %d duplicates in %ds (%sps)' %
                              (project, subject, session, scan, upstat['success'], upstat['total'], dups,
                               transtime, self.bytes_format(mysize/transtime)))
        else:
            os.remove(mytmp)
            self.logger.error("[%s/%s/%s/%s] Failed to batch upload %s (runtime %ds) Server response: %s/%s" %
                              (project, subject, session, scan, os.path.relpath(mytmp, self.target), transtime,
                               response.status_code, response.reason))
            return 0, 0, 0

        os.remove(mytmp)
        return upstat['success'], sumsize, transtime

    def grad_upload_scan(self, project, subject, session, scan, scanlist):
        # Upload generic data files individually
        sumsize = 0
        dups = 0

        for thisscan in scanlist['files']:
            sumsize += os.path.getsize(thisscan['path'])

        if sumsize == 0:
            self.logger.error('[%s/%s/%s/%s] : no files in %s suitable for transfer. Skipping' %
                              (project, subject, session, scan, self.target))
            return 0, 0, 0

        self.logger.debug('[%s/%s/%s/%s] : Gradually uploading %d files @ %s' %
                          (project, subject, session, scan, len(scanlist), self.bytes_format(sumsize)))

        # Double check dependencies are in place
        if not self.check_upload_dependencies(scanlist['files'][0]):
            return 0, 0, 0

        # Set benchmark stats
        bwstarttime = datetime.datetime.now()
        upstat = {'success': 0, 'total': 0}

        # Check if http session needs to be renewed prior to proceeding
        self.renew_httpsession()
        for thisfile in scanlist['files']:
            myurl = (self.host + "/data/services/import?import-handler=gradual-DICOM&PROJECT_ID=%s&SUBJECT_ID=%s&"
                     "EXPT_LABEL=%s&format=json&event_reason=upload&update-stats=false" % (project,
                                                                                           thisfile['subjectlabel'],
                                                                                           thisfile['sessionlabel']))

            mydata = {'file': (os.path.basename(thisfile['path']), open(thisfile['path'], 'rb'), 'multipart/form-data')}

            try:
                response = self.httpsess.post(url=myurl, files=mydata, timeout=(30, self.timeout))
            except requests.exceptions.ReadTimeout or requests.exceptions.ConnectionError as e:
                self.logger.error("[%s/%s/%s/%s] Failed to grad upload %s due to connection error: %s" %
                                  (project, thisfile['subjectlabel'], thisfile['sessionlabel'], thisfile['scanlabel'],
                                   os.path.relpath(thisfile['path'], self.target), str(e)))

            if response.status_code == 200:
                upstat['success'] += 1
                dups = 0
                try:
                    mytxt = json.loads(response.text)
                    if 'duplicates' in mytxt:
                        dups = len(mytxt['duplicates'])
                except Exception:
                    pass
            else:
                transtime = (datetime.datetime.now() - bwstarttime).total_seconds()

                self.logger.error("[%s/%s/%s/%s] Failed to upload %s (runtime %ds) Server response: %s/%s" %
                                  (project, subject, session, scan, os.path.relpath(thisfile['path'], self.target),
                                   transtime, response.status_code, response.reason))

            upstat['total'] += 1

        transtime = (datetime.datetime.now() - bwstarttime).total_seconds()
        self.logger.debug('[%s/%s/%s/%s] Transferred %d/%d files /w %d duplicates over runtime %ds (%s @ %sps)' %
                          (project, subject, session, scan, upstat['success'], upstat['total'], dups, transtime,
                           self.bytes_format(sumsize), self.bytes_format(sumsize/transtime)))

        return upstat['success'], sumsize, transtime

    def batch_upload_nondicom(self):
        sumfiles = len(self.sessionmap['nondicom'])
        sumsize = 0

        if sumfiles == 0:
            self.logger.error('Non nondicom files found to upload, skipping')
            return 0, 0, 0

        for tndf in self.sessionmap['nondicom']:
            sumsize += os.path.getsize(tndf['path'])

        self.logger.debug('[%s/%s] : Batch uploading %d files @ %s' % (self.nondicomlevel,
                                                                       self.uploadnondicom,
                                                                       len(self.sessionmap['nondicom']),
                                                                       self.bytes_format(sumsize)))

        mytmp = self.create_tmpzip(self.sessionmap['nondicom'], includepath=True)

        # Check if http session needs to be renewed prior to proceeding
        self.renew_httpsession()

        # Determine resource level
        myurl = self.host
        if self.nondicomlevel == 'project':
            myurl = (self.host + "/data/projects/%s/" % self.project)
        elif self.nondicomlevel == 'subject':
            myurl = (self.host + "/data/projects/%s/subjects/%s" % (self.project, self.subject))
        elif self.nondicomlevel == 'session':
            myurl = (self.host + "/data/projects/%s/subjects/%s/experiments/%s" % (self.project, self.subject,
                                                                                   self.sessionlabel))

        myurl += ("resources/%s/files/%s?format=json&event_reason=upload&update-stats=false&extract=true" %
                  (self.uploadnondicom, os.path.basename(mytmp)))
        mydata = {'zipupload': (os.path.basename(mytmp), open(mytmp, 'rb'), 'application/zip')}

        upstart = datetime.datetime.now()

        try:
            response = self.httpsess.post(url=myurl, files=mydata, timeout=(30, self.timeout))
        except requests.exceptions.ReadTimeout or requests.exceptions.ConnectionError:
            self.logger.error("[%s/%s] Failed to upload %s due to timeout, increase default from %d" %
                              (self.nondicomlevel, self.uploadnondicom, mytmp, self.timeout))
            os.remove(mytmp)
            return 0, 0, 0

        if response.status_code != 200:
            self.logger.error("[%s/%s] Failed to upload %s, server response: %s/%s" %
                              (self.nondicomlevel, self.uploadnondicom, mytmp, response.status_code, response.reason))
            return 0, 0, 0

        os.remove(mytmp)
        uptime = (upstart - datetime.datetime.now()).total_seconds()

        return sumfiles, sumsize, uptime

    def create_tmpzip(self, filelist, includepath=False):
        # Create a tmp zipfile from list of scans
        # Zip raw files to take advantage of zip handler
        if len(filelist) > 0:
            # Gather source data information for later validation of upload
            zippath = self.tmpdir + '/' + uuid.uuid4().hex + '.zip'

            with zipfile.ZipFile(zippath, 'w') as zipMe:
                for tf in filelist:
                    if includepath:
                        storedpath = os.path.relpath(tf['path'], self.target)
                    else:
                        storedpath = self.strip_invalid(os.path.basename(tf['path']))

                    zipMe.write(tf['path'], storedpath, compress_type=zipfile.ZIP_DEFLATED)

            return zippath

    def check_upload_dependencies(self, di):
        # Check file upload dependencies
        # Check project existence, if not skip
        if not self.check_project(project=di['project']):
            self.logger.error('Project %s access denied, for file %s, skipping' %
                              (di['project'], os.path.relpath(di['path'], self.target)))
            return False

        # # Check subject existence
        if not self.check_subject(di=di, create=True):
            self.logger.error('Subject %s does not exist or cannot be created on %s/%s for file %s, skipping' %
                              (di['subjectlabel'], self.host, di['project'], os.path.relpath(di['path'], self.target)))
            return False

        # # Check for session/scan duplicates
        di = self.check_session(di)
        if not di:
            return False
        di = self.check_scan(di)
        if not di:
            return False

        return di

    def check_project(self, project=None, create=True):
        project = self.strip_invalid(project)
        if not project:
            project = self.strip_invalid(self.project)
        # Checks project existence on server
        if project in self.checked_values['projects']:
            return True
        try:
            response = self.httpsess.get(self.host + '/data/archive/projects/%s?accessible=true' % project)

            if response.status_code == 200:
                # initialized checked lists to assure uniqueness
                self.checked_values['projects'][project] = {'subjects': {}}
                return True
            else:
                raise Exception('Recieved %s code' % response.status_code)
        except Exception as e:
            if str(e) == 'Recieved 404 code':
                self.logger.error('Project not found: %s', project)
            else:
                self.logger.error('Unknown error: %s', str(e))

        if create is True:
            # create new subject
            # curl - u $CRED - X PUT "$HOST/REST/projects/$PROJECT/subjects/$SUBJECT?event_reason=test&
            # req_format=form&gender=$GENDERTEXT&dob=02/14/$YEAR" - d xnat:subjectData / group = group$GROUP
            response = self.httpsess.put('%s/data/projects/%s?event_reason=ScriptedUpload&'
                                         'event_action=Added_nonexistant_project' %
                                         (self.host, project))
            if response.status_code == 200 or response.status_code == 201:
                self.checked_values['projects'][project] = {'subjects': {}}
                self.logger.info('Created new project %s' % project)

                return True
            else:
                self.logger.debug('Unable to create project %s: Response code %s' % (project,
                                                                                     response.status_code))
        return False

    def check_subject(self, di=None, create=True):
        # Checks subject existence on server, create if requested
        if di['subjectlabel'] is None:
            if di['subject'] is not None:
                di['subjectlabel'] = self.subject
            else:
                self.logger.error('Subject is not set, required for this upload.')
                return False

        if di['project'] in self.checked_values['projects'] and \
                'subjects' not in self.checked_values['projects'][di['project']]:
            self.checked_values['projects'][di['project']]['subjects'] = {}

        if di['subjectlabel'] in self.checked_values['projects'][di['project']]['subjects']:
            return True

        try:
            response = self.httpsess.get(self.host + '/data/projects/%s/subjects/%s?format=json' %
                                         (di['project'], di['subjectlabel']))
            if response.status_code == 200:
                # Add subject to cache
                if di['subjectlabel'] not in self.checked_values['projects'][di['project']]['subjects']:
                    self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']] = \
                        {"sessionlabels": {}, "sessionuids": {}}
                return True
        except Exception as e:
            self.logger.error('Error checking subject existence %s', str(e))

        if create is True:
            # create new subject
            self.create_subject(di)

            return True

        return False

    def check_session(self, di):
        # Checks session existence for project/subject, creates with proper fields if necessary

        # Create cache of sessionuid:{sessionlabel,exists} mapping
        # https://rair.avidrp.com/data/experiments?format=html&xsiType=xnat:imageSessionData
        # &UID=1.3.12.2.1107.5.2.32.35248.30000012031314395204600

        # Session data is not on di, fail
        if di['sessionuid'] is None or di['sessionlabel'] is None:
            self.logger.error('Session uid or label is not set, cannot be checked, required for this upload')
            return False

        # If uid in cache, use existing label
        if di['sessionuid'] in self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']]\
                ['sessionuids']:
            di['sessionlabel'] = self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']]\
                ['sessionuids'][di['sessionuid']]['sessionlabel']
            return di

        # Check for uid on server by label, if has proper uid combo add to cache and proceed
        mysessionlabels = self.get_session_by_uid(di)
        if mysessionlabels is not None:
            for thisresult in mysessionlabels:
                if di['sessionlabel'] == self.strip_invalid(thisresult['label']):
                    # Add to cache
                    self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']]['sessionuids']\
                        [thisresult['UID']] = {'sessionlabel': di['sessionlabel'], 'scanuids': [], 'scanlabels': []}
                    self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']]['sessionlabels']\
                        [thisresult['label']] = {'sessionuid': di['sessionuid'], 'scanuids': [], 'scanlabels': []}
                    return di

        # Create session, return None of fail
        if not self.create_session(di):
            return None

        # Return created object
        return di

    def check_scan(self, di):
        # if (scan label is NEW)
        #     -- new
        #     scan
        # else
        #     if (series UID is NEW)
        #         -- new scan - iterate
        #         scan label to be unique
        #     else
        #         -- existing scan - append to

        # Check if scan exists, create if requested
        if di['scanlabel'] is None or di['scanuid'] is None:
            self.logger.error('Scan label or uid is not set, cannot be checked, required for this upload.')
            return None

        # If uid in cache, use existing label
        if di['scanuid'] in self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']]\
                ['sessionuids'][di['sessionuid']]['scanuids']:
            di['scanlabel'] = self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']]\
                ['sessionuids'][di['sessionuid']]['scanuids'][di['scanuid']]['scanlabel']
            return di

        # Create scan, return None of fail
        if not self.create_scan(di):
            return None

        return di

    def get_session_by_uid(self, di):
        # Pulls list of sessions from host based on uid, returns list of sessions

        response = self.httpsess.get(
            self.host + '/data/experiments?format=json&columns=project,subject_label,label,UID&'
                        'xsiType=xnat:imageSessionData&project=%s&UID=%s' %
            (di['project'], di['sessionuid']))

        if response.status_code == 200:
            if int(response.json()['ResultSet']['totalRecords']) == 0:
                return None
            else:
                return response.json()['ResultSet']['Result']
        elif response.status_code == 404:
            return None
        else:
            # Error on request
            self.logger.error('Unable to pull session by uid: response %s' % response.status_code)
        return None

    def get_session_by_label(self, di):
        # Pulls list of sessions from host based on label, returns list of sessions
        response = self.httpsess.get(
            self.host + '/data/experiments?format=json&columns=project,subject_label,label,UID&'
                        'xsiType=xnat:imageSessionData&project=%s&label=%s' %
            (di['project'], di['sessionlabel']))

        if response.status_code == 200:
            if int(response.json()['ResultSet']['totalRecords']) == 0:
                return None
            else:
                return response.json()['ResultSet']['Result']
        elif response.status_code == 404:
            return None
        else:
            # Error on request
            self.logger.error('Unable to pull session %s by label: response %s' % (di['sessionlabel'],
                                                                                   response.status_code))
        return None

    def get_scan_by_uid(self, di):
        # Pulls list of scans from host based on uid, returns list of sessions

        response = self.httpsess.get(
            self.host + '/data/archive/projects/%s/subjects/%s/experiments/%s/scans/?format=json&UID=%s' %
            (di['project'], di['subjectlabel'], di['sessionlabel'], di['scanuid']))

        if response.status_code == 200:
            if int(response.json()['ResultSet']['totalRecords']) == 0:
                return None
            else:
                return response.json()['ResultSet']['Result']
        elif response.status_code == 404:
            return None
        else:
            # Error on request
            self.logger.error('Unable to pull scan %s by uid: response %s' % (di['scanlabel'], response.status_code))
        return None

    def get_scan_by_label(self, di):
        # Pulls list of scans from host based on label, returns list of scan
        response = self.httpsess.get(
            self.host + '/data/archive/projects/%s/subjects/%s/experiments/%s/scans/%s?format=json' %
            (di['project'], di['subjectlabel'], di['sessionlabel'], di['scanlabel']))

        if response.status_code == 200:
            if len(response.json()['items']) == 0:
                return None
            else:
                return response.json()['items']
        elif response.status_code == 404:
            return None
        else:
            # Error on request
            self.logger.error('Unable to pull scan %s by uid: response %s' % (di['scanlabel'], response.status_code))
        return None

    def generate_dup_label(self, label):
        labelnum = re.findall(r'_(\d+)$', label)
        if len(labelnum) > 0:
            # Increment existing dup count
            newlabel = re.sub(r'_' + labelnum[0] + '$', '_' + str(int(labelnum[0]) + 1), label)
            return newlabel
        else:
            # Add _1 since no previous dup count
            return label + '_1'

    def create_subject(self, di):
        self.renew_httpsession()

        # Create new subject
        response = self.httpsess.put(self.host + '/data/projects/%s/subjects/%s?format=json' %
                                     (di['project'], di['subjectlabel']))
        if response.status_code == 201 or response.status_code == 200:
            self.logger.debug('Created new subject %s' % di['subjectlabel'])
            # Add subject to cache
            self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']] = \
                {"sessionlabels": {}, "sessionuids": {}}
            return True
        elif response.status_code == 403:
            self.logger.error('Unable to create subject %s on project %s, insufficent permissions, exiting: %s\n' %
                              (di['subjectlabel'], di['project'], response.text))
            exit(1)
        else:
            self.logger.error('Unable to create subject %s: %s' % (di['subjectlabel'], response.text))
            return False

    def create_session(self, di):
        self.renew_httpsession()

        # If delete session is true, delete prior to create
        if self.deletesessions is True:
            self.delete_session(di)

        mymodality = self.get_session_modality(di['project'], di['subjectlabel'], di['sessionlabel'])

        params = {
            'xsiType': ('xnat:%s' % mymodality + 'SessionData'),
            'UID': di['sessionuid'],
            'label': di['sessionuid'],
            'modality': mymodality.upper()
        }

        if di['sessiondate'] is not None:
            params['date'] = str(di['sessiondate'])

        if di['sessiondesc'] is not None:
            params['note'] = str(di['sessiondesc'])

        # Creates new session on host for project/subject
        response = self.httpsess.post(self.host + '/data/archive/projects/%s/subjects/%s/experiments/'
                                                  '?activate=true&label=%s&event_reason=upload' %
                                      (di['project'], di['subjectlabel'], di['sessionlabel']), params=params)

        if response.status_code == 200:
            self.logger.debug('Session %s created with uid %s as %s' % (di['sessionlabel'],
                                                                        di['sessionuid'],
                                                                        di['modality']))
            # Add to cache
            self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']]['sessionuids']\
                [di['sessionuid']] = di['sessionlabel']
            self.newsessions += 1
        elif response.status_code == 403:
            self.logger.error('Unable to create session %s on project %s, insufficent permissions, exiting: %s\n' %
                              (di['subjectlabel'], di['project'], response.text))
            exit(1)
        else:
            self.logger.debug('Unable to create session %s with uid %s on project %s as %s' %
                              (di['sessionlabel'], di['sessionuid'], di['project'], di['modality']))
            return False

        self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']]['sessionuids']\
            [di['sessionuid']] = {'sessionlabel': di['sessionlabel'], 'scanuids': [], 'scanlabels': []}
        self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']]['sessionlabels']\
            [di['sessionlabel']] = {'sessionuid': di['sessionuid'], 'scanuids': [], 'scanlabels': []}
        return True

    def delete_session(self, di):
        # Delete session by uid

        response = self.httpsess.delete(self.host + "/data/projects/%s/subjects/%s/experiments/%s"
                                        "?removeFiles=true&event_action=ScriptedDeletion" % (
                                             di['project'],
                                             di['subjectlabel'],
                                             di['sessionlabel']
                                         ))

        if response.status_code == 404:
            return True
        elif response.status_code == 200:
            if self.verbose:
                self.logger.debug('Deleted existing project %s session %s/%s' % (di['project'], di['sessionlabel'],
                                                                                 di['sessionuid']))
                return True

        else:
            self.logger.error('Unable to delete existing project %s session %s/%s: %s' % (di['project'],
                                                                                          di['sessionlabel'],
                                                                                          di['sessionuid'],
                                                                                          response.reason))
            return False

        return False

    def create_scan(self, di):
        # Creates new session on host for project/subject
        self.renew_httpsession()

        params = {
            'xsiType': ('xnat:%sScanData' % di['modality']),
            'UID': di['scanuid'],
            ('xnat:%sScanData/type' % di['modality']): str(di['scandesc']),
            ('xnat:%sScanData/series_description' % di['modality']): str(di['scandesc']),
            'xnat:imageScanData/modality': di['modality'].upper()
        }

        response = self.httpsess.put(self.host + '/data/archive/projects/%s/subjects/%s/experiments/%s/scans/%s'
                                     '?event_reason=upload' %
                                     (di['project'], di['subjectlabel'], di['sessionlabel'], di['scanlabel']),
                                     params=params)

        if response.status_code == 200:
            self.logger.debug('Scan %s created with uid %s as %s' % (di['scanlabel'], di['sessionuid'], di['modality']))
            # Add to cache
            self.newscans += 1
        else:
            self.logger.error('Unable to create session %s with uid %s on project %s' %
                              (di['sessionlabel'], di['sessionuid'], di['project']))
            return False

        self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']]['sessionlabels']\
            [di['sessionlabel']]['scanlabels'].append(di['scanlabel'])
        self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']]['sessionlabels']\
            [di['sessionlabel']]['scanuids'].append([di['scanuid']])

        return True

    def iterate_dup(self, project, duptype, value):
        newname = value
        num = 0

        while newname in self.checked_values[project][duptype]:
            newname = "%s_%s" % (value, num)
            num += 1

        return value

    def bytes_format(self, number_of_bytes):
        # Formats byte to human readable text
        if number_of_bytes is None:
            number_of_bytes = 0

        if number_of_bytes < 0:
            raise ValueError("number_of_bytes can't be smaller than 0 !!!")

        step_to_greater_unit = 1024.

        number_of_bytes = float(number_of_bytes)
        unit = 'bytes'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'KB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'MB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'GB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'TB'

        precision = 1
        number_of_bytes = round(number_of_bytes, precision)

        return str(number_of_bytes) + ' ' + unit

    def pull_dicom_tags(self, path):
        td = pydicom.read_file(path)

        myproject = None
        mysubject = None

        try:
            if not (self.splitlabel is not None and td[self.splitlabel]) and not td[self.subjectlabel].value:
                self.logger.error('Subject Label @ %s empty for %s, skipping' % (self.subjectlabel, path))
                return None
            elif not td[self.sessionlabel].value:
                self.logger.error('Session Label @ %s empty for %s, skipping' % (self.sessionlabel, path))
                return None
            elif not td[self.scanlabel].value:
                self.logger.error('Scan Label @ %s empty for %s, skipping' % (self.scanlabel, path))
                return None
            elif not td[self.scanuid].value:
                self.logger.error('Scan UID @ %s empty for %s, skipping' % (self.scanuid, path))
                return None
            elif not td[self.sessionuid].value:
                self.logger.error('Session UID @ %s empty for %s, skipping' % (self.sessionuid, path))
                return None
        except TypeError as e:
            self.logger.error('File %s dicom read error, missing key, skipping: %s' % (path, e))
            return None
        except LookupError as e:
            self.logger.error('File %s dicom read error, invalid encoding, skipping: %s' % (path, e))
            return None

        if self.splitlabel:
            try:
                if td[self.splitlabel].value:
                    mysplabel = str(td[self.splitlabel].value)
                    if "_" in mysplabel:
                        # Check for _, split and use combo
                        (myproject, mysubject) = mysplabel.split('_')
                        myproject = self.strip_invalid(myproject)
                    elif ":" in mysplabel:
                        # Check for :, split and use combo
                        (myproject, mysubject) = mysplabel.split(':')
                        myproject = self.strip_invalid(myproject)
                    else:
                        # If just a single string, check if that project exists
                        # If so, then use that project
                        if not self.check_project(mysplabel):
                            myproject = self.project
                            mysubject = mysplabel
                        else:
                            myproject = mysplabel
                            mysubject = mysplabel
                        # If single string, then use that as subject

                    # Check if project exists, if not do defaults
                    if not self.check_project(myproject):
                        myproject = self.project
                        mysubject = self.subject
                else:
                    myproject = self.project
                    mysubject = self.subject
            except Exception as e:
                # Default to defaults on error
                myproject = None
                mysubject = None
                #self.logger.debug('Unable to determine split label: %s' % e)

        if myproject is None and self.projectlabel is not None:
            myproject = td[self.projectlabel].value
            if not myproject:
                self.logger.error('Project label @ %s empty for %s, skipping' % (myproject, path))
                return None

        if myproject is None:
            myproject = self.project

        if mysubject is None and self.subjectlabel is not None:
            try:
                if td[self.subjectlabel].value:
                    mysubject = self.strip_invalid(td[self.subjectlabel].value)
                else:
                    mysubject = None
            except Exception as e:
                mysubject = None

        if mysubject is None:
            mysubject = self.project

        try:
            if td[self.sessiondate].value:
                year = td[self.scandate].value[0:4]
                month = td[self.scandate].value[5:6]
                day = td[self.scandate].value[7:8]
                sessiondate = "%s/%s/%s" % (month, day, year)
            else:
                sessiondate = None
        except Exception as e:
            sessiondate = None

        try:
            if td[self.studydesc].value:
                studydesc = td[self.studydesc].value
            else:
                studydesc = None
        except Exception as e:
            studydesc = None

        try:
            if td[self.seriesdesc].value:
                seriesdesc = td[self.seriesdesc].value
            else:
                seriesdesc = None
        except Exception as e:
            seriesdesc = None

        try:
            if td[self.scandate].value:
                year = td[self.scandate].value[0:4]
                month = td[self.scandate].value[5:6]
                day = td[self.scandate].value[7:8]
                scandate = "%s/%s/%s" % (month, day, year)
            else:
                scandate = None
        except Exception as e:
            scandate = None

        mydi = {
            'subjectlabel': self.strip_invalid(mysubject),
            'sessionlabel': self.strip_invalid(td[self.sessionlabel].value),
            'scanlabel': self.strip_invalid(td[self.scanlabel].value),
            'scanuid': td[self.scanuid].value,
            'sessionuid': td[self.sessionuid].value,
            'modality': self.translate_modality(td[self.modality].value),
            'project': self.strip_invalid(myproject),
            'path': path,
            'sessiondate': sessiondate,
            'scandate': scandate,
            'sessiondesc': studydesc,
            'scandesc': seriesdesc
        }

        if self.splitsample:
            print(json.dumps(mydi))
            exit(0)

        return mydi

    def pull_single_dicom_tag(self):
        try:
            td = pydicom.read_file(self.target)
            mytag = str(td[self.pulltag].value)
            return mytag
        except Exception:
            return None

    def server_pull_headers(self):
        # Trigger final pull of remote headers via api for all sessions
        # 'http://my.xnat.org/REST/projects/MyProject/subjects/ThisSubject/experiments/ThisSession?pullDataFromHeaders=true'
        # Update stats for all sessions to refresh catalog
        # /services/refresh/catalog?resource=/archive/projects/PROJECT/subjects/SUBJECT/experiments/EXPT&options=populateStats
        self.renew_httpsession()

        for thisproject in self.sessionmap['projects']:
            for thissubject in self.sessionmap['projects'][thisproject]['subjects']:
                for thissession in self.sessionmap['projects'][thisproject]['subjects'][thissubject]['sessions']:
                    self.logger.debug(
                        "Pulling headers from session %s [%s %s]" % (thissession, thisproject, thissubject))
                    response = self.httpsess.put(
                        self.host + '/REST/projects/%s/subjects/%s/experiments/%s?pullDataFromHeaders=true&'
                                    'event_reason=upload&allowDataDeletion=true' % (thisproject,
                                                                                    thissubject,
                                                                                    thissession))

                    response = self.httpsess.post(
                        self.host + '/data/services/refresh/catalog?resource=/archive/projects/%s/subjects/%s'
                                    '/experiments/%s&options=populateStats&event_reason=upload' %
                        (thisproject, thissubject, thissession))

        return True

    def strip_invalid(self, mytext):
        mytext = str(mytext).replace(" ", "_")
        return re.sub(r'\W+', '_', mytext)

    def translate_modality(self, modality):
        # Translate modality code from files into xnat mapping
        if modality == 'MR':
            return 'mr'
        elif modality == 'PT':
            return 'pet'
        elif modality == 'CT':
            return 'ct'
        elif modality == 'XA':
            return 'xa'
        elif modality == 'US':
            return 'us'
        elif modality == 'RT':
            return 'rt'
        elif modality == 'CR':
            return 'cr'
        elif modality == 'OPT':
            return 'opt'
        elif modality == 'MG':
            return 'mg'
        elif modality == 'NM':
            return 'nm'
        elif modality == 'SR':
            return 'sr'
        elif modality == 'SC':
            return 'otherDicom'
        else:
            return 'otherDicom'

    def get_session_modality(self, project, subject, session):
        modalities = list()
        # Pulls session modality based on scans contained within
        for thisscan in self.sessionmap['projects'][project]['subjects'][subject]['sessions'][session]['scans'].items():
            modalities.append(thisscan[1]['files'][0]['modality'])

        modalities = list(dict.fromkeys(modalities))

        if len(modalities) > 1 and 'sr' in modalities:
            modalities.remove('sr')

        if len(modalities) == 1:
            return modalities[0]
        elif 'pet' in modalities and 'mr' in modalities:
            return 'petmr'
        elif 'pet' in modalities and 'ct' in modalities:
            return 'pet'

        return modalities[0]

    def sessionmap_dump(self):
        self.logger.info('Dumping file tree map to file %s' % self.dumpmap)
        opts = jsbeautifier.default_options()
        opts.ident_size = 2
        f = open(self.dumpmap, "w")
        f.write(jsbeautifier.beautify(json.dumps(self.sessionmap), opts))
        return True

    def renew_httpsession(self):
        # Set up request session and get cookie
        if self.lastrenew is None or ((self.lastrenew + self.sessiontimeout) < datetime.datetime.now()):
            self.logger.debug('[SESSION] Renewing http session as %s from %s with timeout %d' % (self.username,
                                                                                                 self.host,
                                                                                                 self.timeout))
            # Renew expired session, or set up new session
            self.httpsess = requests.Session()

            # Retry logic
            retry = Retry(connect=5, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            self.httpsess.mount('http://', adapter)
            self.httpsess.mount('https://', adapter)

            # Log in and generate xnat session
            response = self.httpsess.post(self.host + '/data/JSESSION', auth=(self.username, self.password),
                                          timeout=(30, self.timeout))
            if response.status_code != 200:
                self.logger.error("[SESSION] Renewal failed, no session acquired: %d %s" % (response.status_code,
                                                                                            response.reason))
                exit(1)

            self.lastrenew = datetime.datetime.now()
        else:
            # self.logger.debug('[SESSION] Reusing existing https session until %s' % (self.lastrenew +
            #                                                                         self.sessiontimeout))
            return True

        return True

    def close_httpsession(self):
        # Logs out of session for cleanup
        self.httpsess.delete(self.host + '/data/JSESSION', timeout=(30, self.timeout))
        self.logger.debug('[SESSION] Deleting https session')
        self.httpsess.close()
        return True
