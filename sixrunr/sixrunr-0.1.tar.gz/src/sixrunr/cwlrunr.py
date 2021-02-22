import yaml
import os
import paramiko
import shlex
import subprocess,time
import uuid

from .utils import *

def run_cwl(ssh, local_cwl, local_yml):
    """
    通过vagrant内的docker运行cwl文件
    """


    # 建立远程临时目录
    tmpdir = '/'.join(['/sixoclock_data', 'tmp-{}'.format(str(uuid.uuid1()))]) # 远程目录
    ha.execute_cmd('mkdir {}'.format(tmpdir))

    remote_cwl='/'.join([tmpdir, os.path.basename(local_cwl)])
    remote_yml='/'.join([tmpdir, os.path.basename(local_yml)])
    ssh.put(local_cwl, remote_cwl)

    # 解析并处理yml文件，替换文件路径为客户端临时路径
    ryml = yaml2dict(local_yml)
    for key in ryml:
        
        if isinstance(ryml[key],dict) and 'class' in ryml[key] and ryml[key]['class']=='File':

            src = ryml[key]['path']
            dst = '/'.join([tmpdir, winpath_adjust(ryml[key]['path']).strip('/')] )
            # 将输入文件上传至客户机
            ssh.put(src, dst)
            ryml[key]['path']= dst
    # 写入新的yml到客户机
    ssh.execute_cmd('echo \'{}\' > {}'.format(yaml.dump(ryml), remote_yml))
    # 发送命令，运行cwl流程
    cmd='cd {}; cwltool {} {}'.format(tmpdir, remote_cwl, remote_yml)
    res = ssh.execute_cmd(cmd)
    cwl_res = json.loads(res)
    # 复制结果至本地机
    for file in parse_cwlres(cwl_res):
        ssh.get(file, os.path.join(os.getcwd(),'T', file[len(tmpdir)+1:]))
        print(os.path.join(os.getcwd(), file[len(tmpdir)+1:]))
    ssh.execute_cmd('rm -rf {}'.format(tmpdir)) # 删除临时目录
    print(res)