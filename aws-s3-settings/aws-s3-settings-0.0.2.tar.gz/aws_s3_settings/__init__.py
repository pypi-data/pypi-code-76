from six.moves import urllib
import yaml
import re
import boto3
import os

CREDENTIALS_DIR = "/credentials"

def run(credentials_directory=CREDENTIALS_DIR, bucket_pattern='ls-{CLOUD_ENVIRONMENT}-credentials', bucket_path="{CLOUD_DEV_PHASE}/{CLOUD_APP}/"):
    s3 = boto3.resource('s3')

    user_data_string = urllib.request.urlopen("http://169.254.169.254/2012-01-12/user-data/").read()
    user_data = dict(re.findall(b"\s?export (\w+)+\=\"?([\w\- \.\,\/]+)+\"?", user_data_string))
    user_data = {key.decode(): value.decode() for key,value in user_data.items()}


    # Must have validate false, because of strict IAM rules
    bucket = s3.Bucket(bucket_pattern.format(**user_data))

    user_files = bucket.objects.filter(Prefix=bucket_path.format(**user_data))

    if not os.path.exists(credentials_directory):
        os.makedirs(credentials_directory)

    for f in user_files:
        if not f.key.endswith("/"):  # Is a file
            local_file = f.key.split("/")[-1]
            bucket.download_file(f.key, "%s/%s" % (credentials_directory, local_file))

    with open("%s/settings.yml" % credentials_directory) as settings_file:
        user_env_vars = yaml.safe_load(settings_file)
        if user_env_vars:
            user_data.update(user_env_vars)

    with open("/tmp/envvars", "w") as envvar_file:
        envvar_file.write("\n".join(["export %s=\"%s\"" % itm for itm in user_data.items()]))
