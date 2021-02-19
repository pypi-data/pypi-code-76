

import os
from subprocess import check_output
from microapp.utils import tostr

def xmlquery(casedir, *vargs):

    cmd = [os.path.join(casedir, "xmlquery"), *vargs]
    stdout = check_output(cmd, cwd=casedir)
    return tostr(stdout)
