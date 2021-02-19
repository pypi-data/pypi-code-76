#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import logging

class GoTask():

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def go_alias(self, alias, eval):
        logging.debug("Going to alias: %s" % alias)

        path = self.config_manager.get("go", alias)
        if path == None:
            logging.warning("Alias [%s] is not defined." % alias)
            return
        
        path = os.path.abspath(path)

        if not self.__is_valid_path(path):
            return

        path = os.path.normcase(path)
        if (os.getcwd() == path):
            logging.warning("Already in the target dir.")
            return
        
        if eval:
            self.__generate_cd(path)
        else:
            self.__shell_to_path(path)

    def __generate_cd(self, path):
        return print("cd \"%s\"" % path)

    def __shell_to_path(self, path):
        os.chdir(path)
        os.system("$SHELL")


    def set_alias(self, alias, path):
        path = os.path.abspath(path)
        if not self.__is_valid_path(path):
            return
        self.config_manager.set("go", alias, path)
        logging.info("Updated alias %s" % alias)


    def __is_valid_path(self, path):
        if not os.path.isdir(path):
            logging.warning("Invalid directory: %s" % path)
            return False
        return True
