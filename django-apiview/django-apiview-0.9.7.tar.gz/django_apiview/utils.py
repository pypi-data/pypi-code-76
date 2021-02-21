import json
import inspect
import binascii
import datetime

import bizerror
from fastutils.jsonutils import SimpleJsonEncoder
from fastutils.cacheutils import get_cached_value
from fastutils.typingutils import smart_cast

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder as DjangoJSONEncoderBase
from django.forms.models import model_to_dict
from django.core import serializers
from django.utils import timezone

def encode_model(o):
    text = serializers.serialize("json", [o])
    results = json.loads(text)
    obj = results[0]["fields"]
    obj["pk"] = results[0]["pk"]
    return obj

def encode_queryset(q):
    text = serializers.serialize("json", q)
    results = json.loads(text)
    data = []
    for result in results:
        obj = result["fields"]
        obj["pk"] = result["pk"]
        data.append(obj)
    return data

def encode_datetime(value):
    return timezone.make_naive(value).strftime("%Y-%m-%d %H:%M:%S")

SimpleJsonEncoder.library.register(models.Model, encode_model)
SimpleJsonEncoder.library.register(models.QuerySet, encode_queryset)
SimpleJsonEncoder.library.register(datetime.datetime, encode_datetime)

def _get_request_data(request, extra_view_parameters):
    data = {"_request": request}
    data.update(extra_view_parameters)
    for name, _ in request.GET.items():
        value = request.GET.getlist(name)
        if isinstance(value, (list, tuple, set)) and len(value) == 1:
            data[name] = value[0]
        else:
            data[name] = value
    for name, _ in request.POST.items():
        value = request.POST.getlist(name)
        if isinstance(value, (list, tuple, set)) and len(value) == 1:
            data[name] = value[0]
        else:
            data[name] = value
    if request.body:
        try:
            payload = json.loads(request.body)
            data["_form"] = payload
            data.update(payload)
        except:
            pass
    for name, fobj in request.FILES.items():
        data[name] = fobj
    return data

def get_request_data(request, extra_view_parameters):
    return get_cached_value(request, "_django_apiview_request_data", _get_request_data, request, extra_view_parameters)
