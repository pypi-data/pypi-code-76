#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This tool will generate a DAG according to the JSON file passed in.

20190107  : JGU
For now, this tool will generate a workflow containing a sequence of GBQ SQL queries executions.

20190306 : JGU
The "--deploy" switch will work only if this script is executed within the directory where the .sql files are.

ie :
|
|-- someDirectory
|      |
       |-- my_dag_description.json
       |-- sql_001.sql
       |-- step_N.sql
       |-- cleanup.sql

"""

import os
import argparse
import json
import pprint
import base64
import datetime
import warnings
import requests
import pickle
import re
import sys
import tempfile
import copy
import networkx as nx
from subprocess import Popen, PIPE, STDOUT

from tailer_sdk import tailer_config
from tailer_sdk import tailer_auth
from tailer_sdk import tailer_misc

# Globals
#
_current_version = "2021.02.22.001"

warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")

REGEX_TASKS_ARRAY = re.compile(r"^\[{1}(\s*[0-9a-zA-Z]+[^\s]+[0-9a-zA-Z]+\s*[,]?)+\]{1}$")
REGEX_WHITESPACES = re.compile(r"\s+")
REGEX_BRACKETS = re.compile(r"\[+|\]")


def pickle_and_encode_file_content(input_file):

    with open(input_file, "r") as f:

        file_content = f.read()

    pickled_payload = pickle.dumps(file_content)
    encoded_payload_forced = base64.b64encode(pickled_payload)
    encoded_payload_forced = str(encoded_payload_forced, "utf-8")

    return encoded_payload_forced


def parse_dag_dependencies(dependencies, entry_task=None, exit_task=None):

    graph = nx.DiGraph()
    previous_item = entry_task

    nodes = []

    for line in dependencies:

        # Removing whitespaces
        #
        line = re.sub(REGEX_WHITESPACES, "", line)

        # DEBUG
        #
        # print("Processing line : {}".format(line))

        parsed_line = line.split(">>")

        for item in parsed_line:

            # DEBUG
            #
            print("\nProcessing : {}".format(item))

            # Check for array
            #
            if re.match(REGEX_TASKS_ARRAY, item) is not None:

                print("Tasks array found.")

                tasks_array = (re.sub(REGEX_BRACKETS, "", item)).split(",")

                # Check if previous item is an array of tasks
                #
                if previous_item is None:

                    previous_item = tasks_array
                    continue

                elif isinstance(previous_item, list):

                    for task_previous in previous_item:
                        for task in tasks_array:

                            if task != task_previous:
                                # print("Adding node : {}".format((task_previous, task)))
                                nodes.append((task_previous, task))

                else:

                    for task in tasks_array:

                        if task != previous_item:
                            # print("Adding node : {}".format((previous_item, task)))
                            nodes.append((previous_item, task))

                previous_item = tasks_array

            else:

                # DEBUG
                #
                print("Prv item type : {}".format(type(previous_item)))

                # Check if previous item is an array of tasks
                #
                if previous_item is None:

                    previous_item = item
                    continue

                elif isinstance(previous_item, list):

                    for task in previous_item:

                        if item != task:
                            print("Adding node : {}".format((task, item)))
                            nodes.append((task, item))

                else:

                    if item != previous_item:
                        # print("Adding node : {}".format((previous_item, item)))
                        nodes.append((previous_item, item))

                # print("Prv item type : {}".format(type(previous_item)))

                previous_item = item

        # END FOR
        #

        previous_item = None

    # Add nodes
    #
    graph.add_edges_from(nodes)

    return list(nx.topological_sort(graph))


def check_task_dependencies_vs_workflow(task_dependencies, workflow):

    # Process workflow
    #
    task_list = []
    for item in workflow:

        task_list.append(item["id"].strip())

    missing_tasks = []
    for line in task_dependencies:

        line = re.sub(">>|<<|\[|\]|,", " ", line)

        for item in line.split():

            if item not in task_list:

                missing_tasks.append(item.strip())

    if len(missing_tasks) > 0:

        print("\n")
        for missing_task in  missing_tasks:
            print("ERROR : the task with ID \"{}\" is present in \"task_dependencies\" but not in \"workflow\". Please fix this.".format(missing_task))

        print("\n")
        return False

    else:

        return True


def check_task_id_naming(workflow):

    # Process workflow
    #
    pattern = "(^[a-zA-Z])([a-zA-Z0-9_]+)([a-zA-Z0-9])$"
    final_result = True

    for item in workflow:

        result = re.match(pattern, item["id"].strip())

        if not result:
            final_result = False
            print("The task ID \"{}\" is malformed. First character must be a letter, you can use letters, numbers and underscores afterwards, but the last character cannot be an underscore.".format(item["id"].strip()))

    return final_result


def build_header(dag_name):

    output_payload = """# -*- coding: utf-8 -*-

import datetime
import logging
import sys
import io
import os
import json
import base64
import uuid
import time
import warnings
import copy
import pytz
from jinja2 import Template
from subprocess import Popen, PIPE, STDOUT
import tempfile

from google.cloud import bigquery
from google.cloud import firestore
from google.cloud import storage
from google.cloud import exceptions
from google.oauth2 import service_account
"""

    # Dump dag name
    #
    output_payload += "\n# Globals \n#\n"
    output_payload += "_dag_name = \"" + dag_name + "\"\n"
    output_payload += "_dag_type = \"gbq-to-gbq\"\n"
    output_payload += "_dag_generator_version = \"" + _current_version + "\"\n\r"
    output_payload +="""TASK_STATUS_FIRESTORE_COLLECTION = "gbq-to-gbq-tasks-status"
AIRFLOW_COM_FIRESTORE_COLLECTION = "airflow-com"
"""

    return output_payload


def build_header_full(dag_name, dag_start_date):

    output_payload = """
import airflow
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator, ShortCircuitOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable
from airflow.operators import FashiondDataPubSubPublisherOperator
from airflow.operators import FashiondDataGoogleComputeInstanceOperator

# FD tools
from dependencies import fd_toolbox

default_args = {
    'owner': 'TAILER',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=2),
    'start_date': datetime.datetime(""" + dag_start_date + """),
    'provide_context': True
}

"""

    # DUmp dag name and other globals
    #
    output_payload += "# Globals \n#\n"
    output_payload += "_dag_name = \"" + dag_name + "\"\n"
    output_payload += "_dag_type = \"gbq-to-gbq\"\n"
    output_payload += "_dag_generator_version = \"" + _current_version + "\"\n\r"

    return output_payload


def build_header_for_direct_execution():

    output_payload = """
import argparse
import etcd3

from google.cloud import secretmanager
from google.cloud import pubsub_v1
from google.api_core import exceptions as google_exception

"""

    return output_payload


def build_functions_for_direct_execution():

    output_payload = """

def get_gcs_file(bucket, filename):

    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.get_blob(filename)
    return blob.download_as_string()


def read_from_firestore(collection_id, document_id, sub_collection=None, sub_doc_id=None):

    retry = 3
    message = None

    while retry > 0:

        try:
            db = firestore.Client()
            if (sub_collection is not None) and (sub_doc_id is not None):
                return_payload = db.collection(collection_id).document(document_id).collection(sub_collection).document(sub_doc_id).get().to_dict()
            else:
                return_payload = db.collection(collection_id).document(document_id).get().to_dict()

            return (return_payload, message)

        except Exception as ex:

            message = str(ex)
            time.sleep(5)
            retry -= 1

    time.sleep(2)

    return (None, message)


def write_to_firestore(collection_id, document_id, payload, sub_collection=None, sub_doc_id=None, merge=False):

    retry = 3
    message = None

    payload["last_updated"] = datetime.datetime.now().isoformat('T')

    while retry > 0:

        try:
            db = firestore.Client()
            if (sub_collection is not None) and (sub_doc_id is not None):
                db.collection(collection_id).document(document_id).collection(sub_collection).document(sub_doc_id).set(payload, merge=merge)
            else:
                db.collection(collection_id).document(document_id).set(payload, merge=merge)

            return (True, message)

        except Exception as ex:

            message = str(ex)
            time.sleep(5)
            retry -= 1

    time.sleep(2)

    return (False, message)


