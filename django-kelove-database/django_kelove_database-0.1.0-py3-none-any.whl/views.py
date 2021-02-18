"""
views.py
By IT小强xqitw.cn <mail@xqitw.cn>
At 2/2/21 11:18 AM
"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .ckfinder.ckfinder import Ckfinder
from .models import CkfinderResource
from .kelove_settings import CkfinderFieldSettings


def ckfinder(request):
    return render(request, 'kelove_database/ckfinder/ckfinder.html', {
        "ck_finder_api_url": reverse('django_kelove_database:ckfinder_api'),
        "ck_finder_api_display_folders_panel": 0
    })


@csrf_exempt
def ckfinder_api(request):
    """
    ckfinder api
    :param request:
    :return:
    """

    file = {}
    file_obj = request.FILES.get('upload', None)
    if file_obj:
        file['name'] = file_obj.name
        file['file'] = file_obj.file
    _ckfinder = Ckfinder(
        request.GET,
        request.POST,
        file,
        CkfinderFieldSettings.get_server_settings()
    )
    all_permissions = request.user.get_all_permissions()
    resource_config = CkfinderResource.objects.filter(enabled=True).all()
    for i in resource_config:
        _ckfinder.add_resource(
            **i.get_resource()
        ).add_rule(i.get_rule(all_permissions))

    response_data = _ckfinder.run()

    if response_data['content_type'].lower() == 'application/json':
        response = JsonResponse(data=response_data['content'])
    else:
        response = HttpResponse(
            content=response_data['content'],
            content_type=response_data['content_type'],
        )
    response.status_code = response_data['status_code']

    for header_key, header_val in response_data['headers'].items():
        response[header_key] = header_val
    return response
