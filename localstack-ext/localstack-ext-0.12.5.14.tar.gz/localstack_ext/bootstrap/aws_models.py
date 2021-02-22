from localstack.utils.aws import aws_models
ENWgc=super
ENWgf=None
ENWgz=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  ENWgc(LambdaLayer,self).__init__(arn)
  self.cwd=ENWgf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.ENWgz.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,ENWgz,env=ENWgf):
  ENWgc(RDSDatabase,self).__init__(ENWgz,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,ENWgz,env=ENWgf):
  ENWgc(RDSCluster,self).__init__(ENWgz,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,ENWgz,env=ENWgf):
  ENWgc(AppSyncAPI,self).__init__(ENWgz,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,ENWgz,env=ENWgf):
  ENWgc(AmplifyApp,self).__init__(ENWgz,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,ENWgz,env=ENWgf):
  ENWgc(ElastiCacheCluster,self).__init__(ENWgz,env=env)
class TransferServer(BaseComponent):
 def __init__(self,ENWgz,env=ENWgf):
  ENWgc(TransferServer,self).__init__(ENWgz,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,ENWgz,env=ENWgf):
  ENWgc(CloudFrontDistribution,self).__init__(ENWgz,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,ENWgz,env=ENWgf):
  ENWgc(CodeCommitRepository,self).__init__(ENWgz,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
