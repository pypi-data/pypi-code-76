import random
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework.wechat import App
from .models import WeChatResponseMaterial, WeChatResponseEvent
from .serializers import WeChatResponseMaterialSerializer, WeChatResponseEventSerializer


class WeChatResponseMaterialView(CustomModelViewSet, AllView):
    model_class = WeChatResponseMaterial
    serializer_class = WeChatResponseMaterialSerializer

    filterset_fields = {
        'material_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        },
    }


class WeChatResponseEventView(CustomModelViewSet):
    model_class = WeChatResponseEvent
    serializer_class = WeChatResponseEventSerializer

    filterset_fields = {
        'event_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        },
    }

    def perform_create(self, serializer):
        if self.request.data.get('event_type') == 2:
            event_key = str(random.uniform(1, 10))
            result = App(self.request.data.get('appid')).qrcode.create({
                'action_name': 'QR_LIMIT_STR_SCENE',
                'action_info': {
                    'scene': {'scene_str': event_key},
                }
            })
            qrcode_ticket = result['ticket']
            serializer.save(event_key=event_key, qrcode_ticket=qrcode_ticket)
        else:
            serializer.save()
