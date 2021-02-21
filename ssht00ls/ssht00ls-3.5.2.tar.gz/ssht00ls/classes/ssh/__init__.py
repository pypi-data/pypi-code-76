#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
import ssht00ls.classes.ssh.utils as ssh_utils 

# the ssh object class.
class SSH(object):
	def __init__(self):
		self.utils = ssh_utils

# initialized objects.
ssh = SSH()