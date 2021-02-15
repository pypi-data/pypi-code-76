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

"""
LOCO Template upload/download batch class.
"""

import os.path
import json
import yaml

from bs_lib  import Pod
from bs_lib  import common

import bs_loco

from bs_loco.db.tables import tNoTempl


class BatchUploadDownloadTemplate:
    """
    Provides a class that can be easily used to upload or download correspondence templates files into and
    out of the database.
    """

    def __init__(self, pod: Pod, dao_name: str):
        """
        Constructor

        :param pod: The pod to use.
        :param dao_name: The dao objects to use.
        """
        self._pod = pod
        self._log = pod.log
        self._dao = bs_loco.dao_by_name(dao_name)


    def download_template(self, templ_id: str, fmt: str = 'yaml', dest_filename: str = None) -> None:
        """
        Download the loco template to a yaml file.

        :param templ_name: The template id to download (see the `notempl` table).
        :param fmt: Download the file in either `json` or `yaml` format. The default is `yaml`.
        :param dest_filename: Optionally specifiy the destination file name, if left empty uses the the
                              template name.
        """
        notype    = self._dao.dNoType(self._pod.dbcon)
        templ_qry = self._dao.dNoTemplByNoType(self._pod.dbcon)

        if not notype.try_select_one_deft(templ_id):
            raise Exception('Loco Type not found. [id:%s]' % (templ_id))

        out_pl = {
            'id'  : templ_id,
        }

        templ_qry.exec_deft(templ_id, '')

        while templ_qry.fetch():
            if not templ_qry.orec.templ:
                continue

            out_pl[templ_qry.orec.corrtype_id] = templ_qry.orec.templ


        if dest_filename:
            fname = dest_filename
        else:
            fname = f'{templ_id}.{fmt}'

        with open(fname, 'wt') as fh:
            if fmt == 'json':
                fh.write(json.dumps(out_pl))
            else:
                fh.write(yaml.safe_dump(out_pl))

        self._log.info(f' - downloaded template [file: {fname}] ok')


    def upload_template(self, path_to_templ: str) -> None:
        """
        Upload a yaml or json template file.

        :param path_to_templ: The path to the json or yaml template file to upload.
        """
        if not os.path.exists(path_to_templ):
            raise Exception('File not found [%s]' % (path_to_templ))

        data      = common.read_config_dict_from_file(path_to_templ)
        templ_id  = common.read_dict(data, 'id',    str)
        notype    = self._dao.dNoType(self._pod.dbcon)
        ct_qry    = self._dao.dCorrProvSelectAll(self._pod.dbcon)
        no_templ  = self._dao.dNoTemplBy(self._pod.dbcon)
        mod_by    = '[bs_loco.BatchUploadDownloadTemplate]'
        ucnt      = 0

        if not notype.try_select_one_deft(templ_id):
            raise Exception('Loco Type not found. [id:%s]' % (templ_id))

        ct_qry.exec()

        while ct_qry.fetch():
            ct_data = common.read_dict(data, ct_qry.orec.id, dict, optional=True)

            # TODO, validate the schema of this dictionary, will need to pull in cerebrus parser.

            if not ct_data:
                continue

            # TODO, update the `notemplcfg` table with the old schema if it changed

            if no_templ.try_select_one_deft(templ_id, ct_qry.orec.id):
                no_templ.rec.status      = tNoTempl.Status_Couplet.key_active
                no_templ.rec.templ       = ct_data
                no_templ.rec.modified_by = mod_by
                no_templ.update()

                self._log.info(f' - uploaded template [notype_id: {no_templ.rec.notype_id},'
                               ' corrtype_id: {no_templ.rec.corrtype_id}] ok')

            else:
                no_templ.insert_deft(templ_id,
                                     ct_qry.orec.id,
                                     tNoTempl.Status_Couplet.key_active,
                                     None,
                                     ct_data,
                                     None,
                                     mod_by)

                self._log.info(f' - inserted template [notype_id: {no_templ.rec.notype_id},'
                               ' corrtype_id: {no_templ.rec.corrtype_id}] ok')

            ucnt += 1

        if not ucnt:
            self.log.warning(' - no valid correspondence types configured for upload in file, aborting.')
            return

        self._log.info(f' - uploaded template [file: {path_to_templ}] ok')

        self._pod.dbcon.commit()
