"""Provides the VaultFile class."""

from pathlib import Path
from typing import Dict, Generator, List, Optional, Union

from attr import Factory, attrib, attrs
from cryptography.fernet import Fernet, InvalidToken
from msgpack import dumps, loads

EntriesType = Dict[str, Union[bytes, List[bytes]]]


class IncorrectVaultKey(Exception):
    """The wrong key was given, and the file cannot be decrypted."""


@attrs(auto_attribs=True)
class VaultFile:
    """A class for restoring hidden files.

    This class is used for loading files hidden by the ``earwax vault``
    command.

    Most of the time, you want to create instances with the
    :meth:`~earwax.VaultFile.from_path` constructor.

    To add files, use the :meth:`~earwax.VaultFile.add_path` method.

    :ivar ~earwax.VaultFile.entries: The files which you are saving.

        The format of this dictionary is ``{label: data}``, where ``data`` is
        the contents of the file you added.

        Labels don't necessarily have to be the names of the files they
        represent. They can be whatever you like.
    """

    entries: EntriesType = attrib(default=Factory(dict), repr=False)

    @classmethod
    def from_path(cls, filename: Path, key: bytes) -> 'VaultFile':
        """Load a series of files and return a ``VaultFile`` instance.

        Given a path to a data file, and the *correct* key, load a series of
        files and return a ``VaultFile`` instance.

        If the key is invalid, :class:`earwax.InvalidFaultKey` will be raised.

        :param filename: The name of the file to load.

            This *must* be a data file, generated by a previous call to
            :meth:`earwax.VaultFile.save`, not a yaml file as created by the
            ``earwax vault new`` command.

        :param key: The decryption key for the given file.
        """
        with filename.open('rb') as f:
            data: bytes = f.read()
        fernet: Fernet = Fernet(key)
        try:
            data = fernet.decrypt(data)
        except InvalidToken:
            raise IncorrectVaultKey(filename)
        entries: EntriesType = loads(data)
        return VaultFile(entries=entries)

    def save(self, filename: Path, key: bytes) -> None:
        """Save this instance's entries to a file.

        :path filename: The data file to save to.

            The contents of this file will be encrypted with the given key, and
            will be binary.

        :param key: The key to use to encrypt the data.

            This key must either have been generated by
            ``cryptography.fernet.Fernet.generate_key``, or be of the correct
            format.
        """
        data: bytes = dumps(self.entries)
        fernet: Fernet = Fernet(key)
        data = fernet.encrypt(data)
        with filename.open('wb') as f:
            f.write(data)

    def add_path(
        self, p: Union[Path, Generator[Path, None, None]],
        label: Optional[str] = None
    ) -> str:
        """Add a file or files to this vault.

        This method will add the contents of the given file to the
        :attr:`~earwax.VaultFile.entries` dictionary, using the given label as
        the key.

        :param p: The path to load.

            If the provided value is a generator, the resulting dictionary
            value will be a list of the contents of every file in that
            iterator.

            If the provided value is a directory, then the resulting dictionary
            value will be a list of every file (not subdirectory) in that
            directory.

        :param label: The label that will be given to this entry.

            This value will be the key in the :attr:`~earwax.VaultFile.entries`
            dictionary.

            If ``None`` is provided, a string representation of the path will
            be used.

            If ``None`` is given, and the ``p`` is not a single ``Path``
            instance, ``RuntimeError`` will be raised.
        """
        if label is None:
            if isinstance(p, Path):
                label = str(p)
            else:
                raise RuntimeError(
                    f'Cannot infer label from {p}: Object is not a path.'
                )
        if isinstance(p, Path):
            if p.is_file():
                with p.open('rb') as f:
                    self.entries[label] = f.read()
            elif p.is_dir():
                p = p.iterdir()
                return self.add_path(p, label=label)
            else:
                raise RuntimeError(
                    f'Cannot handle {p!r}: Not a file or directory.'
                )
        else:
            files: List[bytes] = []
            child: Path
            for child in p:
                if child.is_dir():
                    continue
                with child.open('rb') as f:
                    files.append(f.read())
            self.entries[label] = files
        return label
