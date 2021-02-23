from djangoldp.views import LDPViewSet
from djangoldp_i18n.serializers import I18nLDPSerializer, I18nContainerSerializer


class I18nLDPViewSet(LDPViewSet):
    '''
    Overrides LDPViewSet to use custom serializer
    '''
    serializer_class = I18nLDPSerializer

    def build_serializer(self, meta_args, name_prefix):
        meta_args['list_serializer_class'] = I18nContainerSerializer

        return super(I18nLDPViewSet, self).build_serializer(meta_args, name_prefix)
