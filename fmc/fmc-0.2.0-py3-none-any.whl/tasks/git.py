#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import logging

class GitTask():

    def init(self):
        logging.info("ssh-add -K ~/.ssh/id_rsa")
        os.system("ssh-add -K ~/.ssh/id_rsa")
        logging.info("Initialization done.")
