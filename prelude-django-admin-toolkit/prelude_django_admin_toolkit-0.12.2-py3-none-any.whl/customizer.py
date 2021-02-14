DIVIDER = 'divider'


class PreludeIndexPage(object):
    
    def __init__(self, template_name=None, show_apps=False):
        '''
        Constructor of PreludeIndexPage
        '''
    
        self.template_name = template_name
        self.show_apps = show_apps
    
    
    def get_context(self, request):
        '''
        Data that it's going to be sent to view; You need to overwrite it in order to send your own data.
        
        Parameters:
            request - Request object that it will be injected into this function before the final rendering; (in case to capture session)
        '''
        
        return {}


class PreludeDefaultIndexPage(PreludeIndexPage):
    
    def __init__(self, *args, **kwargs):
        super(PreludeDefaultIndexPage, self).__init__(*args, **kwargs)
        
        self.template_name = 'admin/includes/index_customized.html'
        self.show_apps = True      
        

class PreludeAdminCustomizer(object):
    
    def __init__(self, site_header=None, site_title=None, show_about=True, enable_pwa=True):
        self.site_header = site_header
        self.site_title = site_title
        
        self.main_menu = []
        
        self.site_css = 'site_default.css'
        self.show_about = show_about
        
        self.configure_index()
        self.enable_pwa = enable_pwa
        
        
        
    def configure_index(self, index = PreludeIndexPage()):
        self.index = index
        

    def register_menu(self, name, icon=None, to=None, items=None):
        menu_item = {
            'name': name,
            'icon': icon,
            'to': to,
            'items': None
        }
       
        if items is not None: 
            normalized_items = [
                {
                    'name': x.get('name', None),
                    'icon': x.get('icon', None),
                    'to': x.get('to', None),
                    'type': x.get('type', 'item')
                } for x in items
            ]
            
            menu_item.update({'items': normalized_items})
        
        self.main_menu.append(menu_item)

    def get_context_vars(self, request):
        
        return {
            'custom_menu': self.main_menu,
            'admin': {
                'site_css': self.site_css,
                'show_about': self.show_about,
                'enable_pwa': self.enable_pwa,
                'index': {
                    'template_name': self.index.template_name,
                    'show_apps': self.index.show_apps,
                    'context': self.index.get_context(request)
                }
            }
        }
        