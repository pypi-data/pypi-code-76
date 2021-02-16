from Products.Five import BrowserView


class UfficiListView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def filtered_offices_list(self, item_list):
        return [x for x in item_list if x.portal_type == 'Ufficio']

    def get_phone(self,item):
         return item.getObject().phone

    def get_email(self,item):
         return item.getObject().email

    def get_pec(self,item):
         return item.getObject().pec

    def get_url(self,item):
         return item.getObject().absolute_url()
