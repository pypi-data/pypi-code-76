"""The :mod:`unimatrix.const` module declares all constants defined by the
Unimatrix framework.
"""
import os
import tempfile


# Specifies the default database connection. If
# ``DB_CONNECTION`` is ``None``, then it is up
# to the implementation to decide.
DB_CONNECTION = os.getenv('DB_CONNECTION')

RUNDIR = os.getenv('APP_RUNDIR', '/opt/app')

LIBDIR = os.getenv('APP_LIBDIR',
    os.path.join(RUNDIR, 'lib'))

PKIDIR = os.getenv('APP_PKIDIR',
    os.path.join(RUNDIR, 'pki'))

SECDIR = os.getenv('APP_SECDIR',
    '/var/run/secrets/unimatrixone.io')

# Instructs all implementation code to make sure that
# TLS is used with network connections, if possible.
TLS_ENFORCE = not os.getenv('DISABLE_TLS_ENFORCE') == '1'

TMPDIR = tempfile.gettempdir()

VARDIR = os.getenv('APP_VARDIR', '/var/lib/app')
