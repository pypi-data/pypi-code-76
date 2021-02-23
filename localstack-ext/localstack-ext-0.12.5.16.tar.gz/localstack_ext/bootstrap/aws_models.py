from localstack.utils.aws import aws_models
KyCxM=super
KyCxd=None
KyCxN=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  KyCxM(LambdaLayer,self).__init__(arn)
  self.cwd=KyCxd
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.KyCxN.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,KyCxN,env=KyCxd):
  KyCxM(RDSDatabase,self).__init__(KyCxN,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,KyCxN,env=KyCxd):
  KyCxM(RDSCluster,self).__init__(KyCxN,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,KyCxN,env=KyCxd):
  KyCxM(AppSyncAPI,self).__init__(KyCxN,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,KyCxN,env=KyCxd):
  KyCxM(AmplifyApp,self).__init__(KyCxN,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,KyCxN,env=KyCxd):
  KyCxM(ElastiCacheCluster,self).__init__(KyCxN,env=env)
class TransferServer(BaseComponent):
 def __init__(self,KyCxN,env=KyCxd):
  KyCxM(TransferServer,self).__init__(KyCxN,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,KyCxN,env=KyCxd):
  KyCxM(CloudFrontDistribution,self).__init__(KyCxN,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,KyCxN,env=KyCxd):
  KyCxM(CodeCommitRepository,self).__init__(KyCxN,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
