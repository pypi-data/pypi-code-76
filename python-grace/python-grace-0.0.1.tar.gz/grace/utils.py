"""Utility functions."""

import difflib
import filecmp
import hashlib
import os
import shutil
import urllib.request
import uuid
from pathlib import Path
from typing import Optional, Sequence

import appdirs
import patch

DEFAULT_IGNORE_PATTERNS = ("**/*.log", "**/*.o", "**/*.swp")

_cache_path: Optional[Path] = None


def get_cache_path() -> Path:
    """Return the cache path."""
    global _cache_path

    if _cache_path is None:
        # If $PYTHON_GRACE_CACHE_DIR is set, then use it.
        # Otherwise, use an OS-dependent cache directory.
        cache_dir = os.getenv("PYTHON_GRACE_CACHE_DIR")
        if not cache_dir:
            cache_dir = str(appdirs.user_cache_dir("python-grace"))
        _cache_path = Path(cache_dir)

    return _cache_path


def download_file(url: str, sha256: str) -> Path:
    """Download a file and return the path of the downloaded file."""
    # Check if the cache exists.

    url_hash = hashlib.sha256(url.encode()).hexdigest()

    cache_file = (
        get_cache_path() / "downloads" / url_hash[:2] / url_hash / Path(url).name
    )

    if not cache_file.exists():
        # Download the file contents.

        url_lower = url.lower()
        if not (url_lower.startswith("http:") or url_lower.startswith("https:")):
            raise ValueError("forbidden URL scheme: {url}")

        with urllib.request.urlopen(url) as f:  # noqa: S310  # only http/https
            data = f.read()

        # Use the "write-new-then-rename" idiom.

        temp_file = cache_file.parent / (cache_file.name + f".tmp{uuid.uuid4()}")

        temp_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with temp_file.open("wb") as f:
                f.write(data)

            os.replace(temp_file, cache_file)
        finally:
            if temp_file.exists():
                temp_file.unlink()

    # Check the sha256 hash of the downloaded file.

    file_hash = hashlib.sha256()

    with cache_file.open("rb") as f:
        while True:
            chunk = f.read(2048 * file_hash.block_size)
            if len(chunk) == 0:
                break
            file_hash.update(chunk)

    actual_sha256 = file_hash.hexdigest()
    if actual_sha256 != sha256:
        raise RuntimeError(
            f"wrong sha256 for file {cache_file} downloaded from {url},"
            f" expected: {sha256}, actual: {actual_sha256}"
        )

    return cache_file


def download_archive(
    url: str,
    sha256: str,
    extract_dir: Path,
    *,
    normalize_newlines: bool = False,
    patch_dir: Optional[Path] = None,
) -> Path:
    """Download an archive file and extract it to the given directory."""
    url_name = Path(url).name.lower()

    archive_suffixes = [
        ".tar.bz2",
        ".tar.gz",
        ".tar.xz",
        ".tar",
        ".tbz",
        ".tgz",
        ".zip",
    ]

    if any(url_name.endswith(suffix) for suffix in archive_suffixes):
        cache_file = download_file(url, sha256)

        temp_dir = extract_dir.parent / (extract_dir.name + f".tmp{uuid.uuid4()}")

        temp_dir.mkdir(parents=True, exist_ok=False)
        try:
            shutil.unpack_archive(
                os.fspath(cache_file), extract_dir=os.fspath(temp_dir)
            )  # fspath for python<3.7

            temp_root_dir = temp_dir
            while True:
                items = list(temp_root_dir.iterdir())
                if len(items) == 1 and items[0].is_dir():
                    temp_root_dir = items[0]
                else:
                    break

            move_tree(temp_root_dir, extract_dir)
        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    else:
        raise ValueError(f"{url} does not look like an archive file")

    if normalize_newlines:
        normalize_newlines_intree(extract_dir)

    if patch_dir:
        apply_patch(extract_dir, patch_dir)

    return extract_dir


def move_tree(src_dir: Path, dest_dir: Path) -> Path:
    """Move an entire directory tree to another."""
    if not src_dir.is_dir():
        raise ValueError(f"directory {src_dir} does not exist")
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.move(str(src_dir), str(dest_dir))  # str(...) for Python < 3.9
    return dest_dir


def normalize_newlines_intext(text: str) -> str:
    """Normalize new lines in the given text."""
    # This corresponds to:
    #   end_of_line = lf
    #   insert_final_newline = true
    #   trim_trailing_whitespace = true
    text = "\n".join(line.rstrip() for line in text.splitlines())
    if text and text[-1] != "\n":
        text += "\n"
    return text


