"""appel_crises URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from appel_crises.api import (
    sign,
    search_depute,
    get_csrf_token,
    call_out_ajax,
    call_out,
    sign_ajax,
    version,
)
from appel_crises.views import (
    home,
    success,
    form_no_js,
    success_email,
    call_out_no_js,
    legal_notice,
    test_error_reporting,
)

urlpatterns = [
    path('examiner/', admin.site.urls),
    path('confirmation', success, name='success'),
    path('confirmation-courriel', success_email, name='success-email'),
    path('api/call-out', call_out, name='call-out'),
    path('api/call-out-ajax', call_out_ajax, name='call-out-ajaxs'),
    path('api/sign', sign, name='sign'),
    path('api/sign-ajax', sign_ajax, name='sign-ajax'),
    path('api/search-depute', search_depute, name='search-depute'),
    path('api/csrf', get_csrf_token, name='get-csrf'),
    path('', home, name="home"),
    path('signer', form_no_js, name="form-no-js"),
    path('interpeller-ses-elus', call_out_no_js, name="call-out-no-js"),
    path('mentions-legales', legal_notice, name='legal-notice'),
    path('test-error-reporting', test_error_reporting),
    path('version', version),
]
