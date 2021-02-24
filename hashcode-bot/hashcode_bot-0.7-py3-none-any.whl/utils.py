import zipfile


def mkdir(base, path):
    path = base.joinpath(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def iterfiles(path):
    for p in path.iterdir():
        if p.is_dir():
            yield from iterfiles(p)
        elif p.is_file():
            yield p


def archive_dir(fh, dir_path):
    with zipfile.ZipFile(fh, "w") as zip:
        for file in iterfiles(dir_path):
            relpath = file.relative_to(dir_path)
            # TODO: Base this on gitignore
            if relpath.parts[0] in {".git", ".direnv", "__pycache__"}:
                continue
            zip.write(file, arcname=relpath)


def find_in_ancestor(path, filename):
    path = path.joinpath(filename)
    for path in path.parents:
        if path.joinpath(filename).exists():
            return path
        path = path.parent
    raise ValueError("No ancestore contains the file")
