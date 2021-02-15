import time
import requests
from zowe.zos_jobs_for_zowe_sdk import Jobs
from .logger import LOG



class TestJcl:

    # TODO this design needs to be improved
    def __init__(self, test_dataset, connection):
        self.zosmf_url = connection['host_url']
        self.zosmf_user = connection['user']
        self.zosmf_password = connection['password']
        self.test_dataset = test_dataset
        self.zos_jobs = Jobs(connection)
        self.base_jcl = f"""//TESTREXX JOB (AUTOMATION),CLASS=A,MSGCLASS=0,         
//             MSGLEVEL=(1,1),REGION=0M,NOTIFY=&SYSUID
//RUNREXX  EXEC PGM=IKJEFT01
//SYSEXEC  DD DSN={self.test_dataset},DISP=SHR
//SYSTSPRT DD SYSOUT=*
//SYSTSIN  DD *"""

    def trigger_rexx(self, rexx_module):
        LOG.debug(f'Triggering REXX module "{rexx_module}"')
        self.base_jcl += f"\n {rexx_module} \n/*"
        self.__run_jcl()

    def __run_jcl(self):
        LOG.info(f'Submitting test job')
        self.jcl_request = self.zos_jobs.submit_plaintext(self.base_jcl)
        self.jobname = self.jcl_request['jobname']
        self.jcl_status = self.jcl_request['status']
        self.retcode = self.jcl_request['retcode']
        self.jobid = self.jcl_request['jobid']
        self.files_url = self.jcl_request['files-url']
        self.__wait_for_job_to_complete()
        self.result_records = self.__get_result_records()

    def __wait_for_job_to_complete(self):
        while self.retcode != 'CC 0000':
            time.sleep(1.5)
            self.retcode = self.zos_jobs.get_job_status(self.jobname, self.jobid)['retcode']
            LOG.debug(f'Job: {self.jobname} ({self.jobid}) - Return code: {self.retcode}')

    # TODO dependencies on requests module are not ideal (need to improve zowe sdk)
    def __get_result_records(self):
        LOG.info(f"Retrieving output from job {self.jobname} ({self.jobid})")
        file_list = requests.get(self.files_url, auth=(self.zosmf_user, self.zosmf_password), verify=False)
        for item in file_list.json():
            if item['ddname'] == 'SYSTSPRT':
                job_result_object = requests.get(item['records-url'], auth=(self.zosmf_user, self.zosmf_password), verify=False)
                return job_result_object.text.split("\n")
        LOG.error(f"Unable to find valid output for job {self.jobname} ({self.jobid})")
        return []

    # TODO besides removing the dependency on requests I also need to do error checking
    def delete_from_spool(self):
        LOG.debug(f"Deleting {self.jobname}({self.jobid}) from spool")
        requests.delete(f'https://{self.zosmf_url}/zosmf/restjobs/jobs/{self.jobname}/{self.jobid}', auth=(self.zosmf_user, self.zosmf_password), verify=False)
