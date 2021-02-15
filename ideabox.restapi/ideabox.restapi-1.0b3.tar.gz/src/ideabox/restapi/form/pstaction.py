# -*- coding: utf-8 -*-

from ideabox.policy.content.campaign import ICampaign
from ideabox.restapi import _
from imio.restapi.form.form import ImportForm
from imio.restapi.form.importer import BaseContentImporter
from plone.app.z3cform.widget import SelectFieldWidget
from plone.z3cform.layout import FormWrapper
from z3c.form.field import Fields
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IPSTActionImportSchema(Interface):

    import_list = schema.List(
        title=_(u"List of PST Actions that you want to import"),
        description=_(
            u"This list contains only PST Actions that was not already imported"
        ),
        value_type=schema.Choice(
            title=u"document", vocabulary="ideabox.restapi.vocabularies:pstaction",
        ),
    )


class PSTActionImportForm(ImportForm):
    _application_id = "PST"
    fields = Fields(IPSTActionImportSchema)

    def update(self):
        self.fields["import_list"].widgetFactory = SelectFieldWidget
        super(PSTActionImportForm, self).update()

    def _get_data(self, data):
        return data["import_list"]


class PSTActionImportFormView(FormWrapper):
    form = PSTActionImportForm


@adapter(dict, ICampaign)
class PSTActionImporter(BaseContentImporter):
    _fields = [
        "title",
        "description_rich",
        "operational_objective",
        "strategic_objective",
    ]

    def transform_data(self, data):
        data["@type"] = "priority_action"
        data["strategic_objectives"] = data["strategic_objective"]["original_title"]
        del data["strategic_objective"]
        data["operational_objectives"] = data["operational_objective"]["original_title"]
        del data["operational_objective"]
        data["body"] = data["description_rich"]
        del data["description_rich"]
        return data
