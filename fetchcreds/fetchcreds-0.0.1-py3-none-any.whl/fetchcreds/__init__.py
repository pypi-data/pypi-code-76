import os

def getpassword(service_name):
    stream = os.popen('getpassword.sh ' + service_name)
    output = stream.read()
    return output

def getusername(service_name):
    stream = os.popen('getusername.sh ' + service_name)
    output = stream.read()
    return output
