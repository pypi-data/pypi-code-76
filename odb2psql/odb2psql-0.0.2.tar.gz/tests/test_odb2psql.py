import os
import shutil
import pytest
import tempfile
from odb2psql import to_psql

@pytest.fixture
def src(request):
    return 'peminjamanbuku.odb'

# @pytest.mark.usefixtures('src')
def test_yo(src):
    #test preparation
    dir_path = os.path.dirname(os.path.realpath(__file__))
    odbpath = os.path.join(dir_path, src)
    assert os.path.exists(odbpath)

    #candidate for feature
    tempdir = tempfile.TemporaryDirectory()
    zipfile = os.path.join(tempdir.name, 'temp.zip')

    shutil.copyfile(odbpath, zipfile)
    shutil.unpack_archive(zipfile, tempdir.name)
    shutil.unpack_archive(zipfile, r'd:\temp')


    shutil.move(os.path.join(tempdir.name, 'database', 'backup'),
                os.path.join(tempdir.name, 'database', 'db.backup')
                )

    shutil.move(os.path.join(tempdir.name, 'database', 'data'),
                os.path.join(tempdir.name, 'database', 'db.data')
                )

    shutil.move(os.path.join(tempdir.name, 'database', 'properties'),
                os.path.join(tempdir.name, 'database', 'db.properties')
                )

    shutil.move(os.path.join(tempdir.name, 'database', 'script'),
                os.path.join(tempdir.name, 'database', 'script')
                )

    #prepartion complete, next: connection

