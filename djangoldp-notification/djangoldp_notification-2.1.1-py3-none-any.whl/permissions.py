from django.contrib.auth import get_user_model

from djangoldp.permissions import LDPPermissions
from djangoldp_notification.filters import InboxFilterBackend, SubscriptionsFilterBackend
from rest_framework.reverse import reverse


class InboxPermissions(LDPPermissions):
    filter_backends = [InboxFilterBackend]

    def has_permission(self, request, view):
        from djangoldp.models import Model

        if self.is_a_container(request._request.path):
            try:
                """
                If on nested field we use users permissions
                """
                obj = Model.resolve_parent(request.path)
                model = view.parent_model

                """
                If still on nested field and request is post (/users/X/inbox/) we use notification permissions
                """
                if view.parent_model != view.model and request.method == 'POST':
                    obj = None
                    model = view.model
            except:
                """
                Not on nested field we use notification permissions
                """
                obj = None
                model = view.model
        else:
            obj = Model.resolve_id(request._request.path)
            model = view.model

        perms = self.get_permissions(request.method, model)

        for perm in perms:
            if not perm.split('.')[1].split('_')[0] in self.user_permissions(request.user, model, obj):
                return False

        return True


class SubscriptionsPermissions(LDPPermissions):
    filter_backends = [SubscriptionsFilterBackend]

    def has_permission(self, request, view):
        if request.user.is_anonymous and not request.method == "OPTIONS":
            return False

        if request.method in ["GET", "PATCH", "DELETE", "PUT"]:
            return True

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous and not request.method == "OPTIONS":
            return False

        reverse_path_key = "{}-notification-list".format(get_user_model()._meta.object_name.lower())
        user_inbox = reverse(reverse_path_key, kwargs={"slug": request.user.slug}, request=request)
        if obj.inbox == user_inbox:
            return True

        return False
