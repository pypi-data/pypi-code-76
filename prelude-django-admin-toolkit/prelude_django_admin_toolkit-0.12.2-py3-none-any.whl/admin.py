from django.contrib import admin
from django.conf import settings

from prelude_django_admin_toolkit.customizer import PreludeAdminCustomizer
from django.shortcuts import render


'''
class PrlActionForm(helpers.ActionForm):
    action = forms.ChoiceField()
    action.widget.attrs.update({
        'class': 'uk-select uk-width-1-1 uk-padding-remove-right'
    }) 
'''


class PrlModelAdmin(admin.ModelAdmin):
    #form = PrlModelForm
    #action_form = PrlActionForm
    save_as = True
    list_per_page = 50


class PrlAdmin(admin.AdminSite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Custom settings Dict
        custom_settings = getattr(settings, 'PRELUDE_ADMIN', None)
       
        # If you haven't set a custom settings, create one
        if custom_settings is None:
            custom_settings = {
                'customizer_object': PreludeAdminCustomizer()
            }
            
        self.prl_customizer = custom_settings['customizer_object']
        self.load_customizer()
    
    def load_customizer(self):
        if self.prl_customizer.site_header:
            self.site_header = self.prl_customizer.site_header
        
        if self.prl_customizer.site_title:
            self.site_title = self.prl_customizer.site_title
        
        self.show_about = self.prl_customizer.show_about
    
    def each_context(self, request):
        context_vars = super().each_context(request)
       
        context_vars.update(self.prl_customizer.get_context_vars(request))
 
        return context_vars
     
    def page_about(self, request):
        return render(request, 'admin/pages/about.html', self.each_context(request))
    
    def get_urls(self):
        from django.urls import path

        url_patterns = super().get_urls()
        
        if self.show_about:
            url_patterns.append(
                path('about/', self.admin_view(self.page_about), name='about')
            )
        
        return url_patterns

    '''
    @never_cache
    def index(self, request, extra_context=None):
        
        context = {'name': 'JON123456'}
        
        return admin.AdminSite.index(self, request, extra_context=context)
    '''

site = PrlAdmin()

from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

site.register(User, UserAdmin)
site.register(Group, GroupAdmin)
