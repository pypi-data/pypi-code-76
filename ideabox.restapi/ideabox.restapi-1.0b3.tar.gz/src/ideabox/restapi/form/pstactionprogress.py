# -*- coding: utf-8 -*-

from ideabox.policy.content.priority_action import IPriorityAction
from ideabox.restapi import _
from imio.restapi.form.form import ImportForm
from imio.restapi.form.importer import BaseContentImporter
from plone.app.z3cform.widget import SelectFieldWidget
from plone.z3cform.layout import FormWrapper
from z3c.form.field import Fields
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IPSTActionProgressImportSchema(Interface):

    import_list = schema.List(
        title=_(u"List of PST Actions progresses that you want to import"),
        description=_(
            u"This list contains only PST Actions progresses that was "
            u"not already imported"
        ),
        value_type=schema.Choice(
            title=u"document",
            vocabulary="ideabox.restapi.vocabularies:pstactionprogress",
        ),
    )


class PSTActionProgressImportForm(ImportForm):
    _application_id = "PST"
    fields = Fields(IPSTActionProgressImportSchema)

    def update(self):
        self.fields["import_list"].widgetFactory = SelectFieldWidget
        super(PSTActionProgressImportForm, self).update()

    def _get_data(self, data):
        return data["import_list"]


class PSTActionProgressImportFormView(FormWrapper):
    form = PSTActionProgressImportForm


@adapter(dict, IPriorityAction)
class PSTActionProgressImporter(BaseContentImporter):
    _fields = [
        "title",
        "description_rich",
        "modified",
    ]

    def transform_data(self, data):
        data["@type"] = "state_progress"
        data["state_date"] = data["modified"].split('T')[0]
        del data["modified"]
        data["body"] = data["description_rich"]
        del data["description_rich"]
        return data
