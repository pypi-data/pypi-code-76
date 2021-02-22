from django.contrib import admin
from djangoldp_i18n.admin import DjangoLDPI18nAdmin
from djangoldp_skill.models import Skill

class SkillAdmin(DjangoLDPI18nAdmin):
    pass

admin.site.register(Skill, SkillAdmin)
