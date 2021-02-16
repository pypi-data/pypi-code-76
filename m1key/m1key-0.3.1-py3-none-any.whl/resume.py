import requests
import os


def download_resume():
    url = "https://raw.githubusercontent.com/m1-key/Media/main/Mithilesh's%20Resume.pdf"
    r = requests.get(url, allow_redirects=True)
    if not os.path.exists('Mithilesh_Resume.pdf'):
        open('Mithilesh_Resume.pdf', 'wb').write(r.content)
        print("Resume has been downloaded in the current directory with the name Mithilesh_Resume.pdf")
    else:
        print("Resume is already downloaded with the name Mithilesh_Resume.pdf, please check the current directory carefully")
