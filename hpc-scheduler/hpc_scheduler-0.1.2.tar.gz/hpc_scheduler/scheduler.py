#! /usr/bin/python
# coding: utf-8
"""Scheduler

Classes and methods in :mod:`Scheduler` should create jobscripts
for different schedulers and help submitting and checking them. 

"""

import logging
import os
import subprocess
from configobj import ConfigObj
from string import Template
import datetime
import re
import sys

#logging.basicConfig(level=logging.INFO)

# slurm job template
SLURM_TEMPLATE = \
"""@job_shell
#SBATCH --job-name=@job_name                       # Specify job name
#SBATCH --partition=@partition                     # Specify partition name
#SBATCH --ntasks=@ntasks                           # Specify max. number of tasks to be invoked
#SBATCH --mem-per-cpu=@mem_per_cpu                 # Specify real memory required per CPU in MegaBytes
#SBATCH --time=@time                               # Set a limit on the total run time
#SBATCH --mail-type=@mail_type                     # Notify user by email in case of job failure
#SBATCH --account=@account                         # Charge resources on this project account
#SBATCH --output=@{log_dir}/@{job_name}.o%j        # File name for standard output
#SBATCH --error=@{log_dir}/@{job_name}.o%j         # File name for standard error output
"""

SLURM_COMMENT = \
"""

# job script created by PyRemo Job Scheduler

""" + \
"# "+str(datetime.datetime.now())+"\n"


# define job states
UNKNOWN   = -2
FAILED    = -1
COMPLETED =  0
RUNNING   =  1
PENDING   =  2

LOGLEV = {
  COMPLETED   :logging.getLevelName('INFO'),
  FAILED      :logging.getLevelName('ERROR'),
  UNKNOWN     :logging.getLevelName('WARNING'),
  PENDING     :logging.getLevelName('INFO'),
  RUNNING     :logging.getLevelName('INFO')
}

### SLURM definitions ####
SLURM_STATES   = {'FAILED'   : FAILED,   
                  'COMPLETED': COMPLETED,
                  'RUNNING'  : RUNNING ,
                  'PENDING'  : PENDING  }

SLURM_DEFAULTS = {'job_name'    :'unknown',
                  'partition'   :'',
                  'ntasks'      :'1',\
                  'mem_per_cpu' :'1280',
                  'mail_type'   :'FAIL',
                  'account'     :'',
                  'time'        :'',
                  'log_dir'     :''}

SLURM_CONTROL = ['StdErr','StdOut','WorkDir','JobName','Command'] 

### known Schedulers ####
SCHEDULER     = {'SLURM':{'batch'     :'sbatch --parsable',\
                          'accounting':'sacct --parsable2 --format=jobid,elapsed,ncpus,ntasks,state,end,jobname -j',
                          'control'   :'scontrol show jobid -dd',
                          'tpl'       :SLURM_TEMPLATE, 
                          'states'    :SLURM_STATES,
                          'comment'   :SLURM_COMMENT,
                          'ctr_list'  :SLURM_CONTROL,
                          'defaults'  :SLURM_DEFAULTS} 
                }

# pattern to search for in logfiles
ERROR_PATTERN = ['error','failed','exception', 'not found']


