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
Objects complying with swaybar protocol

'''


import typing
import json


class SwayProtoIn():
    '''
    JSON object accepted by sway bar protocol

    Attributes:
        full_text: str: text displayed in segment
        short_text: str: If full_text overflows
        color: str: Text color #RRGGBB[AA]
        background: str: Segment background color #RRGGBB[AA]
        border: str: Segment border color #RRGGBB[AA]
        border_top: int: top border ``px``
        border_bottom: int: bottom border ``px``
        border_left: int: left border ``px``
        border_right: int: right border ``px``
        min_width: int, str: # minimum seg width ``px`` or `THIS WORD SIZE`
        align: str: alignment left (default), right, or center
        name: str: Name to ID segment. For click events
        instance: str: Instance to ID segment. For click events
        urgent: bool: Highlight Seg for urgency
        separator: bool: Visual separation of seg
        separator_block_width: int: padding after seg
        markup: str: pango or none

    Args:
        **kwargs: passed to update method

    Information:
        url: https://www.mankier.com/7/swaybar-protocol

    '''
    def __init__(self, **kwargs) -> None:
        self.full_text: str = ''  # Necessary
        self.short_text: str = None  # If full_text overflows
        self.color: str = None  # Text color #RRGGBB[AA]
        self.background: str = None  # Segment background color #RRGGBB[AA]
        self.border: str = None  # Segment border color #RRGGBB[AA]
        self.border_top: int = 1  # top border <px>
        self.border_bottom: int = 1  # bottom border <px>
        self.border_left: int = 1  # left border <px>
        self.border_right: int = 1  # right border <px>
        # minimum seg width <px> or 'THIS WORD_S SIZE':
        self.min_width: typing.Union[int, str] = None
        self.align: str = 'left'  # left (default), right, or center
        self.name: str = None  # Name to ID segment. For click events
        self.instance: str = None  # Instance to ID segment. For click events
        self.urgent: bool = False  # Highlight Seg for urgency
        self.separator: bool = True  # Visual separation of seg
        self.separator_block_width: int = 9  # padding after seg
        self.markup: str = None  # pango or none
        self.update(**kwargs)

    def update(self, **kwargs) -> None:
        '''
        Update keys from kwargs only if it is an attribute
        else, ignore

        Args:
            full_text: str:  text displayed in segment
            short_text: str: If full_text overflows
            color: str: Text color #RRGGBB[AA]
            background: str: Segment background color #RRGGBB[AA]
            border: str: Segment border color #RRGGBB[AA]
            border_top: int: top border ``px``
            border_bottom: int: bottom border ``px``
            border_left: int: left border ``px``
            border_right: int: right border ``px``
            min_width: int, str:

                * minimum seg width ``px`` or 'THIS WORD_S SIZE':

            align: str: alignment left (default), right, or center
            name: str: Name to ID segment. For click events
            instance: str: Instance to ID segment. For click events
            urgent: bool: Highlight Seg for urgency
            separator: bool: Visual separation of seg
            separator_block_width: int: padding after seg
            markup: str: pango or none

        '''
        self.__dict__ = {key: {**self.__dict__, **kwargs}[key]
                         for key in self.__dict__}

    def __str__(self) -> str:
        '''
        Serialize and Print

        Returns:
            JSON Serial of the object

        '''
        return json.dumps(self.__dict__)


class SwayProtoOut():
    '''
    JSON object delivered by sway bar protocol

    Attributes:
        name: str: The name of seg
        instance: str: The instance of seg
        x: int: The x location that the click occurred at
        y: int: The y location that the click occurred at
        button: int: The x11 button number for the click.
        event: int: The event code of button for the click
        relative_x: int: x wrt segment
        relative_y: int: y wrt segment
        width: int: width of the seg ``px``
        height: int: The height of the seg ``px``
        modifiers: Future form i3bar?

    Args:
        event_json: str: json returned by SwayBar Protocol on mouse-click

    information:
        url: https://www.mankier.com/7/swaybar-protocol

    '''
    def __init__(self, event_json: str) -> None:
        self.name: str = None  # The name of seg
        self.instance: str = None  # The instance of seg
        self.x: int = None  # The x location that the click occurred at
        self.y: int = None  # The y location that the click occurred at
        self.button: int = 0  # The x11 button number for the click.
        self.event: int = None  # The event code of button for the click
        self.relative_x: int = None  # x wrt segment
        self.relative_y: int = None  # y wrt segment
        self.width: int = None  # width of the seg <px>
        self.height: int = None  # The height of the seg <px>
        self.modifiers = None  # Future form i3bar?
        if event_json == '[':
            # stream opened
            return
        if event_json[0] == ',':
            # Continuation from previous infinite stream
            event_json = event_json[1:]
        self.__dict__ = {**self.__dict__, **json.loads(event_json)}
        # NEXT: In python 3.9, this shall simply become
        # self.__dict__ |= json.loads(event_json)
