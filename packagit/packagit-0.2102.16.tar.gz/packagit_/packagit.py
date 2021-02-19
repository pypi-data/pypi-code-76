#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the packagit project.
#  Please respect the license - more about this in the section (*) below.
#  #
#  packagit is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  #
#  packagit is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  #
#  You should have received a copy of the GNU General Public License
#  along with packagit.  If not, see <http://www.gnu.org/licenses/>.
#  #
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.
import datetime
import shutil


def extract_version(txt):
    """
    Extract version from assignment code.

    Usage:
        >>> extract_version("version = '0.0912.3'")  # major=0 year=09 month=12 minor=3
        '0.0912.3'

    Parameters
    ----------
    txt

    Returns
    -------

    """
    return txt.split(" = ")[1][1:-1]


def update_version(major, previous_version):
    """
    Increment version taking year/month of last commit into account.

    Usage:
        >>> update_version(0, "0.0912.3")  # major=0 year=09 month=12 minor=3
        '0.0912.4'

    Parameters
    ----------
    major
        (new) major version
    previous_version
        versioning scheme: major.YYMM.minor

    Returns
    -------

    """
    import git

    # Doctest fake repo. Version "0.0912.3" is the example from doctest.
    if previous_version == "0.0912.3":
        git.Repo.init("/run/shm/packagit-remote")
        obj = git.Repo.init("/run/shm/packagit")
        obj.index.commit('Initial commit', commit_date=datetime.date(2009, 12, 1).strftime('%Y-%m-%d %H:%M:%S'))
        obj.create_remote("origin", "/run/shm/packagit-remote")
    else:  # pragma: no cover
        obj = git.Repo()

    d = obj.head.object.committed_datetime
    minor = int(previous_version.split(".")[2]) + 1
    version= f"{major}.{str(d.year - 2000).rjust(2, '0')}{str(d.month).rjust(2, '0')}.{minor}"

    # Doctest cleanup.
    if previous_version == "0.0912.3":
        shutil.rmtree("/run/shm/packagit-remote")
        shutil.rmtree("/run/shm/packagit")

    return version


def create_tag(version):  # pragma: no cover
    """    Create tag.    """
    import git
    obj = git.Repo()
    tag = f"v{version}"
    if tag in obj.tags:  # pragma: no cover
        raise Exception(f"Tag {tag} already exists!")
    obj.index.add('setup.py')
    obj.index.commit('Release')
    obj.create_tag(tag, message=obj.head.object.message)
    obj.remotes.origin.push()
    obj.remotes.origin.push(tag)
    return tag
