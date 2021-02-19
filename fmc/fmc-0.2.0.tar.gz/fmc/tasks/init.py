#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import logging
import os

class InitTask():

    PREFIX  = "#========== FMC config starts here ==========\n"
    SCRIPT = """# FMC generates below script to config itself.
# If this is out of date, run [fmc init] to regenerate.

export FMC_CONFIG_VER=1

fmce(){
  if [ "$1" = "go" ]; then
    eval "$(fmc $@ --eval)";
  else
    fmc "$@";
  fi
}

"""
    SUFFIX  = "#==========  FMC config ends here  ==========\n"

    def run(self, dry_run):
      self.__config_shell(dry_run)

    def __config_shell(self, dry_run):
      shell = self.__get_shell()
      if shell == "zsh":
        self.__config_zsh(dry_run)

    def __get_shell(self):
      shell = os.getenv("SHELL")
      return os.path.basename(shell)

    def __config_zsh(self, dry_run):
      zshrc_path = os.path.expanduser("~/.zshrc")
      if not os.path.isfile(zshrc_path):
        logging.warning("Cannot config zsh, [%s] doesn't exist" % zshrc_path)
        return
      
      with open(zshrc_path, 'r') as reader:
        zshrc = reader.read()

      prefix_index = zshrc.find(self.PREFIX)
      suffix_index = zshrc.find(self.SUFFIX)
      
      found_config = prefix_index >-1 or suffix_index>-1
      if not found_config:

        if len(zshrc)==0:
          zshrc = self.__generate_config_section()
        elif zshrc[-1:]=="\n":
          zshrc = zshrc + self.__generate_config_section()
        else:
          zshrc = zshrc + "\n" + self.__generate_config_section()

        self.__update_rc(zshrc, zshrc_path, dry_run)

        logging.info("Appended fmc config to %s" % zshrc_path)
        return

      original_zshrc = zshrc
      valid_config = prefix_index >-1 and suffix_index>-1 and prefix_index < suffix_index
      if valid_config:
        (part_one, part_two) = self.__remove_config_section(zshrc, prefix_index, suffix_index)
        zshrc = part_one + self.__generate_config_section() + part_two

        if original_zshrc == zshrc:
          logging.info("fmc is already inited.")
          return

        self.__update_rc(zshrc, zshrc_path, dry_run)

        logging.info("Updated fmc config in %s" % zshrc_path)
        return

      logging.warning("Faild, found invalid configuration in %s" % zshrc_path)

    def __update_rc(self, content, path, dry_run):
      if dry_run:
        logging.info("Dry run updating %s >>>>\n%s" % (path, content))
      else:
        with open(path, 'w') as writer:
          writer.write(content)

    def __generate_config_section(self):
      return "%s%s%s" % (self.PREFIX, self.SCRIPT, self.SUFFIX)

    def __remove_config_section(self, content, prefix_index, suffix_index):
      part_one = content[:prefix_index]
      part_two = content[suffix_index + len(self.SUFFIX):]
      return (part_one, part_two)
