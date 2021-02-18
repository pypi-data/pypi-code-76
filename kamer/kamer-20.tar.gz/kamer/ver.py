# kamer/version.py
#
#

""" version plugin. """

from kamer import __version__

txt = "OTP-CR-117/19 otp.informationdesk@icc-cpi.int http://pypi.org/project/genocide !"

def ver(event):
    event.reply(txt)
