import os

from awscli.customizations.configure.writer import ConfigFileWriter
from botocore.session import get_session


def update_aws_creds(access_token, user_email, aws_profile_name, silent):
    if not user_email:
        raise Exception("User email not returned from Cyral server")
    # we use the botocore and awscli existing code to get this done.
    session = get_session()
    creds_path = session.get_config_variable("credentials_file")
    creds_path = os.path.expanduser(creds_path)

    values = {
        "aws_access_key_id": f"{user_email}:{access_token}",
        "aws_secret_access_key": "none",
        "__section__": aws_profile_name,
    }
    w = ConfigFileWriter()
    # this will create or update the profile as needed.
    w.update_config(values, creds_path)
    if not silent:
        print(f"Updated S3 token for AWS profile '{aws_profile_name}' 🎉")
        if aws_profile_name != "default":
            print(
                "\nTo use this profile, specify the profile name using "
                "--profile, as shown:\n\n"
                f"aws s3 ls --profile {aws_profile_name}\n"
            )
