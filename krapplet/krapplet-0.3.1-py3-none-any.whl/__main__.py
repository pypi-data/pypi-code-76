#!/usr/bin/python3
"""
krapplet: A password manager written as a gnome-keyring applet
__main__.py: a start-up helper 
(c) 2020-2021 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

#import krapplet.__init__

try:
    from krapplet import main
except:
    from krapplet.krapplet import main

main()
