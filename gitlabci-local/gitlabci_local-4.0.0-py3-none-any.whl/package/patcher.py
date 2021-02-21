#!/usr/bin/env python3

# Modules libraries
from PyInquirer import Separator
from PyInquirer.prompts import list as PyInquirer_prompts_list
from PyInquirer.prompts.common import if_mousedown
from PyInquirer.prompts.list import basestring
from prompt_toolkit.layout.controls import TokenListControl
from prompt_toolkit.token import Token

# pylint: skip-file

# Override with https://github.com/CITGuru/PyInquirer/pull/88
class InquirerControl(TokenListControl):
    def __init__(self, choices, **kwargs):
        self.selected_option_index = 0
        self.answered = False
        self.choices = choices
        self._init_choices(choices)
        super(InquirerControl, self).__init__(self._get_choice_tokens, **kwargs)

    def _init_choices(self, choices, default=None):
        # helper to convert from question format to internal format
        self.choices = [] # list (name, value, disabled)
        searching_first_choice = True
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                self.choices.append((c, None, None))
            else:
                if isinstance(c, basestring):
                    self.choices.append((c, c, None))
                else:
                    name = c.get('name')
                    value = c.get('value', name)
                    disabled = c.get('disabled', None)
                    self.choices.append((name, value, disabled))
                if searching_first_choice:
                    self.selected_option_index = i # found the first choice
                    searching_first_choice = False

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self, cli):
        tokens = []
        T = Token

        def append(index, choice):
            selected = (index == self.selected_option_index)

            @if_mousedown
            def select_item(cli, mouse_event): # pragma: no cover
                # bind option with this index to mouse event
                self.selected_option_index = index
                self.answered = True
                cli.set_return_value(None)

            if isinstance(choice[0], Separator):
                tokens.append((T.Separator, '  %s\n' % choice[0]))
            else:
                tokens.append(
                    (T.Pointer if selected else T, ' \u276f ' if selected else '   '))
                if selected:
                    tokens.append((Token.SetCursorPosition, ''))
                if choice[2]: # disabled
                    tokens.append((T.Selected if selected else T,
                                   '- %s (%s)' % (choice[0], choice[2])))
                else:
                    try:
                        tokens.append(
                            (T.Selected if selected else T, str(choice[0]), select_item))
                    except: # pragma: no cover
                        tokens.append(
                            (T.Selected if selected else T, choice[0], select_item))
                tokens.append((T, '\n'))

        # prepare the select choices
        for i, choice in enumerate(self.choices):
            append(i, choice)
        tokens.pop() # Remove last newline.
        return tokens

    def get_selection(self):
        return self.choices[self.selected_option_index]

# Patcher class
class Patcher:

    # Constructor
    def __init__(self):

        # Apply library patches
        PyInquirer_prompts_list.InquirerControl = InquirerControl
