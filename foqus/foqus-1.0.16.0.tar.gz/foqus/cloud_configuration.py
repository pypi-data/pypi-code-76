from foqus.database import *
from azure.storage.blob import BlockBlobService, ContentSettings


import boto3
import pyarrow.parquet as pq
import s3fs
from io import BytesIO
import subprocess

db = PostgreSQL()


def upload_file(file_local_path, file_upload_s3=None, file_upload_azure=None, ext=None):
    if USE_AWS:
        '''
            :param file: file to upload to S3
            :param chemin: the location in which we will upload the file in S3
            :param ext: the extension of the file (if you wish to change when uploading)
            :return: Nothing to return
        '''

        s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_KEY)
        fichier = file_local_path.split('/')[-1]
        if ext is None:
            file_to_upload = file_upload_s3 + fichier
        else:
            file_to_upload = file_upload_s3 + fichier + "." + ext
        try:
            logger.info('Uploading file into %s' % file_to_upload)
            data = open(file_local_path, 'rb')
            s3.Bucket('trynfit-bucket').put_object(Key=file_to_upload, Body=data)
        except Exception as e:
            logger.error('Error in uploading file %s' % e)
        return AWS_S3_CUSTOM_DOMAIN + AWS_STORAGE_BUCKET_NAME + '/' + file_to_upload
    else:
        '''
        :param
        file_upload_path: file azure blob  path
        :param file_local_path: file local pzth
        :return: Nothing
        '''
        block_blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                              account_key=AZURE_ACCOUNT_KEY)
        # Upload a blob into a container
        try:
            block_blob_service.create_blob_from_path(
                AZURE_CONTAINER_NAME,
                file_upload_azure,
                file_local_path,
                content_settings=ContentSettings(content_type='file')
            )
            logger.info('uploading file %s with success ' % file_local_path)
        except Exception as e:
            logger.error('Exception in uploading file in azure storage :' + str(e))
        return AZURE_CUSTOM_DOMAIN_BLOB +AZURE_CONTAINER_NAME +'/'+file_upload_azure


def list_files(prefix_s3=None, prefix_azure=None):
    parquet_files = []
    if USE_AWS:
        '''
        :param prefix: the prefix of the diretcory to list the file into
        :return: list of the objects in the directory
        '''
        s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_KEY)
        try:
            paginator = s3.meta.client.get_paginator('list_objects')
            pages = paginator.paginate(Bucket=AWS_STORAGE_BUCKET_NAME, Prefix=prefix_s3)
            for page in pages:
                for key in page['Contents']:
                    parquet_files.append(key['Key'])
            return parquet_files
        except Exception as e:
            logger.warning("No files in %s %s" % (prefix_s3, e))
    else:

        '''
            :return: list of parquets file
            '''
        block_blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                              account_key=AZURE_ACCOUNT_KEY)
        generator = block_blob_service.list_blobs(AZURE_CONTAINER_NAME)
        files = []
        try:
            for blob in generator:
                if prefix_azure in blob.name:
                    files.append(blob.name)
        except Exception as e:
            logger.error("Exception in listing parquet files ..." + str(e))
        return files


def load_file_from_url(url_s3=None, url_azure=None):
    if USE_AWS:
        '''
        :param url: url of the file to load
        :return: return vector if file exist else None
        '''
        s3 = s3fs.S3FileSystem(key=AWS_KEY_ID, secret=AWS_SECRET_KEY)
        try:
            vector = pq.ParquetDataset('s3://%s'
                                       % (AWS_STORAGE_BUCKET_NAME + '/' + url_s3),
                                       filesystem=s3).read_pandas().to_pandas()
            return vector
        except Exception as e:
            logger.warning('%s file not loaded %s ' % (url_s3, e))
            return None
    else:
        '''
            :param parquet_file: path of parquet file to load from MS azure blob
            :return: the vector data if exist else None
            '''
        byte_stream = BytesIO()
        block_blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                              account_key=AZURE_ACCOUNT_KEY)
        try:
            block_blob_service.get_blob_to_stream(container_name=AZURE_CONTAINER_NAME, blob_name=url_azure,
                                                  stream=byte_stream)
            df = pq.read_table(source=byte_stream).to_pandas()
        except Exception as e:
            df = None
            # Add finally block to ensure closure of the stream
            byte_stream.close()
            logger.error("exception in loading parquet file ..." + str(e))
        return df


