from django.contrib import admin, messages
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from appel_crises.models import Signature, CallOutEmail, BlackListedEmail

admin.site.unregister(Group)
admin.site.unregister(User)


class MyUserChangeForm(UserChangeForm):
    class Meta:
        fields = ["username", "password", "email", "is_active", "is_staff", "groups"]


@admin.register(User)
class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups')}),
    )


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    list_filter = ("created_at", 'has_captcha_verified', 'manually_verified_at')
    list_display = (
        'email',
        'surname',
        'first_name',
        'created_at',
        'has_captcha_verified',
        'manually_verified_at',
        'email_sent_at',
        'email_verified_at',
    )
    readonly_fields = (
        "created_at",
        "email",
        "first_name",
        "surname",
        "news",
        "added_to_newsletter_list",
        "has_captcha_verified",
        # "manually_verified_at",
        "email_sent_at",
        "email_verified_at",
    )

    actions = ["validate_signatures"]

    def validate_signatures(self, request, queryset):
        n_updated = queryset.update(manually_verified_at=timezone.now())
        messages.success(
            request, "{} signatures marquées comme vérifiées".format(n_updated)
        )

    validate_signatures.short_description = (
        "Marquer les signatures comme vérifiées à la main"
    )

    def has_change_permission(self, request, obj: Signature = None):
        if obj is not None:
            # we only want to be able do mark manually verified email that come from
            # no-JS, they are the ones marked as has_captcha_verified=False
            if obj.has_captcha_verified:
                return False

        dpo_group = Group.objects.get(name='DPO')
        reviewer_group = Group.objects.get(name='reviewers')
        user_groups = request.user.groups.all()
        return dpo_group in user_groups or reviewer_group in user_groups

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CallOutEmail)
class CallOutEmailAdmin(admin.ModelAdmin):
    list_filter = ("created_at",)
    search_fields = ('email',)
    list_display = (
        'from_email',
        'sender',
        'postal_code',
        'circonscription_numbers',
        'send_to_government',
        'created_at',
        'email_sent_at',
        'verified_at',
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# This list is completely managed by an admin
admin.site.register(BlackListedEmail)
