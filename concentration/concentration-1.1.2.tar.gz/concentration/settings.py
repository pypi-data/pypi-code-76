"""concentration/settings.py

Defines how the basic concentration settings get loaded.
"""
import os
import sys
from enum import Enum

OS = Enum("OS", "linux mac windows")
HOSTS_FILE = "/etc/hosts"
REDIRECT_TO = "127.0.0.1"
START_TOKEN = "## START DISTRACTORS ##"  # nosec - not password
END_TOKEN = "## END DISTRACTORS ##"  # nosec - not password
SUB_DOMAINS = ("www", "news")
DISTRACTORS = {
    "ycombinator.com",
    "slashdot.com",
    "facebook.com",
    "reddit.com",
    "gawker.com",
    "theverge.com",
    "techcrunch.com",
    "thenextweb.com",
    "wired.com",
    "gizmodo.com",
    "slickdeals.net",
    "mashable.com",
    "digitaltrends.com",
    "techradar.com",
    "twitter.com",
    "tumblr.com",
    "technorati.com",
    "digg.com",
    "buzzfeed.com",
    "twitter.com",
    "youtube.com",
    "netflix.com",
    "iwastesomuchtime.com",
    "pinterest.com",
    "ebay.com",
    "thepointsguy.com",
    "imgur.com",
    "woot.com",
    "flyertalk.com",
    "instagram.com",
    "medium.com",
    "meetup.com",
    "distrowatch.com",
    "arstechnica.com",
    "phoronix.com",
    "arstechnica.com",
    "failblog.com",
    "redfin.com",
    "realtor.com",
    "zillow.com",
    "trulia.com",
    "cnn.com",
    "fox.com",
    "realclearpolitics.com",
    "yelp.com",
    "opentable.com",
    "slashdot.org",
    "xkcd.com",
    "cnet.com",
    "tomshardware.com",
    "engadget.com",
    "zdnet.com",
    "techrepublic.com",
    "gizmag.com",
    "anandtech.com",
    "imore.com",
    "gsmarena.com ",
    "geek.com",
    "firstpost.com",
    "wearables.com",
    "stripgenerator.com",
    "fmylife.com",
    "liveplasma.com",
    "cracked.com",
    "befunky.com",
    "pcworld.com",
    "typepad.com",
    "pogo.com",
    "omegle.com",
    "lifehacker.com",
    "answerbag.com",
    "cheezburger.com",
    "fark.com",
    "popurls.com",
    "sho.com",
    "hulu.com",
    "myparentsjoinedfacebook.com",
    "homestarrunner.com",
    "petsinclothes.com",
    "freerice.com",
    "everypoet.com",
    "mono-1.com",
    "mcsweeneys.net",
    "postsecret.com",
    "textsfromlastnight.com",
    "awkwardfamilyphotos.com",
    "myspace.com",
    "lunchtimers.com",
    "twitterfall.com",
    "break.com",
    "passiveaggressivenotes.com",
    "sciencemag.org",
    "bbc.com",
    "notalwaysright.com",
}

for config_file_path in (
    "/etc/concentration.distractors",
    os.path.expanduser("~/.concentration.distractors"),
):
    if os.path.isfile(config_file_path):
        with open(config_file_path) as config_file:
            DISTRACTORS.update(config_file.read().splitlines())
for config_file_path in ("/etc/concentration.safe", os.path.expanduser("~/.concentration.safe")):
    if os.path.isfile(config_file_path):
        with open(config_file_path) as config_file:
            DISTRACTORS.difference_update(
                config_file.read().splitlines()
            )  # Remove all white listed domains

DISTRACTORS.discard("")

PLATFORM = OS.linux
for platform in (("linux", OS.linux), ("darwin", OS.mac), ("win32", OS.windows)):
    if platform[0] in sys.platform:
        PLATFORM = platform[1]

RESTART_NETWORK = {
    OS.linux: [
        ["/etc/init.d/networking", "restart"],
        ["/etc/init.d/nscd", "restart"],
        ["/etc/rc.d/nscd", "restart"],
        ["/etc/rc.d/init.d/nscd", "restart"],
    ],
    OS.mac: [["dscacheutil", "-flushcache"]],
    OS.windows: [["ipconfig", "/flushdns"]],
}[PLATFORM]
if PLATFORM is OS.windows:
    HOSTS_FILE = "/Windows/System32/drivers/etc/hosts"
