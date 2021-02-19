import requests
import json

def convert(powerpoint_file, dataUrl="", data={}):
    url = "http://192.168.0.24:7071/GeneratePresentation"
    
    if (dataUrl):
        payload = {'JsonDataUrl': dataUrl}

    if (data):
        payload = {'JsonData': json.dumps(data)}

    files = {'file': ('report.pptx', powerpoint_file,
                      'application/vnd.openxmlformats-officedocument.presentationml.presentation', {'Expires': '0'})}

    headers = {}
    print(payload)
    response = requests.request(
        "GET", url, headers=headers, data=payload, files=files)

    if (response.status_code != 200):
        raise Exception(response.content)
    return response.content
