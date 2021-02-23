from .client import Client

import socket
from typing import Optional
from random import randint

from .result import Result
from .job import Job
from .param import Param
from .const import ParamTypes
from .result_file import ResultFile, ResultFileType
from .tcp_client_classes.job_caller import JobCaller


class TcpClient(Client):
    @staticmethod
    def encrypt_password(password:str) -> str:
        if password == None or password == '':
            raise(ValueError('Password must not be empty'))
        
        create_random_char = lambda: chr(ord('0') + (randint(0, 32000) % 8))

        plen = len(password)
        nmax = 4 * plen * 2
        ioff = randint(0, 32000) % max(1, nmax - plen * 3 - 3)
        cryptid = chr(ord('A') + plen) + chr(ord('A') + ioff)
        for _ in range(0, ioff):
            cryptid += create_random_char()

        replace_in_string = lambda i, c: cryptid[:i] + c + cryptid[i + 1:]

        for i in range(0, plen):
            j = 2 + ioff + i * 3
            oct_part = ioff + ord(password[i])
            oct = f'{oct_part:03o}'
            for k in range(0, 3):
                cryptid = replace_in_string(j+k, oct[k])

        for i in range(2 + ioff + 3 * plen, nmax):
            cryptid = replace_in_string(i, create_random_char())

        return cryptid
    

    def __attach__(self, username:str, password:str):
            session_attach_job = Job('krn.SessionAttach', Flags=0, SessionGUID='')
            session_attach_result = self.execute(session_attach_job)
            self.session_guid = session_attach_result.values['SessionGUID']

            session_properties_set_job = Job(
                'krn.SessionPropertiesSet', 
                Flags=0, 
                Properties='instname;statname;address', 
                address=f'{socket.gethostbyname(socket.gethostname())}=dummy',
                instname=self.appname,
                statname=socket.gethostname()
            )
            session_properties_set_result = self.execute(session_properties_set_job)

            session_login_job = Job(
                'krn.SessionLogin', 
                Flags=0, 
                UserName=username, 
                UserPwd=TcpClient.encrypt_password(password)
            )
            session_login_result = self.execute(session_login_job)

            if session_login_result.values['Description'] != None and session_login_result.values['Description'] != '':
                raise RuntimeError(f'Login error: {session_login_result.values["Description"]}')


    def __init__(self, hostname:str, port:int, appname:str, username:str, password:str, use_ssl:Optional[bool]=True, file_cache_byte_limit:Optional[int]=33554432):
        self.hostname = hostname
        self.port = port
        self.appname = appname
        self.username = username
        self.file_cache_byte_limit = file_cache_byte_limit
        self.job_caller = JobCaller(hostname, port, use_ssl, file_cache_byte_limit)
        self.__attach__(username, password)
        
    def __del__(self): 
        try:
            self.job_caller.socket.close()
        except:
            pass

    def execute(self, job:Job) -> Result:
        """Send a job to the blue server (via TCP), execute it and return the response.

        Keyword arguments:
        job -- A previously created Job() object.
        """
        return self.job_caller.execute(job)
        