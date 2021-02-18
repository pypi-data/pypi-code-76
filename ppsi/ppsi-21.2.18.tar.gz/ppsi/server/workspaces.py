#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020-2021 Pradyumna Paranjape
# This file is part of ppsi.
#
# ppsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ppsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ppsi.  If not, see <https://www.gnu.org/licenses/>.
#
'''
SwayWM Workspace Manager

Guess the active workspace of SwayWM and bind keys according
to supplied yaml configuration

Workspace-order-cycle for quick cycling/switching.

'''


import os
import typing
import json
from ..common import shell, misc
from . import CONFIG, SWAYROOT
from .sway_api import sway_assign, sway_nag, sway_ws, sway_query, sway_bind


def get_ws() -> str:
    '''
    Get currently focused workspace name by parsing ``swaymsg``

    On Error:
        ``swaynag`` about unavailability of focused workspace

    Returns:
        Workspace Name as displayed (including workspace number)
    '''
    stdout = sway_query('get_workspaces')
    ws_info: typing.List[dict] = json.loads(stdout)
    for w_space in ws_info:
        if w_space['focused']:
            return w_space['name']
    sway_nag('No workspace appears to be focused', error=True)
    return None


class WorkSpace():
    '''
    Workspace object
    Args:
        index: index (number) of workspace (workspace is bound to this key)
        name: displayed name of wordspace
        suicidal: forget this workspace if unfocused and without containers
        keybindings: "keypress": "binding execution"
        assignments: class|app_id: list(container patterns)
    '''
    def __init__(self, index: str, name: str = None,
                 suicidal: bool = False, keybindings: dict = {},
                 assignments: typing.Dict[str, list] = {}) -> None:
        self.index = index
        self.name = self.index
        if name is not None:
            self.name += f":{name}"
        self.suicidal = suicidal
        self.keybindings = keybindings
        self.assignments = assignments

    def bind(self) -> None:
        '''
        Bind all keybindings for this workspace

        Returns:
            None
        '''
        for key, action in self.keybindings.items():
            sway_bind(key, 'exec', action)

    def unbind(self, manager: 'SwayWsMan') -> None:
        '''
        Unbind this workspace's keybindings.
        Destroy suicidal workspaces
        Recipe to run while leaving this workspace.

        Args:
            manager: parent manager
        '''
        for key, action in self.keybindings.items():
            sway_bind(key, 'nop')
        if self.suicidal:
            if self.name not in sway_query('get_workspaces'):
                manager.destroy_ws(self)

    def switch(self) -> typing.Callable:
        '''
        Switch to this workspace.

        Returns:
            Method to execute while switching away
        '''
        sway_ws(self.name)
        self.bind()
        return self.unbind


class CycleOrder(list):
    '''
    Order of visited workspaces:
    0: Oldest workspace' index
    -1: Current workspace' index
    -2: Latest workspace' index [if exists]
    ... and accordingly.

    Items are indices refering to workspaces in
    manager's ``assigned`` list

    Args:
        Parent: Inherit order from

    '''
    def __init__(self, parent: 'CycleOrder' = None) -> None:
        # Current workspace is at index -1
        super().__init__()
        if parent is not None:
            for w_space in parent:
                self += w_space

    def reverse(self) -> None:
        '''
        Reverse the order of visited workspaces protecting current.
        Oldest [0] workspace index becomes latest [-2].
        '''
        rev_order = reversed(self)
        for w_sp in rev_order:
            self += w_sp
        self += self[0]

    def __iadd__(self, value: int) -> 'CycleOrder':
        '''
        Add a workspace index

        Args:
            value: index of newly arrived workspace

        Returns:
            Updated CycleOrder
        '''
        while value in self:
            self.remove(value)
        self.append(value)
        return self

    def current(self) -> int:
        '''
        Retrieve index of currently focused workspace

        Returns:
            current (active) workspace *as registered* in the cycle
            ``None`` if workspace stack is empty
        '''
        if len(self):
            return self[-1]
        else:
            return None

    def __add__(self, index: int = 0) -> int:
        '''
        Query index of oldest workspace

        Args:
            index: index from beginning of stack (the oldest)
            which is now brought to focus in the cycle
        Returns:
            current focus (``index`` brought to focus)
        '''
        if len(self) > index:
            self.__iadd__(self[index])
        return self.current()

    def __sub__(self, index=2) -> int:
        '''
        Query index of latest Nth workspace

        Args:
            index: index from end of stack (the latest)
            which is brought to focus in the cycle
        Returns:
            current focus (``index`` brought to focus)
        '''
        if len(self) >= index:
            self.__iadd__(self[-index])
        return self.current()


