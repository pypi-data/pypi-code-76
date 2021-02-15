# -*- coding: utf-8 -*-

from ideabox.policy.content.campaign import ICampaign
from ideabox.policy.content.priority_action import IPriorityAction
from ideabox.restapi import _
from imio.restapi.form.action import RESTAction
from zope.component import adapter
from zope.publisher.interfaces.browser import IBrowserRequest


@adapter(ICampaign, IBrowserRequest)
class PSTActionImportAction(RESTAction):
    title = _(u"Import PST Actions")
    application_id = u"PST"
    schema_name = None
    view_name = "pstaction-import-form"


@adapter(IPriorityAction, IBrowserRequest)
class PSTActionImportProgress(RESTAction):
    title = _(u"Import PST Progresses")
    application_id = u"PST"
    schema_name = None
    view_name = "pstaction-progress-import-form"
