from collective.editablemenu.browser.interfaces import IEditableMenuSettings
from collective.editablemenu.browser.interfaces import IEditableMenuSettings
from zope.interface import Interface
from zope.interface import Interface
from zope import schema


class IEditableSecondaryMenuSettings(IEditableMenuSettings):
    """
    Settings for secondary menu
    """


class ISecondaryMenuControlpanelSchema(IEditableMenuSettings):
    """
    Controlpanel for secondary menu
    """


class IRatingEnabled(Interface):
    """marker interface for enable rating"""


class IPartecipazioneAttivaSettings(Interface):

    comments_to_show = schema.Int(
        title=u"Commenti da mostrare",
        description=u"Commenti da mostrare nella sezione partecipazione attiva",  # noqa
    )
