import os
import logging
from copy import deepcopy

from mcutk.debugger.general import DebuggerBase
from mcutk.debugger.redlink import RedLink

class IDE(DebuggerBase):
    """IDE debugger: use IDE to flash application to board.
    """

    # supported ides
    TOOLS = [
        'iar',
        'mdk',
        'mcux'
    ]

    def __init__(self, ides, **kwargs):
        super(IDE, self).__init__("ide", '', **kwargs)
        if not isinstance(ides, list):
            raise TypeError('apps must be a list')
        self._ides = ides
        self._force_ide = None
        self._redlink = None
        self.template_root = ''

    def set_board(self, board):
        self._board = board
        mcux = self.get_ide("mcux", raise_exc=False)
        if not mcux:
            return
        self._redlink = RedLink(mcux.path, version=self.version)
        self._redlink.gdbpath = self.gdbpath
        self._redlink.set_board(board)
        self._redlink.template_root = os.path.join(self.template_root, 'mcux')

    @property
    def redlink(self):
        if not self._redlink:
            logging.error('mcux.path is not exists!')
        return self._redlink

    @property
    def is_ready(self):
        for ide in self._ides:
            if ide.is_ready is False:
                return False
        return True

    def set_force_ide(self, name):
        if name in self.TOOLS:
            self._force_ide = name

    def get_ide(self, name, raise_exc=True):
        convert_map = {
            'armgcc': 'mdk',
            'uv4': 'mdk'
        }
        name = convert_map.get(name, name)
        for app in self._ides:
            if app.name == name:
                return app
        if raise_exc:
            raise ValueError('{} path is not exists or not set!'.format(name))
        return None

    def flash(self, debugfile, idename='mcux', target='flexspi_nor_debug', board=None, template_root=None, **kwargs):
        """Flash image to board by IDE.

        Arguments:
            debugfile - {str}: image path.
            idename - {str}: mcux, mdk, iar.
            target - {str}: project target name.
            board - {Board} overried board object.
            template_root - {str} path to root directory of template projects
        """
        if self._force_ide:
            idename = self._force_ide
            logging.info("mandatory debugger run with %s", idename)

        # force to use mcuxpresso to flash binary to board
        if debugfile.endswith('.bin'):
            idename = 'mcux'

        if template_root is None:
            template_root = self.template_root

        if board is None:
            board = self._board

        # assert template projects root
        if not os.path.exists(template_root):
            raise IOError("template project[%s] is not exists!"%template_root)

        app = self.get_ide(idename)
        idename = app.name
        # assert tool name
        if idename not in IDE.TOOLS:
            raise ValueError("IDE [{}] is unsupported for board programming!".format(app))

        prjdir = os.path.join(template_root, idename)
        kwargs['gdbpath'] = self.gdbpath
        logging.info("IDE name: %s, Version: %s", idename, app.version)
        self._call_registered_callback("before_load")
        if idename == 'mcux':
            ret = self.redlink.flash(debugfile)
        else:
            logging.info("Project template: %s", prjdir)
            ret = app.programming(self._board, prjdir, target, debugfile, **kwargs)
        return ret

    def _erase_by_mcux(self, board, target):
        if not self.redlink:
            logging.error('cannot erase, because mcux.path is not exists!')
            return False
        return self.redlink.erase()

    def _erase_by_mdk(self, board, target, debugfile):
        mdk_ide = self.get_ide("mdk")
        prjdir = os.path.join(self.template_root, 'mdk')
        project = mdk_ide.Project.frompath(prjdir)
        # use flash target
        for tar in project.targets:
            if "flash" in tar or "flexspi_nor_debug" in tar:
                target = tar
                break
        mdk_ide.programming(board, prjdir, target, debugfile, action="erase")

    def erase(self, idename="mcux", target='debug', debugfile=None):
        """Erase flash by IDE.

        Arguments:
            idename - {str}: mcux or mdk.
            target - {str}: project target name.
            debugfile - {str}: path to debug file. must set when idename=mdk
        """
        if idename == "mdk":
            if not debugfile:
                raise ValueError("MDK erase must pass an exists debugfile")
            return self._erase_by_mdk(self._board, target, debugfile)
        else:
            return self._erase_by_mcux(self._board, target)

    def reset(self):
        """Use redlink perform hardware reset."""
        if not self.redlink:
            logging.error('cannot reset, because mcux.path is not exists!')
            return False
        return self.redlink.reset()

