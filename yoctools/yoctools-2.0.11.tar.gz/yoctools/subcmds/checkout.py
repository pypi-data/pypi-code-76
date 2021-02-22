# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *


class Checkout(Command):
    common = True
    helpSummary = "Checkout a branch for development"
    helpUsage = """
%prog <branchname> [<project>...]
"""
    helpDescription = """
Initialize yoc workspace in the current directory.
"""

    def _Options(self, p):
        p.add_option('-b', '--branch',
                     dest='branch', action='store', type='string',
                     help='checkout the branche for the component')

    def Execute(self, opt, args):
        nb = opt.branch
        if not nb:
            self.Usage()
            return
        yoc = YoC()
        components = ComponentGroup()
        for component in yoc.components:
            if len(args) > 0:
                if component.name not in args:
                    continue
            if os.path.exists(os.path.join(component.path, '.git')):
                components.add(component)
        if len(components) == 0:
            put_string("There no git repo found in your workspace.", level='error')
            exit(0)

        pm = Progress('Checkout %s' % nb, len(components))
        for component in components:
            pm.update()
            git = GitRepo(component.path, component.repo_url)
            git.CheckoutBranch(nb)
        pm.end()
