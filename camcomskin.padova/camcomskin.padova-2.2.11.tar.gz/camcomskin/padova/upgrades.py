# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api
from collective.editablemenu.browser.interfaces import MenuEntrySubitem


default_profile = 'profile-camcomskin.padova:default'
agid_profile = 'profile-camcomskin.padova:to_agid'

REGISTRY_NAME = (
    "camcomskin.padova.interfaces.IEditableSecondaryMenuSettings.menu_tabs"
)


def generate_new_settings():
    """
    """
    old_settings = api.portal.get_registry_record(REGISTRY_NAME)
    if not old_settings:
        return
    new_settings = []
    for setting in old_settings:
        if not setting.navigation_folder:
            continue
        new_entry = MenuEntrySubitem()
        new_entry.tab_title = setting.tab_title
        new_entry.additional_columns = u''
        new_entry.navigation_folder = u''
        navigation_folder = api.content.get(UID=setting.navigation_folder)
        if navigation_folder:
            new_entry.navigation_folder = '/'.join(
                navigation_folder.getPhysicalPath()
            ).decode('utf-8')
        # we don't migrate additional columns because we can't know what's
        # the common folder.
        new_settings.append(new_entry)
    return tuple(new_settings)


def to_1100(context):
    """
    delete old registry configuration and add a new one
    """
    setup_tool = getToolByName(context, 'portal_setup')
    new_settings = generate_new_settings()
    setup_tool.runImportStepFromProfile(default_profile, 'plone.app.registry')
    api.portal.set_registry_record(REGISTRY_NAME, new_settings)


def to_2000(context):
    """
    new agid theme
    """
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(default_profile, 'cssregistry')
    setup_tool.runImportStepFromProfile(default_profile, 'jsregistry')
    setup_tool.runAllImportStepsFromProfile(agid_profile)


def to_2100(context):
    """
    """
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(default_profile, 'plone.app.registry')


def to_2200(context):
    """
    """
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(default_profile, 'plone.app.registry')
