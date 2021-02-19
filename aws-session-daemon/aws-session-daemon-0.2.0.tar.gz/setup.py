# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aws_session_daemon']
install_requires = \
['aws_credential_process>=0.10', 'click>=7', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['aws-session-daemon = aws_session_daemon:click_main',
                     'aws-session-daemon-get-config = '
                     'aws_session_daemon:get_config']}

setup_kwargs = {
    'name': 'aws-session-daemon',
    'version': '0.2.0',
    'description': 'AWS session token refreshing daemon',
    'long_description': 'AWS Session daemon\n=================\n\nThis script automatically gets an MFA authenticated session using a Yubikey as MFA (multi factor authentication) and updates\n`~/.aws/credentials`.\n\nAs long as you\'ve got your yubikey connected to your computer you\'ll never have to enter a second factor authentication code for the aws\ncli. As other tools / libraries (boto3) use `~/.aws/credentials` as well you don\'t have to enter a token for these either.\n\nUsage\n-----\n\nYou can install `aws-session-daemon` using pip (`pip install aws-session-daemon`), I recommend to install `aws-session-daemon` using poetry\n(`poetry install aws-session-daemon`) or in a virtualenv.\n\nYour `~/.aws/credentials` should contain your credentials and a profile with the the keys `aws_access_key_id`,\n`aws_secret_access_key` and `aws_session_token`.\n\nFor example:\n\n`~/.aws/credentials`\n\n```ini\n[default]\naws_access_key_id = ...(your key id)...\naws_secret_access_key = ...(your access key)...\n\n[profile]\naws_access_key_id = ...(placeholder, can be anything)...\naws_secret_access_key = ...(placeholder, can be anything)...\naws_session_token = ...(placeholder, can be anything)...\n```\n\nYour `~/.aws/credentials` will be updated in place, only the specified profile section should be touched (your comments will be safe).\n\nOlder versions are rotated up to 5 items.\n\nNext `aws-session-daemon` should be started with the following arguments:\n\n```bash\naws-session-daemon --rolearn ... --oath_slot=... --serialnumber=... --profile_name=... --access-key-id=... --secret-access-key=... --mfa-session-duration=...\n```\n\nArgument                 | Description\n-------------------------|-------------------------------------\n`--rolearn`              | arn of the role you\'d like to assume\n`--oath_slot`            | oath slot on your yubikey\n`--serialnumber`         | serial number of your MFA\n`--profile_name`         | profile used in `~/.aws/credentials`\n`--access-key-id`        | access key (as obtained from IAM console)\n`--secret-access-key`    | secret access key (as obtained from IAM console)\n`--mfa-session-duration` | duration (in seconds) for MFA session\n`--credentials-section`  | you can specify a different section than default in `~/.aws/credentials`\n`--config-section TEXT`  | config section in configuration file `~/config/aws-session-daemon/config.toml`\n\n\nYou should only run one `aws-session-daemon` process per profile, I use systemd for starting `aws-session-daemon`, by using the\nfollowing unit file:\n\n`~/.config/systemd/user/aws-session-daemon@.service`\n\n```ini\n[Unit]\nDescription=Amazon Web Services token daemon\n\n[Service]\nType=simple\nExecStart=%h/bin/aws-session-daemon --config-section=\'%i\'\nRestart=on-failure\n\n[Install]\nWantedBy=default.target\n```\n\nAnd reload systemd using `systemctl --user daemon-reload`, start `aws-session-daemon` using `systemctl --user start aws-session-daemon@...`\n\nIf you\'re not so fortunate to have systemd you can also use something like `supervisord` to start `aws-session-daemon`.\n\n`~/supervisord.conf`\n\n```ini\n[supervisord]\n\n[supervisorctl]\nserverurl=unix:///home/user/supervisord.sock\n\n[unix_http_server]\nfile=/home/user/supervisord.sock\n\n[rpcinterface:supervisor]\nsupervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface\n\n[program:session-daemon-...]\ncommand=/home/user/bin/aws-session-daemon --config-section=...\nautorestart=true\n```\n\nStart supervisord using `supervisord -c supervisor.conf` and start session-daemon using\n`supervisorctl -c supervisor.conf start session-daemon-...`.\n\n## Configuration\n\naws-session-daemon can also use a configuration file, the default location of\nthis file is `~/.config/aws-session-daemon/config.toml`. This file contains\ndefaults so you don\'t have to supply all of the arguments.\n\nYou can define multiple config-sections:\n\n```toml\n[123457890123]\nmfa_oath_slot="Amazon Web Services:user@123457890123"\nassume_role_arn="arn:aws:iam::123457890123:role/Other/Role"\ncredentials_section="123457890123"\nmfa_serial_number="arn:aws:iam::123457890123:mfa/user"\n\n[098765432101]\nmfa_oath_slot="Amazon Web Services:user@098765432101"\ncredentials_section="098765432101"\nmfa_serial_number="arn:aws:iam::098765432101:mfa/user"\n```\n\nIf you need to assume roles from a certain AWS account you\'ll end up with a lot\nof simular entries. To make this simple the configuration can be defined\nhierarchical.\n\n```toml\n[[org]]\nmfa_oath_slot="Amazon Web Services:user@123457890123"\nassume_role_arn="arn:aws:iam::{section}:role/Other/Role"\ncredentials_section="123457890123"\nmfa_serial_number="arn:aws:iam::123457890123:mfa/user"\n\n[[org.098765432101]]\n[[org.567890123456]]\n```\n\nThis would be the same as the following configuration:\n\n```toml\n[098765432101]\nmfa_oath_slot="Amazon Web Services:user@123457890123"\nassume_role_arn="arn:aws:iam::098765432101:role/Other/Role"\ncredentials_section="123457890123"\nmfa_serial_number="arn:aws:iam::123457890123:mfa/user"\n\n[567890123456]\nmfa_oath_slot="Amazon Web Services:user@123457890123"\nassume_role_arn="arn:aws:iam::567890123456:role/Other/Role"\ncredentials_section="123457890123"\nmfa_serial_number="arn:aws:iam::123457890123:mfa/user"\n```\n',
    'author': 'Dick Marinus',
    'author_email': 'dick@mrns.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/meeuw/aws-session-daemon',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
