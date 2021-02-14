
import os
import typeguard
from time import strftime, gmtime
from ast import literal_eval  # str to dict
import boto3  # regions
from cloud_governance.common.logger.logger_time_stamp import logger_time_stamp, logger
from cloud_governance.tag_cluster.run_tag_cluster_resouces import tag_cluster_resource, tag_ec2_resource
from cloud_governance.zombie_cluster.run_zombie_cluster_resources import zombie_cluster_resource
from cloud_governance.gitleaks.gitleaks import GitLeaks
from cloud_governance.main.es_uploader import ESUploader


# # env tests
#os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'
# os.environ['AWS_DEFAULT_REGION'] = 'all'
# os.environ['policy'] = 'tag_ec2'
# os.environ['policy'] = 'ec2_untag'
#os.environ['policy'] = 'zombie_cluster_resource'
# os.environ['policy'] = 'tag_cluster_resource'
# os.environ['policy_output'] ='s3://redhat-cloud-governance/logs'
#os.environ['dry_run'] = 'yes'
# os.environ['policy'] = 'ebs_unattached'
# os.environ['resource_name'] = 'ocp-orch-perf'
# os.environ['resource_name'] = 'ocs-test'
# os.environ['mandatory_tags'] = "{'Owner': 'Eli Battat','Email': 'ebattat@redhat.com','Purpose': 'test'}"
# os.environ['mandatory_tags'] = ''
# os.environ['policy'] = 'gitleaks'
# os.environ['git_access_token'] = ''
# os.environ['git_repo'] = 'https://github.com/redhat-performance/pulpperf'
# os.environ['git_repo'] = 'https://github.com/gitleakstest/gronit'
# os.environ['several_repos'] = 'Yes'
# os.environ['upload_data_elk'] = 'upload_data_elk'

log_level = os.environ.get('log_level', 'INFO').upper()
logger.setLevel(level=log_level)
custodian_policies = ['ec2_idle', 'ebs_unattached', 'ec2_untag']


@logger_time_stamp
@typeguard.typechecked
def run_policy(policy: str, region: str, dry_run: str):
    """
    This method run policy per region, first the custom policy and after custodian policy
    :return:
    """
    # Custom policy Tag Cluster
    if policy == 'tag_cluster_resource':
        cluster_name = os.environ['resource_name']
        if dry_run == 'no':
            mandatory_tags = os.environ.get('mandatory_tags', {})
            mandatory_tags = literal_eval(mandatory_tags)  # str to dict
            mandatory_tags['Date'] = strftime("%Y/%m/%d %H:%M:%S")
            tag_cluster_resource(cluster_name=cluster_name, mandatory_tags=mandatory_tags, region=region)
        else:  # default: yes or other
            tag_cluster_resource(cluster_name=cluster_name, region=region)
    # Custom policy Zombie Cluster
    elif policy == 'zombie_cluster_resource':
        if dry_run == 'no':  # delete
            zombie_cluster_resource(delete=True, region=region)
        else:  # default: yes or other
            zombie_cluster_resource(region=region)
    elif policy == 'tag_ec2':
        instance_name = os.environ['resource_name']
        mandatory_tags = os.environ.get('mandatory_tags', {})
        mandatory_tags = literal_eval(mandatory_tags)  # str to dict
        mandatory_tags['Name'] = instance_name
        mandatory_tags['Date'] = strftime("%Y/%m/%d %H:%M:%S")
        if dry_run == 'no':
            response = tag_ec2_resource(instance_name=instance_name, mandatory_tags=mandatory_tags, region=region)
        else:
            response = tag_ec2_resource(instance_name=instance_name, mandatory_tags=mandatory_tags, region=region)
        logger.info(response)
    elif policy == 'gitleaks':
        git_access_token = os.environ.get('git_access_token')
        git_repo = os.environ.get('git_repo')
        several_repos = os.environ.get('several_repos')
        try:
            if several_repos == 'Yes':
                git_leaks = GitLeaks(git_access_token=git_access_token,
                                     git_repo=git_repo,
                                     several_repos=True)
            else:
                git_leaks = GitLeaks(git_access_token=git_access_token,
                                     git_repo=git_repo)
            logger.info(git_leaks.scan_repo())
        except Exception as err:
            logger.exception(f'BadCredentialsException : {err}')
    # custodian policy - check if its a custodian policy
    elif any(policy == item for item in custodian_policies):
        # default is dry run - change it to custodian dry run format
        if dry_run == 'yes':
            dry_run = '--dryrun'
        elif dry_run == 'no':
            dry_run = ''
        else:  # default dry run
            dry_run = '--dryrun'
        policy_output = os.environ['policy_output']
        # run from local - policies_path = os.path.join(os.path.dirname(__file__), '../' ,f'{policy}.yml')
        policies_path = os.path.join(os.path.dirname(__file__), 'policy')
        if os.path.isfile(f'{policies_path}/{policy}.yml'):
            os.system(f'custodian run {dry_run} -s {policy_output} {policies_path}/{policy}.yml')
        else:
            raise Exception(f'Missing Policy name: "{policies_path}/{policy}.yml"')
            logger.exception(f'Missing Policy name: "{policies_path}/{policy}.yml"')
    else:  # local policy
        # default is dry run - change it to custodian dry run format
        if dry_run == 'yes':
            dry_run = '--dryrun'
        elif dry_run == 'no':
            dry_run = ''
        else:  # default dry run
            dry_run = '--dryrun'
        policy_output = os.environ['policy_output']
        # run from local - policies_path = os.path.join(os.path.dirname(__file__), '../' ,f'{policy}.yml')
        if os.path.isfile(policy):
            os.system(f'custodian run {dry_run} -s {policy_output} {policy}')
        else:
            raise Exception(f'Missing Policy name: {policy}')
            logger.exception(f'Missing Policy name: {policy}')


@logger_time_stamp
def main():
    """
    This main run 2 processes:
    1. ES uploader
    2. Run policy
    :return: the action output
    """
    # environment variables - get while running the docker
    region_env = os.environ.get('AWS_DEFAULT_REGION', 'us-east-2')
    dry_run = os.environ.get('dry_run', 'yes')
    policy = os.environ.get('policy', '')
    upload_data_es = os.environ.get('upload_data_es', '')
    es_host = os.environ.get('es_host', '')
    es_port = os.environ.get('es_port', '')
    es_index = os.environ.get('es_index', '')
    bucket = os.environ.get('bucket', '')

    # 1. ELK Uploader
    if upload_data_es:
        input_data = {'es_host': es_host,
                      'es_port': int(es_port),
                      'es_index': es_index,
                      'es_doc_type': 'json_doc_type',
                      'es_add_items': {},
                      'bucket': bucket,
                      'logs_bucket_key': 'logs',
                      's3_file_name': 'resources.json',
                      'region': region_env,
                      'policy': policy,
                      }
        elk_uploader = ESUploader(**input_data)
        elk_uploader.upload_to_es()
    # 2. POLICY
    else:
        if not policy:
            raise Exception(f'Missing Policy name: "{policy}"')
            logger.exception(f'Missing Policy name: "{policy}"')
        if region_env == 'all':
            # must be set for bot03 client default region
            os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'
            ec2 = boto3.client('ec2')
            regions_data = ec2.describe_regions()
            for region in regions_data['Regions']:
                #logger.info(f"region: {region['RegionName']}")
                os.environ['AWS_DEFAULT_REGION'] = region['RegionName']
                run_policy(policy=policy, region=region['RegionName'], dry_run=dry_run)
        else:
            run_policy(policy=policy, region=region_env, dry_run=dry_run)


main()
