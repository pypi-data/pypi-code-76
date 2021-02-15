# **************************************************************************** #
#                           This file is part of:                              #
#                                BITSMITHS                                     #
#                           https://bitsmiths.co.za                            #
# **************************************************************************** #
#  Copyright (C) 2015 - 2021 Bitsmiths (Pty) Ltd.  All rights reserved.        #
#   * https://bitbucket.org/bitsmiths_za/bitsmiths                             #
#                                                                              #
#  Permission is hereby granted, free of charge, to any person obtaining a     #
#  copy of this software and associated documentation files (the "Software"),  #
#  to deal in the Software without restriction, including without limitation   #
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#  and/or sell copies of the Software, and to permit persons to whom the       #
#  Software is furnished to do so, subject to the following conditions:        #
#                                                                              #
#  The above copyright notice and this permission notice shall be included in  #
#  all copies or substantial portions of the Software.                         #
#                                                                              #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
#  DEALINGS IN THE SOFTWARE.                                                   #
# **************************************************************************** #
import cerberus

from bs_loco.xloco import xLoco

from bs_loco.db.tables import tCorrType


class BaseLocoTrig:
    """
    This is the base class for firing of loco message requests
    into the system.
    """
    SCHEMA_ADDR = {
        'sms' : {
            'type'      : 'list',
            'required'  : False,
            'empty'     : True,
            'nullable'  : True,
            'schema'    : {
                'type'      : 'string',
                'empty'     : False,
                'nullable'  : False,
                'maxlength' : 64,
            },
        },

        'email' : {
            'type'      : 'list',
            'required'  : False,
            'empty'     : True,
            'nullable'  : True,
            'schema'    : {
                'type'      : 'string',
                'empty'     : False,
                'nullable'  : False,
                'maxlength' : 256,
                'regex'     : '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$',
            },
        },
    }

    SCHEMA_RESOURCE = {
        'resources' : {
            'type'      : 'list',
            'required'  : True,
            'empty'     : False,
            'nullable'  : False,
            'schema'    : {
                'type'      : 'dict',
                'schema'    : {
                    'filename' : {
                        'type'      : 'string',
                        'empty'     : False,
                        'nullable'  : False,
                        'maxlength' : 256,
                        'required'  : True,
                    },
                    'mime' : {
                        'type'      : 'string',
                        'empty'     : False,
                        'nullable'  : False,
                        'maxlength' : 128,
                        'required'  : False,
                    },
                    'content' : {
                        # 'anyof_type' : [ 'string', 'bytes' ],  #... for some reason bytes is not known
                        'empty'      : False,
                        'nullable'   : False,
                        'required'   : True,
                    },
                    'for' : {
                        'type'      : 'list',
                        'required'  : True,
                        'empty'     : False,
                        'nullable'  : False,
                        'schema'    : {
                            'type'      : 'string',
                            'empty'     : False,
                            'nullable'  : False,
                            'maxlength' : 16,
                            'allowed'   : list(tCorrType.Id_Couplet().keys()),
                        },
                    },
                },
            },
        },
    }


    def __init__(self):
        """
        Constructor.
        """
        self._pod = None
        self._cfg = None


    def id(self) -> str:
        """
        Pure virtual method, the identifier of the content management overload.

        :return: The overload name.
        """
        raise Exception('id() not implemented.')


    def name(self) -> str:
        """
        Pure virtual method, the name of the content management overload.

        :return: The overload name.
        """
        raise Exception('name() not implemented.')


    def is_deadbeef(self) -> bool:
        """
        Virtual method to check if the interface is active but not configured.

        :return: True if this interface is active but not configure.
        """
        return False


    def _validate_dict(self, schema: dict, inp_data: dict, inp_name: str, req: bool) -> dict:
        """
        Ensure the json data matches the input schema.

        :param schema: The cerberus json schema dictionary to check against.
        :param inp_data: The json data to check.
        :param inp_name: The name of the input argument.
        :param req: Indicate if the input is required.
        :return: The inp_data object for convenience.
        """
        if not inp_data:
            if req:
                raise xLoco('Invalid arg [%s] - %s' % (inp_name, 'May not be null or empty'))

            return inp_data

        val = cerberus.Validator(schema)

        if not val.validate(inp_data):
            raise xLoco('Invalid arg [%s] - %s' % (inp_name, val.errors))

        return inp_data
