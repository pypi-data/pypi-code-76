
from ioc_finder import find_iocs

class Extract_datatype:

    def __init__(self):

        a =1

    def url(self, content):

        iocs = find_iocs(content)
        return iocs.get('urls', [])


    def domain(self, content):

        iocs = find_iocs(content)
        return iocs.get('domains', [])

    def email(self, content):
        
        iocs = find_iocs(content)
        return iocs.get('email_addresses', [])

    def phone(self, content):
        
        iocs = find_iocs(content)
        return iocs.get('phone_numbers', [])


    def google_analytics(self, content):
        
        iocs = find_iocs(content)
        return iocs.get('google_analytics_tracker_ids', [])


