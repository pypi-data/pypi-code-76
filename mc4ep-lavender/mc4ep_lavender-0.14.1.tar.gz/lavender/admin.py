from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from lavender.models import Package, Player, LogHistory, GameLog, Quenta


class PlayerAdmin(UserAdmin):
    filter_horizontal = ('packages',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            perm_fields = ('is_active', 'is_staff')

        return [
            (None, {'fields': ('username', 'password')}),
            (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
            (_('Permissions'), {'fields': perm_fields}),
            ('Minecraft', {'fields': ('packages',)})
        ]


class LogHistoryAdmin(ModelAdmin):
    list_filter = ('date', 'source')
    list_display = ('player', 'date', 'source')
    search_fields = (
        'player__username',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('player')


class GameLogAdmin(ModelAdmin):
    list_display = ('player', 'date', 'kind',)
    list_filter = ('date', 'kind')
    search_fields = (
        'player__username',
        'kind'
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('player')


class QuentaAdmin(ModelAdmin):
    list_display = ('player', 'approved',)
    list_filter = ('approved',)
    search_fields = (
        'player__username',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('player')


class PackageAdmin(ModelAdmin):
    list_display = ('name', 'version', 'title', 'location', 'is_default')
    list_filter = ('is_default',)


admin.site.register(Player, PlayerAdmin)
admin.site.register(LogHistory, LogHistoryAdmin)
admin.site.register(GameLog, GameLogAdmin)
admin.site.register(Quenta, QuentaAdmin)
admin.site.register(Package, PackageAdmin)