class SwayWsMan():
    '''
    Sway Workspace Manager.

        Args:
            config: workspaces config, a part of ppsi.yml
    '''
    def __init__(self, config: dict = CONFIG):
        self.assigned: typing.List[WorkSpace] = []
        self.init_pre_def(config)
        self.bind_base()
        self.cycle_order = CycleOrder()
        self.cycle_order += self.which_workspace((get_ws()))[0]
        self._unbind: typing.Callable = lambda *args, **kwargs: None

    @property
    def unbind(self) -> typing.Callable:
        return self._unbind

    @unbind.deleter
    def unbind(self):
        self._unbind =  lambda *args, **kwargs: None

    @unbind.setter
    def unbind(self, method):
        self._unbind = self.exitter(method)

    def exitter(self, method: typing.Callable) -> typing.Callable:
        def wrapper(method=method, manager=self, **kwargs):
            return method(manager=manager, **kwargs)
        return wrapper

    @staticmethod
    def bind_base():
        '''
        Default hard bindings
        bind $mod + variable + Tab to cycling through workspaces
        bind Alt+Ctrl+p to edit ppsi.yml file in ``SWAYROOT``
        '''
        editor = os.environ.get(
            "EDITOR",
            f"{os.environ.get('defterm', 'xterm')} -- vi"
        )
        ppsi_yml_file = str(SWAYROOT.joinpath("ppsi.yml"))
        sway_bind("Ctrl+Mod1+p",
                  f'"exec {editor} {ppsi_yml_file}"')
        sway_bind("$mod+Tab",
                  '"exec --no-startup-id ppsi workspace latest"')
        sway_bind("$mod+Shift+Tab",
                  '"exec --no-startup-id ppsi workspace oldest"')
        sway_bind("$mod+Ctrl+Tab",
                  '"exec --no-startup-id ppsi workspace reverse"')

    def init_pre_def(self, config: dict) -> None:
        '''
        Initialize all workspaces as directed in ``config``.
        Bind workspace switchings:
        $mod+0 through $mod+9, $mod+F1 through $mod+F12

        Args
            config: Configuration to initialize and assign workspaces

        Returns:
            ``None``

        '''
        undefined_ws = [str(num_key) for num_key in range(10)]
        undefined_ws += [f'F{num_key}' for num_key in range(1, 13)]
        primary: str = config.get('key-primary', '$mod+Shift+Return')
        pre_def: typing.List[dict] = config.get('workspaces', [])
        for w_space in pre_def:
            bindings: typing.Dict[str, str] = {}
            assignments: typing.Dict[str, list] = {'class': [], 'app_id': []}

            # Others
            for add_bind in w_space.get('bind'):
                bindings[add_bind['key']] = add_bind['exec']

            # Primary overrides if the default keybinding is assigned to others
            if w_space.get('primary'):
                bindings[primary] = w_space.get('primary')
            assign = w_space.get('assignments', {})
            if isinstance(assign, list):
                shell.notify('''
                PPSI ERROR: Assignments: <List>.
                Expected: maps {}
                REPLACE leading '-' by <space>
                ''')
                assign = misc.key2dict(keys=assign, vals='class')

            for app, disp_srv in assign.items():
                if disp_srv and any(disp_srv.lower() in w_pat
                                    for w_pat in ('wayland', 'wl', 'app')):
                    disp = 'app_id'
                else:
                    disp = 'class'
                assignments[disp].append(app)

            for index in w_space.get('index', []):
                undefined_ws.remove(str(index))
                self.create_ws(index=str(index),
                               name=w_space.get('name'),
                               keybindings=bindings,
                               assignments=assignments)
        for undef_idx in undefined_ws:
            self.create_ws(index=str(undef_idx))

    def create_ws(self, **kwargs) -> None:
        '''
        Create a structured workspace

        Args:
            **kwargs: passed to initialize ``WorkSpace`` object

        Returns:
            ``None``
        '''
        w_sp = WorkSpace(**kwargs)
        for disp, app_list in w_sp.assignments.items():
            for app in app_list:
                sway_assign(f'[{disp}="{app}"]', w_sp.name)
        sway_bind(
            f'$mod+{w_sp.index}',
            f'"workspace {w_sp.name}, exec --no-startup-id ppsi workspace"'
        )
        sway_bind(f'$mod+Shift+{w_sp.index}', 'move', 'container',
                  'to', 'workspace', w_sp.name)
        self.assigned.append(w_sp)

    def destroy_ws(self, w_sp: WorkSpace) -> None:
        '''
        Unassign ``w_sp`` from this manager
        CAUTION: Program assignments still remain stuck.
        This may cause appearance of zombies for SwayWsMan.
        Switch to a zombie to regularise it.

        Args:
            w_sp: WorkSpace object to destroy

        Returns:
        ``None``
        '''
        sway_bind(f'$mod+{w_sp.index}', 'nop')
        sway_bind(f'$mod+Shift+{w_sp.index}', 'nop')
        idx = self.assigned.index(w_sp)
        self.assigned.remove(w_sp)
        self.cycle_order.remove(idx)

    def which_workspace(self, name: str) -> typing.Tuple[int, WorkSpace]:
        '''
        Args:
            name: name of workspace

        Returns:
            Corresponding WorkSpace object

        Guess and return WorkSpace from its name
        '''
        if name is not None:
            for ws_idx, w_sp in enumerate(self.assigned):
                if name == w_sp.name:
                    return ws_idx, w_sp
        return None, None


