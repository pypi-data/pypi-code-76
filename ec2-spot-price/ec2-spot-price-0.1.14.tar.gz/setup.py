# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ec2_spot_price']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.12,<2.0.0', 'pandas>=1.2.2,<2.0.0']

entry_points = \
{'console_scripts': ['ec2_spot_price = ec2_spot_price:main']}

setup_kwargs = {
    'name': 'ec2-spot-price',
    'version': '0.1.14',
    'description': 'Library and command for retrieving Amazon EC2 spot instance price',
    'long_description': '# ec2-spot-price\n\nLibrary and command for retrieving Amazon EC2 spot instance price\n\n\n## Install\n\n```sh\npip install ec2-spot-price\n```\n\n## Setup\n\nYou need to have IAM user to access EC2\'s DescribeSpotPriceHistory API.\nA simple way to do is to add new user and attach AmazonEC2ReadOnlyAccess\npolicy.\n\nOr you can use existent user which have permissions to access that API.\n\n### Goto IAM Console\n\nhttps://console.aws.amazon.com/iam/home\n\n### Add new IAM user\n\n```\nUser name: myuser  # whatever you want\nAccess type: Programmatic access\nSet permissions: Attach existing policies directly\nPolicy name: AmazonEC2ReadOnlyAccess\nDownload .csv\n```\n\n### Edit ~/.aws/credentials\n\nYou can use "named profile" to have multiple credentials settings.\nSee https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html\n\n```\n[myprofile]  # or [default]\naws_access_key_id=[copy from csv]\naws_secret_access_key=[copy from csv]\nregion=us-east-2  # wherever you want\n```\n\n## Usage\n\n### Run Script\n\nIf you use [myprofile], you need to specify AWS_PROFILE environment\nvariable. If you use [default] section, you can omit AWS_PROFILE.\n\n```\nexport AWS_PROFILE=myprofile\n```\n\n\n```\nec2_spot_price -r us-east-1 -i c5.xlarge\nSpotPrice,AvailabilityZone,InstanceType,ProductDescription,Timestamp\n0.072000,us-east-1b,c5.xlarge,Linux/UNIX,2021-02-20 19:20:57+00:00\n0.074100,us-east-1d,c5.xlarge,Linux/UNIX,2021-02-20 17:39:28+00:00\n0.076800,us-east-1c,c5.xlarge,Linux/UNIX,2021-02-20 16:06:29+00:00\n0.077700,us-east-1a,c5.xlarge,Linux/UNIX,2021-02-20 19:12:58+00:00\n0.106100,us-east-1f,c5.xlarge,Linux/UNIX,2021-02-20 14:32:58+00:00\n```\n\n### Use library\n\n```\nimport sys\nimport ec2_spot_price\nr = ec2_spot_price.get_spot_prices([\'us-east-1\'], [\'g4dn.4xlarge\'], [\'Linux/UNIX\'])\nec2_spot_price.spot_prices_to_csv(r, sys.stdout)\n,SpotPrice,AvailabilityZone,InstanceType,ProductDescription,Timestamp\n0,0.361200,us-east-1d,g4dn.4xlarge,Linux/UNIX,2021-02-19 22:39:19+00:00\n1,0.361200,us-east-1f,g4dn.4xlarge,Linux/UNIX,2021-02-19 22:39:19+00:00\n2,0.361200,us-east-1c,g4dn.4xlarge,Linux/UNIX,2021-02-19 22:39:19+00:00\n3,0.361200,us-east-1b,g4dn.4xlarge,Linux/UNIX,2021-02-19 22:39:19+00:00\n4,0.361200,us-east-1a,g4dn.4xlarge,Linux/UNIX,2021-02-19 22:39:19+00:00\n```\n\n## See also\n\nhttps://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSpotPriceHistory.html\nhttps://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration\nhttps://aws.amazon.com/ec2/spot/pricing/\n\n\n## Author\n\nSusumu OTA\n\n\n',
    'author': 'Susumu OTA',
    'author_email': '1632335+susumuota@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/susumuota/ec2_spot_price',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
