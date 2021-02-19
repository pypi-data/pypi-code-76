""" Helper tools which are used by other modules """
import hashlib

import ssdeep


def _hexdigest(hash_object):
    if hasattr(hash_object, "hexdigest"):
        return hash_object.hexdigest()

    return hash_object.digest()


def get_hashes(path, blocksize=4096, hash_types=None):
    """
    Calculates the MD5, SHA1, SHA256 and SHA512 hashes of a given file

    :param path:
    :param blocksize:
    :return:
    """
    hashes = {
        "md5": hashlib.md5(),
        "sha1": hashlib.sha1(),
        "sha256": hashlib.sha256(),
        "sha512": hashlib.sha512(),
        "ssdeep": ssdeep.Hash(),
    }

    if hash_types is None:
        hash_types = {"sha512"}

    with open(path, "rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(blocksize), b""):
            for algo in hash_types:
                hashes[algo].update(chunk)

    return {hash_type: _hexdigest(hashes[hash_type]) for hash_type in hash_types}
