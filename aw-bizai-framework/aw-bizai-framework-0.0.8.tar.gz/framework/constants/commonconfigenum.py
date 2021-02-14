from enum import Enum

"""
    CommonConfigEnum stores common configurations required for the framework
    
"""
class CommonConfigEnum(Enum):
    """
    IBM_COS_CONFIG is an Enum for IBM Cloud Object Storge configuration    
    """
    IBM_COS_CONFIG = {
        "IBM_COS_API_KEY_ID": "25RdJDYL1Xlj0RvWGKRDCW7Xrn1esbA2yDtxyYGxOMym",
        "IBM_COS_RESOURCE_CRN": "crn:v1:bluemix:public:cloud-object-storage:global:a/f45d02f7085c3cbf06ee8aeb2d38bcd4:ada9b6a7-33d5-43a5-aaa3-f876776a32f8::",
        "IBM_COS_AUTH_ENDPOINT": "https://iam.ng.bluemix.net/oidc/token",
        "IBM_COS_SIGNATURE_VERSION": "oauth",
        "IBM_COS_ENDPOINT": "https://s3.us-south.cloud-object-storage.appdomain.cloud"
    }

    """
    DB2_CONFIG is an Enum for IBM Cloud Object Storge configuration    
    """
    DB2_CONFIG = {
        "DATABASE": "BLUDB",
        "HOSTNAME": "db2w-tiggaci.us-east.db2w.cloud.ibm.com",
        "PORT": 50001,
        "PROTOCOL": "TCPIP",
        "UID": "bluadmin",
        "PASSWORD": "H1_8dZY@YOuHF9BHmT7ZWhdBdQX@k",
        "SECURITY": "SSL"
    }

    DB_SCHEMA_NAME = "NEWBIZAISCHEMA"
    COS_BUCKET_NAME = "bizai-contracts"

    IBM_CLOUD_FUNCTION_USERNAME = '54ede776-9c57-4bcb-a80c-db63cedb0a1a'
    IBM_CLOUD_FUNCTION_PASSWORD = 'XjrdsAwMUa8N4y2FdAKn8R1JMvHgCrsAvifqSnFpIb0klarzW3fopu7aBIg3ZX3g'
    IBM_CLOUD_FUNCTION_URL_PREFIX = 'https://us-south.functions.cloud.ibm.com/api/v1/namespaces/OSNorth.Arun.Wagle.Org_FastStart/actions'

    SYSTEM_USER = "system"

    RUN_UNIT_TEST = True
