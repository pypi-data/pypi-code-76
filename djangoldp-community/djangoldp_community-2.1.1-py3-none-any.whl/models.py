import uuid
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from djangoldp.models import Model
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from djangoldp_community.permissions import CommunityPermissions, CommunityCirclePermissions, \
    CommunityProjectPermissions
from djangoldp_community.views import CommunityMembersViewset

from djangoldp_circle.models import Circle
from djangoldp_project.models import Project
from djangoldp_joboffer.models import JobOffer

class Community(Model):
    name = models.CharField(max_length=255, blank=True, help_text="Changing a community's name is highly discouraged")
    logo = models.URLField(blank=True, null=True)
    allow_self_registration = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.urlid)

    class Meta(Model.Meta):
        verbose_name = _('community')
        verbose_name_plural = _("communities")
        permission_classes = [CommunityPermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        lookup_field = 'slug'
        container_path = "/communities/"
        ordering = ['slug']
        serializer_fields = ['@id', 'name', 'logo', 'allow_self_registration', 'projects', 'circles', 'members', 'joboffers']
        rdf_type = "sib:Community"

class CommunityMember(Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='members', null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="communities", null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    class Meta(Model.Meta):
        verbose_name = _('community member')
        verbose_name_plural = _("community members")
        view_set = CommunityMembersViewset
        permission_classes = [CommunityPermissions]
        anonymous_perms = ['view', 'add']
        authenticated_perms = ['inherit']
        superuser_perms = ['view', 'add']
        container_path = "community-members/"
        serializer_fields = ['@id', 'community', 'user', 'is_admin']
        rdf_type = "as:items"

class CommunityCircle(Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='circles', null=True, blank=True)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name="communities", null=True, blank=True)

    class Meta(Model.Meta):
        verbose_name = _('community circle')
        verbose_name_plural = _("community circles")
        permission_classes = [CommunityPermissions, CommunityCirclePermissions]
        anonymous_perms = []
        authenticated_perms = []
        superuser_perms = []
        container_path = "community-circles/"
        serializer_fields = ['@id', 'community', 'circle']
        rdf_type = "as:items"

class CommunityProject(Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="communities", null=True, blank=True)

    class Meta(Model.Meta):
        verbose_name = _('community project')
        verbose_name_plural = _("community projects")
        permission_classes = [CommunityPermissions, CommunityProjectPermissions]
        anonymous_perms = []
        authenticated_perms = []
        superuser_perms = []
        container_path = "community-projects/"
        serializer_fields = ['@id', 'community', 'project']
        rdf_type = "as:items"

class CommunityJobOffer(Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='joboffers', null=True, blank=True)
    joboffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name="communities", null=True, blank=True)

    class Meta(Model.Meta):
        verbose_name = _('community job offer')
        verbose_name_plural = _("community job offers")
        permission_classes = [CommunityPermissions]
        anonymous_perms = []
        authenticated_perms = []
        superuser_perms = []
        container_path = "community-joboffers/"
        serializer_fields = ['@id', 'community', 'joboffer']
        rdf_type = "as:items"

@receiver(pre_save, sender=Community)
def pre_create_account(sender, instance, **kwargs):
    if not instance.urlid or instance.urlid.startswith(settings.SITE_URL):
        if getattr(instance, Model.slug_field(instance)) != slugify(instance.name):
            if Community.objects.filter(slug=slugify(instance.name)).count() > 0:
                raise Exception(_("Name already taken"))
            setattr(instance, Model.slug_field(instance), slugify(instance.name))
            setattr(instance, "urlid", "")
    else:
        # Is a distant object, generate a random slug
        setattr(instance, Model.slug_field(instance), uuid.uuid4().hex.upper()[0:8])
