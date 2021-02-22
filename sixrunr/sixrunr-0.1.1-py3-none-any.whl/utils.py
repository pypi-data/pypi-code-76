import yaml
import os
import paramiko
import shlex
import subprocess,time
import uuid
import stat
import traceback

def subprocess_read(p):
    """
    读取 subprocess 返回结果
    """
    
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.strip()
        if line:
            print(line.decode('utf-8'))
    if p.returncode == 0:
        print('命令运行成功')
    else:
        print('命令运行失败')

def sshconfig_read(p):
    """
    读取 ssh-config信息，返回字典类型
    """
    
    v_dict = {}
    while p.poll() is None:
        line = p.stdout.readline().strip()
        if line:
            values = line.strip().decode('utf-8').split(' ')
            v_dict[values[0]]=values[1]

    return  v_dict

def yaml2dict(yaml_file):
    """
    yaml 转dict
    """
    with open(yaml_file, 'r', encoding="utf-8") as f:
        return yaml.load(f.read())

# import platform
def winpath_adjust(path: str) -> str:
    r"""
    Adjust only windows paths for Docker.
    The docker run command treats them as unix paths.
    Example: 'C:\Users\foo to /C/Users/foo (Docker for Windows) or /c/Users/foo
    (Docker toolbox).
    """
    if onWindows():
        split = path.split(":")
        if len(split) == 2:
#             if platform.win32_ver()[0] in ("7", "8"):
#                 # Docker toolbox uses lowecase windows Drive letters
#                 split[0] = split[0].lower()
#             else:
            split[0] = split[0].capitalize()
                # Docker for Windows uses uppercase windows Drive letters
            path = ":".join(split)
        path = path.replace(":", "").replace("\\", "/")
        return path if path[0] == "/" else "/" + path
    return path

def winpath_reverse(path: str) -> str:
    r"""
    Change docker path (only on windows os) appropriately back to Windows path.
    Example:  /C/Users/foo to C:\Users\foo
    """
    if path is not None and onWindows():
        if path[0] == "/":
            path = path[1:]
        else:
            raise ValueError("not a docker path")
        splitpath = path.split("/")
        splitpath[0] = splitpath[0] + ":"
        return "\\".join(splitpath)
    return path

def onWindows() -> bool:
    """Check if we are on Windows OS."""
    return os.name == "nt"

def parse_cwlres(cwl_res):
    """
    解析cwltool返回结果，并做路径替换
    """
    lcwl_res = cwl_res
    Files = []
    try:
        if isinstance(cwl_res, dict):
            for key in cwl_res:
                if isinstance(cwl_res[key], dict):
                    if 'secondaryFiles' in cwl_res[key]:
                        for dic in cwl_res[key]['secondaryFiles']:
                            Files.append(dic['path'])
#                             dic['path'] = 
                    if 'class' in cwl_res[key] and cwl_res[key]['class']=='File':
                        Files.append(cwl_res[key]['path'])

    except:
        pass
    return Files                 