PPSI_WS_MAN = SwayWsMan(config=CONFIG)
'''
SwayWsMan instance in use.
'''


def ws_mod(subcmd: int = 0x00, manager: SwayWsMan = PPSI_WS_MAN) -> None:
    '''
    WorkSpace modification requests called by ppsi client

    Args:
        subcmd: int = subcommand {0,1,2,3}
            0x00: Register a switch of workspace, unbind old, bind new
            0x01: Reverse cycle order
            0x02: Switch to oldest workspace in the cycle
            0x03: Switch to the latest workspace (causes back_and_forth)
        manager: Workspace Manager instance

    Returns:
        ``None``
    '''
    if subcmd == 0x00:
        curr_name = get_ws()
        if curr_name is None:
            # Failed to get workspace name and/or corresponding workspace
            return
        current_id, current_ws = manager.which_workspace(curr_name)
        if current_id is None:
            # create anew
            manager.create_ws(index=curr_name, suicidal=True)
            current_id, current_ws = -1, manager.assigned[-1]
        elif current_id == -1:
            # we've switched to already active workspace,
            # hence, we need to do nothing
            return
        manager.cycle_order += current_id
        # unbind old
        manager.unbind()

        # bind new
        current_ws.bind()
        manager.unbind: typing.Callable = current_ws.unbind
        return
    elif subcmd == 0x01:
        manager.cycle_order.reverse()
        return
    elif subcmd == 0x02:
        current_id = manager.cycle_order + 0
    elif subcmd == 0x03:
        current_id = manager.cycle_order - 2
    # current_ws to-be
    sw_2_ws = manager.assigned[current_id]
    manager.unbind()
    manager.unbind: typing.Callable = sw_2_ws.switch()
    return