def normalize_newlines_intree(target_dir: Path) -> None:
    """Normalize new lines in text files in an entire directory tree."""
    for path in target_dir.iterdir():
        if path.is_dir():
            normalize_newlines_intree(path)
            continue

        try:
            # We expect reading binary files or non-UTF8 files fails.
            text1 = path.read_text()
            text2 = normalize_newlines_intext(text1)

            if text1 != text2:
                path.write_text(text2)
        except UnicodeDecodeError:
            pass


def make_patch(
    original_dir: Path,
    changed_dir: Path,
    patch_dir: Path,
    *,
    ignore_patterns: Optional[Sequence[str]] = None,
    normalize_newlines: bool = False,
) -> None:
    """Generate a patch set."""
    if normalize_newlines:
        normalize = normalize_newlines_intext
    else:

        def normalize(text: str) -> str:
            return text

    def make_patch_file(relative_path: Path) -> None:
        file1 = original_dir / relative_path
        file2 = changed_dir / relative_path

        def do_patch_file() -> None:
            if filecmp.cmp(file1, file2):
                return

            patch_file = patch_dir / relative_path
            patch_file = patch_file.parent / f"{patch_file.name}.patch"

            lines1 = normalize(file1.read_text()).splitlines(keepends=True)
            lines2 = normalize(file2.read_text()).splitlines(keepends=True)

            diffs = list(
                difflib.unified_diff(
                    lines1,
                    lines2,
                    str(Path("a") / relative_path),
                    str(Path("b") / relative_path),
                )
            )

            if not diffs:
                return

            patch_file.parent.mkdir(parents=True, exist_ok=True)
            patch_file.write_text("".join(diffs))

        def do_new_file() -> None:
            patch_file = patch_dir / relative_path
            patch_file = patch_file.parent / patch_file.name

            patch_file.parent.mkdir(parents=True, exist_ok=True)
            patch_file.write_text(normalize(file2.read_text()))

        if file1.is_file():
            if file2.is_file():
                do_patch_file()
                return

        if not file1.exists():
            if file2.is_file():
                do_new_file()
                return

        raise RuntimeError(f"diff between {file1} and {file2} not supported")

    # Ensure that the patch directory is empty.

    if patch_dir.exists():
        shutil.rmtree(patch_dir)
    patch_dir.mkdir(parents=True)

    # Collect all files in the two directories.

    if ignore_patterns:
        ignore_patterns = DEFAULT_IGNORE_PATTERNS + tuple(ignore_patterns)
    else:
        ignore_patterns = DEFAULT_IGNORE_PATTERNS

    items = [
        path.relative_to(original_dir)
        for path in original_dir.glob("**/*")
        if path.is_file()
        and all(not path.match(pattern) for pattern in ignore_patterns)
    ] + [
        path.relative_to(changed_dir)
        for path in changed_dir.glob("**/*")
        if path.is_file()
        and all(not path.match(pattern) for pattern in ignore_patterns)
    ]

    # Generate a patch for each file.

    for relative_path in set(items):
        make_patch_file(relative_path)


def apply_patch(target_dir: Path, patch_dir: Path) -> None:
    """Apply a patch set."""
    # Copy all new files.
    ignore_patterns = DEFAULT_IGNORE_PATTERNS + ("**/*.patch",)
    new_files = [
        path
        for path in patch_dir.glob("**/*")
        if path.is_file()
        and all(not path.match(pattern) for pattern in ignore_patterns)
    ]
    for new_file in new_files:
        target_file = target_dir / new_file.relative_to(patch_dir)
        target_file = target_file.parent / target_file.name
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(new_file, target_file)

    # Apply all patch files.
    patch_files = patch_dir.glob("**/*.patch")
    for patch_file in patch_files:
        patch_set = patch.fromfile(patch_file)
        if not patch_set:
            raise RuntimeError(f"failed to load {patch_file}")
        if not patch_set.apply(strip=0, root=target_dir):
            raise RuntimeError(f"failed apply {patch_file}")


def remove_files(target_dir: Path, pattern: str) -> None:
    """Delete files matched with a glob pattern in a directory tree."""
    for path in target_dir.glob(pattern):
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def copy_files(src_dir: Path, dest_dir: Path, pattern: str) -> None:
    """Copy files matched with a glob pattern in a directory tree to another."""
    for src in src_dir.glob(pattern):
        dest = dest_dir / src.relative_to(src_dir)
        if src.is_dir():
            copy_files(src, dest, "*")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
