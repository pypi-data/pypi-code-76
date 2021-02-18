from localstack.utils.aws import aws_models
lFfEY=super
lFfEL=None
lFfEh=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  lFfEY(LambdaLayer,self).__init__(arn)
  self.cwd=lFfEL
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.lFfEh.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,lFfEh,env=lFfEL):
  lFfEY(RDSDatabase,self).__init__(lFfEh,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,lFfEh,env=lFfEL):
  lFfEY(RDSCluster,self).__init__(lFfEh,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,lFfEh,env=lFfEL):
  lFfEY(AppSyncAPI,self).__init__(lFfEh,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,lFfEh,env=lFfEL):
  lFfEY(AmplifyApp,self).__init__(lFfEh,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,lFfEh,env=lFfEL):
  lFfEY(ElastiCacheCluster,self).__init__(lFfEh,env=env)
class TransferServer(BaseComponent):
 def __init__(self,lFfEh,env=lFfEL):
  lFfEY(TransferServer,self).__init__(lFfEh,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,lFfEh,env=lFfEL):
  lFfEY(CloudFrontDistribution,self).__init__(lFfEh,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,lFfEh,env=lFfEL):
  lFfEY(CodeCommitRepository,self).__init__(lFfEh,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
