# -*- coding: utf-8 -*-

def display_help():

    help = """
Tailer SDK Help
===============
usage : tailer COMMAND ARGUMENTS


Configure Tailer SDK
--------------------
usage : tailer config


Authenticate with Firebase
--------------------------
usage : tailer auth login


Configuration checking
-----------------------
Please type : tailer check configuration help


Configuration creation
-----------------------
Please type : tailer create configuration help


Configuration deployment
------------------------
Please type : tailer deploy configuration help


Google Cloud Platform Cloud Functions deployment
------------------------------------------------
Please type : tailer deploy gcp-cloud-function help


Encrypt Message of file content
-------------------------------
Will encrypt data using tailer Public Key.

To encrypt a simple message : tailer encrypt "My message to encrypt."
To encrypt file content     : tailer encrypt PATH_TO_A_FILE/the_file.txt


Generate tailer Private and Public keys
---------------------------------------

Please type : tailer generate-keys

"""

    print(help)