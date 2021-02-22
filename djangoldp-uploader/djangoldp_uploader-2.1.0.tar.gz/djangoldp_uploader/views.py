from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from djangoldp_uploader.forms import DocumentForm
from djangoldp_uploader.models import Document


def home(request):
    documents = Document.objects.all()
    return render(request, 'home.html', { 'documents': documents })


def demo_sib(request):
    return render(request, 'demo_sib.html')


def upload(request):
    file_obj = request.FILES['file']
    fs = FileSystemStorage()
    filename = fs.save(file_obj.name, file_obj)
    uploaded_file_url = fs.url(filename)
    return uploaded_file_url


class FileUploadView(APIView):
    def dispatch(self, request, *args, **kwargs):
        # TODO: This completely disable CSRF verification but this should be handled properly
        # Context: Django REST framework always enforce CSRF verification when user is connected
        # (see https://www.django-rest-framework.org/api-guide/testing/#csrf)
        # Usage of `csrf_exempt` is useless. The front should handle this properly by renewing
        # CSRF before performing the POST request. `csrf_processing_done` is used up to Django 2.2
        # (see https://github.com/django/django/blob/master/django/middleware/csrf.py#L206)
        # but is not documented AFAIK. So this fix could be broken in Django 3.
        request.csrf_processing_done = True
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if request.method == 'POST' and request.FILES['file']:
            uploaded_file_url = upload(request)
            response = Response(status=204, headers={'Location': "{}{}".format(settings.SITE_URL, uploaded_file_url)})
            response["Access-Control-Allow-Origin"] = request.META.get('HTTP_ORIGIN')
            response["Access-Control-Allow-Methods"] = "GET,POST,PUT,PATCH,DELETE"
            response["Access-Control-Allow-Headers"] = "authorization, Content-Type, if-match, accept"
            response["Access-Control-Expose-Headers"] = "Location"
            response["Access-Control-Allow-Credentials"] = 'true'
            
            return response


def upload_view(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file_url = upload(request)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })
