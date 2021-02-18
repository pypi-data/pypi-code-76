class Ganjang:
    def __init__(self, url_staging, url_prod, name_delemeter):
        self.STAGING_URL = url_staging
        self.PRODUCTION_URL = url_prod
        self.BASE_NAME = self.base_url(name_delemeter)
        
    
    def base_url(self, name_delemeter):
        reference_url = self.PRODUCTION_URL
        spam_loc=reference_url.find(name_delemeter)
        return reference_url[spam_loc+len(name_delemeter):].replace('/','-')