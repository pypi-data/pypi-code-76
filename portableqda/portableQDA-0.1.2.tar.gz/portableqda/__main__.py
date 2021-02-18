"""
Copyright 2021 Leandro Batlle

portableQDA is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import portableqda

def main():
    import logging, sys
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    portableqda.log.addHandler(handler)
    portableqda.log.setLevel(logging.DEBUG)

    codebook=portableqda.codebookCls(output="codebook_sample.qdc")
    codebook.writeQdcFile()

if __name__ == "__main__":
    main()