import json
import re
import zipfile
import os
import sys
import certifi
import urllib3.request
import requests
import nuvpy.nuviot_srvc as nuviot_srvc

job_server = os.environ.get('JOB_SERVER')

job_server = 'http://localhost:5051'

def get_launch_args():
    """
    Method to return job_type_id and job_id from the parameters used to launch a script.
   
    Returns
    ---------
    out: job_type_id, job_id
        Returns a tuple that contains the job_type_id and job_id
   
    """

    if(len(sys.argv) < 2):
        raise Exception("Expecting at least two launch args, including one with a comma delimitted job_type_id and job_id")

    parts = sys.argv[1].split(',')

    if(len(parts) != 2):
        raise Exception("Launch argument must be a comma delimitted string that include job type id and job id")

    return parts[0], parts[1]

def set_job_status(job_type_id: str, job_id: str, status: str):
    """
    Set job to current status, this will also post a push notification
    to send updates to any subscribed clients.

    Parameters
    ----------
    job_type_id : string
       The job type id to update the status, for jobs running reports this is the report id

    job_id: string
        The job id to update the percentage completion for the job that is being executed.
    
    """
    r = requests.get('%s/api/job/%s/%s/%s' % (job_server, job_type_id, job_id, status))
    if(r.status_code > 299):
        raise Exception("Error setting job status")

def set_job_progress(job_type_id, job_id, percent_complete):
    """
    Update job the job progress percent, this will also post a push
    notification to sned updates to any subscribed clients.

    Parameters
    ----------
    job_type_id: string
       The job_type_id to update the percentage completed for reports this is the report id

    job_id: string
        The job_id to update the percentage completion for the job that is being executed.

    """
    r = requests.get('%s/api/job/%s/%s/progress/%d' % (job_server, job_type_id, job_id, percent_complete))
    if(r.status_code > 299):
       raise Exception("Error setting job status")

def get_job(job_type_id: str, job_id: str):
    """
    Download a job, a job consists of the information necessary to build a report or process data
    
    Parameters
    ----------
    job_type_id: string
        The job_type_id is the defintion of what needs to be done for this job.

    job_id: string
        The job_id is the instance of the job that should be executed.
   
    Returns
    ----------
    out : job, parameters
        Tuple to include a job and the parmaters that can be used for the execution of the job.
    """

    set_job_status(job_type_id, job_id, "Running")

    getJobUri = job_server + '/api/job/' + job_type_id + '/' + job_id
   
    r = requests.get(getJobUri)
    if(r.status_code > 299):
        raise Exception("Could not get job details for job type id=%s and job id=%s" % (jobTypeId, jobId))

    job = json.loads(r.text)
    reportParameters = json.loads(job["payload"])
    return job, reportParameters


def download_script_file(ctx, script_id, output_dir):
    """
    Download a script file, or collection of files that make up the scripts necessry to execute
    a job or a report.  If the script is a collection of files it will be downloaded as a zip
    file an extracted in the directory provided.

    If a zip file is downloaded, the file that has the method start_job will be returned.

    Parameters
    ---------
    ctx: AuthContext
       Authorization context as previously created with nuviot_auth

    script_id: string
        ID of the script that will be downloaded

    output_dir:
        Base directory of where the file(s) should be downloaded.

    Returns
    ---------
    out: string
        Returns the name of the script file that can be loaded and executed
    
    """
    path = "/clientapi/report/%s/runtime" % script_id
    if ctx.auth_type == 'user':
        headers={'Authorization': 'Bearer ' + ctx.auth_token}
    else:
        headers={'Authorization': 'APIKey ' + ctx.client_id + ':' + ctx.client_token}

    url = ctx.url + path

    chunk_size = 65536

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request("GET", url, headers=headers, preload_content=False)

    if r.status > 299:
        print('Failed http %d url: %s' % (r.status, url))
        print('Headers: ' + str(headers))
        print('--------------------------------------------------------------------------------')
        print()
        r.release_conn()
        return None

    m = re.search('filename=?([\w\.\-]*)',r.headers['Content-Disposition'])
    fileName = m.group(1)
    fullOutput = "%s/%s" % (output_dir, fileName)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(fullOutput, 'wb') as out:
        while True:
            data = r.read(65535)
            if not data:
                break
        
            out.write(data)
    r.release_conn()
   
    if r.headers["Content-Type"] == "application/zip":
        with zipfile.ZipFile(fullOutput, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

        os.remove(fullOutput)
        
        sys.path.append(output_dir)

        files = os.listdir(output_dir)
        for file in files:
            script_file_name, file_extension = os.path.splitext(file)
            if(file_extension.lower() == ".py"):
                module = __import__(script_file_name)
                if(callable(getattr(module, "start_job", None))):
                    return script_file_name

        raise Exception("Could not find script file that implements start_job")
    else:
        script_file_name, file_extension = os.path.splitext(file)
        
        return script_file_name