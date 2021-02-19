#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys, os
import logging

class CheatSheetTask():

    command_list = [
            ("fmc", "test", 'echo "Running test command of fmc cheatsheet."', "Run a simple echo test command."), 
            ("Android", "gradle_ktlint", "./gradlew :ktlint", "Kotlin lint."),
            ("Android", "open_ui_viewer", "~/Library/Android/sdk/tools/bin/uiautomatorviewer", "open UiAutomatorViewer"),
        ]

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def __get_command_max_length(self):
        res = 0
        for command in self.command_list:
            res = max(res, len(command[1]))
        return res

    def run(self, command):
        index = 1
        for item in self.command_list:
            if item[1] == command or command == str(index):
                self.__run_command(item)
                return
            index = index + 1
        
        logging.warning("Command %s doesn't exist in cheatsheet, run [fmc cheatsheet] to check the full list." % command)

    def __run_command(self, command):
        shell_cmd = command[2]
        descr = command[3]
        os.system(shell_cmd)
        if descr != None:
            logging.info(descr)

    def print_commands(self):
        padding_length = self.__get_command_max_length()

        prev_category = None
        count = 1

        for command in self.command_list:
            category = command[0]
            name = command[1]
            descr = command[3]

            if category!=prev_category:
                logging.info("%s" % category)
            prev_category = category

            text = "  %s [%d] >>  %s" % (name.ljust(padding_length), count, descr)
            logging.info(text)
            count = count+1
