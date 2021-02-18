# coding=utf8
# Copyright 2020 Cognicept Systems
# Author: Swarooph Seshadri (swarooph@cognicept.systems)
# --> Pusher class handles pushing stuff to the Cognicept cloud

from dotenv import dotenv_values
from pathlib import Path
import os
import sys
import time
import glob
import requests
import datetime
import threading
import ntpath
import logging
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from cogniceptshell.common import bcolors


class ProgressPercentage(object):
    """
    Track upload progress for chunks uploaded to S3
    ...

    Parameters
    ----------
    TODO

    Methods
    -------
    TODO
    """

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


class Pusher:
    """
    TODO
    ...

    Parameters
    ----------
    TODO

    Methods
    -------
    TODO
    """
    def __init__(self):
        self.bucket_name = 'cognicept-bagfiles'

    def push(self, args):
        """
        Main push entry point
        """
        if args.bag:
            # Construct client
            self.construct_client(args.config)
            # Push bag
            self.push_bag(args)
        else:
            # start or stop must be provided
            print(
                bcolors.FAIL + "Required command is missing." + bcolors.ENDC)

    def construct_client(self, config_obj):
        """
        Utility function to create S3 client based on runtime.env credentials
        """
        local_cfg = config_obj.config

        if 'AWS_SESSION_TOKEN' in local_cfg:
            self.s3_client = boto3.client(
                's3', region_name='ap-southeast-1',
                aws_access_key_id=local_cfg['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=local_cfg['AWS_SECRET_ACCESS_KEY'],
                aws_session_token=local_cfg['AWS_SESSION_TOKEN'])
        else:
            self.s3_client = boto3.client(
                's3', region_name='ap-southeast-1',
                aws_access_key_id=local_cfg['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=local_cfg['AWS_SECRET_ACCESS_KEY'])

    def push_bag(self, args):
        """
        Push bag to S3 and bag metadata to Cognicept cloud
        """
        upload_status = False
        if args.bag == 'latest':
            bag_file_path = self.get_latest_bag(args)
            print(
                bcolors.OKBLUE +
                "Uploading latest bag file to S3: " +
                bcolors.ENDC + bag_file_path)
            upload_status = self.upload_s3(bag_file_path, args.config)
        elif args.bag.endswith('.bag'):
            bag_file_path = os.path.expanduser(args.path+"bags/"+args.bag)
            if(self.check_bag_exists(bag_file_path)):
                print(
                    bcolors.OKBLUE +
                    "Uploading bag file to S3: " +
                    bcolors.ENDC + bag_file_path)
                upload_status = self.upload_s3(bag_file_path, args.config)
            else:
                print(
                    bcolors.FAIL +
                    "Specified bag file not found in expected location: " +
                    bcolors.ENDC + bag_file_path)
        else:
            print(
                bcolors.FAIL + "Only .bag files can be uploaded." + bcolors.ENDC)

        if upload_status:
            print(bcolors.OKGREEN + "\nBag file uploaded." + bcolors.ENDC)
            self.post_bag_metadata(args, bag_file_path)
        else:
            pass

    def get_latest_bag(self, args):
        """
        Get path of the latest bag file
        """
        bag_path = os.path.expanduser(args.path+"bags")
        bag_list = glob.glob(bag_path+"/*.bag")
        if bag_list:
            latest_file = max(bag_list, key=os.path.getctime)
            return latest_file
        else:
            print(
                bcolors.FAIL + "No bags found in the expected path." + bcolors.ENDC)
            raise(SystemExit)

    def check_bag_exists(self, bag_file_path):
        """
        Check if rosbag exists
        """
        if (os.path.exists(bag_file_path)):
            return True
        else:
            return False

    def upload_s3(self, bag_file_path, config_obj):
        """
        Upload rosbag to S3
        """
        # Multipart threaded approach for larger files
        config = TransferConfig(multipart_threshold=1024*25, max_concurrency=10,
                                multipart_chunksize=1024*25, use_threads=True)
        num_retries = 3

        for trial in range(num_retries):
            try:
                # Upload file
                file_name = ntpath.basename(bag_file_path)
                self.s3_client.upload_file(bag_file_path, self.bucket_name, file_name,
                                           Config=config, Callback=ProgressPercentage(bag_file_path))
                # Return true for successful upload
                return True
            except boto3.exceptions.S3UploadFailedError:
                # On failure, retry
                print('Attempt #' + str(trial+1) + bcolors.FAIL +
                      " FAILED" + bcolors.ENDC + "\033[K")
                # Wait for 1 second before retrying
                time.sleep(1.0)
        # If the loop is completed, upload failed, so return false
        return False

    def post_bag_metadata(self, args, bag_file_path):
        """
        Post bag metadata to Cognicept cloud
        """
        payload = {
            "robot_id": args.config.get_field("ROBOT_CODE"),
            "bagfile_name": ntpath.basename(bag_file_path),
            "bagfile_url": ntpath.basename(bag_file_path),
            "bagfile_size": str(os.path.getsize(bag_file_path)),
            "uploaded_at": datetime.datetime.now().isoformat()
        }

        # retrieve cognicept access key
        try:
            token = args.config.get_field("COGNICEPT_ACCESS_KEY")
        except KeyError:
            print(bcolors.FAIL +
                  'COGNICEPT_ACCESS_KEY variable undefined in configuration. Could not update Cognicept cloud with bag metadata.' +
                  bcolors.ENDC)
            raise(SystemExit)

        headers = {"Authorization": "Basic " + token}

        try:
            resp = requests.post(args.config.get_cognicept_api_uri(
            ) + "bagfile", headers=headers, json=payload, timeout=5)

            if resp.status_code != 200:
                print(
                    'Cognicept REST API error: ' +
                    args.config.get_cognicept_api_uri() +
                    ' responded with ' + str(resp.status_code) +
                    '\n' + resp.json()['Message'])
                return False
            else:
                print(
                    bcolors.OKGREEN +
                    "Metadata posted to Cognicept Cloud." +
                    bcolors.ENDC)
        except requests.exceptions.Timeout:
            print("Cognicept REST API error: time out.")
            return False
        except requests.exceptions.TooManyRedirects:
            print("Cognicept REST API error: Wrong endpoint.")
            return False
        except Exception as ex:
            print("Cognicept REST API error, " + str(ex))
            return False