class Vagrant_ssh(object):
    """
    使用paramiko类实现ssh的连接登陆,以及远程文件的上传与下载, 基本远程命令的实现等
    """
    def __init__(self, sshconfig):
        self.host = sshconfig['HostName']
        self.port = int(sshconfig['Port'])
        self.username = sshconfig['User']
        self.pwd = '123456'
        self.pkey = paramiko.RSAKey.from_private_key_file(sshconfig['IdentityFile'])
        self.__k = None
        
        self.ssh = paramiko.SSHClient() # paramiko.SSHClient() 创建一个ssh对象，用于ssh登录以及执行操作
        self.sftp = paramiko.Transport(sock=(self.host, self.port)) # paramiko.Transport()创建一个文件传输对象，用于实现文件的传输


    def _key_connect(self):
        
        # 获取本地的私钥文件 一般是在 ~/.ssh/id_rsa
        # self.pkey = paramiko.RSAKey.from_private_key_file('~/.ssh/id_rsa', ) 
        # 获取本地的knows_hosts 文件，在不允许连接非kown_hosts文件中的主机时，使用它
        # self.ssh.load_system_host_keys() 
        # 允许连接非know_hosts文件中的主机
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.host, port=self.port, username=self.username, pkey=self.pkey)  # 建立登录连接
        self.sftp.connect(username=self.username, pkey=self.pkey) # 建立文件传输的连接

        
    def _password_connect(self):
        
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.host, port=self.port, username=self.username, password=self.pwd)
        self.sftp.connect(username=self.username, password=self.pwd)  # sptf 远程传输的连接
        
    def create_file(self):
        file_name = str(uuid.uuid4())
        with open(file_name,'w') as f:
            f.write('sb')
        return file_name

    def run(self):
        self.connect()
        self.upload()
        self.rename()
        self.close()

    def connect(self):
        """
        连接远程主机
        """
        try:
            self._key_connect()   # 密钥登录
        except:
            print('ssh key connect failed, trying to password connect...')
            try:
                self._password_connect()  # 密码登录
            except:
                print('ssh password connect faild!')


    def close(self):
        self.sftp.close()
        self.ssh.close()

    def put(self, local_path, remote_path):
        # 连接，上传
        sftp = paramiko.SFTPClient.from_transport(self.sftp)
        if not os.path.exists(os.path.dirname(remote_path)):
            self.execute_cmd('mkdir -p %s' % os.path.dirname(remote_path))
        sftp.put(local_path, remote_path)  
    
    def get(self, remote_path, local_path):
        # 连接，下载
        sftp = paramiko.SFTPClient.from_transport(self.sftp)
        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path))
        sftp.get(remote_path, local_path)   

    def execute_cmd(self, cmd):
        """
        执行命令
        """
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        result = stdout.read()
        if not result:
            result = stderr.read()

        return result.decode()
   
    def ls(self, sftp, remote_dir):
        """
        # 递归遍历远程服务器指定目录下的所有文件
        """
        all_files = list()
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        files = sftp.listdir_attr(remote_dir)
        for file in files:
            filename = remote_dir + '/' + file.filename

            if stat.S_ISDIR(file.st_mode):  # 如果是文件夹的话递归处理
                all_files.extend(self._get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files.append(filename)

        return all_files
    
    def lls(self, local_dir):
        """
        # 递归遍历本地服务器指定目录下的所有文件
        """
        all_files = list()

        for root, dirs, files in os.walk(local_dir, topdown=True):
            for file in files:
                filename = os.path.join(root, file)
                all_files.append(filename)

        return all_files

    def get_dir(self, remote_dir, local_dir):
        """
        下载文件夹
        """
        try:

            sftp = paramiko.SFTPClient.from_transport(self.sftp)

            all_files = self.ls(sftp, remote_dir)

            for file in all_files:

                local_filename = file.replace(remote_dir, local_dir)
                local_filepath = os.path.dirname(local_filename)

                if not os.path.exists(local_filepath):
                    os.makedirs(local_filepath)

                sftp.get(file, local_filename)
        except:
            print('ssh get dir from master failed.')
            print(traceback.format_exc())
            
    def put_dir(self, local_dir, remote_dir):
        """
        上传文件夹
        """
        try:
            sftp = paramiko.SFTPClient.from_transport(self.sftp)

            if remote_dir[-1] == "/":
                remote_dir = remote_dir[0:-1]

            all_files = self.lls(local_dir)
            for file in all_files:

                remote_filename = file.replace(local_dir, remote_dir).replace('\\', '/')
                remote_path = os.path.dirname(remote_filename)

                try:
                    sftp.stat(remote_path)
                except:
                    # os.popen('mkdir -p %s' % remote_path)
                    self.execute_cmd('mkdir -p %s' % remote_path) # 使用这个远程执行命令

                sftp.put(file, remote_filename)

        except:
            print('ssh get dir from master failed.')
            print(traceback.format_exc())
            