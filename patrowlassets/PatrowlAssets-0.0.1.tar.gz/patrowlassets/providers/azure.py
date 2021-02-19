# from azure.mgmt.resource import SubscriptionClient
# from azure.identity import ClientSecretCredential
# from . import Asset
#
#
# def init_client(ressource, aws_access_key, aws_secret_key):
#     # Retrieve the IDs and secret to use with ClientSecretCredential
#     subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
#     tenant_id = os.environ["AZURE_TENANT_ID"]
#     client_id = os.environ["AZURE_CLIENT_ID"]
#     client_secret = os.environ["AZURE_CLIENT_SECRET"]
#
#     credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
#
#     subscription_client = SubscriptionClient(credential)
#     # subscription = next(subscription_client.subscriptions.list())
#     # print(subscription.subscription_id)
#
#     return subscription_client
#
#
# def list_ec2_instances(aws_cli, status="running", region_name="eu-west-3"):
#     assets = []
#
#     return assets
