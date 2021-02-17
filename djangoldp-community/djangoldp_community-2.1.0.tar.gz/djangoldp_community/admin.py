from django.contrib import admin
from djangoldp.admin import DjangoLDPAdmin
from djangoldp_community.models import Community, CommunityMember, CommunityCircle, CommunityProject, CommunityJobOffer


class MemberInline(admin.TabularInline):
    model = CommunityMember
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class CircleInline(admin.TabularInline):
    model = CommunityCircle
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class ProjectInline(admin.TabularInline):
    model = CommunityProject
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class JobOfferInline(admin.TabularInline):
    model = CommunityJobOffer
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class CommunityAdmin(DjangoLDPAdmin):
    exclude = ('slug', 'is_backlink', 'allow_create_backlink')
    inlines = [MemberInline, CircleInline, ProjectInline, JobOfferInline]


admin.site.register(Community, CommunityAdmin)
