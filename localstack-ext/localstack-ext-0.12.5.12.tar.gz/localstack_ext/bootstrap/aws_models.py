from localstack.utils.aws import aws_models
RAHva=super
RAHvX=None
RAHvS=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  RAHva(LambdaLayer,self).__init__(arn)
  self.cwd=RAHvX
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.RAHvS.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,RAHvS,env=RAHvX):
  RAHva(RDSDatabase,self).__init__(RAHvS,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,RAHvS,env=RAHvX):
  RAHva(RDSCluster,self).__init__(RAHvS,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,RAHvS,env=RAHvX):
  RAHva(AppSyncAPI,self).__init__(RAHvS,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,RAHvS,env=RAHvX):
  RAHva(AmplifyApp,self).__init__(RAHvS,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,RAHvS,env=RAHvX):
  RAHva(ElastiCacheCluster,self).__init__(RAHvS,env=env)
class TransferServer(BaseComponent):
 def __init__(self,RAHvS,env=RAHvX):
  RAHva(TransferServer,self).__init__(RAHvS,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,RAHvS,env=RAHvX):
  RAHva(CloudFrontDistribution,self).__init__(RAHvS,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,RAHvS,env=RAHvX):
  RAHva(CodeCommitRepository,self).__init__(RAHvS,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
