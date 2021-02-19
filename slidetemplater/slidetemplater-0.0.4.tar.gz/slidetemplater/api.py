import requests


def convert(powerpoint_file, dataUrl):
    url = "https://api.slidetemplater.com/GeneratePresentation"

    payload = {'JsonDataUrl': 'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&format=json'}

    files = {'file': ('report.pptx', powerpoint_file,
                      'application/vnd.openxmlformats-officedocument.presentationml.presentation', {'Expires': '0'})}

    headers = {}

    response = requests.request(
        "GET", url, headers=headers, data=payload, files=files)

    return response.content
