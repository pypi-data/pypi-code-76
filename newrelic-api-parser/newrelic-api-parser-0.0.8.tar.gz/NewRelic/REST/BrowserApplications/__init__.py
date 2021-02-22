from NewRelic.Base import BaseNewRelic
from NewRelic.CustomExceptions import ArgumentException

class BrowserApplications(BaseNewRelic):

    def __init__(self, API_KEY: str):
        super().__init__(API_KEY)

    def get_list(self) -> dict:
        """
        fetch the browser applications for new relic
        """
        url = self.BASE_URI + '/browser_applications.json'
        return super().get_data(url)

    def create(self, browser_application_name: str) -> dict:
        """
        create a browser application
        """
        try:
            url = self.BASE_URI + '/browser_applications.json'
            if browser_application_name is None or browser_application_name == '':
                raise ArgumentException
            data = {
                'browser_application': {
                    'name': browser_application_name
                }
            }
            return super().post_data(url, data=data)
        except ArgumentException as ae:
            return None
        except Exception as ex:
            return None