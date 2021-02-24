# encoding: utf-8
# api: python
# type: init
# title: modseccfg
# description: Editor to tame mod_security rulesets
# version: 0.7.3
# state:   prototype
# support: none
# license: Apache-2.0
# depends: python:pysimplegui (>= 3.0), python:pluginconf (>= 0.7.3),
#    python:appdirs (>= 1.3), python:logfmt1 (>= 0.4),
#    python (>= 3.6), deb:python3-tk, bin:sshfs
# priority: core
# url: https://fossil.include-once.org/modseccfg/
# faq: https://fossil.include-once.org/modseccfg/doc/trunk/FAQ.md
# category: config
# keywords: modsecurity mod-security mod_security apache config desktop sshfs
# classifiers: x11, http
#
# Correlates mod_security SecRules to logs, and simplifies
# disabling unneeded rules. It's very basic and not gonna
# win any usability awards.
# BE WARNED THAT ALPHA RELEASES MAY DAMAGE YOUR APACHE SETUP.
#
# Basically you select your desired vhost *.conf file, then
# hit [Disable] for rules with a high error.log count - if it's
# false positives. Preferrably leave rules untouched that are
# indeed working as intended.
#


    