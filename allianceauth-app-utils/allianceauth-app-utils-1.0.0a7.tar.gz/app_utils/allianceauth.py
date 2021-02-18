from django.contrib.auth.models import User, Permission
from django.db.models import Q

from allianceauth.views import NightModeRedirectView
from allianceauth.notifications import notify


def notify_admins(message: str, title: str, level="info") -> None:
    """send notification to all admins"""
    try:
        perm = Permission.objects.get(codename="logging_notifications")
        users = User.objects.filter(
            Q(groups__permissions=perm)
            | Q(user_permissions=perm)
            | Q(is_superuser=True)
        ).distinct()

        for user in users:
            notify(user, title=title, message=message, level=level)
    except Permission.DoesNotExist:
        pass


def is_night_mode(request) -> bool:
    """Returns True if the current user session is in night mode, else False"""
    return NightModeRedirectView.night_mode_state(request)
