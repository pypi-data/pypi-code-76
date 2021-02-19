# encoding: utf-8

import os

from klity.klity import Klity
from selenium import webdriver


def before_all(context):
    # Using Klity for testing
    context.klity = Klity()
    # Using specific profile to init browser
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", os.getcwd())
    profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "application/forcedownload"
    )
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/vnd.oasis.opendocument.spreadsheet",
    )
    profile.set_preference(
        "browser.helperApps.neverAsk.openFile", "application/forcedownload"
    )
    profile.set_preference("browser.helperApps.neverAsk.openFile", "text/csv")
    profile.set_preference(
        "browser.helperApps.neverAsk.openFile",
        "application/vnd.oasis.opendocument.spreadsheet",
    )
    context.browser = webdriver.Firefox(profile)


def after_all(context):
    context.browser.quit()


def before_feature(context, feature):
    context.klity.before_feature(context, feature)


def after_feature(context, feature):
    context.klity.after_feature(context, feature)


def before_scenario(context, scenario):
    context.klity.before_scenario(context, scenario)


def after_scenario(context, scenario):
    context.klity.after_scenario(context, scenario)
