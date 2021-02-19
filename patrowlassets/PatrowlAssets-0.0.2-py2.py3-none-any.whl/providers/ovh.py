import ovh
from . import Asset

'''
List:
- dedicated servers: OK
- domains: OK
- VPS: OK
- cloud
    - Project
        - instances: OK
        - ips
        - failover_ips
        - load balancers
        - network public
        - kube
        - kube nodes
- cloudDB
- hosting/web
'''

def init_client(ovh_endpoint, ovh_application_key, ovh_application_secret, ovh_consumer_key):
    return ovh.Client(
        endpoint=ovh_endpoint,
        application_key=ovh_application_key,
        application_secret=ovh_application_secret,
        consumer_key=ovh_consumer_key
    )


def list_dedicated_servers(ovh_cli):
    assets = []
    servers = ovh_cli.get('/dedicated/server/')

    for server in servers:
        details = ovh_cli.get('/dedicated/server/%s' % server)
        assets.append(Asset(
            value=details['ip'], exposure='external',
            type='ip', tags=['ovh', 'server', 'dedicated']
        ))
        assets.append(Asset(
            value=details['name'], exposure='external',
            type='fqdn', tags=['ovh', 'server', 'dedicated']
        ))

    return assets


def list_domains(ovh_cli):
    assets = []
    domains = ovh_cli.get('/domain/')

    for domain in domains:
        assets.append(Asset(
            value=domain, exposure='external',
            type='domain', tags=['ovh', 'domain_name']
        ))
    return assets


def list_vps(ovh_cli):
    assets = []
    vps_list = ovh_cli.get('/vps')

    for vps_id in vps_list:
        vps = ovh_cli.get(f'/vps/{vps_id}')
        assets.append(Asset(
            value=vps['name'], exposure='external',
            type='fqdn', tags=['ovh', 'vps']
        ))
        vps_ips = ovh_cli.get(f'/vps/{vps_id}/ips')
        for ip in vps_ips:
            assets.append(Asset(
                value=ip, exposure='external',
                type='ip', tags=['ovh', 'vps']
            ))
    return assets


def list_cloud_projects(ovh_cli):
    assets = []
    projects = ovh_cli.get('/cloud/project/')

    for project_id in projects:
        instances = ovh_cli.get(f'/cloud/project/{project_id}/instance')
        for instance in instances:
            for ip in instance['ipAddresses']:
                assets.append(Asset(
                    value=ip['ip'], exposure='external',
                    type='ip', tags=['ovh', 'cloud', 'instance', f'ipv{ip["version"]}']
                ))

        # ips = ovh_cli.get(f'/cloud/project/{project_id}/ip')
        # for ip in ips:
        #     print(ip)
        # failover_ips = ovh_cli.get(f'/cloud/project/{project_id}/ip/failover')
        # for ip in failover_ips:
        #     print(ip)
        # loadbalancers = ovh_cli.get(f'/cloud/project/{project_id}/loadbalancer')
        # for lb in loadbalancers:
        #     print(lb)
    ip_loadbalancers = ovh_cli.get('/ipLoadbalancing')
    for lb_id in ip_loadbalancers:
        lb = ovh_cli.get(f'/ipLoadbalancing/{lb_id}')
        assets.append(Asset(
            value=lb['ipv4'], exposure='external',
            type='ip', tags=['ovh', 'loadbalancer', 'ipv4']
        ))

    return assets
