from textwrap import dedent

from sh.contrib import git

from pristine_lfs import do_commit


def test_pristine_lfs_commit(fake_tarball):
    repo, tarball, size, sha = fake_tarball

    do_commit(tarball.open('rb'), branch='pristine-lfs')
    do_commit(tarball.open('rb'), branch='pristine-lfs', message='blip %s %s %s')
    do_commit(tarball.open('rb'), branch='pristine-lfs', message='blip')

    # verify the file has indeed been committed
    commit = git('rev-parse', 'pristine-lfs^{tree}').strip('\n')
    pointer = git('cat-file', 'blob', f"{commit}:{tarball.name}")
    assert pointer == dedent(
        f"""
        version https://git-lfs.github.com/spec/v1
        oid sha256:{sha}
        size {size}
        """).lstrip('\n'), 'Object pointer doesn’t match the object'

    stored = repo / '.git' / 'lfs' / 'objects' / sha[:2] / sha[2:4] / sha
    assert stored.is_file(), 'Object has not been stored by LFS'
