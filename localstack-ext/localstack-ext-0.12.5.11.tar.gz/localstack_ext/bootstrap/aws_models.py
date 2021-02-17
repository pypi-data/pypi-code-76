from localstack.utils.aws import aws_models
aCrsO=super
aCrsY=None
aCrsR=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  aCrsO(LambdaLayer,self).__init__(arn)
  self.cwd=aCrsY
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.aCrsR.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,aCrsR,env=aCrsY):
  aCrsO(RDSDatabase,self).__init__(aCrsR,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,aCrsR,env=aCrsY):
  aCrsO(RDSCluster,self).__init__(aCrsR,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,aCrsR,env=aCrsY):
  aCrsO(AppSyncAPI,self).__init__(aCrsR,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,aCrsR,env=aCrsY):
  aCrsO(AmplifyApp,self).__init__(aCrsR,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,aCrsR,env=aCrsY):
  aCrsO(ElastiCacheCluster,self).__init__(aCrsR,env=env)
class TransferServer(BaseComponent):
 def __init__(self,aCrsR,env=aCrsY):
  aCrsO(TransferServer,self).__init__(aCrsR,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,aCrsR,env=aCrsY):
  aCrsO(CloudFrontDistribution,self).__init__(aCrsR,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,aCrsR,env=aCrsY):
  aCrsO(CodeCommitRepository,self).__init__(aCrsR,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
