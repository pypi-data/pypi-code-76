"""
Platform-specific functions, particularly ones with different import requirements
"""

import os
import sys

if sys.platform == 'ios':
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    import console

    def quicklook(path):
        console.quicklook(path)

elif sys.platform == 'darwin':
    def quicklook(path):
        os.system('qlmanage -p %r 2&>/dev/null' % path)
