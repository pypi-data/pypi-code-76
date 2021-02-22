import os
EqPIR=object
EqPIY=None
EqPIK=Exception
EqPIx=set
EqPIn=property
EqPIz=classmethod
EqPIB=False
EqPIX=True
EqPIs=getattr
import re
import json
import logging
import yaml
import requests
from dulwich import porcelain
from dulwich.repo import Repo
from dulwich.client import get_transport_and_path_from_url
from localstack import config
from localstack.constants import API_ENDPOINT
from localstack.utils.common import(load_file,to_str,to_bytes,mkdir,save_file,cp_r,run,is_command_available,clone,retry,safe_requests,disk_usage)
from localstack_ext.utils import auth
LOG=logging.getLogger(__name__)
PERISTED_FOLDERS=['api_states','dynamodb','kinesis']
class CloudPodManager(EqPIR):
 BACKEND='_none_'
 CONFIG_FILE='.localstack.yml'
 def __init__(self,pod_name=EqPIY,config=EqPIY):
  self.pod_name=pod_name
  self.config=config
 def push(self):
  raise EqPIK('Not implemented')
 def pull(self):
  raise EqPIK('Not implemented')
 def get_pod_size(self):
  raise EqPIK('Not implemented')
 def restart_container(self):
  LOG.info('Restarting LocalStack instance with updated persistence state - this may take some time ...')
  data={'action':'restart'}
  url='%s/health'%config.get_edge_url()
  try:
   requests.post(url,data=json.dumps(data))
  except requests.exceptions.ConnectionError:
   pass
  def check_status():
   LOG.info('Waiting for LocalStack instance to be fully initialized ...')
   response=requests.get(url)
   content=json.loads(to_str(response.content))
   statuses=[v for k,v in content['services'].items()]
   assert EqPIx(statuses)==EqPIx(['running'])
  retry(check_status,sleep=3,retries=10)
 @EqPIn
 def pod_config(self):
  return self.config.get('pods',{}).get(self.pod_name)
 @EqPIz
 def get(cls,pod_name,config=EqPIY):
  config=config or CloudPodManager.load_config()
  pod_config=_pod_config(pod_name,config=config)
  backend=pod_config.get('backend')
  for clazz in cls.__subclasses__():
   if clazz.BACKEND==backend:
    return clazz(pod_name=pod_name,config=config)
  raise EqPIK('Unable to find Cloud Pod manager implementation type "%s"'%backend)
 @EqPIz
 def load_config(cls,safe=EqPIB):
  try:
   return yaml.load(to_str(load_file(cls.CONFIG_FILE)))
  except EqPIK:
   if safe:
    return{}
   raise EqPIK('Unable to find and parse config file "%s"'%cls.CONFIG_FILE)
 @EqPIz
 def data_dir(cls):
  if not config.DATA_DIR:
   try:
    details=run('%s inspect %s'%(config.DOCKER_CMD,config.MAIN_CONTAINER_NAME))
    details=json.loads(to_str(details))[0]
    mounts=details.get('Mounts')
    env=details.get('Config',{}).get('Env',[])
    data_dir_env=[e for e in env if e.startswith('DATA_DIR=')][0].partition('=')[2]
    data_dir_host=[m for m in mounts if m['Destination']==data_dir_env][0]['Source']
    data_dir_host=re.sub(r'^(/host_mnt)?',r'',data_dir_host)
    config.DATA_DIR=data_dir_host
   except EqPIK:
    LOG.warning('''Unable to determine DATA_DIR from LocalStack Docker container - please make sure $MAIN_CONTAINER_NAME is configured properly''')
  if not config.DATA_DIR:
   raise EqPIK('Working with local cloud pods requires $DATA_DIR configuration')
  return config.DATA_DIR
