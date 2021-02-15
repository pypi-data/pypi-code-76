"""
PyREXX - Library that enables parsing and analysis of REXX source code.

This program and the accompanying materials are made available under the terms of
The Apache-2.0 License which accompanies this distribution, and is available at
http://www.apache.org/licenses/LICENSE-2.0

SPDX-License-Identifier: Apache-2.0

Copyright (c) Mainframe Services Engineering (IBM GTS).

"""
import re
from .rexx_sub_routine import RexxSubRoutine
from .statements import IncludeStatement
from .statements import DocstringStatement
from .source_code import SourceCode
from utilities import LOG


class RexxCode(SourceCode):

    def __init__(self, code=None):
        self.rexx_routines = {}
        self.include_statements = []
        self.docstring_statements = []
        # The below regex matches to a REXX routine declaration statement
        # e.g:
        # Routine_Name: <...>
        #
        self.rexx_routine_declaration = r'(^([A-Za-z0-9_@#$-])+):'
        # The below regex matches to a custom include statement inside a
        # rexx comment
        # e.g:
        # /* INCLUDE file_name.rex <routine_name,...>
        #
        self.rexx_include_statement = \
            r'(\/\*)\s*(INCLUDE)\s+([A-Za-z0-9_\-]+)(\.rexx|\.rex)?\s*([A-Za-z0-9_@!#$\-\,]+)?\s*(\*\/)?'
        #
        # The below regex matches a custom docstring statement inside a rexx
        # comment
        # e.g:
        # /* @DOCSTRING Value,12345 test */
        self.rexx_docstring_statement = \
            r'(\/\*)\s*(@[A-Za-z0-9_\-]+){1}(\s.*[^*/]\s){1}(\*\/){1}'
        super().__init__(code)
        if code:
            LOG.debug('Processing records of REXX source code')
            self.__process_records()

    def __process_records(self):
        self.__parse_rexx_routines()
        self.__parse_include_statements()
        self.__parse_docstring_statements()

    def __parse_rexx_routines(self):
        current_routine = ""
        current_routine_buffer = ""
        for record in self.records:
            if self.__record_not_comment(record):
                new_routine = re.match(self.rexx_routine_declaration, record)
                if new_routine:
                    if current_routine:
                        self.rexx_routines[current_routine] = RexxSubRoutine(current_routine,
                                                                             current_routine_buffer)
                    current_routine = record.strip().split(":")[0]
                    current_routine_buffer = ''
                if current_routine:
                    current_routine_buffer += record + '\n'
        # Handles last routine
        if current_routine:
            self.rexx_routines[current_routine] = RexxSubRoutine(current_routine,
                                                                 current_routine_buffer)

    def __parse_include_statements(self):
        for record in self.records:
            has_include_statement = re.match(self.rexx_include_statement, record)
            if has_include_statement:
                self.include_statements.append(IncludeStatement(has_include_statement))

    def __parse_docstring_statements(self):
        for record in self.records:
            has_docstring_statement = re.match(self.rexx_docstring_statement, record)
            if has_docstring_statement:
                self.docstring_statements.append(DocstringStatement(has_docstring_statement))

    def __record_not_comment(self, record):
        return not record.strip().startswith("/*")

    def append_comment(self, record, index=None):
        """Append a REXX comment to the file object."""
        temp_record = "/* " + record
        new_record = temp_record.ljust(77, " ")
        new_record += "*/"
        self.append_record(new_record, index)

    def get_routine_contents(self, routine_name):
        try:
            LOG.debug(f'Trying to retrive "{routine_name}"')
            return self.rexx_routines[routine_name].records
        except KeyError:
            LOG.error(f'Unable to locate routine {routine_name}')
            exit(1)
