"""
    Client side functions for working with LDM framework.
"""

import json
import requests
import shutil
import sys
import os
import zipfile

from pathlib import Path


class LDMLogger():
    """
        Class LDMLogger containing methods for working with LDM framework.
            Methods
            -------
                def start_run(self, comment = "", git_commit_url = "" ):
                    Starts a new run
                def log(self, body):
                    Logs message msg to server.
                def finish_run(self):
                    Finish the current run.
                def validate(self, results, dataset_type="Train"):
                    Validate on dataset.
                def upload_file(self, file_name, comment = ""):
                    Uploads file (file_name) to the logging server and attaches it to the current run.
                def add_project(self, name, project_type, description=""):
                    Adding project.
                 def upload_dataset(self, path_to_dataset, dataset_type_in="Train"):
                    Uploads dataset to server.
                def download_dataset(self, path="", dataset_type_in="Train"):
                    Downloads dataset from server.
    """

    def __init__(self, user_token, project_id=None, server_url="http://localhost:5000", 
                 root_dir=Path(os.getcwd()).parent, should_upload_sources = False):
        self.token = user_token
        self.project_id = project_id
        self.server_url = server_url
        self.root_dir = root_dir
        self.current_run_id = None
        self.should_upload_sources = should_upload_sources


    def start_run(self, comment = "", git_commit_url = "" ):
        """ 
        Start a new run.
      
        Parameters: 

        comment (string): Comment for a run.  This parameter is optional and can be ommited.

        git_commit_url (string): URL of a git commit representing the state of a code base used in this run. This prm is optional and can be ommited.
      
        Returns: 

        None  
        """

        try:
            r = requests.post(
                self.server_url + "/logger/start-run/" + self.project_id,
                json={
                    'comment': comment, 
                    'git_commit_url': git_commit_url
                },
                headers={'Content-Type':'application/json', "Authorization": "Bearer " + self.token}
            )

            if (r.status_code == 200):
                self.current_run_id = r.json()['id']

                # uploading source code
                if self.should_upload_sources:
                    self.upload_sources()

            else:
                print("Finish run FAILED. \n" + r.json()['err'])
        except:
            print("Unknown Error in start_run.")
            print(sys.exc_info()[0])
            raise


    def log(self, body):
        """ Logs message msg to server.
      
        Parameters: 

        msg (string): Message to log 

        role_name (string): Role name of a message. Role name is optional and can be ommited.
      
        Returns: 

        None
        """

        try:
            r = requests.post(
                self.server_url + "/logger/log/" + self.project_id + "/" + self.current_run_id, 
                json={
                    'body': body, 
                },
                headers={'Content-Type':'application/json', "Authorization": "Bearer " + self.token}
            )

            if (r.status_code != 200):
                print("Error: " + r.json()['err'])
        except:
            print("Unknown Error in log(msg)")
            print(sys.exc_info()[0])
            raise


    def finish_run(self):
        """ 
        Finish the current run.
      
        Parameters: 
      
        Returns: 

        None
      
        """    

        try:
            r = requests.post(
                self.server_url + "/logger/finish-run/"  + self.project_id + "/" + self.current_run_id, 
                headers={'Content-Type':'application/json', "Authorization": "Bearer " + self.token}
            )
            if (r.status_code != 200):
                print("Error: " + r.json()['err'])
        except:
            print("Unknown error in finish_run.")
            print(sys.exc_info()[0])
            raise


    def validate(self, results, dataset_type="Train"):
        """ 
        Validate on dataset.
      
        Parameters: 
      
        Returns: 

        None
      
        """    

        try:
            r = requests.post(
                self.server_url + "/logger/validate/"  + self.project_id, 
                json={
                    'type': dataset_type,
                    'run_id': self.current_run_id,
                    'results': results,
                },
                headers={'Content-Type':'application/json', "Authorization": "Bearer " + self.token}
            )
            if (r.status_code != 200):
                print("Error: " + r.json()['err'])
        except:
            print("Unknown error in finish_run.")
            print(sys.exc_info()[0])
            raise


    def upload_file(self, file_name, comment = ""):
        """ 
        Upload file (file_name) to the logging server and attaches it to the current run.
      
        Parameters: 

        file_name (string): File path (on a local machine) of file to be uploaded.

        comment (string): Comment for a file to be uploaded.  This prm is optional and can be ommited.
      
        Returns: 

        None
      
        """    

        try:
            with open(file_name, 'rb') as f:

                r = requests.post(self.server_url + '/logger/upload-file/' + self.project_id + "/" + self.current_run_id,
                                  files={'file': f, 'file2': f, 'data': json.dumps({'comment': comment}),},
                                  headers={"Authorization": "Bearer " + self.token}
                                )

                if (r.status_code != 200):
                    print("Error: " + r.json()['err'])

        except:
            print("Unknown error in upload_file.")
            print(sys.exc_info()[0])
            raise


    def upload_sources(self):

        # if self.root_dir is None, then no source code upload
        if (self.root_dir is None):
            return

        # making tmp zip file of the source dir and its subdirs, then posting is as logger_zip.zip
        zf_path = os.path.join(Path(self.root_dir).parent, "logger_zip.zip")
        zf = zipfile.ZipFile(zf_path, "w")

        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(self.root_dir, '..')))
        zf.close()

        try:
            with open(zf_path, 'rb') as f:
                r = requests.post(self.server_url + '/logger/source-code/' + self.project_id + "/" + self.current_run_id,
                                  files={'file': f,},
                                  headers={"Authorization": "Bearer " + self.token}
                                )

                if (r.status_code != 200):
                    print("Error: " + r.json()['err'])

        except:
            print("Unknown error in upload_file.")
            print(sys.exc_info()[0])
            raise

        # removing the tmp zip file
        os.remove(zf_path)


    def add_project(self, name, project_type, description=""):
        """ 
        Adding project.
      
        Parameters: 
      
        Returns: 

        Project
      
        """    

        is_invalid_project_type = self.check_project_type(project_type)
        if (is_invalid_project_type):
            print ("Incorrect project type", project_type)
            return

        try:
            r = requests.post(
                self.server_url + "/logger/project",
                json={
                    'name': name,
                    'type': project_type,
                    'description': description,
                },
                headers={'Content-Type':'application/json', "Authorization": "Bearer " + self.token}
            )
            if (r.status_code != 200):
                print("Error: " + r.json()['err'])
            else:
                self.project_id = r.json()["data"]["id"]
                return self.project_id


        except:
            print("Unknown error in add_project.")
            print(sys.exc_info()[0])
            raise


    def upload_dataset(self, path_to_dataset, dataset_type_in="Train"):
        """ 
        Uploads dataset to server.
      
        Parameters: 
            path_to_dataset - path
            dataset_type_in - one of Train, Test, Validation
        Returns: 
            None
        """
        dataset_type = dataset_type_in.lower()
        is_invalid_dataset_type = self.check_dataset_type(dataset_type)
        if (is_invalid_dataset_type):
            print ("Incorrect dataset type", dataset_type_in)
            return 

        # making tmp zip file of the source dir and its subdirs, then posting is as logger_zip.zip
        zip_file_path = os.path.join(Path(path_to_dataset).parent, (dataset_type + ".zip"))
        zip_file = zipfile.ZipFile(zip_file_path, "w")

        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                zip_file.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path_to_dataset, '..')))
        zip_file.close()

        try:
            with open(zip_file_path, 'rb') as f:
                r = requests.post(self.server_url + "/logger/dataset/" + self.project_id + "/" + dataset_type,
                                  files={'zip_file': f,},
                                  headers={"Authorization": "Bearer " + self.token}
                                )

                if (r.status_code != 200):
                    print("Error: " + r.json()['err'])

        except:
            print("Unknown error in upload_file.")
            print(sys.exc_info()[0])
            raise

        # removing the tmp zip file
        os.remove(zip_file_path)



    # downloading dataset from server
    def download_dataset(self, path="", dataset_type_in="Train"):
        """ 
            Downloads dataset from server.
        
            Parameters: 
                path - path to dir, where to put downloaded file
                dataset_type_in - one of Train, Test, Validation
            Returns: 
                None
        """
        dataset_type = dataset_type_in.lower()
        is_invalid_dataset_type = self.check_dataset_type(dataset_type_in)
        if (is_invalid_dataset_type):
            print ("Incorrect dataset type", dataset_type_in)
            return 

        try:
        # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
        # see second answer
            file_name = os.path.join(path, "logger_zip.zip")

            url = self.server_url + "/logger/dataset/" + self.project_id + "/" + dataset_type
            headers = {'Content-Type':'application/json', "Authorization": "Bearer " + self.token, "responseType": "blob",}
            with requests.get(url, stream=True, headers=headers) as r:
                r.raise_for_status()
                with open(file_name, 'wb') as f:
                    # https://github.com/psf/requests/issues/2155#issuecomment-287628933
                    # r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    
        except:
            print("Failed to download file " + url)
            print("Unknown error in download_dataset.")


    # util
    def check_dataset_type(self, dataset_type_in):
        dataset_type = dataset_type_in.lower()
        allowed_dataset_types = {"train": True, "validation": True, "test": True}
        return dataset_type not in allowed_dataset_types


    def check_project_type(self, project_type):
        allowed_project_types = {
                                    "ImageClassification": True,
                                    "ImageCaptioning": True,
                                    "VideoTranscription": True,
                                    "AudioTranscription": True,
                                }

        return project_type not in allowed_project_types