class CloudPodManagerGit(CloudPodManager):
 BACKEND='git'
 def push(self):
  repo=self.local_repo()
  client,path=self.client()
  branch=to_bytes(self.pod_config.get('branch'))
  remote_location=self.pod_config.get('url')
  try:
   porcelain.pull(repo,remote_location,refspecs=branch)
  except EqPIK as e:
   LOG.info('Unable to pull repo: %s'%e)
  is_empty_repo=b'HEAD' not in repo or repo.refs.allkeys()==EqPIx([b'HEAD'])
  if is_empty_repo:
   LOG.debug('Initializing empty repository %s'%self.clone_dir)
   init_file=os.path.join(self.clone_dir,'.init')
   save_file(init_file,'')
   porcelain.add(repo,init_file)
   porcelain.commit(repo,message='Initial commit')
  if branch not in repo:
   porcelain.branch_create(repo,branch,force=EqPIX)
  self.switch_branch(branch)
  for folder in PERISTED_FOLDERS:
   LOG.info('Copying persistence folder %s to local git repo %s'%(folder,self.clone_dir))
   src_folder=os.path.join(self.data_dir(),folder)
   tgt_folder=os.path.join(self.clone_dir,folder)
   cp_r(src_folder,tgt_folder)
   files=tgt_folder
   if os.path.isdir(files):
    files=[os.path.join(root,f)for root,_,files in os.walk(tgt_folder)for f in files]
   if files:
    porcelain.add(repo,files)
  porcelain.commit(repo,message='Update state')
  porcelain.push(repo,remote_location,branch)
 def pull(self):
  repo=self.local_repo()
  client,path=self.client()
  remote_refs=client.fetch(path,repo)
  branch=self.pod_config.get('branch')
  remote_ref=b'refs/heads/%s'%to_bytes(branch)
  if remote_ref not in remote_refs:
   raise EqPIK('Unable to find branch "%s" in remote git repo'%branch)
  remote_location=self.pod_config.get('url')
  self.switch_branch(branch)
  branch_ref=b'refs/heads/%s'%to_bytes(branch)
  from dulwich.errors import HangupException
  try:
   porcelain.pull(repo,remote_location,branch_ref)
  except HangupException:
   pass
  for folder in PERISTED_FOLDERS:
   src_folder=os.path.join(self.clone_dir,folder)
   tgt_folder=os.path.join(self.data_dir(),folder)
   cp_r(src_folder,tgt_folder)
  self.restart_container()
 def client(self):
  client,path=get_transport_and_path_from_url(self.pod_config.get('url'))
  return client,path
 def local_repo(self):
  self.clone_dir=EqPIs(self,'clone_dir',EqPIY)
  if not self.clone_dir:
   pod_dir_name=re.sub(r'(\s|/)+','',self.pod_name)
   self.clone_dir=os.path.join(config.TMP_FOLDER,'pods',pod_dir_name,'repo')
   mkdir(self.clone_dir)
   if not os.path.exists(os.path.join(self.clone_dir,'.git')):
    porcelain.clone(self.pod_config.get('url'),self.clone_dir)
  return Repo(self.clone_dir)
 def switch_branch(self,branch):
  repo=self.local_repo()
  if is_command_available('git'):
   return run('cd %s; git checkout %s'%(self.clone_dir,to_str(branch)))
  branch_ref=b'refs/heads/%s'%to_bytes(branch)
  if branch_ref not in repo.refs:
   branch_ref=b'refs/remotes/origin/%s'%to_bytes(branch)
  repo.reset_index(repo[branch_ref].tree)
  repo.refs.set_symbolic_ref(b'HEAD',branch_ref)
 def get_pod_size(self):
  self.local_repo()
  return disk_usage(self.clone_dir)
def push_state(pod_name,args):
 backend=CloudPodManager.get(pod_name=pod_name)
 pod_config=clone(backend.pod_config)
 pod_config['size']=backend.get_pod_size()
 store_pod_metadata(pod_name,pod_config)
 backend.push()
def pull_state(pod_name,args):
 backend=CloudPodManager.get(pod_name=pod_name)
 backend.pull()
def store_pod_metadata(pod_name,metadata):
 auth_headers=auth.get_auth_headers()
 metadata['pod_name']=pod_name
 response=safe_requests.post('%s/cloudpods'%API_ENDPOINT,json.dumps(metadata),headers=auth_headers)
 content=response.content
 if response.status_code>=400:
  raise EqPIK('Unable to store pod metadata in API (code %s): %s'%(response.status_code,content))
 return json.loads(to_str(content))
def list_pods(args):
 result=[]
 auth_headers=auth.get_auth_headers()
 response=safe_requests.get('%s/cloudpods'%API_ENDPOINT,headers=auth_headers)
 content=response.content
 if response.status_code>=400:
  raise EqPIK('Unable to fetch list of pods from API (code %s): %s'%(response.status_code,content))
 remote_pods=json.loads(to_str(content)).get('cloudpods',[])
 remote_pods=[{'state':'Shared',**pod}for pod in remote_pods]
 result.extend(remote_pods)
 local_pods=CloudPodManager.load_config(safe=EqPIX).get('pods',{})
 local_pods=[{'pod_name':k,'state':'Local Only',**v}for k,v in local_pods.items()]
 existing_names=EqPIx([pod['pod_name']for pod in result])
 result.extend([pod for pod in local_pods if pod['pod_name']not in existing_names])
 return result
def _pod_config(pod_name,config=EqPIY):
 config=config or CloudPodManager.load_config()
 pod_config=config.get('pods',{}).get(pod_name)
 if not pod_config:
  raise EqPIK('Unable to find config for pod named "%s"'%pod_name)
 return pod_config
# Created by pyminifier (https://github.com/liftoff/pyminifier)
