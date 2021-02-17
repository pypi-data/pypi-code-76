from localstack.utils.aws import aws_models
HaChF=super
HaChP=None
HaCho=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  HaChF(LambdaLayer,self).__init__(arn)
  self.cwd=HaChP
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.HaCho.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,HaCho,env=HaChP):
  HaChF(RDSDatabase,self).__init__(HaCho,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,HaCho,env=HaChP):
  HaChF(RDSCluster,self).__init__(HaCho,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,HaCho,env=HaChP):
  HaChF(AppSyncAPI,self).__init__(HaCho,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,HaCho,env=HaChP):
  HaChF(AmplifyApp,self).__init__(HaCho,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,HaCho,env=HaChP):
  HaChF(ElastiCacheCluster,self).__init__(HaCho,env=env)
class TransferServer(BaseComponent):
 def __init__(self,HaCho,env=HaChP):
  HaChF(TransferServer,self).__init__(HaCho,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,HaCho,env=HaChP):
  HaChF(CloudFrontDistribution,self).__init__(HaCho,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,HaCho,env=HaChP):
  HaChF(CodeCommitRepository,self).__init__(HaCho,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
