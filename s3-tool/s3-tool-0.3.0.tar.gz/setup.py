# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_tool', 's3_tool.choices']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.20,<2.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'tqdm>=4.47.0,<5.0.0',
 'typer[all]>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['s3-tool = s3_tool.main:app']}

setup_kwargs = {
    'name': 's3-tool',
    'version': '0.3.0',
    'description': 'S3 CLI Tool to execute basic commands',
    'long_description': '# S3 Command Line Utility\n\n### Credentials\n\nFirst of all, you will need to have your credentials ready.\nThe following are needed (next to them are the names of the environmental variables associated to them):\n\n- Endpoint `ENDPOINT`\n- Access Key `ACCESS_KEY`\n- Secret Access Key `SECRET_ACCESS_KEY`\n- Bucket `BUCKET`\n- OPTIONALLY: if you have an HTTP prefix for accessing keys over a web browser you can add it with the `HTTP_PREFIX` variable\n\nIn order to avoid having to introduce your credentials after every command execution it is possible to store them as environmental variables.\nYou can even do this temporarily setting a variables as `export ENDPOINT_URL=MyURL`. This way, your credentials will only be set for the current terminal.\n\n### Operations\n\nThe following operations are possible:\n\n- Listing all keys in a bucket\n- Listing keys according to a prefix in a bucket\n- Change key permissions to public-read\n- Upload any number of keys. Is Multithreaded.\n- Download any number of keys. Is Multithreaded.\n- Delete keys. Is Multithreaded.\n\n---\n\n**Usage**:\n\n```console\n$ s3-tool [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n- `--install-completion`: Install completion for the current shell.\n- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n- `--help`: Show this message and exit.\n\n**Commands**:\n\n- `change-permissions`: Takes any number of keys and changes their...\n- `create-upload-list`: Writes a text file of all files in a folder...\n- `delete-key`: USE WITH EXTREME CAUTION! Deletes a given key...\n- `download`: Downloads a key or series of keys\n- `list-keys`: Lists keys according to a given prefix\n- `list-keys-v2`: Lists keys using S3 client. Allows for using a delimiter to limit the output to "subfolders"\n- `upload`: Uploads a single file or multiple files.\n\n## `s3-tool change-permissions`\n\nTakes any number of keys and changes their permissions to public-read\n\n**Usage**:\n\n```console\n$ s3-tool change-permissions [OPTIONS] ARGS...\n```\n\n**Options**:\n\n- `--prefix-threads INTEGER`: Sets the amount of prefixes that should be queried in parallel.\n- `--changer-threads INTEGER`: Sets the amount of threads used to change permissions for a given prefix.\n- `-p, --permissions [private|public-read|public-read-write|authenticated-read|aws-exec-read|bucket-owner-read|bucket-owner-full-control]`: Changes the keys permissions.\n- `--help`: Show this message and exit.\n\n## `s3-tool create-upload-list`\n\nWrites a text file of all files in a folder with a given extension that\ncan be used together with the upload command to upload multiple files\nat once\n\n**Usage**:\n\n```console\n$ s3-tool create-upload-list [OPTIONS] FILES_PATH FILE_EXTENSION\n```\n\n**Options**:\n\n- `--output-path TEXT`: Choose an output path. Else, the file will be written on the folder where the command is executed.\n- `--help`: Show this message and exit.\n\n## `s3-tool delete-key`\n\nUSE WITH EXTREME CAUTION! Deletes a given key or keys\n\n**Usage**:\n\n```console\n$ s3-tool delete-key [OPTIONS]\n```\n\n**Options**:\n\n- `-f, --files TEXT`: Keys to be deleted.\n- `--prompt / --no-prompt`: Display a prompt to confirm deletion.\n- `--threads INTEGER`: Set the amount of threads to delete keys in parallel. Disable the prompt if using this option.\n- `--help`: Show this message and exit.\n\n## `s3-tool download`\n\nDownloads a key or series of keys\n\n**Usage**:\n\n```console\n$ s3-tool download [OPTIONS] DOWNLOAD_PATH\n```\n\n**Options**:\n\n- `-f, --files TEXT`: Either a file or files, or a text file containing paths to files separated by commas (,).\n- `-t, --threads INTEGER`: Amount of threads used to download in parallel.\n- `--help`: Show this message and exit.\n\n## `s3-tool list-keys`\n\nLists keys according to a given prefix\n\n**Usage**:\n\n```console\n$ s3-tool list-keys [OPTIONS]\n```\n\n**Options**:\n\n- `-p, --prefix TEXT`: Prefix to look for keys.\n- `-d, --delimiter TEXT`: A delimiter is a character you use to group keys.\n- ` --max-keys, -mk INTEGER`: Sets the maximum number of keys returned in the response. The response might contain fewer keys but will never contain more.\n- `-hp, --http-prefix`: Append HTTP URL Prefix to keys.\n- `--all / --no-all`: USE WITH CAUTION! If True, will fetch every key in the Bucket.\n- `-l, --limit INTEGER`: Limits the amount of keys returned.\n- `-km, --key-methods [key|last_modified|size|owner]`\n- `--help`: Show this message and exit.\n\n## `s3-tool list-keys-v2`\n\nLists keys using the S3 client rather than Resource (used for thelist-keys command). Allows the usage of a delimiter to limit the output to "subfolders". Only operation not possible is the checking of ACL Grants.\n\n**Usage**:\n\n```console\n$ s3-tool list-keys-v2 [OPTIONS]\n```\n\n**Options**:\n\n* `-p, --prefix TEXT`: Prefix to look for keys  [default: source/]\n* `-d, --delimiter TEXT`: A delimiter is a character you use to group keys.  [default: ]\n* ` --max-keys, -mk INTEGER`: Sets the maximum number of keys returned in the response. The response might contain fewer keys but will never contain more.  [default: 1000]\n* `-hp, --http-prefix`: Append HTTP URL Prefix to keys  [default: False]\n* `-km, --key-methods [key|last_modified|size|owner]`\n* `--help`: Show this message and exit.\n\n## `s3-tool upload`\n\nUploads a single file or multiple files. Files need to have their absolute path.\nThe last argument passed will be the upload path.\nOptionally, one can choose the amount of threads that should be used.\n\n**Usage**:\n\n```console\n$ s3-tool upload [OPTIONS] UPLOAD_PATH\n```\n\n**Options**:\n\n- `-f, --files TEXT`: Chose either a file or files with absolute path.\n- `-uff, --upload-from-file TEXT`: Upload using text file containing paths to files separated by commas (,).\n- `--permissions TEXT`: Sets the permission for the uploaded file. Options are: \'private\' | \'public-read\' | \'public-read-write\' | \'authenticated-read\' | \'aws-exec-read\' | \'bucket-owner-read\' | \'bucket-owner-full-control\'\n- `--worker-threads INTEGER`: Amount of threads used to upload in parallel.\n- `--help`: Show this message and exit.\n',
    'author': 'Ivan Andre Scheel',
    'author_email': 'andrescheel@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/necromeo/s3-tool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
