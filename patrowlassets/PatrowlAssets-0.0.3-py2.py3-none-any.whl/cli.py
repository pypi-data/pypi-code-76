import click
import click_config_file
from providers import aws as aws_provider
from providers import ovh as ovh_provider
from patrowl4py.api import PatrowlManagerApi

@click.group()
@click.version_option("0.0.1")
def main():
    """CLI for PatrowlAssets"""
    pass


@main.command()
@click.option('--aws_access_key', default='')
@click.option('--aws_secret_key', default='')
@click.option('--aws_region', default='')
@click.option('--output-format', type=click.Choice(['list', 'csv', 'patrowl']))
@click.option('--patrowl-url', default='')
@click.option('--patrowl-auth-token', default='')
@click_config_file.configuration_option()
def aws(aws_access_key, aws_secret_key, aws_region, output_format, patrowl_url, patrowl_auth_token):
    aws_session = aws_provider.init_session(aws_access_key, aws_secret_key)
    assets = aws_provider.list_ec2_instances(aws_session, region_name=aws_region)

    aws_cli = aws_provider.init_client('route53', aws_access_key, aws_secret_key)
    assets.extend(aws_provider.list_route53_records(aws_cli, region_name=aws_region))

    aws_cli = aws_provider.init_client('s3', aws_access_key, aws_secret_key)
    assets.extend(aws_provider.list_s3_buckets(aws_cli, region_name=aws_region))

    if output_format.lower() == 'csv':
        click.echo(';'.join(['asset_value', 'asset_name', 'asset_type', 'asset_description',
        'asset_criticity', 'asset_tags', 'owner', 'team', 'asset_exposure', 'created_at']))
        for asset in assets:
            click.echo(';'.join(asset.to_csv()))
    elif output_format.lower() == 'patrowl':
        sendto_patrowl(assets, 'AWS resources', patrowl_url, patrowl_auth_token, tags=['aws', 'sync'])
    else:
        for asset in assets:
            click.echo(asset)


@main.command()
@click.option('--ovh_endpoint', default='')
@click.option('--ovh_application_key', default='')
@click.option('--ovh_application_secret', default='')
@click.option('--ovh_consumer_key', default='')
@click.option('--output-format', type=click.Choice(['list', 'csv', 'patrowl']))
@click.option('--patrowl-url', default='')
@click.option('--patrowl-auth-token', default='')
@click_config_file.configuration_option()
def ovh(ovh_endpoint, ovh_application_key, ovh_application_secret, ovh_consumer_key, output_format, patrowl_url, patrowl_auth_token):
    assets = []
    ovh_cli = ovh_provider.init_client(ovh_endpoint, ovh_application_key, ovh_application_secret, ovh_consumer_key)

    assets.extend(ovh_provider.list_dedicated_servers(ovh_cli))
    assets.extend(ovh_provider.list_domains(ovh_cli))
    assets.extend(ovh_provider.list_vps(ovh_cli))
    assets.extend(ovh_provider.list_cloud_projects(ovh_cli))

    if output_format.lower() == 'csv':
        click.echo(';'.join(['asset_value', 'asset_name', 'asset_type', 'asset_description',
            'asset_criticity', 'asset_tags', 'owner', 'team', 'asset_exposure', 'created_at']))
        for asset in assets:
            click.echo(';'.join(asset.to_csv()))
    elif output_format.lower() == 'patrowl':
        sendto_patrowl(assets, 'OVH resources', patrowl_url, patrowl_auth_token, tags=['ovh', 'sync'])
    else:
        for asset in assets:
            click.echo(asset)


def sendto_patrowl(assets, name, patrowl_url, patrowl_auth_token, tags=[]):
    try:
        patrowl_api = PatrowlManagerApi(patrowl_url, patrowl_auth_token)
    except Exception:
        click.error("Unable to access the Patrowl API")
        return False

    assets_ids = []
    for asset in assets:
        try:
             asset_id = patrowl_api.get_asset_by_value(asset.value)
             assets_ids.append(asset_id['id'])
        except Exception:
            print(f"Syncing '{asset}' to Patrowl")
            try:
                asset_id = patrowl_api.add_asset(
                    value=asset.value,
                    name=asset.value,
                    datatype=asset.type,
                    description=f"Synced with PatrowlAssets: {asset.value}",
                    criticity='low',
                    exposure=asset.exposure,
                    tags=asset.tags,
                    teams=[]
                )
                assets_ids.append(asset_id['id'])
            except Exception:
                pass

    try:
        asset_group_data = patrowl_api.get_assetgroup_by_name(name)
        asset_group_id = asset_group_data['id']
        patrowl_api.edit_assetgroup(asset_group_id, name, f'{name} Sync', 'low', assets_ids, tags=tags)

    except Exception:
        patrowl_api.add_assetgroup(
            name=name,
            description=f'{name} Sync',
            criticity='low',
            assets=assets_ids,
            tags=tags,
        )


if __name__ == '__main__':
    main(prog_name="pa")
