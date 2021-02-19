#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import logging

class SecureTask():

    def __init__(self, config_manager):
        self.config_manager = config_manager


    def secure_alias(self, alias, dry_run):
        path = self.config_manager.get("secure", alias)
        if path == None:
            logging.warning("Alias [%s] is not defined." % alias)
            return
        
        name, ext = os.path.splitext(path)
        if (ext.lower() == '.gpg'):
            original_file_name = name
            encrypted_file_name = path
        else:
            original_file_name = path
            encrypted_file_name = path + ".gpg"

        if os.path.exists(original_file_name) and os.path.exists(encrypted_file_name):
            logging.warning("Original & encrypt both exist, skip processing.")
            return

        if not os.path.exists(original_file_name) and not os.path.exists(encrypted_file_name):
            logging.warning("File does not exist.")
            return

        gpg_recipient = self.__get_gpg_recipient(dry_run)
        
        if (os.path.exists(encrypted_file_name)):
            logging.info("decrypting %s" % path)
            src = encrypted_file_name
            dst = original_file_name
            cmd = "gpg --recipient %s --output %s --decrypt %s" % (gpg_recipient, dst, src)
        else:
            logging.info("encrypting %s" % path)
            src = original_file_name
            dst = encrypted_file_name
            cmd = "gpg --recipient %s --output %s --encrypt %s" % (gpg_recipient, dst, src)

        self.__run_shell_cmd(cmd, dry_run)
        
        if not dry_run:
            os.remove(src)


    def __run_shell_cmd(self, cmd, dry_run):
        logging.debug("Running shell cmd: %s", cmd)
        if dry_run:
            return
        res = os.popen(cmd)
        for message in res.readlines():
            logging.debug(message)


    def __get_gpg_recipient(self, dry_run):
        gpg_recipient = self.config_manager.get("secure", "gpg_recipient")

        if(gpg_recipient==None):
            gpg_recipient = self.__ask_gpg_recipient(dry_run)
        
        return gpg_recipient


    def __ask_gpg_recipient(self, dry_run):
        print("Please input gpg recipient (the email address):")
        gpg_recipient = input()
        if not dry_run:
            self.config_manager.set("secure", "gpg_recipient", gpg_recipient)
        return gpg_recipient


    def set_alias(self, alias, path, dry_run):
        path = os.path.abspath(path)
        if not self.__is_valid_path(path):
            return

        if dry_run:
            logging.info("Dry running [%s = %s]" % (alias, path))
            return
        self.config_manager.set("secure", alias, path)


    def __is_valid_path(self, path):
        if not os.path.isfile(path):
            logging.warning("Invalid file path: %s" % path)
            return False
        return True