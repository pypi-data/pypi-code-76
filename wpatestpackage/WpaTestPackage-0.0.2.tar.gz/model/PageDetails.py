class PageDetails(object):
    buildId=int()
    pageTitle=str()
    applicationName=str()
    typeScan = "Automation"

    def __init__(self,buildId,pageTitle,applicationName):
        self.buildId=buildId
        self.pageTitle=pageTitle
        self.applicationName=applicationName
        self.typeScan="Automation"

    def set_build_id(self, buildId):
        self.buildId = buildId

    def get_build_id(self):
        return self.build_id

    def set_page_title(self, pageTitle):
        self.pageTitle = pageTitle

    def get_page_title(self):
        return self.pageTitle

    def set_application_name(self, applicationName):
        self.applicationName = applicationName

    def get_application_name(self):
        return self.application_name

    def set_type_scan(self, typeScan):
        self.typeScan = typeScan

    def get_type_scan(self):
        return self.typeScan