# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aws_credential_process']
install_requires = \
['boto3>=1.11,<2.0',
 'click>=7.1,<8.0',
 'keyring>=20.0.1',
 'pynentry>=0.1.3,<0.2.0',
 'toml>=0.10.2,<0.11.0',
 'yubikey-manager==3.1.1']

entry_points = \
{'console_scripts': ['aws-credential-process = '
                     'aws_credential_process:click_main']}

setup_kwargs = {
    'name': 'aws-credential-process',
    'version': '0.10.0',
    'description': 'AWS Credential Process',
    'long_description': '# README\n\n## Description\n\nScript to use as `credential_process` for the AWS CLI (including boto3), it\ncaches your MFA session in a keyring and can use a Yubi key to authenticate.\n\nThis is useful if you are required to use MFA authenticated sessions or need\nan MFA authenticated session to assume a role.\n\n## Installing\n\nYou can install aws-credential-process using pip:\n\n```bash\npip install aws_credential_process\n```\n\nI recommend to install aws-credential-process in a virtualenv:\n\n```bash\nvirtualenv ~/venv/aws_credential_process\n~/venv/aws_credential_process/bin/pip install aws_credential_process\n```\n\nAfter the above commands you should be able to run `~/venv/aws_credential_process/bin/aws-credential-process`\n\n## Usage\n\nYou can use the following arguments to start aws-credential-process:\n\n```\nUsage: aws-credential-process [OPTIONS]\n\n  Get output suitable for aws credential process\n\nOptions:\n  --access-key-id TEXT\n  --secret-access-key TEXT\n  --mfa-oath-slot TEXT\n  --mfa-serial-number TEXT\n  --mfa-session-duration INTEGER\n  --assume-session-duration INTEGER\n  --assume-role-arn TEXT\n  --force-renew\n  --credentials-section TEXT\n  --pin-entry TEXT\n  --log-file TEXT\n  --config-section TEXT\n  --config-file TEXT\n  --help                          Show this message and exit.\n```\n\naws-credential-process is meant to be used as `credential_process` in your\n`.aws/config` file. For example:\n\n```ini\n[profile yourprofile]\ncredential_process = /home/user/venv/aws_credential_process/bin/aws-credential-process --mfa-oath-slot "Amazon Web Services:test@example.com" --mfa-serial-number arn:aws:iam::123456789012:mfa/john.doe --assume-role-arn arn:aws:iam::123456789012:role/YourRole\n```\n\nIf you\'ve supplied the secret-access-key once you can omit it with the next call,\nit will be cached in your keyring.\n\nWhen you don\'t supply the access-key-id it will be loaded from `~/.aws/credentials`.\nYou can use another section than "default" by using the credentials-section argument.\n\n## Configuration\n\naws-credential-process can also use a configuration file, the default location of\nthis file is `~/.config/aws-credential-process/config.toml`. This file contains\ndefaults so you don\'t have to supply all of the arguments.\n\nYou can configure a default pin-entry program like:\n\n```toml\npin_entry = /usr/local/bin/pin_entry\n```\n\nOr you can define multiple config-sections:\n\n```toml\n[123457890123]\nmfa_oath_slot="Amazon Web Services:user@123457890123"\nassume_role_arn="arn:aws:iam::123457890123:role/Other/Role"\ncredentials_section="123457890123"\nmfa_serial_number="arn:aws:iam::123457890123:mfa/user"\n\n[098765432101]\nmfa_oath_slot="Amazon Web Services:user@098765432101"\ncredentials_section="098765432101"\nmfa_serial_number="arn:aws:iam::098765432101:mfa/user"\n```\n\nIf you need to assume roles from a certain AWS account you\'ll end up with a lot\nof simular entries. To make this simple the configuration can be defined\nhierarchical.\n\n```toml\n[[org]]\nmfa_oath_slot="Amazon Web Services:user@123457890123"\nassume_role_arn="arn:aws:iam::{section}:role/Other/Role"\ncredentials_section="123457890123"\nmfa_serial_number="arn:aws:iam::123457890123:mfa/user"\n\n[[org.098765432101]]\n[[org.567890123456]]\n```\n\nThis would be the same as the following configuration:\n\n```toml\n[098765432101]\nmfa_oath_slot="Amazon Web Services:user@123457890123"\nassume_role_arn="arn:aws:iam::098765432101:role/Other/Role"\ncredentials_section="123457890123"\nmfa_serial_number="arn:aws:iam::123457890123:mfa/user"\n\n[567890123456]\nmfa_oath_slot="Amazon Web Services:user@123457890123"\nassume_role_arn="arn:aws:iam::567890123456:role/Other/Role"\ncredentials_section="123457890123"\nmfa_serial_number="arn:aws:iam::123457890123:mfa/user"\n```\n\nWith the above configuration aws-credential-process can be used like this in\n`~/.aws/config`:\n\n```ini\n[profile profile1]\ncredential_process = /home/user/venv/aws_credential_process/bin/aws-credential-process --config-section=098765432101\n\n[profile profile2]\ncredential_process = /home/user/venv/aws_credential_process/bin/aws-credential-process --config-section=567890123456\n```\n',
    'author': 'Dick Marinus',
    'author_email': 'dick@mrns.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/meeuw/aws-credential-process',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