def load_vectors(vectors, users=None):
    if USE_AWS:
        '''
        :param vectors: dict with vectors names and values initialised to empty dict
        :param users: list of all users in database
        :return: json with all vectors with values
        '''
        for user in users:
            vector_path = VECTORS_S3 + str(user[8]) + '/' + str(user[1]) + '/'
            try:
                vectors_client = list_files(vector_path)
                for vector in vectors_client:
                    try:
                        vector_name = vector.split('.parquet')[0].split('/')[-1]
                        if vector_name:
                            project_name = vector_name.split('_' + user[1])[0]
                            status = db.get_status_project(STATUS_PROJECT_TABLE, user[1], user[8], 'similars',
                                                           project_name)
                            if status and status[0] == 2:
                                if vector_name not in vectors.keys():
                                    # logger.info(
                                    #     'Vector to load  =====> %s' % (vector.split('.parquet')[0] + '.parquet'))
                                    vector_data = load_file_from_url(vector.split('.parquet')[0] + '.parquet')
                                    if vector_data is not None:
                                        vectors[vector_name] = vector_data
                                        # logger.info('Vector %s  loaded successfully for client %s '
                                        #             % (vector_name, str(user[1])))
                                    # else:
                                    #     logger.info(
                                    #         'Vector %s not loaded for client %s vector is None'
                                    #         % (vector.split('.parquet')[0].split('/')[-1], str(user[1])))
                            else:
                                # logger.info('Status Project not 2 %s %s' % (project_name, status))
                                continue
                    except Exception as e:
                        logger.warning("Vector not loaded %s error %s" % (vector, e))
            except Exception as e:
                logger.warning("Can't get the parquet file for client %s with domaine %s error %s"
                               % (str(user[1]), str(user[8]), e))
        # logger.info("Vectors keys : %s" % vectors.keys())
        return vectors
    else:
        '''
            :param vectors: dict with vectors names and values initialised to empty dict
            :return: json with all vectors with values
        '''
        parquet_files = []
        block_blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                              account_key=AZURE_ACCOUNT_KEY)
        generator = block_blob_service.list_blobs(AZURE_CONTAINER_NAME)
        try:
            for blob in generator:
                if blob.name.endswith('.parquet') and AZURE_VECTORS_PATH in blob.name:
                    try:
                        project = blob.name.split('/')[-3]
                        customer_name = blob.name.split('/')[-4]
                        customer_type = blob.name.split('/')[-5]
                        status = db.get_status_project(STATUS_PROJECT_TABLE, customer_name, customer_type,
                                                       'similars', project)
                        if status and status[0] == 2:
                            parquet_files.append(blob.name)
                        else:
                            # logger.info('Status Project not 2 %s %s' % (project, status))
                            continue
                    except Exception as e:
                        continue
                        # logger.info("Vector not loaded %s" % e)

        except Exception as e:
            logger.error("Exception in listing parquet files ..." + str(e))
        parquet_files = list_files()
        for p in parquet_files:
            # logger.info('Parquet to load ===> %s' % p)
            vector_key = (p.split('/part')[0]).split('/')[-1].split('.parquet')[0]
            vector_data = load_file_from_url(p)
            if vector_data is not None:
                vectors[vector_key] = vector_data
                # logger.info('Parquet %s  loaded successfully' % vector_key)
            # else:
            #     logger.info('Parquet %s not loaded' % vector_key)
        # logger.info("Vectors keys : %s" % vectors.keys())
        return vectors


def delete_folder(prefix_to_delete):

    '''
    :param prefix_to_delete: prefix of the directory to delete
    :return: Nothing to return
    '''

    s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_KEY)
    delete_keys = {}
    try:
        objects_to_delete = s3.meta.client.list_objects(Bucket="trynfit-bucket", Prefix=prefix_to_delete)
        delete_keys['Objects'] = [{'Key': k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]

        s3.meta.client.delete_objects(Bucket="trynfit-bucket", Delete=delete_keys)
        # logger.info("Directory deleted successfully %s" % prefix_to_delete)
    except Exception as e:
        logger.error("Error deleting directory %s error is %s" % (prefix_to_delete, e))


def move_directory(source=None, new_destination=None, prefix=None, directory=None):
    if USE_AWS:
        '''
            :param prefix: prefix of the directory to move
            :param directory: the new directory name to move to
            :return: True if the move completed else False
            '''
        s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_KEY)
        try:
            files = list_files(prefix)
            for file in files:
                copy_source = {'Bucket': 'trynfit-bucket', 'Key': file}
                s3.meta.client.copy(copy_source, 'trynfit-bucket', file.replace('workspace', directory))
            delete_folder(prefix)
            return True
        except Exception as e:
            logger.error("Errorororor move_directory AWS %s" % e)
            return False
    else:
        SAS = AZURE_SAS
        # logger.info("moving blobs from original folder: " + str(source) +
        #             " to recovery folder on the same azure container: " + str(new_destination))
        try:
            comm = 'sudo azcopy cp "' + source + '?' + SAS + '" ' + '"' + new_destination + '?' + SAS + \
                   '" --recursive=true --overwrite=ifSourceNewer'
            process = subprocess.Popen([comm],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True)
            process.communicate()

            supp = 'sudo azcopy rm "' + source + '?' + SAS + '" --recursive=true'
            process = subprocess.Popen([supp],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True)
            process.communicate()
        except Exception as e:
            logger.error("Azure_moving_directory error %s " % e)