class Job():
    """Class to hold job information 


    Written by Lars Buntemeyer

    Last modified: 06.02.2019
    """

    def __init__(self, sys, jobname='', jobscript=None, jobid=-1, tpl=None,
                 commands='', header_dict={}, delimiter='@', control={}):
        """Determines the appropriate job commands and templates. 
           A job can be created from a template, header dictionary and
           commands to write and submit a job script, or by defining a
           jobid to create a job from an existing scheduler job. 
           Therefor, the job definition is hold quite general and requires
           only the sys argument for creating.

        **Arguments:**
            *sys:*
                The batch scheduler implementation.
            *jobname:*
                The batch scheduler implementation.
                (default: *None*) 
            *jobscript:*
                A filename for the jobscript.
                (default: *None*) 
            *jobid:*
                JobID in the Scheduler.
                (default: -1) 
            *tpl:*
                Template file for creating a jobscript.
                (default: *None*) 
            *commands:*
                Text containing commands for the jobscript.
                (default: '') 
            *header_dict:*
                Dictionary to fill the template header 
                (default: *None*) 

        **Raises:**
            *Exception:*
                If the scheduler implementation is unknown 
        """
        if sys not in SCHEDULER:
          print('Unknown scheduler implementation, must be one of: '+\
                str(SCHEDULER.keys())) 
          raise Exception('Unknown sys: '+sys)
        
        self.batch_command  = SCHEDULER[sys]['batch']
        self.acct_command   = SCHEDULER[sys]['accounting'] 
        self.contr_command  = SCHEDULER[sys]['control'] 
        self.header_dict    = SCHEDULER[sys]['defaults']
        self.comment        = SCHEDULER[sys]['comment']
        self.ctr_list       = SCHEDULER[sys]['ctr_list']
        self.jobname       = jobname
        self.jobscript     = jobscript
        self.tpl           = tpl 
        self.jobid         = jobid
        self.commands      = commands
        self.delimiter     = delimiter
        self.control       = control
      
         
        if not self.tpl      : self.tpl       = SCHEDULER[sys]['tpl'] 
        if not self.jobscript: self.jobscript = os.path.join(os.getcwd(),
                                                jobname+'.sh') 
        self._init_tpl()
        self.header_dict['job_name']  = self.jobname
        self.header_dict['job_shell'] = '#!/bin/sh'
        if header_dict: self.header_dict.update(header_dict) 

    def __eq__(self, other):
        if self.jobname == other.jobname:
            return True 
        else:
            return False

    def _init_tpl(self):
        class TmpTemplate(Template):
          delimiter = self.delimiter
        if type(self.tpl) is str:
          if os.path.isfile(self.tpl):
            self.tpl = TmpTemplate( open(self.tpl).read() )
          else:
            self.tpl = TmpTemplate( self.tpl )
        elif type(self.tpl) is not type(Template):
          raise Exception('unknown type of job template, must be either '+
                          'Template or text or valid filename')


    def submit(self, write=False):
        if write: self.write_jobscript()
        output = subprocess.Popen(self.batch_command.split()+[self.jobscript], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
        stdout,stderr = output.communicate()
        logging.debug('stdout '+str(stdout))
        self.jobid = int(stdout)
        if not stderr:    
          logging.info('submitted jobscript: '+self.jobscript) 
          logging.debug('jobid: '+str(self.jobid))
          self.parse_control()
          for entry in self.control:
            logging.debug('control: '+str(entry)+': '+str(self.control[entry]))
        else:
          logging.error('submitted jobscript: '+self.jobscript) 
          logging.error('stderr'+str(self.stderr)) 
        return self.jobid
             

    def write_jobscript(self, header_dict=None):
        if header_dict: self.header_dict.update(header_dict)
        fills = self.header_dict
        logging.info('writing: '+self.jobscript)
        content = self.tpl.substitute(fills)
        content += self.comment
        content += self.commands
        with open(self.jobscript, "w") as script:
          script.write(content)
        return self.jobscript



    def get_acct(self):
        jobid = self.jobid
        command =  self.acct_command.split(' ')+[str(jobid)]
        output = subprocess.Popen(command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)

        stdout,stderr = output.communicate()
        lines = stdout.splitlines()
        header = lines[0].decode().split('|')
        data   = lines[1].decode().split('|')
        acct = {}
        for title,entry in zip(header,data):
          acct[title] = entry
        logging.debug(str(jobid)+': '+str(acct))
        return acct 
   
 

    def parse_control(self):
        jobid = self.jobid
        command =  self.contr_command.split(' ')+[str(jobid)]
        output = subprocess.Popen(command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
        stdout,stderr = output.communicate()
        logging.debug(stdout,stderr)
        lines = stdout.splitlines()
        control = {}
        for line in lines:
          slines = line.split()
          for sline in slines:
            data = sline.split(b'=')
            if len(data)==2:
             control[data[0]] = data[1]
        self.control = control
        return control



    def get_log(self):
        # basic info 
        job_log = {'jobid'    : self.jobid, \
                   'jobscript': self.jobscript}
        # add some info from control command
        for ctr in self.control:
          if ctr in self.ctr_list: job_log[ctr] = self.control[ctr]
        return job_log



    def grep_log_err(self):
        error = []
        errlog = self.control['StdErr'] if 'StdErr' in self.control else None
        if errlog and os.path.isfile(errlog):
            with open(errlog) as origin_file:
              for line in origin_file:
                for pattern in ERROR_PATTERN:
                  if re.search(pattern, line, re.IGNORECASE):
                    error.append(line.rstrip())
                    break
        return error



class Scheduler():
    """Class to interact with an HPC job scheduler 


    Written by Lars Buntemeyer

    Last modified: 06.02.2019
    """

    def __init__(self, sys, name='', tpl=None, logfile='', \
                 job_list = [], header_dict={}):
        """Determines the appropriate scheduler commands and templates.

        **Arguments:**
            *sys:*
                The batch scheduler implementation
            *tpl:*
                Template file for the scheduler
                (default: *None*) 
            *logfile*
                A file in ini style holding jobid information
                (default: *None*) 
            *jobids*
                A dictionary holding {jobname:jobid} 
                (default: *None*) 
            *header_dict*
                A default header dictionary for a new job
                (default: *None*) 
            *job_list*
                A list of type Job 
                (default: *None*) 

        **Raises:**
            *Exception:*
                If the scheduler implementation is unknown 
        """

        self.STAT_STR = '{:<48} | {:>8} | {:<16} | {:<24} | {:<24}'

        if sys not in SCHEDULER:
          print('Unknown scheduler implementation, must be one of: '+\
                str(SCHEDULER.keys())) 
          raise Exception('Unknown sys: '+sys)
        self.STAT = SCHEDULER[sys]['states'] 
        self.sys      = sys
        self.name     = name
        self.logfile  = logfile
        self.job_list = job_list
        self.job_log   = ConfigObj(self.logfile)
        self.batch    = SCHEDULER[sys]['batch'] 
        self.acct     = SCHEDULER[sys]['accounting'] 
        self.tpl      = SCHEDULER[sys]['tpl']
        self.header_dict = header_dict
        if tpl         : self.tpl = tpl
        if self.logfile: self._read_job_log()

    
    def _init_job_list(self):
        """Initiate the job list from scheduler log file

        Written by Lars Buntemeyer

        Last changes 06.02.2019
        """
        self.job_list = []
        for jobname in self.job_log:
           jobid     = self.job_log[jobname]['jobid']
           jobscript = self.job_log[jobname]['jobscript']
           self.job_list.append(Job(self.sys,jobname=jobname,\
                            jobid=jobid,jobscript=jobscript, \
                            control=self.job_log[jobname]))


    def _read_job_log(self):
        """Reads jobnames and ids from an ini-file.

        Written by Lars Buntemeyer

        Last changes 06.02.2019
        """
        logging.debug('reading jobids: '+str(self.logfile))
        self.job_log = ConfigObj(self.logfile)
        self._init_job_list()


    def _write_job_log(self):
        """Writes jobnames and ids to an ini-file.

        Written by Lars Buntemeyer

        Last changes 06.02.2019
        """
        logging.debug('writing jobids to '+str(self.job_log.filename))
        for job in self.job_list:
          self.job_log[job.jobname] = job.get_log()
        self.job_log.write()


    def create_job(self,jobname,jobscript,commands='',
                   header_dict={},write=True):
        header=self.header_dict
        if header_dict: header.update(header_dict)
        # prefix the jobname with the scheduler's name
        job = Job(self.sys,jobname=jobname,jobscript=jobscript,
               commands=commands,header_dict=header,tpl=self.tpl)
        self.update_job_list(job)
        if write: job.write_jobscript()
        return job


    def update_job_list(self,job):
        # update job list, if job alread in list
        if job in self.job_list: 
          self.job_list = [job if job==x
                           else x for x in self.job_list]
        else: self.add_job(job)


    def add_job(self,job):
        self.job_list.append(job)


    def get_job(self,jobname):
        job = next((j for j in self.job_list if j.jobname == jobname), None)
        return job 


    def submit(self,jobname=None):
        if jobname: 
          self.get_job(jobname).submit()
        else:
          for job in self.job_list:
            job.submit()
        self._write_job_log()


    def write_jobscripts(self):
        for job in self.job_list:
           logging.debug('jobname '+job.jobname)
           job.write_jobscript()


    def get_jobids(self):
        """Returns a dict containing {jobname:jobid}

        **Returns:**
            *jobids:*
                A dict containing {jobname:jobid}.

        Written by Lars Buntemeyer

        Last changes 06.02.2019
        """
        self._read_jobids()
        return self.jobids


    def read_jobids(self):
        pass

    
    def get_job_list(self, filters=[]):
        job_list = self.job_list
        #filter job list by filtering jobnames
        if filters:
           job_list = [job for job in self.job_list if any
                      (filter in job.jobname for filter in filters)]
        return job_list


    def get_jobs_acct(self, filters=[]):
        """Returns a dict containing job accounting

        **Arguments:**
            *filters:*
                List of strings to filter jobnames before
                accessing the scheduler database.

        **Returns:**
            *jobs_acct:*
                A dict containing job accounting information, in the
                form, e.g.: {jobname:{'State':state,'JobID':jobid,...}}.

        Written by Lars Buntemeyer

        Last changes 06.02.2019
        """
        jobs_acct = {}
        job_list  = self.get_job_list(filters=filters)
        #filter job list by filtering jobnames
        for job in job_list:
           jobs_acct[job.jobname] = job.get_acct()
        return jobs_acct


    def resubmit(self,states=[]):
        jobs_acct   = self.get_jobs_acct()
        submit_jobs = {}
        for jobname in jobs_acct:
           logging.debug('jobname: '+jobname)
           if jobs_acct[jobname]['State'] in states:
              self.get_job(jobname).submit()
        self._write_job_log()


    def log_jobs_acct(self, filters=None):
        """Logs job accounting information.

        **Arguments:**
            *filters:*
                A string to filter jobnames.

        Written by Lars Buntemeyer

        Last changes 06.02.2019
        """
        counter = {i:0 for i in range(-2,3)}
        jobs_acct = self.get_jobs_acct(filters=filters)
        logging.info(self.STAT_STR.format('StdErr','JobID','State','End','Preview'))
        for jobname in jobs_acct:
           job       = self.get_job(jobname)
           jobid     = jobs_acct[jobname]['JobID']
           state     = jobs_acct[jobname]['State']
           end       = jobs_acct[jobname]['End']
           stateid   = self.STAT[state] if state in self.STAT else UNKNOWN
           counter[stateid]+=1
           logfile   = ''
           error     = []
           if 'StdErr' in job.control:
             logfile = os.path.basename(job.control['StdErr'])
        #   if stateid in [FAILED,UNKNOWN]:
           error     = job.grep_log_err()
           message   = self.STAT_STR.format(logfile,jobid,state,end,'|'.join(error))
           logging.log(LOGLEV[stateid],message)
        invert = {v: k for k, v in self.STAT.items()}
        for i in invert:
          # log errors only if counter > 0 
          if counter[i]>0 or i>=0: logging.log(LOGLEV[i], str(counter[i])+' jobs '+ invert[i] )


