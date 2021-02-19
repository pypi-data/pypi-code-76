
from __future__ import print_functione
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import io
import numpy as np
import pickle


class gdrive(object):

    def __init__(self):

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/drive-python-quickstart.json
        self.SCOPES = 'https://www.googleapis.com/auth/drive'
        self.CLIENT_SECRET_FILE = 'credentials.json'
        self.APPLICATION_NAME = 'pysmm'
        self.CLIENT_ID = ' 953901556634-sllldoe5aaoeg0arom97llbbdlcu2fsc.apps.googleusercontent.com '

        self._init_connection()

    def _get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('./pysmm/token.pickle'):
            with open('./pysmm/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './pysmm/credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('./pysmm/token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def _init_connection(self):
        credentials = self._get_credentials()
        self.service = build('drive', 'v3', credentials=credentials)

    def print_file_list(self):
        results = self.service.files().list(
            pageSize=30, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))

    def get_id(self, filename):

        # get list of files
        results = self.service.files().list(
            pageSize=50, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        # extract list of names and id and find the wanted file
        namelist = np.array([items[i]['name'] for i in range(len(items))])
        idlist = np.array([items[i]['id'] for i in range(len(items))])
        file_pos = np.where(namelist == filename)

        if len(file_pos[0]) == 0:
            return(0, filename + ' not found')
        else:
            return(1, idlist[file_pos])

    def download_file(self, filename, localpath):
        # get file id
        success, fId = self.get_id(filename)

        if success == 0:
            print(filename + ' not found')
            return

        request = self.service.files().get_media(fileId=fId[0])
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print('Download %d%%.' % int(status.progress() * 100))

        fo = open(localpath, 'wb')
        fo.write(fh.getvalue())
        fo.close()

    def delete_file(self, filename):
        # get file id
        success, fId = self.get_id(filename)

        if success == 0:
            print(filename + ' not found')

        self.service.files().delete(fileId=fId[0]).execute()

    # def close(self):
    #     self.service.close()