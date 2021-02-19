import boto3
from . import Asset


def init_session(aws_access_key, aws_secret_key):
    return boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )


def init_client(ressource, aws_access_key, aws_secret_key):
    return boto3.client(
        str(ressource),
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )


def list_ec2_instances(aws_cli, status="running", region_name="eu-west-3"):
    assets = []
    ec2 = aws_cli.resource('ec2', region_name=region_name)

    # Get information for all running instances
    try:
        instances = ec2.instances.filter(Filters=[{
            'Name': 'instance-state-name',
            'Values': [status]}])
        for instance in instances:
            # print(instance.id, instance.instance_type, instance.key_name, instance.private_ip_address, instance.public_dns_name, instance.tags[0].get("Value"))
            assets.append(Asset(
                value=instance.private_ip_address, exposure='internal',
                type='ip', tags=['aws', 'ec2']
            ))
            assets.append(Asset(
                value=instance.public_dns_name, exposure='external',
                type='fqdn', tags=['aws', 'ec2']
            ))
    except Exception:
        pass

    return assets


def list_s3_buckets(aws_cli, region_name="eu-west-3"):
    assets = []
    response = aws_cli.list_buckets()

    for bucket in response['Buckets']:
        assets.append(Asset(
            value=f"https://{bucket['Name']}.s3.{region_name}.amazonaws.com",
            exposure='external',
            type='url', tags=['aws', 's3', 'bucket']
        ))

    return assets


def list_route53_records(route53, region_name="eu-west-3", max_records=1000, zone_ids=[]):
    dns_records = []
    assets = []

    if len(zone_ids) == 0:
        try:
            hosted_zones = route53.list_hosted_zones()
        except Exception:
            print("AWS-Route53: Unable to list hosted zones. Check AWS user authorizations")
            return []

        # print(hosted_zones)
        for zi in hosted_zones['HostedZones']:
            zone_ids.append(zi['Id'])

    # Get information for all running instances
    for zone_id in zone_ids:
        try:
            dns_in_iteration = route53.list_resource_record_sets(HostedZoneId=zone_id)
            dns_records.extend(dns_in_iteration['ResourceRecordSets'])

            while len(dns_records) < max_records and 'NextRecordName' in dns_in_iteration.keys():
                next_record_name = dns_in_iteration['NextRecordName']
                # print('listing next set: ' + next_record_name)
                dns_in_iteration = route53.list_resource_record_sets(HostedZoneId=zone_id, StartRecordName=next_record_name)
                dns_records.extend(dns_in_iteration['ResourceRecordSets'])

            for record in dns_records:
                if record['Type'] == 'CNAME':
                    # print(record['Name'])
                    assets.append(Asset(
                        value=record['Name'], exposure='external',
                        type='domain', tags=['aws', 'route53', 'cname']
                    ))

        except Exception as e:
            print(e)
            pass

    return assets
