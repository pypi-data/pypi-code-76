import redminelib
import keyring
import os

redmine_url = 'https://redmine.isdc.unige.ch/'

def connect():
    for n, m in [
                    ('environ', lambda:(
                            os.environ.get('REDMINE_USERNAME').strip(),
                            os.environ.get('REDMINE_PASSWORD').strip(),
                        ),
                    ),
                    ('keyring', lambda:(
                            keyring.get_password('redmine', 'username'),
                            keyring.get_password('redmine', 'password')
                        ),
                    ),
                ]:
        try:
            username, password = m()
            break
        except Exception as e:
            print("failed to get credentials", n, e)
    

    print("got credentials for", username)

    redmine = redminelib.Redmine(redmine_url, 
                       username=username, 
                       password=password)
    return redmine

