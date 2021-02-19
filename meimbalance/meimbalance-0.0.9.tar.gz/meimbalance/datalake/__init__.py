# Will do the following when included:
#   - Load environment variables
#   - Get Azure credentials
#   - Define constants for the datalakes
#
import os
import tempfile
from azure.identity._credentials.managed_identity import ManagedIdentityCredential
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.datalake.store import core, lib, multithread
from pathlib import Path
import logging
import pandas as pd

# Superclass for both generations of Datalakes
class Datalake:
    def __init__(self, datalake_name):
        self.datalake_name = datalake_name
    

# Class to handle Gen2 Datalakes
class DatalakeGen2(Datalake):
    def __init__(self,datalake_name, azure_credential):
            self.azure_credential = azure_credential
            self.container_name = 'root'
            super().__init__(datalake_name)

    # Get a service client
    def __get_service_client(self):
        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", self.datalake_name), credential=self.azure_credential)
        return service_client

    # Get a file system client for the given root
    def __get_file_system_client(self):
        service_client = self.__get_service_client()
        file_system_client = service_client.get_file_system_client(file_system=self.container_name)
        return file_system_client

    # Get a directory client for the given directory_name
    def __get_directory_client(self, directory_name):
        file_system_client = self.__get_file_system_client()
        try:
            directory_client = file_system_client.get_directory_client(directory=directory_name)
        except Exception as e:
            print('Error in getting directory client for ', directory_name, ': ', e)
            return None

        return directory_client

    # Get a file client for the given directory and file name
    def __get_file_client(self, directory_name, filename):
        directory_client = self.__get_directory_client(directory_name)
        file_client = directory_client.get_file_client(filename)
        return file_client

    # Helper function to download a file
    def __download_file(self, directory_name, filename, file):
        file_client = self.__get_file_client(directory_name, filename)
        download = file_client.download_file()
        downloaded_bytes = download.readall()
        file.write(downloaded_bytes)
        file.seek(0,0)
        return

    # Helper function to check if a file exists
    def __check_if_file_exists(self, directory_name, filename):
        if directory_name == '/':
            file_path = filename
        else:
            file_path = directory_name[1:] + '/' + filename
        file_system_client = self.__get_file_system_client()
        paths = file_system_client.get_paths(path=directory_name, recursive=False)
        for path in paths:
            if file_path == path.name:
                return True
        
        return False

    # List content of a directory
    def list_files_in_directory(self, directory_name):
        file_system_client = self.__get_file_system_client()
        files = []
        paths = file_system_client.get_paths(path=directory_name, recursive=False)
        for path in paths:
            directory_name, filename = os.path.split(path.name)
            files.append(filename)
        return files

    # Get newest file in directory
    def get_latest_file_in_directory(self, directory_name):
        files_df = self.list_files_attributes_in_directory(directory_name=directory_name)
        count = len(files_df)
        if count == 0:
            return None

        files_df.sort_values(by=['last_modified','filename'],ascending=False, inplace=True)
        file_df = files_df[['filename']].head(1)
        filename = file_df.iloc[0]['filename']
        return filename

    # Get Dataframe with directory listing
    def list_files_attributes_in_directory(self, directory_name):
        file_system_client = self.__get_file_system_client()
        names = []
        etags = []
        deleteds = []
        metadatas = []
        last_modifieds = []
        creation_times = []
        sizes = []
        paths = file_system_client.get_paths(path=directory_name, recursive=False)

        count = 0
        for path in paths:

            directory_name, filename = os.path.split(path.name)
            file_client = self.__get_file_client(directory_name, filename)
            properties = file_client.get_file_properties()

            if  not(('hdi_isfolder') in properties.metadata and properties.metadata['hdi_isfolder'] == 'true'):
                count = count + 1
                names.append(filename)
                etags.append(properties.etag)
                deleteds.append(properties.deleted)
                metadatas.append(properties.metadata)
                last_modifieds.append(properties.last_modified)
                creation_times.append(properties.creation_time)
                sizes.append(properties.size)

        data = {'filename':names, 'etag': etags, 'deleted': deleteds, 'metadata': metadatas, 'last_modified': last_modifieds, 'creation_time': creation_times, 'size': sizes}
        dataframe = pd.DataFrame(data=data)
        return dataframe


    # Download a file from the datalake, write it to a local temporary file, and open the file for processing
    def open_file(self, directory_name, filename): 
        localfile=tempfile.TemporaryFile()
        self.__download_file(directory_name, filename, localfile)
        localfile.seek(0,0)
        return localfile

    # Download a file from the datalake, write it to a local temporary file, and open the file for processing
    def open_text_file(self, directory_name, filename): 
        file_client = self.__get_file_client(directory_name, filename)
        download = file_client.download_file()
        downloaded_text = download.readall()
        localfile=tempfile.TemporaryFile(mode='a+t')
        localfile.writelines(downloaded_text)
        localfile.seek(0,0)
        return localfile

    # Upload a local file to a new file in the Datalake
    def upload_file(self, file, directory_name, filename, overwrite=False):
        file.seek(0,0)
        file_contents = file.read()
        directory_client = self.__get_directory_client(directory_name)
        
        # Check if file already exist in the lake if Owerwrite is False
        if overwrite == False:
            if self.__check_if_file_exists(directory_name=directory_name, filename=filename):
                logging.error('File ' + filename + ' already exists in directory ' + directory_name)
                return

        directory_client.create_file(file=filename)
        file_client = directory_client.get_file_client(filename)
        file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
        file_client.flush_data(len(file_contents))

    # Upload a local named file to the datalake
    def upload_local_file(self, local_filepath, directory_name, filename, overwrite=False):
        file=open(local_filepath,"r")
        self.upload_file(file, directory_name, filename, overwrite=overwrite)
        file.close()

        # Download a file to a local filesystem
    def download_to_local_file(self, directory_name, filename, local_filepath):
        file=open(local_filepath, "wb")
        self.__download_file(directory_name, filename, file)
        file.close()
        pass    

    

