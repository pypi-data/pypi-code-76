from djangoldp.permissions import LDPPermissions
from django.db.models.base import ModelBase


class CommunityPermissions(LDPPermissions):

    filter_backends = []

    def user_permissions(self, user, model, obj, community=None):
        # Get guardians permissions, over everything else
        perms = set(super().user_permissions(user, model, obj))

        # Communities affiliations list are public
        perms = perms.union({'view'})

        from djangoldp_community.models import Community, CommunityMember
        if community and isinstance(community, Community):

            if model == CommunityMember and community.allow_self_registration:
                perms = perms.union({'add'})

            # Get the user membership, also manage the anonymous user
            try:
                membership = community.members.get(user=user)
            except:
                membership = None

            if membership:
                # Any member can add a job offer, circle or project to the community
                if not model == Community and not model == CommunityMember:
                    perms = perms.union({'add'})

                if membership.is_admin:
                    # Admins can add members
                    perms = perms.union({'add'})

                    if not isinstance(obj, Community) and not obj.is_admin:
                        # Admins can't delete community or other admins, but have super-powers on everything else
                        perms = perms.union({'delete'})

        return list(perms)


    def get_model_or_obj(self, request, view, origin=None):
    
        from djangoldp.models import Model
        if self.is_a_container(request._request.path):
            try:
                # Container have a parent, follow its perms
                obj = Model.resolve_parent(request.path)
                model = view.parent_model
            except:
                # Container have no parent
                obj = None
                model = view.model
        else:
            # Is an object
            obj = Model.resolve_id(request._request.path)
            model = view.model

        if origin:
            # Always follow origins
            if isinstance(origin, ModelBase):
                # Have an origin, is a model
                model = origin
            if not isinstance(origin, ModelBase):
                # Have an origin, is an object
                obj = origin

        from djangoldp_community.models import Community
        # Get the related community, from origin or from the object itself
        if isinstance(origin, Community):
            community = origin
        else:
            community = getattr(obj, 'community', obj)
        
        return community, model, obj


    def filter_user_perms(self, context, origin, permissions):
        # Only used on Model.get_permissions to translate permissions to LDP
        community, model, obj = self.get_model_or_obj(context['request'], context['view'], origin)
        return [perm for perm in permissions if perm in self.user_permissions(context['request'].user, model, obj, community)]


    def has_permission(self, request, view):
        # get permissions required
        community, model, obj = self.get_model_or_obj(request, view)
        perms = self.get_permissions(request.method, model)
        user_perms = self.user_permissions(request.user, model, obj, community)

        # compare them with the permissions I have
        for perm in perms:
            if not perm.split('.')[-1].split('_')[0] in user_perms:
                return False

        return True
