"""Wrapper around prompt toolkit."""

import logging
from datetime import date, datetime
from typing import List

from prompt_toolkit import prompt as prmpt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import ValidationError, Validator


class DateValidator(Validator):
    """Date input validator."""

    def validate(self, document):
        """Validate input.

        Arguments:
            document -- Input stream to validate.

        Raises:
            ValidationError: When the number is not a digit.
            ValidationError: When the length is > 8 digits.
        """
        text = document.text

        if text and not text.isdigit():
            i = 0

            # Get index of fist non numeric character.
            # We want to move the cursor here.
            for i, value in enumerate(text):
                if not value.isdigit():
                    break

            raise ValidationError(message='Input is not a number',
                                  cursor_position=i)
        if text and not len(text) == 8:
            i = 0

            # Get index of fist non numeric character.
            # We want to move the cursor here.
            for i, value in enumerate(text):
                if not value.isdigit():
                    break

            raise ValidationError(message='This input is not 8 digits long.',
                                  cursor_position=i)


class NumberValidator(Validator):
    """Number input validation."""

    def validate(self, document):
        """Validate the input stream.

        Arguments:
            document -- Document input stream to validate.

        Raises:
            ValidationError: When input is not a number.
        """
        text = document.text

        if text and not text.isdigit():
            i = 0

            # Get index of fist non numeric character.
            # We want to move the cursor here.
            for i, value in enumerate(text):
                if not value.isdigit():
                    break

            raise ValidationError(message='Input is not a number',
                                  cursor_position=i)


class YesNoValidator(Validator):
    """Yes and No validation."""

    def validate(self, document):
        """Validate input strem.

        Arguments:
            document -- Document input to validate.

        Raises:
            ValidationError: When input is not a y or n.
        """
        text = document.text

        if text and text not in ["y", "Y", "n", "N"]:
            i = 0

            # Get index of fist non numeric character.
            # We want to move the cursor here.
            for i, value in enumerate(text):
                if not value.isdigit():
                    break

            raise ValidationError(message='Value not y or n',
                                  cursor_position=i)


def prompt(message: str, validator=None, completion=None, default="") -> str:
    """Request user for input.

    Arguments:
        message {str} -- Message for user.

    Keyword Arguments:
        validator {list} -- List of valid values. (default: {None})
        completion {list} -- List of completion options. (default: {None})

    Returns:
        str -- Response from user.
    """
    complete = WordCompleter(completion) if completion else None
    response = prmpt("{} >".format(message), validator=validator,
                     completer=complete, search_ignore_case=True, default=default)
    logging.info("%s: %s", message, response)
    return response


def prompt_date(message: str, default=None) -> date:
    """Request date from user.

    Arguments:
        message {str} -- Message to user.

    Returns:
        datetime -- Date that user input.
    """
    if not default:
        default = datetime.now().date().strftime("%d%m%Y")
    response = prompt("{} [DDMMYYYY]".format(message), validator=DateValidator(), default=default)
    form_date = datetime.strptime(response, "%d%m%Y").date()
    return form_date


def prompt_number(message: str) -> int:
    """Request number from user.

    Arguments:
        message {str} -- Message to user.

    Returns:
        int -- Number that user input.
    """
    num = int(prompt(message, validator=NumberValidator()))
    logging.info("%s: %s", message, num)
    return num


def prompt_yes_no(message: str) -> bool:
    """Request a yes or no from user.

    Arguments:
        message {str} -- Message to user.

    Returns:
        bool -- Response from user.
    """
    response = prompt("{} [y/n]".format(message), validator=YesNoValidator())
    return response in ['y', 'Y']


def prompt_option(message: str, options: List[str]) -> str:
    """Request a choice from a list of options

    Args:
        message (str): message to user.
        options (List): Options to provide in completion and validation

    Returns:
        str: [description]
    """
    def is_in_list(text):
        return text in options

    validator = Validator.from_callable(is_in_list,
                                        error_message="Input is not in list of options",
                                        move_cursor_to_end=True)
    response = prompt(message, completion=options, validator=validator)
    return response