# Class to handle Gen1 Datalakes
class DatalakeGen1(Datalake):
    def __init__(self,datalake_name, token):
        self.token = token
        super().__init__(datalake_name)

    # Helper function to download a file from the datalake
    def __download_file(self, directory_name, filename, file):
        filepath=directory_name+filename
        adlFileSystem = core.AzureDLFileSystem(self.token, store_name=self.datalake_name)
        with adlFileSystem.open(filepath, 'rb') as f:
            downloaded_bytes = f.read()
            file.write(downloaded_bytes)
            file.seek(0,0)
    
    # Download a file from the datalake, write it to a local temporary file, and open the file for processing
    def open_file(self, directory_name, filename):
        localfile=tempfile.TemporaryFile()
        self.__download_file(directory_name=directory_name, filename=filename, file=localfile)
        return localfile

    # Download a file to a local filesystem
    def download_to_local_file(self, directory_name, filename, local_filepath):
        file=open(local_filepath, "w")
        self.__download_file(directory_name, filename, file)
        file.close()
        pass  


    # Old code
    def old_open_file(self, directory_name, filename):
        filepath=directory_name+filename

        adlFileSystem = core.AzureDLFileSystem(self.token, store_name=self.datalake_name)
        with adlFileSystem.open(filepath, 'rb') as f:
            downloaded_bytes = f.read()
            localfile=tempfile.TemporaryFile()
            localfile.write(downloaded_bytes)
            localfile.seek(0,0)
            return localfile


# Helper class to initialize instances for the 3 datalakes in use in the project and 
# get Azure Credentials and token
class ImbalanceDatalakes:
    def __init__(self):
        self.__check_for_multiple_env()
        print('Loading .env...')
        load_dotenv(verbose=True, override=True)
        print('Reading environment variables....')
        try:
            self.imbalance_datalake_name=os.environ['IMBALANCE_DATALAKE_NAME']
            print('IMBALANCE_DATALAKE_NAME: ' + self.imbalance_datalake_name)
            self.shared_datalake_gen2_name=os.environ['SHARED_DATALAKE_GEN2_NAME']
            print('SHARED_DATALAKE_GEN2_NAME: ' + self.shared_datalake_gen2_name)
            self.shared_datalake_gen1_name=os.environ['SHARED_DATALAKE_GEN1_NAME']
            print('SHARED_DATALAKE_GEN1_NAME: ', self.shared_datalake_gen1_name)
            self.azure_tenant_id=os.environ['AZURE_TENANT_ID']
            print('TENANT_ID: ' + self.azure_tenant_id)
            self.azure_client_id=os.environ['AZURE_CLIENT_ID']
            print('AZURE_CLIENT_ID: ', self.azure_client_id)
            self.azure_client_secret=os.environ['AZURE_CLIENT_SECRET']
            print('AZURE_CLIENT_SECRET: ', self.azure_client_secret)
        except:
            print('ERROR: Missing environment variables, need to declare IMBALANCE_DATALAKE_NAME, SHARED_DATALAKE_GEN2_NAME and SHARED_DATALAKE_GEN1_NAME')
            print('Hint: Put these variables in the .env file in the project root, and create a source statement in ~/.bashrc:')
            print('if [ -f ~/source/Imbalance/.env ]; then')
            print('    source ~/source/Imbalance/.env')
            print('fi')
            exit(1)
        
        print('Getting Default Azure Credentials...')
        self.azure_credential = DefaultAzureCredential()

        print('Getting token...')
        token = lib.auth(tenant_id = self.azure_tenant_id, client_id = self.azure_client_id, client_secret = self.azure_client_secret)

        self.imbalance_datalake = DatalakeGen2(self.imbalance_datalake_name, self.azure_credential)
        self.shared_datalake_gen2 = DatalakeGen2(self.shared_datalake_gen2_name, self.azure_credential)
        self.shared_datalake_gen1 = DatalakeGen1(self.shared_datalake_gen1_name, token)

    def __check_for_multiple_env(self):
        print('Checking for .env in ' + str(Path.home()))
        results = self.__find_all__(name='.env', path=str(Path.home()))
        if len(results) > 1:
            print('Warning: Multiple .env found: ' + str(len(results)))
            for result in results:
                print('  ' + result)


    def __find_all__(self, name, path):
        result = []
        for root, dirs, files in os.walk(path):
            if name in files:
                if 'pythonFiles' not in root:
                    result.append(os.path.join(root, name))
        return result