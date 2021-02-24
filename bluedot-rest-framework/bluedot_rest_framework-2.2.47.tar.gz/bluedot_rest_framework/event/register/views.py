from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response

from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create
from bluedot_rest_framework.utils.jwt_token import jwt_get_wechatid_handler,jwt_get_userid_handler


EventRegister = import_string('event.register.models')
EventRegisterSerializer = import_string('event.register.serializers')
EventRegisterConfig = import_string('event.register.config_models')
EventRegisterConfigSerializer = import_string(
    'event.register.config_serializers')


class EventRegisterView(CustomModelViewSet):
    model_class = EventRegister
    serializer_class = EventRegisterSerializer
    filterset_fields = {
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'event_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)

    @action(detail=False, methods=['get'], url_path='state', url_name='state')
    def state(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        wechat_id = jwt_get_wechatid_handler(request.auth)
        if wechat_id == 0:
            userid=jwt_get_userid_handler(request.auth)
            queryset = self.model_class.objects.filter(
            userid=userid, event_id=event_id).first()
        else:
            queryset = self.model_class.objects.filter(
                wechat_id=wechat_id, event_id=event_id).first()
        state = -1
        if queryset:
            state = queryset.state
        return Response({'state': state})


class EventRegisterConfigView(CustomModelViewSet):
    model_class = EventRegisterConfig
    serializer_class = EventRegisterConfigSerializer
    pagination_class = None

    filterset_fields = {
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().first())
        serializer = self.get_serializer(queryset)
        data = serializer.data
        data['state'] = 1  # 是否可报名
        if data['over_time']:
            now_time = datetime.now()
            over_time = datetime.strptime(
                data['over_time'], '%Y-%m-%dT%H:%M:%S')
            if now_time > over_time:
                data['state'] = 0
        return Response(data)

    def create(self, request, *args, **kwargs):
        data = {
            'event_id': request.data.get('event_id', None),
            'field_list': request.data.get('field_list', []),
            'over_time': request.data.get('over_time', None),
        }
        queryset = self.model_class.objects.filter(
            event_id=data['event_id']).first()
        if queryset:
            queryset.event_id = data['event_id']
            queryset.field_list = data['field_list']
            queryset.over_time = data['over_time']
            queryset.save()
        else:
            self.model_class.objects.create(**data)
        return Response()
