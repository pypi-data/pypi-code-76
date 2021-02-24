import yaml


def convert_compose_to_vars(src, dest):
    with open(src, 'rt') as fp:
        from_compose = yaml.load(fp, Loader=yaml.SafeLoader)
    containers = []
    secrets = set()
    for container, data in from_compose['services'].items():
        if 'environment' in data:
            for env, env_data in data['environment'].items():
                if isinstance(env_data, str):
                    if env_data.startswith('${'):
                        # ${INTEGRATION_HTTP_PORT:-5001}
                        if ':' in env_data:
                            parsed = env_data.split(':')[0].strip()[2:]
                        else:
                            parsed = env_data.strip()[2:-1]
                        secrets.add(parsed)
        containers.append(container)
    project = from_compose['networks'].popitem()[0]
    with open(dest, 'wt') as fp:
        yaml.dump({
            'secrets': list(secrets),
            'project': project,
            'containers': containers
        }, fp)
