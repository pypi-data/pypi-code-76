import requests
from getpass import getpass
from termcolor import cprint

import webbrowser, requests
import inquirer

url = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["url"]
banner = """
|_|  _   _ _|_ |_|  _  ._ _   _  
| | (_) _>  |_ | | (_) | | | (/_    - pip                                   
"""

def login():
    
    print(banner)

    questions = [
        inquirer.Text('mail', message="Escribe tu email"),
    ]
    answers = inquirer.prompt(questions)

    mail = answers["mail"]
    psw = getpass("[?] Escribe tu contraseña: ")
    
    data = requests.post(f"{url}login?psw={psw}&mail={mail}").json()

    # print(data)

    if str(data) == "{}":
        cprint("Esa cuenta no existe intentalo otra vez", "red")
        answers = inquirer.prompt([inquirer.Confirm('si_no',
                message="Should I stop", default=True)])
        if answers["si_no"]:
            webbrowser.open(f'{url}register', new=2)
            return login()
        else:
            cprint("Veo que no", "red")
            exit(0)

    return data
