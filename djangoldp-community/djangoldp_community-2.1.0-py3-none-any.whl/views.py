from djangoldp.views import LDPViewSet

class OpenCommunitiesViewset(LDPViewSet):
  def get_queryset(self):
    queryset = super().get_queryset().exclude(allow_self_registration=False)
    # invalidate cache for every open communities, unless that if /open-communities/ is loaded before /communities/xyz/, the last one will get wrong permission nodes
    from djangoldp.permissions import LDPPermissions
    from djangoldp.serializers import LDListMixin, LDPSerializer
    LDPPermissions.invalidate_cache()
    LDListMixin.to_representation_cache.reset()
    for result in queryset:
      if(result.urlid):
        LDPSerializer.to_representation_cache.invalidate(result.urlid)
    return queryset
