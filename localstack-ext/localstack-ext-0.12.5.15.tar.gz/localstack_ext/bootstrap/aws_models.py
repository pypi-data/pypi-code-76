from localstack.utils.aws import aws_models
nOYJw=super
nOYJq=None
nOYJG=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  nOYJw(LambdaLayer,self).__init__(arn)
  self.cwd=nOYJq
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.nOYJG.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,nOYJG,env=nOYJq):
  nOYJw(RDSDatabase,self).__init__(nOYJG,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,nOYJG,env=nOYJq):
  nOYJw(RDSCluster,self).__init__(nOYJG,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,nOYJG,env=nOYJq):
  nOYJw(AppSyncAPI,self).__init__(nOYJG,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,nOYJG,env=nOYJq):
  nOYJw(AmplifyApp,self).__init__(nOYJG,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,nOYJG,env=nOYJq):
  nOYJw(ElastiCacheCluster,self).__init__(nOYJG,env=env)
class TransferServer(BaseComponent):
 def __init__(self,nOYJG,env=nOYJq):
  nOYJw(TransferServer,self).__init__(nOYJG,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,nOYJG,env=nOYJq):
  nOYJw(CloudFrontDistribution,self).__init__(nOYJG,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,nOYJG,env=nOYJq):
  nOYJw(CodeCommitRepository,self).__init__(nOYJG,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