def publish_dag_info_to_firestore(dag_name, dag_run_id, task_id, payload):

    # Set task status
    #
    task_infos = {}
    task_infos[task_id] = "running"
    doc_id = dag_name + \"_\" + dag_run_id
    feedback, message = write_to_firestore(TASK_STATUS_FIRESTORE_COLLECTION, doc_id, task_infos, merge=True)

    if feedback is True:
        logging.info("Pushed {} status to : {}".format(task_id, doc_id))
    else:
        logging.error("Error while processing Task Status : \\n{}".format(message))

    # Process payload
    #

    copy_payload = copy.deepcopy(payload)

    # Add timestamp
    #
    pst = pytz.timezone("UTC")
    status_updated = str(datetime.datetime.now(pst).isoformat(\"T\"))
    copy_payload["status_updated"] = status_updated

    # We need to resolve the configuration context if present
    #
    task_infos[task_id] = "success"

    if "configuration_context" in copy_payload.keys():

        conf_context_document, message = read_from_firestore(copy_payload["configuration_context"]["collection"], copy_payload["configuration_context"]["doc_id"])

        if conf_context_document is None:
            logging.error("Error while processing configuration context : \\n{}".format(message))
            task_infos[task_id] = "failed"

        else:
            copy_payload["configuration_context"] = conf_context_document[copy_payload["configuration_context"]["item"]]

    # Update the DAG status
    #
    feedback, message = write_to_firestore(_dag_type + "-runs", doc_id, copy_payload, merge=True)

    if feedback is True:
        logging.info("Pushed {} status to : {}".format(_dag_name, doc_id))
    else:
        logging.error("Error while processing DAG Status : \\n{}".format(message))
        task_infos[task_id] = "failed"


    # Update task status
    #
    feedback, message = write_to_firestore(TASK_STATUS_FIRESTORE_COLLECTION, doc_id, task_infos, merge=True)

    if feedback is True:
        logging.info("Pushed {} status to : {}".format(task_id, doc_id))
    else:
        logging.error("Error while processing Task Status : \\n{}".format(message))


def check_dag_concurrency(dag_run_id, max_active_runs, firestore_com_id):

    retry = 0

    while retry < 3:

        try:
            # Create the Secret Manager client.
            secret_manager_client = secretmanager.SecretManagerServiceClient()

            # Build the resource name of the secret version.
            #
            secret_id = "tailer-etcd-infos"
            secret_name = "projects/{}/secrets/{}/versions/latest".format(os.environ["PROJECT_ID"], secret_id)

            # Access the secret version.
            #
            secret_response = secret_manager_client.access_secret_version(request={"name": secret_name})

            secret_payload = json.loads(secret_response.payload.data.decode('UTF-8'))

            # Get ETCD information
            #
            etcd_host_address = secret_payload["etcd_host"]
            etcd_host_port = int(secret_payload["etcd_port"])
            etcd_user = secret_payload["etcd_user"]
            etcd_secret = secret_payload["etcd_secret"]

            logging.info("Connecting to ETCD : {}:{}".format(etcd_host_address, str(etcd_host_port)))

            etcd = etcd3.client(host=etcd_host_address, port=etcd_host_port, user=etcd_user, password=etcd_secret)
            etcd_lock = etcd.lock(_dag_name, ttl=15)

            # Instantiate Firestore client
            #
            fs_db = firestore.Client()
            collection = _dag_type + "-runs"
            doc_id = firestore_com_id

            while True:

                # Kill switch
                #
                dag_run_doc = None
                while dag_run_doc is None:

                    dag_run_doc = (fs_db.collection(collection).document(doc_id).get()).to_dict()
                    # dag_run_doc, message = read_from_firestore(collection, doc_id)

                    # if dag_run_doc is None:
                    #     logging.info("Error while retrieving DAG run status.")

                    if (dag_run_doc is not None) and ("killswitch" in dag_run_doc.keys()) and (dag_run_doc["killswitch"] is True):
                        raise Exception("Killed.")
                    else:
                        time.sleep(2)

                if etcd_lock.acquire(timeout=2):

                    logging.info("DAG {} with run ID {} has acquired the lock.".format(_dag_name, dag_run_id))

                    # Now, we need to check how many running instances are there
                    #
                    # TODO
                    # work on the type
                    #

                    logging.info("Trying to retrieve DAG status. Doc ID: {}".format(doc_id))

                    # with firestore.Client() as fs_db:
                    fs_query_result = fs_db.collection(collection).where("dag_id", "==", _dag_name).where("status", "==", "RUNNING").order_by("dag_execution_date", direction=firestore.Query.DESCENDING).limit(int(max_active_runs))

                    counter = 0
                    for instance in fs_query_result.stream():
                        counter += 1

                    logging.info("Count of running instances : {}".format(str(counter)))

                    if counter >= int(max_active_runs):

                        # we cannot launch an new instance
                        #

                        # Release the lock:
                        #
                        etcd_lock.release()
                        time.sleep(5)
                        continue

                    else:

                        # OK, we're good to go
                        #
                        # we need to modify the status of the run to RUNNING
                        #

                        logging.info("We have available slots to run instance ...")

                        dag_run_doc = (fs_db.collection(collection).document(doc_id).get()).to_dict()
                        # dag_run_doc, message = read_from_firestore(collection, doc_id)

                        # if dag_run_doc is None:
                        #     raise Exception("Cannot retrieve DAG run status.")

                        logging.info("DAG status : {}".format(dag_run_doc))

                        dag_run_doc["status"] = "RUNNING"
                        fs_db.collection(collection).document(doc_id).set(dag_run_doc)

                        # ret_value, message = write_to_firestore(collection, doc_id, dag_run_doc)

                        # if ret_value is False:
                        #     raise Exception(message)

                        # Release the lock:
                        #
                        etcd_lock.release()

                        return

                else:

                    logging.info("DAG {} with run ID {} is waiting to get the lock.".format(_dag_name, dag_run_id))
                    time.sleep(5)

        except Exception as ex:

            logging.info("Exception type : {}".format(type(ex)))
            logging.info("Exception      : {}".format(str(ex)))
            time.sleep(5)
            retry += 1

    raise Exception("Error during initialization step.")


def initialize(dag_run_id, firestore_com_id):

    # Read the configuration is stored in Firestore
    #
    collection           = "gbq-to-gbq-conf"
    conf_doc_id          = _dag_name
    task_statuses_doc_id = firestore_com_id

    # Set this task as RUNNING
    #
    task_infos = {}
    task_infos[\"initialize\"] = "running"
    feedback, message = write_to_firestore(TASK_STATUS_FIRESTORE_COLLECTION, task_statuses_doc_id, task_infos, merge=True)

    if feedback is True:
        logging.info("Pushed {} status to : {}".format(\"initialize\", task_statuses_doc_id))
    else:
        logging.error("Error while processing Task Status : \\n{}".format(message))
        raise

    # Check if there is a Run already associated to this ID
    # We are looking for the following attribute : attempt_number
    #
    logging.info("Attempting to retrieve a potential RUN : {}".format(firestore_com_id))
    data_read, message = read_from_firestore("gbq-to-gbq-runs", firestore_com_id)

    if data_read is not None:
        if "attempt_number" in data_read.keys():
            return None, None, None, True
        else:
            # Add "attempt_number" attribute
            #
            data_read["attempt_number"] = 1
            feedback, message = write_to_firestore("gbq-to-gbq-runs", firestore_com_id, data_read, merge=True)

            if feedback is not True:
                logging.error("Error while processing RUN Status : \\n{}".format(message))
                raise
    else:
        logging.error("Error while retrieving RUNS information : \\n{}".format(message))
        raise

    # Retrieve configuration
    #
    dag_configuration, message = read_from_firestore(collection, conf_doc_id)

    if dag_configuration is None:
        logging.error("Error while retrieving configuration : \\n{}".format(message))
        raise

    dag_configuration['sql'] = {}

    # retrieve maximum active runs
    #
    try:
        max_active_runs = dag_configuration["configuration"]["max_active_runs"]
    except Exception:
        max_active_runs = 1

    # Push configuration context
    #
    conf_context = {}
    conf_context["configuration_context"] = dag_configuration
    feedback, message = write_to_firestore(AIRFLOW_COM_FIRESTORE_COLLECTION, task_statuses_doc_id, conf_context, merge=False)

    if feedback is False:
        logging.error("Error while writing configuration context to Firestore : \\n{}".format(message))
        raise

    # Do we need to run this DAG
    # let's check the 'activated' flag
    #
    try:
        dag_activated = dag_configuration["activated"]
    except KeyError:
        print("No activated attribute found in DAGs config. Setting to default : True")
        dag_activated = True

    if dag_activated is True:

        # Allright, we are going to execute this DAG.
        # First of all, we need to check that we are above the DAG concurrency threshold.
        #
        try:

            check_dag_concurrency(dag_run_id=dag_run_id, max_active_runs=max_active_runs, firestore_com_id=firestore_com_id)

        except Exception as ex:

            logging.error("Error while checking DAG concurrency.")
            logging.error("Exception type : {}".format(str(type(ex))))
            logging.error("Exception      : {}".format(str(ex)))
            return None, None, None, None

    # Set this task as SUCCESS
    #
    task_infos = {}
    task_infos[\"initialize\"] = "success"
    feedback, message = write_to_firestore(TASK_STATUS_FIRESTORE_COLLECTION, task_statuses_doc_id, task_infos, merge=True)

    if feedback is True:
        logging.info("Pushed {} status to : {}".format(\"initialize\", task_statuses_doc_id))
    else:
        logging.error("Error while processing Task Status : \\n{}".format(message))
        raise

    # Return these values
    # dag activated : boolean
    # account : string
    # environment : string
    # force_failed = boolean
    #
    return dag_activated, dag_configuration["account"], dag_configuration["environment"], False


def execute_python_script(firestore_com_id, task_id):

    # Read the configuration is stored in Firestore
    #
    db                   = firestore.Client()
    collection           = "gbq-to-gbq-conf"
    conf_doc_id          = _dag_name
    task_statuses_doc_id = firestore_com_id

    # Set this task as RUNNING
    #
    task_infos = {}
    task_infos[\"execute_python_script\"] = "running"
    db.collection("gbq-to-gbq-tasks-status").document(task_statuses_doc_id).set(task_infos, merge=True)

    # Retrieve DAG configuration from Firestore
    #
    dag_conf = db.collection(collection).document(conf_doc_id).get().to_dict()


    # Get PYTHON file
    #
    for wk_item in dag_conf["configuration"]["workflow"]:
        if wk_item["id"] == task_id:
            python_filename = wk_item["python_file"]

    python_filename_composed = "dags/TTT/python_script_tasks/" + _dag_name + "/"+ python_filename

    logging.info("Attempting to retrieve file : {}".format(python_filename_composed))

    python_script = get_gcs_file(bucket=dag_conf["dag_script"]["bucket"], filename=python_filename_composed)

    logging.info(python_script)

    # create file-like string to capture output
    codeOut = io.StringIO()
    codeErr = io.StringIO()

    # capture output and errors
    sys.stdout = codeOut
    sys.stderr = codeErr

    exec(str(python_script))

    # restore stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    s = codeErr.getvalue()

    logging.info("Errors : {}".format(s))

    s = codeOut.getvalue()

    logging.info("Out : {}".format(s))

    codeOut.close()
    codeErr.close()

    # with tempfile.TemporaryDirectory() as tmpdirname:

    #     tmp_file_path = tmpdirname + _dag_name + "_" + task_id + "_" + python_filename

    #     with open(tmp_file_path, "wb") as outfile:

    #         outfile.write(python_script)

    #         # Command building
    #         #
    #         cmd = sys.executable + " " + tmp_file_path

    #         logging.info("Command to execute : {}".format(cmd))

    #         p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, text=True)

    #         with open("/tmp/app.log", "r") as logfile:

    #             lines = logfile.readlines()

    #         for line in lines:
    #             logging.info(line)

    #         # # Get the logs
    #         # #
    #         # output = p.stdout.readlines()
    #         # for line in output:
    #         #     logging.info(line)

    # Set this task as SUCCESS
    #
    task_infos = {}
    task_infos[\"execute_python_script\"] = "success"
    db.collection("gbq-to-gbq-tasks-status").document(task_statuses_doc_id).set(task_infos, merge=True)


def execute_gbq(
    sql_id,
    env,
    dag_name,
    gcp_project_id,
    bq_dataset,
    table_name,
    write_disposition,
    sql_query_template,
    sql_execution_date=None,
    local_sql_query=None,
    firestore_com_id=None,
    use_query_cache=False,
    task_id=None,
    sql_parameters=None,
    **kwargs):

    # Caller function processing for logging
    #
    caller_task_id_for_logging = \"[task_id=\" + task_id + \"]\"

    # Strip the ENVIRONMENT out of the DAG's name
    # i.e : my_dag_PROD -> my_dag
    #
    # stripped_dag_name = _dag_name.rpartition("_")[0]

    # Firestore infos for TTT DAG Configuration
    #
    collection      = "gbq-to-gbq-conf"
    doc_id          = _dag_name

    # Set this task as RUNNING
    #
    logging.info("{} Setting task status : running".format(caller_task_id_for_logging))
    task_infos = {}
    task_infos[task_id] = "running"
    status_doc_id = firestore_com_id

    feedback, message = write_to_firestore(TASK_STATUS_FIRESTORE_COLLECTION, status_doc_id, task_infos, merge=True)

    if feedback is True:
        logging.info("Pushed {} status to : {}".format(task_id, status_doc_id))
    else:
        logging.error("Error while processing Task Status : \\n{}".format(message))
        raise

    # Retrieve SQL Query
    #
    logging.info("{} Trying to retrieve SQL query from Firestore : {} > {}  : sql -> {}".format(caller_task_id_for_logging, collection, doc_id, sql_id))
    data_read, message = read_from_firestore(collection, doc_id)
    if data_read is None:
        logging.error("Error while retrieving SQL query: \\n{}".format(message))
        task_infos[task_id] = "failed"

    data_decoded = base64.b64decode(data_read['sql'][sql_id])
    sql_query = str(data_decoded, 'utf-8')

    # Update the configuration context
    #
    doc_id = firestore_com_id
    airflow_com_doc, message = read_from_firestore(AIRFLOW_COM_FIRESTORE_COLLECTION, doc_id)

    if airflow_com_doc is None:
        logging.error("Error while retrieving configuration : \\n{}".format(message))
        raise

    config_context = airflow_com_doc["configuration_context"]

    config_context['sql'][sql_id] = sql_query
    final_config_context = {}
    final_config_context["configuration_context"] = config_context
    feedback, message = write_to_firestore(AIRFLOW_COM_FIRESTORE_COLLECTION, doc_id, final_config_context, merge=False)

    if feedback is False:
        logging.error("Error while writing configuration context to Firestore : \\n{}".format(message))
        raise

    # Retrieve flag : temporary_table
    #
    temporary_table = False
    for wf_item in data_read["configuration"]["workflow"]:
        try:
            if wf_item["id"].strip() == task_id:
                temporary_table = wf_item["temporary_table"]
        except Exception as ex:
            logging.info("Error while retrieving temporary_table flag. Setting to default -> False")
            logging.info("{} : {}".format(type(ex), str(ex)))
            temporary_table = False

    logging.info("Temporary table flag : {}".format(temporary_table))

    # Replace "sql_query_template" with DAG Execution DATE
    #
    # The expected format id : YYYY-MM-DD
    #
    logging.info("{} sql_query_template : {}".format(caller_task_id_for_logging, sql_query_template))
    if sql_query_template != "":

        if sql_execution_date is not None:
            execution_date = sql_execution_date
        else:
            execution_date = kwargs.get('ds')

        logging.info("{} execution_date : {}".format(caller_task_id_for_logging, execution_date))

        sql_query = sql_query.replace("{{" + sql_query_template + "}}", execution_date)

    # Process SQL parameters
    # sql_parameters
    #
    if sql_parameters is not None:

        for key in sql_parameters.keys():

            sql_query = sql_query.replace("{{" + key.strip() + "}}", str(sql_parameters[key]))

    # Escape " in the query
    #
    sql_query = sql_query.replace('"', '\"')

    logging.info("{} SQL Query : \\n\\r{}".format(caller_task_id_for_logging, sql_query))

    # Specify scopes
    #
    client_options = {
        "scopes": [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/datastore',
            'https://www.googleapis.com/auth/bigquery',
            'https://www.googleapis.com/auth/drive'
        ]}

    # Some initialization
    #
    exception_occured = False
    is_gbq_script = False
    task_information_payload = {
        "task_id": task_id,
        "task_type": "sql",
        "referenced_tables": []
    }

    try:

        # Instantiate GBQ client
        #
        gbq_client = bigquery.Client(
            project=gcp_project_id,
            client_options=client_options)

        dataset_id = bq_dataset
        dataset_ref = gbq_client.dataset(dataset_id)
        dataset = bigquery.Dataset(dataset_ref)
        # dataset.location = "EU"  

        if table_name is not None:
            table_ref = gbq_client.dataset(dataset_id).table(table_name)

        # Try to retrieve schema
        # This will be used later on in a case of query with WRITE_TRUNCATE
        # We do that only when we do not deal with a temporary table AND we have a destination table
        #
        if (temporary_table is False) and (table_name is not None):
            try:
                retrieved_schema = list(gbq_client.get_table(table_ref).schema)
                logging.info("{} {}".format(caller_task_id_for_logging, str(retrieved_schema)))
            except exceptions.NotFound:
                logging.info("{} Table {} does not exist, cannot retrieve schema.".format(caller_task_id_for_logging, table_name))
                retrieved_schema = None

        # Process temporary table
        #
        if (temporary_table is True) and (table_name is not None):

            logging.info("Processing temporary table ...")

            # First, we delete the table
            #
            logging.info("Deleting table : {}".format(table_ref.table_id))
            gbq_client.delete_table(table=table_ref, not_found_ok=True)

            # Second, create the table with an expiration after 12 hours
            #
            pst = pytz.timezone("UTC")
            expiry_date = datetime.datetime.now(pst) + datetime.timedelta(hours=12)
            temp_table = bigquery.Table(table_ref)
            temp_table.expires = expiry_date
            gbq_client.create_table(temp_table)

        # Special loop to determine if we have a regular SQL query or a script
        #
        retry = 3
        first_pass = True

        while retry > 0:

            try:
                # Job Config setup
                #
                job_config = bigquery.QueryJobConfig()
                job_config.use_query_cache = use_query_cache

                # We do a special init for the first pass
                # The goal is to determine if we will run a regular SQL query or a script
                #
                if (table_name is not None) and (first_pass is True):
                    job_config.write_disposition = write_disposition
                    job_config.destination = table_ref

                query_job = gbq_client.query(
                    sql_query,
                    location="EU",
                    job_config=job_config
                )

                results = None

                # Waits for query to complete.
                #
                results = query_job.result()
                is_gbq_script = False
                break

            except google_exception.BadRequest as google_br_exception:
                if len(google_br_exception.errors) > 0:
                    for error in google_br_exception.errors:
                        try:
                            if (error["reason"].strip() == "invalid") \\
                                and ("configuration.query.destinationTable" in error["message"]) \\
                                and ("script" in error["message"]):

                                is_gbq_script = True
                                first_pass = False
                                exception_occured = False
                                retry = 0
                                break

                            else:
                                logging.info("Exception during query execution : {}".format(google_br_exception))
                                exception_occured = True
                                retry = 0
                                break

                        except Exception:
                            retry -= 1
                            logging.info("Exception during query execution : {}".format(type(ex)))
                            logging.info("Exception during query execution : {}".format(ex))
                            exception_occured = True

            except Exception as ex:
                retry -= 1
                logging.info("Exception during query execution : {}".format(ex))
                exception_occured = True

        # Test for exception occurence
        #
        if exception_occured is True:
            raise Exception("Exception during query execution")

        # Add some info
        #
        task_information_payload["is_gbq_script"] = is_gbq_script

        # Check if we have a simple query job or a SCRIPT
        #
        # if query_job.num_child_jobs > 0:
        #     is_gbq_script = True
        # else:
        #     is_gbq_script = False
        # logging.info("This job is GBQ script ? => {}".format(is_gbq_script))
        # task_information_payload["is_gbq_script"] = is_gbq_script

        # Get duration
        #
        job_duration = query_job.ended - query_job.created
        logging.info("{} Duration : {}".format(caller_task_id_for_logging, job_duration))
        task_information_payload["job_duration"] = str(job_duration)

        # Get extra info
        #
        task_information_payload["slot_millis"] = query_job.slot_millis
        task_information_payload["total_bytes_billed"] = query_job.total_bytes_billed
        task_information_payload["total_bytes_processed"] = query_job.total_bytes_processed
        task_information_payload["user_email"] = query_job.user_email

        # Retrieve some information
        #
        if is_gbq_script is True:

            child_jobs_iterable = gbq_client.list_jobs(parent_job=query_job)
            for child_job in child_jobs_iterable:

                # Referenced tables
                #
                for referenced_table in child_job.referenced_tables:
                    task_information_payload["referenced_tables"].append({
                            "table_id": referenced_table.table_id,
                            "dataset_id": referenced_table.dataset_id,
                            "project_id": referenced_table.project})

                # Look for last child job
                #
                if int((child_job.job_id).rpartition("_")[2]) == query_job.num_child_jobs - 1:
                    last_child_job = child_job

            logging.info("\\nThe last job of the script should be : {}\\n".format(last_child_job.job_id))

            # Source table
            #
            source_table = last_child_job.destination

        else:

            # Referenced tables
            #
            for referenced_table in query_job.referenced_tables:
                task_information_payload["referenced_tables"].append({
                        "table_id": referenced_table.table_id,
                        "dataset_id": referenced_table.dataset_id,
                        "project_id": referenced_table.project})

            # Source table
            #
            source_table = query_job.destination

        # Retrieve Referenced Tables
        #
        # referenced_tables = query_job.referenced_tables
        # logging.info("{} Referenced tables : {}".format(caller_task_id_for_logging, referenced_tables))

        # Copy job result to the table
        #
        if (table_name is not None) and (is_gbq_script is True):

            retry = 3
            while retry != 0:
                try:
                    logging.info("Results of the script are going to be written to table : {}".format(table_ref.table_id))

                    # Copy table
                    #
                    job_config = bigquery.CopyJobConfig()
                    job_config.create_disposition = "CREATE_IF_NEEDED"
                    job_config.write_disposition = write_disposition
                        
                    logging.info("{} Source table : {}".format(caller_task_id_for_logging, source_table))

                    job = gbq_client.copy_table(
                            source_table,
                            table_ref,
                            job_config=job_config,
                            location="EU")

                    job.result()
                    break

                except Exception as ex:
                    logging.info("Exception type : {}".format(type(ex)))
                    logging.info(str(ex))
                    retry -= 1

                    if retry == 0:
                        raise

        # Try to update destination schema
        # This is useful in a WRITE_TRUNCATE context
        #
        if (temporary_table is False) and (table_name is not None):
            try:

                # Update schema
                #
                if (write_disposition == "WRITE_TRUNCATE") and (retrieved_schema is not None):
                    logging.info("{} Updating table schema ...".format(caller_task_id_for_logging))
                    table_ref = gbq_client.dataset(dataset_id).table(table_name)
                    table_to_modify = gbq_client.get_table(table_ref)
                    table_to_modify.schema = retrieved_schema
                    table_to_modify = gbq_client.update_table(table_to_modify, ["schema"])
                    assert table_to_modify.schema == retrieved_schema

                next(iter(results))
                logging.info("{} Output of result : {}".format(caller_task_id_for_logging, results))
                logging.info("{} Rows             : {}".format(caller_task_id_for_logging, results.total_rows))

            except Exception as ex:
                logging.info("{} Error while updating table schema : {}".format(caller_task_id_for_logging, str(ex)))


        # Update task status information
        #
        feedback, message = write_to_firestore(TASK_STATUS_FIRESTORE_COLLECTION, status_doc_id, task_information_payload, sub_collection="task-information", sub_doc_id=task_id, merge=True)

        if feedback is True:
            logging.info("Pushed {} task information to : {}".format(task_id, status_doc_id))
        else:
            logging.error("Error while processing Task Information : \\n{}".format(message))
            exception_occured = True
            raise

    except Exception as ex:
        logging.error("{} ERROR while executing query : {}".format(caller_task_id_for_logging, ex))
        exception_occured = True

    # Set task status
    #
    if exception_occured is True:
        task_status = "failed"
    else:
        task_status = "success"

    logging.info("{} Setting task status : {}".format(caller_task_id_for_logging, task_status))
    task_infos = {}
    task_infos[task_id] = task_status
    status_doc_id = firestore_com_id

    feedback, message = write_to_firestore(TASK_STATUS_FIRESTORE_COLLECTION, status_doc_id, task_infos, merge=True)

    if feedback is True:
        logging.info("Pushed {} status to : {}".format(task_id, status_doc_id))
    else:
        logging.error("Error while processing Task Status : \\n{}".format(message))
        raise

    if exception_occured is True:
        raise

"""

    return output_payload


def build_common_function(dag_name, environment):

    output_payload = """

def process_bigquery_record(payload, convert_type_to_string=False, caller_task_id_for_logging=None):

    logging.info("{} Processing RECORD type ...".format(caller_task_id_for_logging))

    # Check for field description
    #
    field_description = None
    try:
        field_description = payload['description']
    except Exception:
        field_description = None

    # Check for field MODE
    #
    mode = None
    try:
        mode = payload['mode']
    except Exception:
        mode = "NULLABLE"

    # Check for field FIELDS
    #
    fields = ()
    try:
        fields_list = payload['fields']
        logging.info("{} {}".format(caller_task_id_for_logging, str(payload['fields'])))
        list_tuples = []

        for field in fields_list:

            # Field, NAME
            field_name = None
            try:
                field_name = field['name']
            except KeyError:
                # error
                continue

            # Field, TYPE
            field_type = None
            try:
                field_type = field['type'].strip()
            except KeyError:
                # error
                continue

            logging.info("{} Field name : {} || Field type : {}".format(
                caller_task_id_for_logging, field_name, field_type))

            # Check if field type is RECORD
            #
            if field_type == "RECORD":
                logging.info("{} Going to process sub Record.".format(caller_task_id_for_logging))
                processed_record = process_bigquery_record(field, caller_task_id_for_logging=caller_task_id_for_logging)
                logging.info("{} Sub Record processed : \\n{}".format(caller_task_id_for_logging, processed_record))
                list_tuples.append(processed_record)

            else:

                # Field, MODE
                field_mode = None
                try:
                    field_mode = field['mode']
                except KeyError:
                    field_mode = "NULLABLE"

                # Field, DESCRIPTION
                field_desc = None
                try:
                    field_desc = field['description']
                except KeyError:
                    field_desc = None

                # Convert FIELD TYPE to STRING
                #
                if convert_type_to_string is True:
                    field_type = "STRING"

                list_tuples.append(bigquery.SchemaField(name=field_name,
                                                        field_type=field_type,
                                                        mode=field_mode,
                                                        description=field_desc))

        fields = tuple(list_tuples)

    except Exception:
        fields = ()

    # Must return a bigquery.SchemaField
    #
    logging.info("{} Creating SchemaField : name : {} || type : {} || desc. : {} || mode : {} || fields : {}".format(
        caller_task_id_for_logging, payload['name'], payload['type'], field_description, mode, fields))
    return bigquery.SchemaField(payload['name'], payload['type'], description=field_description, mode=mode, fields=fields)


def get_firestore_data(collection, doc_id, item, credentials=None):

    # Read the configuration is stored in Firestore
    #
    if credentials is None:
        db              = firestore.Client()
    else:
        info            = json.loads(credentials)
        credentials     = service_account.Credentials.from_service_account_info(info)
        db              = firestore.Client(credentials=credentials)

    collection      = collection

    return (db.collection(collection).document(doc_id).get()).to_dict()[item]


def set_firestore_data(collection, doc_id, item, value, credentials=None):

    # Read the configuration is stored in Firestore
    #
    if credentials is None:
        db              = firestore.Client()
    else:
        info            = json.loads(credentials)
        credentials     = service_account.Credentials.from_service_account_info(info)
        db              = firestore.Client(credentials=credentials)

    collection      = collection

    date_now = datetime.datetime.now().isoformat('T')
    data = {item : value, "last_updated":date_now}

    db.collection(collection).document(doc_id).set(data, merge=True)


def execute_bq_copy_table(  source_gcp_project_id,
                            source_bq_dataset,
                            source_bq_table,
                            destination_gcp_project_id,
                            destination_bq_dataset,
                            destination_bq_table,
                            destination_bq_table_date_suffix,
                            destination_bq_table_date_suffix_format,
                            run_locally=False,
                            firestore_com_id=None,
                            task_id=None,
                            **kwargs):

    try:

        # Caller function processing for logging
        #
        if task_id is None:
            task_id = kwargs["ti"].task_id

        caller_task_id_for_logging = \"[task_id=\" + task_id + \"]\"


        logging.info("{} source_gcp_project_id : {}".format(caller_task_id_for_logging, source_gcp_project_id))
        logging.info("{} source_bq_dataset : {}".format(caller_task_id_for_logging, source_bq_dataset))
        logging.info("{} source_bq_table : {}".format(caller_task_id_for_logging, source_bq_table))
        logging.info("{} destination_gcp_project_id : {}".format(caller_task_id_for_logging, destination_gcp_project_id))
        logging.info("{} destination_bq_dataset : {}".format(caller_task_id_for_logging, destination_bq_dataset))
        logging.info("{} destination_bq_table : {}".format(caller_task_id_for_logging, destination_bq_table))
        logging.info("{} destination_bq_table_date_suffix : {}".format(caller_task_id_for_logging, str(destination_bq_table_date_suffix)))
        logging.info("{} destination_bq_table_date_suffix_format : {}".format(caller_task_id_for_logging, destination_bq_table_date_suffix_format))

        # Create Bigquery client
        #
        if run_locally is False:
            info = json.loads(Variable.get("COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET"))
            credentials = service_account.Credentials.from_service_account_info(info)
            gbq_client = bigquery.Client(project="fd-jarvis-datalake", credentials=credentials)
            db = firestore.Client(credentials=credentials)

        else:

            gbq_client = bigquery.Client(project="fd-jarvis-datalake")
            db = firestore.Client()


        # Set this task as RUNNING
        #
        logging.info("{} Setting task status : running".format(caller_task_id_for_logging))
        task_infos = {}
        if run_locally is False:
            task_infos[kwargs["ti"].task_id] = "running"
            status_doc_id = kwargs["ti"].dag_id + "_" + kwargs["run_id"]
        else:
            task_infos[task_id] = "running"
            status_doc_id = firestore_com_id

        time.sleep(1)
        db.collection("gbq-to-gbq-tasks-status").document(status_doc_id).set(task_infos, merge=True)

        # Source data
        #
        source_dataset = gbq_client.dataset(source_bq_dataset, project=source_gcp_project_id)
        source_table_ref = source_dataset.table(source_bq_table)

        # Destination
        #
        if destination_bq_table_date_suffix is True:
            today = datetime.datetime.now().strftime(destination_bq_table_date_suffix_format)
            logging.info("{} Today : {}".format(caller_task_id_for_logging, today))
            destination_bq_table += "_" + today
            logging.info("{} Destination table : {}".format(caller_task_id_for_logging, destination_bq_table))

        dest_table_ref = gbq_client.dataset(destination_bq_dataset, project=destination_gcp_project_id).table(destination_bq_table)

        job_config = bigquery.CopyJobConfig()
        job_config.write_disposition = "WRITE_TRUNCATE"

        job = gbq_client.copy_table(
            source_table_ref,
            dest_table_ref,
            location="EU",
            job_config = job_config
        )

        job.result()  # Waits for job to complete.
        assert job.state == "DONE"

        # Set this task as SUCCESS
        #
        logging.info("{} Setting task status : success".format(caller_task_id_for_logging))
        task_infos = {}
        if run_locally is False:
            task_infos[kwargs["ti"].task_id] = "success"
            status_doc_id = kwargs["ti"].dag_id + "_" + kwargs["run_id"]
        else:
            task_infos[task_id] = "success"
            status_doc_id = firestore_com_id

        time.sleep(1)
        db.collection("gbq-to-gbq-tasks-status").document(status_doc_id).set(task_infos, merge=True)

    except Exception as ex:

        logging.info("Exception during execute_bq_copy_table.")
        logging.info("Type      : {}".format(type(ex)))
        logging.info("Exception : {}".format(ex))
        raise ex


def execute_bq_create_table(gcp_project_id,
                            force_delete,
                            bq_dataset,
                            bq_table,
                            bq_table_description,
                            bq_table_schema,
                            bq_table_clustering_fields,
                            bq_table_timepartitioning_field,
                            bq_table_timepartitioning_expiration_ms,
                            bq_table_timepartitioning_require_partition_filter,
                            run_locally=False,
                            firestore_com_id=None,
                            sql_execution_date=None,
                            task_id=None,
                            sql_parameters=None,
                            **kwargs):


    # Caller function processing for logging
    #
    if task_id is None:
        task_id = kwargs["ti"].task_id

    caller_task_id_for_logging = \"[task_id=\" + task_id + \"]\"


    logging.info("{} gcp_project_id : {}".format(caller_task_id_for_logging, gcp_project_id))
    logging.info("{} bq_dataset : {}".format(caller_task_id_for_logging, bq_dataset))
    logging.info("{} bq_table : {}".format(caller_task_id_for_logging, bq_table))

    # Create Bigquery client and Firestore client
    #
    if run_locally is False:
        info = json.loads(Variable.get("COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET"))
        credentials = service_account.Credentials.from_service_account_info(info)
        gbq_client = bigquery.Client(project=gcp_project_id, credentials=credentials)
        db = firestore.Client(credentials=credentials)
    else:
        gbq_client = bigquery.Client(project=gcp_project_id)
        db = firestore.Client()

    # Set this task as RUNNING
    #
    logging.info("{} Setting task status : running".format(caller_task_id_for_logging))
    task_infos = {}
    if run_locally is False:
        task_infos[kwargs["ti"].task_id] = "running"
        status_doc_id = kwargs["ti"].dag_id + "_" + kwargs["run_id"]
    else:
        task_infos[task_id] = "running"
        status_doc_id = firestore_com_id

    time.sleep(1)
    db.collection("gbq-to-gbq-tasks-status").document(status_doc_id).set(task_infos, merge=True)


    # Instantiate a table object
    #
    dataset_ref = gbq_client.dataset(bq_dataset, project=gcp_project_id)
    table_ref = dataset_ref.table(bq_table)
    table = bigquery.Table(table_ref)

    # Check wether the table already exist or not
    #
    try:
        table_tmp = gbq_client.get_table(table_ref)
        logging.info("{} Table {} exists.".format(caller_task_id_for_logging, gcp_project_id + "." + bq_dataset + "." + bq_table))

        if force_delete is True:
            logging.info("{} Table {} is flagged to be deleted.".format(caller_task_id_for_logging, gcp_project_id + "." + bq_dataset + "." + bq_table))
            gbq_client.delete_table(gcp_project_id + "." + bq_dataset + "." + bq_table)

        else:

            # Is the table partitioned
            #
            time_partitioning = table_tmp.partitioning_type

            # Let's delete the current date partition
            #
            if time_partitioning is not None:

                if run_locally is False:
                    sql_execution_date = (kwargs.get('ds')).replace("-", "")
                else:
                    sql_execution_date = sql_execution_date.replace("-", "")

                # table_name_with_partition = gcp_project_id + "." + bq_dataset + "." + bq_table + "$" + (kwargs.get('ds')).replace("-", "")
                table_name_with_partition = gcp_project_id + "." + bq_dataset + "." + bq_table + "$" + sql_execution_date
                logging.info("{} Delete partition : {}".format(caller_task_id_for_logging, table_name_with_partition))
                gbq_client.delete_table(table_name_with_partition)

            # Set this task as SUCCESS
            #
            logging.info("{} Setting task status : success".format(caller_task_id_for_logging))
            task_infos = {}
            if run_locally is False:
                task_infos[kwargs["ti"].task_id] = "success"
                status_doc_id = kwargs["ti"].dag_id + "_" + kwargs["run_id"]
            else:
                task_infos[task_id] = "success"
                status_doc_id = firestore_com_id

            time.sleep(1)
            db.collection("gbq-to-gbq-tasks-status").document(status_doc_id).set(task_infos, merge=True)

            return

    except exceptions.NotFound:
        logging.info("{} Table {} does not exist. Let's create it.".format(caller_task_id_for_logging, gcp_project_id + ":" + bq_dataset + "." + bq_table))

    except ValueError as error:
        logging.info("{} {}".format(caller_task_id_for_logging, str(error)))
        logging.info("{} Table {} exists and is not time partitioned.".format(caller_task_id_for_logging, gcp_project_id + ":" + bq_dataset + "." + bq_table))

        # Set this task as SUCCESS
        #
        logging.info("{} Setting task status : success".format(caller_task_id_for_logging))
        task_infos = {}
        if run_locally is False:
            task_infos[kwargs["ti"].task_id] = "success"
            status_doc_id = kwargs["ti"].dag_id + "_" + kwargs["run_id"]
        else:
            task_infos[task_id] = "success"
            status_doc_id = firestore_com_id

        time.sleep(1)
        db.collection("gbq-to-gbq-tasks-status").document(status_doc_id).set(task_infos, merge=True)

        return


    # Get a new REF
    #
    table = bigquery.Table(table_ref)

    # Set table description
    #
    table.description = bq_table_description

    # Processing the table schema
    #
    table_schema_in = bq_table_schema
    table_schema_out = []

    logging.info("{} Table Schema :".format(caller_task_id_for_logging))

    for item in table_schema_in:

        # Field, NAME
        field_name = None
        try:
            field_name = item['name'].strip()
        except KeyError:
            # error
            logging.info("{} ERROR : field does note have NAME".format(caller_task_id_for_logging))
            continue

        # Field, TYPE
        field_type = None
        try:
            field_type = item['type'].strip()
        except KeyError:
            # error
            logging.info("{} ERROR : field does note have TYPE".format(caller_task_id_for_logging))
            continue

        logging.info("{} Field name : {} || Field type : {}".format(caller_task_id_for_logging, field_name, field_type))

        # Check for field description
        field_description = None
        try:
            field_description = item['description']
        except Exception:
            field_description = None

        # Check for field MODE
        mode = None
        try:
            mode = item['mode']
        except Exception:
            mode = "NULLABLE"

        # Process RECORD type
        #
        if field_type == "RECORD":
            if run_locally is False:
                schemafield_to_add = fd_toolbox.process_bigquery_record(item, caller_task_id_for_logging=caller_task_id_for_logging)
            else:
                schemafield_to_add = process_bigquery_record(item, caller_task_id_for_logging=caller_task_id_for_logging)

            logging.info("{} Record processed : \\n{}".format(caller_task_id_for_logging, schemafield_to_add))

        else:
            schemafield_to_add = bigquery.SchemaField(field_name, field_type, description=field_description, mode=mode)

        table_schema_out.append(schemafield_to_add)
        logging.info("{} SchemaField added : {}".format(caller_task_id_for_logging, schemafield_to_add))

    # Some infos
    #
    logging.info("{} {}".format(caller_task_id_for_logging, str(table_schema_out)))


    # Processing clustering fields
    #
    if (bq_table_clustering_fields is not None) and (len(bq_table_clustering_fields) > 0):

        table.clustering_fields = bq_table_clustering_fields
        logging.info("{} Clustering fields : {}".format(caller_task_id_for_logging, str(bq_table_clustering_fields)))

        # Clustering fields option needs time_partition enabled
        #
        table.time_partitioning = bigquery.table.TimePartitioning()

    else:
        logging.info("{} No clustering fields option to process.".format(caller_task_id_for_logging))

    # Processing time partitioning options
    #
    if (bq_table_timepartitioning_field is not None) or (bq_table_timepartitioning_expiration_ms is not None) or (bq_table_timepartitioning_require_partition_filter is not None):

        logging.info("{} Time Partitioning FIELD                    : {}".format(caller_task_id_for_logging, bq_table_timepartitioning_field))
        logging.info("{} Time Partitioning EXPIRATION MS            : {}".format(caller_task_id_for_logging, bq_table_timepartitioning_expiration_ms))
        logging.info("{} Time Partitioning REQUIRE PARTITION FILTER : {}".format(caller_task_id_for_logging, bq_table_timepartitioning_require_partition_filter))
        table.time_partitioning = bigquery.table.TimePartitioning(field=bq_table_timepartitioning_field, expiration_ms=bq_table_timepartitioning_expiration_ms)
        table.require_partition_filter = bq_table_timepartitioning_require_partition_filter

    # Schema
    #
    table.schema = table_schema_out

    for item in table.schema:
        logging.info("{} {}".format(caller_task_id_for_logging, str(item)))

    # Create table
    #
    job = gbq_client.create_table(table)

    # Set this task as SUCCESS
    #
    logging.info("{} Setting task status : success".format(caller_task_id_for_logging))
    task_infos = {}
    if run_locally is False:
        task_infos[kwargs["ti"].task_id] = "success"
        status_doc_id = kwargs["ti"].dag_id + "_" + kwargs["run_id"]
    else:
        task_infos[task_id] = "success"
        status_doc_id = firestore_com_id

    time.sleep(1)
    db.collection("gbq-to-gbq-tasks-status").document(status_doc_id).set(task_infos, merge=True)


"""

    return output_payload


def build_functions(dag_name, environment):

    output_payload = """

def initialize(**kwargs):

    # Read the configuration is stored in Firestore
    #
    info            = json.loads(Variable.get("COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET"))
    credentials     = service_account.Credentials.from_service_account_info(info)
    db              = firestore.Client(credentials=credentials)
    collection      = "gbq-to-gbq-conf"
    doc_id          = \"""" + dag_name + """\"

    # Delete the Task statuses if it exists
    #
    try:
        db.collection("gbq-to-gbq-tasks-status").document(kwargs["ti"].dag_id + "_" + kwargs["run_id"]).delete()
    except Exception:
        logging.info("No Tasks Statuses found.")

    # Set this task as RUNNING
    #
    task_infos = {}
    task_infos[kwargs["ti"].task_id] = "running"
    db.collection("gbq-to-gbq-tasks-status").document(kwargs["ti"].dag_id + "_" + kwargs["run_id"]).set(task_infos, merge=True)


    data_read = (db.collection(collection).document(doc_id).get()).to_dict()
    data_read['sql'] = {}

    # Push configuration context
    #
    guid = datetime.datetime.today().strftime("%Y%m%d") + "-" + str(uuid.uuid4())
    set_firestore_data('airflow-com', guid, 'configuration_context', data_read, Variable.get("COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET"))
    kwargs['ti'].xcom_push(key='configuration_context', value={})
    kwargs['ti'].xcom_push(key='airflow-com-id', value=guid)

    # Push the environment
    kwargs['ti'].xcom_push(key='environment', value=data_read['environment'])


    # Push the account
    kwargs['ti'].xcom_push(key='account', value=data_read['account'])

    # Do we need to run this DAG
    # let's check the 'activated' flag
    #
    #
    dag_activated = True
    try:
        # dag_activated = data_read["activated"]
        dag_activated = json.loads(data_read["activated"])
    except Exception:
        print("No activated attribute found in DAGs config. Setting to default : True")

    # Set this task as SUCCESS
    #
    task_infos = {}
    task_infos[kwargs["ti"].task_id] = "success"
    db.collection("gbq-to-gbq-tasks-status").document(kwargs["ti"].dag_id + "_" + kwargs["run_id"]).set(task_infos, merge=True)

    if dag_activated is True:
        return "send_dag_infos_to_pubsub_after_config"
    else:
        return "send_dag_infos_to_pubsub_deactivated"


def log_to_gbq( short_dag_exec_date,
                dag_execution_date,
                dag_run_id,
                dag_name,
                environment,
                source_sql,
                dest_dataset,
                dest_table,
                num_rows_inserted ):

    # Create Bigquery client
    #
    info = json.loads(Variable.get("COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET"))
    credentials = service_account.Credentials.from_service_account_info(info)
    gbq_client = bigquery.Client(credentials=credentials)

    # Dataset
    #
    dataset_ref = gbq_client.dataset("jarvis_plateform_logs")

    # Table
    #
    schema = [
        bigquery.SchemaField('dag_execution_date', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('dag_run_id', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('dag_name', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('environment', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('source_sql', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('dest_dataset', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('dest_table', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('num_rows_inserted', 'INT64', mode='NULLABLE')
    ]

    # Prepares a reference to the table
    # Create the table if needed
    #
    table_ref = dataset_ref.table("sql_to_gbq_" + short_dag_exec_date)

    try:
        # Check if the table already exists
        #
        gbq_client.get_table(table_ref)

    except Exception as error:

        # The table does not exits, let's create it !
        #
        logging.info("Exception : %s", error)
        gbq_client.create_table(bigquery.Table(table_ref, schema=schema))


    # Prepare the insert query
    #
    query = "INSERT jarvis_plateform_logs.sql_to_gbq_" + short_dag_exec_date + " (dag_execution_date, dag_run_id, dag_name, environment, source_sql, dest_dataset, dest_table, num_rows_inserted) VALUES ('{}','{}','{}','{}','{}','{}','{}',{})"
    query = query.format(   dag_execution_date,
                            dag_run_id,
                            dag_name,
                            environment,
                            source_sql,
                            dest_dataset,
                            dest_table,
                            int(num_rows_inserted) )

    logging.info("QUERY : %s", query)

    job_config = bigquery.QueryJobConfig()

    query_job = gbq_client.query(
        query,
        job_config=job_config
    )

    # Waits for table load to complete.
    #
    query_job.result()

    assert query_job.state == 'DONE'


def execute_gbq(
    sql_id,
    env,
    dag_name,
    gcp_project_id,
    bq_dataset,
    table_name,
    write_disposition,
    sql_query_template,
    sql_execution_date=None,
    run_locally=False,
    local_sql_query=None,
    firestore_com_id=None,
    task_id=None,
    sql_parameters=None,
    **kwargs):

    # Caller function processing for logging
    #
    if task_id is None:
        task_id = kwargs["ti"].task_id

    caller_task_id_for_logging = \"[task_id=\" + task_id + \"]\"

    # Strip the ENVIRONMENT out of the DAG's name
    # i.e : my_dag_PROD -> my_dag
    #
    stripped_dag_name = dag_name.rpartition("_")[0]

    # Read SQL file according to the configuration specified
    # The configuration is stored in Firestore
    #
    if run_locally is False:
        info            = json.loads(Variable.get("COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET"))
        credentials     = service_account.Credentials.from_service_account_info(info)
        db              = firestore.Client(credentials=credentials)

    collection      = "gbq-to-gbq-conf"
    doc_id          = \"""" + dag_name + """\"

    # Set this task as RUNNING
    #
    logging.info("{} Setting task status : running".format(caller_task_id_for_logging))
    task_infos = {}
    if run_locally is False:
        task_infos[kwargs["ti"].task_id] = "running"
        status_doc_id = kwargs["ti"].dag_id + "_" + kwargs["run_id"]
        time.sleep(1)
        db.collection("gbq-to-gbq-tasks-status").document(status_doc_id).set(task_infos, merge=True)
    else:
        task_infos[task_id] = "running"
        status_doc_id = firestore_com_id

        feedback, message = write_to_firestore(TASK_STATUS_FIRESTORE_COLLECTION, status_doc_id, task_infos, merge=True)

        if feedback is True:
            logging.info("Pushed {} status to : {}".format(\"initialize\", status_doc_id))
        else:
            logging.error("Error while processing Task Status : \\n{}".format(message))
            raise

    # Retrieve SQL Query
    #
    logging.info("{} Trying to retrieve SQL query from Firestore : {} > {}  : sql -> {}".format(caller_task_id_for_logging, collection, doc_id, sql_id))

    if run_locally is False:
        data_read = (db.collection(collection).document(doc_id).get()).to_dict()
    else:
        data_read, message = read_from_firestore(collection, doc_id)

        if data_read is None:
            logging.error("Error while retrieving SQL query: \\n{}".format(message))
            task_infos[task_id] = "failed"

    data_decoded = base64.b64decode(data_read['sql'][sql_id])
    sql_query = str(data_decoded, 'utf-8')

    # Update the configuration context
    #
    if run_locally is False:
        doc_id = kwargs['ti'].xcom_pull(key='airflow-com-id')
        config_context = get_firestore_data('airflow-com', doc_id, 'configuration_context', Variable.get("COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET"))
        config_context['sql'][sql_id] = sql_query
        set_firestore_data('airflow-com', doc_id, 'configuration_context', config_context, Variable.get("COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET"))
    else:
        doc_id = firestore_com_id
        airflow_com_doc, message = read_from_firestore(AIRFLOW_COM_FIRESTORE_COLLECTION, doc_id)

        if airflow_com_doc is None:
            logging.error("Error while retrieving configuration : \\n{}".format(message))
            raise

        config_context = airflow_com_doc["configuration_context"]

        config_context['sql'][sql_id] = sql_query
        final_config_context = {}
        final_config_context["configuration_context"] = config_context
        feedback, message = write_to_firestore(AIRFLOW_COM_FIRESTORE_COLLECTION, doc_id, final_config_context, merge=False)

        if feedback is False:
            logging.error("Error while writing configuration context to Firestore : \\n{}".format(message))
            raise

    # Retrieve flag : temporary_table
    #
    if run_locally is True:
        temporary_table = False
        for wf_item in data_read["configuration"]["workflow"]:
            try:
                if wf_item["id"].strip() == task_id:
                    temporary_table = wf_item["temporary_table"]
            except Exception as ex:
                logging.info("Error while retrieving temporary_table flag. Setting to default -> False")
                logging.info("{} : {}".format(type(ex), str(ex)))
                temporary_table = False

        logging.info("Temporary table flag : {}".format(temporary_table))


    # Replace "sql_query_template" with DAG Execution DATE
    #
    # The expected format id : YYYY-MM-DD
    #
    logging.info("{} sql_query_template : {}".format(caller_task_id_for_logging, sql_query_template))
    if sql_query_template != "":

        if sql_execution_date is not None:
            execution_date = sql_execution_date
        else:
            execution_date = kwargs.get('ds')

        logging.info("{} execution_date : {}".format(caller_task_id_for_logging, execution_date))

        sql_query = sql_query.replace("{{" + sql_query_template + "}}", execution_date)

    logging.info("{} SQL Query : \\n\\r{}".format(caller_task_id_for_logging, sql_query))

    scopes = [
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/datastore',
        'https://www.googleapis.com/auth/bigquery',
        'https://www.googleapis.com/auth/drive'
    ]

    if run_locally is False:
        info                = json.loads(Variable.get("COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET"))
        credentials         = service_account.Credentials.from_service_account_info(info, scopes=scopes)
        gbq_client          = bigquery.Client(project=gcp_project_id, credentials=credentials)

    else:
        gbq_client          = bigquery.Client(project=gcp_project_id)

    dataset_id          = bq_dataset
    dataset_ref         = gbq_client.dataset(dataset_id)
    dataset             = bigquery.Dataset(dataset_ref)
    dataset.location    = "EU"
    job_config          = bigquery.QueryJobConfig()
    table_ref           = gbq_client.dataset(dataset_id).table(table_name)

    # Process temporary table
    #
    if (run_locally is True) and (temporary_table is True):

        logging.info("Processing temporary table ...")

        # First, we delete the table
        #
        logging.info("Deleting table : {}".format(table_ref.table_id))
        gbq_client.delete_table(table=table_ref, not_found_ok=True)

        # Second, create the table with an expiration after 12 hours
        #
        pst = pytz.timezone("UTC")
        expiry_date = datetime.datetime.now(pst) + datetime.timedelta(hours=12)
        temp_table = bigquery.Table(table_ref)
        temp_table.expires = expiry_date
        gbq_client.create_table(temp_table)

    # Try to retrieve schema
    # This will be used later on in a case of query with WRITE_TRUNCATE
    try:
        retrieved_schema = list(gbq_client.get_table(table_ref).schema)
        logging.info("{} {}".format(caller_task_id_for_logging, str(retrieved_schema)))
    except exceptions.NotFound:
        logging.info("{} Table {} does not exist, cannot retrieve schema.".format(caller_task_id_for_logging, table_name))
        retrieved_schema = None

    job_config.destination = table_ref
    job_config.write_disposition = write_disposition
    job_config.use_query_cache = False

    query_job = gbq_client.query(
        sql_query,
        location="EU",
        job_config=job_config
    )

    results = None
    try:

        # Waits for query to complete.
        #
        results = query_job.result()

        # Retrieve Referenced Tables
        #
        if run_locally is True:

            referenced_tables = query_job.referenced_tables

            if len(referenced_tables) >= 1:

                # Initialize the object if first arrived
                #
                ref_tables_payload = {}
                ref_tables_payload["referenced_tables"] = {}

                ref_tables_payload["referenced_tables"][task_id] = []

                for table_ref in referenced_tables:
                    ref_tables_payload["referenced_tables"][task_id].append({
                        "table_id": table_ref.table_id,
                        "dataset_id": table_ref.dataset_id,
                        "project_id": table_ref.project})

                # Write status back to Firestore
                #
                feedback, message = write_to_firestore("gbq-to-gbq-runs", doc_id, ref_tables_payload, merge=True)

                if feedback is True:
                    logging.info("Pushed {} status to : {}".format(task_id, doc_id))
                else:
                    logging.error("Error while processing Task Status : \\n{}".format(message))
                    raise

    except exceptions.GoogleCloudError as error:
        logging.error("{} ERROR while executing query : {}".format(caller_task_id_for_logging, error))
        raise error

    try:

        # Update schema
        #
        if (write_disposition == "WRITE_TRUNCATE") and (retrieved_schema is not None):
            logging.info("{} Updating table schema ...".format(caller_task_id_for_logging))
            table_ref = gbq_client.dataset(dataset_id).table(table_name)
            table_to_modify = gbq_client.get_table(table_ref)
            table_to_modify.schema = retrieved_schema
            table_to_modify = gbq_client.update_table(table_to_modify, ["schema"])
            assert table_to_modify.schema == retrieved_schema

        next(iter(results))
        logging.info("{} Output of result : {}".format(caller_task_id_for_logging, results))
        logging.info("{} Rows             : {}".format(caller_task_id_for_logging, results.total_rows))

        if run_locally is False:
            log_to_gbq( kwargs["ds_nodash"],
                        kwargs["ds"],
                        kwargs["run_id"],
                        _dag_name,
                        \"""" + environment + """\",
                        sql_id,
                        bq_dataset,
                        table_name,
                        results.total_rows )
    except:
        logging.info("{} Query returned no result...".format(caller_task_id_for_logging))

    # Set this task as SUCCESS
    #
    logging.info("{} Setting task status : success".format(caller_task_id_for_logging))
    task_infos = {}
    if run_locally is False:
        task_infos[kwargs["ti"].task_id] = "success"
        status_doc_id = kwargs["ti"].dag_id + "_" + kwargs["run_id"]
        time.sleep(1)
        db.collection("gbq-to-gbq-tasks-status").document(status_doc_id).set(task_infos, merge=True)

    else:
        task_infos[task_id] = "success"
        status_doc_id = firestore_com_id

        feedback, message = write_to_firestore(TASK_STATUS_FIRESTORE_COLLECTION, status_doc_id, task_infos, merge=True)

        if feedback is True:
            logging.info("Pushed {} status to : {}".format(task_id, status_doc_id))
        else:
            logging.error("Error while processing Task Status : \\n{}".format(message))
            raise


"""

    return output_payload


def build_complementary_code():

    output_payload = """

    # Initial logging
    #
    send_dag_infos_to_pubsub_start = FashiondDataPubSubPublisherOperator(
        task_id="send_dag_infos_to_pubsub_start",
        dag=dag,
        google_credentials="{{ var.value.COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET }}",
        payload={"dag_id": _dag_name,
                 "dag_execution_date": "{{ execution_date }}",
                 "dag_run_id": "{{ run_id }}",
                 "dag_type": _dag_type,
                 "dag_generator_version": _dag_generator_version,
                 "job_id": _dag_type + "|" + _dag_name,
                 "status": "RUNNING"
                 }
    )

    # First step
    #
    initialize = BranchPythonOperator(
        task_id="initialize",
        dag=dag,
        python_callable = initialize
    )

    # Some logging after reading the configuration
    #
    send_dag_infos_to_pubsub_after_config = FashiondDataPubSubPublisherOperator(
        task_id = "send_dag_infos_to_pubsub_after_config",
        dag = dag,
        google_credentials = "{{ var.value.COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET }}",
        payload = { "dag_id" : _dag_name ,
                    "dag_execution_date" : "{{ execution_date }}",
                    "dag_run_id" : "{{ run_id }}",
                    "dag_type": _dag_type,
                    "dag_generator_version": _dag_generator_version,
                    "configuration_context": {"collection" : "airflow-com", "doc_id" : "{{ task_instance.xcom_pull(key='airflow-com-id') }}", "item" : "configuration_context"},
                    "account": "{{task_instance.xcom_pull(key='account')}}",
                    "environment": "{{task_instance.xcom_pull(key='environment')}}",
                    "job_id": _dag_type + "|" + _dag_name,
                    "status": "RUNNING"
                }
    )

    # In case of failure
    #
    send_dag_infos_to_pubsub_failed = FashiondDataPubSubPublisherOperator(
        task_id = "send_dag_infos_to_pubsub_failed",
        dag = dag,
        trigger_rule='one_failed',
        google_credentials = "{{ var.value.COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET }}",
        payload = { "dag_id" : _dag_name ,
                    "dag_execution_date" : "{{ execution_date }}",
                    "dag_run_id" : "{{ run_id }}",
                    "dag_type": _dag_type,
                    "dag_generator_version": _dag_generator_version,
                    "job_id": _dag_type + "|" + _dag_name,
                    "status": "FAILED"
                }
    )

    # Final step
    #
    send_dag_infos_to_pubsub = FashiondDataPubSubPublisherOperator(
        task_id = "send_dag_infos_to_pubsub",
        dag = dag,
        google_credentials = "{{ var.value.COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET }}",
        payload = { "dag_id" : _dag_name ,
                    "dag_execution_date" : "{{ execution_date }}",
                    "dag_run_id" : "{{ run_id }}",
                    "dag_type": _dag_type,
                    "dag_generator_version": _dag_generator_version,
                    "configuration_context": {"collection" : "airflow-com", "doc_id" : "{{ task_instance.xcom_pull(key='airflow-com-id') }}", "item" : "configuration_context"},
                    "account": "{{task_instance.xcom_pull(key='account')}}",
                    "environment": "{{task_instance.xcom_pull(key='environment')}}",
                    "job_id": _dag_type + "|" + _dag_name,
                    "status": "SUCCESS"
                }
    )

    # Send status via PubSub in case the "activated" configuration flag is set to FALSE
    #
    send_dag_infos_to_pubsub_deactivated = FashiondDataPubSubPublisherOperator(
        task_id = "send_dag_infos_to_pubsub_deactivated",
        dag = dag,
        google_credentials = "{{ var.value.COMPOSER_SERVICE_ACCOUNT_CREDENTIALS_SECRET }}",
        payload = { "dag_id" : _dag_name ,
                    "dag_execution_date" : "{{ execution_date }}",
                    "dag_run_id" : "{{ run_id }}",
                    "dag_type": _dag_type,
                    "dag_generator_version": _dag_generator_version,
                    "configuration_context": {"collection" : "airflow-com", "doc_id" : "{{ task_instance.xcom_pull(key='airflow-com-id') }}", "item" : "configuration_context"},
                    "account": "{{task_instance.xcom_pull(key='account')}}",
                    "environment": "{{task_instance.xcom_pull(key='environment')}}",
                    "job_id": _dag_type + "|" + _dag_name,
                    "status": "DEACTIVATED"
                }
    )

"""

    return output_payload


def build_sql_task(payload, env, default_gcp_project_id, default_bq_dataset, default_write_disposition, global_path, run_locally=False, task_id=None):

    # Check for overridden values : GCP Project ID, Dataset, ...
    #
    gcp_project_id = None
    bq_dataset = None
    write_disposition = None

    print("Building SQL task : {}".format(task_id))

    try:
        gcp_project_id = payload["gcp_project_id"]

    except KeyError:
        gcp_project_id = default_gcp_project_id

    try:
        bq_dataset = payload["bq_dataset"]

    except KeyError:
        bq_dataset = default_bq_dataset

    try:
        write_disposition = payload["write_disposition"]

    except KeyError:
        write_disposition = default_write_disposition

    # Retrieve sql_query_template
    #
    try:
        sql_query_template = payload["sql_query_template"]
    except KeyError:
        sql_query_template = ""

    # Retrieve documentation
    #
    dag_doc = ""
    try:

        # Read the content of the file, UTF-8 converted
        #
        dag_doc = tailer_misc.read_file_as_utf_8("./" + payload["doc_md"])

        if dag_doc is not None:
            dag_doc = dag_doc.decode("utf-8")
        else:
            dag_doc = ""

    except:
        print("No documentation provided for task : {}".format(payload["id"]))

    # Retrieve SQL file to inject into Documentation
    #
    sql_doc = " "

    try:
        # Read the content of the file, UTF-8 converted
        #
        sql_doc = tailer_misc.read_file_as_utf_8("./" + payload["sql_file"])

        if sql_doc is not None:
            sql_doc = sql_doc.decode("utf-8")
            sql_doc = sql_doc.replace("\n", "\n\n")
            sql_doc = sql_doc.replace('"', '\\"')
        else:
            sql_doc = " "

    except Exception as ex:

        print("Error while processing SQL file : {}".format(payload["sql_file"]))
        print("Exception : \n {} \n".format(ex))


    # Retrieve SQL query cache flag
    #
    try:
        use_query_cache = "use_query_cache = " + str(payload["use_query_cache"])
    except Exception:
        use_query_cache = "use_query_cache = False"


    if run_locally is True:

        # Table name becomes optional
        #
        try:
            table_name = "table_name = \"" + payload["table_name"].strip() + "\""
        except Exception:
            table_name = "table_name = None"

        output_payload = """def """ + task_id + """(firestore_com_id, sql_execution_date, sql_parameters=None):

    logging.info("\\n\\nExecuting task with id : {}\\n".format(\"""" + task_id + """\"))

    execute_gbq(sql_id = \"""" + payload["id"] + """\",
        env = \"""" + env + """\",
        dag_name = "TEST",
        gcp_project_id = \"""" + gcp_project_id + """\",
        bq_dataset = \"""" + bq_dataset + """\",
        """ + table_name + """,
        write_disposition = \"""" + write_disposition + """\",
        sql_query_template = \"""" + sql_query_template + """\",
        local_sql_query = \"\"\"""" + sql_doc + """\"\"\",
        firestore_com_id = firestore_com_id,
        """ + use_query_cache + """,
        task_id = \"""" + task_id + """\",
        sql_execution_date = sql_execution_date,
        sql_parameters=sql_parameters
        )

"""

    else:

        # Table name becomes optional
        #
        try:
            table_name = "\"table_name\": \"" + payload["table_name"].strip() + "\""
        except Exception:
            table_name = "\"table_name\": = \"\""

        sql_doc = sql_doc.replace("`", "'")

        output_payload = ""
        output_payload += "    " + payload["id"] + " = "
        output_payload += """PythonOperator(
                task_id = \"""" + payload["id"] + """\",
                dag = dag,
                python_callable = execute_gbq,
                op_kwargs={ "sql_id" : \"""" + payload["id"] + """\",
                            "env" : \"""" + env + """\",
                            "dag_name" : _dag_name,
                            "gcp_project_id" : \"""" + gcp_project_id + """\",
                            "bq_dataset" : \"""" + bq_dataset + """\",
                            """ + table_name + """,
                            "write_disposition" : \"""" + write_disposition + """\",
                            "sql_query_template" : \"""" + sql_query_template + """\"
                            }
                )

    """ + payload["id"] + """.doc_md = \"\"\"""" + dag_doc + """

    # **SQL Query**

    """ + sql_doc + """
    \"\"\"

    """

    # DEBUG
    #
    # print(output_payload)

    return output_payload


def build_copy_bq_table_task(payload, default_gcp_project_id, default_bq_dataset, run_locally=False, task_id=None, firestore_com_id=None):

    # Check for overridden values : GCP Project ID, Dataset, ...
    #
    gcp_project_id = None
    bq_dataset = None

    try:
        gcp_project_id = payload["gcp_project_id"]

    except KeyError:
        gcp_project_id = default_gcp_project_id

    try:
        bq_dataset = payload["bq_dataset"]

    except KeyError:
        bq_dataset = default_bq_dataset

    destination_bq_table_date_suffix = "False"
    destination_bq_table_date_suffix_format = ""
    try:
        destination_bq_table_date_suffix = str(payload["destination_bq_table_date_suffix"])
        destination_bq_table_date_suffix_format = payload["destination_bq_table_date_suffix_format"].strip()
    except KeyError:
        print()

    # Prepare output value
    output_payload = ""

    if run_locally is True:

        output_payload += """def """ + task_id + """(firestore_com_id):

    logging.info("\\n\\nExecuting task with id : {}\\n".format(\"""" + task_id + """\"))

    execute_bq_copy_table(source_gcp_project_id = \"""" + payload["source_gcp_project_id"].strip() + """\",
        source_bq_dataset = \"""" + payload["source_bq_dataset"].strip() + """\",
        source_bq_table = \"""" + payload["source_bq_table"].strip() + """\",
        destination_gcp_project_id = \"""" + gcp_project_id.strip() + """\",
        destination_bq_dataset = \"""" + bq_dataset.strip() + """\",
        destination_bq_table = \"""" + payload["destination_bq_table"].strip() + """\",
        destination_bq_table_date_suffix = """ + destination_bq_table_date_suffix + """,
        destination_bq_table_date_suffix_format = \"""" + destination_bq_table_date_suffix_format + """\",
        run_locally = True,
        firestore_com_id=firestore_com_id,
        task_id = \"""" + task_id + """\"
        )

"""

    else:

        output_payload += "    " + payload["id"] + " = "
        output_payload += """PythonOperator(
            task_id=\"""" + payload["id"] + """\",
            dag=dag,
            python_callable=execute_bq_copy_table,
            op_kwargs={
                "source_gcp_project_id" : \"""" + payload["source_gcp_project_id"].strip() + """\",
                "source_bq_dataset" : \"""" + payload["source_bq_dataset"].strip() + """\",
                "source_bq_table" : \"""" + payload["source_bq_table"].strip() + """\",
                "destination_gcp_project_id" : \"""" + gcp_project_id.strip() + """\",
                "destination_bq_dataset" : \"""" + bq_dataset.strip() + """\",
                "destination_bq_table" : \"""" + payload["destination_bq_table"].strip() + """\",
                "destination_bq_table_date_suffix" : """ + destination_bq_table_date_suffix + """,
                "destination_bq_table_date_suffix_format" : \"""" + destination_bq_table_date_suffix_format + """\"
            }
        )
"""

    return output_payload


def build_create_bq_table_task(payload, default_gcp_project_id, default_bq_dataset, global_path, run_locally=False, task_id=None):

    # Prepare output value
    output_payload = ""

    # Check for overridden values : GCP Project ID, Dataset, ...
    #
    gcp_project_id = None
    bq_dataset = None

    try:
        gcp_project_id = payload["gcp_project_id"]

    except KeyError:
        gcp_project_id = default_gcp_project_id

    try:
        bq_dataset = payload["bq_dataset"]

    except KeyError:
        bq_dataset = default_bq_dataset

    # Open DDL file
    #
    # Add the parameters inside the current payload to save them down the process.
    #

    # Read the content of the file, UTF-8 converted
    #
    ddl_file_read = tailer_misc.read_file_as_utf_8(payload["ddl_file"])

    try:

        payload_ddl = json.loads(ddl_file_read)

    except Exception as ex:
        print("\nError while parsing DDL JSON file : {}".format(payload["ddl_file"]))
        print(ex)
        return False

    payload["bq_table_description"] = payload_ddl["bq_table_description"]
    payload["bq_table_schema"] = payload_ddl["bq_table_schema"]

    # Optional fields
    #
    try:
        payload["bq_table_clustering_fields"] = payload_ddl["bq_table_clustering_fields"]
    except KeyError:
        print("Optional \"bq_table_clustering_fields\" parameter not provided.")

    try:
        payload["bq_table_timepartitioning_field"] = payload_ddl["bq_table_timepartitioning_field"]
    except KeyError:
        print("Optional \"bq_table_timepartitioning_field\" parameter not provided.")

    try:
        payload["bq_table_timepartitioning_expiration_ms"] = payload_ddl["bq_table_timepartitioning_expiration_ms"]
    except KeyError:
        print("Optional \"bq_table_timepartitioning_expiration_ms\" parameter not provided.")

    try:
        payload["bq_table_timepartitioning_require_partition_filter"] = payload_ddl["bq_table_timepartitioning_require_partition_filter"]
    except KeyError:
        print("Optional \"bq_table_timepartitioning_require_partition_filter\" parameter not provided.")

    # Table description
    #
    table_description = ""
    try:
        table_description = payload["bq_table_description"].strip()
    except KeyError:
        table_description = ""

    # Table Schema
    #
    table_schema = []
    try:
        table_schema = payload["bq_table_schema"]
    except KeyError:
        table_schema = []

    # Retrieve clustering fields options
    # Optional
    #
    bq_table_clustering_fields = None
    try:
        bq_table_clustering_fields = payload['bq_table_clustering_fields']
    except KeyError:
        bq_table_clustering_fields = None

    # Retrieve "force_delete" flag
    #
    force_delete = False
    try:
        force_delete = payload['force_delete']
    except KeyError:
        force_delete = False

    # Retrieve BQ Table Time Partitioning options
    # These are optional
    #
    bq_table_timepartitioning_field = None
    bq_table_timepartitioning_expiration_ms = None
    bq_table_timepartitioning_require_partition_filter = None
    try:
        bq_table_timepartitioning_field = payload['bq_table_timepartitioning_field']
    except KeyError:
        bq_table_timepartitioning_field = None
    try:
        bq_table_timepartitioning_expiration_ms = payload['bq_table_timepartitioning_expiration_ms']
    except KeyError:
        bq_table_timepartitioning_expiration_ms = None
    try:
        bq_table_timepartitioning_require_partition_filter = payload[
            'bq_table_timepartitioning_require_partition_filter']
    except KeyError:
        bq_table_timepartitioning_require_partition_filter = None


    if run_locally is True:

        output_payload += """def """ + task_id + """(firestore_com_id, sql_execution_date, sql_parameters=None):

    logging.info("\\n\\nExecuting task with id : {}\\n".format(\"""" + task_id + """\"))

    execute_bq_create_table(gcp_project_id = \"""" + gcp_project_id + """\",
        force_delete = """ + str(force_delete) + """,
        bq_dataset = \"""" + bq_dataset + """\",
        bq_table = \"""" + payload["bq_table"].strip() + """\",
        bq_table_description = \"""" + table_description + """\",
        bq_table_schema = """ + str(table_schema) + """,
        bq_table_clustering_fields = """ + str(bq_table_clustering_fields) + """,
        bq_table_timepartitioning_field = """ + (str(bq_table_timepartitioning_field) if (bq_table_timepartitioning_field is None) else ("\"" + bq_table_timepartitioning_field + "\"")) + """,
        bq_table_timepartitioning_expiration_ms = """ + (str(bq_table_timepartitioning_expiration_ms) if (bq_table_timepartitioning_expiration_ms is None) else ("\"" + bq_table_timepartitioning_expiration_ms + "\"")) + """,
        bq_table_timepartitioning_require_partition_filter = """ + (str(bq_table_timepartitioning_require_partition_filter) if (bq_table_timepartitioning_require_partition_filter is None) else ("\"" + bq_table_timepartitioning_require_partition_filter + "\"")) + """,
        run_locally = True,
        firestore_com_id=firestore_com_id,
        sql_execution_date=sql_execution_date,
        task_id = \"""" + task_id + """\",
        sql_parameters=sql_parameters
        )
"""

        return output_payload

    else:

        output_payload += "    " + payload["id"] + " = "
        output_payload += """PythonOperator(
        task_id=\"""" + payload["id"] + """\",
        dag=dag,
        python_callable=execute_bq_create_table,
        op_kwargs={
            "gcp_project_id" : \"""" + gcp_project_id + """\",
            "force_delete" : """ + str(force_delete) + """,
            "bq_dataset" : \"""" + bq_dataset + """\",
            "bq_table" : \"""" + payload["bq_table"].strip() + """\",
            "bq_table_description" : \"""" + table_description + """\",
            "bq_table_schema" : """ + str(table_schema) + """,
            "bq_table_clustering_fields" : """ + str(bq_table_clustering_fields) + """,
            "bq_table_timepartitioning_field" : """ + (str(bq_table_timepartitioning_field) if (bq_table_timepartitioning_field is None) else ("\"" + bq_table_timepartitioning_field + "\"")) + """,
            "bq_table_timepartitioning_expiration_ms" :""" + (str(bq_table_timepartitioning_expiration_ms) if (bq_table_timepartitioning_expiration_ms is None) else ("\"" + bq_table_timepartitioning_expiration_ms + "\"")) + """,
            "bq_table_timepartitioning_require_partition_filter" :""" + (str(bq_table_timepartitioning_require_partition_filter) if (bq_table_timepartitioning_require_partition_filter is None) else ("\"" + bq_table_timepartitioning_require_partition_filter + "\"")) + """
        }
    )
"""

    return output_payload


def build_vm_launcher_task(payload, gcp_project_id, run_locally=False, task_id=None):

    # Infos
    #
    print("Generating VM LAUNCHER task ...")

    if run_locally is True:
        return ""

    # Retrieve parameters
    #
    try:
        vm_delete = payload["vm_delete"]
    except KeyError:
        vm_delete = False

    try:
        vm_working_directory = payload["vm_working_directory"]
    except KeyError:
        vm_working_directory = "/tmp"

    try:
        vm_compute_zone = payload["vm_compute_zone"]
    except KeyError:
        vm_compute_zone = "europe-west1-b"

    try:
        vm_core_number = payload["vm_core_number"]
    except KeyError:
        vm_core_number = "1"

    try:
        vm_memory_amount = payload["vm_memory_amount"]
    except KeyError:
        vm_memory_amount = "4"

    try:
        vm_disk_size = payload["vm_disk_size"]
    except KeyError:
        vm_disk_size = "10"

    # Prepare output value
    #
    output_payload = ""
    output_payload += "    " + payload["id"] + " = "
    output_payload += """FashiondDataGoogleComputeInstanceOperator(
        task_id=\"""" + payload["id"] + """\",
        dag=dag,
        gcp_project_id = \"""" + gcp_project_id + """\",
        script_to_execute =  """ + "{}".format(payload["script_to_execute"])  + """,
        vm_delete = """ + "{}".format(vm_delete)  + """,
        vm_working_directory = """ + "\"{}\"".format(vm_working_directory)  + """,
        vm_compute_zone = """ + "\"{}\"".format(vm_compute_zone)  + """,
        vm_core_number = """ + "\"{}\"".format(vm_core_number)  + """,
        vm_memory_amount = """ + "\"{}\"".format(vm_memory_amount)  + """,
        vm_disk_size = """ + "\"{}\"".format(vm_disk_size)  + """,
        private_key_id = \"COMPOSER_RSA_PRIVATE_KEY_SECRET\"
    )
"""

    return output_payload


def build_python_script_task(payload, run_locally, task_id):

    # Infos
    #
    print("Generating Python Script task ...")

    if run_locally is False:
        return ""

    else:

        output_payload = """def """ + task_id + """(firestore_com_id):

    logging.info("\\n\\nExecuting task with id : {}\\n".format(\"""" + task_id + """\"))

    execute_python_script(firestore_com_id=firestore_com_id,
        task_id = \"""" + task_id + """\"
        )
"""

    return output_payload


def build_python_script(
    configuration_file,
    read_configuration=None,
    arguments=None,
    run_locally=False):

    # Do we run locally ?
    # We need to check the arguments
    #
    local_tasks = []
    if (run_locally is True) and (arguments is not None):

        index = 2
        while index < len(arguments):
            local_tasks.append(arguments[index].strip())
            index += 1

    # Default env
    #
    environment = "PROD"

    # Infos
    #
    print("Generating and deploying DAG ...")

    if read_configuration is None:

        print("File to process      : {}".format(configuration_file))

        # Open JSON configuration file
        #
        try:

            # Read the content of the file, UTF-8 converted
            #
            json_file_read = tailer_misc.read_file_as_utf_8(configuration_file)

            json_payload = json.loads(json_file_read)

        except Exception as ex:
            print("Error while parsing JSON file : {}".format(configuration_file))
            print(ex)
            return False

    else:

        json_payload = read_configuration

    # Get path of filename
    #
    global_path = tailer_misc.get_path_from_file(configuration_file)

    # Process environment
    #
    # The value set in the JSON file will always be the greatest priority
    #
    try:

        environment = json_payload["environment"].strip()

    except KeyError as ex:

        environment = environment.strip()

    print("Environment          : {}".format(environment))

    # Process ACCOUNT
    #
    try:
        account = json_payload["account"].strip()
    except KeyError as ex:
        account = "000000"

    print("Account          : {}".format(environment))

    # Extract dag name and add the ENV
    #
    if read_configuration is None:
        dag_name = json_payload["configuration_id"] + "_" + environment
    else:
        dag_name = json_payload["configuration_id"]

    # Extract "start_date" and "schedule_interval"
    #
    dag_start_date = json_payload["start_date"]

    # Extract DAG's description
    #
    dag_description = ""
    try:
        dag_description = json_payload["short_description"]
    except KeyError:
        print("No description provided for the DAG.")
        raise Exception("No description provided for the DAG.")

    # Extract DAG's documentation
    #
    dag_doc = ""
    try:
        dag_documentation = global_path + json_payload["doc_md"]

        # Read the content of the file, UTF-8 converted
        #
        dag_doc_file_read = tailer_misc.read_file_as_utf_8(dag_documentation)
        dag_doc = dag_doc_file_read.decode("utf-8")

    except Exception:
        print("No Markdown documentation provided for the DAG.")

    # Extract max_active_runs
    #
    max_active_runs = None
    try:
        max_active_runs = json_payload["max_active_runs"]
    except KeyError:
        max_active_runs = 1

    # Extract task_concurrency
    #
    task_concurrency = None
    try:
        task_concurrency = json_payload["task_concurrency"]
    except KeyError:
        task_concurrency = 5

    # Extract catchup
    #
    catchup = False
    try:
        catchup = json_payload["catchup"]
    except KeyError:
        print("Global parameter \"catchup\" not found. Setting to default : False")

    # Check for direct execution
    #
    try:
        direct_execution = json_payload["direct_execution"]
    except Exception:
        direct_execution = False


    # Extract various default values
    #
    default_gcp_project_id = json_payload["default_gcp_project_id"]
    default_bq_dataset = json_payload["default_bq_dataset"]
    default_write_disposition = json_payload["default_write_disposition"]

    # Extract task dependencies, this should use the Airflow syntax : t1>>t2>>[t31,t32]>>t4
    #
    dag_task_dependencies = json_payload["task_dependencies"]

    # Check that all task declared in "task_dependencies" are properly described in "workflow".
    #
    if check_task_dependencies_vs_workflow(task_dependencies=dag_task_dependencies, workflow=json_payload["workflow"]) is False:
        return False

    # Check that all task IDs are formed properly
    #
    if check_task_id_naming(workflow=json_payload["workflow"]) is False:
        return False

    # Start building the payload
    # build the header
    #
    output_payload = build_header(dag_name)
    if run_locally is True:
        output_payload += build_header_for_direct_execution()
    else:
        output_payload += build_header_full(dag_name, dag_start_date)


    # Build functions according to the case
    #
    output_payload += build_common_function(dag_name, environment)

    if run_locally is True:
        output_payload += build_functions_for_direct_execution()
    else:
        output_payload += build_functions(dag_name, environment)


    # Main code
    #

    # Check for Schedule Interval
    #
    if json_payload["schedule_interval"] == "None":
        dag_schedule_interval = "None"
    else:
        dag_schedule_interval = "\"" + json_payload["schedule_interval"] + "\""

    if run_locally is False:
        output_payload += """
with airflow.DAG(
    _dag_name,
    default_args=default_args,
    concurrency=""" + str(task_concurrency) + """,
    max_active_runs=""" + str(max_active_runs) + """,
    schedule_interval = """ + dag_schedule_interval + """,
    catchup = """ + str(catchup) + """,
    description = \"""" + dag_description + """\") as dag:"""

        output_payload += """
    dag.doc_md = \"\"\"""" + dag_doc + """\"\"\"

    # Create all the task that will execute SQL queries
    #
"""

    # In the case we run locally and the user asked for specific tasks,
    # we need to filter out which task to process
    #
    # First, we make a copy of the original tasks
    #
    tasks_to_process = copy.deepcopy(json_payload["workflow"])

    if (run_locally is True) and (len(local_tasks) > 0):

        tmp_tasks_to_process = []

        for task_requested in local_tasks:

            print("Looking for task : {}".format(task_requested))

            found = False

            for item in tasks_to_process:

                if item["id"].strip() == task_requested:

                    tmp_tasks_to_process.append(copy.deepcopy(item))
                    found = True
                    break

            # No match found
            #
            if found is False:
                print("\nThe task \"{}\" that you've requested does not exist in the configuration workflow. Please check and retry.\n".format(task_requested))
                return

        # Finally overwrite the tasks to process
        #
        tasks_to_process = copy.deepcopy(tmp_tasks_to_process)

    # Process all the tasks
    #
    for item in json_payload["workflow"]:
    #
    #for item in tasks_to_process:

        generated_code = ""

        # Retrieve the task type
        #
        task_type = None
        try:
            task_type = item['task_type'].strip()
        except Exception:
            print("Could not retrieve task type for task id : " +
                  item['id'] + ". This task will be considered as SQL query task.")

        if task_type == "copy_gbq_table":
            generated_code = build_copy_bq_table_task(
                item, default_gcp_project_id, default_bq_dataset, run_locally=run_locally, task_id=item['id'])

        elif task_type == "create_gbq_table":
            generated_code = build_create_bq_table_task(
                item, default_gcp_project_id, default_bq_dataset, global_path, run_locally=run_locally, task_id=item['id'])

            if generated_code is False:
                return False

        elif task_type == "vm_launcher":
            generated_code = build_vm_launcher_task(item, default_gcp_project_id, run_locally=run_locally, task_id=item['id'])

        elif task_type == "python_script":
            generated_code = build_python_script_task(item, run_locally=run_locally, task_id=item['id'])

        else:
            generated_code = build_sql_task(
                item, environment, default_gcp_project_id, default_bq_dataset, default_write_disposition, global_path, run_locally=run_locally, task_id=item['id'])

        output_payload += generated_code + "\n"


    # Add "main" for local execution
    #
    if run_locally is True:

        output_payload += """if __name__ == \"__main__\":

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    root.addHandler(handler)

    warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")

    # Display environment
    #
    logging.info("Environment : {}".format(os.environ))

    # Parsing arguments if any
    #
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--execution-id", help="Execution ID for the DAG.", type=str, default=None)
    parser.add_argument("--configuration-id", help="Configuration ID for the DAG.", type=str, default=None)
    parser.add_argument("--sql-execution-date", help="Date used in SQL template. Format expected YYY-MM-DD", type=str, default=None)
    parser.add_argument("--sql-parameters", help="Extra parameters that will be replacer in the SQL queries", type=str, default=None)
    args = parser.parse_args()
    print("Arguments : {}".format(args))

    # Processing DAG Execution ID, if provided
    #
    if args.execution_id is not None:
        dag_run_id = args.execution_id
    else:
        dag_run_id = \"""" + dag_name + """\" + datetime.datetime.now().strftime(\"%Y%m%d-%H%M%S\") + \"-\" + str(uuid.uuid4())

    # Generate Firestore Com ID
    #
    firestore_com_id = \"""" + dag_name + """\" + "_" + dag_run_id

    # Process SQL parameters
    #
    sql_parameters = None
    if args.sql_parameters is not None:
        try:
            sql_parameters = json.loads(args.sql_parameters)
        except Exception as ex:
            print("Exception")
            print("Type    : {}".format(type(ex)))
            print("Message : {}".format(ex))
            sql_parameters = None

    print("SQL Parameters : {}".format(sql_parameters))

    # DAG execution date
    #
    pst = pytz.timezone("UTC")
    dt_now = datetime.datetime.now(pst)
    dag_execution_date = dt_now.isoformat(\"T\")

    # Processing DAG Execution DATE, if provided
    #
    sql_execution_date = args.sql_execution_date
    if sql_execution_date is None:
        sql_execution_date = dt_now.strftime("%Y-%m-%d")
    logging.info(\"SQL Execution date : {}\".format(sql_execution_date))

    # Job ID
    #
    job_id =  _dag_type + "|" + \"""" + dag_name + """\"


"""

        # Add the generation of dag_run_id
        #
        # output_payload += """    dag_run_id = \"""" + dag_name + """\" + datetime.datetime.today().strftime(\"%Y%m%d-%H%M%S\") + "-" + str(uuid.uuid4())\n"""

        output_payload += """    logging.info(\"Execution of DAG : {}\".format(\"""" + dag_name + """\"))\n"""
        output_payload += """    logging.info(\"DAG Run ID       : {}\".format(dag_run_id))\n\n"""

        # First call to pubsub
        #
        #
        output_payload += """    pubsub_payload={\"dag_id\": \"""" + dag_name + """\",
                    \"dag_execution_date\": dag_execution_date,
                    \"dag_run_id\": dag_run_id,
                    \"dag_type\": _dag_type,
                    \"dag_generator_version\": _dag_generator_version,
                    \"job_id\": job_id,
                    \"status\": "WAITING",
                    \"killswitch\": False,
                    \"env_hostname\": os.environ["HOSTNAME"],
                    \"environment\": \"""" + environment + """\",
                    \"account\": \"""" + account + """\"}
"""
        output_payload += """
    publish_dag_info_to_firestore(dag_name=\"""" + dag_name + """\", dag_run_id=dag_run_id, task_id=\"send_dag_infos_to_pubsub\", payload=pubsub_payload)

"""

        # PubSub payload to be sent after the initialize function
        #
        output_payload += """
    pubsub_payload={\"dag_id\": \"""" + dag_name + """\",
                    \"dag_execution_date\": dag_execution_date,
                    \"dag_run_id\": dag_run_id,
                    \"dag_type\": _dag_type,
                    \"dag_generator_version\": _dag_generator_version,
                    \"configuration_context\": {\"collection\" : \"airflow-com\", \"doc_id\" : firestore_com_id, \"item\" : \"configuration_context\"},
                    \"job_id\": job_id,
                    \"status\": "RUNNING",
                    \"environment\": \"""" + environment + """\",
                    \"account\": \"""" + account + """\"}
"""

        # Initialize function
        #
        output_payload += """
    try:
        ret, account, environment, force_failed = initialize(dag_run_id=dag_run_id, firestore_com_id=firestore_com_id)

        # Start time
        # The duration measurement will starts here
        #
        start_time = datetime.datetime.now()

        pubsub_payload={\"dag_id\": \"""" + dag_name + """\",
                        \"dag_execution_date\": dag_execution_date,
                        \"dag_run_id\": dag_run_id,
                        \"dag_type\": _dag_type,
                        \"dag_generator_version\": _dag_generator_version,
                        \"configuration_context\": {\"collection\" : \"airflow-com\", \"doc_id\" : firestore_com_id, \"item\" : \"configuration_context\"},
                        \"environment\": \"""" + environment + """\",
                        \"account\": \"""" + account + """\",
                        \"job_id\": job_id,
                        \"status\": "RUNNING"}

        if force_failed is True:

            # The DAG must be forced to FAILED
            #
            raise Exception("The DAG has been forced FAILED. An instance must have run before and turned into a staled state.")

        if ret is None:
            raise Exception("Error during initialization.")

        if ret is False:

            # The DAG is deactivated
            #
            pubsub_payload[\"status\"] = \"DEACTIVATED\"
            pubsub_payload[\"duration\"] = str(datetime.datetime.now() - start_time)
            publish_dag_info_to_firestore(dag_name=\"""" + dag_name + """\", dag_run_id=dag_run_id, task_id=\"send_dag_infos_to_pubsub_after_initialization\", payload=pubsub_payload)
            exit(0)

        # We keep going
        #
        publish_dag_info_to_firestore(dag_name=\"""" + dag_name + """\", dag_run_id=dag_run_id, task_id=\"send_dag_infos_to_pubsub_after_initialization\", payload=pubsub_payload)

"""

        # Parse dependencies
        #
        # if len(json_payload["task_dependencies"]) == 0:
        if len(json_payload["workflow"]) <= 1:

            # In that case, we are going to build the execution in the order of the workflow
            #
            parsed_dag_dependencies = []
            for task in tasks_to_process:
                parsed_dag_dependencies.append(task["id"].strip())
        else:

            # We try to parse as a DAG
            #
            parsed_dag_dependencies = parse_dag_dependencies(dependencies=json_payload["task_dependencies"])
            print("Parsed dependencies : {}".format(parsed_dag_dependencies))

        # Add the user tasks
        #
        for task in parsed_dag_dependencies:

            # look for task details
            #
            for pr_task in tasks_to_process:

                if task == pr_task["id"]:

                    # Add sql type if missing
                    #
                    try:
                        task_type = pr_task["task_type"].strip()
                    except Exception:
                        task_type = "sql"

                    if (task_type == "sql") \
                        or ( task_type == "create_gbq_table") \
                        or ( task_type == "run_gbq_script"):

                        output_payload += """
        """ + task + """(firestore_com_id=firestore_com_id, sql_execution_date=sql_execution_date, sql_parameters=sql_parameters)\n"""
                    else:
                        output_payload += """
        """ + task + """(firestore_com_id=firestore_com_id)\n"""


        output_payload += """

    except Exception as ex:
        print(\"Exception type : {}\".format(type(ex)))
        print(\"Exception      : {}\".format(ex))

        # Failure
        #
        pubsub_payload[\"status\"] = \"FAILED\"
        pubsub_payload[\"duration\"] = str(datetime.datetime.now() - start_time)
        publish_dag_info_to_firestore(dag_name=\"""" + dag_name + """\", dag_run_id=dag_run_id, task_id=\"send_dag_infos_to_pubsub_failed\", payload=pubsub_payload)

        exit(0)

    # Success
    #
    pubsub_payload[\"status\"] = \"SUCCESS\"
    pubsub_payload[\"duration\"] = str(datetime.datetime.now() - start_time)
    publish_dag_info_to_firestore(dag_name=\"""" + dag_name + """\", dag_run_id=dag_run_id, task_id=\"send_dag_infos_to_pubsub_success\", payload=pubsub_payload)

    exit(0)
"""



    # Processing for COMPOSER (Airflow) version
    #
    if run_locally is False:

        # Add "initialize" function
        # Add PubSub logging
        output_payload += build_complementary_code()

        # Add task dependencies
        #
        output_payload += """
    # Task dependencies
    #
    send_dag_infos_to_pubsub_start >> initialize >> send_dag_infos_to_pubsub_after_config
    initialize >> send_dag_infos_to_pubsub_deactivated
"""

        if len(dag_task_dependencies) > 0:
            for index in range(0, len(dag_task_dependencies)):
                output_payload += "    " + dag_task_dependencies[index] + "\n"

        # Add the task "send_dag_infos_to_pubsub" as the last task
        #
        for item in json_payload["workflow"]:
            output_payload += """    """ + \
                item["id"] + """ << send_dag_infos_to_pubsub_after_config\n\r"""
            output_payload += """    """ + \
                item["id"] + """ >> send_dag_infos_to_pubsub\n\r"""
            output_payload += """    """ + \
                item["id"] + """ >> send_dag_infos_to_pubsub_failed\n\r"""

    # Add direct_execution if not present
    #
    try:
        direct_execution = json_payload["direct_execution"]

        if type(direct_execution) is not bool:
            json_payload["direct_execution"] = True

    except Exception:
        json_payload["direct_execution"] = True

    return output_payload, json_payload, dag_name, environment


def process(
        configuration_file,
        read_configuration=None,
        run_locally=False,
        arguments=None,
        tailer_sdk_version=None):

    # Force local generation
    #
    output_payload_forced, json_payload, dag_name, environment = \
        build_python_script(
            configuration_file,
            read_configuration=read_configuration,
            arguments=None,
            run_locally=True)

    # Generate python script
    #
    output_payload, json_payload, dag_name, environment = \
         build_python_script(
             configuration_file,
             read_configuration=read_configuration,
             arguments=arguments,
             run_locally=run_locally)

    # print(json.dumps(json_payload))
    # return True

    data = {}
    sql_data = {}
    short_description_data = {}
    doc_md_data = {}

    index = 0
    for item in json_payload["workflow"]:

        # Info
        print("Processing task : " + item["id"])

        # Retrieve the task type
        #
        task_type = None
        try:
            task_type = item['task_type'].strip()
        except Exception:
            print("Could not retrieve task type for task id : " +
                    item['id'] + ". This task will be considered as SQL query task.")

        # retrieve short description
        #
        short_description = ""
        try:
            short_description = item['short_description']
            short_description_data[item["id"]] = short_description
        except KeyError:
            print("No short description found. Continue ...")

        # retrieve Markdown documentation
        #
        try:

            # Read the content of the file, UTF-8 converted
            #
            doc_md_file_read = tailer_misc.read_file_as_utf_8("./" + item["doc_md"])

            if doc_md_file_read is not None:
                doc_md = doc_md_file_read.decode("utf-8")
            else:
                doc_md = ""

            doc_md_data[item["id"]] = doc_md

            # Overwrite in the source configuration
            #
            json_payload["workflow"][index]['doc_md'] = doc_md

        except KeyError:
            print("No Markdown documentation to process. Continue.")
        except Exception as error:
            print(type(error))
            print("Error while attempting to read Markdown doc : {}. Check your MD file. Continue.".format(error))

        # Specific processing depending of the task type
        #
        if task_type == "copy_gbq_table":
            print("")
        elif task_type == "create_gbq_table":
            print("")
        elif task_type == "vm_launcher":
            print("")
        elif task_type == "python_script":
            print("")
        else:

            # default : SQL query
            #

            # Read the content of the file, UTF-8 converted
            #
            sql_file_read = tailer_misc.read_file_as_utf_8("./" + item["sql_file"])

            sql_data[item["id"]] = base64.b64encode(sql_file_read)

            # Retrieve temporary_table flag
            #
            try:
                temporary_table = item["temporary_table"]
            except KeyError:
                # We set the flag to False and save it back to the main payload
                #
                json_payload["workflow"][index]['temporary_table'] = False


        index += 1
    # END FOR

    # Add SQL data
    data["sql"] = sql_data

    # Add short descriptions
    data['short_descriptions'] = short_description_data

    # Add Markdown documentations
    data['docs_md'] = doc_md_data

    # Add account
    data['account'] = json_payload['account']

    # Add environment
    data['environment'] = environment

    # Let's add the whole configuration file as well
    #
    data["configuration"] = json_payload

    # Add info for regular processing by the API
    #
    data["configuration_type"] = "gbq-to-gbq"

    if read_configuration is None:
        data["configuration_id"] = dag_name
    else:
        data["configuration_id"] = json_payload["configuration_id"]


    data["client_type"] = "tailer-sdk"
    data["client_version"] = tailer_sdk_version

    # Process the "run locally" option
    #
    if run_locally is True:

        # Run locally
        #
        with tempfile.TemporaryDirectory() as tmpdirname:

            print(tmpdirname)

            tmp_file_path = tmpdirname + dag_name + ".py"

            # DEBUG
            #
            with open(dag_name + ".py", "w") as local_out_file:
                local_out_file.write(output_payload_forced)

            return

            with open(tmp_file_path, "w") as outfile:

                outfile.write(output_payload_forced)

                print("\n\nThe TTT configuration will now run locally...\n\n")

                # Python executable used here
                #
                python_executable = sys.executable
                print("Python executable used : {}\n".format(python_executable))

                # Execute the file
                #
                command = python_executable + " " + tmp_file_path
                p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, text=True)

                # Get the logs
                #
                for line in p.stdout.readlines():
                    print(line, end="")


        return

    #######################
    # Prepare call to API #
    #######################

    # Get configuration
    #
    print()
    print("Get Tailer configuration ...")
    tailer_configuration = tailer_config.get_tailer_configuration_file()

    # Get firebase user
    #
    print("Get user information ...")
    firebase_user = tailer_auth.get_refreshed_firebase_user(tailer_configuration)

    # Check if the Default GCP Project is there
    #
    try:
        project_profile = json_payload["default_gcp_project_id"].strip()

    except Exception:

        # Get list of project profiles open to the user and ask him to pick one
        #
        ret_code, project_profile = tailer_misc.choose_project_profiles(tailer_configuration, firebase_user)
        if ret_code is False:
            return False

    print("\nThis DAG is going to be deployed to : {}\n".format(project_profile))

    # Check for direct execution
    #
    try:
        direct_execution = json_payload["direct_execution"]
    except Exception:
        direct_execution = False

    # Check if a DAG with the same name is already deployed
    #
    if direct_execution is False:

        try:

            print("Calling Tailer API ...")

            url = tailer_configuration["tailer_api_endpoint"] + "dag-generator-v2"
            payload = {
                "payload": {
                    "resource": "check_dag_exists",
                    "dag_file" : {
                        "name": dag_name + ".py"
                    },
                    "project_profile": project_profile
                }
            }
            headers = {
                "Content-type": "application/json",
                "Authorization": "Bearer " + firebase_user["idToken"]}

            r = requests.put(url, headers=headers, data=json.dumps(payload), verify=tailer_configuration["perform_ssl_verification"])

            if r.status_code == 200:
                response = r.json()
                print(response["payload"]["message"])

                # DAG file already exists
                # We need to ask the user if everything is OK
                #
                while True:
                    print("The DAG {} already exists, do you want to overwrite it y/n ? : ".format(dag_name), end='', flush=True)
                    user_value = input()

                    if user_value == "y":
                        break
                    elif user_value == "n":
                        return True
                    else:
                        continue

            elif r.status_code == 404:
                # Everything is OK
                print(str(r.content, "utf-8"))
            else:
                print("\nError : %s\n" % str(r.content, "utf-8"))
                print(r.json())
                return False

        except Exception as ex:
            print("Error while trying to contact Tailer API ...")
            print(ex)
            return False


    # Process data
    #
    pickled_data = pickle.dumps(data)
    encoded = base64.b64encode(pickled_data)
    encoded = str(encoded, "utf-8")

    # Process payload
    #
    pickled_payload = pickle.dumps(output_payload)
    encoded_payload = base64.b64encode(pickled_payload)
    encoded_payload = str(encoded_payload, "utf-8")

    # Process AIRFLOW version
    # Debug
    # with open(dag_name + ".py", "w") as local_out_file:
    #     local_out_file.write(output_payload)
    #     return

    # Process LOCAL payload
    #
    # DEBUG
    # with open(dag_name + ".py", "w") as local_out_file:
    #     local_out_file.write(output_payload_forced)
    #     return

    pickled_payload = pickle.dumps(output_payload_forced)
    encoded_payload_forced = base64.b64encode(pickled_payload)
    encoded_payload_forced = str(encoded_payload_forced, "utf-8")

    # Ask if the user wants to launch an execution upon successfull upload
    #
    while True:
        print("Do you want to execute your TTT DAG upon successfull upload ? y/n. Press enter for \"n\" : ", end='', flush=True)
        user_value = input()

        if len(user_value) == 0:
            user_value = "n"

        if user_value == "y":
            execute_dag = True
            break
        elif user_value == "n":
            execute_dag = False
            break

    # Call API
    #
    try:

        print("Calling Tailer API ...")

        url = tailer_configuration["tailer_api_endpoint"] + "dag-generator-v2"
        payload = {
            "payload": {
                "resource": encoded,
                "dag_file" : {
                    "name" : dag_name + ".py",
                    "data" : encoded_payload
                },
                "python_script" : {
                    "name" : dag_name + ".py",
                    "data" : encoded_payload_forced
                },
                "project_profile": project_profile,
                "uid": firebase_user["userId"],
                "client_type": "tailer-sdk",
                "client_version": tailer_sdk_version,
                "execute_dag": execute_dag
            }
        }

        # Add headers
        #
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"]}

        r = requests.put(url, headers=headers, data=json.dumps(payload), verify=tailer_configuration["perform_ssl_verification"])

        if r.status_code != 200:
            print("\nERROR : %s\n" % str(r.content, "utf-8"))
            return False
        else:
            response = r.json()
            print(response["payload"]["message"])
            return True

    except Exception as ex:
        print("Error while trying to contact Tailer API ...")
        print(ex)
        return False
